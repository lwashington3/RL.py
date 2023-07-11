from json import loads, dumps
from logging import getLogger
from playwright.sync_api import sync_playwright, expect
from re import search


def scrape_skill_distributions(output_file, **kwargs):
	headless = kwargs.get("headless", True)
	logger = kwargs.get("logger", getLogger(__name__))
	playlists = {"10": "Ranked Duel 1v1",
				"11": "Ranked Doubles 2v2",
				"13": "Ranked Standard 3v3",
				"27": "Hoops",
				"28": "Rumble",
				"29": "Dropshot",
				"30": "Snowday",
				"34": "Tournament Matches"}
	with sync_playwright() as p:
		browser = p.firefox.launch(headless=headless)
		page = browser.new_page()
		json = {"data": [], "population": []}
		for num, name in playlists.items():
			page.goto(f"https://api.tracker.gg/api/v1/rocket-league/distribution/{num}")
			html = page.inner_text("*")
			dct = loads(html)["data"]
			for attribute in ("tiers", "divisions"):
				json.setdefault(attribute, dct[attribute])
			json["data"].extend(dct["data"])

			logger.debug(f"Scraping from: https://rocketleague.tracker.network/rocket-league/distribution?playlist={num}")

			page.goto(f"https://rocketleague.tracker.network/rocket-league/distribution?playlist={num}")
			itms = page.locator("li.dropdown__item")
			for itm in itms.all():
				if itm.inner_text() == name:
					itm.click(force=True)
					break

			pop_loc = page.locator("div.description").inner_text()

			match = search(r": Find out the percentage of tracked players by tier in the latest season and learn the true value of your skill\. We are currently tracking ([\d,]+) players for the chosen playlist\.", pop_loc)
			if match is None:
				raise ValueError(f"Could not scrape the total population for: {name}")
			json["population"].append({
				"tier": num,
				"population": match.group(1).replace(',', '')
			})

			logger.info(f"Playlist: \"{name}\" finished.")

	json["playlists"] = playlists

	with open(output_file, 'w') as f:
		f.writelines(dumps({"info": json}))


if __name__ == "__main__":
	scrape_skill_distributions("extra/current_season.json", verbose=True, headless=True)
