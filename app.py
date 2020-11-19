import os
import mysql.connector


db_user = os.environ.get("DB_MYSQL_USER")
db_pass = os.environ.get("DB_MYSQL_PASS")

mydb = mysql.connector.connect(
    host="localhost",
    user=db_user,
    passwd=db_pass
)


print(mydb)