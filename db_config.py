from flaskext.mysql import MySQL
from main import app

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ticket_mngt'

app.secret_key = 'ticket_manager'

mysql.init_app(app)
