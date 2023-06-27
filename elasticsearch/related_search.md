# 연관검색어

- 방식
  - 절차적 유사성
    - 한 검색어가 다른 검색어와 연달아 검색 된 경우
    - 로그 기반
    - 로그가 쌓여야 연관 검색어 표출이 가능
    - 연달아 검색된 로그들을 어떻게 찾을 것인지(실시간으로는 불가능)
    - 결국 별도의 저장 공간이 필요하진 않을지
    - 로그를 지금처럼 검색 단위가 아니라 세션 단위로 저장해야 할지
    - 범위를 어떻게 잡을지(app, index, 시간)
  - 의미적 유사성
    - 두 검색어의 검색어 자체의 의미가 유사한 경우
    - 크게 세 가지 방식으로 다시 나눌 수 있다.
      - 한 문서 내에서 두 검색어가 함께 등장하는 빈도(text field 대상 fielddata를 true로 주어 aggs가 가능하도록 변경?)
      - 특정 검색 결과 중 이용자들이 많이 조회한 결과의 컨텐츠로부터 연관 검색어 추출
      - 특정 질의에 대한 백과사전이나 블로그, 등의 컨텐츠로부터 연관 검색어를 추출
    - 별도의 analyzer가 필요할 듯 하다.
  - 철자적 유사성
    - 두 검색어의 철자가 유사할 경우
    - 사실상 자동완성과 크게 다르지 않음
    - 자동완성 결과를 그냥 던져주면?
  - 직접 등록
    - 별도의 저장 공간 필요.



- 절차적 유사성 구현

  - 구현
    - Search log에서 이전에 해당 term으로 검색된 문서들 검색
    - 해당 문서들의 시간을 찾아 일정 시간 내에 동일한 app_id, index_id, user_identity으로 검색한 log 검색.
    - 해당 문서들 중 임계치 이상 나타나는 term들을 연관 검색어로 추천
    - 아래에서는 dictionary를 썼지만 aggs로 집계하는 것도 괜찮을 듯 하다.
  - 위 방식의 문제
    - 시간이 오래 걸린다(100개만 대상으로 해도 100번 검색을 해야한다).

  ```python
  from datetime import datetime, timedelta
  
  from elasticsearch import Elasticsearch
  
  
  INDEX = "search-log"
  FIELD = "term.keyword"
  search_term = "강아지"
  es_client = Elasticsearch("localhost:9200")
  
  res = es_client.search(index=INDEX, query={"term":{FIELD:search_term}}, size=10)
  
  related_terms = {}
  
  for doc in res["hits"]["hits"]:
      gt = doc["_source"]["timestamp"]
      lte = datetime.strptime(gt, "%Y-%m-%dT%H:%M:%S.%f") + timedelta(hours=1)
      query = {
          "bool":{
              "filter":[
                  {
                      "range":{
                          "timestamp":{
                              "gt": gt,
                              "lte": lte
                          }
                      }
                  },
                  {
                      "term":{
                          "app_id": doc["_source"]["app_id"]
                      }
                  },
                  {
                      "term":{
                          "user_identity": doc["_source"]["user_identity"]
                      }
                  },
                  {
                      "term":{
                          "index_name": doc["_source"]["index_name"][0]
                      }
                  }
              ]
          }
      }
      adjacent_logs = es_client.search(index=INDEX, query=query, sort={"timestamp":"asc"})
  
      for log in adjacent_logs["hits"]["hits"]:
          term = log["_source"]["term"]
          if term == search_term:
              continue
          if term in related_terms:
              related_terms[term] += 1
          else:
              related_terms[term] = 1
  
  print(related_terms)
  """
  {'강아지': 2, '강아지 사진': 1, '강아지 간식': 1}
  """
  ```

  - mapping

  ```json
  PUT my-index-000001
  {
    "mappings": {
      "properties": {
        "my_join_field": { 
          "type": "join",
          "relations": {
            "question": "answer" 
          }
        }
      }
    }
  }
  
  PUT my-index-000001/_doc/234?refresh
  {
    "text": "This is a question",
    "my_join_field": {
      "name": "question" 
    }
  }
  
  PUT my-index-000001/_doc/2?routing=1&refresh 
  {
    "text": "This is an answer",
    "my_join_field": {
      "name": "answer", 
      "parent": "234" 
    }
  }
  
  PUT my-index-000001/_doc/3?routing=1&refresh 
  {
    "my_id": "3",
    "text": "This is an answer2",
    "my_join_field": {
      "name": "answer", 
      "parent": "234" 
    }
  }
  
  GET my-index-000001/_search
  {
    "query": {
      "has_child": {
        "type": "answer",
        "query": {
          "match": {
            "text": "answer"
          }
        }
      }
    },
    "aggs": {
      "to-answers": {
        "children": {
          "type": "answer"
        },
        "aggs": {
          "top-names": {
            "terms": {
              "field": "text.keyword",
              "size": 10
            }
          }
        }
      }
    }
  }
  ```



- 의미적 유사성 구현

  - 구현
    - 검색된 문서들 중 상위 k개의 문서를 뽑아 각 문서들에서 terms을 추출.
    - 추출된 terms 중 가장 빈번히 등장하는 n개의 term을 연관검색어로

  ```python
  from elasticsearch import Elasticsearch
  
  
  INDEX = "search-log"
  FIELD = "term"
  query = "강아지"
  es_client = Elasticsearch("localhost:9200")
  
  res = es_client.search(index=INDEX, query={"match":{FIELD:query}}, size=10)
  
  related_terms = {}
  
  for doc in res["hits"]["hits"]:
      termvectors = es_client.termvectors(index=INDEX, id=doc["_id"], fields=[FIELD])
      # 실제 구현에는 termvectors API가 아닌 analyzer API를 써야 할 것 같다.
      for term in termvectors["term_vectors"][FIELD]["terms"]:
          if term == query:
              continue
          if term in related_terms:
              related_terms[term] += 1
          else:
              related_terms[term] = 1
  
  print(related_terms)
  ```

  - 불필요한 term들을 어떻게 걸러내야 할지
    - `part_of_speech`로 N만 추출.
    - `part_of_speech`가 강제된다.
  - 두 단어 이상은 어떻게 만들지



- 고려사항
  - 금칙어 제외
  - 절차적, 의미적 유사성 기반의 경우 검색 할 때마다 연관검색어를 찾아야 하는데 검색 속도는 괜찮을지
  - 모든 방식을 구현 후 공통적으로 등장하는 terms을 연관검색어로.
    - 의미적 유사성, 절차적 유사성 방식으로 인해 두 단어 이상의 연관검색어는 표출이 되지 않을 수 있음.
  - 연관검색어 등록, 삭제 기능
  - threshold



