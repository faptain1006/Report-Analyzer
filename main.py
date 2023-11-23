import csv
import pathlib 
import os
from datetime import datetime

# this will process the CSV files
def processCSV(run):
    
    # get the list of files
    os.chdir(".")
    cwd = os.getcwd()
    files = os.listdir(cwd)

    # initiate the variables
    numFiles = 0
    dataSets = []
    fileNames = []

    # check for csv files
    for file in files:
        if pathlib.Path(file).suffix == ".csv":
            numFiles = numFiles + 1

    # check number of files and create the dataset        
    if (numFiles < 3):
        print("***ERROR - Incomplete datasets")
        run = False
    else:
        for file in files:
            if pathlib.Path(file).suffix == ".csv":

                recordNum = 0 # initiate the record number var

                # create a fileNames list
                fileName = pathlib.Path(file).stem 
                fileNames.append(fileName)

                # open and read the files
                dataFile = open(f"{file}","r")
                dataReader = csv.reader(dataFile)
                print(f">>>Loading Dataset {file}")

                # generate the dataset
                for row in dataReader:
                    recordNum = recordNum + 1
                    dataSets.append([fileName] + [recordNum] + row) # add filename and record number for each rows of each datasets
                dataFile.close()
        

    return dataSets, run, fileNames


# this will analyze the dataSet
def analyzeData(dataSets):

    print(">>>Searching Datasets for hacker User ID")

    # initiate list
    hackerTransactions = []
    hackerID = []

    # get the hacker ID/s from the dataSet
    for row in range(0, len(dataSets)):
        if (float(dataSets[row][4]) > 5):
            hackerID.append(dataSets[row][2])    
    
    # get all the hackers' transactions
    for row in range(0, len(dataSets)):
        if (dataSets[row][2] in hackerID):
            hackerTransactions.append(dataSets[row])
        

    return hackerTransactions


# genearate the report.txt
def generateReport(hackerTransactions, fileNames): 
    
    # initiate list
    columnSpaces = [0,12,20,20,20,0]
    totalStolen = []
    header = ["Filename","Record #","User ID","Transaction ID","Amount (K)","Timestamp"]

    # get the stolen amounts and format certain columns
    for row in range(0,len(hackerTransactions)):  
        totalStolen.append(float(hackerTransactions[row][4]))
        hackerTransactions[row][4] = f"${hackerTransactions[row][4]}"
        hackerTransactions[row][5] = str(datetime.fromtimestamp(int(hackerTransactions[row][5])))

    # create the report file
    report = open("report.txt","w")
    
    report.write("HACKER ACTIVITY REPORT:\n\n")

    # create a report for each fileNames
    for fileName in fileNames:
        report.write(f"> Reporting on {fileName}.csv:\n")
        
        # write the required headers
        for col in range(1,len(hackerTransactions[0])):
            report.write(f"{header[col]:<{columnSpaces[col]}}")

        report.write("\n")

        # write the data and group them according to fileName
        for row in range(0,len(hackerTransactions)):  
            if hackerTransactions[row][0] == fileName:
                for col in range(1,len(hackerTransactions[0])):
                    report.write(f"{hackerTransactions[row][col]:<{columnSpaces[col]}}")
                report.write("\n")
                  
        report.write("\n")

    # write the total stolen amount
    report.write(f"> total amount stolen: ${sum(totalStolen):.2f}K")  

    report.close()

    print(">>>Report generated and stored in report.txt")
    

def main():

    run = True

    dataSets, run, fileNames = processCSV(run) # process the CSV

    if (run == True):
        hackerTransactions = analyzeData(dataSets)  # analyze the dataset
        generateReport(hackerTransactions, fileNames)  # generate the final report
        

main()
