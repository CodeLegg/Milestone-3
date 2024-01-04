from flask import render_template, url_for, request, flash, redirect
from foodblog import app
from foodblog.forms import RegistrationForm, LoginForm
from foodblog.models import User, Post, Comment

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
@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

# MEALS PAGE
@app.route('/meals')
def meals():
    return render_template('meals.html', title='BiteBurst - Meals')

# RECEIPES PAGE
@app.route('/receipes')
def receipes():
    return render_template('receipes.html', title='BiteBurst - Receipes')

# COOKING TIPS PAGE
@app.route('/cooking_tips')
def cooking_tips():
    return render_template('cooking_tips.html', title='BiteBurst - Cooking Tips')

# DISCUSSION PAGE
@app.route('/discussion')
def discussion():
    return render_template('discussion.html', title='BiteBurst - Discussion')

# SIGN UP/REGISTER PAGE
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        if form.username.data == 'CodeLegg' and form.email.data == 'CodeLegg@gmail.com' and form.password.data == 'Password12!':
            flash(f"You've Succsessfly Logged In {form.username.data}!", 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# LAYOUT/SITE NAVBAR & CONTENT
@app.route("/layout")
def layout():
    return render_template('layout.html')
