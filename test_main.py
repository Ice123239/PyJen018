import io
import unittest
from contextlib import redirect_stdout

from main import (
    DEFAULT_HEIGHT_M,
    DEFAULT_WEIGHT_KG,
    _format_report,
    calculate_bmi,
    get_measurements,
)


class CalculateBmiTests(unittest.TestCase):
    def test_calculates_normal_bmi(self):
        bmi, category = calculate_bmi(68, 1.7)

        self.assertAlmostEqual(bmi, 68 / (1.7**2))
        self.assertEqual(category, "ปกติ (สุขภาพดี)")

    def test_classifies_underweight_bmi(self):
        bmi, category = calculate_bmi(45, 1.7)

        self.assertAlmostEqual(bmi, 45 / (1.7**2))
        self.assertEqual(category, "ผอม/น้ำหนักน้อย")

    def test_converts_height_in_centimeters_to_meters(self):
        bmi_from_centimeters, category_from_centimeters = calculate_bmi(65, 170)
        bmi_from_meters, category_from_meters = calculate_bmi(65, 1.7)

        self.assertAlmostEqual(bmi_from_centimeters, bmi_from_meters)
        self.assertEqual(category_from_centimeters, category_from_meters)

    def test_converts_short_height_in_centimeters_to_meters(self):
        bmi_from_centimeters, category_from_centimeters = calculate_bmi(45, 129)
        bmi_from_meters, category_from_meters = calculate_bmi(45, 1.29)

        self.assertAlmostEqual(bmi_from_centimeters, bmi_from_meters)
        self.assertEqual(category_from_centimeters, category_from_meters)

    def test_classifies_overweight_and_obesity_levels_in_thai(self):
        self.assertEqual(calculate_bmi(70, 1.6)[1], "น้ำหนักเกิน")
        self.assertEqual(calculate_bmi(80, 1.6)[1], "อ้วนระดับ 1")
        self.assertEqual(calculate_bmi(90, 1.6)[1], "อ้วนระดับ 2")

    def test_zero_height_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_bmi(68, 0)

    def test_non_numeric_measurement_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_bmi("not a number", 1.7)


class InputTests(unittest.TestCase):
    def test_reprompts_for_blank_and_invalid_values(self):
        responses = iter(["", "bad", "65", "0", "170"])
        output = io.StringIO()

        with redirect_stdout(output):
            measurements = get_measurements(
                input_fn=lambda _prompt: next(responses), interactive=True
            )

        self.assertEqual(measurements, (65.0, 170.0))
        self.assertEqual(output.getvalue().count("กรุณากรอก"), 3)
        self.assertNotIn("Please enter", output.getvalue())

    def test_non_interactive_mode_uses_defaults(self):
        output = io.StringIO()
        with redirect_stdout(output):
            measurements = get_measurements(
                input_fn=lambda _prompt: self.fail("ไม่ควรเรียกถามข้อมูล"),
                interactive=False,
            )

        self.assertEqual(measurements, (DEFAULT_WEIGHT_KG, DEFAULT_HEIGHT_M))
        self.assertIn("โหมดไม่โต้ตอบ", output.getvalue())


class ReportFormattingTests(unittest.TestCase):
    def test_report_uses_aligned_ascii_frame_and_normalized_height(self):
        report = _format_report(65, 170, 22.49, "ปกติ (สุขภาพดี)")
        lines = report.rstrip("\n").splitlines()

        self.assertEqual(len({len(line) for line in lines}), 1)
        self.assertTrue(all(line.startswith("|") or line.startswith("+") for line in lines))
        self.assertIn("1.70 เมตร", report)
        self.assertIn("รายงานดัชนีมวลกาย", report)
        self.assertIn("ปกติ (สุขภาพดี)", report)
        self.assertNotIn("BMI", report)


if __name__ == "__main__":
    unittest.main()
