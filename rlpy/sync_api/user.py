from logging import getLogger
from playwright.sync_api import Page, Error as PlaywrightError
from ..user import BaseUser, Console, UserScrapeError


class User(BaseUser):
	def get_data(self, page: Page = None, get_player_name=False, wait_for_update=True,
									close_page_on_finish=False, use_request_api=False, **kwargs) -> "User":
		super().get_data(page=page, get_player_name=get_player_name, wait_for_update=wait_for_update,
						 close_page_on_finish=close_page_on_finish, use_request_api=use_request_api, **kwargs)
		from time import sleep
		from bs4 import BeautifulSoup
		from datetime import datetime as dt, timedelta as td
		from re import search

		logger = kwargs.get("logger", getLogger(__name__))
		max_tries = kwargs.get("max_tries", 5)
		delay = kwargs.get("delay_seconds", 1)
		tries = 1

		created_playwright = page is None
		if created_playwright:
			from playwright.sync_api import sync_playwright

			p = sync_playwright().start()
			logger.debug("Opened playwright to get data.", extra=self.log_extra)
			browser = p.firefox.launch(headless=kwargs.get("headless", True),
									   slow_mo=kwargs.get("slow_mo", 85))
			logger.debug("Opened chromium.", extra=self.log_extra)
			page = browser.new_page()
			page.set_default_timeout(kwargs.get("timeout", 0))
			logger.debug("Opened page.", extra=self.log_extra)

		page.goto(self.link)
		logger.debug(f"Requesting RLStats webpage for {self.player_name}: {self.link}.",
					 extra=self.log_extra)

		while tries <= max_tries:
			try:
				compact = page.locator('button[title="Switch to Compact Version"]')
				compact.wait_for(state="attached")
				logger.debug(f"Page loaded for {self.link}.", extra=self.log_extra)

				if page.title() == "404 Not Found":
					raise UserScrapeError(f"The requested URL was not found on this server.")

				soup = BeautifulSoup(page.content(), "html.parser")

				if close_page_on_finish:
					page.close()
				break
			except KeyboardInterrupt as e:
				logger.warning("Keyboard Interrupt stopped the page scraping process in Playwright.",
							   extra=self.log_extra)
				page.close()
				raise e
			except BaseException as e:
				if isinstance(e, PlaywrightError):
					if "crashed" in e.message:
						logger.exception("Something crashed in Playwright trying to scrape the data.", extra=self.log_extra)
						raise e

				logger.exception(f"An error occurred trying to scrape website data. Try: {tries:,} of {max_tries:,}.",
								 extra=self.log_extra)
				tries += 1
				if tries == max_tries:
					raise e
				sleep(delay)
				page.reload()

		if created_playwright:
			if not page.is_closed():
				page.close()
			browser.close()
			p.stop()

		return self._process_data(soup, get_player_name=get_player_name, **kwargs)
