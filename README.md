# AI 여행 플래너

## 1. 프로젝트 소개

AI 여행 플래너는 사용자가 입력한 여행 날짜를 기반으로 AI가 국내 여행지를 추천하고, 추천 지역의 맛집을 검색한 후 최종 여행 리포트를 생성하는 Python 콘솔 프로그램입니다.

Gemini API와 Kakao Local API를 연결하여 여러 API의 결과를 하나의 여행 정보로 통합합니다.

이 프로젝트의 전체 흐름은 다음과 같습니다.

```text
여행 날짜 입력
    ↓
날짜 형식 검사
    ↓
Gemini 1차 여행지 추천
    ↓
구조화된 JSON 검증
    ↓
recommended_city 추출
    ↓
Kakao Local API 맛집 검색
    ↓
추천 정보 + 맛집 정보 통합
    ↓
Gemini 최종 여행 리포트 생성
    ↓
JSON + Markdown 파일 저장
```

---

## 2. 주요 기능

### ① 날짜 입력 및 검증

명령줄에서 여행 날짜를 `YYYY-MM-DD` 형식으로 입력합니다.

```powershell
python travel_planner.py --date 2026-03-15
```

입력된 날짜가 올바른 날짜 형식인지 검사합니다.

잘못된 날짜를 입력하면 프로그램을 종료하고 올바른 형식의 예시를 보여줍니다.

---

### ② Gemini AI 여행지 추천

Gemini API를 이용하여 입력한 여행 날짜에 적합한 국내 여행지를 추천받습니다.

Gemini의 1차 응답은 다음 구조로 관리합니다.

```json
{
    "recommended_city": "추천 지역",
    "weather": "예상 날씨",
    "events": [
        "행사 또는 축제"
    ],
    "reason": "추천 이유"
}
```

Pydantic의 `TravelRecommendation` 모델을 사용하여 응답 데이터의 구조를 검증합니다.

---

### ③ JSON 구조화 및 재요청

Gemini 응답을 JSON 형식으로 요청하고 Pydantic 모델로 검증합니다.

JSON 파싱 또는 Gemini 요청에 실패하면 최대 1회 재요청합니다.

```text
1차 Gemini 요청
      ↓
JSON 검증
      ↓
성공 ─────────→ 다음 단계
      ↓ 실패
1회 재요청
      ↓
성공 ─────────→ 다음 단계
      ↓ 실패
오류 기록 후 종료
```

---

### ④ Kakao Local API 맛집 검색

Gemini가 추천한 지역을 Kakao Local API에 전달하여 맛집을 검색합니다.

검색 결과에서 다음 정보를 사용합니다.

- 맛집 이름
- 주소
- 분류
- URL
- X 좌표
- Y 좌표

검색 결과는 최대 5개를 사용합니다.

Kakao API에 문제가 발생하더라도 프로그램 전체를 종료하지 않고 맛집 데이터를 빈 목록으로 처리하여 다음 단계로 진행합니다.

---

### ⑤ 최종 여행 리포트 생성

1차 Gemini 추천 결과와 Kakao 맛집 검색 결과를 다시 Gemini에게 전달합니다.

Gemini는 다음 내용을 포함한 Markdown 여행 리포트를 생성합니다.

- 추천 지역
- 추천 이유
- 날씨
- 행사 및 축제
- 추천 맛집
- 1일 여행 일정
- 오류 및 참고사항

최종 리포트에서는 실제로 전달된 데이터를 기준으로 작성하도록 요청하며, 확인되지 않은 사실을 임의로 만들지 않도록 지시합니다.

---

### ⑥ 결과 파일 저장

실행 결과는 `results` 폴더에 저장됩니다.

```text
results/
├── 2026-03-15_travel_data.json
└── 2026-03-15_travel_plan.md
```

#### JSON 파일

`날짜_travel_data.json`

다음 정보를 저장합니다.

- 여행 날짜
- Gemini 추천 결과
- Kakao 맛집 결과
- 오류 정보

