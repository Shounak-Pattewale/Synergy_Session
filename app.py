from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
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

        resp = list(mongo.db.user.find({'email': email}, {'_id':0, 'password':1, 'type':1}))
        print(resp[0]['type'])

        check = bcrypt.checkpw(pwd.encode('utf-8'), resp[0]['password'])

        if check:
            session.clear()
            session['logged_in'] = True
            session['EMAIL'] = email
            session['USERTYPE'] = resp[0]['type']
            flash("Login Successfully!")
            print("User logged in")
            return redirect(url_for('home'))
        else:
            flash("Incorrect EMailID or Password.")
            # print("Error while logging in")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout(): 
    print("CLEARING SESSION FOR : ",session['EMAIL'])
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

        if user_type == 'voter':        
            mongo.db.user.insert_one(
                {
                    'fname': fname,
                    'lname': lname,
                    'email': email,
                    'type': user_type,
                    'password': hashed_pw,
                    'vote_flag' :0
                }
            )
        else:
            mongo.db.user.insert_one(
                {
                    'fname': fname,
                    'lname': lname,
                    'email': email,
                    'type': user_type,
                    'password': hashed_pw,
                    'vote_flag' : 1
                }
            )
            mongo.db.nominee.insert_one(
                {
                    'fname': fname,
                    'lname': lname,
                    'email': email,
                    'type': user_type,
                    'password': hashed_pw,
                    'vote_flag' : 1
                }
            )

        return render_template('login.html')

    return render_template('signup.html')


@app.route('/cast_vote', methods=['GET', 'POST'])
def cast_vote():
    user_type = session['USERTYPE']
    email = session['EMAIL']

    nominees = list(mongo.db.nominee.find({}, {'_id':0, 'fname':1, 'lname':1, 'email':1}))
    user = list(mongo.db.user.find({'email':email}, {'_id':0, 'vote_flag':1}))

    x = []

    flag = user[0]['vote_flag']
    print(flag)

    for i in nominees:
        name = i['fname'] + " " + i['lname']
        email = i['email']
        x.append({'name': name, 'email': email})


    if user_type == 'voter':
        if flag == 1:
            return "You have already casted your vote."
        else:
            return render_template('cast_vote.html', nominees=x)
    
    else:
        return "Nominee cannot cast a Vote"


@app.route('/vote', methods=['POST'])
def vote():
    if request.method == "POST":
        # req = request.json
        req = request.form
        user_email = session['EMAIL']
        nominee_email = req['vote']

        resp = mongo.db.nominee.update_one({'email': nominee_email}, {'$push': {'votes': user_email}})
        user = mongo.db.user.update_one({'email': user_email}, {'$set':{'vote_flag': 1}})

        return "Vote casted!"

    return render_template('cast_vote.html')
        


@app.route('/vote_count')
def vote_count():
    all_ = list(mongo.db.nominee.find({}, {'_id':0, 'votes':1, 'fname':1, 'lname':1}))
    print(all_)
    y = []
    for i in range(len(all_)):
        fn, ln, v = all_[i]['fname'], all_[i]['lname'], len(all_[i]['votes'])
        y.append({'fn':fn, 'ln':ln, 'v':v})
    
    length = len(y)
    return render_template('vote_count.html', vote_count=y, len=length)


if __name__ == "__main__":
    app.run(debug=True)
