import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def deep_probe():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    details = {}

    try:
        # 1. Invalid login & validation error inspection
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        wait.until(EC.visibility_of_element_located((By.NAME, "username")))

        # Test empty submit
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(1)

        val_errors = driver.find_elements(By.CSS_SELECTOR, ".oxd-input-group__message")
        details["empty_login_errors"] = [e.text for e in val_errors]

        # Test invalid credentials
        user_input = driver.find_element(By.NAME, "username")
        pass_input = driver.find_element(By.NAME, "password")
        user_input.send_keys("InvalidUser999")
        pass_input.send_keys("WrongPass123")
        submit_btn.click()

        alert_elem = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-alert-content-text"))
        )
        details["invalid_login_alert"] = alert_elem.text

        # 2. Login valid Admin
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        user_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        pass_input = driver.find_element(By.NAME, "password")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        user_input.send_keys("Admin")
        pass_input.send_keys("admin123")
        submit_btn.click()
        wait.until(EC.url_contains("/dashboard/index"))

        # 3. Add Employee Form
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee")
        wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))

        first_name = driver.find_element(By.NAME, "firstName")
        middle_name = driver.find_element(By.NAME, "middleName")
        last_name = driver.find_element(By.NAME, "lastName")

        # Check employee ID field
        inputs = driver.find_elements(By.CSS_SELECTOR, ".oxd-input")
        emp_id_val = ""
        for inp in inputs:
            val = inp.get_attribute("value")
            # Usually emp id is pre-filled with next id
            if val and val.isdigit():
                emp_id_val = val
                break

        # Check toggle for login details
        login_switch = driver.find_elements(By.CSS_SELECTOR, ".oxd-switch-input")

        details["add_employee_form"] = {
            "first_name_name": first_name.get_attribute("name"),
            "middle_name_name": middle_name.get_attribute("name"),
            "last_name_name": last_name.get_attribute("name"),
            "emp_id_default": emp_id_val,
            "has_login_switch": len(login_switch) > 0,
        }

        # 4. Check PIM employee list search fields and records count
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-table")))

        records_found = driver.find_elements(
            By.CSS_SELECTOR, ".orangehrm-horizontal-padding .oxd-text"
        )
        records_text = [r.text for r in records_found if "Record" in r.text or "Found" in r.text]

        details["employee_list"] = {"records_text": records_text[0] if records_text else "N/A"}

        # 5. Check Apply Leave form
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/leave/applyLeave")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-form")))
        leave_selects = driver.find_elements(By.CSS_SELECTOR, ".oxd-select-wrapper")
        date_inputs = driver.find_elements(By.CSS_SELECTOR, ".oxd-date-input input")

        details["apply_leave_form"] = {
            "dropdowns": len(leave_selects),
            "date_inputs": len(date_inputs),
        }

        # 6. Check Recruitment Add Candidate form
        driver.get(
            "https://opensource-demo.orangehrmlive.com/web/index.php/recruitment/addCandidate"
        )
        wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
        cand_first = driver.find_element(By.NAME, "firstName")
        cand_last = driver.find_element(By.NAME, "lastName")
        cand_email = driver.find_elements(
            By.XPATH, "//label[text()='Email']/../following-sibling::div//input"
        )

        details["add_candidate_form"] = {
            "first_name": cand_first.get_attribute("name"),
            "last_name": cand_last.get_attribute("name"),
            "email_found": len(cand_email) > 0,
        }

    finally:
        driver.quit()

    with open("docs/deep_probe_output.json", "w") as f:
        json.dump(details, f, indent=2)
    print("Deep probe completed successfully and saved to docs/deep_probe_output.json")
    print(json.dumps(details, indent=2))


if __name__ == "__main__":
    deep_probe()
