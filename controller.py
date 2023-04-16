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
      
    
class loginAPI(Resource):
    def post(self):
        try:
            if 'username' in request.form and 'password' in request.form:
                username = request.form['username']
                password = request.form['password']
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute("select * from users where username = %s and password = %s",(username,password))
                userData = cur.fetchone()
                cur.close()
                if userData:
                    session['loggedin'] = True
                    session['username'] = userData['username']
                    message = "Logged In successfully"
                    return redirect(url_for('dashboard'))
                else:
                    message = "Please enter correct username/password"
                    return redirect(url_for('login',message =message))
            else:
                return redirect(url_for('login'))
        except Exception as e:
            print(e)
    def get(self):
        try:
            if request.args.get('message'):
                message = request.args.get('message')
                return make_response(render_template('login.html',message =message))
            else:    
                return make_response(render_template('login.html'))
        except Exception as e:
            print(e)
           
class logout(Resource):
    def get(self):
        try:
            session.pop('loggedin',None)
            session.pop('username',None)
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            
            
class createTicket(Resource):
    def get(self):
        try:
            if 'loggedin' in session:
                return make_response(render_template('ticket.html'))
            else:
                return make_response(render_template('login.html'))
        except Exception as e:
            print(e)            

 class tickets(Resource):
    def get(self):
        try:
            message = 'redirect to tickets'
            username = session['username']
            if 'loggedin' in session:
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                if request.args.get('ticketId'):
                    try:
                        ticketId = request.args.get('ticketId')
                        cur.execute("select * from tickets where id = %s", (ticketId))
                        ticketwithId = cur.fetchone()
                        if ticketwithId:
                            message = "Fetch ticket with ticketId =" + ticketId
                            cur.execute("select * from ticket_history where ticket_id = %s order by createdAt desc ",
                                        (ticketId))
                            ticketHis = cur.fetchall()
                            cur.close()
                            print(ticketHis)
                            return make_response(
                                render_template('ticket-view.html', ticketDetails=ticketwithId, ticketHistory=ticketHis,
                                                username=username))
                        else:
                            message = "TicketId not found"
                            return make_response(
                                render_template('ticket-view.html', ticketDetails=ticketwithId, username=username))
                        print(ticketwithId)
                    except Exception as e:
                        print(e)
                else:
                    cur.execute("select * from tickets")
                    tickets = cur.fetchall()
                    cur.close()
                    message = "Fetch All Tickets"
                    return make_response(render_template('ticket-list.html', ticketDetails=tickets, username=username))
            else:
                message = 'User not login'
                return make_response(render_template('login.html'))
        except Exception as e:
            print(e)
            
          
def post(self):
        try:
            if 'loggedin' in session:
                username = session['username']
                if 'id' in request.form:
                    id = request.form['id']
                    description = request.form['description']
                    status = request.form['status']
                    print(status)
                    if status == 'Closed':
                        isActive = 0
                    else:
                        isActive = 1
                    conn = mysql.connect()
                    cur = conn.cursor(pymysql.cursors.DictCursor)
                    cur.execute("update tickets set status=%s,\
                                isActive=%s where id= %s",
                                (status, isActive, (int(id))))
                    cur.execute("insert into ticket_history (ticket_id,remark,status,updatedBy) values (%s ,%s,%s,%s)", \
                                (id, description, status, session['username']))
                    conn.commit()
                    cur.close()
                    print("values are updated")
                    return redirect(url_for('tickets', ticketId=id, username=username))
                else:
                    print("POST")
                    title = request.form['title']
                    description = request.form['description']
                    customer_name = request.form['customer_name']
                    customer_phone = request.form['customer_phone']
                    customer_email = request.form['customer_email']
                    status = 'New'
                    isActive = 1
                    try:
                        conn = mysql.connect()
                        cur = conn.cursor(pymysql.cursors.DictCursor)
                        cur.execute(
                            "insert into tickets (title,description,customer_name,customer_phone,customer_email,status,isActive) values (%s ,%s,%s,%s,%s,%s,%s)", \
                            (title, description, customer_name, customer_phone, customer_email, status, isActive))
                        last_row = cur.lastrowid
                        cur.execute("select * from tickets where id = %s", (last_row))
                        print(cur.fetchone())
                        cur.execute(
                            "insert into ticket_history (ticket_id,remark,status,updatedBy) values (%s ,%s,%s,%s)", \
                            (last_row, description, status, customer_name))
                        conn.commit()
                        cur.close()
                    except Exception as e:
                        print(e)
                    message = "New Ticket Added"
                    return redirect(url_for('dashboard', username=username))
            else:
                message = 'User not login'
                return make_response(render_template('login.html'))
        except Exception as e:
            print(e)

    def delete(self):
        try:
            message='redirect to tickets'
            if 'loggedin' in session:
                username = session['username']
                print(request.form)
                id = request.form['id']
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute("delete from tickets where id = %s",(int(id)))
                cur.execute("delete from ticket_history where ticket_id = %s",(int(id)))
                conn.commit()
                cur.close()
                print("values are inserted")
                message = "Ticket deleted"
                return True
            else:
                message = 'User not login'
                return False
        except Exception as e:
            print(e)            
