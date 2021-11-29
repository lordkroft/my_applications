import os
import boto3
from flask import Flask
from flask import request
from flask import redirect
from datetime import datetime


app = Flask(__name__)

CLIENT = boto3.client(
    "s3",
    region_name= 'us-east-2'
)


PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S3 Form</title>
</head>
<body>
    <form action="/save_to_s3" method="post">
        <p>
            <input type="text" name="subject" id="subject"><br/>
        </p>
        <p>
            <textarea name="message" id="message" cols="30" rows="10"></textarea><br/>
        </p>
        <p>
            <input type="submit" value="Send">
        </p>
    </form>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def get_form():
    return PAGE


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


