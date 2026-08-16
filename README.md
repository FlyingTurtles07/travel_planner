# travel_planner

### 1. 가상환경 만들기
VScode에서 터미널을 열고 " python -m venv .venv " 입력 --> 프로젝트 폴더 안에 " .venv " 폴더 생김
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












---
---








