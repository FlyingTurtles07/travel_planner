import argparse
import os
import requests

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
# Kakao 맛집 검색
# ----------------------------------------

def search_restaurants(city):
    """Kakao Local API로 추천 지역의 맛집을 검색한다."""

    # .env 파일 불러오기
    load_dotenv()

    # Kakao API 키 가져오기
    kakao_api_key = os.getenv("KAKAO_REST_API_KEY")

    if not kakao_api_key:
        print("❌ KAKAO_REST_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하세요.")
        print("  - 다음 단계로 진행합니다.")
        return []

    # Kakao Local API 주소
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    # 인증 헤더
    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    # 검색 조건
    params = {
        "query": f"{city} 맛집",
        "size": 5
    }

    try:
        print()
        print("[2/3] 맛집 검색 중(Kakao Local)...")

        # Kakao API 요청
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        # HTTP 오류 확인
        response.raise_for_status()

        # JSON 응답으로 변환
        data = response.json()

        # 검색 결과 가져오기
        documents = data.get("documents", [])

        # ----------------------------------------
        # 검색 결과가 0개인 경우
        # ----------------------------------------

        if not documents:
            print("  - 검색 결과 0건")
            print("  - 다음 단계로 진행합니다.")

            return []

        # ----------------------------------------
        # 검색 결과가 있는 경우
        # ----------------------------------------

        restaurants = []

        for item in documents:

            restaurant = {
                "name": item.get("place_name", ""),
                "address": (
                    item.get("road_address_name")
                    or item.get("address_name", "")
                ),
                "category": item.get("category_name", ""),
                "url": item.get("place_url", ""),
                "x": item.get("x", ""),
                "y": item.get("y", "")
            }

            restaurants.append(restaurant)

        print(f"  - 맛집 {len(restaurants)}곳 검색 완료")

        return restaurants

    # ----------------------------------------
    # Kakao API 오류
    # ----------------------------------------

    except requests.RequestException as e:

        print("  - Kakao API 요청 중 오류가 발생했습니다.")
        print(f"  - 오류 내용: {e}")
        print("  - 다음 단계로 진행합니다.")

        return []

    except Exception as e:

        print("  - 맛집 검색 처리 중 오류가 발생했습니다.")
        print(f"  - 오류 내용: {e}")
        print("  - 다음 단계로 진행합니다.")

        return []


# ----------------------------------------
# 메인 프로그램
# ----------------------------------------

def main():

    # CLI 설정
    parser = argparse.ArgumentParser(
        description="AI 여행 플래너"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="여행 날짜를 YYYY-MM-DD 형식으로 입력하세요."
    )

    args = parser.parse_args()

    # ----------------------------------------
    # 날짜 검사
    # ----------------------------------------

    if not validate_date(args.date):

        print("❌ 잘못된 날짜 형식입니다.")
        print("예시: 2026-03-15")

        return

    # ----------------------------------------
    # 프로그램 시작 화면
    # ----------------------------------------

    print("=" * 40)
    print("       AI 여행 플래너")
    print("=" * 40)

    print(f"여행 날짜: {args.date}")
    print("✅ 날짜 형식이 올바릅니다.")
    print()

    # ----------------------------------------
    # STEP 1
    # Gemini 여행지 추천
    # ----------------------------------------

    print("[1/3] 1차 추천 생성 중(Gemini)...")

    recommendation = get_travel_recommendation(args.date)

    # Gemini 실패
    if recommendation is None:
        return

    # ----------------------------------------
    # Gemini 결과 출력
    # ----------------------------------------

    print()
    print("===== 1차 여행 추천 결과 =====")

    print(
        f"추천 지역: "
        f"{recommendation.recommended_city}"
    )

    print(
        f"날씨: "
        f"{recommendation.weather}"
    )

    print(
        f"추천 이유: "
        f"{recommendation.reason}"
    )

    print("행사/축제:")

    for event in recommendation.events:
        print(f"  - {event}")

    # ----------------------------------------
    # JSON 데이터 출력
    # ----------------------------------------

    print()
    print("===== JSON 데이터 =====")

    print(
        recommendation.model_dump_json(
            indent=4,
            ensure_ascii=False
        )
    )

    # ----------------------------------------
    # STEP 2
    # Gemini의 recommended_city를
    # Kakao API의 검색 지역으로 사용
    # ----------------------------------------

    city = recommendation.recommended_city

    restaurants = search_restaurants(city)

    # ----------------------------------------
    # Kakao 검색 결과 출력
    # ----------------------------------------

    print()
    print("===== 맛집 검색 결과 =====")

    if not restaurants:

        print("검색된 맛집이 없습니다.")
        print("맛집 데이터 없이 다음 단계로 진행합니다.")

    else:

        for index, restaurant in enumerate(
            restaurants,
            start=1
        ):

            print(
                f"{index}. "
                f"{restaurant['name']}"
            )

            print(
                f"   주소: "
                f"{restaurant['address']}"
            )

            print(
                f"   분류: "
                f"{restaurant['category']}"
            )

            print(
                f"   URL: "
                f"{restaurant['url']}"
            )

            print()

    # ----------------------------------------
    # STEP 3는 다음 단계에서 추가
    # ----------------------------------------

    print()
    print("[3/3] 최종 리포트 생성 단계는 다음 STEP에서 추가합니다.")

    print()
    print("=" * 40)
    print("현재 STEP 12까지 완료")
    print("=" * 40)


# ----------------------------------------
# 프로그램 실행
# ----------------------------------------

if __name__ == "__main__":
    main()