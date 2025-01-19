import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, filedialog, messagebox
from tkinter import ttk

from dotenv import load_dotenv
from utils.calendar import generate_calendar


def run_script(email, password):
    try:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 40)

        driver.get("https://intoconnect.intoglobal.com/org/exeter/StudentTimetableMember")


        student_login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class, 'login login--INTO')])[last()]"))
        )
        student_login_button.click()

        email_field = wait.until(EC.visibility_of_element_located((By.ID, "Email")))
        driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
        email_field.send_keys(email)

        password_field = wait.until(EC.visibility_of_element_located((By.ID, "Password")))
        password_field.send_keys(password)

        student_login_button = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@class='btn btn-lg btn-brand-primary btn-block' and @type='submit']")
        ))
        student_login_button.click()


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
                    date_string = dateField.text  # "13 January 2025"
                    current_date = datetime.strptime(date_string, "%d %B %Y").strftime("%Y-%m-%d")
                except Exception as e:
                    print(f"Error parsing date: {e}")
                    continue
            else:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells and current_date:
                    event_time = cells[0].text.strip() if len(cells) > 0 else None
                    event_title = cells[2].text.strip() if len(cells) > 2 else None

                    data.append({
                        "date": current_date,
                        "time": event_time,
                        "title": event_title
                    })

        driver.quit()


        generate_calendar(data)
        return data

    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        raise e


def on_run():
    email = email_entry.get()
    password = password_entry.get()


    if not email or not password :
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        events = run_script(email, password)
        output_text.delete(1.0, "end")
        for event in events:
            output_text.insert("end", f"{event['date']} {event['time']} - {event['title']}\n")
        messagebox.showinfo("Success", "Events fetched and calendar generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = Tk()
root.title("Calendar Event Fetcher")
root.geometry("600x400")

# Labels and Inputs
Label(root, text="Email:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
email_entry = Entry(root, width=40)
email_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = Entry(root, width=40, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)





# Run Button
run_button = Button(root, text="Run", command=on_run)
run_button.grid(row=3, column=1, pady=10)

# Output Text Area
Label(root, text="Output:").grid(row=4, column=0, padx=10, pady=5, sticky="ne")
output_text = Text(root, width=60, height=15)
output_text.grid(row=4, column=1, padx=10, pady=5)
scrollbar = Scrollbar(root, command=output_text.yview)
scrollbar.grid(row=4, column=2, sticky="ns")
output_text.config(yscrollcommand=scrollbar.set)

# Start GUI
root.mainloop()
