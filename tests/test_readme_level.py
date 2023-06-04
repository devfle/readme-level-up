"""
Unit Tests for readme_level.py
"""

import unittest
from unittest.mock import patch
from readme_level import ReadmeLevel

class TestLevelSystem(unittest.TestCase):
    """Tests the LevelSystem class"""

    def test_percentage_ep_level(self):
        """Tests the level percantage calc"""
        readme_instance: ReadmeLevel = ReadmeLevel()
        level_data: int = readme_instance.percentage_ep_level(200, 1000)
        self.assertEqual(level_data, 20)

        level_data = readme_instance.percentage_ep_level(0, 1000)
        self.assertEqual(level_data, 0)

        level_data = readme_instance.percentage_ep_level(12, 1000)
        self.assertEqual(level_data, 1.2)

        level_data = readme_instance.percentage_ep_level(-5, 1000)
        self.assertEqual(level_data, -0.5)

    @patch('readme_level.ReadmeLevel._update_user_data')
    def test_calc_current_ep(self, mock_update_user_data):
        """Tests the ep calc"""
        mock_update_user_data.return_value = None
        readme_instance: ReadmeLevel = ReadmeLevel()

        readme_instance.contribution_count = 120
        readme_instance.project_count = 0
        readme_instance.discussion_count = 0
        readme_instance.follower_count = 12

        readme_instance.calc_current_ep()
        self.assertEqual(readme_instance.current_ep, 2700)


if __name__ == '__main__':
    unittest.main()
