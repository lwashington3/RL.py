from pytz import timezone


__all__ = ["get_timezone"]


def get_timezone(abbreviation:str) -> timezone:
	return {
		"CST": timezone("US/Central"),
		"CDT": timezone("US/Central"),
		"EST": timezone("US/Eastern"),
		"EDT": timezone("US/Eastern"),
		"PST": timezone("US/Pacific"),
		"PDT": timezone("US/Pacific"),
		"MST": timezone("US/Mountain"),
		"MDT": timezone("US/Mountain"),
	}.get(abbreviation, None)
