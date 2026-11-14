import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def run_recon():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    recon_data = {}

    try:
        print("[1] Navigating to Login Page...")
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        # Wait for login form
        wait.until(EC.visibility_of_element_located((By.NAME, "username")))

        login_url = driver.current_url
        page_title = driver.title

        # Check login credentials hint box
        hint_elements = driver.find_elements(By.CSS_SELECTOR, ".orangehrm-demo-credentials")
        hint_text = hint_elements[0].text if hint_elements else "N/A"

        # Check inputs
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        recon_data["login"] = {
            "url": login_url,
            "title": page_title,
            "username_name": username_input.get_attribute("name"),
            "username_placeholder": username_input.get_attribute("placeholder"),
            "password_name": password_input.get_attribute("name"),
            "password_placeholder": password_input.get_attribute("placeholder"),
            "button_type": login_button.get_attribute("type"),
            "button_text": login_button.text,
            "credentials_hint": hint_text,
        }
        print("Login Page Details:", json.dumps(recon_data["login"], indent=2))

        # Perform login
        print("[2] Logging in with Admin / admin123...")
        username_input.send_keys("Admin")
        password_input.send_keys("admin123")
        login_button.click()

        # Wait for dashboard
        wait.until(EC.url_contains("/dashboard/index"))
        dashboard_url = driver.current_url

        # Capture sidebar items
        sidebar_items = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".oxd-main-menu-item"))
        )
        menu_items = []
        for item in sidebar_items:
            href = item.get_attribute("href")
            span = item.find_elements(By.CSS_SELECTOR, ".oxd-main-menu-item--name")
            text = span[0].text if span else item.text
            menu_items.append({"name": text, "href": href})

        # User dropdown
        user_dropdown = driver.find_elements(By.CSS_SELECTOR, ".oxd-userdropdown-name")
        user_name = user_dropdown[0].text if user_dropdown else "N/A"

        # Version info/footer
        footer_links = driver.find_elements(By.CSS_SELECTOR, ".oxd-layout-footer p")
        footer_text = " | ".join([f.text for f in footer_links])

        recon_data["dashboard"] = {
            "url": dashboard_url,
            "user_name": user_name,
            "footer": footer_text,
            "menu_items": menu_items,
        }
        print("Dashboard details:", json.dumps(recon_data["dashboard"], indent=2))

        # Module Reconnaissance
        modules_to_check = ["Admin", "PIM", "Leave", "Recruitment", "My Info", "Directory"]
        recon_data["modules"] = {}

        for item in menu_items:
            name = item["name"]
            href = item["href"]
            if name in modules_to_check and href:
                print(f"[3] Inspecting module: {name} at {href}...")
                driver.get(href)
                time.sleep(2)

                # Header title
                header_elems = driver.find_elements(
                    By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6"
                )
                headers = [h.text for h in header_elems if h.text]

                # Check for top bar navigation tabs
                nav_tabs = driver.find_elements(By.CSS_SELECTOR, ".oxd-topbar-body-nav-tab-item")
                tabs = [t.text for t in nav_tabs if t.text]

                # Check for action buttons (Add, Search, Reset)
                buttons = driver.find_elements(By.CSS_SELECTOR, "button")
                button_texts = [b.text for b in buttons if b.text]

                # Check for table headers if present
                th_elems = driver.find_elements(By.CSS_SELECTOR, ".oxd-table-header .oxd-table-th")
                col_headers = [th.text.replace("\n", " ").strip() for th in th_elems if th.text]

                # Check for inputs / dropdowns in filter/form
                inputs = driver.find_elements(By.CSS_SELECTOR, ".oxd-input")
                selects = driver.find_elements(By.CSS_SELECTOR, ".oxd-select-wrapper")

                recon_data["modules"][name] = {
                    "url": driver.current_url,
                    "breadcrumb": headers,
                    "tabs": tabs,
                    "buttons": button_texts,
                    "table_columns": col_headers,
                    "inputs_count": len(inputs),
                    "dropdowns_count": len(selects),
                }
                print(f"Module {name} summary:", json.dumps(recon_data["modules"][name], indent=2))

        # Test logout
        print("[4] Testing Logout...")
        driver.find_element(By.CSS_SELECTOR, ".oxd-userdropdown-tab").click()
        time.sleep(1)
        logout_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']")))
        logout_link.click()
        wait.until(EC.url_contains("/auth/login"))
        recon_data["logout"] = {
            "final_url": driver.current_url,
            "success": "/auth/login" in driver.current_url,
        }
        print("Logout verified:", recon_data["logout"])

    finally:
        driver.quit()

    with open("docs/recon_output.json", "w") as f:
        json.dump(recon_data, f, indent=2)
    print("Recon completed successfully and saved to docs/recon_output.json")


if __name__ == "__main__":
    run_recon()
