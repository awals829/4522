# Adv DB Winter 2024 - 1

# Incredibly Redundant, But Pretty, Header For ... Reasons...
'''
===================================================================================================
=======================          ASSIGNMENT #1 WINTER 2024                  =======================
=======================          COMP 4522 ADVANCED DATABASES               =======================
=======================          GROUP: ANDREW W., RUTU K., BRANDON K.      =======================
=======================          DUE: FEBRUARY 14                           =======================
===================================================================================================
'''

import random
import csv


import os
import string
'''
NOTE:
Imported the 'os' library to aid with file reader as the file was having issues being found.
To ensure this runs, make sure the two files 'advdb-1.py' & 'Employees_DB_ADV.csv' are in the same folder.

Imported the 'string' library to give access to the ascii characters for the transaction ID in the DB_Log
as well as the custom function 'generate_transId_sequence()'.
'''


# =================================================================================================
# =================================================================================================


data_base = [] # Global binding for the Database contents


'''
transactions = [['id1',' attribute2', 'value1'], ['id2',' attribute2', 'value2'],
                ['id3', 'attribute3', 'value3']]
'''

'''
NOTE:
Added 5 more test transactions to test program generalization.
'''
transactions = [
                ['1', 'Department', 'Music'], 
                ['5', 'Civil_status', 'Divorced'],
                ['15', 'Salary', '200000'],
                ['4', 'First_name', 'Bill'],
                ['4','Civil_status','Single'],
                ['8','Salary','350000'],
                ['12','Department','Engineering'],
                ['2','First_name','Jane']
            ]


# =================================================================================================
# =================================================================================================


DB_Log = [['transId', 'targetTable', 'empId', 'targetAttribute', 'valueBefore', 'valueAfter', 'success', 'ownerTransId']] # <-- You WILL populate this as you go
"""
Details:

    Structure of 'DB_Log' = [[\n
    'transId',\n 
    'targetTable',\n 
    'targetAttribute',\n 
    'valueBefore',\n
    'valueAfter',\n 
    'success',\n
    'ownerTransId'\n
    ]]\n

Attributes:

    'transId'       --> Identification key of the specific transaction.

    'table'         --> Table the transaction is attempting to change.

    'attribute'     --> The requested attribute to be changed for the transaction.

    'targetTable'   --> The data table being changed

    'empId'         --> The Id of the employee data being changed

    'valueBefore'   --> The current attribute value in the table of selected transaction.

    'valueAfter'    --> The new attribute value pending change of the selected transaction.

    'success'       --> The state of the transaction. 
                        'S' = Committed, 'P' = Not-Executed, 'F' = Rolled-Back.

    'ownerTransId'  --> The id of the owner who ran the transaction.
"""


# =================================================================================================
# =================================================================================================
''' Start Of Custom Variables and Functions '''

P = "Not-Executed"  # Pending
S = "Committed"     # Success
F = "Rolled-Back"   # Failure

def generate_transId_sequence(size : int, crud_type : chr) -> str:
    """
    Generates a 'unique' transaction Id for the DB_log using a CRUD character and a random sequence of numbers and letters
    appended to the CRUD character. For example, if the size is 6 and the crud_type is 'C', the generated sequence could
    look like: C-5TUI8Q.

    Args:
        size (int): amount of characters for the sequence to generate.
        crud_type (chr): CRUD type to append to the front of the sequence. Ex. 'U' for update.

    Returns:
        str: Returns a random sequence of letters and numbers according to the size parameter and crud_type character.
    """
    all_characters = string.ascii_uppercase + string.digits  # includes letters (both cases) and digits
      
    # For Loop calls random.choice() until the size requested is hit, generating a random sequence.
    random_sequence = ''.join(random.choice(all_characters) for _ in range(size))
    return (crud_type + '-' + random_sequence)


# =================================================================================================
# =================================================================================================


def updateDbLog(success_status: str):
    """
    Updates the Database Log with all current pending ('P') entries, to the new parameter success state. 
    Failure ('F') or Success ('S'). This function does not check for a valid success_state character entry. 
    Useful to make changes to all pending success states in the DB_Log.

    Args:
        success_status (str): The character to place into the DB_Log success attribute.
    """
    index = DB_Log[0].index('success')
    for log in DB_Log:
        if log[index] == P:
            log[index] = success_status
 
 
