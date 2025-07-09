from agent import strategy_agent  # local import within the same folder

mock_input = {
    "stock_information_result": {
        "ticker": "AAPL",
        "current_price": 172.35,
        "rsi": 28.5,
        "sentiment_summary": "Investor sentiment is positive following strong earnings.",
        "valuation_summary": "Apple shows solid fundamentals with strong earnings and a low P/E ratio.",
        "recommendation": None
    }
}

def test_strategy_agent():
    print("Running test for strategy_agent...\n")
    result = strategy_agent.run(input=mock_input)
    print("Response:\n")
    print(result)

if __name__ == "__main__":
    test_strategy_agent()