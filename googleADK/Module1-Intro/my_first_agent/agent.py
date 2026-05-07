import os
from google.adk.agents.llm_agent import Agent


os.environ['GOOGLE_API_KEY'] = "[GCP_API_KEY]"
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)