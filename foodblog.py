from flask import Flask, render_template
app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template('home.html', posts = posts)

@app.route("/")
def about():
    return render_template('about.html')

@app.route("/")
def layout():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)