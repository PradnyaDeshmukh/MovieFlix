from flask import Flask, render_template, session, redirect, request
from functools import wraps
from flask_mail import Mail, Message
import pymongo
from passlib.hash import pbkdf2_sha256



app = Flask(__name__)
app.secret_key = 'movieflix'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USE_TSL=False,
    MAIL_USERNAME='dpradnya757@gmail.com',
    MAIL_PASSWORD='Pradnu@59'
)
mail = Mail(app)

client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system
# count = db.movieDetails.objects.all()
# print("No of documnets: ", count)

collection = db.movieDetails
cursor = list(collection.find({}))
print("type",type(cursor))
# for document in cursor:
#     print(document)
print(cursor[0]['image'])


from user.models import User, Kartik, Movie

@app.route('/user/signup/', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout/')
def signout():
    return User().signout()

@app.route('/user/login/', methods=['POST'])
def login():
    return User().login()

@app.route('/forget_pass/', methods=['POST'])
def forPass():
    return User().forget_password()

@app.route('/reset/', methods=['GET'])
def reset():
    email = request.args.get("email")
    print("line 45",email)
    return User().re_in(email)

@app.route('/reset_pass/', methods=['POST'])
def reset_pass():
    return User().reset()

@app.route('/update/', methods=['GET'])
def update():
    return render_template("update.html")

@app.route('/update_profile/',methods=['POST'])
def update_profile():
    return User().updateProfile()
        
@app.route('/movie_details/<movieName>')
def movie_details(movieName):
    print("line no 73"+movieName)
    return Movie().movieDetails(movieName)  

@app.route('/search/', methods=['POST'])
def search():
    if request.method=='POST':
        m_name=request.form.get('movie_name')
        return Movie().movieDetails(m_name)  

@app.route('/review/', methods=['POST'])
def review():
    return Movie().review()

@app.route('/genre/<gtype>', methods=['GET'])
def genere(gtype):
    return Movie().genere(gtype)

@app.route('/mylist/<movieName>')
def mylist(movieName):
   
    return Movie().addMovie(movieName) 

@app.route('/display_mylist/')
def DisplayList():
    return Movie().display_list()

@app.route('/delete/')
def delete():
    return User().delete()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

@app.route('/')
def home():
    return render_template('login.html') 

@app.route('/signup/')
def signup_form():
    return render_template("register.html")

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('frontpage.html',details=cursor)

@app.route("/contact/")
def contact():
    return render_template("contact.html")





if __name__ == "__main__":
    app.run(debug=True)