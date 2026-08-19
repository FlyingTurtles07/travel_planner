# travel_planner

---

## 0. API 발급 전 기본 셋팅하기 

### 1. 가상환경 만들기
VScode에서 터미널을 열고 " python -m venv .venv " 입력 --> 프로젝트 폴더 안에 " .venv " 폴더 생김

> 만약 안된다면 " python -m venv .venv " 대신 " py -m venv .venv " 쓰면 됨
> 확인 방법은 " python --version "  안먹히면 위에 명령도 안먹힘, 이렇게 " py --version " 해봐서 되면 위희 py명령어 사용 하면 됨


### 2. 가상환경 활성화
C:\Users\moon7\Desktop\travel_planner\.venv\Scripts 안에서 " activate " 입력하면
  ---> 실행 안되다가 PowerShell Extension v2025.4.0 설치 할꺼냐고 나오고 ---> 설치하면

터미널이 새로운 PowerShell 열리면서
```
PowerShell Extension v2025.4.0
Copyright (c) Microsoft Corporation.

https://aka.ms/vscode-powershell
Type 'help' to get help.

PS C:\Users\moon7\Desktop\travel_planner> (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\Users\moon7\Desktop\travel_planner\.venv\Scripts\Activate.ps1)
(.venv) PS C:\Users\moon7\Desktop\travel_planner>
```
이렇게 변함

### 3. 라이브러리 설치
터미널에서 --> 반드시 " (.venv) PS C:\Users\moon7\Desktop\travel_planner> " 에서 입력해야 함
```
(.venv) PS C:\Users\moon7\Desktop\travel_planner> pip install requests python-dotenv openai
```
입력

그리고:

```
pip freeze > requirements.txt
```

이렇게 하면 나중에 다른 컴퓨터에서도 필요한 라이브러리를 설치할 수 있습니다.

> ⭐ 주의 사항 아주 쉽게 기억하세요

> 터미널 창에 ' >>> ' 가 보이면 터미널 명령어를 입력하면 안 됩니다. <br>
> 우선 >>> exit()만 입력해서 >>>를 없애는 것부터..... 

| 화면                   | 의미             | 입력하는 것                                 |
| -------------------- | -------------- | -------------------------------------- |
| `>>>`                | Python 실행창     | `print()`, `import` 같은 Python 코드       |
| `PS C:\...>`         | VS Code 터미널    | `python -m venv`, `pip install` 같은 명령어 |
| `(.venv) PS C:\...>` | 가상환경이 활성화된 터미널 | `pip install` 등 프로젝트 명령어               |


### 4. API 연동 미션에서는 가상환경을 만드는 단계부터 차근차근 해야함.




---
---
### * 더 자세한 보충 설명

#### 1. 라이브러리란?

쉽게 말하면 다른 사람이 미리 만들어 놓은 Python 기능 묶음입니다.

예를 들어 우리가 API를 직접 연결하려면 여러 가지 복잡한 코드를 작성해야 하는데, 다른 개발자들이 이미 만들어 놓은 라이브러리를 가져다 쓰면 훨씬 쉽게 할 수 있습니다.


- 이번 미션에서 설치하는 것이 바로 아래 3가지 입니다.

① requests     ---> "requests = 다른 API에 요청 보내기"

인터넷으로 API에 요청을 보내기 위한 도구입니다.

예를 들어 우리가 지도 API나 관광 API에

"이 지역의 관광지 정보를 주세요." 라고 요청하려면 인터넷을 통해 요청을 보내야 합니다.

그때 python프로그램에서 아래처럼 requests를 사용.

```
import requests
```


② python-dotenv     ---> "python-dotenv = .env 파일에 저장한 비밀 정보 가져오기"

API를 사용할 때 API 키라는 비밀번호 같은 정보를 사용하는 경우가 많습니다.

예를 들어 : OPENAI_API_KEY=xxxxxxxxxxxxxxxx

이런 정보를 Python 코드에 직접 적어버리면 보안상 좋지 않습니다.

그래서 .env라는 파일에 넣어두고 Python에서 가져오는 방법을 사용합니다.

이때 python-dotenv가 필요합니다.

```
from dotenv import load_dotenv
```

