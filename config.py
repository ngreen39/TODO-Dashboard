
DB_CONFIG = {
    "host": "localhost",        # MySQL server (usually localhost)
    "user": "root",             # MySQL username
    "password": "Birth2011!",# Replace with your MySQL root password
    "database": "TodoDB"        # The database name we will create
}
from config import DB_CONFIG
import pymysql

connection = pymysql.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)

print("Connected to database!")