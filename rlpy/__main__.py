from argparse import ArgumentParser
from os import getenv
from .sync_api import User
from ._enum_classes import *


def _add_common_options(parser):
	pass


def _create_user_parser(parser_factory):
	parser = parser_factory("user", help="Collecting data from a specific user")
	_add_common_options(parser)
	parser.add_argument("-u", "--user", help="The user you want to collect data for")
	parser.add_argument("-c", "--console", help="The console type the user data belongs to.")
	return parser


def _create_playvs_parser(parser_factory):
	parser = parser_factory("playvs", help="Getting team information from PlayVS")
	_add_common_options(parser)
	parser.add_argument("-l", "--link", help="The link to the match website")
	parser.add_argument("-i", "--id", help="The id of the website")
	return parser


def create_argument_parser():
	parser = ArgumentParser(prog="Rocket League Bot")
	subparsers = parser.add_subparsers()
	subparsers.dest = 'command'
	subparsers.required = False
	_create_user_parser(subparsers.add_parser)
	_create_playvs_parser(subparsers.add_parser)
	return parser


def main():
	try:
		parser = create_argument_parser()
		arguments = parser.parse_args()
		if arguments.command == "user":
			user = arguments.user
			console = convert_str_to_console(arguments.console)
			print(User(user,console).get_data())
		elif arguments.command == "playvs":
			pass
		else:
			print(User(getenv("user_name"), convert_str_to_console(getenv("console"))).get_data())
	except ValueError as e:
		print(repr(e))


if __name__ == "__main__":
	main()
