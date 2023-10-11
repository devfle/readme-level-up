"""Module that contains all the logic about the levelsystem."""
from os import getenv
from logging import exception, info
from requests import post
from graphql_query import QUERY
from readme_data import ReadmeLevelData


class ReadmeLevel:
    """Class that contains all the logic about the levelsystem."""

    level_data: ReadmeLevelData = ReadmeLevelData(
        contribution_ep=20, project_ep=5, discussion_ep=10, star_ep=40, follower_ep=25)

    def __init__(self) -> None:
        self.max_level: int = 99
        self.ep_to_next_level: int = 100
        self.current_ep: int = 0
        self.current_level: int = 1

    def fetch_user_data(self) -> dict[str, int] | None:
        """Fetches the user data from github api"""

        if not getenv("INPUT_GITHUB_TOKEN"):
            exception("an error with the github token occurred")

        auth_header = {"Authorization": "Bearer " +
                       getenv("INPUT_GITHUB_TOKEN")}
        response = post("https://api.github.com/graphql",
                        json={"query": QUERY}, headers=auth_header, timeout=2)

        if response.status_code == 200:
            info("request to github api was successfull")

            response_data = response.json()

            user_data = (response_data["data"]["user"]
                         ["contributionsCollection"]["contributionCalendar"])

            user_data["totalFollowers"] = (response_data["data"]["user"]
                                           ["followers"]["totalCount"])

            user_data["totalRepositories"] = (response_data["data"]["user"]
                                           ["repositories"]["totalCount"])

            return user_data

        exception("request to github api failed")
        return None

    def calc_current_ep(self) -> int:
        """Calculates the current user experience points"""

        # get user stats
        user_stats: dict[str, int] = self.fetch_user_data()

        # calc the current experience points
        self.current_ep = (
            user_stats["totalContributions"] * self.level_data.contribution_ep +
            user_stats["totalFollowers"] * self.level_data.follower_ep +
            user_stats["totalRepositories"] * self.level_data.project_ep)

        return self.current_ep

    # should be part of data class
    @property
    def get_contribution_ep(self) -> int:
        """gets the contribution ep"""
        return self.level_data.contribution_ep


    # should be part of data class
    @property
    def get_follower_ep(self) -> int:
        """gets the follower ep"""
        return self.level_data.follower_ep

    # should be part of data class
    @property
    def get_project_ep(self) -> int:
        """gets the project ep"""
        return self.level_data.project_ep

    @property
    def get_current_level(self) -> dict[str, int]:
        """Calculates user level."""

        # get current user experience points
        current_ep: int = self.calc_current_ep()

        while current_ep >= self.ep_to_next_level:

            if self.current_level > self.max_level:
                self.current_level = self.max_level
                break

            # increase user level
            self.current_level += 1
            current_ep -= self.ep_to_next_level
            self.ep_to_next_level += 100

        percentage_level = self.percentage_ep_level(
            current_ep, self.ep_to_next_level)

        # sync current ep
        self.current_ep = current_ep

        return {
            "current_level": self.current_level,
            "current_ep": self.current_ep,
            "ep_to_next_level": self.ep_to_next_level,
            "percentage_level": percentage_level
        }

    def percentage_ep_level(self, current_ep: int, ep_to_next_level: int) -> float:
        """Helper function that calcs the percentage value to the next level"""
        return current_ep / ep_to_next_level * 100
