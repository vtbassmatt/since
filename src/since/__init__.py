from datetime import datetime

from flask import Flask, render_template, jsonify, abort

from .commit import COMMIT, DEPLOY_DATE
from .history import find_historical_fact, FACT_COUNT

app = Flask(__name__)


@app.context_processor
def inject_version_info():
    return {
        'deployed_commit': COMMIT[0:7],
        'deployed_at': DEPLOY_DATE,
        'fact_count': FACT_COUNT,
    }


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/since/<request_date>")
def since_page(request_date):
    try:
        parsed_date = datetime.strptime(request_date, '%Y-%m-%d')
    except ValueError:
        abort(404)
    
    string_date = parsed_date.strftime('%Y-%m-%d')
    api_response = since_api(string_date)

    return render_template(
        'since.html',
        rdate=string_date,
        api_response=api_response.get_json())


@app.route("/api/v1/<request_date>")
def since_api(request_date):
    try:
        parsed_date = datetime.strptime(request_date, '%Y-%m-%d')
    except ValueError as e:
        return api_error(f"Could not parse date: {e}"), 400
    
    request_date_cleaned = parsed_date.date()
    today = datetime.utcnow().date()
    days_since = today - request_date_cleaned

    if days_since.days <= 0:
        return api_error(f"Must pick a date before {today}"), 400
    
    search_date = request_date_cleaned - days_since

    response = {
        'requested': {
            'date': request_date_cleaned.strftime('%Y-%m-%d'),
            'days_since': days_since.days,
        },
        'historical_fact': {
            'searched_date': search_date.strftime('%Y-%m-%d'),
        },
    }

    try:
        historical_thing = find_historical_fact(search_date)
        days_from_historical_to_request = (request_date_cleaned - historical_thing[0]).days

        if days_from_historical_to_request >= 0:
            response['historical_fact'].update({
                'found_date': historical_thing[0].strftime('%Y-%m-%d'),
                'caption': historical_thing[1],
                'days_from_this_to_requested': days_from_historical_to_request,
            })

    except ValueError:
        pass

    return jsonify(response)


def api_error(message):
    return jsonify({
        "error": message,
    })
