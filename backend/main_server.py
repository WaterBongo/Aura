import flask,uuid
from flask_cors import CORS
from flask import request
app = flask.Flask(__name__)
CORS(app)





def video_to_text(uuid):
    pass



@app.route("/")
def index():
    return "sex"









@app.route("/upload_video", methods=["POST"])
def upload_video():
    file = request.files['audio_data']   
    uuid_generated = str(uuid.uuid4())
    file.save(f"./videos/{uuid_generated}.wav")
    return {"id":uuid_generated}



app.run("0.0.0.0",8080)