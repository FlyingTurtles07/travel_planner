import argparse
import json
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
# 진행 로그
# ----------------------------------------

def log_step(step, message):
    """프로그램 진행 상황을 출력한다."""
    print(f"[{step}/3] {message}")


def log_info(message):
    """일반 진행 정보를 출력한다."""
    print(f"  - {message}")


def log_success(message):
    """성공 메시지를 출력한다."""
    print(f"  - ✅ {message}")


def log_warning(message):
    """경고 메시지를 출력한다."""
    print(f"  - ⚠️ {message}")


def log_error(message):
    """오류 메시지를 출력한다."""
    print(f"  - ❌ {message}")


# ----------------------------------------
# 날짜 형식 검사
# ----------------------------------------

def validate_date(date_string):
    """날짜 형식이 YYYY-MM-DD인지 확인한다."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ----------------------------------------
# Gemini 1차 요청
# ----------------------------------------

def request_gemini(client, date):
    """Gemini에게 여행 추천 JSON을 요청한다."""

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

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TravelRecommendation,
        ),
    )

    if not response.text:
        raise ValueError("Gemini가 빈 응답을 반환했습니다.")

    return response.text


# ----------------------------------------
# Gemini 여행 추천
# ----------------------------------------

def get_travel_recommendation(date):
    """
    Gemini API 호출
    + JSON 파싱
    + JSON 파싱 실패 시 1회 재요청
    """

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        log_error("GEMINI_API_KEY가 설정되지 않았습니다.")
        log_info(".env 파일을 확인하세요.")

        return None, {
            "step": "llm_recommendation",
            "type": "MISSING_API_KEY",
            "message": "GEMINI_API_KEY가 설정되지 않았습니다.",
        }

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        log_error("Gemini 클라이언트 생성에 실패했습니다.")
        log_info(f"오류 내용: {e}")

        return None, {
            "step": "llm_recommendation",
            "type": "CLIENT_ERROR",
            "message": str(e),
        }

    # 최대 2회 요청
    for attempt in range(2):
        try:
            if attempt == 0:
                log_info("1차 JSON 요청 중...")
            else:
                log_warning("JSON 파싱 실패 → 1회 재요청 중...")

            response_text = request_gemini(client, date)

            log_info("JSON 응답 검증 중...")

            recommendation = TravelRecommendation.model_validate_json(
                response_text
            )

            log_success("JSON 파싱 및 검증 성공")

            return recommendation, None

        except Exception as e:
            if attempt == 0:
                log_warning("JSON 파싱 또는 Gemini 요청에 실패했습니다.")
                log_info("1회 재요청합니다.")
                continue

            log_error("JSON 파싱 재시도도 실패했습니다.")

            return None, {
                "step": "llm_recommendation",
                "type": "JSON_PARSE_ERROR",
                "message": str(e),
            }

    return None, {
        "step": "llm_recommendation",
        "type": "UNKNOWN_ERROR",
        "message": "알 수 없는 오류가 발생했습니다.",
    }


# ----------------------------------------
# Kakao 맛집 검색
# ----------------------------------------

def search_restaurants(city):
    """Kakao Local API로 추천 지역의 맛집을 검색한다."""

    load_dotenv()

    kakao_api_key = os.getenv("KAKAO_REST_API_KEY")

    if not kakao_api_key:
        log_warning("KAKAO_REST_API_KEY가 설정되지 않았습니다.")
        log_info("맛집 검색 없이 다음 단계로 진행합니다.")

        return [], {
            "step": "kakao_restaurant_search",
            "type": "MISSING_API_KEY",
            "message": "KAKAO_REST_API_KEY가 설정되지 않았습니다.",
        }

    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    params = {
        "query": f"{city} 맛집",
        "size": 5,
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()
        documents = data.get("documents", [])

        if not documents:
            log_warning("검색 결과 0건")
            log_info("맛집 데이터 없이 다음 단계로 진행합니다.")

            return [], None

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
                "y": item.get("y", ""),
            }

            restaurants.append(restaurant)

        return restaurants, None

    except requests.RequestException as e:
        log_error("Kakao API 요청 중 오류가 발생했습니다.")
        log_info(f"오류 내용: {e}")
        log_info("맛집 데이터 없이 다음 단계로 진행합니다.")

        return [], {
            "step": "kakao_restaurant_search",
            "type": "REQUEST_ERROR",
            "message": str(e),
        }

    except ValueError as e:
        log_error("Kakao API 응답 JSON 처리 중 오류가 발생했습니다.")
        log_info(f"오류 내용: {e}")

        return [], {
            "step": "kakao_restaurant_search",
            "type": "JSON_RESPONSE_ERROR",
            "message": str(e),
        }

    except Exception as e:
        log_error("맛집 검색 처리 중 오류가 발생했습니다.")
        log_info(f"오류 내용: {e}")
        log_info("다음 단계로 진행합니다.")

        return [], {
            "step": "kakao_restaurant_search",
            "type": "PROCESSING_ERROR",
            "message": str(e),
        }


# ----------------------------------------
# 최종 여행 리포트 생성
# ----------------------------------------

def generate_final_report(
    date,
    recommendation,
    restaurants,
    errors,
):
    """
    Gemini에게 1차 추천 결과와 Kakao 맛집 결과를 전달하여
    최종 Markdown 여행 리포트를 생성한다.
    """

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        log_error("GEMINI_API_KEY가 설정되지 않았습니다.")

        return None, {
            "step": "final_report",
            "type": "MISSING_API_KEY",
            "message": "GEMINI_API_KEY가 설정되지 않았습니다.",
        }

    try:
        client = genai.Client(api_key=api_key)

        recommendation_data = recommendation.model_dump()

        prompt = f"""
