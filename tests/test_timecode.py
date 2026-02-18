import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from videotools.timecode import parse_timecode


class TestParseTimecode(unittest.TestCase):
    def test_minutes_seconds(self) -> None:
        self.assertEqual(parse_timecode("0:00"), 0.0)
        self.assertEqual(parse_timecode("1:12"), 72.0)

    def test_minutes_seconds_with_ms(self) -> None:
        self.assertAlmostEqual(parse_timecode("3:25.500"), 205.5)

    def test_seconds_numeric(self) -> None:
        self.assertEqual(parse_timecode(10), 10.0)
        self.assertEqual(parse_timecode(2.5), 2.5)
        self.assertEqual(parse_timecode("15.25"), 15.25)

    def test_hours_minutes_seconds(self) -> None:
        self.assertEqual(parse_timecode("1:02:03"), 3723.0)

    def test_invalid(self) -> None:
        with self.assertRaises(ValueError):
            parse_timecode("")
        with self.assertRaises(ValueError):
            parse_timecode("bad")


if __name__ == "__main__":
    unittest.main()
