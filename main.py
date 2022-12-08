"""
Adam Richmond - submission to Save the Children Skills Assessment
December 2022
"""

import os
import boto3
import mysql.connector
from flask_bootstrap import Bootstrap4
from flask import Flask, render_template
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap4(app)


@app.route("/")
def site():
    img_filename = 'Logo_SavetheChildren.png'
    get_image_from_s3(img_filename)
    img_file = os.path.join('static', img_filename)
    return render_template("site.html", image=img_file)


def get_image_from_s3(img_filename):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name="eu-west-2"
    )
    s3.download_file(
        Bucket="adamr-stc-filestore",
        Key=img_filename,
        Filename=f"static/{img_filename}",
    )


@app.route("/get_data", methods=["GET"])
def get_data():
    mydb = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        port=3306,
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
    )
    cursor = mydb.cursor()
    cursor.execute("use web_data;")
    cursor.execute("select * from stc_statistics;")
    data = cursor.fetchall()
    data_json = reformat_data(data)
    return data_json


def reformat_data(data):
    data_json = {i: {} for i in range(len(data))}
    for i, row in enumerate(data):
        row_json = {
            "group": row[0],
            "value": row[1],
            "info": row[2],
        }
        data_json[i] = row_json
    return data_json
