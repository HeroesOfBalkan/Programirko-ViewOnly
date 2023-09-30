    ## IMPORTS

import os
from importlib.resources import path
from random import randrange
from datetime import timedelta
from re import U
from flask import Flask, url_for, render_template, flash, redirect, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy

import local_modules as lm





    ## FUNCTIONS

def generate_code():
    secret = ""
    for _ in range(0, 10):
        secret += (chr(randrange(48, 90)))
    return secret





    ## SETTINGS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "nuh uh!"
app.secret_key = generate_code()
app.permanent_session_lifetime = timedelta(days = 3)

db = SQLAlchemy(app)





    ## DATABASES

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key = True)
    username = db.Column("username", db.String(17), unique = True, nullable = False)
    password = db.Column("pass", db.String(17), nullable = False)
    l_plan = db.Column("l_plan", db.Text, default = "free")
    pre_knowledge = db.Column("pre_knowledge", db.Text, default = "beginenr")
    interests = db.Column("interests", db.ARRAY(db.Text))

    def __init__(self, username, password, l_plan, pre_knowledge, interests):
        self.username = username
        self.password = password
        self.l_plan = l_plan
        self.pre_knowledge = pre_knowledge
        self.interests = interests



class Recommend(db.Model):
    __tablename__ = "recommend"

    id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.Text, nullable = False)
    tag = db.Column("tag", db.Text, nullable = False)
    relations = db.Column("relations", db.ARRAY(db.Text))

    def __init__(self, name, tag, relations):
        self.name = name
        self.tag = tag
        self.relations = relations





    ## ROUTING

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = session["user"] if "user" in session else ""
    return render_template("index.html", usr = user)



@app.route("/login", methods = ["POST", "GET"])
def login():
    user = session["user"] if "user" in session else ""
    if user != "":
        return redirect("/")

    if request.method == "POST":
        un = request.form["username"]
        pas = request.form["password"]

        q = Users.query.filter_by(username = un).first()
        print(q)
        if ( (q is None) or (q.password != pas) ):
            flash("Netačno korisničko ime ili lozinka")
        else:
            session["user"] = un
            return redirect("/")

    return render_template("login.html", usr = user)



@app.route("/logout")
def logout():
    user = session["user"] if "user" in session else ""
    if user != "":
        session.pop("user", None)
    return redirect("/")



@app.route("/register", methods = ["POST", "GET"])
def register():
    user = session["user"] if "user" in session else ""
    if user != "": return redirect("/")
    
    if request.method == "POST":
        pas = request.form["password"]
        rpas = request.form["repeat_pw"]

        if rpas != pas:
            flash("Pogrešno potvrđena lozinka (ne podudaraju se)", "error")
        else:
            un = request.form["username"]
            q = Users.query.filter_by(username = un).first()

            if q is not None:
                flash("Korisničko ime već postoji. Izaberite neko drugo.", "error")
            else:
                lp = request.form["learning_plan"]
                know = request.form["pre_knowledge"]
                inter = request.form.getlist("interests")

                put = Users(un, pas, lp, know, inter)
                db.session.add(put)
                db.session.commit()

                to_login = request.form.getlist("to_login_prompt")  # get info either to log in ("True") or not (empty)
                if len(to_login):
                    session["user"] = un
                    user = session["user"]
                else:
                    user = ""

                # redirect(url_for("user"), usr = user)

    return render_template("register.html", usr = user)



@app.route("/user", methods = ["GET", "POST"])
def user():
    user = session["user"] if "user" in session else ""

    # Make sure no non-logged in user doesn't access it
    if user == "": return "<h1>Access denied!</h1><p>You have no privileges to access the content.<br>Reason: You are not logged in</p>", 401

    q = Users.query.filter_by(username = user).first()
    print(q.interests)

    if request.method == "POST":
        c_pas = request.form["check_password"]
        if c_pas != q.password:
            flash("Pogrešna lozinka", "error")

        else:
            try:
                un = request.form["username"]
                q.username = un
            except Exception as e:
                print(e)

            try:
                n_pas = request.form["new_password"]
                r_n_pas = request.form["repeat_npw"]
                if n_pas != "" and n_pas == r_n_pas:
                    q.password = n_pas
                else: flash("Resetovanje lozinke nije uspelo: ne podudaraju se.", "error")
            except Exception as e:
                print(e)

            try:
                lp = request.form["learning_plan"]
                q.l_plan = lp
            except Exception as e:
                print(e)

            try:
                know = request.form["pre_knowledge"]
                q.pre_knowledge = know
            except Exception as e:
                print(e)

            try:
                inter = request.form.getlist("interests")
                q.interests = inter
            except Exception as e:
                print(e)

            db.session.commit()


    return render_template("user.html", usr = user, intrs = q.interests, knw = q.pre_knowledge)





@app.route("/lessons")
def lessons():
    user = session["user"] if "user" in session else ""
    return render_template("lessonpage.html", usr = user)


@app.route("/cheatsheets")
def cheatsheets():
    user = session["user"] if "user" in session else ""
    return render_template("cheatsheets.html", usr = user)





@app.route("/editor")
def editor():
    user = session["user"] if "user" in session else ""
    return render_template("editor.html", usr = user)





@app.route("/videos")
@app.route("/videos/")
def video_main():
    user = session["user"] if "user" in session else ""

    return render_template("videosmain.html", usr = user, watch = "")



@app.route("/videos/<video_id>")
def watch(video_id):
    user = session["user"] if "user" in session else ""

    to_watch = lm.youtube_video(video_id)

    return render_template("videosmain.html", usr = user, watch = to_watch)





    ## API/FETCH Routes

@app.route("/yts/<wish>")
def srch(wish):
    bro = lm.youtube_search(wish)
    return jsonify(bro)
    



@app.route("/recm")
def recm():
    user = session["user"] if "user" in session else ""

    # Make sure client will have recommendations
    if "recommendations" not in session:

        q = Users.query.filter_by(username = user).first()
        inters = q.interests if q != None else []
        if (len(inters) < 5):
            lackin = 5 - len(inters)

            from random import randrange
            for _ in range(0, lackin):
                r = Recommend.query.all()
                inters.append(r[randrange(0, len(r))].name)


        elif (len(inters) > 5):
            from random import randrange
            x = []
            for _ in range(0, 5):
                x.append( inters[randrange(0, len(inters))] )
            inters = x

        session["recommendations"] = inters


    return jsonify(session["recommendations"])



@app.route("/recm_list")
def recms():
    result = []

    recommendations = session["recommendations"] if "recommendations" in session else ["Flask", "Vue", "Django", "Web Development", "Postgres"]

    for recommend in recommendations:
        item = lm.youtube_search(recommend)
        result.append(item)

    return jsonify(result)





    ## START

if __name__ == "__main__":
    db.create_all()
    app.run()
