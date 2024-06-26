from id_dates import IdDates


def compare(strava: IdDates, ebird: IdDates) -> bool:
    return strava.end_date < ebird.start_date and strava.start_date > ebird.end_date