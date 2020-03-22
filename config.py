import os

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'healthdeclaration'
DB_HOST = 'localhost'
DB_PORT = '3306'

MAIL_SERVER = 'smtp-relay.sendinblue.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'mrbs@hybotic.com'
MAIL_PASSWORD = '3BhFbZXPMxdROKEj'

def db_url():
    return 'mysql+pymysql://root:root@localhost:3306/healthdeclaration'
