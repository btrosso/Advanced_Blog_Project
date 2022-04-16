import requests
from dotenv import load_dotenv
from flask import Flask, render_template
load_dotenv()

app = Flask(__name__)
BLOG_DATA = {}

@app.route('/')
def home_page():
    global BLOG_DATA
    blog_url = "https://api.npoint.io/7e3ecf77ba150ea6865d"
    all_blogs = requests.get(blog_url).json()
    BLOG_DATA = all_blogs
    return render_template("index.html", all_blogs=all_blogs)

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/contact')
def contact_page():
    return render_template("contact.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in BLOG_DATA:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)

