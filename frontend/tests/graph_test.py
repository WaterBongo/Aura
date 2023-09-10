# Install required packages
# pip install matplotlib streamlit pandas

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Incoming emotion data
emotion_data = {'emotion': {'negative': '0.0054', 'neutral': '0.0747', 'positive': '0.92'}, 'text': 'testing testing I hope my day went well', 'time': '22:54:19'}
#only use the biggest to graph
emotion_data['emotion'] = max(emotion_data['emotion'], key=emotion_data['emotion'].get)

# Parse the emotion data
emotion_time = pd.to_datetime(emotion_data['time']) 
emotions = { key: float(value) for key, value in emotion_data['emotion'].items() }

# Create a dataframe
df = pd.DataFrame(emotions, index=[emotion_time])

# Set title
st.title('Emotions over time')

# Plot the data
st.line_chart(df)