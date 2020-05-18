from locust import HttpLocust, TaskSet, between

auth = open("auth.txt", "r").read().split("\n")[0]
print("Using Auth Token: %s" % (auth,))

def register(l):
	with l.client.post("/rw/save/user",
		data={"fullName": "Tester, Locust",
			  "dept": "1203000",
			  "subDept": "1300101",
			  "phone": "301-314-2806",
			  "supervisor": "Vladmir Labar",
			  "email": "ssaxena1@terpmail.umd.edu",
			  "buildingId": "115",
			  "wasteRoom": "500",
			  "wasteLocation": "n/a"},
		name = "Register User",
		catch_response=True) as res:
		
		if "/rw/public" not in res.url: 
			res.failure("Registration Was Not Successful")
	
def login(l):
	with l.client.post("https://login.qa.umd.edu/cas/login", 
		params={"service":"https://app.essr.dev.umd.edu/rw/register"}, 
		headers={"Authorization": auth}, 
		name= "Login",#"https://login.qa.umd.edu/cas/login",
		catch_response = True) as res:
		
		if "/rw/register" not in res.url: 
			res.failure("Login Did not Go to Registration Page")
		
def logout(l):
	with l.client.post("https://login.qa.umd.edu/cas/logout", 
		name= "Logout",#"https://login.umd.edu/cas/logout",
		catch_response = True) as res:
		
		if "/logout" not in res.url:
			res.failure("Logout Failed to Jump to Correct Page")

def index(l):
    l.client.get("/rw", name="Go To Homepage")

def goToForm(l):
	with l.client.get("/rw/chemForm", catch_response=True, name = "Go To ChemForm") as res:
		if "/rw/chemForm" not in res.url: 
			res.failure("Chem Form Page Was Redirected Elsewhere")

def goToChem(l, chemid = 159644):
	with l.client.get("/rw/chemForm/%d" % chemid, catch_response=True, name = "See Specific ChemForm") as res:
		if str(chemid) not in res.url: 
			res.failure("ChemForm %d Not Found" % chemid)

def goToDrum(l, drumid = 11800):
	with l.client.get("/rw/drum/info", params={"drumId": drumid}, catch_response=True, name= "Go To Drum") as res:
		if "/drum/info" not in res.url:
			res.failure("Drum %d Not Found In" % drumid)

def goToDrumList(l):
	with l.client.get("/rw/listdrum", catch_response=True, name= "Go To Drum List") as res:
		if "/rw/listdrum" not in res.url: 
			res.failure("Drum List Not Found")

def search(l, chemical="acetone"):
	with l.client.post("/rw/search/chemicalByName", data={"name": chemical}, catch_response=True, name="Search For A Chemical") as res:
		if "/rw/search/chemicalByName" not in res.url:
			res.failure("Search Redirected Elsewhere")
	
def goToSearch(l):
	with l.client.get("/rw/search/chemicalByName", catch_response=True, name="Go To Chemical Search") as res:
		if "/rw/search/chemicalByName" not in res.url:
			res.failure("Search Page Not Found")

def goToStatus(l):
	with l.client.get("/rw/chemStatus", catch_response=True, name="Go To Chem Status") as res:
		if "/chemStatus" not in res.url:
			res.failure("Status Page Not Found")

def runSearch(l):
	goToSearch(l)
	search(l)

def runDrum(l):
	goToDrumList(l)
	goToDrum(l)
	goToChem(l)

class UserBehavior(TaskSet):
	tasks = {index: 1, goToForm: 1, runDrum: 1, runSearch: 1, goToStatus: 1}

	def on_start(self):
		login(self)
		register(self)
	
	def on_stop(self):
	    logout(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
