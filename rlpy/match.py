from abc import ABC, abstractmethod
from tabulate import tabulate
from .user import BaseUser
from ._enum_classes import Playlist
from datetime import datetime
from pytz import timezone


__all__ = ["RLTeam", "Match", "StarLeague", "BaseUser"]


class RLTeam(list[BaseUser]):
	def __init__(self, name:str, *users, captain:BaseUser=None):
		super().__init__(users)
		self.teamname = name
		self.captain = captain

	def __str__(self) -> str:
		string = ""
		for player in self:
			string += f"{player.username}, {player.wins}, {player.trn_score}\n"
		return string

	def __repr__(self):
		string = ""
		for player in self:
			string += f"{player.username} | "
		return string.strip(" | ")

	@property
	def teamname(self) -> str:
		return self._team_name

	@teamname.setter
	def teamname(self, team_name:str):
		if not isinstance(team_name, str):
			team_name = str(team_name)
		self._team_name = team_name

	@property
	def captain(self) -> BaseUser | None:
		return self._captain

	@captain.setter
	def captain(self, captain: BaseUser | None):
		if not isinstance(captain, BaseUser | None) and not issubclass(captain.__class__, BaseUser):
			raise ValueError(f"The captain of a team must be a user, or None if there isn't a captain, not: {type(captain).__name__}")
		self._captain = captain
		if captain not in self and captain is not None:
			self.insert(0, captain)

	def is_captain(self, user:BaseUser) -> bool:
		return self.captain == user

	def append(self, __object: BaseUser) -> None:
		if not isinstance(__object, BaseUser):
			raise ValueError(f"Type {type(__object).__name__} cannot be added to list of Rocket League Users")
		super().append(__object)

	def insert(self, __index: int, __object: BaseUser) -> None:
		if not isinstance(__object, BaseUser):
			raise ValueError(f"Type {type(__object).__name__} cannot be added to list of Rocket League Users")
		super().insert(__index, __object)

	def average_mmr(self, __playlist: Playlist) -> float:
		if not isinstance(__playlist, PlayList):
			raise ValueError(f"The playlist must be a rlpy.Playlist object, not type {type(__playlist).__name__}.")
		average_mmr = 0
		for player in self:
			average_mmr += getattr(player, f"{__playlist.name.lower().replace(' ', '_')}").mmr
		return average_mmr / len(self)

	def __setitem__(self, key, value):
		if not isinstance(vale, RLTeam):
			raise ValueError(f"rlpy.RLTeam elements must be of type rlpy.User, not {type(value).__name__}")
		super().__setitem__(key, value)

	@staticmethod
	def _average(lis):
		return sum(lis) / len(lis)

	def abbreviatied_players_details_list(self, tablefmt="fancy_grid", **kwargs):
		data = []
		return tabulate(data, headers=("Player name"), tablefmt=tablefmt, **kwargs)

	def player_details_list(self, tablefmt="fancy_grid") -> str:
		data = [
			["User names:"] + [i.player_name for i in self] + ["Averages"],
			["Console:"] + [f"{i.console.name.replace('_', ' ').title()}" for i in self] + ["null"],
			["Wins:"] + [f"{i.wins:,}" for i in self] + [f"{self._average([i.wins for i in self]):,}"],
			["Goal Shot Ratio:"] + [str(i.goal_shot_ratio) for i in self] + [
				f"{self._average([i.goal_shot_ratio for i in self]):,}"],
			["Goals:"] + [f"{i.goals:,}" for i in self] + [f"{self._average([i.goals for i in self]):,}"],
			["Shots:"] + [f"{i.shots:,}" for i in self] + [f"{self._average([i.shots for i in self]):,}"],
			["Assists:"] + [f"{i.assists:,}" for i in self] + [f"{self._average([i.assists for i in self]):,}"],
			["Saves:"] + [f"{i.saves:,}" for i in self] + [f"{self._average([i.saves for i in self]):,}"],
			["MVPs:"] + [f"{i.mvps:,}" for i in self] + [f"{self._average([i.mvps for i in self]):,}"],
			["TRN Score:"] + [f"{i.trn_score:,}" for i in self] + [f"{self._average([i.trn_score for i in self]):,}"],

			["Un_Ranked"] + [i.un_ranked.mmr for i in self] + [f"{self._average([i.un_ranked.mmr for i in self]):,}"],
			["Ranked_Duel"] + [i.ranked_duel.mmr for i in self] + [
				f"{self._average([i.ranked_duel.mmr for i in self]):,}"],
			["Ranked_Doubles"] + [i.ranked_doubles.mmr for i in self] + [
				f"{self._average([i.ranked_doubles.mmr for i in self]):,}"],
			["Ranked_Standard"] + [i.ranked_standard.mmr for i in self] + [
				f"{self._average([i.ranked_standard.mmr for i in self]):,}"],
			["Ranked_Chaos"] + [i.ranked_chaos.mmr for i in self] + [
				f"{self._average([i.ranked_chaos.mmr for i in self]):,}"],
			["Hoops"] + [i.hoops.mmr for i in self] + [f"{self._average([i.hoops.mmr for i in self]):,}"],
			["Rumble"] + [i.rumble.mmr for i in self] + [f"{self._average([i.rumble.mmr for i in self]):,}"],
			["Dropshot"] + [i.dropshot.mmr for i in self] + [f"{self._average([i.dropshot.mmr for i in self]):,}"],
			["Snowday"] + [i.snowday.mmr for i in self] + [f"{self._average([i.snowday.mmr for i in self]):,}"],
			["Tournament_Matches"] + [i.tournament_matches.mmr for i in self] + [
				f"{self._average([i.tournament_matches.mmr for i in self]):,}"]
		]

		for row in data:
			if row[0] != "User names:" and row[0] != "Console:":  # and False not in [i==0 for i in row]:
				test = [float(str(i).replace(",", "")) for i in row[1:]]
				index = test.index(max(test)) + 1
				row[index] = str(row[index]) + " (Highest)"

		return tabulate(data, headers="firstrow", tablefmt=tablefmt)


