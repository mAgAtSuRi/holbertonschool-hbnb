#!/usr/bin/python3
from app import create_app

app = create_app("development")
if __name__ == '__main__':
    print("DEBUG =", app.config["DEBUG"])
    print("DB URI =", app.config["SQLALCHEMY_DATABASE_URI"])
    app.run()
    