
# No other modules apart from 'socket', 'BeautifulSoup', 'requests' and 'datetime'
# need to be imported as they aren't required to solve the assignment

# Import required module/s
import socket
from bs4 import BeautifulSoup
import requests
import datetime


# Define constants for IP and Port address of Server
# NOTE: DO NOT modify the values of these two constants
HOST = '127.0.0.1'
PORT = 24680

# Define global variables
try_count = 0

def fetchWebsiteData(url_website):
	"""Fetches rows of tabular data from given URL of a website with data excluding table headers.

	Parameters
	----------
	url_website : str
		URL of a website

	Returns
	-------
	bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	"""
	
	web_page_data = ''

	##############	ADD YOUR CODE HERE	##############
	
	req = requests.get(url_website)
	soup = BeautifulSoup(req.text, "html.parser")
	
	web_page_data = soup.find("tbody").find_all("tr")
	
	##################################################

	return web_page_data


def fetchVaccineDoses(web_page_data):
	"""Fetch the Vaccine Doses available from the Web-page data and provide Options to select the respective Dose.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers

	Returns
	-------
	dict
		Dictionary with the Doses available and Options to select, with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchVaccineDoses(web_page_data))
	{'1': 'Dose 1', '2': 'Dose 2'}
	"""

	vaccine_doses_dict = {}

	##############	ADD YOUR CODE HERE	##############
	
	dose = list()
	for row in web_page_data:
		sub_row = row.find_all("td")
		for ele in sub_row:
			if("dose_num" in ele["class"]):
				if(ele.text not in dose):
					dose.append(ele.text)
	
	dose.sort()
	for n,i in enumerate(dose):
		vaccine_doses_dict[i] = "Dose {}".format(n+1)
	
	##################################################

	return vaccine_doses_dict


def fetchAgeGroup(web_page_data, dose):
	"""Fetch the Age Groups for whom Vaccination is available from the Web-page data for a given Dose
	and provide Options to select the respective Age Group.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Age Groups (for whom Vaccination is available for a given Dose) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchAgeGroup(web_page_data, '1'))
	{'1': '18+', '2': '45+'}
	>>> print(fetchAgeGroup(web_page_data, '2'))
	{'1': '18+', '2': '45+'}
	"""

	age_group_dict = {}

	##############	ADD YOUR CODE HERE	##############
	
	age = list()
	for row in web_page_data:
		sub_row = row.find_all("td")
		dose_flag = False
		
		for ele in sub_row:
			if("dose_num" in ele["class"]):
				if(ele.text == dose):
					dose_flag = True
			elif("age" in ele["class"]):
				if(dose_flag and ele.text not in age):
					age.append(ele.text)
	
	age.sort()
	for n,i in enumerate(age):
		age_group_dict[str(n+1)] = i
	
	##################################################

	return age_group_dict


def fetchStates(web_page_data, age_group, dose):
	"""Fetch the States where Vaccination is available from the Web-page data for a given Dose and Age Group
	and provide Options to select the respective State.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the States (where the Vaccination is available for a given Dose, Age Group) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchStates(web_page_data, '18+', '1'))
	{
		'1': 'Andhra Pradesh', '2': 'Arunachal Pradesh', '3': 'Bihar', '4': 'Chandigarh', '5': 'Delhi', '6': 'Goa',
		'7': 'Gujarat', '8': 'Harayana', '9': 'Himachal Pradesh', '10': 'Jammu and Kashmir', '11': 'Kerala', '12': 'Telangana'
	}
	"""

	states_dict = {}

	##############	ADD YOUR CODE HERE	##############
	
	states = list()
	for row in web_page_data:
		sub_row = row.find_all("td")
		age_flag = False
		dose_flag = False
		
		for ele in sub_row:
			if("age" in ele["class"]):
				if(ele.text == age_group):
					age_flag = True
			elif("dose_num" in ele["class"]):
				if(ele.text == dose):
					dose_flag = True
		for ele in sub_row:
			if("state_name" in ele["class"]):
				if(age_flag and dose_flag and ele.text not in states):
					states.append(ele.text)
	states.sort()
	for n,i in enumerate(states):
		states_dict[str(n+1)] = i
	
	##################################################

	return states_dict


