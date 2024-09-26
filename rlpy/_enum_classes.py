from ._exceptions import *
from enum import Enum as IntEnum, Enum as StrEnum
from re import match, I
from warnings import warn


__all__ = ["PlaylistNumber", "Console", "convert_str_to_console", "Division", "Rank", "Playlist", "PlayListNames",
			"UnrankedDivision", "Unranked", "UnrankedPlaylist"]


class PlaylistNumber(IntEnum):
	RANKED_DUEL = 10
	RANKED_DOUBLES = 11
	RANKED_STANDARD = 13
	HOOPS = 27
	RUMBLE = 28
	DROPSHOT = 29
	SNOW_DAY = 30
	TOURNAMENT_MATCHES = 34
	UNRANKED = 0


class Console(StrEnum):
	EPIC_GAMES = "Epic"
	STEAM = "Steam"
	XBOX = "Xbox"
	PLAY_STATION = "PS4"
	SWITCH = "switch"

	@classmethod
	def from_string(cls, string:str) -> "Console":
		"""
		Converts a string to the proper rlpy.Console value.

		:param str string:
		:return:
		:rtype rlpy.Console:
		:raises ConsoleNotFoundError: If the string is malformed or cannot be matched to a value.
		"""
		converted_string = string.upper().replace(" ", "_")

		for console in cls:
			if match(f"^{console.value}$", string, I) is not None or match(f"^{console.name}$", converted_string, I) is not None:
				return console

		if match("^PS[L4n]?$", string, I) is not None:
			return cls.PLAY_STATION

		if match("^epic$", string, I) is not None:
			return cls.EPIC_GAMES

		raise ConsoleNotFoundError(f"Cannot find console type: {string}")


def convert_str_to_console(string:str) -> Console:
	warn("convert_str_to_console is deprecated, use Console.from_string() instead.", DeprecationWarning, stacklevel=2)
	return Console.from_string(string)


class Division(object):
	def __init__(self, name:str, lower_bound:int, upper_bound:int):
		self.name = name
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound

	# region Division Properties

	@property
	def name(self) -> str:
		return self._name

	@name.setter
	def name(self, name:str):
		if not isinstance(name, str):
			name = str(name)
		self._name = name

	@property
	def lower_bound(self) -> int:
		return self._lower_bound

	@lower_bound.setter
	def lower_bound(self, lower_bound:int):
		if not isinstance(lower_bound, int):
			lower_bound = int(lower_bound)
		self._lower_bound = lower_bound

	@property
	def upper_bound(self) -> int:
		return self._upper_bound

	@upper_bound.setter
	def upper_bound(self, upper_bound: int):
		if not isinstance(upper_bound, int):
			upper_bound = int(upper_bound)
		self._upper_bound = upper_bound

	# endregion

	def __repr__(self) -> str:
		return f"Division(name={self.name}, bounds=({self.lower_bound}, {self.upper_bound}))"


class Rank(object):
	def __init__(self, name:str, players:int, player_percentage:float = None, **kwargs):
		self.name = name
		self.players = players
		self.player_percentage = player_percentage
		self.division_1 = kwargs.get("division_1", None)
		self.division_2 = kwargs.get("division_2", None)
		self.division_3 = kwargs.get("division_3", None)
		self.division_4 = kwargs.get("division_4", None)

	# region Rank Properties

	@property
	def name(self) -> str:
		return self._name

	@name.setter
	def name(self, name):
		if not isinstance(name, str):
			name = str(name)
		self._name = name

	@property
	def players(self) -> int:
		return self._players

	@players.setter
	def players(self, players):
		if not isinstance(players, int):
			players = int(players)
		self._players = players

	@property
	def player_percentage(self) -> float:
		return self._player_percentage

	@player_percentage.setter
	def player_percentage(self, player_percentage):
		if not isinstance(player_percentage, float):
			player_percentage = float(player_percentage)
		self._player_percentage = player_percentage

	@property
	def division_1(self):
		return self._div_1

	@division_1.setter
	def division_1(self, div:(Division, None)):
		if not isinstance(div, Division | None):
			raise ValueError(f"rlpy.Playlist.division_1 property must be of type rlpy.Division or None, not {type(div).__name__}")
		self._div_1 = div

	@property
	def division_2(self):
		return self._div_2

	@division_2.setter
	def division_2(self, div: (Division, None)):
		if not isinstance(div, Division | None):
			raise ValueError(f"rlpy.Playlist.division_2 property must be of type rlpy.Division or None, not {type(div).__name__}")
		self._div_2 = div

	@property
	def division_3(self):
		return self._div_3

	@division_3.setter
	def division_3(self, div: (Division, None)):
		if not isinstance(div, Division | None):
			raise ValueError(f"rlpy.Playlist.division_3 property must be of type rlpy.Division or None, not {type(div).__name__}")
		self._div_3 = div

	@property
	def division_4(self):
		return self._div_4

	@division_4.setter
	def division_4(self, div: (Division, None)):
		if not isinstance(div, Division | None):
			raise ValueError(f"rlpy.Playlist.division_4 property must be of type rlpy.Division or None, not {type(div).__name__}")
		self._div_4 = div

	# endregion

	def __repr__(self):
		return f"Rank(name={self.name}, players={self.players:,}, player_percentage={self.player_percentage})"

	def get_division(self, mmr:int, default_div:int=None) -> Division:
		"""
		Returns the Division within this rank
		:param int mmr: The Match-Making Rating (MMR) of the user
		:return:
		:raise: MMROutOfBoundError: The mmr would not be ranked in this rank.
		"""
		for div in (self.division_1, self.division_2, self.division_3, self.division_4):
			if div is not None:
				if div.lower_bound <= mmr <= div.upper_bound:
					return div
		if self.division_1 is not None:
			if 0 <= self.division_1.lower_bound - mmr <= 15:
				return self.division_1
		if self.division_4 is not None:
			if 0 <= mmr - self.division_4.upper_bound <= 15:
				return self.division_4
		if default_div is not None:
			div = getattr(self, f"division_{default_div}", None)
			if div is not None:
				return div
		raise MMROutOfBoundError(f"The MMR: {mmr} is not found in {self.name}.")


