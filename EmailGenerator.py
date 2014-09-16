import CasaleClasses
import random, string

import MiscFunctions
import os

# seeding random generator
random.seed()

# here, we assume that there exists a database called 'casale_test' in the server
# 
emailDB = CasaleClasses.emailDatabase('asusanto','','localhost','casale_test')

# as per instruction, 'mailing' is set to be initially empty
# so if the table already exists, we will wipe it off here,
# as per the instruction. Here, we also assume that the 
# table mailing only contains one column, 'addr', and we will not 
# modify this table at all, as per the instruction. 

# for this simulation, we will have, in the end, two tables,
# 'mailing' and 'totalcount', where 'totalcount' keeps track
# of all the emails added for each day
emailDB.resetMailingTableInDatabase()
emailDB.resetDailyCountInDatabase()

# http://tinyurl.com/ooknlll

# this part will simulate the addition of new email addresses daily
# char_set = string.ascii_lowercase + string.digits


numberOfSimulationDays = 100
MiscFunctions.addEmailAddresses(emailDB, numberOfSimulationDays)

## print 'Committing now'
emailDB.cnx.commit()


dataFromLast30Days = emailDB.getPercentageGrowthTheLastNDays(30)

top_50 = dataFromLast30Days[:50]

for k in range(len(top_50)):
    print('%d : %s %.4f' % (k+1,top_50[k][0],100*top_50[k][1]))
    
