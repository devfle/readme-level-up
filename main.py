"""The main file of this project."""
from os import getenv
from re import sub
from operator import itemgetter
from readme_level import ReadmeLevel


def draw_progress_bar(current_progress: float | int) -> str:
    """Draws the progress bar"""
    progress_bar_length: int = int(getenv("INPUT_PROGRESS_BAR_CHAR_LENGTH"))

    progress_bar_content = {
        "empty_bar": getenv("INPUT_EMPTY_BAR"),
        "filled_bar": getenv("INPUT_FILLED_BAR")
    }

    progress_bar: str = ""
    filled_progress: int = round(
        progress_bar_length * (current_progress / 100), 0)

    for index in range(progress_bar_length):

        # because the index starts at 0 we reduce filled_progress
        # we should define our own index
        if index <= filled_progress - 1:
            progress_bar += progress_bar_content["filled_bar"]

        if index > filled_progress - 1:
            progress_bar += progress_bar_content["empty_bar"]

    return progress_bar


def generate_content(readme_instance: ReadmeLevel, start_section: str, end_section: str) -> str:
    """Generates the content for readme file"""
    user_level, to_next_lvl = itemgetter("current_level",
                                         "percentage_level")(readme_instance.get_current_level)

    CONTRIBUTION_EP = readme_instance.get_contribution_ep
    FOLLOWER_EP = readme_instance.get_follower_ep

    # should be generated in later versions
    ep_information = (f"<pre>💪 1x contribute → { CONTRIBUTION_EP } experience points\n"
                      f"🌟 1x follower → { FOLLOWER_EP } experience points</pre>\n")

    return (f"{start_section}\n"
            f"{ getenv('INPUT_CARD_TITLE') if getenv('INPUT_CARD_TITLE') else '' } \n"
            f"<pre>level: { user_level }  { draw_progress_bar(to_next_lvl) } {round(to_next_lvl, 2)}%</pre>\n"
            f"{ ep_information if getenv('INPUT_SHOW_EP_INFO') else '' }"
            f"{end_section}")


if __name__ == "__main__":

    README_PATH: str = getenv("INPUT_README_PATH")
    START_SECTION: str = "<!--README_LEVEL_UP:START-->"
    END_SECTION: str = "<!--README_LEVEL_UP:END-->"
    SEARCH_PATTERN: str = fr"{START_SECTION}[\s\S]*?{END_SECTION}"

    replace_str: str = generate_content(
        ReadmeLevel(), START_SECTION, END_SECTION)

    # update readme
    with open(README_PATH, mode="r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()

    changed_readme = sub(SEARCH_PATTERN, repl=replace_str,
                         string=readme_content)

    with open(README_PATH, mode="w", encoding="utf-8") as readme_file:
        readme_file.write(changed_readme)
