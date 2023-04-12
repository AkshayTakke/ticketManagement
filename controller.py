from flask import Flask,render_template,request,session,make_response,redirect,url_for
from db_config import mysql
from flask_restful import Resource
import pymysql,sys

class homePage(Resource):
    def get(self):
        return redirect(url_for('login'))
