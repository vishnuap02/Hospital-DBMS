# from flask import Flask, render_template
import pymysql

# app = Flask(__name__)

# Space also effects the values in string given below.
def connection():
    s = '127.0.0.1'
    d = 'hospital'
    u = 'root'
    p = 'Vishnuap@02'
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn

def search(placename):
    hosps=[]
    conn = connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM HOSPITALS WHERE CITY = '+placename +';')
    for row in cursor.fetchall():
        hosps.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    print(hosps)
    return hosps
