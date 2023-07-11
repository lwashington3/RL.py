from setuptools import setup, find_packages


with open("README.md", 'r') as f:
	long_description = f.read()


project_name = "rlpy"
git_url = "https://github.com/lwashington3/RL.py"


setup(
	name=project_name,
	version="2.0.0",
	author="Len Washington III",
	description="Rocket League Data Scraper",
	include_package_data=True,
	long_description=long_description,
	long_description_content_type="test/markdown",
	url=git_url,
	project_urls={
		"Bug Tracker": f"{git_url}/issues"
	},
	license="MIT",
	packages=find_packages(),
	install_requires=[
		"beautifulsoup4", "playwright >= 1.3.0", "tabulate", "pytz"
	],
	entry_points={
		"console_scripts": [f"{project_name}={project_name}.__main__:main"]
	},
	classifiers=[
		"Programming Language :: Python :: 3.10"
	]
)
