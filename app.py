from __future__ import print_function
from flask import Flask,send_from_directory

app = Flask(__name__)

@app.route("/eu/videos.txt")
def videos_EUR():
    return send_from_directory("static","EU_videos.txt")

@app.route("/us/videos.txt") # they're different
def videos_USA():
    return send_from_directory("static","US_videos.txt") 

@app.route("/<string:region>/<string:num>.3gp",defaults={"lang":None})
@app.route("/<string:region>/<string:lang>/<string:num>.3gp")
def servevid(region,lang,num):
    if region == "us":
        vid = f"{region}/{num}.3gp"
    else:
        vid = f"{region}/{lang}/{num}.3gp"

    return send_from_directory("videos",vid)

if __name__ == "__main__":
    app.run("127.0.0.1",80,True)