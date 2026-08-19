import argparse
import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


# ----------------------------------------
# Gemini가 반환할 JSON 구조
# ----------------------------------------

class TravelRecommendation(BaseModel):
    recommended_city: str
    weather: str
    events: list[str]
    reason: str


# ----------------------------------------
# 날짜 형식 검사
# ----------------------------------------

def validate_date(date_string):
    """날짜 형식이 YYYY-MM-DD인지 확인"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ----------------------------------------
# Gemini API 호출
# ----------------------------------------

def get_travel_recommendation(date):
    """Gemini API를 이용해 여행지 추천을 JSON으로 받는다."""

    # .env 파일 불러오기
    load_dotenv()

    # Gemini API 키 가져오기
    api_key = os.getenv("GEMINI_API_KEY")

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

다음 정보를 작성해주세요.

- 추천 지역
- 예상 날씨
- 해당 날짜에 즐길 수 있는 행사나 축제
- 추천 이유

반드시 지정된 JSON 구조로 응답하세요.
"""

        # Gemini에게 구조화된 JSON 요청
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TravelRecommendation,
            ),
        )

        # Gemini의 JSON 응답을 Pydantic 객체로 변환
        recommendation = TravelRecommendation.model_validate_json(
            response.text
        )

        return recommendation

    except Exception as e:
        print("❌ Gemini API 호출 또는 JSON 처리 중 오류가 발생했습니다.")
        print(f"오류 내용: {e}")
        return None


# ----------------------------------------
# 메인 프로그램
# ----------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="AI 여행 플래너"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="여행 날짜를 YYYY-MM-DD 형식으로 입력하세요."
    )

    args = parser.parse_args()

    # 날짜 검사
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

    # Gemini 호출
    print("[1/3] 1차 추천 생성 중(Gemini)...")

    recommendation = get_travel_recommendation(args.date)

    if recommendation is None:
        return

    print()
    print("===== 1차 여행 추천 결과 =====")

    print(f"추천 지역: {recommendation.recommended_city}")
    print(f"날씨: {recommendation.weather}")
    print(f"추천 이유: {recommendation.reason}")

    print("행사/축제:")
    for event in recommendation.events:
        print(f"  - {event}")

    print()
    print("===== JSON 데이터 =====")
    print(recommendation.model_dump_json(indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()