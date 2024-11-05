import os
import streamlit as st
from crewai import LLM
from dotenv import load_dotenv

if load_dotenv('.env'):
#Acccess serperdev API key from env
    SERPER_API_KEY=os.getenv("SERPER_API_KEY")

    llm = LLM(
        model="gpt-4o-mini",  # Use the standard OpenAI model name
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://litellm.govtext.gov.sg/",
        default_headers={
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"
        },
        custom_llm_provider="azure openai",
        deployment_id="gpt-4o-prd-gcc2-lb"  # Your Azure deployment name
    )
else: 
    st.secrets["SERPER_API_KEY"]
    st.secrets["OPENAI_API_KEY"]