import os

DB_USERNAME = 'dbusername'
DB_PASSWORD = 'dbpassword'
DB_NAME = 'dbname'
DB_HOST = 'dbhost'
DB_PORT = '3306'

MAIL_SERVER = 'smtp-relay.sendinblue.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'myemail.com'
MAIL_PASSWORD = 'myemail password'

def db_url():
    return 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME
