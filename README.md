# Multi-Agent Stock Research Assistant

The Multi-Agent Stock Research Assistant is an AI-powered system designed to make stock market research easier to understand and more interactive. By combining multiple specialized agents with a conversational LLM interface, users can explore company fundamentals, market trends, sentiment analysis, and strategy insights through natural dialogue while still receiving accurate, grounded information.  

## Demo
<a href="" target="_blank">Link to demo video (Coming Soon) </a>

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
