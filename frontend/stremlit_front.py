import streamlit as st
from io import BytesIO
import requests
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
from audio_recorder_streamlit import audio_recorder

# Set page title
st.set_page_config(page_title="Aura")
SERVER_URL = "http://127.0.0.1:8080/upload_video"
# Define sidebar
st.sidebar.title("Navigation")
menu = ["🎥 Recorder", "📚 History", "❓ Help", "🔍 Analysis"]
choice = st.sidebar.selectbox("Go to", menu)

# Add emojis for each section
if choice == "🎥 Recorder":
    st.title("🎤 Audio recorder")
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

elif choice == "📚 History":
    st.title("📜 History")
elif choice == "❓ Help":
    st.title("❓ Help")
elif choice == "🔍 Analysis":
    st.title("🚧 Section 4")
else:
    st.title("🏠 Home")