③ openai     ---> openai = Python에서 OpenAI API 사용하기

이번 미션에서 OpenAI API를 사용하기 위한 라이브러리입니다.

예를 들어 Python 프로그램에서 AI에게

"이 여행지에 대한 여행 코스를 추천해줘."

라고 요청하려면 OpenAI API와 연결해야 합니다.

그때 사용하는 것이 openai입니다.

```
from openai import OpenAI
```

> (.venv) PS C:\Users\moon7\Desktop\travel_planner> pip install requests python-dotenv openai
> " pip install requests python-dotenv openai " 는
> ---> "Python아, requests, python-dotenv, openai 필요한 3가지 도구를 다운로드해서 설치해줘." 라는 명령임
```
Collecting requests
  Downloading requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
Collecting python-dotenv
  Downloading python_dotenv-1.2.2-py3-none-any.whl.metadata (27 kB)
Collecting openai
  Downloading openai-3.1.0-py3-none-any.whl.metadata (39 kB)
  ```

#### 2. 가상환경 .venv를 먼저 만든 이유?

---> 이번 프로젝트만을 위한 별도의 Python 작업 공간을 만드는 것 <br>
     프로젝트마다 필요한 라이브러리와 버전이 다를 수 있기 때문에 프로젝트마다 
     " .venv "라는 독립된 가상환경을 만들어 사용 해야 함.

```
python -m venv .venv
```
#### 3. 과정을 간단하게 나타내면

```
내 컴퓨터
│
├─ Python
│
└─ 여행 API 프로젝트
     │
     └─ .venv  ← 이 프로젝트 전용 작업공간
          │
          ├─ requests
          ├─ python-dotenv
          └─ openai


Python 프로그램
      │
      ├── requests ─────→ 관광/지도 API
      │
      ├── python-dotenv ─→ API 키
      │
      └── openai ───────→ OpenAI API
```



---



## 1. 전체 구조 잡기

### 날짜 → AI 지역 추천 → 추천 지역을 지도 API에 전달 → 맛집 검색 → 다시 AI에게 전달 → 여행 리포트 생성

```
사용자
  │
  │ -date "2026-03-15"
  ▼
① Python CLI
  │
  ▼
② LLM API
  │
  │ 날짜를 전달
  │
  ▼
[1차 추천 JSON]
  ├─ recommended_city
  ├─ weather
  ├─ events
  └─ reason
       │
       │ recommended_city 전달
       ▼
③ 지도/장소 API
       │
       ▼
[맛집 검색 결과]
  ├─ name
  ├─ address
  ├─ category
  ├─ url
  ├─ x
  └─ y
       │
       │ 1차 추천 + 맛집
       ▼
④ LLM API
       │
       ▼
⑤ 최종 여행 리포트
       │
       ├─ JSON 저장
       └─ Markdown 저장
```

## 2. 전체 폴더 구조 및 각 파일의 역할

```
travel-planner/
│
├─ travel_planner.py
├─ .env
├─ .gitignore
├─ README.md
├─ requirements.txt
│
└─ results/
   ├─ 2026-03-15_travel_data.json
   └─ 2026-03-15_travel_plan.md
```

| 파일                  | 역할                          |
| ------------------- | --------------------------- |
| `travel_planner.py` | 메인 Python 프로그램              |
| `.env`              | API 키 보관                    |
| `.gitignore`        | `.env`가 GitHub에 올라가지 않도록 차단 |
| `README.md`         | 프로그램 설명서                    |
| `requirements.txt`  | 필요한 Python 라이브러리            |
| `results/`          | 실행 결과 저장                    |
| `.json`             | API 원본/구조화 데이터              |
| `.md`               | 최종 여행 리포트                   |

> 중요: .env는 GitHub에 절대 올리면 안됨

---

## 3. API키 준비

### 1. travel_planner에 추가
```
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
kakao_api_key = os.getenv("KAKAO_REST_API_KEY")
```

### 2. .gitignore 만들고 내용 추가  --> .env 반드시 추가해야 함

```
.env
.venv/
__pycache__/
```


