from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

import os
mongo_url = os.environ.get("MONGO_URI")
mongo_db = os.environ.get("DB_NAME")
client = MongoClient(mongo_url)
mydb = client[mongo_db]
mycol = mydb["routers"]


app = Flask(__name__)


@app.route("/")
def main():
    data = []
    for x in mycol.find():
        data.append(x)
    return render_template("index.html", data=data)

@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    if ip and username and password:
        mycol.insert_one({"ip": ip, "username" : username, "password" : password})
    return redirect("/")

@app.route("/delete/<idx>", methods=["POST"])
def delete_comment(idx):
    try:
        mycol.delete_one({'_id': ObjectId(idx)})
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
