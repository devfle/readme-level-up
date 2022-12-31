"""
Unit Tests for main.py
"""

import os
import unittest
from unittest.mock import patch
from main import draw_progress_bar

class TestDrawProgressBar(unittest.TestCase):
    """Tests the DrawProgressBar function"""

    @patch.dict(os.environ, {'INPUT_PROGRESS_BAR_CHAR_LENGTH': '30',
     'INPUT_EMPTY_BAR': '░', 'INPUT_FILLED_BAR': '█'}, clear=True)
    def test_draw_progress_bar(self):
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

if __name__ == '__main__':
    unittest.main()