### 3. 프로젝트 폴더 (travel_planner) 한번 push 후 .env 만들고 내용 만들기
> .ignore랑 같이 만들어 놓고 push하면 gitHub에 올라가 버릴수 있음... 곤란해짐....(실제 키 넣고 push시 보안에 걸려 안올라가지기도 함)
```
OPENAI_API_KEY=실제키
KAKAO_REST_API_KEY=실제키
```

### 4. 시작 전에 결정할 것 (5분)

LLM API: Gemini <br>
장소 API: Kakao Local

> LLM API: OpenAI vs Gemini 중 1개 선택 (계정 있는 쪽, 또는 무료 크레딧 있는 쪽)

> 장소 API: Kakao Local vs Naver Local Search 중 1개 선택 (Kakao가 문서/커뮤니티 자료 많아서 초보자에게 편함)

> 이 선택에 따라 필요한 API 키 발급 사이트가 다르니, 이걸 제일 먼저 정해야 다음 단계(키 발급)로 넘어갈 수 있어요.



- Gemini API 키 발급 (Google AI Studio)
https://aistudio.google.com/app/apikey  (바로접속)

https://aistudio.google.com 접속 → Google 계정으로 로그인
화면 좌측 사이드바 하단 도큐멘트 누르니 아래로 이동 
API 키 관리 페이지로 이동 → "API 키 만들기(Create API key)" 버튼 클릭
연결할 Google Cloud 프로젝트를 선택하는 창이 뜨는데, 기존 프로젝트가 없으면 "새 프로젝트 만들기"를 눌러 하나 생성
몇 초 뒤 AQAb...로 시작하는 키가 발급됨 → 바로 복사해서 메모장에 저장
참고로 새로 발급한 키는 자동으로 **"승인 키(Auth key)"**로 생성되므로 별도 설정 없이 그대로 쓰면 됩니다.
무료 티어(분당/일일 요청 제한 있음)로 바로 테스트 가능 — 별도 결제 등록 없이도 시작 가능

💡 Gemini는 이 미션 수준(테스트용 호출 몇 번)에서는 무료 티어만으로 충분해서, "결제 등록"이라는 진입 장벽이 없다는 게 초보자 입장에서 가장 큰 장점입니다.

