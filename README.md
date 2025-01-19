# Selenium-Based Event Fetcher

This Python script uses Selenium to log in to a student platform, fetch event data for the upcoming week, and process it into a calendar format. The calendar is generated using the `generate_calendar` function from the `utils/calendar.py` module.

---

## Features
- Logs in to the student platform automatically using Selenium.
- Fetches event data for the next week from the platform.
- Processes and formats the data into a calendar using `generate_calendar`.

---

## Prerequisites
- Python 3.8 or higher
- Google Chrome installed
- ChromeDriver installed and added to the system PATH
- Required Python libraries installed (`pip install -r requirements.txt`)

---

## Folder Structure
```
project/
│
├── main.py               # Main script (the provided code)
├── .env                  # Environment variables file
├── utils/
│   ├── __init__.py       # Makes the utils folder a package
│   └── calendar.py       # Contains the generate_calendar function
├── README.md             # Usage guide and documentation
```

---

## Configuration

### Environment Variables
The script uses a `.env` file for sensitive credentials and configurations. Create a `.env` file in the root directory and include the following variables:

```env
EMAIL=your_email@example.com
PASSWORD=your_password
URL=https://example.com/login
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd project
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `ChromeDriver` is installed and added to your system PATH.

4. Set up your `.env` file as described above.

---

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. The script will:
   - Navigate to the login page specified in the `URL`.
   - Log in using the provided `EMAIL` and `PASSWORD`.
   - Fetch event data for the next week.
   - Pass the data to the `generate_calendar` function for calendar generation.

---

## Example Output

The script fetches events and formats them as JSON-like objects. Example:
```json
[
    {
        "date": "2025-01-13",
        "time": "10:00 AM",
        "title": "Mathematics Lecture"
    },
    {
        "date": "2025-01-14",
        "time": "2:00 PM",
        "title": "Physics Lab"
    }
]
```

The `generate_calendar` function processes this data into a calendar format.

---

## Dependencies

Install the following libraries via `pip`:
- `selenium`
- `ics`
- `python-dotenv`

---

## Notes
- Ensure your Chrome browser version matches the installed ChromeDriver version.
- If any element is not found during execution, check the XPaths or class names used in the script and update them as needed.
