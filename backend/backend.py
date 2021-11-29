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

<<<<<<< HEAD


#FRONT_PATH = pathlib.Path("/home/uladzimir/projects/my_applications/front/code").absolute()


#@app.route("/", methods=["GET"])
#def get_form():
#    with open(FRONT_PATH / "index.html") as page_file:
#        return page_file.read()
=======
FRONT_PATH = pathlib.Path(__file__).parent.parent.absolute()


@app.route("/", methods=["GET"])
def get_form():
    with open(FRONT_PATH / "front" / "index.html") as page_file:
        return page_file.read()
>>>>>>> 8ab8d13b6c8c8c1fab735aae868a5af1f1740a8a


@app.route("/save_to_s3", methods=["POST"])
def save_to_s3():
    data = (request.form["subject"] + "\n\n" + request.form["message"]).encode("utf-8")
    CLIENT.put_object(
        **{
            "Body": data,
            "Bucket": os.environ["BUCKET_NAME"],
            "Key": datetime.utcnow().strftime("%Y/%m/%d/%H%M%S.txt"),
        }
    )
    return redirect("/")