def fetchDistricts(web_page_data, state, age_group, dose):
	"""Fetch the District where Vaccination is available from the Web-page data for a given State, Dose and Age Group
	and provide Options to select the respective District.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Districts (where the Vaccination is available for a given State, Dose, Age Group) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchDistricts(web_page_data, 'Ladakh', '18+', '2'))
	{
		'1': 'Kargil', '2': 'Leh'
	}
	"""

	districts_dict = {}

	##############	ADD YOUR CODE HERE	##############
	
	dist = list()
	for row in web_page_data:
		sub_row = row.find_all("td")
		state_flag = False
		age_flag = False
		dose_flag = False

		for ele in sub_row:
			if("state_name" in ele["class"]):
				if(ele.text == state):
					state_flag = True
			elif("age" in ele["class"]):
				if(ele.text == age_group):
					age_flag = True
			elif("dose_num" in ele["class"]):
				if(ele.text == dose):
					dose_flag = True
		for ele in sub_row:
			if("district_name" in ele["class"]):
				if(state_flag and age_flag and dose_flag and ele.text not in dist):
					dist.append(ele.text)
	dist.sort()
	for n,i in enumerate(dist):
		districts_dict[str(n+1)] = i
	
	##################################################

	return districts_dict


def fetchHospitalVaccineNames(web_page_data, district, state, age_group, dose):
	"""Fetch the Hospital and the Vaccine Names from the Web-page data available for a given District, State, Dose and Age Group
	and provide Options to select the respective Hospital and Vaccine Name.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	district : str
		District where Vaccination is available for a given State, Dose and Age Group
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Hosptial and Vaccine Names (where the Vaccination is available for a given District, State, Dose, Age Group)
		and Options to select, with Key as 'Option' and Value as another dictionary having Key as 'Hospital Name' and Value as 'Vaccine Name'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchHospitalVaccineNames(web_page_data, 'Kargil', 'Ladakh', '18+', '2'))
	{
		'1': {
				'MedStar Hospital Center': 'Covaxin'
			}
	}
	>>> print(fetchHospitalVaccineNames(web_page_data, 'South Goa', 'Goa', '45+', '2'))
	{
		'1': {
				'Eden Clinic': 'Covishield'
			}
	}
	"""
	
	hospital_vaccine_names_dict = {}

	##############	ADD YOUR CODE HERE	##############
	
	hosp = list()
	vacc = list()
	for row in web_page_data:
		sub_row = row.find_all("td")
		dist_flag = False
		state_flag = False
		age_flag = False
		dose_flag = False
		
		for ele in sub_row:
			if("district_name" in ele["class"]):
				if(ele.text == district):
					dist_flag = True
			elif("state_name" in ele["class"]):
				if(ele.text == state):
					state_flag = True
			elif("age" in ele["class"]):
				if(ele.text == age_group):
					age_flag = True
			elif("dose_num" in ele["class"]):
				if(ele.text == dose):
					dose_flag = True
		for ele in sub_row:
			if("hospital_name" in ele["class"]):
				if(dist_flag and state_flag and age_flag and dose_flag and ele.text not in hosp):
					hosp.append(ele.text)
			elif("vaccine_name" in ele["class"]):
				if(dist_flag and state_flag and age_flag and dose_flag and ele.text not in vacc):
					vacc.append(ele.text)
	for n in range(len(hosp)):
		hosp_vacc = dict()
		hosp_vacc[hosp[n]] = vacc[n]
		hospital_vaccine_names_dict[str(n+1)] = hosp_vacc
	
	##################################################

	return hospital_vaccine_names_dict


