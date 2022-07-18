from flask import Flask, jsonify, request, session, redirect, flash
import uuid
from flask.templating import render_template
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import redirect
import bcrypt
from flask_mail import Mail, Message


Re_email = ""
class Kartik:
    email = ""
    # movieName = ""
    def __init__(self,email):
        Kartik.email=email
        print("Kartk class", Kartik.email)

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        obj = Kartik(user['email'])
        flash("you are successfuly logged in", "success")
        return jsonify(user), 200

    def signup(self):


        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "phn": request.form.get('phn')
        }

        # encrypt password
        user['password'] = bcrypt.hashpw((user['password']).encode('utf-8'),bcrypt.gensalt())
        print(user['password'])
        from app import db
        #check for existing email
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({"error":"Email address already in use"}), 400

       
        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({ "error": "Signup failed" }), 400

    def signout(self):
        session.clear()
        flash("you are signed out", "success")
        return redirect('/')

    def login(self):


        from app import db
        user = db.users.find_one({
            "email": request.form.get('email')
        })
        new_pass = bcrypt.hashpw(request.form.get('password').encode('utf-8'),bcrypt.gensalt())
    
        
        if user and (bcrypt.checkpw(request.form.get('password').encode('utf-8'), user['password'])):
            return self.start_session(user)

        return jsonify({"error": "Invalid Credentials" }), 401


    def forget_password(self):
        user = { 'email': request.form.get('email') }
        print("forget"+user['email'])
        from app import mail, db
        if db.users.find_one({ "email": user['email'] }):
            msg = Message('Hello',
                sender ='dpradnya757@gmail.com',
                recipients = [user['email']]
               )
            msg.body = "Here you can set you new password http://127.0.0.1:5000/reset/?email="+user['email']
            mail.send(msg)
            return jsonify({"success": "Mail sent" }), 200
        
        return jsonify({"error": "Pls reenter email" }), 401

    def re_in(self,email):
        abc = Kartik(email)
        return render_template("reset.html")

    def reset(self):
        from app import db
        print("Kartik email in rese"+Kartik.email)
        user = { 'password': request.form.get('pass1') }
        print("line 82"+user['password'])
        user['password'] = bcrypt.hashpw((user['password']).encode('utf-8'),bcrypt.gensalt())
        print(user['password'])
        db.users.find_one_and_update({"email":Kartik.email},{"$set" :{'password':user['password']}})
        return jsonify({"success": "Updated" }), 200

    
    def updateProfile(self):
        from app import db
        user = {
            "name": request.form.get('Profile_Name'),
            "password": request.form.get('password'),
            "C_pass": request.form.get('C_pass'),
            "phn": request.form.get('phn')
        }
        if(user['password']!=user['C_pass']):
             return jsonify({"error": "Password not matching" }), 401 
        user['password'] = bcrypt.hashpw((user['password']).encode('utf-8'),bcrypt.gensalt())
        
        db.users.find_one_and_update({ "email": Kartik.email },{"$set":{"name":user['name'],"phn":user['phn'],"password":user['password']}})
        flash("Profile updated successfuly", "success")
        
        return jsonify({"success": "Updated" }), 200
        
    
    def delete(self):
        from app import db
        if db.users.delete_one({ "email": Kartik.email }):
            return redirect('/') 
        else:
            return jsonify({"error": "Cant delete" }), 401

        


class MName:
    movieName = ""
    def __init__(self,movieName):
        MName.movieName=movieName
        print("mname1",MName.movieName)


class Movie:

    def movieDetails(self,movieName):
        print("line 140", movieName)
        from app import db
        obj1 = MName(movieName)
        print("mname",obj1.movieName)

        # obj.MName(movieName)
        movie = db.movieDetails.find_one({
            "Name": movieName
        })
        if db.movieDetails.find_one({"Name": movieName}):
            # print(movie)
            return render_template("movie.html",Movie=movie)
        else:
            return jsonify({"error":"Movie not found"}), 401


    def review(self):
        from app import db
        review = str(request.form.get('review'))
        print(review)
        db.movieDetails.find_one_and_update({ "Name": MName.movieName },{"$push":{"review":review}})
        movie = db.movieDetails.find_one({
            "Name": MName.movieName     
        })
        
        flash("Review added successfuly", "success")
        return render_template("movie.html",Movie=movie)

    def genere(self, gtype):
        from app import db
        cursor = list(db.movieDetails.find({ "genere": gtype }))
        # movie_list = db.movieDetails.find({ "genere": gtype })
        print(cursor)

        return render_template("genere.html",Title=gtype, Movielist=cursor)


    def addMovie(self, moviename):
        print("Kartik email in rese"+Kartik.email)
        from app import db
        if(db.myList.find_one_and_update({"email":Kartik.email},{"$push" :{'list':moviename}})):
            flash("Movie added to list successfuly", "success")
        else:
            data = {
                'email':Kartik.email,
                'list':[moviename]
            }
            db.myList.insert_one(data)
            flash("Movie added to list successfuly", "success") 
        return redirect('/dashboard/')

    def display_list(self):
        from app import db
        cursor = list(db.myList.find({ "email": Kartik.email }))
        # movie_list = db.movieDetails.find({ "genere": gtype })
        print(cursor)
        # user = list(db.myList.find({ "email": Kartik.email }))
        print("line 196",cursor)
        return render_template('mylist.html', movie_list=cursor)
            








        