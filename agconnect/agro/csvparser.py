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
		myfile='dubuque.csv'
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
		perp_tally=0.0
		perp_count=0
		temp_tally=0.0
		temp_count=0
		myJSON={}
		for row in weatherreader:
			if count==1:
				myJSON={"month":[]}
			total_percipitation= "%.2f" % (float(row[3]) / 254.0)
			celsius=row[4][:len(row[4])-1:]+"."+row[4][len(row[4])-1]
			#ftemp stands for farenehieht temperature
			ftemp= (float(celsius)*9.0)/5.0 -32
			perp_count+=1
			perp_tally+=float(total_percipitation)
			if row[4]!="-9999":
				temp_tally+=ftemp
				temp_count+=1
			month ="month" 
			try:
				myJSON[month][0]=perp_tally/perp_count
				myJSON[month][1]=temp_tally/temp_count
			except:
				myJSON[month].append(perp_tally)
				myJSON[month].append(temp_tally)
			if count==12:
				myJSONLIST.append(myJSON)
				count=0
			count+=1
		
	return myJSONLIST