- 코드에서 라이브러리 설치:
```
pip install google-genai
```
설치 결과 :  
```
(.venv) PS C:\Users\swedu18\Desktop\travel_planner> pip install google-genai
Collecting google-genai
  Downloading google_genai-2.18.1-py3-none-any.whl.metadata (56 kB)
Requirement already satisfied: anyio<5.0.0,>=4.8.0 in .\.venv\Lib\site-packages (from google-genai) (4.14.2)
Collecting google-auth<3.0.0,>=2.56.0 (from google-auth[requests]<3.0.0,>=2.56.0->google-genai)
  Downloading google_auth-2.56.3-py3-none-any.whl.metadata (6.0 kB)
Collecting httpx<1.0.0,>=0.28.1 (from google-genai)
  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Requirement already satisfied: pydantic<3.0.0,>=2.12.5 in .\.venv\Lib\site-packages (from google-genai) (2.13.4)
Requirement already satisfied: requests<3.0.0,>=2.28.1 in .\.venv\Lib\site-packages (from google-genai) (2.34.2)
Collecting tenacity<9.2.0,>=8.2.3 (from google-genai)
  Downloading tenacity-9.1.4-py3-none-any.whl.metadata (1.2 kB)
Collecting websockets<17.0,>=13.0.0 (from google-genai)
  Downloading websockets-16.1.1-cp314-cp314-win_amd64.whl.metadata (7.0 kB)
Requirement already satisfied: typing-extensions<5.0.0,>=4.14.0 in .\.venv\Lib\site-packages (from google-genai) (4.16.0)
Requirement already satisfied: distro<2,>=1.7.0 in .\.venv\Lib\site-packages (from google-genai) (1.9.0)
Requirement already satisfied: sniffio in .\.venv\Lib\site-packages (from google-genai) (1.3.1)
Requirement already satisfied: idna>=2.8 in .\.venv\Lib\site-packages (from anyio<5.0.0,>=4.8.0->google-genai) (3.18)
Collecting pyasn1-modules>=0.2.1 (from google-auth<3.0.0,>=2.56.0->google-auth[requests]<3.0.0,>=2.56.0->google-genai)
  Downloading pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)
Collecting cryptography>=41.0.5 (from google-auth<3.0.0,>=2.56.0->google-auth[requests]<3.0.0,>=2.56.0->google-genai)
  Downloading cryptography-50.0.0-cp311-abi3-win_amd64.whl.metadata (4.3 kB)
Requirement already satisfied: certifi in .\.venv\Lib\site-packages (from httpx<1.0.0,>=0.28.1->google-genai) (2026.7.22)
Collecting httpcore==1.* (from httpx<1.0.0,>=0.28.1->google-genai)
  Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Requirement already satisfied: h11>=0.16 in .\.venv\Lib\site-packages (from httpcore==1.*->httpx<1.0.0,>=0.28.1->google-genai) (0.16.0)
Requirement already satisfied: annotated-types>=0.6.0 in .\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.12.5->google-genai) (0.8.0)
Requirement already satisfied: pydantic-core==2.46.4 in .\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.12.5->google-genai) (2.46.4)
Requirement already satisfied: typing-inspection>=0.4.2 in .\.venv\Lib\site-packages (from pydantic<3.0.0,>=2.12.5->google-genai) (0.4.4)
Requirement already satisfied: charset_normalizer<4,>=2 in .\.venv\Lib\site-packages (from requests<3.0.0,>=2.28.1->google-genai) (3.5.1)
Requirement already satisfied: urllib3<3,>=1.26 in .\.venv\Lib\site-packages (from requests<3.0.0,>=2.28.1->google-genai) (2.7.0)
Collecting cffi>=2.0.0 (from cryptography>=41.0.5->google-auth<3.0.0,>=2.56.0->google-auth[requests]<3.0.0,>=2.56.0->google-genai)
  Downloading cffi-2.1.1-cp314-cp314-win_amd64.whl.metadata (2.6 kB)
Collecting pycparser (from cffi>=2.0.0->cryptography>=41.0.5->google-auth<3.0.0,>=2.56.0->google-auth[requests]<3.0.0,>=2.56.0->google-genai)
  Downloading pycparser-3.0-py3-none-any.whl.metadata (8.2 kB)
Collecting pyasn1<0.7.0,>=0.6.1 (from pyasn1-modules>=0.2.1->google-auth<3.0.0,>=2.56.0->google-auth[requests]<3.0.0,>=2.56.0->google-genai)
  Downloading pyasn1-0.6.4-py3-none-any.whl.metadata (8.4 kB)
Downloading google_genai-2.18.1-py3-none-any.whl (1.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 8.5 MB/s  0:00:00
Downloading google_auth-2.56.3-py3-none-any.whl (259 kB)
Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
Downloading tenacity-9.1.4-py3-none-any.whl (28 kB)
Downloading websockets-16.1.1-cp314-cp314-win_amd64.whl (179 kB)
Downloading cryptography-50.0.0-cp311-abi3-win_amd64.whl (3.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.8/3.8 MB 10.4 MB/s  0:00:00
Downloading cffi-2.1.1-cp314-cp314-win_amd64.whl (187 kB)
Downloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
Downloading pyasn1-0.6.4-py3-none-any.whl (84 kB)
Downloading pycparser-3.0-py3-none-any.whl (48 kB)
Installing collected packages: websockets, tenacity, pycparser, pyasn1, httpcore, pyasn1-modules, httpx, cffi, cryptography, google-auth, google-genai
Successfully installed cffi-2.1.1 cryptography-50.0.0 google-auth-2.56.3 google-genai-2.18.1 httpcore-1.0.9 httpx-0.28.1 pyasn1-0.6.4 pyasn1-modules-0.4.2 pycparser-3.0 tenacity-9.1.4 websockets-16.1.1
(.venv) PS C:\Users\swedu18\Desktop\travel_planner>
```




### 5. API 키 발급 & 보안 설정 (가장 먼저 해야 할 실질적 작업)
선택한 LLM API 키 발급 (Google AI Studio) <br>
선택한 장소 API 키 발급 (Kakao Developers)

> 선택한 LLM API 키 발급 (OpenAI platform 또는 Google AI Studio)

> 선택한 장소 API 키 발급 (Kakao Developers 또는 Naver Developers)

