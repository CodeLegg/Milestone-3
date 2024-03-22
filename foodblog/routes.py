import os
from flask import render_template, url_for, request, flash, redirect, request, abort
from foodblog import app, db, bcrypt
from foodblog.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    PostForm,
    CommentForm,
    ReplyForm,
    DeleteCommentForm,
)
from foodblog.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/meals")
@login_required
def meals():
    return render_template("meals.html", title="Meals")


@app.route("/receipes")
@login_required
def receipes():
    return render_template("receipes.html", title="Receipes")


@app.route("/discussion")
@login_required
def discussion():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("discussion.html", title="Discussion", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            favorite_food=form.favorite_food.data,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to login", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Sign Up", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(
                f"Login Unsuccessful. Please check Username Email and Password",
                "danger",
            )
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.favorite_food = form.favorite_food.data

        db.session.commit()

        flash("Your account has been updated!", "success")
        return redirect(url_for("profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.favorite_food.data = current_user.favorite_food

    # Paginate user's posts
    posts_page = request.args.get("posts_page", 1, type=int)
    user_posts = current_user.posts.order_by(Post.date_posted.desc()).paginate(
      page=posts_page, per_page=1
    )

    # Paginate user's comments
    comments_page = request.args.get("comments_page", 1, type=int)
    user_comments = current_user.comments.order_by(Comment.date_posted.desc()).paginate(
        page=comments_page, per_page=1
    )

    # # Paginate user's comments
    # comments_per_page = 1  # Adjust this value as needed
    # comments_page = request.args.get("comments_page", 1, type=int)
    # user_comments = Comment.query.filter_by(author=current_user).paginate(
    #     page=comments_page, per_page=comments_per_page, error_out=False
    # )

    return render_template(
        "profile.html",
        title="Profile",
        form=form,
        user_posts=user_posts,
        user_comments=user_comments,
    )


@app.route("/layout")
def layout():
    return render_template("layout.html")


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("discussion"))
    return render_template(
        "create_post.html", form=form, title="New Post", legend="New Post"
    )


@app.route("/latest_post", methods=["GET"])
def latest_post():
    latest_post = Post.query.order_by(Post.id.desc()).first()
    if latest_post:
        return redirect(url_for("post", post_id=latest_post.id))
    else:
        # Handle the case where there are no posts
        flash("No posts available.", "warning")
        return redirect(url_for("discussion"))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)

    comments = (
        Comment.query.filter_by(post_id=post.id, parent_comment_id=None)
        .order_by(Comment.date_posted.desc())
        .all()
    )

    comment_form = CommentForm()
    reply_form = ReplyForm()

    if request.method == "POST":
        if "parent_comment_id" in request.form:
            # This is a reply
            parent_comment_id = int(request.form["parent_comment_id"])
            parent_comment = Comment.query.get_or_404(parent_comment_id)

            if reply_form.validate_on_submit():
                reply = Comment(
                    content=reply_form.content.data,
                    user_id=current_user.id,
                    post=post,
                    parent_comment=parent_comment,
                )
                db.session.add(reply)
                db.session.commit()
                flash("Your reply has been posted!", "success")
                return redirect(url_for("post", post_id=post.id))
        else:
            # This is a comment
            if comment_form.validate_on_submit():
                comment = Comment(
                    content=comment_form.content.data,
                    user_id=current_user.id,
                    post=post,
                )
                db.session.add(comment)
                db.session.commit()
                flash("Your comment has been posted!", "success")
                return redirect(url_for("post", post_id=post.id))

    return render_template(
        "post.html",
        post=post,
        comments=comments,
        comment_form=comment_form,
        reply_form=reply_form,
    )


@app.route("/comment/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    user_comment = Comment.query.get_or_404(comment_id)

    # Check if the current user is the author of the comment
    if current_user != user_comment.author:
        abort(403)

    # Detach the comment from the session before deletion
    db.session.expunge(user_comment)

    db.session.delete(user_comment)
    db.session.commit()
    flash("Your comment has been deleted!", "success")

    # Redirect back to the post page
    return redirect(url_for("post", post_id=user_comment.post_id))


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("discussion"))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "create_post.html", form=form, title="Update Post", legend="Update Post"
    )


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("discussion"))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_posts.html", posts=posts, user=user)


# RECEIPE PAGES


@app.route("/card1")
@login_required
def card1():
    return render_template("card1.html", title="Fish Receipe")


@app.route("/card2")
@login_required
def card2():
    return render_template("card2.html", title="Chicken Receipe")


@app.route("/card3")
@login_required
def card3():
    return render_template("card3.html", title="Chinese Receipe")


@app.route("/card4")
@login_required
def card4():
    return render_template("card4.html", title="Taco Receipe")


@app.route("/card5")
@login_required
def card5():
    return render_template("card5.html", title="Sweet Treat Receipe")


@app.route("/card6")
@login_required
def card6():
    return render_template("card6.html", title="Baking Receipe")


@app.route("/card7")
@login_required
def card7():
    return render_template("card7.html", title="Sweet Treat Receipe")


@app.route("/card8")
@login_required
def card8():
    return render_template("card8.html", title="Meat Receipe")


@app.route("/card9")
@login_required
def card9():
    return render_template("card9.html", title="Baking Receipe")


@app.route("/card10")
@login_required
def card10():
    return render_template("card10.html", title="Chicken Receipe")


@app.route("/card11")
@login_required
def card11():
    return render_template("card11.html", title="Chicken Receipe")


@app.route("/card12")
@login_required
def card12():
    return render_template("card12.html", title="Pasta Receipe")
