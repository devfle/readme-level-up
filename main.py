"""The main file of this project."""
from os import getenv
from re import sub
from operator import itemgetter
from readme_level import ReadmeLevel


readme_instance: ReadmeLevel = ReadmeLevel()


def draw_progress_bar() -> str:
    """Draws the progress bar"""
    progress_bar_length: int = int(getenv("INPUT_PROGRESS_BAR_CHAR_LENGTH"))

    progress_bar_content = {
        "empty_bar": getenv("INPUT_EMPTY_BAR"),
        "filled_bar": getenv("INPUT_FILLED_BAR")
    }

    progress_bar: str = ""
    filled_progress: int = round(progress_bar_length * (50 / 100), 0)

    for index in range(progress_bar_length):

        if index <= filled_progress:
            progress_bar += progress_bar_content["filled_bar"]

        if index > filled_progress:
            progress_bar += progress_bar_content["empty_bar"]

    return progress_bar


user_level, to_next_lvl = itemgetter("current_level",
                                     "percentage_level")(readme_instance.calc_current_level())

readme_path: str = getenv("INPUT_README_PATH")
start_section: str = "<!--README_LEVEL_UP:START-->"
end_section: str = "<!--README_LEVEL_UP:END-->"
search_pattern: str = fr"{start_section}[\s\S]*?{end_section}"
replace_str: str = (f"{start_section}\n"
                    "```text\n"
                    f"level: { user_level }  { draw_progress_bar() } {round(to_next_lvl, 2)}%\n"
                    "```\n"
                    f"{end_section}")


# update readme
with open(readme_path, mode="r", encoding="utf-8") as readme_file:
    readme_content = readme_file.read()

changed_readme = sub(search_pattern, repl=replace_str, string=readme_content)

with open(readme_path, mode="w", encoding="utf-8") as readme_file:
    readme_file.write(changed_readme)
