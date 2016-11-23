#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common import keys

import sys
import time
import getpass

URL = "http://responseware.turningtechnologies.com"
ID = "jweatherspoon"

def main():
	if len(sys.argv) < 2:
		print "Usage:", sys.argv[0], "<session id>"
		sys.exit(1)
	
	sessionId = sys.argv[1]
	
	#Create the browser 
	b = webdriver.Chrome()
	b.get(URL)
	
	
	passwd = getpass.getpass()
	SignIn(b, URL, sessionId, ID, passwd)
	
	#Begin waiting for a question
	while True:
		if QuestionOpen(b):
			AnswerQuestion(b)
		time.sleep(.1)
		
	b.close()

#Sign in to the responseware online app
def SignIn(b, url, sessionId, username, password):
	GoToUrl(b, url)
	EnterSessionId(b, sessionId)
	EnterUsername(b, username)
	EnterPassword(b, password)
	AcceptParticipation(b)
	
def GoToUrl(b, url):
	b.get(url)

#Enter the session id and move onto the next step
def EnterSessionId(b, sessionId):
	while(True):
		try:
			#Enter the session id
			idInput = b.find_element_by_css_selector("input#sessionId.form-control")
			idBtn = b.find_element_by_css_selector("button#joinSessionButton.btn.btn-default.btn-primary.pull-right")

			idInput.send_keys(sessionId)
			idBtn.click()
			break
		except:
			pass
		time.sleep(.1)
		
#Enter your username and move on to the next step
def EnterUsername(b, ID):
	userEntered = False
	while True:
		try:
			if not userEntered:
				emailInput = b.find_element_by_css_selector("input#j_username.form-control.input-lg")
				emailInput.send_keys(ID + "@nevada.unr.edu")
				userEntered = True
				
			signInBtn = b.find_element_by_css_selector("button#signInButton.signInPanelControl.signInPanelControlPrimary.phaseOneControl.pull-right")
			signInBtn.click()
			
			break
		except:
			pass
		time.sleep(.1)

#Enter your password and move on to the next step
def EnterPassword(b, PASSWORD):
	passEntered = False
	while True:
		try:
			if not passEntered:
				passInput = b.find_element_by_css_selector("input#j_password.form-control.input-lg")
				passInput.send_keys(PASSWORD)
				passEntered = True
			
			time.sleep(1)

			signInBtn = b.find_element_by_css_selector("button#secondarySignInButton.signInPanelControl.signInPanelControlPrimary.phaseTwoControl.pull-right")
			signInBtn.click()
			
			break
		except:
			pass
		time.sleep(.1)

#Accept participation in the app and finish signing in
def AcceptParticipation(b):
	while True:
		try:
			submitBtn = b.find_element_by_id("participantInfoButton")
			submitBtn.click()
			
			break
		except:
			pass

		
def QuestionOpen(b):
	#Try getting a handle to something 
	try:
		messageView = b.find_element_by_id("sessionMessageView")
		return ("display: none;" in messageView.get_attribute("style"))
	except:
		return False

def AnswerQuestion(b):
	#Try getting multiple choice values first
	try:
		mC = b.find_element_by_id("multipleChoice")
		if "hidden" not in mC.get_attribute("class"):
			#Click the first available button
			answerButtons = b.find_elements_by_class_name("answerButtonGroup")[0].find_elements_by_css_selector("*")
			print answerButtons
			answerButtons[0].click()
	except Exception as e:
		print "Cannot find multiple choice answers!", e
		pass
	
	
#main()