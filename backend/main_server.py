from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import flask,uuid,time
from flask_cors import CORS
from flask import request
import os
import speech_recognition as sr
recognizer = sr.Recognizer()
app = flask.Flask(__name__)
CORS(app)
os.environ['TOKENIZERS_PARALLELISM'] = 'False'
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
config = AutoConfig.from_pretrained(MODEL)
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
#model.save_pretrained(MODEL)

video_info = {}


def video_to_text(uuid):
    with sr.AudioFile(f"./videos/{uuid}.wav") as source:
        recorded_audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(
                recorded_audio, 
                language="en-US"
            )
            print(text)
        except sr.UnknownValueError:
            return ""
        return text

def sentimental_anasysis(text):
    scores_total = {}
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]


    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        print(scores)
        scores_total[l] = str(np.round(float(s), 4))
        print(f"{i+1}) {type(l)} {(np.round(float(s), 4))}")
        print(scores_total)
    return scores_total
def get_time():
    from datetime import datetime
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    return current_time


@app.route("/")
def index():
    return "potato"




#endpoint is Upload_video
@app.route("/upload_video", methods=["POST"])
def upload_video():
    file = request.files['audio_data']      
    uuid_generated = str(uuid.uuid4())
    file.save(f"./videos/{uuid_generated}.wav") 
    textz = video_to_text(uuid_generated)
    print(textz)
    feeling = sentimental_anasysis(textz)
    #get the time
    time_event = get_time()
    video_info[uuid_generated]={"text":textz,"emotion": feeling,"time":time_event}
    print(video_info)
    return video_info[uuid_generated] #example, {"id":"da013b0d-2252-4d3c-b8bd-2c30afe24d47","text":"I love hot dog"}

@app.route("/analyze",methods=["POST"])
def analyze():
    uuid = request.form["id"]
    text = video_info[uuid]["text"]
    if text == "":
        return {"error":"no text found"}
    return sentimental_anasysis(text)


@app.route("/archieve")
def archieve():
    #get all videos from videos folder, find timestamp of creation
    #return all videos
    all_videos = []
    video_time = []
    for filename in os.listdir("./videos"):
        if filename.endswith(".wav"):
            #get the timestamp of video
            timestamp = os.path.getmtime(f"./videos/{filename}")
            local_time = time.ctime(timestamp)
            all_videos.append(filename)
            video_time.append(local_time)
    return {"videos":all_videos,"timestamp":video_time}


@app.route("/reanalysis",methods=['POST'])
def reanalysis():
    uuid = request.form["id"]
    text = video_to_text(uuid.strip(".wav"))
    return sentimental_anasysis(text)


@app.route("/view/<videoid>",methods=["GET"])
def view_vid(videoid):
    #check if file exists
    if not os.path.isfile(f"./videos/{videoid}"):
        return {"file":False},404
    return flask.send_from_directory("./videos",videoid)

app.run("0.0.0.0",8080)