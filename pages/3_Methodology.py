import streamlit as st

st.set_page_config(
    layout="centered",
    page_title="Methodology")

st.title("Methodology Flow Chart")



st.image("Crewai Flow Chart.jpg", caption="Crewai workflows")

with st.expander("Use cases", expanded=False): 
    st.write('''a) Aggregating news and analyzing trends on a specific topic from various news sources. \
            b) Enabling market research for a particular product or generating leads by gathering data from multiple web sources. \
            c) Conducting sentiment analysis on a product or service by analyzing popular forums and websites.
             ''')