def fetchVaccineSlots(web_page_data, hospital_name, district, state, age_group, dose):
	"""Fetch the Dates and Slots available on those dates from the Web-page data available for a given Hospital Name, District, State, Dose and Age Group
	and provide Options to select the respective Date and available Slots.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	hospital_name : str
		Name of Hospital where Vaccination is available for given District, State, Dose and Age Group
	district : str
		District where Vaccination is available for a given State, Dose and Age Group
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Dates and Slots available on those dates (where the Vaccination is available for a given Hospital Name,
		District, State, Dose, Age Group) and Options to select, with Key as 'Option' and Value as another dictionary having
		Key as 'Date' and Value as 'Available Slots'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchVaccineSlots(web_page_data, 'MedStar Hospital Center', 'Kargil', 'Ladakh', '18+', '2'))
	{
		'1': {'May 15': '0'}, '2': {'May 16': '81'}, '3': {'May 17': '109'}, '4': {'May 18': '78'},
		'5': {'May 19': '89'}, '6': {'May 20': '57'}, '7': {'May 21': '77'}
	}
	>>> print(fetchVaccineSlots(web_page_data, 'Eden Clinic', 'South Goa', 'Goa', '45+', '2'))
	{
		'1': {'May 15': '0'}, '2': {'May 16': '137'}, '3': {'May 17': '50'}, '4': {'May 18': '78'},
		'5': {'May 19': '145'}, '6': {'May 20': '64'}, '7': {'May 21': '57'}
	}
	"""

	vaccine_slots = {}

	##############	ADD YOUR CODE HERE	##############
	
	slots = list()
	for row in web_page_data:
		sub_row = row.find_all("td")
		hosp_flag = False
		dist_flag = False
		state_flag = False
		age_flag = False
		dose_flag = False
		
		for ele in sub_row:
			if("hospital_name" in ele["class"]):
				if(ele.text == hospital_name):
					hosp_flag = True
			elif("state_name" in ele["class"]):
				if(ele.text == state):
					state_flag = True
			elif("district_name" in ele["class"]):
				if(ele.text == district):
					dist_flag = True
			elif("dose_num" in ele["class"]):
				if(ele.text == dose):
					dose_flag = True
			elif("age" in ele["class"]):
				if(ele.text == age_group):
					age_flag = True
		for ele in sub_row:
			slot = dict()
			if(ele["class"][0].startswith("may_")):
				if(hosp_flag and state_flag and dist_flag and dose_flag and age_flag):
					slot["May "+ele["class"][0].split("_")[1]] = ele.text
					slots.append(slot)
	for n,i in enumerate(slots):
		vaccine_slots[str(n+1)] = i
	
	##################################################

	return vaccine_slots


def openConnection():
	"""Opens a socket connection on the HOST with the PORT address.

	Returns
	-------
	socket
		Object of socket class for the Client connected to Server and communicate further with it
	tuple
		IP and Port address of the Client connected to Server
	"""

	client_socket = None
	client_addr = None

	##############	ADD YOUR CODE HERE	##############
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(1)
	client_socket, client_addr = s.accept()
	print("Client is connected at: ('{}', {})".format(client_addr[0], client_addr[1]))
	
	##################################################
	
	return client_socket, client_addr


def startCommunication(client_conn, client_addr, web_page_data):
	"""Starts the communication channel with the connected Client for scheduling an Appointment for Vaccination.

	Parameters
	----------
	client_conn : socket
		Object of socket class for the Client connected to Server and communicate further with it
	client_addr : tuple
		IP and Port address of the Client connected to Server
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	"""

	##############	ADD YOUR CODE HERE	##############
	
	data = "Welcome to CoWIN ChatBot-Schedule an Appointment for Vaccination:-"
	client_conn.send(data.encode("utf-8"))
	
	global try_count
	try_count = 0
	vaccineDoses(client_conn, client_addr, web_page_data)
	
	##################################################


def stopCommunication(client_conn):
	"""Stops or Closes the communication channel of the Client with a message.

	Parameters
	----------
	client_conn : socket
		Object of socket class for the Client connected to Server and communicate further with it
	"""

	##############	ADD YOUR CODE HERE	##############
	
	data = "\n<<< See ya! Visit again :)"
	client_conn.send(data.encode("utf-8"))
	client_conn.close()
	
	##################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

