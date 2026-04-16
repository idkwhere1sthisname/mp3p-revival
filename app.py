from __future__ import print_function
from flask import Flask,send_from_directory,abort,send_file
from werkzeug.serving import WSGIRequestHandler
import os
import xml.etree.ElementTree as ET
STATIC = os.path.join(os.path.dirname(__file__),"static")
VIDEOS = os.path.join(os.path.dirname(__file__),"videos")
CONFIG = os.path.join(os.path.dirname(__name__),"config.xml")
CONFIGXML = "config.xml"
app = Flask("mp3p-revival",static_folder=STATIC)

@app.route("/<string:region>/videos.txt")
def videos_EUR(region):
    regionarr = ["us","eu"]
    region = str(region)
    if region not in regionarr:
        abort(400)
    f = region.upper()+"_videos.txt"
    path = os.path.join(STATIC,f)
    if not os.path.exists(path):
        return abort(404)
    return send_from_directory(STATIC,f),200,{"Content-Type":"text/plain; charset=UTF-8"}

@app.route("/<string:region>/<string:num>.3gp",defaults={"lang":None})
@app.route("/<string:region>/<string:lang>/<string:num>.3gp")
def servevid(region,lang,num):
    regionarr = ["us","eu"]
    languagesarr = ["ita","ger","eng","spa","dut","fra"]
    if region not in regionarr:
        abort(400)
    if region == "us":
        if lang is not None:
            abort(400)
        vid = f"{region}/{num}.3gp"
    else:
        if lang not in languagesarr:
            abort(400)
        vid = f"{region}/{lang}/{num}.3gp"
    finalvid = os.path.join(VIDEOS,vid)
    if not os.path.exists(finalvid):
        abort(404)
    return send_file(finalvid),200

if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    try:
        if not os.path.exists(CONFIG):
            host = input("Where should the server run? (0.0.0.0 for all interfaces): ")
            port = None
            while port is None:
                try:
                    port_i = input("On what port should the server run? (80 is recommended): ")
                    port = int(port_i)
                except ValueError:
                    print("Invalid port, please enter a valid port")
            port = str(port)
            dbg = input("Should the server run in debug mode? (yes/no): ").lower()
            while dbg not in ["yes","no"]:
                dbg = input("Please enter either yes or no: ").lower()
            debugmode = dbg == "yes"
            configXml = ET.Element("configuration")
            ET.SubElement(configXml,"host").text = host
            ET.SubElement(configXml,"port").text = port
            ET.SubElement(configXml,"debug").text = str(debugmode)
            ET.ElementTree(configXml).write(file_or_filename=CONFIGXML,encoding="utf-8",xml_declaration=True)
        else:
            tree = ET.parse(CONFIGXML)
            cfg = tree.getroot()
            host = cfg.find("host").text
            port = int(cfg.find("port").text)
            dbg = cfg.find("debug").text.lower() == "true"
        app.run(host=host,port=port,debug=dbg)
    except KeyboardInterrupt:
        print("\nExiting...")
