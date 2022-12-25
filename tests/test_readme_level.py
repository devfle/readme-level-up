"""
Unit Tests for readme_level.py
"""

import unittest
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

if __name__ == '__main__':
    unittest.main()
