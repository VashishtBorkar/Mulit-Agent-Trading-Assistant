import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class PolygonMCPClient:
    """Client for interacting with the Polygon MCP server from polygon-io/mcp_polygon"""
    
    def __init__(self, polygon_api_key: str):
        self.polygon_api_key = polygon_api_key
        self.session: Optional[ClientSession] = None
        
        # Server parameters for the Polygon MCP server
        self.server_params = StdioServerParameters(
            command="python",  # or "python3" depending on your system
            args=["-m", "mcp_polygon"],  # This runs the MCP server
            env={"POLYGON_API_KEY": polygon_api_key}  # Pass API key to server
        )
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.stdio_client = stdio_client(self.server_params)
        self.session, _ = await self.stdio_client.__aenter__()
        
        # Initialize the server connection
        # await self.session.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.stdio_client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def get_aggregates(
        self, 
        ticker: str, 
        multiplier: int = 1, 
        timespan: str = "day",
        from_date: str = None,
        to_date: str = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get aggregate bars for a ticker using the MCP server's get_aggs tool"""
        try:
            # Set default dates if not provided
            if not to_date:
                to_date = datetime.now().strftime("%Y-%m-%d")
            if not from_date:
                from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            result = await self.session.call_tool(
                "get_aggs",
                arguments={
                    "ticker": ticker.upper(),
                    "multiplier": multiplier,
                    "timespan": timespan,
                    "from_": from_date,
                    "to": to_date,
                    "limit": limit
                }
            )
            
            # Parse the result from MCP
            if result.content and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return json.loads(content.text)
                else:
                    return content
            return {}
            
        except Exception as e:
            return {"error": f"Failed to get aggregates for {ticker}: {str(e)}"}
    
    async def call_tool_safe(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Safely call any tool on the MCP server"""
        try:
            result = await self.session.call_tool(tool_name, arguments)
            
            if result.content and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    return json.loads(content.text)
                else:
                    return content
            return {}
            
        except Exception as e:
            return {"error": f"Failed to call {tool_name}: {str(e)}"}

class StockDataService:
    """Service class for stock data operations using Polygon MCP"""
    
    def __init__(self, polygon_api_key: str):
        self.polygon_api_key = polygon_api_key
    
    async def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get current stock data (latest daily bar)"""
        async with PolygonMCPClient(self.polygon_api_key) as client:
            # Get the latest daily data
            data = await client.get_aggregates(
                ticker=symbol,
                multiplier=1,
                timespan="day",
                limit=1
            )
            
            # Transform the data to include current price info
            if "results" in data and data["results"]:
                latest = data["results"][-1]
                return {
                    "symbol": symbol.upper(),
                    "price": latest.get("c"),  # close price
                    "open": latest.get("o"),
                    "high": latest.get("h"), 
                    "low": latest.get("l"),
                    "volume": latest.get("v"),
                    "timestamp": latest.get("t"),
                    "date": datetime.fromtimestamp(latest.get("t", 0) / 1000).strftime("%Y-%m-%d") if latest.get("t") else None
                }
            return data
    
    async def get_historical_data(self, symbol: str, days: int = 30) -> Dict[str, Any]:
        """Get historical stock data"""
        async with PolygonMCPClient(self.polygon_api_key) as client:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            return await client.get_aggregates(
                ticker=symbol,
                multiplier=1,
                timespan="day",
                from_date=start_date,
                to_date=end_date,
                limit=days
            )
    
    async def get_intraday_data(self, symbol: str, hours: int = 24) -> Dict[str, Any]:
        """Get intraday data (hourly bars)"""
        async with PolygonMCPClient(self.polygon_api_key) as client:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")  # Get 2 days to ensure we have enough data
            
            return await client.get_aggregates(
                ticker=symbol,
                multiplier=1,
                timespan="hour",
                from_date=start_date,
                to_date=end_date,
                limit=hours
            )
    
    async def get_multiple_quotes(self, symbols: List[str]) -> Dict[str, Any]:
        """Get quotes for multiple stocks"""
        results = {}
        async with PolygonMCPClient(self.polygon_api_key) as client:
            for symbol in symbols:
                quote_data = await self.get_stock_quote(symbol)
                results[symbol.upper()] = quote_data
                
                # Add small delay to avoid rate limits
                await asyncio.sleep(0.1)
        
        return results
    
    async def get_market_data_batch(self, symbols: List[str], timespan: str = "day", days: int = 7) -> Dict[str, Any]:
        """Get market data for multiple symbols"""
        results = {}
        async with PolygonMCPClient(self.polygon_api_key) as client:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            for symbol in symbols:
                data = await client.get_aggregates(
                    ticker=symbol,
                    multiplier=1,
                    timespan=timespan,
                    from_date=start_date,
                    to_date=end_date,
                    limit=days
                )
                results[symbol.upper()] = data
                
                # Add small delay to avoid rate limits
                await asyncio.sleep(0.1)
        
        return results
    
    async def get_comprehensive_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive stock analysis data"""
        try:
            # Get multiple timeframes for analysis
            current_quote = await self.get_stock_quote(symbol)
            daily_data = await self.get_historical_data(symbol, 30)
            weekly_data = await self.get_historical_data(symbol, 90)
            
            analysis = {
                "symbol": symbol.upper(),
                "current_quote": current_quote,
                "daily_trend": daily_data,
                "weekly_trend": weekly_data,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return analysis
        except Exception as e:
            return {"error": f"Failed to get comprehensive analysis for {symbol}: {str(e)}"}

# Initialize service instance
def get_stock_data_service():
    """Get stock data service instance"""
    import os
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    if not polygon_api_key:
        raise ValueError("POLYGON_API_KEY environment variable is required")
    
    return StockDataService(polygon_api_key)