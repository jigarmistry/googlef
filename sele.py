from selenium import webdriver
import time
# browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
browser = webdriver.PhantomJS("/usr/local/lib/phantomjs/bin/phantomjs")

browser.get('https://accounts.google.com/ServiceLogin?service=finance')

emailElem = browser.find_element_by_id('Email')
emailElem.send_keys('parasdoshipu@gmail.com')
nextButton = browser.find_element_by_id('next')
nextButton.click()
time.sleep(2)
passwordElem = browser.find_element_by_id('Passwd')
passwordElem.send_keys('algoforme12')
signinButton = browser.find_element_by_id('signIn')
signinButton.click()

browser.get('https://www.google.com/finance/portfolio?action=view&pid=3&authuser=2&ei=sAg8WLn-MYviugSQ_4WQBA?pview=sview')
element = browser.find_element_by_class_name("gf-table").get_attribute('innerHTML')
print (element.encode("utf-8"))
