from flask import Flask, render_template, request, redirect, url_for, session
import re
import db_manage

app = Flask(__name__)
app.secret_key = ""


@app.route('/search', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'placename' in request.form:
     placen = request.form["placename"]
     placename = '"'+ placen + '"'
     account = db_manage.search(placename)
     print(account)
    return render_template("search.html")


@app.route('/displayresults')
def displayresults():
    if 'loggedin' in session:
        account = db_manage.search()
        account1 = account[0]
        return render_template("displayresults.html",dict=account1)
    return redirect(url_for('search'))

@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)