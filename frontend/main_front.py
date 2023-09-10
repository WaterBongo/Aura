import streamlit as st
import requests
import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
SERVER_URL = "http://127.0.0.1:8080/upload_video"  # Replace with your server URL

st.title("Voice Audio Recorder")

# Record audio using the custom component
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    # Display the recorded audio in the Streamlit app
    st.audio(wav_audio_data, format='audio/wav')
    
    # If the Submit button is clicked, send the audio data to the server
    if st.button('Submit'):
        # You need to convert the audio data from the Bytes datatype to a File-like object that can be handled by the requests library
        audio_file = BytesIO(wav_audio_data)
        files = {'audio_data': audio_file}
        
        # Make a POST request to the server with the recorded audio file
        res = requests.post(SERVER_URL, files=files)
        print(res.json( ))

        if res.ok:
            st.success("Audio successfully uploaded to server.")
        else:
            st.error("Error occurred while uploading audio to server.")

        st.text(res.json())