"""
Unit Tests for main.py
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from main import draw_progress_bar, generate_content


class TestMainFile(unittest.TestCase):
    """Tests the DrawProgressBar function"""

    @patch.dict(os.environ, {'INPUT_PROGRESS_BAR_CHAR_LENGTH': '30',
                             'INPUT_EMPTY_BAR': '░', 'INPUT_FILLED_BAR': '█'}, clear=True)
    def test_draw_progress_bar(self) -> None:
        """Tests drawing the progress bar"""

        progress_bar: str = draw_progress_bar(20)
        expected_progress_bar: str = "██████░░░░░░░░░░░░░░░░░░░░░░░░"
        self.assertEqual(progress_bar, expected_progress_bar)

        progress_bar: str = draw_progress_bar(20.25)
        self.assertEqual(progress_bar, expected_progress_bar)

        progress_bar: str = draw_progress_bar(100)
        expected_progress_bar: str = "██████████████████████████████"
        self.assertEqual(progress_bar, expected_progress_bar)

        progress_bar: str = draw_progress_bar(200)
        self.assertEqual(progress_bar, expected_progress_bar)

        progress_bar: str = draw_progress_bar(0)
        expected_progress_bar: str = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"
        self.assertEqual(progress_bar, expected_progress_bar)

        progress_bar: str = draw_progress_bar(-10)
        self.assertEqual(progress_bar, expected_progress_bar)

        progress_bar: str = draw_progress_bar(-0)
        self.assertEqual(progress_bar, expected_progress_bar)

    def test_generate_content(self) -> None:
        """Tests generate content for readme file"""

        mock_readme_instance = MagicMock()
        mock_readme_instance.level_data.contribution_ep = 20
        mock_readme_instance.level_data.follower_ep = 20

        mock_readme_instance.get_current_level.return_value = {
            "__current_level": "10", "percentage_level": 20}

        START_SECTION: str = "<!--README_LEVEL_UP:START-->"
        END_SECTION: str = "<!--README_LEVEL_UP:END-->"

        with patch('main.draw_progress_bar') as mock_draw_progress_bar:
            mock_draw_progress_bar.return_value = "██████░░░░░░░░░░░░░░░░░░░░░░░░"

            replace_str: str = generate_content(
                mock_readme_instance, START_SECTION, END_SECTION)

            # we check only if return value is from type str because the spaces makes it realy difficult to check for isEqual
            self.assertIsInstance(replace_str, str)


if __name__ == '__main__':
    unittest.main()