def vaccineDoses(c_c, c_a, w_d):
	global try_count
	if(try_count < 3):
		vaccine_doses = fetchVaccineDoses(w_d)
		data = "\n>>> Select the Dose of Vaccination:\n{}\n".format(vaccine_doses)
		c_c.send(data.encode("utf-8"))
		dose_sel = c_c.recv(1024).decode("utf-8")
		
		if(dose_sel in ["b", "B"]):
			vaccineDoses(c_c, c_a, w_d)
		elif(dose_sel in ["q", "Q"]):
			print("Client wants to quit!\nSaying Bye to client and closing the connection!")
			stopCommunication(c_c)
		elif(dose_sel not in list(vaccine_doses.keys())):
			try_count += 1
			data = "\n<<< Invalid input provided {} times(s)! Try again.".format(try_count)
			c_c.send(data.encode("utf-8"))
			print("Invalid input detected {} time(s)!".format(try_count))
			vaccineDoses(c_c, c_a, w_d)
		else:
			print("Dose selected:  {}".format(dose_sel))
			if(dose_sel == "1"):
				dose_one(c_c, c_a, w_d, dose_sel)
			elif(dose_sel == "2"):
				dose_two(c_c, c_a, w_d, dose_sel)
	else:
		print("Notifying the client and closing the connection!")
		stopCommunication(c_c)

def dose_one(c_c, c_a, w_d, dose_sel):
	data = "\n<<< Dose selected: {}".format(dose_sel)
	c_c.send(data.encode("utf-8"))
	ageGroup(c_c, c_a, w_d, dose_sel)

def dose_two(c_c, c_a, w_d, dose_sel):
	data = "\n<<< Dose selected: {}\n".format(dose_sel)
	c_c.send(data.encode("utf-8"))
	dose_two_eligibility(c_c, c_a, w_d, dose_sel)

def dose_two_eligibility(c_c, c_a, w_d, dose_sel):
	data = "\n>>> Provide the date of First Vaccination Dose (DD/MM/YYYY), for e.g. 12/5/2021\n"
	c_c.send(data.encode("utf-8"))
	dose_one_date = c_c.recv(1024).decode("utf-8")
	
	if(dose_one_date in ["b", "B"]):
		vaccineDoses(c_c, c_a, w_d)
	elif(dose_one_date in ["q", "Q"]):
		print("Client wants to quit!\nSaying Bye to client and closing the connection!")
		stopCommunication(c_c)
	else:
		try:
			dd, mm, yyyy = dose_one_date.split("/")
			flag_split_date = True
		except:
			data = "\n<<< Invalid Date provided of First Vaccination Dose: {}".format(dose_one_date)
			c_c.send(data.encode("utf-8"))
			print("Invalid date provided!")
			dose_two_eligibility(c_c, c_a, w_d, dose_sel)
			flag_split_date = False
		
		if(flag_split_date):
			isValidDate = True
			try:
				dose_date = datetime.datetime(int(yyyy), int(mm), int(dd))
			except ValueError:
				isValidDate = False
			
			today = datetime.datetime.now()
			if(dose_date>today):
				isValidDate = False
			
			if(isValidDate):
				print("First dose date:  {}".format(dose_one_date))
				weeks_up_from_dose_one = (today-dose_date).days//7
				data = "\n<<< Date of First Vaccination Dose provided: {}\n<<< Number of weeks from today: {}".format(dose_one_date, weeks_up_from_dose_one)
				c_c.send(data.encode("utf-8"))
				
				if(weeks_up_from_dose_one<4):
					data = "\n<<< You are not eligible right now for 2nd Vaccination Dose! Try after {} weeks.".format(4-weeks_up_from_dose_one)
					c_c.send(data.encode("utf-8"))
					stopCommunication(c_c)
				elif(weeks_up_from_dose_one>8):
					data = "\n<<< You have been late in scheduling your 2nd Vaccination Dose by {} weeks.".format(weeks_up_from_dose_one-8)
					c_c.send(data.encode("utf-8"))
					ageGroup(c_c, c_a, w_d, dose_sel)
				else:
					data = "\n<<< You are eligible for 2nd Vaccination Dose and are in the right time-frame to take it."
					c_c.send(data.encode("utf-8"))
					ageGroup(c_c, c_a, w_d, dose_sel)
			else:
				data = "\n<<< Invalid Date provided of First Vaccination Dose: {}".format(dose_one_date)
				c_c.send(data.encode("utf-8"))
				print("Invalid date provided!")
				dose_two_eligibility(c_c, c_a, w_d, dose_sel)

