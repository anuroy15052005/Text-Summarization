import os
os.environ["NUMEXPR_MAX_THREADS"] = "16"

import streamlit as st
from textSummarizer.pipeline.prediction import PredictionPipeline

st.title("Dialogue Summarizer")
text = st.text_area("Enter dialogue:")

if st.button("Summarize"):
    obj = PredictionPipeline()
    summary = obj.predict(text)
    st.write("**Summary:**")
    st.write(summary)
    