class Match(ABC):
	def __init__(self, home_team: RLTeam, away_team: RLTeam):
		self.home_team = home_team
		self.away_team = away_team

	@property
	def home_team(self) -> RLTeam:
		return self._home_team

	@home_team.setter
	def home_team(self, team):
		if not isinstance(team, RLTeam):
			raise ValueError(f"Home team of an rlpy.Match must be of type \"rlpy.RLTeam\", not \"{type(team).__name__}\"")
		self._home_team = team

	@property
	def away_team(self) -> RLTeam:
		return self._away_team

	@away_team.setter
	def away_team(self, team):
		if not isinstance(team, RLTeam):
			raise ValueError(f"Away team of an rlpy.Match must be of type \"rlpy.RLTeam\", not \"{type(team).__name__}\"")
		self._away_team = team

	@abstractmethod
	def player_details_list(self, tablefmt="fancy_grid") -> str:
		pass


class StarLeague(Match):
	def __init__(self, home_team:RLTeam, away_team:RLTeam, **kwargs):
		super().__init__(home_team, away_team)
		self.date = kwargs.get("date", None)

	@property
	def date(self) -> datetime | None:
		return self._date

	@date.setter
	def date(self, date:datetime | None):
		if not isinstance(date, datetime) and date is not None:
			raise ValueError(f"The date attribute of an rlpy.StarLeague match must be a datetime object, not: {type(date).__name__}")
		self._date = date

	@date.deleter
	def date(self):
		self.date = None

	def player_details_list(self, headers=("Player", "Team Name", "Status", "3v3 Rank", "3v3 MMR"), tablefmt="fancy_grid", print_team_names=True) -> str:
		from tabulate import tabulate
		players = list(self._home_team)
		players.extend(self.away_team)
		if not len(players):
			return "Empty player list"

		data = [[user.player_name + ("*" if self.home_team.is_captain(user) else ""), self.home_team.teamname, "Home", f"{user.get_playlist(Playlist.PLAYLISTS['Ranked Standard 3v3']).rank.name} {user.get_playlist(Playlist.PLAYLISTS['Ranked Standard 3v3']).division.name}",
			  user.get_playlist(Playlist.PLAYLISTS['Ranked Standard 3v3']).mmr] for user in self.home_team]
		data.extend([[user.player_name + ("*" if self.away_team.is_captain(user) else ""), self.away_team.teamname, "Away", f"{user.get_playlist(Playlist.PLAYLISTS['Ranked Standard 3v3']).rank.name} {user.get_playlist(Playlist.PLAYLISTS['Ranked Standard 3v3']).division.name}",
			  user.get_playlist(Playlist.PLAYLISTS['Ranked Standard 3v3']).mmr] for user in self.away_team])

		data.sort(key=lambda x: -x[4])

		if not print_team_names:
			data = [[i[0]] + i[2:] for i in data]

		return tabulate(data, headers=headers, tablefmt=tablefmt)
