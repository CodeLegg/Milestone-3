from flask import Flask, render_template, url_for, request, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY'] = '4567bfpahg309bndh357hfpsba245'

csrf = CSRFProtect(app)
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

@app.route('/home')
def home():
    return render_template('home.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html', title='')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/layout")
def layout():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)