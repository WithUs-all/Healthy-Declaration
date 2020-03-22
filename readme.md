1. Please install all needed python packages.
    windows: pip install -r requirements.txt
    linux: (sudo) pip3 install -r requirements.txt

2. Please create database.
3. please create tables by model classes using command line in project directory.
    python(or python3)
    >> from app import db
    >> db.create_all()
2. Please set all config info in config.py
    DB_USERNAME : database username
    DB_PASSWORD : database password
    DB_HOST : database server address
    DB_PORT : database port
    DB_NAME : database name

3. Please run flask server.
    (after entering into project folder)
        windows: python app.py
        linux: (sudo) python3 app.py
Now that's all! please input localhost:5000 in browser and then you can see this project home page.