from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Paths
path_to_Chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
path_to_chromedriver = r"D:\ALL FOR ONE\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Set up the Service object
service = Service(path_to_chromedriver)

# Set up ChromeOptions
options = webdriver.ChromeOptions()
options.binary_location = path_to_Chrome
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-features=WebRTC")
options.add_argument("--use-angle=gl")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

def random_delay():
    time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds

def login_linkedin(email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

# Open LinkedIn login page
login_linkedin("ali.ahmedali042022@gmail.com", "#@#__#($-$)***AL")

# Wait for user input (manually login)
time.sleep(5)  # Give enough time to manually log in or use automation to log in

# List of profiles to visit (replace with actual LinkedIn profile URLs)
profiles = [
    "https://www.linkedin.com/in/mahmoud-attia-ibrahime-6b5720247/details/skills/?detailScreenTabIndex=0",
    "https://www.linkedin.com/in/mohammedemad-9951m/details/skills/",
    "https://www.linkedin.com/in/sayed-salama-843492284/details/skills/"
]

def endorse_skill(profile):
    driver.get(profile)
    random_delay()

    try:
        # Wait for the "Endorse" button to be present
        skills_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'artdeco-card pb3')]"))
        )
        
        # Scroll the skills section into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skills_section)
        random_delay()
        endorse_skill = skills_section.find_elements_by_xpath("//ul[contains(@class, 'QIkNKyDfARoaQLytMYhLUqyuMqYhzWNeA ')]")
        
        
        num_to_click = random.randint(1, len(endorse_skill))
        
        
        # Scroll the button into view
        
        random_delay()
        for button in num_to_click:
            try:
                # Scroll the button into view
                button_will_click=endorse_skill.find_elements_by_class_name("artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_will_click)
                random_delay()

                # Wait for the button to be clickable
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button_will_click))

                # Click the button
                button_will_click.click()
                print("Skill endorsed!")
                random_delay()
            except Exception as e:
                print("Could not click the endorse button:", e)
        # Wait for the button to be clickable
        
        
        # Click the button
        
        print("Skill endorsed!")
    except Exception as e:
        print("Could not find or click the endorse button:", e)

for profile in profiles:
    endorse_skill(profile)

# Close the browser
driver.quit()