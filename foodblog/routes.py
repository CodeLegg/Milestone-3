import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, flash, redirect, request
from foodblog import app, db, bcrypt
from foodblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from foodblog.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Mike Legg',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Feb 01, 2023'
    },
      {
        'author': 'Mel Lowth',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Feb 02, 2023'
    }

]

# HOME PAGE
@app.route('/')
def home():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('home.html', image_file=image_file, posts = posts)

# MEALS PAGE
@app.route('/meals')
@login_required
def meals():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('meals.html', image_file=image_file, title='Meals')

# RECEIPES PAGE
@app.route('/receipes')
@login_required
def receipes():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('receipes.html', image_file=image_file, title='Receipes')

# COOKING TIPS PAGE
@app.route('/cooking_tips')
@login_required
def cooking_tips():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('cooking_tips.html', image_file=image_file, title='Cooking Tips')

# DISCUSSION PAGE
@app.route('/discussion')
@login_required
def discussion():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('discussion.html', image_file=image_file, title='Discussion')

# SIGN UP/REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, favorite_food=form.favorite_food.data )
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

# LOGIN PAGE
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

# LOGOUT PAGE
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
   

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) 
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)
    return picture_fn

# LAYOUT/SITE NAVBAR & CONTENT
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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

# LAYOUT/SITE NAVBAR & CONTENT
@app.route("/layout")
def layout():
    return render_template('layout.html')

# LAYOUT/SITE NAVBAR & CONTENT
@app.route("/post/new")
@login_required
def new_post():
    return render_template('create_post.html', image_file=image_file, title='New Post')
