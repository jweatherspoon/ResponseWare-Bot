#!/usr/bin/python

from Tkinter import *

from selenium import webdriver
from selenium.webdriver.common import keys

import time
import thread
import clicker

URL = "http://responseware.turningtechnologies.com"

def main():
	w = Window(font="Century Gothic")
	w.setTitle("ResponseWare Bot")
	#w.setIcon("./responseware.ico")
	w.run()
	
class Window():
	def __init__(self, *args, **kwargs):
		self.root = Tk()
		
		self.bg = self.fg = self.font = None
		#Check for font, bg, fg, etc.
		if kwargs is not None:
			if "font" in kwargs.keys():
				self.font = (kwargs["font"], 12)
			if "bg" in kwargs.keys():
				self.bg = kwargs["bg"]
			if "fg" in kwargs.keys():
				self.fg = kwargs["fg"]
		
		self.root["bg"] = self.bg
		self.root["fg"] = self.fg
		
		self.BTN_FG = "#000"
		self.BTN_BG = "#DDD"
		
		self.active = False
		
		self.__createGUI()
		
		#focus session id for the user
		self.sessionId.focus()
		
		#Add event handlers
		self.signInBtn.bind("<Button-1>", self.signIn)
		self.closeBrowserBtn.bind("<Button-1>", self.closeBrowser)
		self.activeBtn.bind("<Button-1>", self.toggleActive)
		self.reloadClickerBtn.bind("<Button-1>", self.reloadClicker)
		
		self.sessionId.bind("<Return>", self.signIn)
		self.username.bind("<Return>", self.signIn)
		self.passwd.bind("<Return>", self.signIn)
		
		self.root.bind("<Escape>", self.close)
		self.root.protocol("WM_DELETE_WINDOW", self.close)
		
		self.browser = webdriver.Chrome()
		
	def run(self):
		self.root.mainloop()
		
	def signIn(self, event):
		sessId = self.sessionId.get()
		user = self.username.get()
		passwd = self.passwd.get()
			
		if self.browser is None:
			self.browser = webdriver.Chrome()
			time.sleep(2)
			
		thread.start_new_thread(clicker.SignIn, (self.browser, URL, sessId, user, passwd))
		
	def closeBrowser(self, event):
		if self.browser is not None:
			self.browser.close()
			self.browser = None
			
	def toggleActive(self, event):
		self.active = not self.active
		self.activeBtn["text"] = "Disable" if self.active else "Activate"
		
		if self.active:
			thread.start_new_thread(self.__pollQuestions, ())
		
	def setTitle(self, title):
		self.root.wm_title(title)
		
	def setIcon(self, iconPath):
		self.root.wm_iconbitmap(iconPath)
		
	def close(self, *args):
		self.root.destroy()
		if self.browser is not None:
			self.browser.close()
		raise SystemExit()
		
	def reloadClicker(self, event):
		reload(clicker)
		
	def __createGUI(self):
		
		self.topRow = Frame(self.root)
		self.topRow.grid(row=0,columnspan=2, sticky=S)
		
		self.sessionLbl = Label(self.root, text="Session ID: ", font=self.font, bg=self.bg, fg=self.fg)
		self.userLbl = Label(self.root, text="Username: ", font=self.font, bg=self.bg, fg=self.fg)
		self.passLbl = Label(self.root, text="Password: ", font=self.font, bg=self.bg, fg=self.fg)
		
		self.sessionId = Entry(self.root, font=self.font)
		self.username = Entry(self.root, font=self.font)
		self.passwd = Entry(self.root, font=self.font, show="*")
	
		self.signInBtn = Button(self.topRow, text="Sign In", bg=self.BTN_BG, fg=self.BTN_FG)
		self.activeBtn = Button(self.topRow, text="Activate", bg=self.BTN_BG, fg=self.BTN_FG)
		
		self.signInBtn.grid(row=0, column=0, sticky=EW, padx=10)
		self.activeBtn.grid(row=0, column=1, sticky=EW, padx=10)
		
		self.sessionLbl.grid(row=1, column=0, sticky=E)
		self.sessionId.grid(row=1, column=1)
		
		self.userLbl.grid(row=2, column=0, sticky=E)
		self.username.grid(row=2, column=1)
		
		self.passLbl.grid(row=3, column=0, sticky=E)
		self.passwd.grid(row=3, column=1)
	
		self.closeBrowserBtn = Button(self.root, text="Close Browser", font=self.font, bg=self.BTN_BG, fg=self.BTN_FG)
		self.closeBrowserBtn.grid(row=4, column=0)
		
		self.reloadClickerBtn = Button(self.root, text="Reload", font=self.font, bg=self.BTN_BG, fg=self.BTN_FG)
		self.reloadClickerBtn.grid(row=4, column=1)
		
	def __pollQuestions(self):
		while self.active and self.browser is not None:
			if clicker.QuestionOpen(self.browser):
				clicker.AnswerQuestion(self.browser)
			time.sleep(1)
	
main()