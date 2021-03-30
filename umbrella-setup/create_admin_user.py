
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pyvirtualdisplay import Display
import os, sys

def connectFirefox():
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    print("Firefox Headless Browser Invoked")
    return driver


EMAIL = "admin@wifisess.gov"
driver = connectFirefox()

print(sys.argv)
driver.get("https://" + sys.argv[1] + "/admins/signup")
elem = driver.find_element(By.ID, 'admin_username')
elem.send_keys(EMAIL)
elem = driver.find_element(By.ID, "admin_password")
elem.send_keys(EMAIL)
elem = driver.find_element(By.ID, "admin_password_confirmation")
elem.send_keys(EMAIL)

elem = driver.find_element(By.NAME, "commit")
elem.click()