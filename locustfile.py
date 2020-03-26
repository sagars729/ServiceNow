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
		catch_response=True) as res:
		
		if "/rw/public" not in res.url: 
			res.failure("Registration Was Not Successful")
	
def login(l):
	with l.client.post("https://login.qa.umd.edu/cas/login", 
		params={"service":"https://app.essr.qa.umd.edu/rw/register"}, 
		headers={"Authorization": auth}, 
		name="https://login.qa.umd.edu/cas/login",
		catch_response = True) as res:
		
		if "/rw/register" not in res.url: 
			res.failure("Login Did not Go to Registration Page")

def logout(l):
	with l.client.post("https://login.qa.umd.edu/cas/logout", 
		name="https://login.umd.edu/cas/logout",
		catch_response = True) as res:
		
		if "/logout" not in res.url:
			res.failure("Logout Failed to Jump to Correct Page")

def index(l):
    l.client.get("/rw")

def goToForm(l):
	with l.client.get("/rw/chemForm", catch_response=True) as res:
		if "/rw/chemForm" not in res.url: 
			res.failure("Chem Form Page Was Redirected Elsewhere")
 
def goToDrumList(l):
	with l.client.get("/rw/listdrum", catch_response=True) as res:
		if "/rw/listdrum" not in res.url: 
			res.failure("Drum List Not Found")

def search(l, checmical="acetone"):
	with l.client.post("/rw/search/chemicalByName", data={"name": chemical}, catch_response=True) as res:
		if "/rw/search/chemicalByName" not in res.url:
			res.failure("Search Redirected Elsewhere")
	
def goToSearch(l):
    with l.client.get("/rw/search/chemicalByName", catch_response=True) as res:
		if "/rw/search/chemicalByName" not in res.url:
			res.failure("Search Page Not Found")

def runSearch(l)
	goToSearch(l)
	search(l)

class UserBehavior(TaskSet):
	tasks = {index: 2, goToForm: 5, goToDrumList: 10, goToSearch: 10, runSearch: 5}
	def on_start(self):
		login(self)
		register(self)
	
	def on_stop(self):
	    logout(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
