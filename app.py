from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_pymongo import PyMongo
import bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get/<string:var>')
def _get(var):
    return "GET" + var

@app.route('/session')
def _session():
   
#    CREATE SESSION
    session['name']="shounak"
    print(session)

#   POP SESSION key:value
    # session.pop('name')
    # print(session)

#   CLEAR SESSION
    session.clear()
    print(session)
    return "clear"


@app.route('/temp')
def _temp():
    name = "Shounak"
    return render_template('home.html', n1=name)


@app.route('/url')
def url():
    return redirect(url_for('_temp'))


@app.route('/methods', methods=["GET", "POST"])
def methods():

    if request.method == "POST":

        req = request.json
        name = req['name']
        roll = req['roll']

        return render_template('home.html', name=name, roll=roll)
    else:
        name = "Taha"
        roll = "1213"
        return render_template('home.html', name=name, roll=roll)


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        req = request.form
        # email = req.get('email')
        
        email = req['email']
        pwd = req['password']

        session['email']=email
        print("USER LOGIN IN AS : ",session['email'])

        return "Email : " + email + "Password : " + pwd

    return render_template('login.html')


@app.route('/logout')
def logout():
    
    print("CLEARING SESSION FOR : ",session['email'])
    session.clear()
    return render_template('home.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        # req = request.json
        req = request.form

        fname = req['fname']
        lname = req['lname']
        email = req['email']
        password = req['password']
        user_type = req['user_type']

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        print(hashed_pw)
        
        # mongo.db.user.insert_one(
        #     {
        #         'fname':fname,
        #         'lname': lname,
        #         'email': email,
        #         'type': user_type,
        #         'password': hashed_pw,
        #         'vote_flag' :0
        #     }
        # )

        df = [
            {
            "fname": fname,
            "lname": lname
            },
            {"email": email,
             "password": password
            },
            {"user type": user_type
            }
            ]

        return jsonify(df)

    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)
