from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os, sys

def connectFirefox():
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    print("Firefox Headless Browser Invoked")
    return driver


EMAIL = "admin@wifisess.gov"
driver = connectFirefox()

print(sys.argv)
# We need some implicit waiting.
# Why? Because API Umbrella has some weird interstertials from the Ember
# framework, and pageload often results in a JS thing loading yet more content.
# So, we'll try/catch, and wait to see if key elements arrive.
driver.implicitly_wait(10) 

print("Creating initial admin user: " + EMAIL)
# This might not be the first run. Make sure there's a admin_password_confirmation
# box on this page. If there is, then fill this stuffs
logged_in = False
try:
    driver.get("https://" + sys.argv[1] + "/admins/signup")
    # Try and find this first. If this fails, it means we're not doing this
    # for the first time. *Groundhog Day*...
    driver.find_element(By.ID, "admin_password_confirmation")

    e = driver.find_element(By.ID, 'admin_username')
    e.send_keys(EMAIL)
    e = driver.find_element(By.ID, "admin_password")
    e.send_keys(EMAIL)
    e = driver.find_element(By.ID, "admin_password_confirmation")
    e.send_keys(EMAIL)
    e = driver.find_element(By.NAME, "commit")
    e.click()
    logged_in = True
except:
    print("Admin may have been created already. Try logging in.")

# If the user is already created, we now need to try logging in.
if not logged_in:
    try:
        driver.get("https://" + sys.argv[1] + "/admin/login")
        e = driver.find_element(By.ID, 'admin_username')
        e.send_keys(EMAIL)
        e = driver.find_element(By.ID, "admin_password")
        e.send_keys(EMAIL)
        e = driver.find_element(By.NAME, "commit")
        e.click()
    except:
        print("Could not log in. Exiting.")
        sys.exit()
    

# We can click on #/admins to get a list of admin users.
print("Trying to get the admin listing")
try:
    driver.get("https://" + sys.argv[1] + "/admin/#/admins")
except:
    print("Failed to get the admin listing. Exiting.")
    sys.exit()


print("Getting the admin user's API key.")
# Now, we can click on our email address.
# This is annoying, because the ember framework inserts unique IDs everywhere
# Or, perhaps that is our unique ID. Either way, we need to find the <a> with our email address.
# <a href="#/admins/0a852db1-c3a3-45db-96c2-a937648a954e/edit">admin@wifisess.gov</a>
driver.get("https://" + sys.argv[1] + "/admin/#/admins")
e = driver.find_element(By.XPATH, '//a[text()="' + EMAIL + '"]')    
e.click()
# Find the span element that has the appropriate class. It's not terribly unique in this page otherwise.
e = driver.find_element(By.XPATH, "//div/span[contains(concat(' ',normalize-space(@class),' '),' api-key ')]")

if not(len(e.text) > 0):
    print("Could not find the API key. Exiting.")
    sys.exit()

print("Admin API key is: " + e.text)

# Now, we can do things with the API key!



