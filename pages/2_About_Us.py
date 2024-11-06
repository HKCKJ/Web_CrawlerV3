import streamlit as st

st.set_page_config(
    layout="centered",
    page_title="About Us")

st.title("About Us")

st.write("Hello, welcome to AI-Web Crawler, \
        web scraping is the automated process of extracting data from websites. \
        While it enables gathering large datasets efficiently, it faces challenges like changing website structures, \
        blocking mechanisms, and legal restrictions. Many websites prohibit scraping in their terms of service, making ethical and \
        compliant data collection critical to avoid potential legal issues.")

st.title("Scope")

st.write("In this app, our goal is to collect publicly available data from multiple authorized news websites simultaneously, enabling AI-powered \
         trend generation and insightful analysis while ensuring compliance by excluding data from any sites that prohibit scraping in their terms of service.")

st.title("Objectives")

st.write("Enable AI-driven web scraping to be performed efficiently, requiring minimal human intervention and reducing the time and effort needed.")

st.title("Features")

st.write("1. AI-powered search to find relevant URLs based on the input topic when no URLs are provided.")
         
st.write("2. Option to summarise or not to summarise scraped data from the web")   

st.write("3. Options to choose the output file format for the data to facilitate downstream analysis or presentation")

st.write("4. Displays the agent's thought process, tools utilized, and the results at each given step, enabling users to better understand the workflow \
          and provide feedback for continuous improvements.")