from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = '12345'



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    


    def __init__(self, title, body):
        self.title = title
        self.body = body

        self.created = datetime.utcnow()
    
    
    def is_valid(self):
        if self.title and self.body and self.created:
            return True
        else:
            return False


@app.route('/')
def index():
    return redirect('/blog')

#signup route-validate/verify 

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        exist = User.query.filter_by(username=username).first()

        username_error = ""
        password_error = ""
        verify_error = ""

        if username == "":
            username_error = "Please enter a username."
        elif len(username) <= 3 or len(username) > 20:
            username_error = "Username must be between 3 and 20 characters long."
        elif " " in username:
            username_error = "Username cannot contain any spaces."
        if password == "":
            password_error = "Please enter a password."
        elif len(password) <= 3:
            password_error = "Password must be greater than 3 characters long."
        elif " " in password:
            password_error = "Password cannot contain any spaces."
        if password != verify or verify == "":
            verify_error = "Passwords do not match."
        if exist:
            username_error = "Username already taken."
        # If fields are good, continue to creating session with new username and password.
        if len(username) > 3 and len(password) > 3 and password == verify and not exist:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('signup.html',
            username=username,
            username_error=username_error,
            password_error=password_error,
            verify_error=verify_error
            )

    return render_template('signup.html')

#login route-validate/verify user info in database

@app.route('/login', methods=['POST', 'GET'])


#index route-redirects to home



#route to main blog page
@app.route('/blog')
def blog_index():

    blog_id = request.args.get('id')
    blogs = Blog.query.all()

    if blog_id:
        post = Blog.query.get(blog_id)
        blog_title = post.title
        blog_body = post.body
        # Use Case 1: Click on a blog entry's title on the main page and go to a blog's individual entry page.
        return render_template('entry.html', title="Blog Entry #" + blog_id, blog_title=blog_title, blog_body=blog_body)
            
   #TODO - Sort post request from newest to oldest         
    sort = request.args.get('sort')

    if (sort=="newest"):
        blogs = Blog.query.order_by(Blog.created.desc()).all()
    elif (sort=="oldest"):
        blogs = Blog.query.order_by(Blog.created.asc()).all()
    else:
        blogs = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", blogs=blogs)      

#handler route to new post page.
@app.route('/post')
def new_post():
    return render_template('post.html', title ="Add New Blog Entry")

#handler route ot validate post title and body fields
@app.route('/post', methods=['POST'])
def verify_post():
    blog_title = request.form['title']
    blog_body = request.form['body']
    title_error = ''
    body_error = ''

    #error validation messages if blog/title is empty return error text.
    if blog_title == "":
        title_error = "Title required"
    if blog_body == "":
        body_error = "Content required"

    # add new blog post and commit it to table with new id.
    if not title_error and not body_error:
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        blog = new_blog.id
        # Use Case 2: After adding a new blog post, instead of going back to the main page, we go to that blog post's individual enrty page. Redirect to specific blog id page.
        return redirect('/blog?id={0}'.format(blog))
    else:
        # return user to post page with errors.
        return render_template('post.html', title="Add New Blog Entry", blog_title=blog_title, blog_body=blog_body, title_error = title_error, body_error=body_error)


if __name__ == '__main__':
    app.run()