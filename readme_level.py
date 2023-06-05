"""Module that contains all the logic about the levelsystem."""
from os import getenv
from logging import error
from requests import post
from graphql_query import QUERY
from readme_data import ReadmeLevelData


class ReadmeLevel:
    """Class that contains all the logic about the levelsystem."""

    # static variables
    max_level: int = 99
    ep_to_next_level: int = 100
    current_ep: int = 0
    current_level: int = 1

    level_data: ReadmeLevelData = ReadmeLevelData(
        contribution_ep=20, project_ep=5, discussion_ep=10, star_ep=40, follower_ep=25)

    def __init__(self) -> None:
        pass

    def fetch_user_data(self) -> dict[str, int] | None:
        """Fetches the user data from github api"""

        if not getenv("INPUT_GITHUB_TOKEN"):
            raise TypeError("github token is not a string")

        auth_header = {"Authorization": "Bearer " +
                       getenv("INPUT_GITHUB_TOKEN")}
        response = post("https://api.github.com/graphql",
                        json={"query": QUERY}, headers=auth_header, timeout=2)

        if response.status_code == 200:
            response_data = response.json()

            user_data = (response_data["data"]["user"]
                         ["contributionsCollection"]["contributionCalendar"])

            user_data["totalFollowers"] = (response_data["data"]["user"]
                                           ["followers"]["totalCount"])

            return user_data

        error("request to github api failed")
        return None

    def calc_current_ep(self) -> int:
        """Calculates the current user experience points"""

        # get user stats
        user_stats: dict[str, int] = self.fetch_user_data()

        # calc the current experience points
        self.current_ep = (
            user_stats["totalContributions"] * self.level_data.contribution_ep +
            user_stats["totalFollowers"] * self.level_data.follower_ep)

        return self.current_ep

    @property
    def get_contribution_ep(self) -> int:
        """gets the contribution ep"""
        return self.level_data.contribution_ep

    @property
    def get_follower_ep(self) -> int:
        """gets the follower ep"""
        return self.level_data.follower_ep

    @property
    def get_current_level(self) -> dict[str, int]:
        """Calculates user level."""

        # get current user experience points
        # maybe we should use return value instead of attributes?
        self.calc_current_ep()

        while self.current_ep >= self.ep_to_next_level:

            if self.current_level > self.max_level:
                self.current_level = self.max_level
                break

            # increase user level
            self.current_level += 1
            self.current_ep -= self.ep_to_next_level
            self.ep_to_next_level += 100

            percentage_level = self.percentage_ep_level(
                self.current_ep, self.ep_to_next_level)

        return {
            "current_level": self.current_level,
            "current_ep": self.current_ep,
            "ep_to_next_level": self.ep_to_next_level,
            "percentage_level": percentage_level
        }

    def percentage_ep_level(self, current_ep: int, ep_to_next_level: int) -> float:
        """Helper function that calcs the percentage value to the next level"""
        return current_ep / ep_to_next_level * 100
