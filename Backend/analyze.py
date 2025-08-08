# app/analyze.py

import yfinance as yf
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for
from transformers import pipeline

main = Blueprint('main', __name__)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Home route that displays the form and handles submission

@main.route('/analyze', methods=['GET'])
def analyze():
    return render_template('analysis.html')



# Result route that displays the stock analysis
@main.route('/result', methods=['GET'])
def result():
    ticker = request.args.get('ticker', '').upper().strip()

    if not ticker:
        return render_template('results.html', error="No ticker provided.")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or 'shortName' not in info:
            raise ValueError("Ticker not found or no data available.")

        # Basic stock data
        result = {
            'company_name': info.get('shortName', 'N/A'),
            'ticker': ticker,
            'sector': info.get('sector', 'N/A'),
            'market_cap': human_format(info.get('marketCap')),
            'current_price': info.get('currentPrice', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'dividend_yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else "N/A"
        }

        # Price history (last 5 days)
        history = stock.history(period="5d").reset_index()
        result['recent_history'] = history.to_dict(orient='records')

        # Prepare text for summarization
        summary_input = f"""
        Company: {result['company_name']}
        Sector: {result['sector']}
        Market Cap: {result['market_cap']}
        Price: {result['current_price']}
        P/E Ratio: {result['pe_ratio']}
        Dividend Yield: {result['dividend_yield']}
        Last 5 Days Prices: {[row['Close'] for row in result['recent_history']]}
        """

        # ML-based summarization
        summary = summarizer(summary_input, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        result['summary'] = summary

        # Auto-generate pros and cons
        result['pros'], result['cons'] = generate_pros_cons(summary)

        return render_template('results.html', result=result)

    except Exception as e:
        return render_template('results.html', error=str(e))


# Human-readable market cap
def human_format(num):
    if not num:
        return "N/A"
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.1f%s' % (num, ['', 'K', 'M', 'B', 'T'][magnitude])


# Extract pros and cons using keyword matching
def generate_pros_cons(summary_text):
    pros, cons = [], []
    summary_text = summary_text.lower()

    if "strong" in summary_text or "high" in summary_text:
        pros.append("Strong market presence or valuation.")
    if "dividend" in summary_text:
        pros.append("Pays consistent dividends.")
    if "low p/e" in summary_text:
        pros.append("Undervalued based on P/E ratio.")
    if "growth" in summary_text:
        pros.append("Positive growth potential.")

    if "volatile" in summary_text or "risk" in summary_text:
        cons.append("Price shows high volatility.")
    if "decline" in summary_text:
        cons.append("Recent decline in performance.")
    if "high p/e" in summary_text:
        cons.append("Overvalued based on P/E ratio.")
    if "low dividend" in summary_text:
        cons.append("Poor dividend returns.")

    if not pros:
        pros.append("No strong pros found.")
    if not cons:
        cons.append("No significant cons.")

    return pros, cons


# Optional: reusable logic for testing or APIs
def get_stock_analysis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period="5d").reset_index()

    return {
        'company_name': info.get('shortName', 'N/A'),
        'ticker': ticker,
        'current_price': info.get('currentPrice', 'N/A'),
        '20_day_ma': history['Close'].rolling(window=20).mean().iloc[-1] if len(history) >= 20 else 'N/A',
        'latest_close': history['Close'].iloc[-1] if not history.empty else 'N/A',
        'volume': history['Volume'].iloc[-1] if not history.empty else 'N/A',
        'message': 'Generated from API.'
    }
