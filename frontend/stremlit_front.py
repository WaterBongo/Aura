import streamlit as st
from io import BytesIO
import requests
import streamlit.components.v1 as components
from st_custom_components import st_audiorec
from audio_recorder_streamlit import audio_recorder
import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import openai,spacy
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

openai.api_key = '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'

# Set page title



def ask_gpt(question):
    e =openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{question} give positive reinforcment to the user! talk alittle about the current scores"}])
    return e['choices'][0]['message']['content']

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
        if st.button('Check!'):
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

            st.text(ask_gpt(str(res.json())))
            df = pd.DataFrame([[0,0,0],[1,1,1]], columns=("potato","test","3"))
            st.dataframe(df) 

elif choice == "📚 History":
    data = {
        'time': ['12:00 AM', '3:00 AM', '6:00 AM', '9:00 AM', '12:00 PM', '3:00 PM', '6:00 PM', '9:00 PM'],
        'negative': [0.2, 0.3, 0.1, 0.4, 0.3, 0.2, 0.1, 0.2],
        'neutral': [0.5, 0.4, 0.6, 0.3, 0.4, 0.5, 0.6, 0.5],
        'positive': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Create the chart
    fig = px.line(df, x='time', y=['negative', 'neutral', 'positive'], title='Emotions for the Current Day')

    

    import pandas as pd
    import plotly.express as px
    import streamlit as st

    # Define sample data
    data = {
        'date': pd.date_range(start='2022-01-01', end='2022-01-07'),
        'negative': [0.2, 0.3, 0.1, 0.4, 0.3, 0.2, 0.1],
        'neutral': [0.5, 0.4, 0.6, 0.3, 0.4, 0.5, 0.6],
        'positive': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
    }

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Create the chart
    fig = px.line(df, x='date', y=['negative', 'neutral', 'positive'], title='Feelings over a Week')

    # Add a button to switch to monthly view
    if st.button('Switch to Monthly View'):
        # Define sample data for monthly view
        data_monthly = {
            'date': pd.date_range(start='2022-01-01', end='2022-01-31'),
            'negative': [0.2, 0.3, 0.1, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.1, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.1, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.1, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.1],
            'neutral': [0.5, 0.4, 0.6, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.6, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.6, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.6, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.6],
            'positive': [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,0.3]
        }

        # Create a DataFrame from the data
        df_monthly = pd.DataFrame(data_monthly)

        # Create the chart for monthly view
        fig_monthly = px.line(df_monthly, x='date', y=['negative', 'neutral', 'positive'], title='Feelings over a Month')

        # Display the chart for monthly view
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        # Display the chart for weekly view
        st.plotly_chart(fig, use_container_width=True)
elif choice == "❓ Help":
    st.title("❓ Help")
elif choice == "🔍 Analysis":
    st.title("🚧 Section 4")
else:
    st.title("🏠 Home")