# CIA_Project ☣️ ![Static Badge](https://img.shields.io/badge/version-0.0.1-blue)

> **_Organized crime constitutes nothing less than a guerilla war against society._**
>  _- Lyndon B. Johnson -_


  _**"우리는 범죄를 지양하고, 정의를 지향한다."**_ ㅡ 
  **K-Shield Junior 13th CIA_TEAM & ws1004.**



## MariaDB Setting 🔏

해당 도구를 사용하고자 하는 PC에서는 **`ID: root / pw: root`** 계정으로 MariaDB 설치를 해야합니다.

현재 이 Repository의 코드는 **MariaDB 10.11** 이상에서 올바르게 동작합니다.


## How Can I ‘pip install’? 👀

Just run your code ㅡ 😎
```powershell
python .\run.py
```

**수사관의 편의성**을 고려해, CIA_PROJECT™ 최상위 디렉토리에서 `run.py`를 실행하면 자동으로 pip install을 먼저 진행합니다. 

CIA_PROJECT SHELL™이 동작하기 위한 모든 필요한 모듈들이 설치됩니다. 
자세한 모듈들의 목록은 `requirements.txt`를 참조하십시오.


## Data_Crawling_Bot 🔎

Google에서 지정한 검색어에 대한 결과 텍스트들을 대량으로 모아오는 도구입니다. 

  1) 사용자가 직접 검색어를 입력하여 검색하거나 - 

  2) CIA_TEAM이 미리 정리해둔 한국 마약 카테고리 분야 500여 개의 `user_search_query.txt`를 이용하여 자동 대량 검색이 가능합니다. 

크롤링해온 데이터는 우선 MariaDB에 저장되며, 이후 유해 게시물 계정 추출 작업을 위해 `updated_search_results.xlsx`, `suspiciousID.db`등으로 변환한 뒤, Telegram_Search_bot에 데이터를 넘겨줍니다. 


♻️ 동작 순서는 `google_crawlbot` → `csv_to_clean` → `ExtractID` → `csv_to_sqldb` 로 진행되며, 만약 각 동작을 따로 진행하고 싶다면 아래와 같이 Shell에서 명령을 입력합니다. 


예를 들어,  Data_Crawling_bot 디렉토리로 진입 후,

```powershell
python .\google_crawlbot.py
```

**[Used Engine]** : **BeautifulSoup** + **Selenium** Combined.


## CIA-Bert Model 👾

기존 영어로 구성된 Bert 모델과는 달리, CIA_TEAM이 직접 구현한 **한국어 특화** **마약 유해 게시물 탐지 Text-Classification Model**입니다. 

CIA_TEAM이 한땀한땀 정성껏 2주 동안 수작업(!)한 **4,000여 개의 마약 유해 및 무해 게시물 Dataset**을 바탕으로 학습하였습니다. 

`CIABert_Korean_Drug_classification_model.pth` 형태로 디렉토리 내에 저장되어 있으며, 필요한 경우 이 모델을 추가 학습시키거나, 충분한 성능을 낸다고 판단될 경우 그대로 사용하셔도 됩니다. 


> **[Base Model]** : **kykim/bert-kor-base** 

https://huggingface.co/kykim/bert-kor-base

> **CIA-Bert™ 성능 분석 보고서** :

https://api.wandb.ai/links/jjuny1-h3ind33r/xi8m3fd5


## Telegram_Search_Bot 📲 


CIA-Bert Model™의 판단에 따라 필터링된 유해 게시물에 대하여, 마약 판매 Telegram 계정이라고 의심되는 **ID 텍스트를 추가로 필터링**합니다. 

이후, 직접 Telegram 개발자 API를 이용하여 대화 및 공지방 아카이빙을 진행합니다. 

이 때, Export Data 기능이 지원되는 Desktop Telegram은 물론, **미디어 파일 보호 기능이 활성화 되어있는** 대화방의 미디어, 대화, ID, 계정 목록 등을 모두 아카이빙합니다. 

이것이 CIA_PROJECT™ 도구만이 가지는 특장점이라고 할 수 있겠습니다. 

다만, 수사관이 직접 Telegram에 가입하여 개발자 api를 획득한 상태인 경우를 상정합니다.


이후, 의심 유해 계정에 대한 분석이 모두 마치고 나면, **범죄 수사에 필요한 관련 크롤링 데이터 및 Site Status(**🟢Alive**/**🔴Dead**/**🟡Unknown**), 마지막 수정 기록, 의심 계정이 모두 일목요연하게 분석된 최종 분석 DB**가 완성됩니다. 


> 자세한 프로젝트 특장점 기술 보고서는 다음 문서를 참조하십시오:

[Comparison between Original_Telegram_ExportData_feature vs CIA_Project.docx](https://github.com/user-attachments/files/17280290/Comparison.between.Original_Telegram_ExportData_feature.vs.CIA_Project.docx)

♻️ 동작 순서는 `create_DB` → `configure` → `channel` → `message` → `telegram_to_html` 로 진행되며, 만약 각 동작을 따로 진행하고 싶다면 마찬가지로 아래와 같이 Shell에서 명령을 입력합니다. 

예를 들어, Telegram_Search_bot 디렉토리로 진입 후, 

```powershell
python .\telegram_to_html.py
```

이후, 모든 동작이 완료되면, **`/Telegram_Search_Bot/result`** 디렉토리에, 아카이빙된 대화방이 한눈에 보이는 `.html`, 각 대화를 엑셀로 정리한 `.xslx`, 미디어 파일만 따로 모은 `media` 디렉토리로 정리되어 있습니다. 정리된 html 생성 예시는 아래와 같습니다. 

### 최종 추출된 html 파일 예시 🚨

![스크린샷 2024-10-07 234120](https://github.com/user-attachments/assets/307661cf-3a0c-4a1e-a89a-c23541c106f0)
