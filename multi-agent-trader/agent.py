from google.adk.agents import SequentialAgent
from .sub_agents.information_agent import information_agent
from .sub_agents.output_agent import output_agent
from .sub_agents.strategy_agent import strategy_agent

root_agent = SequentialAgent(
    name="investment_advisor_root",
    description="Orchestrator that determines whether a stock is a good investment",
    sub_agents=[information_agent, output_agent, strategy_agent],
)

# root_agent = SequentialAgent(
#     name="investment_advisor_root",
#     model="gemini-2.0-flash",
#     description="Orchestrator that determines whether a stock is a good investment",
#     instruction="""
#     You are an investment advisor system that analyzes whether a stock is a good investment.

#     When a user asks about a specific stock:
#     1. Call the information_agent to gather market, fundamental, and sentiment data in parallel.
#     2. Pass the combined outputs to the output_agent, which converts the raw text into a structured format.
#     3. Send the structured output to the strategy_agent, which will make a final investment recommendation and suggest a price to buy at.

#     Only respond to the user after the strategy_agent completes its recommendation.
#     """,
#     sub_agents=[information_agent, output_agent, strategy_agent],
#     tools=[],
#     output_schema=None,
# )