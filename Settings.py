from flask import Flask,jsonify,Request,Response,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType
from flask_migrate import Migrate
from werkzeug.security import check_password_hash,generate_password_hash
# from flask_mail import Mail, Message
from datetime import date,datetime,timedelta
from functools import wraps
import jwt
import pandas as pd
import uuid
import time
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import calendar
import numpy as np











app = Flask(__name__)

scheduler = BackgroundScheduler(daemon=True)
scheduler=APScheduler()
# 1c238f7da0e686c58f6d0ed9d9939715
app.config["SECRET_KEY"] = "1c238f7da0e686c58f6d0ed9d9939715"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345@localhost/fin_tech"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



CORS(app)
db = SQLAlchemy(app)
migrate=Migrate(app,db)










def reference_number():
    random_number=str(uuid.uuid4().fields[-1])[:9]
    return int(random_number)




def get_rows(sequence, num):
    count = 1
    rows = list()
    cols = list()
    for item in sequence:
        if count == num:
            cols.append(item)
            rows.append(cols)
            cols = list()
            count = 1
        else:
            cols.append(item)
            count += 1
    if count > 0:
        rows.append(cols)
    return rows


# calendar.setfirstweekday(6)

def get_week_of_month(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x==day)[0][0] + 1
    return(week_of_month)



def find_age(year,month,day):
    dob=date(year,month,day)
    today=datetime.today()
    age=today.year-dob.year-((today.month,today.day)<(dob.month,dob.day))
    return age