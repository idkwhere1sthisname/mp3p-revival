from flask import Flask,send_from_directory

app = Flask(__name__)

@app.route("/eu/videos.txt")
def videos_EUR():
    return send_from_directory("static","EU_videos.txt")

@app.route("/us/videos.txt") # they're different
def videos_USA():
    return send_from_directory("static","US_videos.txt") 

#offsets (EUR)
#FUN_80017724 #video.txt
#FUN_800252ac #logging
#redir to OSReport

#vid parse
#FUN_800fdb88
#LAB_800fcf5c
#FUN_800fd2b8
#FUN_800fd6f0
#FUN_801048ac

#offsets (USA)
#FUN_80024fa4 #logging

@app.route("/<string:region>/<string:lang>/<string:num>.3gp")
def servevid(region,lang,num):
    vid = f"{region}/{lang}/{num}.3gp"
    if lang == None:
        vid = f"{region}/{num}.3gp"

    return send_from_directory("videos",vid)

if __name__ == "__main__":
    app.run("127.0.0.1",80,True)