#### Markdown 파일

`날짜_travel_plan.md`

사람이 읽을 수 있는 최종 여행 리포트입니다.

---

## 3. 프로그램 구조

```text
사용자
  ↓
argparse
  ↓
여행 날짜
  ↓
날짜 형식 검사
  ↓
Gemini API
  ↓
1차 여행 추천 JSON
  ↓
Pydantic JSON 검증
  ↓
recommended_city
  ↓
Kakao Local API
  ↓
맛집 검색 결과
  ↓
1차 추천 + 맛집 데이터
  ↓
Gemini API
  ↓
최종 Markdown 리포트
  ↓
JSON + Markdown 저장
```

---

## 4. 개발 환경

- Python 3.10 이상
- Visual Studio Code
- Gemini API
- Kakao Local API
- Git / GitHub

주요 Python 라이브러리:

- `requests`
- `python-dotenv`
- `google-genai`
- `pydantic`

---

## 5. 설치 방법

### 5-1. 프로젝트 폴더 이동

터미널에서 프로젝트 폴더로 이동합니다.

```powershell
cd travel_planner
```

프로젝트 폴더 이름이 다르면 실제 폴더 이름을 사용하세요.

---

### 5-2. 가상환경 생성

```powershell
python -m venv .venv
```

---

### 5-3. 가상환경 활성화

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

정상적으로 활성화되면 터미널 앞에 다음과 비슷한 표시가 나타납니다.

```text
(.venv) PS C:\...\travel_planner>
```

---

### 5-4. 필요한 라이브러리 설치

```powershell
pip install requests python-dotenv google-genai pydantic
```

설치가 완료된 후 현재 환경의 라이브러리 목록을 저장하려면 다음 명령을 사용합니다.

```powershell
pip freeze > requirements.txt
```

---

## 6. API 키 설정

프로젝트 폴더에 `.env` 파일을 생성합니다.

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
KAKAO_REST_API_KEY=YOUR_KAKAO_REST_API_KEY
```

`YOUR_GEMINI_API_KEY`와 `YOUR_KAKAO_REST_API_KEY` 부분에는 실제 발급받은 API 키를 입력합니다.

### 중요

실제 API 키를 Python 코드에 직접 작성하지 않습니다.

또한 `.env` 파일은 GitHub에 업로드하면 안 됩니다.

---

## 7. `.gitignore` 설정

프로젝트 폴더의 `.gitignore` 파일에는 최소한 다음 내용을 포함합니다.

```text
.env
.venv/
__pycache__/
*.pyc
```

`.env`에는 API 키가 들어 있으므로 GitHub에 공개되지 않도록 반드시 제외해야 합니다.

---

## 8. 실행 방법

가상환경을 활성화한 상태에서 다음 명령을 실행합니다.

```powershell
python travel_planner.py --date 2026-03-15
```

정상 실행 시 다음 3단계가 진행됩니다.

```text
[1/3] Gemini 여행지 추천
[2/3] Kakao 맛집 검색
[3/3] 최종 여행 리포트
```

실행이 완료되면 다음과 같은 결과 파일이 생성됩니다.

```text
results/
├── 2026-03-15_travel_data.json
└── 2026-03-15_travel_plan.md
```

---

## 9. 진행 로그

프로그램은 각 단계의 진행 상황을 화면에 표시합니다.

예:

```text
========================================
       AI 여행 플래너
========================================
여행 날짜: 2026-03-15
✅ 날짜 형식이 올바릅니다.

[1/3] Gemini 여행지 추천
  - API 호출 중...
  - 1차 JSON 요청 중...
  - JSON 응답 검증 중...
  - ✅ JSON 파싱 및 검증 성공
  - 추천 지역: 전주

[2/3] Kakao 맛집 검색
  - 검색 지역: 전주
  - API 호출 중...
  - ✅ 맛집 5곳 검색 완료

[3/3] 최종 여행 리포트
  - Gemini에게 여행 데이터 전달 중...
  - Markdown 생성 중...
  - ✅ 최종 리포트 생성 완료
  - JSON 저장 완료
  - Markdown 저장 완료

