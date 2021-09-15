from typing import NewType
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import send_from_directory
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.before_first_request
def create_table():
    db.create_all()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    print('here')
    if request.method == "POST":
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=request.form.get('password')
        )

        db.session.add(new_user)
        db.session.commit()

        return render_template("secrets.html",user_name=new_user.name)

    return render_template("register.html")


@app.route('/swag')
def swag():
    print('here')
    return {'a': 1}


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'cheat_sheet.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
