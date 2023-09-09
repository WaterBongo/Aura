import flask,uuid
from flask import request
app = flask.Flask(__name__)



@app.route("/")
def index():
    return "sex"


@app.route("/upload_video", methods=["POST"])
def upload_video():
    file = request.files['video']   
    uuid_generated = str(uuid.uuid4())
    file.save(f"./videos/{uuid_generated}.webm")
    return {"id":uuid_generated}

app.run("0.0.0.0",8080)