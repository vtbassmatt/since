from datetime import datetime

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/<historical_date>")
def get_since(historical_date):
    try:
        parsed_date = datetime.strptime(historical_date, '%Y-%m-%d')
    except ValueError as e:
        return f"Could not parse date: {e}", 400
    
    actual_date = parsed_date.date()
    today = datetime.utcnow().date()
    days_since = today - actual_date

    if days_since.days <= 0:
        return f"Must pick a date before {today}", 400

    return str(days_since.days)
