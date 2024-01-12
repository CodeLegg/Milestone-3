import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, flash, redirect, request, abort
from foodblog import app, db, bcrypt
from foodblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, ReplyForm, DeleteCommentForm
from foodblog.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required

def get_image_file():
    """Helper function to get the image file URL based on user authentication."""
    if current_user.is_authenticated:
        return url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        return None

@app.route('/')
def home():
    return render_template('home.html', image_file=get_image_file())

@app.route('/meals')
@login_required
def meals():
    return render_template('meals.html', image_file=get_image_file(), title='Meals')

@app.route('/receipes')
@login_required
def receipes():
    return render_template('receipes.html', image_file=get_image_file(), title='Receipes')



@app.route('/discussion')
@login_required
def discussion():
    posts = Post.query.all()
    return render_template('discussion.html', image_file=get_image_file(), title='Discussion', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, favorite_food=form.favorite_food.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check Username Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)

    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.png':
        os.remove(prev_picture)
    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.favorite_food = form.favorite_food.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.favorite_food.data = current_user.favorite_food
    image_file = get_image_file()
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

@app.route("/layout")
def layout():
    return render_template('layout.html')

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    image_file = get_image_file()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('discussion'))
    return render_template('create_post.html', image_file=image_file, form=form, title='New Post', legend='New Post')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    image_file = get_image_file()

    comments = Comment.query.filter_by(post_id=post.id, parent_comment_id=None).all()

    comment_form = CommentForm()
    reply_form = ReplyForm()

    if request.method == 'POST':
        if 'parent_comment_id' in request.form:
            # This is a reply
            parent_comment_id = int(request.form['parent_comment_id'])
            parent_comment = Comment.query.get_or_404(parent_comment_id)

            if reply_form.validate_on_submit():
                reply = Comment(content=reply_form.content.data, user_id=current_user.id, post=post, parent_comment=parent_comment)
                db.session.add(reply)
                db.session.commit()
                flash('Your reply has been posted!', 'success')
                return redirect(url_for('post', post_id=post.id))
        else:
            # This is a comment
            if comment_form.validate_on_submit():
                comment = Comment(content=comment_form.content.data, user_id=current_user.id, post=post)
                db.session.add(comment)
                db.session.commit()
                flash('Your comment has been posted!', 'success')
                return redirect(url_for('post', post_id=post.id))

    return render_template('post.html', post=post, comments=comments, comment_form=comment_form, reply_form=reply_form, image_file=image_file)

@app.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Check if the current user is the author of the comment
    if current_user != comment.author:
        abort(403)

    # Detach the comment from the session before deletion
    db.session.expunge(comment)    

    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')

    # Redirect back to the post page
    return redirect(url_for('post', post_id=comment.post_id))





@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        flash('Your post has been updated!', 'success')
        return redirect(url_for('discussion'))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    image_file = get_image_file()
    return render_template('create_post.html', image_file=image_file, form=form, title='Update Post', legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('discussion'))
