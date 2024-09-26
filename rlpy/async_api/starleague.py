from .._enum_classes import Console, Playlist
from .._exceptions import UserScrapeError
from ..match import RLTeam, StarLeague
from ..tools import get_timezone
from .user import User
import logging
from playwright.async_api import Locator, Page, expect, async_playwright, TimeoutError
from pytz import timezone


__all__ = ["nace_starleague_login", "create_team", "team_next_match"]


async def nace_starleague_login(page:Page, username:str, password:str):
	await page.goto("https://nsl.leaguespot.gg/login/")
	await page.locator("input#username").type(username)
	await page.locator("input#password").type(password)
	await page.locator("button.login-button.button.button--primary.button--wide.button--round").click(force=True)
	await page.wait_for_url("https://nsl.leaguespot.gg/")


async def create_team(locator:Locator, name:str, info_page:Page) -> RLTeam:
	team = RLTeam(name)
	users = locator.locator("li.match-user")
	
	for team_li in await users.all():
		handles = team_li.locator("div.match-user__handle")
		for div_handle in await handles.all():
			verified = await div_handle.get_by_alt_text("Verified").count() == 1
			if not verified:
				continue

			try:
				user = User(await div_handle.locator("span").inner_text(), Console.EPIC_GAMES)
				await user.get_data(page=info_page)
			except UserScrapeError:
				logging.getLogger(__name__).exception(f"An error occurred when scraping information for `{user.player_name}` on `{user.console}`")
				continue

			if await team_li.locator("div.avatar.small.avatar__role--captain").count():
				team.captain = user
			else:
				team.append(user)

	return team


async def team_next_match(page:Page, team_id:str, info_page, match_index=0, **kwargs) -> None | StarLeague:
	"""
	Gets information about the next match for a Rocket League team participating in a NACE StarLeague season.

	:param page:
	:param str team_id: The team's id. This is the hexadecimal numbers after `https://nsl.leaguespot.gg/teams/`
	:param info_page:
	:param int match_index: The index of the match on the team's page.
	:return: An rlpy.StarLeague object representing the match, or None if there are no foreseeable matches.
	:raises TimeoutError: If there is a timeout error within playwright.
	:raises ValueError: If the match index is higher than the amount of remaining matches.
	"""
	from datetime import datetime as dt

	await page.goto(f"https://nsl.leaguespot.gg/teams/{team_id}")
	await page.wait_for_timeout(2000)
	try:
		upcoming = page.locator("div.team-match-schedule").first
		matches = upcoming.locator("a.match-schedule__match__stage-time")
		count = await matches.count()
		if count == 0:
			return
		if match_index >= count:
			raise ValueError(f"The match index {match_index} was out of bounds of the elements {count} for team {team_id}.")
		next_match_url = await matches.nth(match_index).get_attribute("href")
	except TimeoutError as e:
		raise TimeoutError(f"A timeout error occurred on page: {page.url}. Exception ({e}).")

	await page.goto(f"https://nsl.leaguespot.gg{next_match_url}")
	datetime_info = page.locator("div.match-page__text-container--top")
	time = await page.locator("p.match-page__text.match-page__text--time").inner_text()
	date = await datetime_info.locator("p.match-page__text").last.inner_text()

	tz = get_timezone(time[-3:])
	date = dt.strptime(f"{date} {time}"[:-4], "%b %d, %Y %I:%M %p").replace(tzinfo=tz)
	now = dt.now(tz=tz)

	if (date - now).total_seconds() < 0:  # The first match listed has already past means that there are no new matches
		return

	try:
		teams = page.locator("div.match-page__match-participant")
		names = page.locator("a.head-to-head__label")
	except TimeoutError as e:
		raise TimeoutError(f"A timeout error occurred on page: {page.url}. Exception ({e})")

	return StarLeague(home_team=await create_team(teams.first, await names.first.inner_text(), info_page),
						away_team=await create_team(teams.last, await names.last.inner_text(), info_page),
					  	date=date)
