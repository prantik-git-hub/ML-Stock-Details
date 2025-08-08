from flask import Flask, request, jsonify, render_template
import yfinance as yf
from datetime import datetime, timedelta
from app import app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("analysis.html")  # Page with form to input ticker

@app.route("/analyze", methods=["GET"])
def analyze_stock():
    ticker = request.args.get("ticker", "").upper()

    if not ticker:
        return render_template("result.html", error="Ticker symbol is required.")

    try:
        stock = yf.Ticker(ticker)

        # Fetch history: ensure last 5 trading days ending at yesterday
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        history = stock.history(start=start_date, end=end_date)

        if history.empty:
            raise ValueError("No price history found.")

        # Get last 5 trading days
        history = history.tail(5)
        recent_history = history.reset_index()[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        recent_history = recent_history.to_dict(orient="records")

        info = stock.info

        result = {
            'company_name': info.get('longName', 'N/A'),
            'ticker': ticker,
            'sector': info.get('sector', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'current_price': info.get('currentPrice', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'dividend_yield': round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 'N/A',
            'recent_history': recent_history,
            'pros': [],
            'cons': [],
            'summary': ''
        }

        # Evaluate pros
        if info.get('dividendYield'):
            result['pros'].append("Pays regular dividends")
        if info.get('trailingPE') and info['trailingPE'] < 15:
            result['pros'].append("Low P/E ratio (possibly undervalued)")
        if info.get('marketCap') and info['marketCap'] > 10**10:
            result['pros'].append("Large market capitalization")

        # Evaluate cons
        if info.get('trailingPE') and info['trailingPE'] > 50:
            result['cons'].append("High P/E ratio (potential overvaluation)")
        if not info.get('dividendYield'):
            result['cons'].append("Does not pay dividends")

        # Summary logic
        if result['pros'] and result['cons']:
            result['summary'] = "This stock has both strengths and weaknesses based on key financial indicators."
        elif result['pros']:
            result['summary'] = "This stock shows promising financial indicators."
        elif result['cons']:
            result['summary'] = "This stock may have some financial red flags to consider."
        else:
            result['summary'] = "Limited data available to evaluate this stock."

        return render_template("result.html", result=result)

    except Exception as e:
        return render_template("result.html", error=f"Failed to analyze stock: {str(e)}")



# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
