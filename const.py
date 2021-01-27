# const.py

######DB CONSTS#######
#db name
DB_NAME = 'test.db'

#bday
bday_entries = 'ID INT PRIMARY KEY     NOT NULL,    \
    YEAR INT                NOT NULL,               \
    MONTH INT               NOT NULL,               \
    DAY INT                 NOT NULL'                   
bday_types = 'ID,YEAR,MONTH,DAY'


#generic text
generic_entries = 'ID INT PRIMARY KEY     NOT NULL,    \
    ENTRY TEXT                NOT NULL'               
generic_types = 'ID, ENTRY'


######RESPONSES#######

#help responses
help_response = 'This is the help function'

#error responses
error_response = 'There was an error running your command, try again later!'

#birthday reponses
birthday_response = 'Today is <@%d>\'s birthday! 🥳🎉🎂'
birthday_check_response = 'Their birthday is on %s'
birthday_add_response = 'Added <@%d>\'s birthday to my sus list'