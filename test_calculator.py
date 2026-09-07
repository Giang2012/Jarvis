from skills.calculator import CalculatorSkill


def check(skill, text, expected):
    actual = skill.execute(text)
    assert actual == expected, f"{text!r}: expected {expected!r}, got {actual!r}"


def main():
    skill = CalculatorSkill()

    check(skill, "25 nhân 4", "100")
    check(skill, "100 chia 4", "25")
    check(skill, "12 cộng 8", "20")
    check(skill, "30 trừ 7", "23")
    check(skill, "2 mũ 8", "256")
    check(skill, "10 + 5 * 2", "20")
    check(skill, "10 / 0", "Không thể chia cho 0.")

    # Security/regression: Python code must not execute.
    bad = skill.execute("__import__('os').system('echo BAD')")
    assert bad == "Biểu thức không hợp lệ.", bad

    print("CALCULATOR TEST PASSED")


if __name__ == "__main__":
    main()
