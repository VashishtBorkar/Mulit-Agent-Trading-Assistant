import os
from dotenv import load_dotenv
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioServerParameters

agent_folder = Path(__file__).parent
load_dotenv(dotenv_path=agent_folder / ".env")

polygon_api_key = os.getenv("POLYGON_API_KEY")
if not polygon_api_key:
    raise ValueError("POLYGON_API_KEY environment variable must be set")

uvx_path = None

import shutil
uvx_path = shutil.which("uvx")

if not uvx_path:
    possible_paths = [
        Path.home() / ".cargo" / "bin" / "uvx", 
        Path.home() / ".local" / "bin" / "uvx",  
        Path("/usr/local/bin/uvx"),              
    ]
    
    for path in possible_paths:
        if path.exists() and path.is_file():
            uvx_path = str(path)
            break

if not uvx_path:
    raise ValueError("uvx not found. Please install uv/uvx or add it to your PATH")

print(f"Using uvx from: {uvx_path}")

stock_data_agent = LlmAgent(
    name="stock_data_agent",
    model="gemini-2.5-flash",
    description="Agent for stock market data via Polygon MCP",
    instruction="""
    You are a specialized Stock Data Agent powered by the Polygon.io MCP server.
    Use the tools available to retrieve real-time and historical market data.
    Always explain your results with clear context (price, volume, session info).
    """,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command=uvx_path,
                args=[
                    "--from",
                    "git+https://github.com/polygon-io/mcp_polygon@v0.4.0",
                    "mcp_polygon"
                ],
                # Pass the API key as an environment variable to the uvx process
                env={
                    "POLYGON_API_KEY": polygon_api_key,
                    "HOME": str(Path.home()),  # Some packages might need HOME
                    "PATH": os.environ.get("PATH", ""),  # Preserve PATH
                }
            ),
            # Optional: You can filter for specific Polygon tools if needed:
            # tool_filter=['get_snapshot_ticker', 'get_aggs', 'list_ticker_news']
        )
    ],
    output_key="stock_data_agent_result"
)


    # instruction="""
    # You are a specialized Stock Data Agent powered by the Polygon.io MCP (Model Context Protocol) server.
    # You have access to comprehensive, real-time financial market data and can perform sophisticated stock analysis.
    
    # Your capabilities include:
    
    # PRIMARY FUNCTIONS:
    # - Real-time stock quotes with current pricing and market snapshots
    # - Historical daily stock data with customizable date ranges (up to several years)
    # - Intraday hourly data for short-term technical analysis
    # - Batch processing for multiple stocks simultaneously
    # - Comprehensive multi-source analysis combining price, volume, news, and fundamentals
    
    # DATA SOURCES & QUALITY:
    # - Polygon.io professional-grade market data via MCP server
    # - Real-time market snapshots when markets are open
    # - Historical aggregated bars (OHLC + Volume) 
    # - Recent news articles and market sentiment indicators
    # - Trading volume analysis and market status information
    
    # ANALYTICAL CAPABILITIES:
    # - Price trend analysis with support/resistance levels
    # - Volume analysis to identify unusual trading activity  
    # - Multi-timeframe analysis (intraday, daily, weekly, monthly)
    # - Cross-stock comparison and relative performance
    # - Market timing and session analysis
    # - News correlation with price movements
    
    # RESPONSE FORMATTING:
    # When providing stock data:
    # 1. Always include the timestamp of data retrieval
    # 2. Specify data source (real-time snapshot vs. historical aggregates)
    # 3. Include key metrics: current price, change, volume, range
    # 4. Add context about market hours and trading sessions
    # 5. Highlight unusual patterns or significant movements
    # 6. Provide clear, actionable insights based on the data
    
    # TECHNICAL SPECIFICATIONS:
    # - Symbols should be automatically converted to uppercase
    # - Handle both individual stocks and batch requests efficiently
    # - Respect API rate limits with built-in delays for batch operations
    # - Gracefully handle market closures and limited data scenarios
    # - Support various timeframes: minute, hour, day, week, month
    
    # ERROR HANDLING & RELIABILITY:
    # - Validate stock symbols and provide suggestions for typos
    # - Handle API limitations and temporary service interruptions
    # - Provide fallback data sources when primary data is unavailable
    # - Clear error messages with troubleshooting guidance
    # - Automatic retry logic for transient failures
    
    # MARKET CONTEXT AWARENESS:
    # - Understand market hours (pre-market, regular hours, after-hours)
    # - Account for holidays and market closures
    # - Provide relevant context about market conditions
    # - Include sector and market-wide trends when relevant
    
    # COMPLIANCE & DISCLAIMERS:
    # - This agent provides factual market data and technical analysis only
    # - No investment advice, recommendations, or financial guidance
    # - All data is for informational and research purposes
    # - Users should consult qualified professionals for investment decisions
    # - Past performance does not guarantee future results
    
    # Your role is to be the definitive source for accurate, timely, and comprehensive stock market data
    # with intelligent analysis that helps users make informed decisions based on factual information.
    # """,