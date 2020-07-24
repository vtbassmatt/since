from bisect import bisect_right
from datetime import date

from . import exceptions


_SOME_HISTORICAL_DATES = [
    ('1066-10-14', "the Battle of Hastings (Norman conquest)"),
    ('1492-10-12', "Christopher Columbus makes landfall in the Caribbean"),
    ('1776-07-04', "the signing of the Declaration of Independence"),
    ('1859-11-24', "publication of Darwin's On the Origin of Species"),
    ('1930-07-07', "the death of Arthur Conan Doyle"),
    ('1935-05-30', "Babe Ruth's last career game"),
    ('1940-03-02', "Elmer Fudd's cartoon debut"),
    ('1945-09-02', "the official end of World War II"),
    ('1947-08-15', "Indian independence from the United Kingdom"),
    ('1950-03-08', "the first Volkswagen Type 2 (Microbus) rolling off the assembly line"),
    ('1955-07-17', "Disneyland opening in Anaheim"),
    ('1958-07-29', "NASA's founding"),
    ('1960-02-01', "the Greensboro sit-in at Woolworth's"),
    ('1965-08-06', "the Voting Rights Act being signed into law"),
    ('1970-04-13', "Apollo 13's oxygen tank exploding"),
    ('1977-08-16', "Elvis Presley's death"),
    ('1980-05-18', "Mount St. Helens's eruption"),
    ('1982-10-01', "DisneyWorld's EPCOT opening"),
    ('1985-10-18', "the NES launch in New York"),
    ('1987-12-09', "the introduction of Windows 2.0"),
    ('1991-12-26', "the end of the USSR"),
    ('1993-09-21', "the release of Nirvana's In Utero"),
    ('1995-04-19', "the Oklahoma City bombing"),
    ('1998-08-15', "the launch of the iMac"),
    ('2001-09-11', "the destruction of the World Trade Center"),
    ('2005-02-14', "the launch of YouTube"),
    ('2008-11-04', "Barack Obama's first presidential election victory"),
    ('2013-02-28', "Pope Benedict XVI's resignation"),
    ('2017-03-02', "Snapchat's IPO"),
    ('2018-05-19', "Prince Harry married Meghan Markle"),
    ('2018-11-11', "the 100th anniversary of the end of World War I"),
    ('2019-04-26', "Avengers: Endgame was released"),
    ('2019-12-18', "Donald Trump's impeachment"),
]

def parse_date(date_str):
    "Turn a yyyy-mm-dd string into a date"
    return date(*map(int, date_str.split('-')))

DATES = [parse_date(x[0]) for x in _SOME_HISTORICAL_DATES]
EVENTS = [x[1] for x in _SOME_HISTORICAL_DATES]
FACT_COUNT = len(EVENTS)
del _SOME_HISTORICAL_DATES

def find_historical_fact(search_date):
    "Find the oldest date more recent than the searched date."
    if search_date < DATES[0]:
        raise exceptions.DateTooEarlyError
    if search_date > DATES[-1]:
        raise exceptions.DateTooLateError

    index = _find_gt(DATES, search_date)
    return DATES[index], EVENTS[index]


# https://docs.python.org/3/library/bisect.html#searching-sorted-lists
def _find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        # return the index, not the item
        return i
    raise ValueError
