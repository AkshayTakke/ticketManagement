from flask import Flask,render_template,request,session,make_response,redirect,url_for
from db_config import mysql
from flask_restful import Resource
import pymysql,sys

class homePage(Resource):
    def get(self):
        return redirect(url_for('login'))

    
class dashboard(Resource):
    def get(self):
        if 'loggedin' in session:
            try:
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute("SELECT count(isActive) as count  FROM tickets where isActive=1;")
                activeCount = cur.fetchall()
                cur.execute("SELECT count(isActive) as count FROM tickets where isActive=0;")
                closeCount = cur.fetchall()
            except Exception as e:
                print(e)
            return make_response(render_template('dashboard.html',countActive = activeCount,countClose = closeCount))
        else:
            return make_response(render_template('login.html'))
