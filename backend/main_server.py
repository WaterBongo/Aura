from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import flask,uuid
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
    scores = {}
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
        print(f"{i+1}) {type(l)} {(np.round(float(s), 4))}")

@app.route("/")
def index():
    return "sex"




#endpoint is Upload_video
@app.route("/upload_video", methods=["POST"])
def upload_video():
    file = request.files['audio_data']   
    uuid_generated = str(uuid.uuid4())
    file.save(f"./videos/{uuid_generated}.wav")
    text = video_to_text(uuid_generated)
    print(text)
    print(sentimental_anasysis(text))
    return {"id":uuid_generated,"text" :text}



app.run("0.0.0.0",8080)