다음 데이터를 바탕으로 국내 여행 최종 리포트를 작성해주세요.

여행 날짜:
{date}

[1차 여행 추천]
{json.dumps(
    recommendation_data,
    ensure_ascii=False,
    indent=4
)}

[맛집 검색 결과]
{json.dumps(
    restaurants,
    ensure_ascii=False,
    indent=4
)}

[오류 정보]
{json.dumps(
    errors,
    ensure_ascii=False,
    indent=4
)}

다음 Markdown 형식으로 작성해주세요.

# 국내 여행 추천 리포트

## 1. 추천 지역

추천 지역을 설명해주세요.

## 2. 추천 이유

왜 이 지역을 추천했는지 설명해주세요.

## 3. 날씨

예상 날씨를 정리해주세요.

## 4. 행사 및 축제

해당 날짜에 즐길 수 있는 행사나 축제를 정리해주세요.

## 5. 추천 맛집

검색된 맛집을 정리해주세요.
각 맛집의 이름, 주소, 분류, URL을 포함해주세요.

## 6. 추천 여행 일정

해당 지역에서 하루 동안 여행한다고 가정하고
간단한 1일 여행 일정을 제안해주세요.

## 7. 오류 및 참고사항

API 오류나 검색 결과가 없는 경우
그 내용을 설명해주세요.

주의사항:

- Markdown 형식으로만 작성하세요.
- JSON 형식으로 작성하지 마세요.
- 실제로 제공된 데이터만 사용하세요.
- 맛집 정보는 제공된 검색 결과를 기준으로 작성하세요.
- 확인되지 않은 사실을 임의로 만들어내지 마세요.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        report = response.text

        if not report:
            raise ValueError("Gemini가 빈 리포트를 반환했습니다.")

        return report, None

    except Exception as e:
        log_error("최종 리포트 생성 중 오류가 발생했습니다.")
        log_info(f"오류 내용: {e}")

        return None, {
            "step": "final_report",
            "type": "REPORT_GENERATION_ERROR",
            "message": str(e),
        }


# ----------------------------------------
# 여행 데이터 JSON 저장
# ----------------------------------------

def save_travel_data(
    date,
    recommendation,
    restaurants,
    errors=None,
):
    """전체 여행 데이터를 JSON으로 저장한다."""

    os.makedirs("results", exist_ok=True)

    filename = f"results/{date}_travel_data.json"

    data = {
        "date": date,
        "recommendation": (
            recommendation.model_dump()
            if recommendation
            else None
        ),
        "places": restaurants,
        "errors": errors or [],
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )

    return filename


# ----------------------------------------
# Markdown 여행 리포트 저장
# ----------------------------------------

def save_markdown_report(date, report):
    """최종 여행 리포트를 Markdown 파일로 저장한다."""

    os.makedirs("results", exist_ok=True)

    filename = f"results/{date}_travel_plan.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    return filename


# ----------------------------------------
# 오류 데이터 저장
# ----------------------------------------