def ageGroup(c_c, c_a, w_d, dose_sel):
	global try_count
	if(try_count < 3):
		age_group = fetchAgeGroup(w_d, dose_sel)
		data = "\n>>> Select the Age Group:\n{}\n".format(age_group)
		c_c.send(data.encode("utf-8"))
		age_sel = c_c.recv(1024).decode("utf-8")
		
		if(age_sel in ["b", "B"]):
			vaccineDoses(c_c, c_a, w_d)
		elif(age_sel in ["q", "Q"]):
			print("Client wants to quit!\nSaying Bye to client and closing the connection!")
			stopCommunication(c_c)
		elif(age_sel not in list(age_group.keys())):
			try_count += 1
			data = "\n<<< Invalid input provided {} time(s)! Try again.".format(try_count)
			c_c.send(data.encode("utf-8"))
			print("Invalid input detected {} time(s)!".format(try_count))
			ageGroup(c_c, c_a, w_d, dose_sel)
		else:
			data = "\n<<< Selected Age Group: {}".format(age_group[age_sel])
			c_c.send(data.encode("utf-8"))
			print("Age Group selected:  {}".format(age_group[age_sel]))
			states(c_c, c_a, w_d, age_group[age_sel], dose_sel)
	else:
		print("Notifying the client and closing the connection!")
		stopCommunication(c_c)

def states(c_c, c_a, w_d, age_sel, dose_sel):
	global try_count
	if(try_count < 3):
		state = fetchStates(w_d, age_sel, dose_sel)
		data = "\n>>> Select the State:\n{}\n".format(state)
		c_c.send(data.encode("utf-8"))
		state_sel = c_c.recv(1024).decode("utf-8")
		
		if(state_sel in ["b", "B"]):
			ageGroup(c_c, c_a, w_d, dose_sel)
		elif(state_sel in ["q", "Q"]):
			print("Client wants to quit!\nSaying Bye to client and closing the connection!")
			stopCommunication(c_c)
		elif(state_sel not in list(state.keys())):
			try_count += 1
			data = "\n<<< Invalid input provided {} time(s)! Try again.".format(try_count)
			c_c.send(data.encode("utf-8"))
			print("Invalid input detected {} time(s)!".format(try_count))
			states(c_c, c_a, w_d, age_sel, dose_sel)
		else:
			data = "\n<<< Selected State: {}".format(state[state_sel])
			c_c.send(data.encode("utf-8"))
			print("State selected:  {}".format(state[state_sel]))
			districts(c_c, c_a, w_d, state[state_sel], age_sel, dose_sel)
	else:
		print("Notifying the client and closing the connection!")
		stopCommunication(c_c)

def districts(c_c, c_a, w_d, state_sel, age_sel, dose_sel):
	global try_count
	if(try_count < 3):
		district = fetchDistricts(w_d, state_sel, age_sel, dose_sel)
		data = "\n>>> Select the District:\n{}\n".format(district)
		c_c.send(data.encode("utf-8"))
		dist_sel = c_c.recv(1024).decode("utf-8")
		
		if(dist_sel in ["b", "B"]):
			states(c_c, c_a, w_d, age_sel, dose_sel)
		elif(dist_sel in ["q", "Q"]):
			print("Client wants to quit!\nSaying Bye to client and closing the connection!")
			stopCommunication(c_c)
		elif(dist_sel not in list(district.keys())):
			try_count += 1
			data = "\n<<< Invalid input provided {} time(s)! Try again.".format(try_count)
			c_c.send(data.encode("utf-8"))
			print("Invalid input detected {} time(s)!".format(try_count))
			districts(c_c, c_a, w_d, state_sel, age_sel, dose_sel)
		else:
			data = "\n<<< Selected District: {}".format(district[dist_sel])
			c_c.send(data.encode("utf-8"))
			print("District selected:  {}".format(district[dist_sel]))
			hospitalVaccineNames(c_c, c_a, w_d, district[dist_sel], state_sel, age_sel, dose_sel)
	else:
		print("Notifying the client and closing the connection!")
		stopCommunication(c_c)

