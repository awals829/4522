# Adv DB Winter 2024 - 1

import random
import csv

# ***Using this library to generate a random string of characters for the Transaction ID pweeease***
import string

data_base = []  # Global binding for the Database contents


'''
transactions = [['id1',' attribute2', 'value1'], ['id2',' attribute2', 'value2'],
                ['id3', 'attribute3', 'value3']]
'''
transactions = [['1', 'Department', 'Music'], ['5', 'Civil_status', 'Divorced'],
                ['15', 'Salary', '200000']]


# ***Gave this a definition to mimic attributes, is this fine UwU?***
DB_Log = [['transId', 'targetTable', 'empId', 'targetAttribute', 'valueBefore', 'valueAfter', 'success', 'ownerTransId']] # <-- You WILL populate this as you go
'''
Structure of 'DB_Log' = [['transId', 'targetTable', 'targetAttribute', 'valueBefore', 'valueAfter', 'success', 'ownerTransId']]

Documentation for DB_Log
'transId'       --> Identification key of the specific transaction.
**(The transaction Id will be a ran through a generator function to create a "unique" Id. 
Since each transaction is a hard-coded UPDATE, a 'U' will be appended to the beginning of the each transaction id.)**

'table'         --> Table the transaction is attempting to change.

'attribute'     --> The requested attribute to be changed for the transaction.

'targetTable'   --> The data table being changed

'empId'         --> The Id of the employee data being changed

'valueBefore'   --> The current attribute value in the table of selected transaction.

'valueAfter'    --> The new attribute value pending change of the selected transaction.

'success'       --> The state of the transaction. 'S' = Success, 'P' = Pending, 'F' = Failure.

'ownerTransId'  --> The id of the owner who ran the transaction. 
**(Since this is simulated, a random number based on the size of 
the of the Employees table will be generated to fill this space)**
'''

# ***Can we keep these? Don't make us lose the drip-code!***
''' Custom Functions '''

def generate_transId_sequence(size):
    all_characters = string.ascii_uppercase + string.digits  # includes letters (both cases) and digits
      
    # For Loop calls random.choice() until the size requested is hit, generating a random sequence.
    random_sequence = ''.join(random.choice(all_characters) for _ in range(size))
    return ("U-" + random_sequence) # 'U' For Update

def updateDbLog(success_status: str):
    index = DB_Log[0].index('success')
    for log in DB_Log:
        if log[index] == 'P':
            log[index] = success_status
            
''' End Of Custom Functions'''



def recovery_script(log:list, data_base:list ):  #<--- Your CODE
    logEmpIdIndex = log[0].index('empId') # Use this to acquire the Attribute index in the log
    logAttributeIndex = log[0].index('targetAttribute') # Use this to acquire the Attribute index in the log
    successIndex = log[0].index('success') # Use this to acquire the success index in the log
    valueBeforeIndex = log[0].index('valueBefore') # Use this to acquire the valueBefore index in the log
    
    for datalog in log:
        if datalog[successIndex] == 'F':
                attributeToRevert = datalog[logAttributeIndex]
                valueBefore = datalog[valueBeforeIndex]
                empId = datalog[logEmpIdIndex]
                databaseAttributeIndex = data_base[0].index(attributeToRevert)
                data_base[int(empId)][databaseAttributeIndex] = valueBefore

    print("Recovery in process ...\n")


def transaction_processing(transaction : list, data : list): #<-- Your CODE
    empId = int(transaction[0])
    targetAttribute = transaction[1]
    transId = generate_transId_sequence(8)
    indexOfAttribute = data[0].index(targetAttribute)
    attributeBeforeValue = data[empId][indexOfAttribute]
    attributeAfterValue = transaction[2]
    ownerTransId = random.randint(1, len(data))
        
    # data_base = ['Unique_ID', 'First_name', 'Last_name', 'Salary', 'Department', 'Civil_status']
    data[empId][indexOfAttribute] = attributeAfterValue
    
    # Structure of 'DB_Log' = [['transId', 'targetTable', 'empId', 'targetAttribute', 'valueBefore', 'valueAfter', 'success', 'ownerTransId']]     
    DB_Log.append([transId, 'Employees', transaction[0], targetAttribute, attributeBeforeValue, attributeAfterValue, 'P', ownerTransId])
    

def read_file(file_name:str)->list:
    '''
    Read the contents of a CSV file line-by-line and return a list of lists
    '''
    data = []
    #
    # one line at-a-time reading file
    #
    with open(file_name, 'r') as reader:
    # Read and print the entire file line by line
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            line = line.strip().split(',')
            data.append(line)
             # get the next line
            line = reader.readline()

    size = len(data)
    print('The data entries BEFORE updates are presented below:')
    for item in data:
        print(item)
    print(f"\nThere are {size} records in the database, including one header.\n")
    return data


def is_there_a_failure()->bool:
    '''
    Simulates randomly a failure, returning True or False, accordingly
    '''
    value = random.randint(0,1)
    if value == 1:
        result = True
    else:
        result = False
    return result


def main():
    number_of_transactions = len(transactions)
    must_recover = False
    data_base = read_file("Assignments\A1\CodeAndData\Employees_DB_ADV.csv")
    failing_transaction_index = None

    # Process transaction
    for index in range(number_of_transactions):
        print(f"\nProcessing transaction No. {index+1}.")    #<--- Your CODE (Call function transaction_processing)
        transaction_processing(transactions[index], data_base) # ***Defined function placed here***
        print("UPDATES have not been committed yet...\n")
        failure = is_there_a_failure()
        if failure:
            must_recover = True
            failing_transaction_index = index + 1
            print(f'There was a failure whilst processing transaction No. {failing_transaction_index}.')
            updateDbLog('F') # ***No idea if we need this, it just sets the logged pending transactions to the argument value.***
            break
        else:
            print(f'Transaction No. {index+1} has been commited! Changes are permanent.')
            updateDbLog('S') # ***No idea if we need this, it just sets the logged pending transactions to the argument value.***
                
    if must_recover:
        #Call your recovery script
        recovery_script(DB_Log, data_base) ### Call the recovery function to restore DB to sound state
        
        print(f"The Transaction That Failed Was: {transactions[failing_transaction_index-1]}\n") # ***Group Test Print Remove Later***
    else:
        # All transactions ended up well
        print("All transaction ended up well.")
        print("Updates to the database were committed!\n")
    
    

    print('The data entries AFTER updates -and RECOVERY, if necessary- are presented below:')
    for item in data_base:
        print(item)
        
    print(f"\nLogged Transactions are:\n{'\n'.join(map(str, DB_Log[1:]))}")

main()
