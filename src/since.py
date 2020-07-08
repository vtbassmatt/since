from datetime import date, datetime

from flask import Flask, render_template, jsonify

app = Flask(__name__)

SOME_HISTORICAL_DATES = [
    (date(1930, 7, 7), 'the death of Arthur Conan Doyle'),
    (date(1945, 9, 2), 'the official end of World War II'),
    (date(1947, 8, 15), 'Indian independence from the United Kingdom'),
    (date(1977, 8, 16), 'Elvis Presley\'s death'),
    (date(2008, 11, 4), 'Barack Obama\'s first presidential election victory'),
]

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/<request_date>")
def get_since(request_date):
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
            'date': request_date_cleaned,
            'days_since': days_since.days,
        },
        'historical_fact': {
            'searched_date': search_date,
        },
    }

    try:
        historical_thing = find_historical_thing(SOME_HISTORICAL_DATES, search_date)
        days_from_historical_to_request = (request_date_cleaned - historical_thing[0]).days

        if days_from_historical_to_request >= 0:
            response['historical_fact'].update({
                'found_date': historical_thing[0],
                'caption': historical_thing[1],
                'days_from_this_to_requested': days_from_historical_to_request,
            })

    except ValueError:
        pass

    return jsonify(response)


# dumbest possible implementation that works
def find_historical_thing(items, search_date):
    print(search_date)
    for i in range(len(items)):
        if items[i][0] > search_date:
            return items[i]
    raise ValueError("could not find a valid historical event")


def api_error(message):
    return jsonify({
        "error": message,
    })