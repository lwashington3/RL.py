__all__ = ["PlayerNotFoundError", "ConsoleNotFoundError", "RankNotFoundError", "MMROutOfBoundError", "PlaylistNotFoundError", "UserScrapeError"]


class PlayerNotFoundError(BaseException):
    pass


class ConsoleNotFoundError(BaseException):
    pass


class RankNotFoundError(BaseException):
    pass


class MMROutOfBoundError(BaseException):
    pass


class PlaylistNotFoundError(BaseException):
    def __init__(self, *args, playlist_name=None):
        super().__init__(*args)
        self.playlist_name = playlist_name


class UserScrapeError(BaseException):
    pass
