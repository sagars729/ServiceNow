from locust import HttpLocust, TaskSet, between
import threading
from random import random

my_mutex = threading.Lock() 
body = {
    "employee.uId":"",
    "employee.dirId":"",
    "employee.employeeName":"Saxena, Sagar",
    "employee.title":"Engineer",
    "employee.dept":"DIT-EE-Enterprise Engineering & Operations",
    "employee.sectionUnit":"DIT-Software Engineering",
    "employee.supervisorUId":"",
    "employee.supervisorName":"Labar, Vladimir",
    "activeQuarterTypeCode":"0",
    "prd.prdId":"76c93dfd-4803-47af-810a-c34de3cb9eac",
    "prd.docId":"8171729",
    "quarterDetails[1].quarter.prdId":"76c93dfd-4803-47af-810a-c34de3cb9eac",
    "quarterDetails[0].quarter.qId":"b5e448c3-2a96-42e8-be0b-a84084c61613",
    "quarterDetails[1].quarter.qId":"c7914d2f-4cf1-4c73-abb0-7ddc72815853",
    "quarterDetails[2].quarter.qId":"b92d4dc7-cb3d-4424-afb3-5a2341a54aea",
    "quarterDetails[3].quarter.qId":"",
    "quarterDetails[1].quarter.quarterTypeCode":"1",
    "actionQuarter":"1",
    "prd.workflowState":"P2 Expectation Setting",
    "prd.cycleYear":"2020",
    "prd.supervisorUid":"",
    "copyExpTypeCode":"0",
    "quarterDetails[1].quarter.updatedDate":"2020-05-11 15:00:49.0",
    "quarterDetails[1].quarter.quarterRating":"0",
    "quarterDetails[1].quarter.quarterCulturalRating":"0",
    "quarterDetails[1].quarter.quarterWorkflowState":"0",
    "quarterDetails[1].expectationRating[0].ratingTypeCode":"0",
    "quarterDetails[1].expectationRating[0].qId":"c7914d2f-4cf1-4c73-abb0-7ddc72815853",
    "quarterDetails[1].expectationRating[0].expTypeCode":"0",
    "_quarterDetails[1].operationList[0].expSelect":"on",
    "quarterDetails[1].operationList[0].expDesc":"HelloWorldWork",
    "quarterDetails[1].operationList[0].expActionOutcome":"",
    "quarterDetails[1].operationList[0].expAccomplishments":"",
    "quarterDetails[1].operationList[0].qId":"c7914d2f-4cf1-4c73-abb0-7ddc72815853",
    "quarterDetails[1].operationList[0].expTypeCode":"0",
    "quarterDetails[1].operationList[0].expectationOperation":"UPDATE",
    "quarterDetails[1].expectationRating[0].notes":"",
    "quarterDetails[1].expectationRating[2].ratingTypeCode":"0",
    "quarterDetails[1].expectationRating[2].qId":"c7914d2f-4cf1-4c73-abb0-7ddc72815853",
    "quarterDetails[1].expectationRating[2].expTypeCode":"2",
    "_quarterDetails[1].developmentList[0].expSelect":"on",
    "quarterDetails[1].developmentList[0].expDesc":"HelloWorld",
    "quarterDetails[1].developmentList[0].expActionOutcome":"",
    "quarterDetails[1].developmentList[0].expAccomplishments":"",
    "quarterDetails[1].developmentList[0].qId":"7914d2f-4cf1-4c73-abb0-7ddc72815853",
    "quarterDetails[1].developmentList[0].expTypeCode":"2",
    "quarterDetails[1].developmentList[0].expectationOperation":"UPDATE",
    "quarterDetails[1].expectationRating[2].notes":"",
    "quarterDetails[1].operationList[0].expId":"7e2a352c-fc90-4b87-b90f-9dce9c99fa1e",
    "quarterDetails[1].developmentList[0].expId":"59407509-211c-4365-9a20-b253abee58d7",
}
headers = {
	"Host": "itprd.dev.umd.edu",
	"Origin": "https://itprd.dev.umd.edu",
	"Connection": "keep-alive",
	"Referer": "https://itprd.dev.umd.edu/form?prdId=76c93dfd-4803-47af-810a-c34de3cb9eac",
	"X-Requested-With": "XMLHttpRequest"
}
auth = open("auth.txt", "r").read().split("\n")[0]
print("Using Auth Token: %s" % (auth,))

def login(l):
	with l.client.post("https://login.qa.umd.edu/cas/login", 
		params={"service":"https://itprd.dev.umd.edu/"}, 
		headers={"Authorization": auth}, 
		name= "Login",#"https://login.qa.umd.edu/cas/login",
		catch_response = True) as res:
		
		if "prd" not in res.url: 
			res.failure("Login Did not Go to PRD Page")
		
def logout(l):
	with l.client.post("https://login.qa.umd.edu/cas/logout", 
		name= "Logout",#"https://login.umd.edu/cas/logout",
		catch_response = True) as res:
		
		if "/logout" not in res.url:
			res.failure("Logout Failed to Jump to Correct Page")

def goToDash(l):
	l.client.get("/", name="Go Home")

def goToForm(l, prdId = "76c93dfd-4803-47af-810a-c34de3cb9eac"):
	with l.client.get("/form", params={"prdId": prdId}, catch_response=True, name= "Go To Form") as res:
		if prdId not in res.url:
			res.failure("Form %s Not Found" % prdId)

def goToNextDash(l):
	with l.client.get("/nextsupervisor", catch_response=True, name= "Next Supervisor Page") as res:
		if "nextsupervisor" not in res.url:
			res.failure("Next Supervisor Dashboard Not Found")

def impersonate(l, user = "testprd0"):
	with l.client.get("/backdoor/j_spring_security_switch_user", params={"username": user}, catch_response=True, name= "Impersonate %s" % user) as res:
		if "prd" not in res.url:
			res.failure("Impersonation Failed")

def updateForm(l, prdId = "76c93dfd-4803-47af-810a-c34de3cb9eac"):
	global my_mutex
	my_mutex.acquire()
	global body
	body["quarterDetails[1].operationList[0].expDesc"] = body["quarterDetails[1].quarter.updatedDate"]
	global headers
	with l.client.post("/form", params={"prdId": prdId}, headers=headers, data=body, catch_response=True, name="Update Form") as res:
		body["quarterDetails[1].quarter.updatedDate"] = res.text[:-1]
	my_mutex.release()

def runUser(l):
	impersonate(l,"ssaxena1")
	goToForm(l)
	updateForm(l)

def runSuper(l):
	impersonate(l,"labaru")
	goToForm(l)
	updateForm(l)

def runNext(l):
	impersonate(l,"wgomes")
	goToNextDash(l)
	#goToForm(l)

class UserBehavior(TaskSet):
	tasks = {goToDash: 1, runUser: 1, runSuper: 1, runNext: 1}

	def on_start(self):
		login(self)
	
	def on_stop(self):
	    logout(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1.25, 2.25)
