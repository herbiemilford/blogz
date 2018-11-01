from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import flask_SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:beproductive:localhost8889/build-a-blog'
app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)
app.secret_key = '12345'





if __name__ == '__main__':
    app.run()