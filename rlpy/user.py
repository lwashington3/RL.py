from ._enum_classes import *
from ._exceptions import *
from .user_playlist import UserPlaylist
from logging import getLogger
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from playwright.sync_api import Page as SyncPage
from playwright.async_api import Page as ASyncPage


class BaseUser(ABC):
	SIMPLE_USER_REGEX = r"[a-zA-Z\d_.\[\]$^&*()<>%+]+"
	COMPLEX_USER_REGEX = r"[a-zA-Z\d_. \[\]$^&*()<>%+]+"

	def __init__(self, user_name:str, console:Console, **kwargs):
		self.username = user_name
		self.console = console

		self.player_name = kwargs.get("player_name", None)
		self.wins = 0
		self.goals = 0
		self.shots = 0
		self.assists = 0
		self.saves = 0
		self.mvps = 0
		self.trn_score = 0
		self.reward_level = ""
		self._playlists = {i:None for i in Playlist.PLAYLISTS}

	def __getitem__(self, item):
		if isinstance(item, Playlist):
			return self._playlists[item]
		else:
			return self.__getattribute__(item)

	def __str__(self) -> str:
		return f"{self.player_name} on {self.console}"

	def __repr__(self) -> str:
		return f"rlpy.User(username={self.username}, player_name={self.player_name}, console={self.console})"

	def __eq__(self, other):
		if not isinstance(other, BaseUser):
			return False
		return self.player_name == other.player_name and self.console == other.console

	@abstractmethod
	def get_data(self, page: SyncPage | ASyncPage = None, get_player_name=False, wait_for_update=True,
									close_page_on_finish=False, **kwargs) -> "BaseUser":
		"""

		:param page:
		:param bool get_player_name: If the program should scrape the display name from RLStats.
		:param bool wait_for_update: If the program should wait for the web page to reload or if the data should be taken immediately.
		:param bool close_page_on_finish: If the page object should be closed as soon as it is no longer required,
		regardless of if it was passed as an argument or created in the method.
		:return: This User object, for chaining
		:raises UserScrapeError: If an error occurs during scraping information for the player.
		"""
		if self.console == Console.SWITCH:
			raise UserScrapeError(f"RLStats cannot support some features, including stats for Switch players.")

	def _process_data(self, soup:BeautifulSoup, get_player_name=False, **kwargs) -> "BaseUser":
		"""

		:param soup:
		:param get_player_name:
		:return:
		:raises rlpy.UserScrapeError: If there is an error when the scrape occurs.
		"""
		from re import compile

		logger = kwargs.get("logger", getLogger(__name__))
		logger.info("Processing User data retrieved from web.", extra=self.log_extra)
		error_message = soup.select("div.error-message")
		if len(error_message) != 0:
			raise UserScrapeError(f"The website: {self.link} had an error and could not be loaded. Error message: \"{error_message}\".")

		if get_player_name:
			try:
				match = search(r"\n*([\w -]+) Updated (\d+) minutes ago[Fancy|Compact] Version", soup.select_one("section#userinfo").text)
			except AttributeError:
				logger.exception("Could not find player name in website.", extra=self.log_extra)

		# region Collect Lifetime Stats
		lifetime_stat_conversion = {
			"Wins": "wins",
			"Goals": "goals",
			"Shots": "shots",
			"Assists": "assists",
			"Saves": "saves",
			"MVPs": "mvps",
		}
		lifetime_stats = soup.select_one("div.block-stats").select("td")
		stat_regex = compile(r"([\d,]+)\s(\w+)")
		for stat in lifetime_stats:
			match = stat_regex.search(stat.text)
			if match is None:
				logger.error(f"Could not match regex for {stat.text}.", extra=self.log_extra)
				continue

			value = int(match.group(1).replace(",", "_"))
			name = match.group(2)
			setattr(self, lifetime_stat_conversion[name], value)

		del lifetime_stats, lifetime_stat_conversion
		logger.debug("Lifetime stats collected.",
					 extra=self.log_extra)
		# endregion

		# region Collect Reward Level
		reward_level = soup.select_one("div.fullwidth", text=compile(r"([\w ]+)\s*\n?\s*Season Reward Level"))
		reward_level = reward_level.find("h2").text.strip()
		if reward_level == "Unranked":
			reward_level = None
		self.reward_level = reward_level
		logger.debug("Reward level collected.",extra=self.log_extra)
		# endregion

		# region Collect Playlist Data
		region = soup.select_one("div.block-skills")
		tables = region.select("table")
		match_regex = compile(r"Matches Played:\s([\d,]+)")
		streak_regex = compile(r"(Win|Loss) Streak:\s([\d,]+)")
		mmr_regex = compile(r"(~\d+)? ?([\d,]+) ?(~\d+)?")
		casual_regex = compile(r"Rating ([\d,]+)")
		playlists = []
		for table_num, table in enumerate(tables):
			if table_num == 2:
				for row in table.select("tr"):
					match = casual_regex.search(row.text)
					if match is None:
						continue
					playlist = UserPlaylist.from_text("Casual", "Unranked", "Division I", int(match.group(1).replace(',', '_')), None, None)
					self._playlists[playlist.playlist.name] = playlist
					break
				break

			cells = [[], [], [], []]
			for i, row in enumerate(table.select("tr")):
				if i == 4:
					continue
				elif i == 0:
					values = row.find_all("th")
				else:
					values = row.find_all("td")
				if len(values) != 4:
					logger.error(f"There are not the correct amount of items in the user's playlist tables. Table: {table_num}. Row: {i}. Cells: {len(values)}",
								 extra=self.log_extra)

				for lst, value in zip(cells, values):
					lst.append(value.text)
			playlists.extend(cells)

		for lst in playlists:
			playlist, rank, division, mmr, matches_played, streak = lst

			mmr = mmr_regex.search(mmr)
			if mmr is None:
				logger.error("The MMR could not be properly extracted.", extra=self.log_extra)
				continue

			if len(mmr.groups()) == 3:
				mmr = mmr.group(2)
			elif len(mmr.groups()) == 1:
				mmr = mmr.group(1)
			else:
				logger.debug(f"An unknown number of groups was found trying to scrape the MMR.", extra=self.log_extra)

			match = match_regex.search(matches_played)
			if match is None:
				logger.error("Could not match the number of matches played.", extra=self.log_extra)
				continue

			matches_played = match.group(1)

			streak = streak_regex.search(streak)
			if streak is None:
				logger.error("Could not pull the match streak.", extra=self.log_extra)
				continue
			streak = int(streak.group(2)) * (1 if streak.group(1) == "Win" else -1)

			playlist = UserPlaylist.from_text(playlist, rank, division, mmr, streak, matches_played)
			self._playlists[playlist.playlist.name] = playlist

		logger.debug("Playlist data collected.", extra=self.log_extra)
		# endregion

		logger.debug(f"Finished scraping user info from {self.link}.", extra=self.log_extra)
		return self

	def get_playlist(self, playlist:str | Playlist) -> UserPlaylist:
		"""

		:param str | rlpy.Playlist playlist:
		:return:
		:rtype: rlpy.UserPlaylist
		:raises rlpy.PlaylistNotFoundError: If no playlist with the given name or playlist type is found.
		"""
		if not isinstance(playlist, (str,Playlist)):
			raise ValueError(f"Playlist must be a rlpy.Playlist object or the string name of the playlist, not {type(playlist).__name__}")
		if isinstance(playlist, str):
			for name, _playlist in self._playlists.items():
				if _playlist is None:
					continue
				if name == playlist or _playlist.playlist == playlist or _playlist.playlist.name == playlist:
					return _playlist
		else:
			for name, _playlist in self._playlists.items():
				if _playlist is None:
					getLogger(__name__).error(f"The playlist value for: `{name}` did not have it's data collected. Check why.",
											  extra=self.log_extra)
					continue
				if playlist == _playlist or _playlist.playlist == playlist or _playlist.playlist.name == playlist.name:
					return _playlist
		raise PlaylistNotFoundError(f"Could not find playlist: {playlist} for RL user {self.username}.", playlist_name=playlist.name if isinstance(playlist, Playlist) else playlist)

	# region User Properties
	@property
	def log_extra(self) -> dict[str, "Any"]:
		"""
		A dictionary of values that might be useful in logging.
		:return:
		"""
		return {"player_name": self.player_name, "console": self.console, "username": self.username}

	@property
	def username(self) -> str:
		"""The user's defined username, which is tied to their account. This is the username that displays RLStats data. Should not be changed."""
		return self._user_name

	@username.setter
	def username(self, value):
		self._user_name = value

	@username.deleter
	def username(self):
		raise ValueError("Cannot delete username from User object")

	@property
	def player_name(self) -> str:
		"""The user's chosen name, nickname, or screen name. May be changed at will without changing data sources."""
		if self._player_name is None:
			return self._user_name
		return self._player_name

	@player_name.setter
	def player_name(self, player_name:str | None):
		if not isinstance(player_name, str | None):
			player_name = str(player_name)
		self._player_name = player_name

	@player_name.deleter
	def player_name(self):
		if self.console == Console.STEAM:
			raise ValueError("Steam players must have a player name.")
		self.player_name = None

	@property
	def link_name(self) -> str:
		return self.username.replace(' ', '%20')

	@property
	def link(self) -> str:
		"""The link for the user's RLStats page."""
		return f"https://rlstats.net/profile/{self.console.value}/{self.link_name}"

	@link.setter
	def link(self, value):
		raise ValueError("Cannot change the link directly, change the username or the console to change the link")

	@link.deleter
	def link(self):
		raise ValueError("Cannot delete the link from User object")

	@property
	def console(self) -> Console:
		return self._console_type

	@console.setter
	def console(self, console:Console | str):
		if isinstance(console, str):
			console = convert_str_to_console(console)
		if not isinstance(console, Console):
			raise ValueError(f"Value of console must be of enum `rlpy.Console`. Not {type(console).__name__}.")
		self._console_type = console

	@console.deleter
	def console(self):
		raise ValueError("Cannot delete the console object from User object")

	@property
	def wins(self) -> int | None:
		return self._wins

	@wins.setter
	def wins(self, wins: int | None):
		if not isinstance(wins, int | None):
			wins = int(wins)
		self._wins = wins

	@wins.deleter
	def wins(self):
		self._wins = None

	@property
	def goals(self) -> int | None:
		return self._goals

	@goals.setter
	def goals(self, goals:int | None):
		if not isinstance(goals, int | None):
			goals = int(goals)
		self._goals = goals

	@goals.deleter
	def goals(self):
		self._goals = None

	@property
	def shots(self) -> int | None:
		return self._shots

	@shots.setter
	def shots(self, shots: int | None):
		if not isinstance(shots, int | None):
			shots = int(shots)
		self._shots = shots

	@shots.deleter
	def shots(self):
		self._shots = None

	@property
	def goal_shot_ratio(self) -> float:
		if not self.shots:
			return self.goals
		else:
			return self.goals / self.shots

	@property
	def saves(self) -> int | None:
		return self._saves

	@saves.setter
	def saves(self, saves: int | None):
		if not isinstance(saves, int | None):
			saves = int(saves)
		self._saves = saves

	@saves.deleter
	def saves(self):
		self._saves = 0

	@property
	def mvps(self) -> int:
		return self._mvps

	@mvps.setter
	def mvps(self, mvps):
		if mvps is None:
			mvps = 0
		if not isinstance(mvps, int):
			mvps = int(mvps)
		self._mvps = mvps

	@mvps.deleter
	def mvps(self):
		self._mvps = 0

	@property
	def trn_score(self) -> float:
		return self._trn_score

	@trn_score.setter
	def trn_score(self, trn_score):
		if trn_score is None:
			trn_score = 0
		if not isinstance(trn_score, float):
			trn_score = float(trn_score)
		self._trn_score = trn_score

	@trn_score.deleter
	def trn_score(self):
		self._trn_score = 0

	# endregion

	@classmethod
	def from_link(cls, link:str, **kwargs):
		from re import search, I
		match = search(f"https://rlstats.net/profile/(Epic|Steam|Xbox|PS4|switch)/({cls.SIMPLE_USER_REGEX})", link, I)
		if match is None:
			raise PlayerNotFoundError("This link does not match the convention for RLStats links, please try again.")
		console = convert_str_to_console(match.group(1))
		username = match.group(2).replace("%20", " ")
		if console == Console.SWITCH:
			from warnings import warn
			warn("RLStats does not have the ability to scrape data for Switch users.")
		return cls(username, console, **kwargs)
