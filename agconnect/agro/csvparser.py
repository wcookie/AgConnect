import csv
import os
#STATION,STATION_NAME,DATE,TPCP,MNTM
#divide every TPCP value by 254 in order to get inches
#last digit of every MNTM is decimal point
#MNTM is in celsius
#might need to readd the dash as last line???
def weather_stuff(city):
	myfile=""
	if city=="Dubuque":
		myfile='691186.csv'
	elif city=="Stamford":
		myfile='stamford.csv'
	elif city=="Morris":
		myfile='morris.csv'
	elif city=="Colombus":
		myfile='colombus.csv'
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, myfile)

	with open(file_path, 'rb') as csvfile:
		weatherreader= csv.reader(csvfile)
		count=1

		myJSONLIST=[]
		for row in weatherreader:
			myJSON={}
			total_percipitation= "%.2f" % (float(row[3]) / 254.0)
			celsius=row[4][:len(row[4])-1:]+"."+row[4][len(row[4])-1]
			#ftemp stands for farenehieht temperature
			ftemp= (float(celsius)*9.0)/5.0 +32.0
			month ="month" 
			myJSON[month] =[]
			myJSON[month].append(float(total_percipitation))
			myJSON[month].append(ftemp)
			myJSONLIST.append(myJSON)
			count+=1
		
	return myJSONLIST
