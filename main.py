from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ics import Calendar, Event

from dotenv import load_dotenv
import os


load_dotenv()


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 40)

try:
    
    driver.get(URL)

    
    student_login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'login login--INTO')])[last()]"))
    )
    student_login_button.click()

    
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "Email")))
    driver.execute_script("arguments[0].scrollIntoView(true);", email_field)

    
    if email_field.is_displayed():
        email_field.send_keys(EMAIL)
    else:
        print("Email field is not visible.")

    
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "Password")))
    if password_field.is_displayed():
        password_field.send_keys(PASSWORD)
    else:
        print("Password field is not visible.")

    student_login_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@class='btn btn-lg btn-brand-primary btn-block' and @type='submit']")))

    
    if student_login_button.is_displayed():
        student_login_button.click()
    else:
        print("Login button is not visible.")


    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fc-list-table")))


    rows = table.find_elements(By.TAG_NAME, "tr")


    data = []
    for row in rows:
        
        cells = row.find_elements(By.TAG_NAME, "td")  
        
        data.append([cell.text for cell in cells])
    
    
    for row in data:
        print(row)
    calendar = Calendar()


    for item in data:
        if not item:
            continue  
        time_range, _, description = item
        start_time, end_time = time_range.split(" - ")


        event = Event()
        event.name = description  
        event.begin = f"2025-01-13 {start_time}"  
        event.end = f"2025-01-13 {end_time}"      


        calendar.events.add(event)

    with open("schedule.ics", "w") as file:
        file.writelines(calendar)

    print("ICS file created: schedule.ics")

finally:

    driver.quit()
