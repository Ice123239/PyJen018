import math
import sys
from pathlib import Path


REPORT_DIRECTORY = Path(r"D:\bmi")
DEFAULT_WEIGHT_KG = 65.0
DEFAULT_HEIGHT_M = 1.70


def _height_in_meters(height):
    """แปลงส่วนสูงจากเซนติเมตรเป็นเมตรเมื่อค่ามากกว่า 3"""
    return height / 100 if height > 3 else height


def calculate_bmi(weight_kg, height_m):
    """คำนวณดัชนีมวลกายและเกณฑ์ โดยรับส่วนสูงได้ทั้งเมตรและเซนติเมตร"""
    try:
        weight_kg = float(weight_kg)
        height_m = float(height_m)
    except (TypeError, ValueError) as error:
        raise ValueError("กรุณากรอกน้ำหนักและส่วนสูงเป็นตัวเลข") from error

    if not math.isfinite(weight_kg) or weight_kg <= 0:
        raise ValueError("น้ำหนักต้องเป็นตัวเลขที่มากกว่าศูนย์")
    if not math.isfinite(height_m) or height_m <= 0:
        raise ValueError("ส่วนสูงต้องเป็นตัวเลขที่มากกว่าศูนย์")

    height_m = _height_in_meters(height_m)
    bmi = weight_kg / (height_m**2)
    if bmi < 18.5:
        category = "ผอม/น้ำหนักน้อย"
    elif bmi < 25:
        category = "ปกติ (สุขภาพดี)"
    elif bmi < 30:
        category = "น้ำหนักเกิน"
    elif bmi < 35:
        category = "อ้วนระดับ 1"
    else:
        category = "อ้วนระดับ 2"
    return bmi, category


def _read_positive_number(prompt, label, input_fn):
    while True:
        entered_value = input_fn(prompt).strip()
        try:
            value = float(entered_value)
            if not math.isfinite(value) or value <= 0:
                raise ValueError
            return value
        except ValueError:
            print(f"กรุณากรอก{label}เป็นตัวเลขที่มากกว่าศูนย์")


def get_measurements(input_fn=None, interactive=None):
    """รับข้อมูลจากผู้ใช้ หรือใช้ค่าเริ่มต้นเมื่อทำงานแบบไม่โต้ตอบ"""
    if input_fn is None:
        input_fn = input
    if interactive is None:
        interactive = sys.stdin.isatty() and sys.stdout.isatty()

    if not interactive:
        print(
            "โหมดไม่โต้ตอบ: ใช้ค่าเริ่มต้น "
            f"(น้ำหนัก {DEFAULT_WEIGHT_KG:.0f} กิโลกรัม, "
            f"ส่วนสูง {DEFAULT_HEIGHT_M:.2f} เมตร)"
        )
        return DEFAULT_WEIGHT_KG, DEFAULT_HEIGHT_M

    try:
        weight = _read_positive_number(
            "กรุณากรอกน้ำหนัก (กิโลกรัม): ", "น้ำหนัก", input_fn
        )
        height = _read_positive_number(
            "กรุณากรอกส่วนสูง (เมตรหรือเซนติเมตร): ", "ส่วนสูง", input_fn
        )
        return weight, height
    except EOFError:
        print(
            "ไม่มีข้อมูลนำเข้า: ใช้ค่าเริ่มต้น "
            f"(น้ำหนัก {DEFAULT_WEIGHT_KG:.0f} กิโลกรัม, "
            f"ส่วนสูง {DEFAULT_HEIGHT_M:.2f} เมตร)"
        )
        return DEFAULT_WEIGHT_KG, DEFAULT_HEIGHT_M


def _format_report(weight_kg, height_m, bmi, category):
    normalized_height = _height_in_meters(height_m)
    border = "+" + "-" * 55 + "+"
    rows = [
        f"| {'รายงานดัชนีมวลกาย':^53} |",
        border,
        f"| {'น้ำหนัก':<18} : {f'{weight_kg:.2f} กิโลกรัม':>32} |",
        f"| {'ส่วนสูง':<18} : {f'{normalized_height:.2f} เมตร':>32} |",
        f"| {'ดัชนีมวลกาย':<18} : {f'{bmi:.2f}':>32} |",
        f"| {'เกณฑ์':<18} : {category:>32} |",
        border,
    ]
    return "\n".join(rows) + "\n"


def save_and_open_report(weight_kg, height_m):
    """บันทึกรายงานภาษาไทยที่ D:\\bmi และแสดงรายงานในคอนโซล"""
    bmi, category = calculate_bmi(weight_kg, height_m)
    weight_kg = float(weight_kg)
    height_m = float(height_m)
    report = _format_report(weight_kg, height_m, bmi, category)

    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIRECTORY / "bmi_report.txt"
    report_path.write_text(report, encoding="utf-8")
    print(report_path.read_text(encoding="utf-8"), end="")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    weight, height = get_measurements()
    save_and_open_report(weight, height)


if __name__ == "__main__":
    main()
