import sys
import re
import datefinder


def find_id(message):
    result = re.search('<@!(.+?)>', message)
    if(result):
        return result.group(1)
    return None

def find_date(message):
    result = list(datefinder.find_dates(message))
    if(result):
        return str(result[0])
    return None

# def find_census_answer(message):

#     return None
