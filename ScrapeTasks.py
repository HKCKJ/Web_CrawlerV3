import streamlit as st
from crewai import Task
from crewai.tasks.conditional_task import ConditionalTask
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

#Function for user input in case a conditional task needs to be added. These can be then used to define conditional task.
def user_url():
    return st.text_input("URLs:")

def user_topic():
    return st.text_input("What is the topic of interest:")

def summarised_output():
    return st.selectbox("Do you wish to summarise scraped content:", ["Yes", "No"])

def user_format():
    return st.selectbox("Output format:", ["Markdown", "JSON", "Plain Text","Excel Table"])

#Conditional function to feed into the task. If the answer is yes then the data will be summarised before it is formatted.
def should_execute_task(summary: str) -> bool:
    return summary == 'Yes'

#Encapsulates all scraping tasks done by agents
class Scrape_Tasks:

    #First task which contains many steps from determining whether there is a url input to scraping information from relevant url.
    #User has the choice to define a url for scraping or just have the LLM to search urls for scraping.
    #Task act as a first pass filter to remove urls that potentially prohibits web-scraping.
    #The researcher tend to be overzealous with the web-scraping prohibitions part that was why line 35 was added.
    #Scrape url info that is relevant to user-defined topic.

    def research_task(self, agent, inputs):
        return Task(description=f""" \
            Determine the steps to take based on the {inputs}
            1. Determine if there is url input from the user, if not then proceed to step 3. \
            If a url input is being provided by the user then proceed to step 4.
            2. Search the web for all urls related to this topic.
            3. Create a list of urls that can be accessed by the Web scraper that is relevant to the topic. \
            The urls must be relevant to the topic.
            4. Remove url sites where the terms and conditions prohibits web-scraping.\
            If there are no specifications stated on web-scraping for the site then proceed with the scraping.
            5. Remove url sites where the content is not recent or up to date for the topic.
            6. Scrape the url sites that are relevant to the topic.
                    
            """,
            expected_output= f"""
            1.If there is no url from {inputs} from the user then output a list of top 5 urls relevant to the topic from {inputs}.
            2. else if there is a url from {inputs} then scrape all information relevant to the topic from the {inputs}""",
            tools = [SerperDevTool(), ScrapeWebsiteTool()],
            agent= agent,
            delegation = True
        )

    #Writer summarises input from the researcher and proofreads for errors.
    def writer_task(self, agent, context):
        return ConditionalTask(description=""" \
            Check if the user wants to summarise the scraped results from the researcher.\
            If yes then proceed with step 1.
            1. Write a report based on the raw scraped data provided by the Researcher.
            2. The summary should be based on the growing trends and development of the topic.
            3. Proofread for grammatical errors.
                    
            You should not make-up any data in the process. Ensure that all outputs are factually correct.

            """,
            expected_output= "A fully fledge reports with the mains topics, each with a full \
            section of information. Formatted as markdown without '```'",
            agent= agent,
            context=context,
            condition= should_execute_task
        )

    # Info structrurer gathers the information from writer and output desired file type.
    def structuring_task(self, agent, inputs):
        return Task(description=f""" \
            Determine the output format from user {inputs}.
            Take the data that are relevant to the topic from the writer \
            and structure it into the desired format    
            
            Your data/data points in the format should always be factually correct. 
            Do not make-up any data points.

            """,

            expected_output= f"""Data structured into a format requested by the user
            from the {inputs}""",
            agent= agent
        )

    

