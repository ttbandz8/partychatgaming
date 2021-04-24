import db
import time
import classes as data
import test_data as td

now = time.asctime()

'''User must have predefined roles of the games they play before creating users
   User input for IGN will be available after User is created and goes to join game events
   User input for TEAM will be available after User is created. There will be a command to add Team. '''


print(db.createSession(data.newSession(td.OneVsOne)))

