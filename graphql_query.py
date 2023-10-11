"""Query for github graphql api"""
from os import getenv

QUERY = f"""
            {{
                user(login: "{getenv("INPUT_GITHUB_USERNAME")}") {{
                    contributionsCollection {{
                        contributionCalendar {{
                            totalContributions
                        }}
                    }}
                    followers {{
                        totalCount
                    }}
                    RepositoryConnection {{
                        totalCount
                    }}
                }}
            }}
        """
