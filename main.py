from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ics import Calendar, Event
from utils.calendar import generate_calendar

from dotenv import load_dotenv
import os


load_dotenv()


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("URL")

NEXT_WEEK_BUTTON = "fc-next-button fc-button fc-button-primary"


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

    # now the user is logged in






    next_week_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-next-button")))
    next_week_button.click()

    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fc-list-table")))


    rows = table.find_elements(By.TAG_NAME, "tr")


    data = []
    current_date = None  


    for row in rows:

        heading = row.find_elements(By.TAG_NAME, "th")
        if heading:
            try:

                dateField = heading[0].find_element(By.CLASS_NAME, "fc-list-day-side-text")
                date_string = dateField.text  #"13 January 2025"
                current_date = datetime.strptime(date_string, "%d %B %Y").strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
            except Exception as e:
                print(f"Error parsing date: {e}")
                continue
        else:

            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and current_date:  # Ensure we have a valid date for the event
                event_time = cells[0].text.strip() if len(cells) > 0 else None
                event_title = cells[2].text.strip() if len(cells) > 2 else None
                

                data.append({
                    "date": current_date,
                    "time": event_time,
                    "title": event_title
                })


    for row in data:
        print(row)

    generate_calendar(data)

finally:

    driver.quit()



