from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from html.parser import HTMLParser
from flask_wtf import FlaskForm

from wtforms import TextField, SubmitField, StringField
from wtforms.validators import DataRequired
# initializing app
app = Flask(__name__)

# App configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notebook.sqlite3'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"

#initializing sessions
Session(app)
# initializing db
db = SQLAlchemy(app)



#db stuff
class Posts(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(30), nullable = False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable = False)
    perma = db.Column(db.Text, nullable=False)

    def __init__(self, date, title, content,perma):
        self.date = date
        self.title = title
        self.content = content
        self.perma = perma

    def __repr__(self):
        return f"note('id:{self.id}', date:{self.date}, content:{self.content}, permalink:{self.perma})"

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    link_text = db.Column(db.String(80), unique=True,nullable=False)
    link = db.Column(db.Text, unique=False,nullable=False)

    def __init__(self, link_text, link):
        self.link_text = link_text
        self.link = link
    
    def __repr__(self):
        return f"link('id:{self.id}', link_text:{self.link_text}, link:{self.link})"


#PARSING HTML

class para_parser(HTMLParser):
    def handle_data(self, data):
        return data

# class searchForm(Form):
#     query = StringField('Search')
#     submit = SubmitField('Search')

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextField("Post", validators=[DataRequired()])
    submit = SubmitField("Save")

# SESSIONS:

# ROUTING




# Default route 
@app.route("/")
def index():
    if not session.get('username') or not session.get('password'):
        return render_template('homepage.html')
    return redirect('/all-posts')

@app.route('/status', methods = ['GET','POST'])
def status():
    if request.method == "POST":
        username = request.form.get("username")     
        session['username'] = username
        password = request.form.get("password")
        session['password'] = password

    return render_template('status.html', USERNAME= username, PASSWORD = password)


# adding notes or entries
@app.route('/add')
def add():
    if session.get('username') and session.get('password'):
        return render_template('add.html')
    else:
        return redirect('/')



@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        now = datetime.now()
        date = now.strftime("%B %d, %Y %H:%M")
        title = request.form.get('title')
        content = request.form.get('content')
        perma = request.form.get('permalink')
        # posting form data into database.
        post = Posts(date, title, content, perma)
        db.session.add(post)
        db.session.commit()
        
        print("Post is saved in db")
        
        return render_template('posts.html', TITLE = title, CONTENT = content, DATE = date, PERMA = perma)

    
    
# logging in
@app.route('/login')
def login():
    return render_template('login.html')

# showing status of entry after save
@app.route('/posts/edit/<permalink>', methods=['GET', 'POST'])
def editor(permalink):
    print(f"permalink is: "+permalink)
    e_posts = Posts.query.filter_by(perma=permalink).first()
    # print(f"epost is : "+ e_posts.content)
    if request.method == "POST":
        e_posts.date = datetime.now().strftime("%B %d, %Y, %H:%M")
        e_posts.title = request.form.get('title')
        e_posts.perma = request.form.get('perma')
        e_posts.content = request.form.get('content')
        # db.session.add(e_posts)
        db.session.commit()
        return url_for('results')
    return render_template('edit_post.html', TITLE = e_posts.title, CONTENT = e_posts.content, PERMA = e_posts.perma)
          

@app.route('/editpost')
def edit_post():
    return render_template('add.html')

@app.route('/all-posts')
def allposts():
    if not session.get("username") or not session.get("password"):
        return redirect('/')
    entries =Posts.query.all()
    return render_template('allposts.html', entries = entries)

@app.route('/posts/<permalink>', methods=['GET','POST'])
def showpost(permalink):
    requested_post = Posts.query.filter_by(perma=permalink).first()
    return render_template('post.html', REQUESTEDPOST = requested_post)

@app.route('/results', methods=['GET','POST'])
def results():
    if request.method == 'POST':
        query = request.form.get('query')
        result = Posts.query.filter(Posts.title.like(f'%{query}%')).all()
        session['result']=result
        session['query'] = query
        return redirect(url_for('results'))
    else:
        return render_template('search_results.html', results = session.get('result'), query= session.get('query'))


@app.route('/important_links', methods=['GET','POST'])
def important_links():
    links = None
    msg = None
    if request.method == 'POST':
        l_text = request.form.get('l_text')
        link = request.form.get('link')
        print(l_text, link)
        # adding to db
        link = Link(l_text, link)
        db.session.add(link)
        db.session.commit()
        msg = "Link added Successfully!"

    return render_template('important_links.html', message = msg, links = Link.query.all())



@app.route('/add_link', methods=[ 'GET', 'POST'])
def add_link():
    return render_template('add_link.html')

@app.route('/delete_link/<link_id>', methods=['GET','POST'])
def delete_link(link_id):
    Link.query.filter_by(link_text = link_id).delete()
    db.session.commit()
    return redirect(url_for('important_links'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)