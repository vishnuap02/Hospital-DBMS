import requests.cookies
from flask import *
import dbmsHosps as db

app = Flask(__name__)

app.secret_key = 'Vishnuap@02'

@app.route('/')
def index():
    totalbeds=[]
    bedtypes = ["ICUBEDS","GENWARDBEDS","OPETHEATER"]
    ndocs = db.totalcount('DOCTORS')
    nhosps = db.totalcount('HOSPITALS')
    for beds in bedtypes:
      totalbeds.append(db.totalValuecount('HOSPITALS',beds))
    return render_template("index.html",ndocs=ndocs,nhosps=nhosps,total_types=zip(totalbeds,bedtypes))


@app.route('/search',methods =['POST','GET'])
def search():
    if request.method == "POST":
        placename = request.form['placename']
        beds = request.form.get('beds')
        hosps = db.displayresults(placename,beds)
        total = db.countresults('HOSPITALS',placename)
        return render_template("search.html",hosps=hosps,total=int(total[0]))
    return render_template("search.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        id = request.form['id']
        password = request.form['password']
        hosps = db.loginfetch('HOSPITALS',id,password)
        if hosps:
            session['loggedin'] = True
            session['id'] = hosps[0]
            session['username'] = hosps[1]
            msg = 'Logged in successfully !'
            return render_template('login.html', msg=msg,idno=session['id'])
    msg = "Enter Correct details"
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/update')
def update():
    return render_template('update.html')


@app.route('/display',methods=['POST','GET'])
def display():
    if 'loggedin' in session:
        hosps = db.displayelements(session['id'])
        print(session['id'])
        print(hosps)
        return render_template("display.html",hosps=hosps,id=session['id'])
    return render_template('display.html')

@app.route('/doctorreg',methods=['POST','GET'])
def doctorreg():
    msg=''
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form and 'fname' in request.form and 'lname' in request.form and 'rating' in request.form and 'spl' in request.form and 'experience' in request.form:
        id = request.form['id']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        rating=  request.form['rating']
        spl= request.form['spl']
        experience= request.form['experience']
        msg = db.doctorregister(id,password,fname,lname ,rating,spl,experience)
    else :
        msg = 'Please fill out form properly .!'
    return render_template('doctorreg.html',msg=msg)

@app.route('/doctorlogin',methods=['POST','GET'])
def doctorlogin():
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        id = request.form['id']
        password = request.form['password']
        print(id,password)
        docts = db.loginfetch('DOCTORS',id,password)
        if docts:
            session['loggedin'] = True
            session['id'] = docts[0]
            msg = 'Logged in successfully !'
            return render_template('doctorlogin.html', docts=docts , loggedin=True)
        return render_template('login.html', loggedin=False)
    msg = "Enter Correct details"
    return render_template('login.html',loggedin=False)

if __name__ == '__main__':
   app.run(debug = True)

# test_request_context() tells Flask to behave as though
# it’s handling a request even while we use a Python shell
# When we use " URL_FOR()" function , the passed argument(string)
# must be same as the Function name u want to use.

# Fuinding difficulty in  need to take palcename from 'search.html ' and give 'personalised'(/<placename>)
# results in 'displaysearch.html' page

# problem in '/search' , not entering if condition method=["POST]

# https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data
# The GET method is used to request data from specified resources .
# GET method the data sent by the server is appended to the URL of the page .
# "Hey server, I want to get this resource." In this case, the browser sends an empty body.
# Because the body is empty, if a form is sent using this method the data sent to the server is appended to the URL.
# The data is appended to the URL as a series of name/value pairs. After the URL web address has ended,
# we include a question mark (?) followed by the name/value pairs, each one separated by an ampersand (&).
# In this case we are passing two pieces of data to the server:

# The POST method is used to send data to a server to create and update a resource.
# It's the method the browser uses to talk to the server when asking for a response that takes into account
# the data provided in the body of the HTTP request: "Hey server, take a look at this data and
# send me back an appropriate result." If a form is sent using this method, the data is appended to the body of the HTTP request.
# for passwords use 'POST' only.