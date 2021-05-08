from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

@app.route('/get/<string:var>')
def _get(var):
    return "GET" + var

@app.route('/temp')
def _temp():
    name = "Shounak"
    return render_template('index.html',n1=name)

@app.route('/url')
def url():
    return redirect(url_for('_temp'))



if __name__=="__main__":
    app.run()