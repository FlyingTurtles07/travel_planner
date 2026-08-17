import argparse
from datetime import datetime


def validate_date(date_string):
    """날짜 형식이 YYYY-MM-DD인지 확인"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():
    # CLI 명령어 설정
    parser = argparse.ArgumentParser(
        description="AI 여행 플래너"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="여행 날짜를 YYYY-MM-DD 형식으로 입력하세요."
    )

    args = parser.parse_args()

    # 날짜 형식 검사
    if not validate_date(args.date):
        print("❌ 잘못된 날짜 형식입니다.")
        print("예시: 2026-03-15")
        return

    print("=" * 40)
    print("       AI 여행 플래너")
    print("=" * 40)
    print(f"여행 날짜: {args.date}")
    print("✅ 날짜 형식이 올바릅니다.")
    print("다음 단계로 진행합니다.")


if __name__ == "__main__":
    main()