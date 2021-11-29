import os
#import pathlib
import boto3
from flask import Flask
from flask import request
from flask import redirect
from datetime import datetime


app = Flask(__name__)

CLIENT = boto3.client(
    "s3",
    region_name= 'us-east-2',
)



#FRONT_PATH = pathlib.Path("/front/code").absolute()


#@app.route("/", methods=["GET"])
#def get_form():
#    with open(FRONT_PATH / "index.html") as page_file:
#        return page_file.read()


@app.route("/save_to_s3", methods=["POST"])
def save_to_s3():
    data = (request.form["subject"] + "\n\n" + request.form["message"]).encode("utf-8")
    CLIENT.put_object(
        **{
            "Body": data,
            "Bucket": 'my-test-musorka',
            "Key": datetime.utcnow().strftime("%Y/%m/%d/%H%M%S.txt"),
        }
    )
    return redirect("/")


