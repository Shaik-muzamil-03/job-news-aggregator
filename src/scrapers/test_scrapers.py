import logging
from indeed import IndeedScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scraper_test")

def test_indeed_scraper():
    scraper = IndeedScraper()
    scraper.start_driver()
    jobs = scraper.search_jobs("Angular developer")
    logger.info(f"Indeed jobs: {jobs}")
    scraper.close()

if __name__ == "__main__":
    # test_indeed_scraper()
    test_indeed_scraper()