========================================
🎉 AI 여행 플래너 실행 완료!
========================================
```

---

## 10. 에러 처리

프로그램은 다음과 같은 오류 상황을 처리합니다.

| 오류 상황 | 처리 방법 |
|---|---|
| 잘못된 날짜 형식 | 오류 메시지 출력 후 종료 |
| Gemini API 키 없음 | 오류 메시지 출력 후 종료 |
| Gemini 클라이언트 생성 오류 | 오류 기록 후 종료 |
| Gemini 요청 또는 JSON 파싱 실패 | 1회 재요청 |
| JSON 재요청도 실패 | 오류 기록 후 종료 |
| Kakao API 키 없음 | 맛집 없이 다음 단계 진행 |
| Kakao 네트워크/API 요청 오류 | 오류 기록 후 다음 단계 진행 |
| Kakao 응답 JSON 처리 오류 | 오류 기록 후 다음 단계 진행 |
| Kakao 검색 결과 0건 | 빈 데이터로 다음 단계 진행 |
| 최종 리포트 생성 오류 | 지금까지의 여행 데이터를 JSON으로 저장 |

오류 정보는 JSON 파일의 `errors` 항목에 저장됩니다.

예:

```json
{
    "errors": [
        {
            "step": "kakao_restaurant_search",
            "type": "REQUEST_ERROR",
            "message": "오류 내용"
        }
    ]
}
```

---

## 11. 테스트 방법

미션에서 제시한 테스트 기준에 따라 다음 항목을 확인합니다.

### 테스트 1 — 정상 실행

```powershell
python travel_planner.py --date 2026-03-15
```

확인 사항:

- Gemini 추천 성공
- JSON 검증 성공
- Kakao 맛집 검색
- 최종 Markdown 리포트 생성
- JSON 저장
- Markdown 저장

---

### 테스트 2 — 잘못된 날짜

```powershell
python travel_planner.py --date abc
```

다음과 같은 메시지가 나와야 합니다.

```text
❌ 잘못된 날짜 형식입니다.
예시: 2026-03-15
```

---

### 테스트 3 — Gemini API 키 없음

`.env`의 Gemini 키를 임시로 비웁니다.

```text
GEMINI_API_KEY=
```

다시 실행합니다.

```powershell
python travel_planner.py --date 2026-03-15
```

API 키 오류가 표시되고 오류 데이터가 JSON으로 저장되는지 확인합니다.

테스트가 끝나면 반드시 실제 API 키를 다시 복구합니다.

---

### 테스트 4 — Kakao API 오류

Kakao API 키를 임시로 잘못 입력합니다.

```text
KAKAO_REST_API_KEY=wrong_key
```

실행 후 다음 단계인 최종 리포트 생성까지 진행되는지 확인합니다.

```text
[2/3] Kakao 맛집 검색
  - ⚠️ Kakao API 또는 검색 처리 중 문제가 발생했습니다.
  - 맛집 데이터 없이 계속 진행합니다.

