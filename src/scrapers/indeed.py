
import time
import logging
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up logger
logger = logging.getLogger("IndeedScraper")
logger.setLevel(logging.DEBUG)



class IndeedScraper:

    

    def __init__(self, email: str = None, password: str = None, use_google_login: bool = False):
        self.email = email
        self.password = password
        self.use_google_login = use_google_login
        self.driver = None
        logger.debug(f"IndeedScraper initialized with email={email}, use_google_login={use_google_login}")

    def start_driver(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        logger.debug("Starting Chrome driver with options: %s", options.arguments)
        self.driver = webdriver.Chrome(options=options)
        logger.info("Chrome driver started.")

    def login(self):
        if not self.use_google_login:
            logger.debug("Google login not requested, skipping login.")
            return  # Implement regular login if needed
        logger.debug("Navigating to Indeed login page.")
        self.driver.get('https://secure.indeed.com/auth')
        try:
            google_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-gnav-element-name, 'google')]"))
            )
            logger.debug("Google login button found, clicking.")
            google_btn.click()
            # Google login flow
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            logger.debug("Google email input found, entering email.")
            email_input.send_keys(self.email)
            email_input.send_keys(Keys.RETURN)
            time.sleep(2)
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            logger.debug("Google password input found, entering password.")
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(3)
        except Exception as e:
            logger.error(f"Google login failed: {e}")

    def search_jobs(self, query: str, location: str = ""):  # Add more filters as needed
        logger.info(f"Searching Indeed for jobs with query='{query}' and location='{location}'")
        self.driver.get(f"https://www.indeed.com/jobs?q={query}&l={location}")
        time.sleep(2)
        jobs = []
        job_cards = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'job_seen_beacon')]")
        logger.debug(f"Found {len(job_cards)} job cards on the page.")
        for idx, card in enumerate(job_cards):
            try:
                # Title
                try:
                    title = card.find_element(By.CSS_SELECTOR, 'h2.jobTitle').text.strip()
                    if not title:
                        raise ValueError("Title is empty or whitespace.")
                except Exception as e:
                    logger.warning(f"Job card {idx}: Could not find job title: {e}")
                    title = None

                # Use BeautifulSoup for company and location
                soup = BeautifulSoup(card.get_attribute('outerHTML'), 'html.parser')
                company = None
                location_val = None
                company_tag = soup.select_one('span[data-testid="company-name"]')
                if company_tag:
                    company = company_tag.get_text(strip=True)
                else:
                    logger.warning(f"Job card {idx}: Could not find company name with BeautifulSoup.")

                location_tag = soup.select_one('div[data-testid="text-location"]')
                if location_tag:
                    location_val = location_tag.get_text(strip=True)
                else:
                    logger.warning(f"Job card {idx}: Could not find location with BeautifulSoup.")

                # URL
                try:
                    url = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    if url:
                        url = url.strip()
                except Exception as e:
                    logger.warning(f"Job card {idx}: Could not find job URL: {e}")
                    url = None

                logger.debug(f"Job {idx}: title='{title}', company='{company}', location='{location_val}', url='{url}'")
                # Only append jobs with all required non-empty fields
                if title and company and url:
                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location_val,
                        'url': url
                    })
                else:
                    logger.info(f"Job card {idx} skipped due to missing required fields.")
            except Exception as e:
                logger.warning(f"Failed to parse job card {idx}: {e}")
                continue
        logger.info(f"Total jobs scraped: {len(jobs)}")
        return jobs

    def close(self):
        if self.driver:
            logger.debug("Closing Chrome driver.")
            self.driver.quit()
