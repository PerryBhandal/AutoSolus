USERNAME = "netid_nospaces"
PASSWORD = "password"

#Time to sleep on pages that render their contents using AJAX
RENDER_SLEEP_TIME = 3

import logging
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchFrameException, NoSuchElementException

class AutoSolus():
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        self.createDriver()
        
        self.run()
    
    def createDriver(self):
        logging.warn("Creating web driver")
        self.driver = webdriver.Firefox()
        self.driver.get("http://my.queensu.ca")
    
    def run(self):
        logging.warn("Logging in");
        #Log in
        self.logIn()
        
        #Hit the solus link
        logging.warn("Clicking solus link")
        self.clickSolus()
        
        #Get to the course cart page
        self.getToAdd()

        self.renderSleep()

        #Try to add what's in your cart
        self.clickButton("DERIVED_REGFRM1_LINK_ADD_ENRL$115$")

        self.renderSleep()

        #Finish enrolling
        self.clickButton("DERIVED_REGFRM1_SSR_PB_SUBMIT")

        self.renderSleep()
    
    
    def renderSleep(self):
        """
        Sleep to be used on pages that render
        using AJAX. Prevents element not found
        errors.
        """
        time.sleep(RENDER_SLEEP_TIME)

    def clickButton(self, elementID):
        self.driver.find_element_by_id(elementID).click()
    
    def doOptionClick(self, name, text):
        self.driver.find_element_by_xpath("//select[@name='"+name+"']/option[text()='"+text+"']").click()
    
    def getToAdd(self):
        """
        Gets from the main logged in SOLUS page to the course add page.
        """
        logging.warn("Getting to add page")
        #Switch to our main frame
        try:
            self.driver.switch_to_frame("TargetContent")
        except NoSuchFrameException:
            logging.error("Hit NoSuchFramEexception, sleeping then trying again.");
            time.sleep(0.5)
            self.driver.switch_to_frame("TargetContent")
        
        #click our select on add courses
        self.doOptionClick("DERIVED_SSS_SCL_SSS_MORE_ACADEMICS", "Enrollment: Add")
        
        #Submit that page
        self.clickButton("DERIVED_SSS_SCL_SSS_GO_1")
        
    
    def clickSolus(self):
        solusButton = self.driver.find_element_by_link_text("SOLUS")
        solusButton.click()

    def clickButton(self, buttonID):
        self.driver.find_element_by_id(buttonID).click()
    
    def logIn(self):
        """
        Gets to the main logged in page of SOLUS.
        """
        #Find the form inputs
        username = self.driver.find_element_by_id('username')
        password = self.driver.find_element_by_id('password')
        
        #Enter our login data
        username.send_keys(self.username)
        password.send_keys(self.password)
        
        #Submit the page
        logging.warn("Submitting login form")
        submitButton = self.driver.find_element_by_name("Login")
        submitButton.click()
    
AutoSolus(USERNAME, PASSWORD)
