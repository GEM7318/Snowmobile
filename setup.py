import pathlib
import subprocess

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


version_str = (
    str((subprocess.check_output(["git", "describe"]).strip()))
    .split("-")[0]
    .replace("'", "")
    .replace("b", "")
)

# This call to setup() does all the work
setup(
    name="snowmobile",
    version=version_str,
    description="A simple set of modules for streamlined interaction with the Snowflake Database",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GEM7318/Snowmobile",
    author="Grant Murray",
    author_email="gmurray203@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    # packages=["snowmobile"],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "pandas",
        "snowflake-connector-python",
        "sqlparse",
        "fcache",
        "ipython",
    ],
    entry_points={"console_scripts": ["snowmobile=snowmobile.__main__:main"]},
)
