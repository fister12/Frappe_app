from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ai_quality_checker/__init__.py
from ai_quality_checker import __version__ as version

setup(
	name="ai_quality_checker",
	version=version,
	description="An app to integrate AI vision models for automated quality assurance in ERPNext",
	author="Your Name",
	author_email="your.email@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
