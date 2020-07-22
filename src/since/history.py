from datetime import date


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


def find_historical_thing(search_date):
    "Find the oldest date in the database that's more recent than the searched date."
    return _linear_search(search_date)


# dumbest possible implementation that works
def _linear_search(search_date):
    for i in range(len(SOME_HISTORICAL_DATES)):
        if SOME_HISTORICAL_DATES[i][0] > search_date:
            return SOME_HISTORICAL_DATES[i]
    raise ValueError("could not find a valid historical event")
