from datetime import datetime
from flask import Flask, Response, render_template, jsonify

try:
    from commit import COMMIT, DEPLOY_DATE
    from history import find_historical_fact, FACT_COUNT
except ImportError:
    COMMIT = 'import-failed'
    DEPLOY_DATE = 'test'
    FACT_COUNT = 0

flask_app = Flask(__name__)

@flask_app.context_processor
def inject_version_info():
    return {
        'deployed_commit': COMMIT,
        'deployed_at': DEPLOY_DATE,
        'fact_count': FACT_COUNT,
    }

@flask_app.get("/return_http") 
def return_http(): 
    return Response('<h1>Hello World™</h1>', mimetype='text/html')

@flask_app.route("/base")
def home():
    return render_template('base.html')

@flask_app.route("/")
def index():
    return Response('<h1>Home sweet 🏡</h1>', mimetype='text/html')

@flask_app.route("/api/v1/<request_date>")
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
    
    try:
        search_date = request_date_cleaned - days_since
    except OverflowError:
        return api_error("Can't search that far back."), 404

    response = {
        'requested': {
            'date': request_date_cleaned.strftime('%Y-%m-%d'),
            'days_since': days_since.days,
        },
        'historical_fact': {
            'searched_date': search_date.strftime('%Y-%m-%d'),
        },
    }

    # try:
    #     historical_thing = find_historical_fact(search_date)
    #     days_from_historical_to_request = (request_date_cleaned - historical_thing[0]).days

    #     if days_from_historical_to_request >= 0:
    #         response['historical_fact'].update({
    #             'found_date': historical_thing[0].strftime('%Y-%m-%d'),
    #             'caption': historical_thing[1],
    #             'days_from_this_to_requested': days_from_historical_to_request,
    #         })
    #     else:
    #         return api_error("Everything we found was too far back."), 404

    # except exceptions.DateTooEarlyError:
    #     return api_error("No interesting facts that far back."), 404

    # except exceptions.DateTooLateError:
    #     return api_error("No interesting facts that recent."), 404

    # except ValueError:
    #     return api_error("Unspecified error"), 404

    return jsonify(response), 200


def api_error(message):
    return jsonify({
        "error": message,
    })
