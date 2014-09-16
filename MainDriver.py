import CasaleClasses
import random, string

import MiscFunctions
import os

os.system('reset')

# seeding random generator
random.seed()

# opening input file for database, we assume that there exists
# a database called 'casale_test'
f = open('input.txt')

config = []

for k in f:
    config.append(k.strip())

# only take the first four elements, to ensure there are no trailing spaces
config = config[0:4]
emailDB = CasaleClasses.emailDatabase(*config)

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

# this part represents the email addresses that have not been included
# in the daily count. These addresses represent addresses that have been
# added today (on a 24-hour cycle). Daily count is updated every 24 hour.
# The statistics that will be generated will be up to the point the last
# email address is added. 
MiscFunctions.addEmailWithoutUpdatingCount(emailDB)

## print 'Committing now'
emailDB.cnx.commit()

# total domain counts
f = open('output_count_total_top_50.txt','w')

domainNameCount = emailDB.getDomainCountTotal()
sortedDomainCount = sorted(domainNameCount.items(),
                           key=lambda growth: growth[1],
                           reverse=True)

for k in range(50):
    if k == 0:
        f.write(repr('rank').rjust(5))
        f.write(repr('domain').rjust(20))
        f.write(repr('count').rjust(20))
        f.write('\n')
    
    f.write(repr(k+1).rjust(5))
    f.write(repr(sortedDomainCount[k][0]).rjust(20))
    f.write(repr(sortedDomainCount[k][1]).rjust(20))
    f.write('\n')

f.close()

# domain counts for the past 30 days

f = open('output_count_30_days_top_50.txt','w')

domainNameCountLast30Days = emailDB.getDomainCountFromLastNDays(30)
sortedDomainNameCountLast30Days = sorted(domainNameCountLast30Days.items(),
                                         key=lambda growth: growth[1],
                                         reverse=True)

for k in range(50):
    if k == 0:
        f.write(repr('rank').rjust(5))
        f.write(repr('domain').rjust(20))
        f.write(repr('count').rjust(20))
        f.write('\n')
    
    f.write(repr(k+1).rjust(5))
    f.write(repr(sortedDomainNameCountLast30Days[k][0]).rjust(20))
    f.write(repr(sortedDomainNameCountLast30Days[k][1]).rjust(20))
    f.write('\n')

f.close()




# this part will only work if there are enough data to show statistics for the last 30 days
dataFromLast30Days = emailDB.getPercentageGrowthTheLastNDays(30)

top_50 = dataFromLast30Days[:50]
f = open('output_growth_30_days_top_50.txt','w')
    
for k in range(len(top_50)):
    if k == 0:
        f.write(repr('rank').rjust(5))
        f.write(repr('domain').rjust(20))
        f.write(repr('growth_percentage').rjust(20))
        f.write('\n')
        # print repr('rank').rjust(5),
        # print repr('domain').rjust(20),
        # print repr('growth_percentage').rjust(20)

    f.write(repr(k+1).rjust(5))
    f.write(repr(top_50[k][0]).rjust(20))
    f.write(repr('%.4f' % (100*top_50[k][1]) ).rjust(20))
    f.write('\n')
    # print repr(k+1).rjust(5),
    # print repr(top_50[k][0]).rjust(20),
    # print repr('%.4f' % (100*top_50[k][1]) ).rjust(20)
    ## print('%d : %s %.4f' % (k+1,top_50[k][0],100*top_50[k][1]))

f.close()
