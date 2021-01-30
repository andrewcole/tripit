from os.path import abspath, dirname, join

from setuptools import find_packages, setup


def get_long_description():
    with open(
        join(dirname(abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="tripit-to-sqlite",
    version="0.0.1",
    author="Andrew Cole",
    author_email="andrew.cole@illallangi.com",
    description="Create a SQLite database containing your flight history from Tripit",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/illallangi/tripit-to-sqlite",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["tripit-to-sqlite=illallangi.tripitsqlite.__main__:cli"],
    },
    project_urls={
        "Issues": "https://github.com/illallangi/tripit-to-sqlite/issues",
        "CI": "https://github.com/illallangi/tripit-to-sqlite/actions",
        "Changelog": "https://github.com/illallangi/tripit-to-sqlite/releases",
    },
    license="MIT License",
    install_requires=[
        "click",
        "diskcache",
        "loguru",
        "peewee",
        "requests",
        "requests_oauthlib",
        "tqdm",
        "yarl",
    ],
)
