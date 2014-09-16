import random, string

emailDomainNames = ['gmail', 'yahoo','hotmail','uwaterloo','casalemedia',
                    'glassdoor','linkedin','facebook','nasa','washington',
                    'google','microsoft','susanto','oneplus','samsung',
                    'meizu','singularity','plato','socrates','microtubule',
                    'consciousness']

emailExtension = ['.com','.edu','.ca','.cn','.in','.id','.io','.ky','.se','.hk']

def generateRandomEmailAddress():
    random.seed()
    char_set = string.ascii_lowercase + string.digits
    emailName = (''.join(random.sample(char_set*random.randint(4,9),
                                       random.randint(4,9))))
    emailDomain = (emailDomainNames[random.randint(0, len(emailDomainNames)-1)] + 
                   emailExtension[random.randint(0, len(emailExtension)-1)])


    
    return (emailName + '@' + emailDomain)

def addEmailAddresses(emailDB, numberOfSimulationDays):
    emailAddressesOfTheDay = []
    
    for m in range(numberOfSimulationDays):
        numberOfAddressesAdded = random.randint(1,200)
        
        for k in range(numberOfAddressesAdded):
            # emailName = ''.join(random.sample(char_set*random.randint(4,9), random.randint(4,9)))
            emailAddressesOfTheDay.append(generateRandomEmailAddress())
            # emailAddressesOfTheDay.append(emailName +'@'+
            #                               domainNames[random.randint(0,len(domainNames)-1)])        
            query_statement = ('INSERT INTO ' + emailDB.getEmailTableName() +
                               '(' + emailDB.getEmailColumnName() + ') VALUES (' +
                               '\'' + emailAddressesOfTheDay[k] + '\')' )
            
            emailDB.cursor.execute(query_statement)
            
        emailAddressesOfTheDay = []
           
        query_statement = ('INSERT INTO ' + emailDB.emailTotalCountTable  +
                           '( ' + emailDB.emailTotalCountColumn1 +', ' + emailDB.emailTotalCountColumn2 + ')'
                           ' VALUES (' + str(m+1) + ', ' +
                           str(numberOfAddressesAdded) + ')')
        
        emailDB.cursor.execute(query_statement)

def addEmailWithoutUpdatingCount(emailDB):
    # adding up to 200 email
    numberOfAddressesAdded = random.randint(1,random.randint(1,1000))
    emailAddressesOfTheDay = []
    for k in range(numberOfAddressesAdded):
        # emailName = ''.join(random.sample(char_set*random.randint(4,9), random.randint(4,9)))
        emailAddressesOfTheDay.append(generateRandomEmailAddress())
        # emailAddressesOfTheDay.append(emailName +'@'+
        #                               domainNames[random.randint(0,len(domainNames)-1)])        
        query_statement = ('INSERT INTO ' + emailDB.getEmailTableName() +
                           '(' + emailDB.getEmailColumnName() + ') VALUES (' +
                           '\'' + emailAddressesOfTheDay[k] + '\')' )
        
        emailDB.cursor.execute(query_statement)

    emailDB.cnx.commit()
