import datetime
def check_request_form(request_form, values):
    msg = ""
    for value in values:
        if value not in request_form or request_form[value] == "":
            msg += str(value) + " cannot be empty. "
    return msg

def get_date(strDate):
    dateMsg = ''
    datelist = strDate.split("-")
    if len(datelist) != 3:
        dateMsg += "The date must be formatted like yyyy-mm-dd"
        return dateMsg
    year = datelist[0]
    month = datelist[1]
    day = datelist[2]
    try:
        year = int(year)
        month = int(month)
        day = int(day)
    except:
        dateMsg += "Only type number for the date please"
        return dateMsg
    date = datetime.datetime(year, month, day)
    return date

def to_string(input):
    try:
        input = str(input)
    except:
        return None
    return input

def to_int(input):
    try:
        input = int(input)
    except:
        return None
    return int(input)