def hospitalVaccineNames(c_c, c_a, w_d, dist_sel, state_sel, age_sel, dose_sel):
	global try_count
	if(try_count < 3):
		hosp_vacc_names = fetchHospitalVaccineNames(w_d, dist_sel, state_sel, age_sel, dose_sel)
		data = ">>> Select the Vaccination Center Name:\n{}\n".format(hosp_vacc_names)
		c_c.send(data.encode("utf-8"))
		cen_sel = c_c.recv(1024).decode("utf-8")
		
		if(cen_sel in ["b", "B"]):
			districts(c_c, c_a, w_d, state_sel, age_sel, dose_sel)
		elif(cen_sel in ["q", "Q"]):
			print("Client wants to quit!\nSaying Bye to client and closing the connection!")
			stopCommunication(c_c)
		elif(cen_sel not in list(hosp_vacc_names.keys())):
			try_count += 1
			data = "\n<<< Invalid input provided {} time(s)! Try again.".format(try_count)
			c_c.send(data.encode("utf-8"))
			print("Invalid input detected {} time(s)!".format(try_count))
			hospitalVaccineNames(c_c, c_a, w_d, dist_sel, state_sel, age_sel, dose_sel)
		else:
			data = "\n<<< Selected Vaccination Center: {}".format(list(hosp_vacc_names[cen_sel].keys())[0])
			c_c.send(data.encode("utf-8"))
			print("Hospital selected:  {}".format(list(hosp_vacc_names[cen_sel].keys())[0]))
			vaccineSlots(c_c, c_a, w_d, hosp_vacc_names[cen_sel], dist_sel, state_sel, age_sel, dose_sel)
	else:
		print("Notifying the client and closing the connection!")
		stopCommunication(c_c)

def vaccineSlots(c_c, c_a, w_d, cen_sel, dist_sel, state_sel, age_sel, dose_sel):
	global try_count
	if(try_count < 3):
		vacc_slots = fetchVaccineSlots(w_d, list(cen_sel.keys())[0], dist_sel, state_sel, age_sel, dose_sel)
		data = ">>> Select one of the available slots to schedule the Appointment:\n{}\n".format(vacc_slots)
		c_c.send(data.encode("utf-8"))
		slot_sel = c_c.recv(1024).decode("utf-8")
		
		if(slot_sel in ["b", "B"]):
			hospitalVaccineNames(c_c, c_a, w_d, dist_sel, state_sel, age_sel, dose_sel)
		elif(slot_sel in ["q", "Q"]):
			print("Client wants to quit!\nSaying Bye to client and closing the connection!")
			stopCommunication(c_c)
		elif(slot_sel not in list(vacc_slots.keys())):
			try_count += 1
			data = "\n<<< Invalid input provided {} time(s)! Try again.".format(try_count)
			c_c.send(data.encode("utf-8"))
			print("Invalid input detected {} time(s)!".format(try_count))
			vaccineSlots(c_c, c_a, w_d, cen_sel, dist_sel, state_sel, age_sel, dose_sel)
		else:
			data = "\n<<< Selected Vaccination Appointment Date: {}\n<<< Available Slots on the selected Date: {}".format(list(vacc_slots[slot_sel].keys())[0], list(vacc_slots[slot_sel].values())[0])
			c_c.send(data.encode("utf-8"))
			print("Vaccination Date selected:  {}".format(list(vacc_slots[slot_sel].keys())[0]))
			print("Available Slots on that date:  {}".format(list(vacc_slots[slot_sel].values())[0]))
			slotConfirmation(c_c, c_a, w_d, vacc_slots[slot_sel], cen_sel, dist_sel, state_sel, age_sel, dose_sel)
	else:
		print("Notifying the client and closing the connection!")
		stopCommunication(c_c)

def slotConfirmation(c_c, c_a, w_d, slot_sel, cen_sel, dist_sel, state_sel, age_sel, dose_sel):
	if(int(list(slot_sel.values())[0]) > 0):
		data = "\n<<< Your appointment is scheduled. Make sure to carry ID Proof while you visit Vaccination Center!"
		c_c.send(data.encode("utf-8"))
		stopCommunication(c_c)
	else:
		data = "\n<<< Selected Appointment Date has no available slots, select another date!"
		c_c.send(data.encode("utf-8"))
		vaccineSlots(c_c, c_a, w_d, cen_sel, dist_sel, state_sel, age_sel, dose_sel)

##############################################################


if __name__ == '__main__':
	"""Main function, code begins here
	"""
	url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	web_page_data = fetchWebsiteData(url_website)
	client_conn, client_addr = openConnection()
	startCommunication(client_conn, client_addr, web_page_data)
