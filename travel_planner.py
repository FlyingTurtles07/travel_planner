import argparse
import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai


def validate_date(date_string):
    """날짜 형식이 YYYY-MM-DD인지 확인"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_travel_recommendation(date):
    """Gemini API를 이용해 여행지를 추천받는다."""

    # .env 파일 불러오기
    load_dotenv()

    # Gemini API 키 가져오기
    api_key = os.getenv("GEMINI_API_KEY")

    # API 키가 없는 경우
    if not api_key:
        print("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하세요.")
        return None

    try:
        # Gemini 클라이언트 생성
        client = genai.Client(api_key=api_key)

        prompt = f"""
{date}에 국내 여행을 간다고 가정하고,
여행하기 좋은 지역 하나를 추천해주세요.

다음 내용을 포함해서 간단하게 설명해주세요.

1. 추천 지역
2. 추천 이유
3. 예상되는 여행 분위기
"""

        # Gemini API 호출
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("❌ Gemini API 호출 중 오류가 발생했습니다.")
        print(f"오류 내용: {e}")
        return None


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
    print()

    # Gemini API 호출
    print("[1/3] 여행지 추천 생성 중(Gemini)...")

    recommendation = get_travel_recommendation(args.date)

    if recommendation is None:
        return

    print()
    print("===== AI 여행 추천 결과 =====")
    print(recommendation)


if __name__ == "__main__":
    main()