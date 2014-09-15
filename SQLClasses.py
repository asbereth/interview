import mysql.connector
import datetime

class database(object):
    # from mysql.connector import errorcode

    def __init__(self, user, password, host, database_name):
        
            
        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database_name,
        }
        
        # print self.config
        # self.trollPrint(config)
        self.cnx = self.connectToADatabase(config)
        self.cursor = self.cnx.cursor(buffered=True)
        # self.cnx = mysql.connector.connect(**self.config)

    def connectToADatabase(self, config):
        # this part is a routine to connect to a database given
        # by a dictionary, config
        # I got this routine from the website
        # http://dev.mysql.com/doc/connectors/en/connector-python-example-connecting.html
        try:
            # the ** basically indicates that connect takes config as kwargs, where
            # a dictionary is converted onto keyword arguments
            cnx = mysql.connector.connect(**config)
            return cnx
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print 'Database', database_name, 'does not exists'
            else:
                print(err)

    def getTableNames(self):
        self.cursor.execute('SHOW tables')
        return self.cursor.fetchall()
    # return mysql.connector.connect(**config)
    
    def getColumnNamesFromTable(self, tableName):
        query_statement = 'DESC ' + tableName
        self.cursor.execute(query_statement)
        #self.cursor.execute(query_statement, tableName)
        return self.cursor.fetchall()

    def getColumnNamesFromTableInString(self, tableName):
        dummy_names = self.getColumnNamesFromTable(tableName)
        number_of_columns = len(dummy_names)
        
        buffer = [];
        for k in range(number_of_columns):
            buffer.append(str(dummy_names[k][0]))
        return buffer
    
    def showColumns(self, columnName, tableName):
        # query_statement = 'SELECT %s FROM %s'
        query_statement = 'SELECT ' + columnName +  ' FROM ' + tableName
        self.cursor.execute(query_statement)
        # self.cursor.execute(query_statement, (columnName, tableName))
        
        # self.cursor.execute('SELECT ' + columnName +
        #                     ' FROM ' + tableName)
        return self.cursor.fetchall()

    def showColumnsInString(self, columnName, tableName):
        dummy_buffer = self.showColumns(columnName, tableName)
        number_of_entries = len(dummy_buffer)

        buffer = []
        for k in range(number_of_entries):
            try: 
                buffer.append(str(dummy_buffer[k][0]))
            except UnicodeEncodeError:
                buffer.append( dummy_buffer[k][0].encode('utf-8') )

        return buffer
