#	ORDER IS State Code, Distric Code, County Code, State or County Name, BS thing i don't care about
import os

def state_code(state):
	return {

		'Alabama':'01',
		'Alaska' : '02',
		'Arizona': '04',
		'Arkansas': '05',
		'California': '06',
		'Colorado' : '08',
		'Connecticut' : '09',
		'Delaware' : '10',
		'Florida' : '12',
		'Georgia' : '13',
		'Hawaii' : '15',
		'Idaho' : '16',
		'Illinois' : '17',
		'Indiana' : '18',
		'Iowa' : '19',
		'Kansas' : '20',
		'Kentucky' : '21',
		'Louisiana' : '22',
		'Maine' : '23',
		'Maryland' : '24',
		'Massachusetts' : '25',
		'Michigan' : '26',
		'Minnesota': '27',
		'Mississippi' : '28',
		'Missouri' : '29',
		'Montana' : '30',
		'Nebraska' :'31',
		'Nevada' : '32',
		'New Hampshire' : '33',
		'New Jersey' : '34',
		'New Mexico' : '35',
		'New York' :'36',
		'North Carolina': '37',
		'North Dakota' : '38',
		'Ohio' : '39',
		'Oklahoma' : '40',
		'Oregon' : '41',
		'Pennsylvania' : '42',
		'Rhode Island' : '44',
		'South Carolina' : '45',
		'South Dakota' : '46',
		'Tennessee' : '47',
		'Texas' : '48',
		'Utah' : '49',
		'Vermont' : '50',
		'Virginia'  : '51',
		'Washington' : '53',
		'West Virginia' : '54',
		'Wisconsin' : '55',
		'Wyoming' : '56',
		'Morris' : '34',
	}[state] 

def parse_file(state, county):
	if county=="Shongum":
		county="Morris"
	code = state_code(state)
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, 'codes.txt')
	text= open(file_path, 'r') 
	
	for row in text:
		row =row.strip('\n')
		values = row.strip(' ')
		if code == values[0]+values[1]:
			if county in values[7:len(values)-1] or values[7:len(values)-1] in county:
				return [code, values[10:13]]			