import csv
import random as rd
import numpy as np

# run command: python3 randData.py

def main():
	minNumFileGen = 4
	maxNumFileGen = 10
	numFiles = rd.randint(minNumFileGen,maxNumFileGen)

	minRows = 3
	maxRows = 20

	maxTime = 120	#in second
	maxSpeed = 20	#metre per sec

	errorCap = 30	#percent
	minErr, maxErr = 1-(errorCap/100), 1+(errorCap/100) #can go under or over to these bounds

	arg1 = []	#name of expected files
	arg2 = []	#name of actual files

	for i in range(0,numFiles): #generate a exp and act set with random row
		numRows = rd.randint(minRows,maxRows)
		expFileName = 'exp' + str(i+1) + '.csv'
		actFileName = 'act' + str(i+1) + '.csv'

		arg1.append(expFileName)
		arg2.append(actFileName)

		with open(expFileName, mode='w+') as out_orig_file, open(actFileName, mode='w+') as out_error_file:
			for j in range(0,numRows):
				currRow = np.array([rd.uniform(-360,360),rd.uniform(0,maxTime),rd.uniform(0,maxSpeed)])
			    
				wrt1 = csv.writer(out_orig_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				wrt1.writerow(currRow)

				errorRow = np.array([rd.uniform(minErr,maxErr),rd.uniform(minErr,maxErr),rd.uniform(minErr,maxErr)])*currRow

				wrt2 = csv.writer(out_error_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				wrt2.writerow(errorRow)

	print('Function call:')
	print("plotmicrocar(['{0:s}'],['{1:s}'])".format("','".join(arg1),"','".join(arg2)))

if __name__ == "__main__":
    main()
