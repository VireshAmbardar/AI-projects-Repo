from google.adk.agents import LlmAgent


ROOT_AGNET_DESCRIPTION="""

"""

ROOT_INSTRUCTIONS= '''
'''

# Free  gemini-3.5-flash or gemini-3.1-flash-lite 
MODEL = "gemini-3.5-flash"
 
root_agent = LlmAgent(
    name='root_agent',
    model=MODEL,
    description="Root Agent",
    instruction="Act as a Financial Assistent that Does the curretn market research Finds the Best bond According to user needs.",
    # tools=[get_current_time],
)