> python-dotenv 설치 후 os.getenv()로 키 불러오는 테스트 코드 작성

> 이 단계에서 키가 제대로 로드되는지 print(len(key)) 정도로만 확인하고 절대 키 자체를 출력하지 않기


- Kakao Local API 키 발급 (Kakao Developers)
https://developers.kakao.com 접속 → 카카오 계정으로 로그인
상단 메뉴 "내 애플리케이션" 클릭
"애플리케이션 추가하기" 버튼 클릭
앱 이름(예: 여행플래너), 사업자명(개인이면 본인 이름/닉네임)을 입력하고 저장
생성된 앱 카드를 클릭해서 상세 페이지로 이동
좌측 메뉴에서 "앱 키" 탭 클릭
여러 키(네이티브 앱 키, REST API 키, JavaScript 키, Admin 키)가 보이는데, 우리가 쓸 건 "REST API 키" — 이걸 복사

⚠️ 참고: 최근 카카오는 보안 강화를 위해 REST API 키에 "클라이언트 시크릿(client secret)" 기능이 기본 활성화되어 함께 생성됩니다. 하지만 이건 카카오 로그인(사용자 인증) 기능을 쓸 때만 필요하고, 우리가 쓸 Local(장소 검색) API는 REST API 키만 헤더에 넣으면 되고 client secret은 필요 없습니다. 그러니 지금은 무시하고 넘어가도 됩니다.

왼쪽 메뉴의 "플랫폼" 설정은 웹/앱 URL을 등록하는 곳인데, 우리는 서버(터미널)에서만 직접 호출하므로 이 단계는 건너뛰어도 됩니다.
Local API는 별도 심사나 신청 없이 REST API 키만 있으면 바로 호출 가능합니다.


### 6. 테스트 호출 한 번 해보기

키를 발급받자마자 코드를 짜기 전에, 브라우저나 터미널에서 키가 진짜 작동하는지 먼저 확인하는 습관을 들이면 나중에 디버깅 시간이 훨씬 줄어듭니다.

- Kakao 키 테스트 (터미널에 바로 붙여넣기, 본인 키로 교체):

```
curl -v -G GET "https://dapi.kakao.com/v2/local/search/keyword.json" \
  --data-urlencode "query=제주 맛집" \
  -H "Authorization: KakaoAK 여기에_본인_REST_API_키"
```

→ JSON 형태로 장소 목록이 쭉 뜨면 성공, 401이 뜨면 키를 잘못 복사했거나 앱이 제대로 생성 안 된 것입니다.

- Gemini 키 테스트 (Python으로):

```
from google import genai

client = genai.Client(api_key="여기에_본인_키")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="안녕? 한 문장으로 인사해줘"
)
print(response.text)
```

→ 정상 응답 텍스트가 뜨면 성공입니다.

---

## 4. travel_planner.py 기본 틀 짜기

```
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
```

- test 결과 :
  1. 정상 작동
입력 : 
```
 python travel_planner.py --date "2026-03-15"
```
결과 :
```
========================================
       AI 여행 플래너
========================================
여행 날짜: 2026-03-15
✅ 날짜 형식이 올바릅니다.
다음 단계로 진행합니다.
```
  2. 잘못된 날짜 입력 확인
입력 1 :
```
python travel_planner.py --date "abc"
```
입력 2 :
```
python travel_planner.py --date "2026/03/15"
```

결과 :
```
❌ 잘못된 날짜 형식입니다.
예시: 2026-03-15
```

```
(.venv) PS C:\Users\swedu18\Desktop\travel_planner> python travel_planner.py --date "2026-0
========================================
       AI 여행 플래너
========================================
여행 날짜: 2026-03-15
✅ 날짜 형식이 올바릅니다.
다음 단계로 진행합니다.
(.venv) PS C:\Users\swedu18\Desktop\travel_planner> python travel_planner.py --date "abc"
❌ 잘못된 날짜 형식입니다.
예시: 2026-03-15
(.venv) PS C:\Users\swedu18\Desktop\travel_planner> python travel_planner.py --date "2026/03/15"
❌ 잘못된 날짜 형식입니다.
예시: 2026-03-15
```
<img width="694" height="282" alt="기본 프로그램 실행 결과 캡쳐" src="https://github.com/user-attachments/assets/85f34eb7-9ab6-439a-9cd7-765f3f8e484b" />


