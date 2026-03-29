def get_stock_ticker(nifty50_tickers, stock_name):
    tickers_dict = {}

    stock_name = stock_name.strip()

    try:
        ticker = nifty50_tickers[stock_name]
        tickers_dict[stock_name] = ticker

    except KeyError:
        print("❌ Stock not found in Nifty 50")

        # Suggest closest matches
        suggestions = [
            s for s in nifty50_tickers.keys()
            if stock_name.lower() in s.lower()
        ]

        if suggestions:
            print("Did you mean:")
            for s in suggestions[:5]:
                print(f" - {s}")

    return tickers_dict