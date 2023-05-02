"""Module that contains all the data for the levelsystem."""
from dataclasses import dataclass

@dataclass
class ReadmeLevelData:
    """Class that contains the data for the levelsystem."""
    contribution_ep: int
    project_ep: int
    discussion_ep: int
    star_ep: int
    follower_ep: int
