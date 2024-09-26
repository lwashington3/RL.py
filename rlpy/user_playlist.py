from ._enum_classes import Playlist, Division, Rank
from ._exceptions import RankNotFoundError, PlaylistNotFoundError


__all__ = ["UserPlaylist"]


def format_none(value) -> str | None:
	return None if value is None else f"{value:,}"


class UserPlaylist(object):
	def __init__(self, playlist:Playlist, rank:Rank, division:Division, mmr:int, streak:int, matches_played:int):
		self.playlist = playlist
		self.rank = rank
		self.division = division
		self.streak = streak
		self.mmr = mmr
		self.matches_played = matches_played

	@property
	def playlist(self) -> Playlist:
		"""The playlist enumeration to help keep things organized."""
		return self._playlist

	@playlist.setter
	def playlist(self, playlist:Playlist):
		if not isinstance(playlist, Playlist):
			raise ValueError(f"playlist variable: {playlist} must be a rlpy.Playlist object, not {type(playlist).__name__}")
		self._playlist = playlist

	@property
	def rank(self) -> Rank:
		"""The rank enumeration to help keep things organized."""
		return self._rank

	@rank.setter
	def rank(self, rank:Rank):
		if not isinstance(rank, Rank):
			raise ValueError(f"rank variable: {rank} is not of enumerated type Rank")
		self._rank = rank

	@property
	def division(self) -> Division:
		return self._division

	@division.setter
	def division(self, division:Division):
		"""The division enumeration to help keep things organized."""
		if not isinstance(division, Division):
			raise ValueError(f"division variable: {division} is not of enumerated type Divisions")
		self._division = division

	@property
	def mmr(self) -> int:
		"""The Match Making Rank (MMR) for the specified playlist."""
		return self._mmr

	@mmr.setter
	def mmr(self, mmr:int):
		if not isinstance(mmr, int):
			mmr = int(mmr)
		self._mmr = mmr

	@property
	def streak(self) -> int | None:
		"""
		The win/lose streak in this playlist. A positive number indicates a win streak, negative indicates a loss streak.
		"""
		return self._streak

	@streak.setter
	def streak(self, streak:int | None):
		if not isinstance(streak, int | None):
			streak = int(streak)
		self._streak = streak

	@property
	def matches_played(self) -> int | None:
		"""
		The number of matches played for a playlist.
		"""
		return self._matches_played

	@matches_played.setter
	def matches_played(self, matches_played:int | None):
		if not isinstance(matches_played, int | None):
			matches_played = int(matches_played)
		self._matches_played = matches_played

	def __eq__(self, other):
		if not isinstance(other, UserPlaylist):
			return False
		return (self.playlist == other.playlist) and (self.rank == other.rank) and (self.division == other.division) and (self.streak == other.streak) and (self.mmr == other.mmr) and (self.matches_played == other.matches_played)

	def __ne__(self, other):
		return not (self == other)

	def __str__(self) -> str:
		return f"PlayList: {self.playlist.name}\nRank: {self.rank.name} {self.division.name}\nMMR: {self.mmr:,}\nMatches Played: {self.matches_played:,}\nStreak: {format_none(self.streak)}"

	def __repr__(self):
		return f"Playlist({self.playlist.name}, Rank={self.rank.name}, Division={self.division.name}, MMR={format_none(self.mmr)}, Matches Played={format_none(self.matches_played)}, Streak={format_none(self.streak)})"

	@classmethod
	def from_text(cls, playlist:str, rank:str, division:str, mmr:str | int, streak:str | int | None, matches_played: int | None):
		from re import search, match
		# region Parse Playlist object
		playlist_dct = {
			"Casual": "Un-Ranked",
			"1v1( Solo)? Duel": "Ranked Duel 1v1",
			"2v2 Doubles": "Ranked Doubles 2v2",
			"3v3 Standard": "Ranked Standard 3v3",
			"(3v3 )?Tournaments?": "Tournament Matches",
			"2v2 Hoops": "Hoops",
			"3v3 Rumble": "Rumble",
			"3v3 Dropshot": "Dropshot",
			"3v3 Snow Day": "Snowday"
		}#.get(playlist, playlist)

		playlist = playlist_dct.get(list(filter(lambda key: match(key, playlist), playlist_dct.keys()))[0], playlist)

		for name, _playlist in Playlist.PLAYLISTS.items():
			if name == playlist:
				playlist = _playlist
				break
		else:
			raise PlaylistNotFoundError(f"Playlist name: {playlist} could not be found in the given playlists.", playlist_name=playlist)
		# endregion

		if isinstance(mmr, str):
			mmr = int(mmr.removeprefix("#").replace(",", "_"))

		def roman_to_arabic(roman:str) -> int:
			roman = roman.strip().upper()
			if roman.isnumeric():
				return int(roman)
			match roman:
				case "I":
					return 1
				case "II":
					return 2
				case "III":
					return 3
				case "IV":
					return 4
				case _:
					raise ValueError(f"{roman} is not a numeral that can be matched.")

		match = search(r"Division ([IV1-4]+)", division)
		if match is None:
			raise ValueError(f"Could not get the data from the full rank: {division}")
		rank = playlist.get_rank(rank)
		division = rank.get_division(mmr, default_div=roman_to_arabic(match.group(1)))

		if isinstance(streak, str):
			try:
				streak = int(streak.replace(",", "_"))
			except ValueError:
				streak = None

		matches_played = None if matches_played == "N/A" or matches_played is None else int(matches_played)
		return cls(playlist, rank, division, mmr, streak, matches_played)