## 5. OpenAI API 단독 테스트??? ---> Gemini API 키 발급 받고, pip install google-genai 설치하고 OpenAI용으로 잘못 짜서 5.1에서 Gemini API로 변경 함
OpenAI() 클라이언트를 만들고 responses.create()로 호출하는 방식으로

1. 기본구조 
```
날짜 입력
   ↓
CLI
   ↓
OpenAI API
   ↓
AI 응답
   ↓
터미널 출력
```

### 1. .env 에 키 넣기

```
OPENAI_API_KEY=여기에_본인의_API_키
```
> 주의 ) 실제 API 키는 나에게 보내지 마.

### 2. .gitignore 확인
그리고 .gitignore 확인 반드시 있어야 할 내용:
```
.env
.venv/
__pycache__/
```

### 3. travel_planner.py 다음과 같이 수정

```
import argparse
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


def validate_date(date_string):
    """날짜 형식이 YYYY-MM-DD인지 확인"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_travel_recommendation(date):
    """OpenAI API를 이용해 여행지를 추천받는다."""

    # .env 파일의 환경변수 불러오기
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    # API 키가 없는 경우
    if not api_key:
        print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하세요.")
        return None

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=api_key)

    prompt = f"""
{date}에 국내 여행을 간다고 가정하고,
여행하기 좋은 지역 하나를 추천해주세요.

다음 내용을 포함해서 간단하게 설명해주세요.

1. 추천 지역
2. 추천 이유
3. 예상되는 여행 분위기
"""

    try:
        response = client.responses.create(
            model="gpt-5.6",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        print("❌ OpenAI API 호출 중 오류가 발생했습니다.")
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

    # OpenAI API 호출
    print("[1/3] 여행지 추천 생성 중(LLM)...")

    recommendation = get_travel_recommendation(args.date)

    if recommendation is None:
        return

    print()
    print("===== AI 여행 추천 결과 =====")
    print(recommendation)


if __name__ == "__main__":
    main()
```

> 포인트 1. .env에서 API 키 가져오기
> .env --> OPENAI_API_KEY --> Python

```
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

> 포인트 2. OpenAI 연결
```
client = OpenAI(api_key=api_key)
```
여기서 OpenAI API를 사용할 준비를 하는 거야.


> 포인트 3. 실제 API 호출 (핵심)
> Python --> OpenAI API 요청 --> gEMINI --> 응답
 ```
response = client.responses.create(
    model="gpt-5.6",
    input=prompt
)
```

> 포인트 4. AI가 보내준 텍스트 꺼내기
```
return response.output_text
```
그래서 최종적으로:
```
recommendation = get_travel_recommendation(args.date)
```
에 AI의 답변이 들어가게 돼.


## 5.1 Gemini API로 변경 

```
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

```

PowerShell 실행 결과

```
(.venv) PS C:\Users\swedu18\Desktop\travel_planner> python travel_planner.py --date "2026-03-15"
========================================
       AI 여행 플래너
========================================
여행 날짜: 2026-03-15
✅ 날짜 형식이 올바릅니다.

[1/3] 여행지 추천 생성 중(Gemini)...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.

===== AI 여행 추천 결과 =====
2026년 3월 15일 봄의 시작을 맞이하여 추천하는 국내 여행지는 **'제주도(특히 서귀포 및 남부 지역)'**입니다.

---

### 1. 추천 지역
* **제주특별자치도 서귀포시 일대** (산방산, 섭지코지, 성산일출봉 주변 등)

### 2. 추천 이유
* **가장 먼저 만나는 완연한 봄:** 3월 중순은 육지에 비해 기온이 포근하여 봄 기운을 가장 빠르게 체감할 수 있는 시기입니다.
* **유채꽃의 절정:** 이 시기 서귀포와 동부 일대는 노란 **유채꽃이 만개**하여 섬 전체가 화사하게 물듭니다.
* **여유로운 여행 가능:** 3월 말부터 시작되는 본격적인 벚꽃 시즌이나 4월 봄방학 전이라, 비교적 덜 붐비고 쾌적하게 여행을 즐길 수 있습니다.

