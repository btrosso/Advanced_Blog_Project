import os
import smtplib
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
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

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        phone_number = request.form["phoneNumber"]
        message = request.form["message"]
        success_message = "Successfully sent your message"

        # send the message via smtp
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=os.environ["MY_EMAIL"], password=os.environ["EMAIL_PASSWORD"])
            connection.sendmail(
                from_addr=os.environ["MY_EMAIL"],
                to_addrs="riseandgrind2020@yahoo.com",
                msg="Subject:New Message\n\n"
                    f"Name: {name}\n"
                    f"Email:{email}\n"
                    f"Phone Number:{phone_number}\n"
                    f"Message:{message}")
        print(name)
        print(email)
        print(phone_number)
        print(message)
        return render_template("contact.html", success_message=success_message)
    else:
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

