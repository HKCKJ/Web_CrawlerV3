from crewai import Crew, Process
from ScrapeAgents import Scrape_Agents
from ScrapeTasks import Scrape_Tasks

#Class to group and define all inputs, agents, tasks and crew.
class ScrapeCrew():
    def __init__(self, inputs):
        self.inputs = inputs
        self.agents = Scrape_Agents()
        self.tasks = Scrape_Tasks()

    def run(self):
        Researcher = self.agents.Researcher()
        Agent_write= self.agents.Agent_writer()
        Info_organizer= self.agents.Info_organizer()

        research_task = self.tasks.research_task(
             Researcher, 
             self.inputs
        )

        writer_task = self.tasks.writer_task(
            Agent_write,
            [research_task]
        )

        structuring_task = self.tasks.structuring_task(
            Info_organizer,
            self.inputs,
        )

        crew = Crew(
            agents=[Researcher, Agent_write, Info_organizer],
            tasks=[research_task, writer_task, structuring_task],
            process= Process.sequential,
            verbose=True
        )

        return crew.kickoff()

#Define inputs for crew kickoff run
if __name__ == "__main__":
    url = input("URL you want to scrape?")
    topic = input( "What is the topic of interest? Examples: Price of products? Summary on forensic science ")
    summary = input("Do you wish to summarise scraped content?:", ["Yes", "No"])
    format = input("Output format:", ["Markdown", "JSON", "Plain Text","Excel Table"])
    inputs = f"url: {url}\ntopic: {topic}\nformat: {format}"
    Crew_result = ScrapeCrew(inputs)
    result = Crew_result.run()
    print(result)

