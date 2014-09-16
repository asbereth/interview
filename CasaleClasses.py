import SQLClasses
import collections

class emailDatabase(SQLClasses.database):
    
    emailTableName = 'mailing'
    emailColumnName = 'addr'
    emailTotalCountTable = 'totalcount'
    emailTotalCountColumn1 = 'day'
    emailTotalCountColumn2 = 'daycount'
    
    def __init__(self, user, password, host, email_db_name):
        SQLClasses.database.__init__(self, user, password, host, email_db_name)

    def getDomainNames(self):
        entries = self.showColumnsInString(self.emailColumnName, self.emailTableName)
        domainNames = []
        
        for k in range(len(entries)):
            domainNames.append(entries[k].partition('@')[2])
        
        return domainNames

    def resetMailingTableInDatabase(self):
        try:
            query_statement = 'TRUNCATE ' + self.emailTableName
            self.cursor.execute(query_statement)
        except:
            query_statement = ('CREATE TABLE ' + self.emailTableName
                               + '(' + self.emailColumnName +
                               ' VARCHAR(255) NOT NULL)' )
            self.cursor.execute(query_statement)

    def resetDailyCountInDatabase(self):
        try:
            query_statement = 'TRUNCATE ' + self.emailTotalCountTable
            self.cursor.execute(query_statement)
        except:
            query_statement = ('CREATE TABLE ' + self.emailTotalCountTable
                               + '(' + self.emailTotalCountColumn1 + ' INT,' +
                               self.emailTotalCountColumn2 +  ' INT)' )
            ## print query_statement
            self.cursor.execute(query_statement)

    def howManyDaysCounted(self):
        statement = 'count(' + self.emailTotalCountColumn1 + ')'
        return int(self.showColumnsInString(statement,self.emailTotalCountTable)[0])

    def howManyEmailsCounted(self):
        statement = 'sum(' + self.emailTotalCountColumn2 + ')'
        return int(self.showColumnsInString(statement,self.emailTotalCountTable)[0])
    
    def howManyEmailsRecorded(self):
        statement = 'count(' + self.emailColumnName + ')'
        return int(self.showColumnsInString(statement,self.emailTableName)[0])

    def totalEmailsAddedTheLastNDays(self, N):
        if self.isCountUpdated():
            statement = ('SELECT sum(' + self.emailTotalCountColumn2 + ') FROM ' +
                         self.emailTotalCountTable + ' WHERE ' +
                         self.emailTotalCountColumn1 + ' >= ' +
                         str(self.howManyDaysCounted() - N + 1))
            self.cursor.execute(statement)
            return int(self.cursor.fetchall()[0][0])
        else:
            print 'WARNING: This operation will only include partial results from today!!\n' \
                  'Update is done only once every 24 hours!!!!'
            if N > 1:
                statement = ('SELECT sum(' + self.emailTotalCountColumn2 + ') FROM ' +
                             self.emailTotalCountTable + ' WHERE ' +
                             self.emailTotalCountColumn1 + ' >= ' +
                             str(self.howManyDaysCounted() - N + 2))
            elif N == 1:
                return (self.howManyEmailsRecorded() -
                        self.howManyEmailsCounted())
            # print statement
            self.cursor.execute(statement)
            return int(self.cursor.fetchall()[0][0] +
                       self.howManyEmailsRecorded() -
                       self.howManyEmailsCounted())
        # print statement


    def getDomainCountTotal(self):
        return dict(collections.Counter(self.getDomainNames()))

    def isCountUpdated(self):
        return self.howManyEmailsRecorded() == self.howManyEmailsCounted()

    ## the routine updateDailyCount() is performed only ONCE a day
    ## This part will not be simulated in this project, but in real life,
    ## this routine will performed only once per day
    def updateDailyCount(self):
        if self.isCountUpdated():
            print 'Count already up to date'
        else:
            numberOfDaysAlreadyRecorded = self.howManyDaysCounted()
            numberOfEmailsAddedToday = self.howManyEmailsRecorded() - self.howManyEmailsCounted()
            query_statement = ('INSERT INTO ' + self.emailTotalCountTable  +
                               '( ' + self.emailTotalCountColumn1 +', ' + self.emailTotalCountColumn2 + ')'
                               ' VALUES (' + str(numberOfDaysAlreadyRecorded+1) + ', ' +
                               str(numberOfEmailsAddedToday) + ')')
            self.cursor.execute(query_statement)
            self.cnx.commit()

    
    def getDomainCountFromLastNDays(self, N):
        if self.howManyEmailsRecorded() != self.howManyEmailsCounted():
            print 'WARNING: This operation will only include partial results from today!!\n' \
                  'Update is done only once every 24 hours!!!!'
        
        startingIndex = self.howManyEmailsCounted() - self.totalEmailsAddedTheLastNDays(N)
        return dict(collections.Counter( (self.getDomainNames())[startingIndex:] ))
        
    def getPercentageGrowthTheLastNDays(self, N):
        # keep in mind these two are dictionaries
        totalCounts = self.getDomainCountTotal()
        lastNDaysCounts = self.getDomainCountFromLastNDays(N)
        growthLastNDays = {}
        for k in lastNDaysCounts.keys():
            if k in totalCounts:
                growthLastNDays[k] = float(lastNDaysCounts[k])/totalCounts[k]
            else:
                growthLastNDays[k] = 1.0

        return sorted(growthLastNDays.items(), key=lambda growth: growth[1], reverse=True)
        
        ## return growthLastNDays
        
    def getEmailTableName(self):
        return self.emailTableName

    def getEmailColumnName(self):
        return self.emailColumnName
