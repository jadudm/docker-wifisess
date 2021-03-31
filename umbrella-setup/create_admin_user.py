from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json, os, requests, sys

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
URL = "https://" + sys.argv[1]
# We need some implicit waiting.
# Why? Because API Umbrella has some weird interstertials from the Ember
# framework, and pageload often results in a JS thing loading yet more content.
# So, we'll try/catch, and wait to see if key elements arrive.
driver.implicitly_wait(10) 

def create_admin_user(email):
    print("Creating initial admin user: " + email)
    # This might not be the first run. Make sure there's a admin_password_confirmation
    # box on this page. If there is, then fill this stuffs
    logged_in = False
    try:
        driver.get(f"{URL}/admins/signup")
        # Try and find this first. If this fails, it means we're not doing this
        # for the first time. *Groundhog Day*...
        driver.find_element(By.ID, "admin_password_confirmation")
        e = driver.find_element(By.ID, 'admin_username')
        e.send_keys(email)
        e = driver.find_element(By.ID, "admin_password")
        e.send_keys(email)
        e = driver.find_element(By.ID, "admin_password_confirmation")
        e.send_keys(email)
        e = driver.find_element(By.NAME, "commit")
        e.click()
        logged_in = True
    except:
        print("Admin may have been created already. Try logging in.")
    return logged_in

def try_logging_in(email):
    # If the user is already created, we now need to try logging in.
    logged_in = False
    if not logged_in:
        try:
            driver.get(f"{URL}/admin/login")
            e = driver.find_element(By.ID, 'admin_username')
            e.send_keys(email)
            e = driver.find_element(By.ID, "admin_password")
            e.send_keys(email)
            e = driver.find_element(By.NAME, "commit")
            e.click()
            logged_in = True
        except:
            print("Could not log in. Exiting.")
            sys.exit()
    return logged_in

def wait_for(condition_function):
  start_time = time.time()
  while time.time() < start_time + 3:
    if condition_function():
      return True
    else:
      time.sleep(0.1)
  raise Exception(
   'Timeout waiting for {}'.format(condition_function.name)
  )
class wait_for_page_load(object):
  def __init__(self, browser):
    self.browser = browser
  def __enter__(self):
    self.old_page = self.browser.find_element_by_tag_name('html')
  def page_has_loaded(self):
    self.new_page = self.browser.find_element_by_tag_name('html')
    return self.new_page.id != self.old_page.id
  def __exit__(self, *_):
    wait_for(self.page_has_loaded)
    # self.old_page = self.new_page
    # wait_for(self.page_has_loaded) 

def create_new_api_user(email):
    print("Creating new API user for " + email)
    driver.get(f"{URL}/admin/#/api_users/new")
    e = driver.find_element(By.XPATH, "//input[contains(@id,'email')]")
    e.clear()
    e.send_keys(email)
    e = driver.find_element(By.XPATH, "//input[contains(@id,'firstName')]")
    e.clear()
    e.send_keys("Admin")
    e = driver.find_element(By.XPATH, "//input[contains(@id,'lastName')]")
    e.clear()
    e.send_keys("WifiSess")
    e = driver.find_element(By.XPATH, "//textarea[contains(@id,'useDescription')]")
    e.clear()
    e.send_keys("FOR GREAT JUSTICE")
    e = driver.find_element(By.XPATH, "//label[contains(@for,'termsAndConditions')]")
    e.click()
    print(f"Clicking Save")
    button_xpath = "//button[contains(concat(' ',normalize-space(@class),' '), ' save-button ')][contains(., 'Save')]"
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
    # e = driver.find_element(By.XPATH, button_xpath)
    # e.click()
    # Wait for the page to refresh, or the data isn't saved.

    # print(driver.page_source.encode("utf-8"))
    # with wait_for_page_load(driver):
    #     driver.find_element(By.XPATH, "//div[contains(@id, 'content')]/h1[text()='API Users']")

    # FIXME: This is finding the button, but the save is not happening.
    # Ember.js could be part of the challenge? Or, am I clicking the wrong element?
    e = driver.find_element(By.XPATH, button_xpath)
    e.click()

def try_retrieving_admin_listing():
    # We can click on #/admins to get a list of admin users.
    print("Trying to get the admin listing")
    try:
        driver.get(f"{URL}/admin/#/admins")
    except:
        print("Failed to get the admin listing. Exiting.")
        sys.exit()

def fetch_api_key(email):
    print("Getting the admin user's API key.")
    # Now, we can click on our email address.
    # This is annoying, because the ember framework inserts unique IDs everywhere
    # Or, perhaps that is our unique ID. Either way, we need to find the <a> with our email address.
    # <a href="#/admins/0a852db1-c3a3-45db-96c2-a937648a954e/edit">admin@wifisess.gov</a>
    driver.get(f"{URL}/admin/#/admins")
    e = driver.find_element(By.XPATH, '//a[text()="' + email + '"]')    
    e.click()
    # Find the span element that has the appropriate class. It's not terribly unique in this page otherwise.
    e = driver.find_element(By.XPATH, "//div/span[contains(concat(' ',normalize-space(@class),' '),' api-key ')]")
    
    if not(len(e.text) > 0):
        print("Could not find the API key. Exiting.")
        sys.exit()
    print("Admin API key is: " + e.text)
    api_key = e.text

    # Exit the page by saving. This eliminates the risk of alerts.
    e = driver.find_element(By.XPATH, "//button/span[text()='Save']")
    e.click()
    
    return api_key

def get(url, data, headers):
    return requests.get(url, data=data, headers=headers, verify=False)

def list_admins(api_key):
    headers = {'Content-Type': 'application/json', 'X-Api-Key': api_key}
    # We always need to set verify to false.
    response = get(f'{URL}/api-umbrella/v1/admins.json', {}, headers)
    return response.json()

logged_in = create_admin_user(EMAIL)
if not logged_in:
    logged_in = try_logging_in(EMAIL)
if logged_in:
    # First, create a new API user.
    create_new_api_user(EMAIL) # FIXME: This is failing.
    try_retrieving_admin_listing()
    admin_token = fetch_api_key(EMAIL)
    print(list_admins(api_key))


# Now, we can do things with the API key!



