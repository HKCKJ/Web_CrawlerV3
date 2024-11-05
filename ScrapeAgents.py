import re
import streamlit as st
from crewai import Agent
from access.LLMconfig import llm

 #Crew members who are responsible for task of gathering relevant and legitimate url for scraping, scraping from url, summarising scraped information and lastly organizing data into format requested by user
class Scrape_Agents:

    #Researcher role will only execute task of finding sites relevant to the topic if no sites are provided by user.
    #The researcher tend to be overzealous with the web-scraping prohibitions part that was why line 19 was added.
	def Researcher(self):
		return Agent(
			role= "Web-collector",
            goal= "Search for all available websites related to the {topic}",
            backstory= """You're the subject matter expert of the {topic}. You're gathering all website url about the {topic} using your expertise. 
			You will filter off other sites based on these conditions:\
            (1) Site does not have a terms and condition clause that states that web scraping is prohibited. \
			If there are no specifications stated on web-scraping for the site then proceed with the scraping.
            (2) Information provided is up to date and recent. \
            Your work is the basis for the Agent_writer to summarise information from the urls on the {topic}""",
			verbose=True,
			llm = llm
        )

    #Writer will be the default summarizer for the information scraped from the web.
	def Agent_writer(self):
		return Agent(
			  role= "Summary_writer",
			  goal= "Create insightful and factually accurate summary on the: {topic}",
			  backstory= """You're the subject matter expert of the {topic} and a meticulous analyst with a keen eye for detail. You will work with the \
			  information that is collected from the web_scraper. You're known for your ability to turn complex \
		      data into clear and concise reports, making it easy for others to understand and act on the information you provide.""",
			  verbose=True,
			  llm = llm
		)

	#Info organizer to output the desired file format for the user.
	def Info_organizer(self):
		return Agent(
			role= "Data_organizer",
			goal= "Parse and structure the scraped information regarding the {topic} into a {format} and store it locally.",
			max_iter= 2,
			backstory= """You're a skilled data organization expert with the expertise to convert any unstructured data gathered from \
			the web_scraper into a desired {format}. Your task is to take raw scraped data and transform it into a strucured 
			{format} for ease of data integration or analysis.""",
			verbose=True,
		    llm = llm
		)

#Printing agent processes to the streamlit app to allow user to view the thought process of agents 
# This portion of the code is adapted from @AbubakrChan; thank you!                       
# https://github.com/AbubakrChan/crewai-UI-business-product-launch/blob/main/main.py#L210 	
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Web-collector" in cleaned_data:
            # Apply different color 
            cleaned_data = cleaned_data.replace("Web-collector", f":{self.colors[self.color_index]}[Web-collector]")
        if "Summary_writer" in cleaned_data:
            cleaned_data = cleaned_data.replace("Summary_writer", f":{self.colors[self.color_index]}[Summary_writer]")
        if "Data_organizer" in cleaned_data:
            cleaned_data = cleaned_data.replace("Data_organizer", f":{self.colors[self.color_index]}[Data_organizer]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []