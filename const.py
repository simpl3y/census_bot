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
Delete your response ;;remove {name} \n\
Create a reminder ;;remindme {time} \"{message}\" \n\
Generate receipts ;;receipt`'                          

#error responses
error_response = 'Unknown command! Try `;;help` to see all my commands!'

#birthday reponses
birthday_response = 'Today is <@%d>\'s birthday! 🥳🎉🎂'
birthday_check_response = 'Their birthday is on %s'
birthday_add_response = 'Added <@%d>\'s birthday to my sus list'

#census responses
generic_check_response = 'Their response to census question %d is %s. %s'
interesting_response_list = ['Very cool!','Wow!','Interesting 🤔','Neat!']
list_response = 'Here is a list of current census polls: '
question_created_response = 'New census poll created! Please use %d. when answering 😊'

#reciept response
receipt_message_response = 'I got the receipts! <@%d> said `%s`'
image_types = ["png", "jpeg", "gif", "jpg"]

#remindme consts stuff
REMINDME_CSV = 'remindme.csv'
REMINDME_FORMAT = ['ID','TIME','MESSAGE']
REMINDME_MESSAGE = '<@%s> I\'m reminding you to %s!'