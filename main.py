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


if __name__ == "__main__":

    readme_instance: ReadmeLevel = ReadmeLevel()

    user_level, to_next_lvl = itemgetter("current_level",
                                         "percentage_level")(readme_instance.calc_current_level())

    CONTRIBUTION_EP = readme_instance.level_data.contribution_ep
    FOLLOWER_EP = readme_instance.level_data.follower_ep
    # should be generated in later versions
    ep_information = (f"<pre>💪 1x contribute → { CONTRIBUTION_EP } experience points\n"
                      f"🌟 1x follower → { FOLLOWER_EP } experience points</pre>\n")

    readme_path: str = getenv("INPUT_README_PATH")
    start_section: str = "<!--README_LEVEL_UP:START-->"
    end_section: str = "<!--README_LEVEL_UP:END-->"
    search_pattern: str = fr"{start_section}[\s\S]*?{end_section}"
    replace_str: str = (f"{start_section}\n"
                        f"{ getenv('INPUT_CARD_TITLE') if getenv('INPUT_CARD_TITLE') else '' } \n"
                        f"<pre>level: { user_level }  { draw_progress_bar(to_next_lvl) } {round(to_next_lvl, 2)}%</pre>\n"
                        f"{ ep_information if getenv('INPUT_SHOW_EP_INFO') else '' }"
                        f"{end_section}")

    # update readme
    with open(readme_path, mode="r", encoding="utf-8") as readme_file:
        readme_content = readme_file.read()

    changed_readme = sub(search_pattern, repl=replace_str,
                         string=readme_content)

    with open(readme_path, mode="w", encoding="utf-8") as readme_file:
        readme_file.write(changed_readme)
