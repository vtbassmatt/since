from datetime import date, datetime

from flask import Flask, render_template, jsonify, abort

from .commit import COMMIT

app = Flask(__name__)

SOME_HISTORICAL_DATES = [
    (date(1776, 7, 4), "the signing of the Declaration of Independence"),
    (date(1859, 11, 24), "publication of Darwin's On the Origin of Species"),
    (date(1930, 7, 7), "the death of Arthur Conan Doyle"),
    (date(1945, 9, 2), "the official end of World War II"),
    (date(1947, 8, 15), "Indian independence from the United Kingdom"),
    (date(1955, 7, 17), "Disneyland opening in Anaheim"),
    (date(1965, 8, 6), "the Voting Rights Act being signed into law"),
    (date(1970, 4, 13), "Apollo 13's oxygen tank exploding"),
    (date(1977, 8, 16), "Elvis Presley's death"),
    (date(1980, 5, 18), "Mount St. Helens's eruption"),
    (date(1982, 10, 1), "DisneyWorld's EPCOT opening"),
    (date(1985, 10, 18), "the NES launch in New York"),
    (date(1987, 12, 9), "the introduction of Windows 2.0"),
    (date(1991, 12, 26), "the end of the USSR"),
    (date(1993, 9, 21), "the release of Nirvana's In Utero"),
    (date(1995, 4, 19), "the Oklahoma City bombing"),
    (date(1998, 8, 15), "the launch of the iMac"),
    (date(2001, 9, 11), "the destruction of the World Trade Center"),
    (date(2005, 2, 14), "the launch of YouTube"),
    (date(2008, 11, 4), "Barack Obama's first presidential election victory"),
    (date(2013, 2, 28), "Pope Benedict XVI's resignation"),
    (date(2017, 3, 2), "Snapchat's IPO"),
    (date(2018, 5, 19), "Prince Harry married Meghan Markle"),
    (date(2018, 11, 11), "the 100th anniversary of the end of World War I"),
    (date(2019, 4, 26), "Avengers: Endgame was released"),
    (date(2019, 12, 18), "Donald Trump's impeachment"),
]

@app.route("/")
def home():
    return render_template('home.html', commit=COMMIT[0:7])


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
        historical_thing = find_historical_thing(SOME_HISTORICAL_DATES, search_date)
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


# dumbest possible implementation that works
def find_historical_thing(items, search_date):
    for i in range(len(items)):
        if items[i][0] > search_date:
            return items[i]
    raise ValueError("could not find a valid historical event")


def api_error(message):
    return jsonify({
        "error": message,
    })
