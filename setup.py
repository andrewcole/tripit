from os.path import abspath, dirname, join

from setuptools import find_packages, setup


def get_long_description():
    with open(
        join(dirname(abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="",
    version="0.0.1",
    author="Andrew Cole",
    author_email="andrew.cole@illallangi.com",
    description="TODO: SET DESCRIPTION",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/illallangi/TripItAPI",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
    },
    project_urls={
        "Issues": "https://github.com/illallangi/TripItAPI/issues",
        "CI": "https://github.com/illallangi/TripItAPI/actions",
        "Changelog": "https://github.com/illallangi/TripItAPI/releases",
    },
    license="MIT License",
    install_requires=[
        "diskcache",
        "loguru",
        "requests",
        "requests_oauthlib",
        "yarl",
    ],
)