### 3. 예상되는 여행 분위기
* **화사하고 싱그러운 분위기:** 파란 제주 바다와 대비되는 노란 유채꽃밭을 배경으로 따스한 햇살을 받으며 여행하는 화사한 분위기입니다.
* **설레고 여유로운 봄 드라이브:** 포근한 해안 바람을 맞으며 해안도로를 드라이브하고, 야외 카페 테라스에서 느긋하게 휴식을 취하는 '설렘 가득한 휴양'의 분위기를 느끼실 수 있습니다.
(.venv) PS C:\Users\swedu18\Desktop\travel_planner> 

```

## 6. Gemini 응답을 JSON으로 구조화 (가장 중요)

### 1. Pydantic 설치
```
pip install pydantic

```

### 2. 만들 JSON구조 설명 : Gemini 답변 형태 설정

```
{
    "recommended_city": "제주",
    "weather": "3월 중순은 비교적 온화한 날씨입니다.",
    "events": [
        "유채꽃 관련 행사",
        "봄꽃 축제"
    ],
    "reason": "봄꽃을 즐기기 좋고 자연 경관이 아름답기 때문입니다."
}
```

> 1차 추천 JSON의 핵심 필드인 recommended_city, weather, events, reason을 그대로 형식화 함


### 3. travel_planner.py 수정

```
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

```

> 포인트 1. 핵심 코드
```
class TravelRecommendation(BaseModel):
    recommended_city: str
    weather: str
    events: list[str]
    reason: str

```
> 포인트 2. jsom 설계도

```
TravelRecommendation
        ↓
┌──────────────────────┐
│ recommended_city     │ → 문자열
│ weather              │ → 문자열
│ events               │ → 문자열 목록
│ reason               │ → 문자열
└──────────────────────┘
```

> 포인트 3. Gemini에게 JSON 구조를 알려주는 부분 (핵심)
> "아무 말이나 하지 말고 이 구조의 JSON으로 답해." 라는 의미
```
config=types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=TravelRecommendation,
)
```
> 포인트 4. Gemini 응답을 Python 객체로 변환
```
recommendation = TravelRecommendation.model_validate_json(
    response.text
)
```
Gemini가:

{
    "recommended_city": "제주",
    "weather": "...",
    "events": [],
    "reason": "..."
}

를 보내면 Python에서:
```
recommendation.recommended_city
```
로 받고 
```
print(recommendation.recommended_city)
```
이렇게 사용하면 결과  :   "제주" 로 출력됨


실행 결과는 지금  사용자 너무 많아서 못함  0819 1:31


## 7. JSON 파싱 실패 처리



## 8. Kakao 맛집 검색 결과가 0개여도 프로그램이 죽지 않는 처리를 추가

### 1. requests 추가 
```
pip install requests 
```
### 2. .env에 kakao_REST_API 키 추가

### 3. travel_planner.py 수정

```
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

```
> 포인트 1. import os 밑에 import requests 추가 <br>
> kakao API에 인터넷 요청 보내기 위해 필요

> 포인트 2. search_restaurants() 함수 추가

Gemini가 알려준:
```
recommendation.recommended_city
```
를 받아서 :
```
city = recommendation.recommended_city

restaurants = search_restaurants(city)
```
로 kakao에 전달

" Gemini --> recommended_city --> Kakao Local API --> ○○ 지역 맛집 "

> 포인트 3. 검색 결과가 없으면 [] 반환
```
if not documents:
    print("  - 검색 결과 0건")
    print("  - 다음 단계로 진행합니다.")
    return []
```

API 자체에 문제가 생겨도 : 
```
except requests.RequestException:
    return []
```
처리 하므로 맛집 API가 실패해도 프로그램 전체가 죽지 않음
















LLM은 가끔 JSON 주변에 설명을 붙일 수 있는데 그러면 JSON파싱에 문제 발생 하기 때문에
```
try:
    ...
except:
    ...
``` 

로 처리하고 최대 1회 재요청 하도록 만든다

구조 : 
```
JSON 파싱 실패
      ↓
1회 재요청
      ↓
성공 → 진행
실패 → 오류 기록
```





















---
---








