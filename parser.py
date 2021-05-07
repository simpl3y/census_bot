import sys
import re
import datefinder

#finds the first ID found in a string
def find_id(message):
    result = re.search('<@!(.+?)>', message)
    if(result):
        return result.group(1)

    return None

#finds the first date in a string
def find_date(message):
    result = list(datefinder.find_dates(message))
    if(result):
        birthday_entry = str(result[0])
        date = '%s-%s-%s' % ((birthday_entry[5:7],birthday_entry[8:10],birthday_entry[0:4]))
        return date

    return None

def find_census_answer(message):
    answer = []
    result = list(map(int, re.findall(r"(?<![^\s>])([0-9]+)\.", message)))
    if(not result):
        return None
    answer.append(result[0])
    answer.append(message.split("%d." % result[0],1)[1])
    print(answer)
    
    return answer

#finds time and returns in seconds
def find_time(message):
    time = 0
    count = 0
    msg_split = message.split(' ')
    print(msg_split)
    for word in msg_split:
        count += 1
        if ';;' in word:
            continue
        elif 'min' in word:
            try:
                # print("min found: %s" % msg_split[count-2])
                time += int(msg_split[count-2]) * 60 
            except:
                continue
        elif 'hr' in word or 'hour' in word:
            try:
                # print("hr found: %s" % msg_split[count-2])
                time += int(msg_split[count-2]) * 3600 
            except:
                continue
        elif 'day' in word:
            try:
                time += int(msg_split[count-2]) * 86400
            except:
                continue
        elif 'week' in word:
            try:
                time += int(msg_split[count-2]) * 86400 * 7
            except:
                continue
        elif '\"' in word:
            break

    return time


