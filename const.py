# const.py

#####BOT CONSTS######
status = ';;help'


######DB CONSTS#######
#db name
DB_NAME = 'census.db'

#bday
bday_entries = 'ID INT PRIMARY KEY     NOT NULL,    \
    YEAR INT                NOT NULL,               \
    MONTH INT               NOT NULL,               \
    DAY INT                 NOT NULL'                   
bday_types = 'ID,YEAR,MONTH,DAY'


#generic text
generic_entries = 'ID INT PRIMARY KEY     NOT NULL,    \
    CENSUS_RESPONSE TEXT                NOT NULL'               
generic_types = 'ID,CENSUS_RESPONSE'


######RESPONSES#######

#help responses
help_response = '__Census Bot Help Page__ \n\
`Create census question: ;;new {name} \n\
See list of census questions: ;;list \n\
See someones or your response: ;;check {name} {user} \n\
Change a response: #. {answer} OR ;;add {name} {answer} \n\
Delete your response ;;remove {name}`'                          

#error responses
error_response = 'There was an error running your command, try again later!'

#birthday reponses
birthday_response = 'Today is <@%d>\'s birthday! 🥳🎉🎂'
birthday_check_response = 'Their birthday is on %s'
birthday_add_response = 'Added <@%d>\'s birthday to my sus list'

#census responses
generic_check_response = 'Their response to census question %d is %s. %s'
interesting_response_list = ['Very cool!','Wow!','Interesting 🤔','Neat!']
list_response = 'Here is a list of current census polls: '
question_created_response = 'New census poll created! Please use %d. when answering 😊'