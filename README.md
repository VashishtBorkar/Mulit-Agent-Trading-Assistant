# Multi-Agent Stock Research Assistant

The Multi-Agent Stock Research Assistant is an AI-powered system designed to make stock market research easier to understand and more interactive. By combining multiple specialized agents with a conversational LLM interface, users can explore company fundamentals, market trends, sentiment analysis, and strategy insights through natural dialogue while still receiving accurate, grounded information.  

## Demo
<a href="https://youtu.be/jzH8b4IN4pM" target="_blank">Link to demo video</a>

## Features
- Multi-agent orchestration, with agent focusing on a different research track (market data and sentiment)  
- Conversational interface that allows users to ask questions in plain language and receive accurate, data-backed insights  
- Market insights including financial metrics, company performance, and recent trends  
- Google AI SDK integration for reliable, fast responses with reduced AI hallucinations  

## Tech Stack
- Python for core orchestration and backend logic  
- Google AI SDK for LLM integration  
- Polygon API and Polygon MCP for financial data  
- Docker (optional) for containerized deployment  

## Getting Started
1. Clone the repository:  
   ```bash
   git clone https://github.com/VashishtBorkar/multi-agent-trading-assistant.git
   ```
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (Polygon API key, Google AI SDK) in a .env file
4. Run adk web interface
   ```bash
   adk web
   ```

## Limitations

- **API Access Restrictions:** The bot relies on the Polygon.io API for market and historical data. The available information and update frequency are limited by the permissions and quota of your Polygon API plan. Upgrading your plan can provide access to more comprehensive datasets and higher request limits.  

- **MCP Server Version:** The bot uses the Polygon MCP server (`mcp_polygon`) to interface with the API. Certain endpoints or features may not be available if the MCP server is outdated. Keeping the MCP server up to date ensures the bot can access the latest tools and endpoints.  

- **Data Accuracy and Coverage:** The bot’s reports are only as accurate as the data retrieved from Polygon.io. Delays or gaps in data from the API will affect the generated reports.  

- **Future Improvements:** Performance and coverage of the bot will improve as the Polygon API and MCP server continue to evolve, providing more endpoints, higher quality data, and more robust tooling for multi-agent workflows.