def save_error_data(date, error):
    """치명적인 오류를 JSON으로 저장한다."""

    os.makedirs("results", exist_ok=True)

    filename = f"results/{date}_travel_data.json"

    data = {
        "date": date,
        "recommendation": None,
        "places": [],
        "errors": [error] if error else [],
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )

    return filename


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
        help="여행 날짜를 YYYY-MM-DD 형식으로 입력하세요.",
    )

    args = parser.parse_args()

    # 날짜 검사
    if not validate_date(args.date):
        print("❌ 잘못된 날짜 형식입니다.")
        print("예시: 2026-03-15")
        return

    # 시작 화면
    print("=" * 40)
    print("       AI 여행 플래너")
    print("=" * 40)
    print(f"여행 날짜: {args.date}")
    print("✅ 날짜 형식이 올바릅니다.")
    print()

    # ==================================================
    # STEP 1 — Gemini 여행지 추천
    # ==================================================

    log_step(1, "Gemini 여행지 추천")

    log_info("API 호출 중...")

    recommendation, gemini_error = get_travel_recommendation(
        args.date
    )

    if recommendation is None:
        log_error("여행지 추천 생성 실패")

        filename = save_error_data(
            args.date,
            gemini_error,
        )

        log_info(f"오류 기록 저장: {filename}")
        return

    log_success("추천 생성 완료")
    log_info(
        f"추천 지역: {recommendation.recommended_city}"
    )

    print()
    print("===== 1차 여행 추천 결과 =====")
    print(f"추천 지역: {recommendation.recommended_city}")
    print(f"날씨: {recommendation.weather}")
    print(f"추천 이유: {recommendation.reason}")
    print("행사/축제:")

    if recommendation.events:
        for event in recommendation.events:
            print(f"  - {event}")
    else:
        print("  - 제공된 행사/축제 정보가 없습니다.")

    # ==================================================
    # STEP 2 — Kakao 맛집 검색
    # ==================================================

    print()

    log_step(2, "Kakao 맛집 검색")
    log_info(
        f"검색 지역: {recommendation.recommended_city}"
    )
    log_info("API 호출 중...")

    restaurants, kakao_error = search_restaurants(
        recommendation.recommended_city
    )

    if kakao_error:
        log_warning("Kakao API 또는 검색 처리 중 문제가 발생했습니다.")
        log_info("맛집 데이터 없이 계속 진행합니다.")
    elif restaurants:
        log_success(
            f"맛집 {len(restaurants)}곳 검색 완료"
        )
    else:
        log_warning("검색된 맛집이 없습니다.")
        log_info("맛집 데이터 없이 계속 진행합니다.")

    print()
    print("===== 맛집 검색 결과 =====")

    if not restaurants:
        print("검색된 맛집이 없습니다.")
    else:
        for index, restaurant in enumerate(
            restaurants,
            start=1,
        ):
            print(f"{index}. {restaurant['name']}")
            print(f"   주소: {restaurant['address']}")
            print(f"   분류: {restaurant['category']}")
            print(f"   URL: {restaurant['url']}")
            print()

    # 오류 목록
    errors = []

    if kakao_error:
        errors.append(kakao_error)

    # ==================================================
    # STEP 3 — 최종 여행 리포트
    # ==================================================

    print()

    log_step(3, "최종 여행 리포트")
    log_info("Gemini에게 여행 데이터 전달 중...")
    log_info("Markdown 생성 중...")

    report, report_error = generate_final_report(
        date=args.date,
        recommendation=recommendation,
        restaurants=restaurants,
        errors=errors,
    )

    # 최종 리포트 생성 실패
    if report is None:
        log_error("최종 리포트 생성 실패")

        if report_error:
            errors.append(report_error)

        json_filename = save_travel_data(
            date=args.date,
            recommendation=recommendation,
            restaurants=restaurants,
            errors=errors,
        )

        log_info(
            f"지금까지의 여행 데이터 저장 완료: {json_filename}"
        )
        return

    log_success("최종 리포트 생성 완료")

    # ==================================================
    # JSON 저장
    # ==================================================

    log_info("JSON 파일 저장 중...")

    json_filename = save_travel_data(
        date=args.date,
        recommendation=recommendation,
        restaurants=restaurants,
        errors=errors,
    )

    log_success(f"JSON 저장 완료: {json_filename}")

    # ==================================================
    # Markdown 저장
    # ==================================================

    log_info("Markdown 파일 저장 중...")

    markdown_filename = save_markdown_report(
        date=args.date,
        report=report,
    )

    log_success(
        f"Markdown 저장 완료: {markdown_filename}"
    )

    # 최종 결과 출력
    print()
    print("===== 최종 여행 리포트 =====")
    print(report)

    print()
    print("=" * 40)
    print("🎉 AI 여행 플래너 실행 완료!")
    print("=" * 40)
    print(f"JSON    : {json_filename}")
    print(f"Markdown: {markdown_filename}")


if __name__ == "__main__":
    main()
