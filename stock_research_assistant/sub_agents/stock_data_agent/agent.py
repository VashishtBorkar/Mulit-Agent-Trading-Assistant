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
    Use the tools available to retrieve market data.
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
            # tool_filter=['get_snapshot_ticker', 'get_aggs', 'list_ticker_news']
        )
    ],
    output_key="stock_data_agent_result"
)
