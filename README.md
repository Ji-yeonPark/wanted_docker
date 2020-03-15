# 원티드

기간 : 2020.03.10~2020.03.16

## Run

```
$ python app/main.py
```

## Test

```
$ PYTHONPATH=app pytest tests
```

## API Recipe

1. **GET** /company/

   > parameter: name

   - 회사명 검색 자동완성 api
   - name이라는 검색어를 받아와서 한글, 영어, 일어 한번에 검색해서 회사명이 일부분이라도 존재하는 경우 반환.
   - ex) /company/?name=원
     ```
     [
       {
           "id": 1,
           "name_ko": "원티드랩",
           "name_en": "Wantedlab",
           "name_ja": ""
       },
     ]
     ```

2) **GET** /tag/

   > parameter: tag

   - 태그명으로 회사 검색.
   - 태그로 검색 관련된 회사가 검색되어야 합니다.
     - 다국어로 검색이 가능.
     - 동일한 회사는 한번만 노출(distinct)
   - ex) /tag/?tag=タグ\_6
     ```
     [
       {
           "tag": {
               "id": 68,
               "name": "タグ_6",
               "language": "JA"
           },
           "company": {
               "id": 3,
               "name_ko": "이상한마케팅",
               "name_en": "",
               "name_ja": ""
           }
       },
       {
           "tag": {
               "id": 68,
               "name": "タグ_6",
               "language": "JA"
           },
           "company": {
               "id": 17,
               "name_ko": "와이케이비앤씨",
               "name_en": "",
               "name_ja": ""
           }
       },
       ...
     ]
     ```

3) **POST** /company/<int:company_id>/

   > data: tag(int)

   - 회사 태그 정보 추가
   - 태그 id 값을 데이터로 받아와야한다.
     - 태그 테이블에 존재하는 태그만 추가가 가능.
   - ex) /company/3/
     ```
     # 데이터
     data = {
       "tag": "17"
     }
     # 결과 dataset
     {
         "tag": {
             "id": 17,
             "name": "태그_16",
             "language": "KO"
         },
         "company": {
             "id": 3,
             "name_ko": "이상한마케팅",
             "name_en": "",
             "name_ja": ""
         }
     }
     ```

4) **DELETE** /company/<int:company_id>/

   > data: tag(int)

   - 회사 태그 정보 삭제
   - 태그 id 값을 데이터로 받아와야한다.
   - ex) /company/3/
     ```
     # 데이터
     data = {
       "tag": "1"
     }
     # 결과 dataset
     Deleted
     ```