class Playlist(object):
	PLAYLISTS = {}

	def __init__(self, name:str, **kwargs):
		self.name = name
		self.ranks = kwargs

	def __repr__(self):
		return f"{self.name}"

	def add_rank(self, rank:Rank):
		self.ranks[rank.name] = rank

	def get_rank(self, rank_name:str) -> Rank:
		"""
		Finds the rank object related to the given rank name. For Champion and Grand Champion, ranks can be found using C1, GC2, etc...
		:param rank_name: The name of the rank
		:return: The rank object
		:raises: RankNotFoundError
		"""
		rank_name = rank_name.replace("3", "III").replace("2", "II").replace("1", "I")
		lowered = rank_name.strip().lower().replace("gc", "grand champion")
		for key in self.ranks.keys():
			if lowered == key.lower():
				return self.ranks[key]
		if lowered.startswith("c"):
			lowered = lowered.replace("c", "champion")
			for key in self.ranks.keys():
				if lowered == key.lower():
					return self.ranks[key]
		if rank_name == "Unranked":
			rank = Unranked()
			self.ranks[rank_name] = rank
			return rank
		raise RankNotFoundError(f"The rank \"{repr(rank_name)}\" could not be found in {self.name}")

	@staticmethod
	def load_data(file_path=None):  # Unranked isn't in here
		from json import load
		if file_path is None:
			from os.path import join, dirname, realpath
			file_path = join(dirname(realpath(__file__)), "extra/current_season.json")
		with open(file_path, ) as f:  # No mode given on purpose
			data = load(f)["info"]
		Playlist.PLAYLISTS["Un-Ranked"] = UnrankedPlaylist("Un-Ranked")
		ranks = {}
		for row in data["data"]:
			div = Division(data['divisions'][row['division']], row["minMMR"], row["maxMMR"])

			rank = ranks.get((row["playlist"], row["tier"]), None)
			if rank is None:
				rank = Rank(data["tiers"][row["tier"]], 0, 0)
				ranks[(row["playlist"], row["tier"])] = rank

			match row["division"]:
				case 0:
					rank.division_1 = div
				case 1:
					rank.division_2 = div
				case 2:
					rank.division_3 = div
				case 3:
					rank.division_4 = div
				case _:
					raise RankNotFoundError(f"There is no division numbered {row['division']}.")

			playlist = Playlist.PLAYLISTS.get(data["playlists"][str(row["playlist"])], None)
			if playlist is None:
				playlist = Playlist(name=data["playlists"][str(row["playlist"])])
				Playlist.PLAYLISTS[playlist.name] = playlist

			playlist.add_rank(rank)
		return Playlist.PLAYLISTS


# region Unranked classes
class UnrankedDivision(Division):
	def __init__(self):
		super().__init__("Division I", -1, -1)
		self._upper_bound = self._lower_bound = None


class Unranked(Rank):
	def __init__(self, **kwargs):
		super().__init__("Un-Ranked", 0, 0)
		self.division_1 = UnrankedDivision()

	def get_division(self, mmr:int, **kwargs) -> Division:
		return self.division_1


class UnrankedPlaylist(Playlist):
	def get_rank(self, rank_name:str) -> Rank:
		return Unranked()
# endregion


Playlist.load_data()


class PlayListNames(StrEnum):
	Un_Ranked = "Un-Ranked"
	Ranked_Duel = "Ranked Duel 1v1"
	Ranked_Doubles = "Ranked Doubles 2v2"
	Ranked_Standard = "Ranked Standard 3v3"

	Hoops = "Hoops"
	Rumble = "Rumble"
	Dropshot = "Dropshot"
	Snowday = "Snowday"

	Tournament_Matches = "Tournament Matches"