# =================================================================================================
# ================================================================================================= 
       
           
def writeOutput(data : list , file_name : str):
    """
    Writes the output of a list of items to a csv file using the requested filename. 
    The file being written to will appear in the relative path of the current file.
    This is useful for seeing output without printing the Log and Database continuously,
    or if the data needs to be accessed elsewhere.
    
    Args:
        data (list): list to print to the csv file.
        file_name (str): the filename to output to, will create a new file with this name, 
        or overwrite a current file with the same name.
    """
    directory = os.path.dirname(os.path.realpath(__file__)) + file_name 
    with open(directory, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in data:
            writer.writerow(_)


''' End Of Custom Variables and Functions '''
# =================================================================================================
# =================================================================================================



def recovery_script(log:list):  #<--- Your CODE
    logEmpIdIndex = log[0].index('empId') # Use this to acquire the Attribute index in the log
    logAttributeIndex = log[0].index('targetAttribute') # Use this to acquire the Attribute index in the log
    successIndex = log[0].index('success') # Use this to acquire the success index in the log
    valueBeforeIndex = log[0].index('valueBefore') # Use this to acquire the valueBefore index in the log
    
    for datalog in log:
        if datalog[successIndex] == F:
                attributeToRevert = datalog[logAttributeIndex]
                valueBefore = datalog[valueBeforeIndex]
                empId = datalog[logEmpIdIndex]
                databaseAttributeIndex = data_base[0].index(attributeToRevert)
                data_base[int(empId)][databaseAttributeIndex] = valueBefore

    print("Recovery in process ...\n")


# =================================================================================================
# =================================================================================================


def transaction_processing(transaction : list, data : list): #<-- Your CODE
    '''
    NOTE:
    Only runs transaction_processing provided the lists have values
    to use. It is assumed that values being changed are valid.
    '''
    if (len(data) > 1 and len(transaction) > 0):
        empId = int(transaction[0])
        targetAttribute = transaction[1]
        transId = generate_transId_sequence(4, 'U') # <-- Custom Function Call.
        indexOfAttribute = data[0].index(targetAttribute)
        attributeBeforeValue = data[empId][indexOfAttribute]
        attributeAfterValue = transaction[2]
        
        ''' 
        NOTE:
        The following script will randomly select an integer value based on the size of the current database 
        to give a hypothetical employee ID from the current Database.
        '''
        ownerTransId = random.randint(1, len(data)-1)
            
        ''' 
        NOTE:
        Details of data_base = ['Unique_ID', 'First_name', 'Last_name', 'Salary', 'Department', 'Civil_status']
        "Updates database to new value, but the update is set to pending until it is finalized. This pending flag
        allows for eventual failure flag changes and rollbacks.
        '''
        data[empId][indexOfAttribute] = attributeAfterValue
        
        '''
        NOTE:
        Details of 'DB_Log' = [['transId', 'targetTable', 'empId', 'targetAttribute', 'valueBefore', 'valueAfter', 'success', 'ownerTransId']]
        set targetTable attribute as 'Employees' due to the nature of the assignment, and set success attribute as 'P' for Not-Executed (Pending).
        '''   
        DB_Log.append([transId, 'Employees', transaction[0], targetAttribute, attributeBeforeValue, attributeAfterValue, P, ownerTransId])

 
# =================================================================================================
# =================================================================================================


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


# =================================================================================================
# =================================================================================================


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


# =================================================================================================
# =================================================================================================


def main():
    number_of_transactions = len(transactions)
    must_recover = False
    
    '''
    NOTE:
    Added following script to grab the relatively located 'Employees_DV_ADV.csv' file.
    '''
    csv_file = os.path.dirname(os.path.realpath(__file__)) + '\Employees_DB_ADV.csv'
    
    '''
    NOTE:
    Changed the data_base variable to access the predeclared
    "global" data_base variable at the top of the file.
    This change allowed ua to access data_base in all 
    functions called in main without passing it as a parameter.
    '''
    global data_base
    data_base = read_file(csv_file)
    failing_transaction_index = None
    # Process transaction
    
    ''' 
    NOTE:
    Following writeOutput() call resets database output file to original database. 
    Useful to see changes only made on the most recent run.
    '''
    writeOutput(data_base, '\Employees_DB_Output.csv')
    
    '''
    NOTE:
    Removed exterior while loop and failure check to always 
    allow an attempt of a transaction. The original for loop will 
    run at max the total transactions being attempted in the 'transactions' 
    list variable.
    '''
    for index in range(number_of_transactions):
        ''' 
        NOTE:
        Randomly chooses a transaction from transactions and removes it to avoid duplicates.
        Transactions in random order help to mimic random transaction ordering.
        '''
        transaction = random.choice(transactions)
        
        print(f"\nProcessing transaction No. {index + 1}. Requested transaction: {transaction}")   #<--- Your CODE (Call function transaction_processing)
        transaction_processing(transaction, data_base) # ***Defined function placed here***
        print("UPDATES have not been committed yet...\n")
        failure = is_there_a_failure()
        if failure:
            must_recover = True
            failing_transaction_index = index + 1
            print(f'There was a failure whilst processing transaction No. {failing_transaction_index}.')
            updateDbLog(F) # <-- Custom Function Call
            break
        else:
            print(f'Transaction No. {index+1} has been commited! Changes are permanent.')
            updateDbLog(S) # <-- Custom Function Call
            
            ''' NOTE: Remove successful transaction from transactions list. '''
            transactions.remove(transaction)
                
    if must_recover:
        #Call your recovery script
        recovery_script(DB_Log) ### Call the recovery function to restore DB to sound state
        
        ''' NOTE: Printing just to see the failed trans details (Uncomment to see) '''
        # print(f"The Transaction That Failed Was: {transactions[failing_transaction_index-1]}\n")
    else:
        # All transactions ended up well
        print("All transaction ended up well.")
        print("Updates to the database were committed!\n")
    

    print('The data entries AFTER updates -and RECOVERY, if necessary- are presented below:')
    for item in data_base:
        print(item)
    
    writeOutput(data_base, '\Employees_DB_Output.csv') # Writes the final data_base details to a csv file.
    writeOutput(DB_Log, '\DB_Log_Output.csv') # Writes the final DB_Log details to a csv file.
    writeOutput(transactions, '\Remaining_Transactions.csv') # Writes remaining transactions to a csv file. (Empty if all successful).
     
    ''' NOTE: Printing just to see the final DB_Log details (Uncomment to see) '''
    # print("\nLogged Transactions are:\n", '\n'.join(map(str, DB_Log[1:])))


# =================================================================================================
# =================================================================================================


main()
