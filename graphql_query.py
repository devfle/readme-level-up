"""Query for github graphql api"""
from os import getenv, linesep
from datetime import datetime

# get the current year
current_year = datetime.now().year
contribution_list = []

# in a later version we can replace the 2015 date with user input
while current_year >= 2015:

    temp_query = f"""
                    {"_" + str(current_year)}: contributionsCollection(from: "{str(current_year)}-01-01T00:00:00") {{
                        contributionCalendar {{
                            totalContributions
                        }}
                    }}
                """

    contribution_list.append(temp_query)
    current_year -= 1

QUERY = f"""
            {{
                user(login: "{getenv("INPUT_GITHUB_USERNAME")}") {{
                    {linesep.join(contribution_list)}
                    followers {{
                        totalCount
                    }}
                    repositories {{
                        totalCount
                    }}
                }}
            }}
        """
