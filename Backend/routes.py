from flask import Flask, Blueprint, render_template, request, redirect, url_for, send_file
from io import BytesIO
import json
from flask import request, jsonify
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import yfinance as yf
import os
app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with your actual secret key
bp = Blueprint('main', __name__)  # Renamed from 'bp' to 'main'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if not exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@bp.route('/upload-json', methods=['POST'])
def upload_json():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.json'):
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)
        return jsonify({'message': 'File received!', 'filename': file.filename})

    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/api/analyze-stock/', methods=['POST'])
def analyze_stock_file():
    uploaded_file = request.files.get('file')
    
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        json_data = json.load(uploaded_file)
        ticker = json_data.get("ticker")
        return jsonify({"ticker": ticker, "message": "File received!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@bp.route('/api/analyze-stock/', methods=['POST'])
def analyze_stock_api():
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper()

        if not ticker:
            return jsonify({"error": "Ticker is required"}), 400

        stock = yf.Ticker(ticker)
        info = stock.info

        if "shortName" not in info:
            return jsonify({"error": "Invalid ticker"}), 404

        pe = info.get("trailingPE", "N/A")
        dy = info.get("dividendYield", "N/A")

        pros = []
        cons = []

        if isinstance(pe, (int, float)):
            if pe < 15:
                pros.append("Low P/E ratio, undervalued")
            if pe > 30:
                cons.append("High P/E ratio")
        else:
            cons.append("P/E ratio not available")

        if isinstance(dy, (int, float)):
            if dy > 0.02:
                pros.append("Good dividend yield")
            else:
                cons.append("Low dividend yield")
        else:
            cons.append("Dividend yield not available")

        return jsonify({
            "ticker": ticker,
            "company": info.get("longName", "N/A"),
            "pe_ratio": pe,
            "dividend_yield": dy,
            "pros": pros,
            "cons": cons
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
def generate_analysis_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # Attempt NSE ticker if regular one is invalid
    if 'shortName' not in info or not info['shortName']:
        ticker += ".NS"
        stock = yf.Ticker(ticker)
        info = stock.info
        if 'shortName' not in info or not info['shortName']:
            raise ValueError("Invalid ticker symbol.")

    result = {
        "company_name": info.get("longName", "N/A"),
        "ticker": ticker,
        "sector": info.get("sector", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "current_price": info.get("currentPrice", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "dividend_yield": info.get("dividendYield", "N/A"),
        "pros": [],
        "cons": [],
        "price_history": [],
    }

    pe = result["pe_ratio"]
    dy = result["dividend_yield"]

    if isinstance(pe, (int, float)):
        if pe < 15:
            result["pros"].append("Low P/E ratio, may be undervalued.")
        elif pe > 30:
            result["cons"].append("High P/E ratio, may be overvalued.")
    else:
        result["cons"].append("P/E ratio not available.")

    if isinstance(dy, (int, float)):
        if dy > 0.02:
            result["pros"].append("Attractive dividend yield.")
        else:
            result["cons"].append("Low dividend yield.")
    else:
        result["cons"].append("Dividend yield not available.")

    # Fetch price history for past 5 days (excluding today)
    hist = stock.history(period="6d")
    if not hist.empty:
        hist = hist.reset_index()
        today_str = datetime.today().strftime("%Y-%m-%d")
        filtered = hist[hist["Date"].dt.strftime("%Y-%m-%d") < today_str].tail(5)
        for _, row in filtered.iterrows():
            result["price_history"].append({
                "Date": row["Date"].strftime("%Y-%m-%d"),
                "Open": round(row["Open"], 2),
                "High": round(row["High"], 2),
                "Low": round(row["Low"], 2),
                "Close": round(row["Close"], 2),
                "Volume": int(row["Volume"]),
            })

    return result


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/analyze", methods=["POST"])
def analyze_stock():
    ticker = request.form.get("ticker", "").strip().upper()
    if not ticker:
        return redirect(url_for("main.index", error="No ticker provided."))
    return redirect(url_for("main.results", ticker=ticker))


@bp.route("/results")
def results():
    ticker = request.args.get("ticker", "").strip().upper()
    if not ticker:
        return render_template("results.html", error="No ticker provided.")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if 'shortName' not in info or not info['shortName']:
            ticker += ".NS"
            stock = yf.Ticker(ticker)
            info = stock.info
            if 'shortName' not in info or not info['shortName']:
                return render_template("results.html", error="Invalid ticker symbol.")

        result = {
            "company_name": info.get("longName", "N/A"),
            "ticker": ticker,
            "sector": info.get("sector", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "current_price": info.get("currentPrice", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "pros": [],
            "cons": [],
            "recent_history": [],
            "summary": ""
        }

        pe = result["pe_ratio"]
        dy = result["dividend_yield"]

        if isinstance(pe, (int, float)):
            if pe < 15:
                result["pros"].append("Low P/E ratio, may be undervalued.")
            elif pe > 30:
                result["cons"].append("High P/E ratio, may be overvalued.")
        else:
            result["cons"].append("P/E ratio not available.")

        if isinstance(dy, (int, float)):
            if dy > 0.02:
                result["pros"].append("Attractive dividend yield.")
            else:
                result["cons"].append("Low dividend yield.")
        else:
            result["cons"].append("Dividend yield not available.")

        hist = stock.history(period="5d")
        if not hist.empty:
            hist = hist.reset_index()
            for _, row in hist.iterrows():
                result["recent_history"].append({
                    "Date": row["Date"].strftime("%Y-%m-%d"),
                    "Open": round(row["Open"], 2),
                    "High": round(row["High"], 2),
                    "Low": round(row["Low"], 2),
                    "Close": round(row["Close"], 2),
                    "Volume": int(row["Volume"]),
                })

        return render_template("results.html", result=result)

    except Exception as e:
        return render_template("results.html", error=f"Failed to analyze stock: {str(e)}")


@bp.route("/download/<ticker>")
def download_result(ticker):
    try:
        result = generate_analysis_data(ticker)
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        y = height - 50
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, f"Stock Analysis Report: {result['ticker'].upper()}")
        y -= 30

        p.setFont("Helvetica", 11)
        p.drawString(50, y, f"Company: {result['company_name']}")
        y -= 20
        p.drawString(50, y, f"Sector: {result['sector']}")
        y -= 20
        p.drawString(50, y, f"Market Cap: {result['market_cap']}")
        y -= 20
        p.drawString(50, y, f"Current Price: {result['current_price']}")
        y -= 20
        p.drawString(50, y, f"P/E Ratio: {result['pe_ratio']}")
        y -= 20
        p.drawString(50, y, f"Dividend Yield: {result['dividend_yield']}")
        y -= 30

        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Price History (Last 5 Days):")
        y -= 20
        p.setFont("Helvetica", 10)
        for row in result['price_history']:
            if y < 60:
                p.showPage()
                y = height - 50
            p.drawString(60, y, f"{row['Date']} - O:{row['Open']} H:{row['High']} L:{row['Low']} C:{row['Close']} V:{row['Volume']}")
            y -= 15

        if y < 100:
            p.showPage()
            y = height - 50

        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Pros:")
        y -= 20
        p.setFont("Helvetica", 10)
        for pro in result['pros']:
            p.drawString(60, y, f"• {pro}")
            y -= 15

        y -= 10
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, "Cons:")
        y -= 20
        p.setFont("Helvetica", 10)
        for con in result['cons']:
            p.drawString(60, y, f"• {con}")
            y -= 15

        p.showPage()
        p.save()
        buffer.seek(0)

        filename = f"{ticker.upper()}_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')

    except Exception as e:
        return render_template("results.html", error=f"Failed to generate PDF: {str(e)}")


# Register blueprint
app.register_blueprint(bp)
