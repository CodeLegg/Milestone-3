from flask import render_template, url_for, request, flash, redirect, request
from foodblog import app, db, bcrypt
from foodblog.forms import RegistrationForm, LoginForm
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
    return render_template('home.html', posts = posts)

# MEALS PAGE
@app.route('/meals')
@login_required
def meals():
    return render_template('meals.html', title='Meals')

# RECEIPES PAGE
@app.route('/receipes')
@login_required
def receipes():
    return render_template('receipes.html', title='Receipes')

# COOKING TIPS PAGE
@app.route('/cooking_tips')
@login_required
def cooking_tips():
    return render_template('cooking_tips.html', title='Cooking Tips')

# DISCUSSION PAGE
@app.route('/discussion')
@login_required
def discussion():
    return render_template('discussion.html', title='Discussion')

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
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check Username Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)

# LOGOUT PAGE
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
   

# LAYOUT/SITE NAVBAR & CONTENT
@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title='Profile')

# LAYOUT/SITE NAVBAR & CONTENT
@app.route("/layout")
def layout():
    return render_template('layout.html')