[3/3] 최종 여행 리포트
```

테스트가 끝나면 Kakao API 키를 원래 값으로 복구합니다.

---

### 테스트 5 — 검색 결과 0건

Kakao 검색 결과가 없는 상황에서 프로그램이 종료되지 않고 최종 리포트 단계까지 진행되는지 확인합니다.

```text
검색된 맛집이 없습니다.
맛집 데이터 없이 계속 진행합니다.
```

---

## 12. 결과 데이터 구조

정상 실행 시 JSON 결과는 다음과 같은 구조입니다.

```json
{
    "date": "2026-03-15",
    "recommendation": {
        "recommended_city": "추천 지역",
        "weather": "예상 날씨",
        "events": [
            "행사 또는 축제"
        ],
        "reason": "추천 이유"
    },
    "places": [
        {
            "name": "맛집 이름",
            "address": "주소",
            "category": "분류",
            "url": "URL",
            "x": "좌표",
            "y": "좌표"
        }
    ],
    "errors": []
}
```

오류가 발생한 경우 `errors` 배열에 단계, 오류 유형, 메시지가 저장됩니다.

---

## 13. 보안 주의사항

API 키는 Python 코드에 직접 작성하지 않습니다.

`.env` 파일에 저장하고 `python-dotenv`를 이용해 환경변수로 불러옵니다.

다음 파일은 GitHub에 공개하지 않도록 합니다.

```text
.env
.venv/
```

GitHub에 올리기 전에 반드시 다음 명령으로 상태를 확인합니다.

```powershell
git status
```

`.env`가 Git에 추적되고 있다면 업로드를 중단하고 `.gitignore` 설정을 확인합니다.

---

## 14. GitHub 업로드

Git 상태를 먼저 확인합니다.

```powershell
git status
```

변경 사항을 추가합니다.

```powershell
git add .
```

다시 상태를 확인합니다.

```powershell
git status
```

커밋합니다.

```powershell
git commit -m "Complete AI travel planner"
```

GitHub의 `main` 브랜치로 업로드합니다.

```powershell
git push origin main
```

업로드 전에 `.env`가 포함되지 않았는지 반드시 확인합니다.

---

## 15. 프로젝트 폴더 구조

최종적으로 다음과 같은 구조를 권장합니다.

```text
travel_planner/
│
├── travel_planner.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
│
└── results/
    ├── 2026-03-15_travel_data.json
    └── 2026-03-15_travel_plan.md
```

`.env`는 로컬 환경에서만 사용하고 GitHub에는 업로드하지 않습니다.

---

## 16. 프로젝트 전체 실행 흐름

```text
① 여행 날짜 입력
        ↓
② 날짜 형식 검사
        ↓
③ Gemini 1차 여행지 추천
        ↓
④ JSON 구조화 및 Pydantic 검증
        ↓
⑤ JSON 파싱 실패 → 1회 재요청
        ↓
⑥ recommended_city 추출
        ↓
⑦ Kakao 맛집 검색
        ↓
⑧ Kakao 오류 또는 검색 결과 0건
   → 맛집 데이터 없이 계속 진행
        ↓
⑨ 추천 정보 + 맛집 정보 통합
        ↓
⑩ Gemini 최종 여행 리포트 생성
        ↓
⑪ 여행 데이터 JSON 저장
        ↓
⑫ Markdown 리포트 저장
        ↓
⑬ 테스트
        ↓
⑭ README 작성
        ↓
⑮ GitHub 업로드
```

---

## 17. 학습한 내용

이 프로젝트를 통해 다음 과정을 학습할 수 있습니다.

- Python CLI 프로그램 작성
- `argparse`를 이용한 명령줄 인자 처리
- 날짜 형식 검증
- Gemini API 호출
- Pydantic을 이용한 구조화된 JSON 검증
- JSON 파싱 실패 시 재요청
- Kakao Local API 호출
- 여러 API의 결과 통합
- API 오류 및 네트워크 오류 처리
- 진행 로그 작성
- JSON 데이터 저장
- Markdown 리포트 저장
- `.env`를 이용한 API 키 관리
- `.gitignore`를 이용한 민감 정보 보호
- Git과 GitHub를 이용한 프로젝트 관리

---

## 18. 주의사항

이 프로젝트의 Gemini 모델명과 API 호출 방식은 현재 프로젝트에서 사용하도록 작성된 코드를 기준으로 합니다.

실행 환경의 `google-genai` 버전이나 사용 가능한 Gemini 모델 설정에 따라 API 호출 오류가 발생할 수 있습니다. 그런 경우 설치된 라이브러리 버전과 API 콘솔의 사용 가능한 모델 설정을 확인해야 합니다.

또한 날씨와 행사 정보는 Gemini가 생성한 추천 정보이므로 실제 여행 전에 공식 관광·행사 정보와 날씨 정보를 별도로 확인하는 것이 좋습니다.
