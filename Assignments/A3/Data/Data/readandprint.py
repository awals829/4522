'''
===================================================================================================
=======================          ASSIGNMENT #3 WINTER 2024                  =======================
=======================          COMP 4522 ADVANCED DATABASES               =======================
=======================          GROUP: ANDREW W., RUTU K., BRANDON K.      =======================
=======================          DUE: April 5                               =======================
===================================================================================================
'''

import csv
import os

# =============================================================================================
# =============================================================================================

'''
CSV FILES
'''
DEP_DATA = 'Department_Information.csv'
EMP_DATA = 'Employee_Information.csv'
STUD_COUNS_DATA = 'Student_Counceling_Information.csv'
STUD_PERF_DATA = 'Student_Performance_Data.csv'

def getCWD() -> str:
    """_summary_ : Gets the current file current working directory. Requires 'import os'.

    Returns:
        str: String literal of the current working directory appended with a final backslash.
    """
    return os.path.dirname(os.path.realpath(__file__)) + '\\'

# =============================================================================================
# =============================================================================================

def myreader(filename:str)->list:
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        return your_list

def mywriter(filename:str, mylist:list):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write multiple rows
        writer.writerows(mylist)

# =============================================================================================
# =============================================================================================

def main():
    cwd = getCWD()
    # read PERFORMANCE data
    mydata = myreader(cwd + STUD_PERF_DATA)
    print("STUDENT_PERFORMANCE_DATA")
    for i in range(0,29):
        print(mydata[i])
    print("=============================================================================================")
    # read DEPT data
    mydata = myreader(cwd + DEP_DATA)
    print("DEPARTMENT_DATA")
    for i in range(0,29):
        print(mydata[i])
    print("=============================================================================================")
    # read COUNCIL data
    mydata = myreader(cwd + STUD_COUNS_DATA)
    print("STUDENT_COUNCELING_DATA")
    for i in range(0,29):
        print(mydata[i])
    print("=============================================================================================")
    # read EMPLOYEE data
    mydata = myreader(cwd + EMP_DATA)
    print("EMPLOYEE_INFORMATION")
    for i in range(0,29):
        print(mydata[i])


# =============================================================================================
# =============================================================================================
        
main()
