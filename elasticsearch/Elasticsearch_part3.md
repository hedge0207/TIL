# Elasticsearch의 자료 구조

- 역색인(Inverted Index)

  - 역색인은 키워드들에 문서들의 PK(또는 주소, 파일명 등)와 같은 값들을 매핑하여 저장하는 기술이다.
    - 역색인 작업의 장점은 매우 빨리 찾을 수 있다는 것이다.
    - 기존보다 추가적인 작업과 메모리가 필요하게 되지만, 검색은 매우 빠른 속도로 처리가 된다.
  - 다음과 같이 dictionary 구조로 저장되어 있는 데이터(문서)가 있다.

  ```python
  data1 = {1:"사과의 효능에 대해서 알아봅시다."}
  data2 = {2:"사과의 효능과 유통기한에 대해서 알아봅시다."}
  data3 = {3:"제가 가장 좋아하는 과일은 사과입니다."}
  ```

  - 위 data들의 value에 형태소 분석을 수행하면 각 value의 형태소들이 추출된다.
    - 일반적으로 검색엔진은 불필요한 품사를 제외한 명사등만 추출한다(명사만 추출된다고 가정).
    - data1: 사과, 효능
    - data2: 사과, 효능, 유통기한
    - data3: 사과, 과일
  - 검색 엔진은 위 결과를 토대로 역색인 작업을 하게 된다.

  | 키워드   | 문서 번호 |
  | -------- | --------- |
  | 사과     | 1, 2, 3   |
  | 효능     | 1, 2      |
  | 유통기한 | 2         |
  | 과일     | 3         |

  - "사과 효능"을 검색했을 경우
    - 사과가 포함된 문서 1,2,3을 가져오고
    - 유통기한이 포함된 문서 1, 2를 가져온다.
    - 마지막으로 둘의 교집합인 1, 2를 출력해준다.

  - AND가 아닌 OR 처리가 필요하다면 다음과 같은 처리를 하면 된다.
    - "사과 효능"을 검색할 경우
    - 1번 문서에는 사과, 효능이 모두 일치한다 - 2개가 일치
    - 2번 문서도 사과, 효능이 모두 일치한다 - 2개가 일치
    - 3번 문서는 사과만 일치한다 - 1개만 일치
    - 이제 문서별로 일치도가 높은 순으로 정렬(1,2,3) 후 사용자에게 출력한다.
  - 문서의 개수가 증가하더라도, 각 keyword에 문서 번호가 추가될 뿐이기에 큰 속도 저하 없이 검색이 가능하다.
  - Inverted index는 Elasticsearch segment로 disk에 저장된다.
    - 검색시에 disk에 저장된 모든 inverted index(segment)를 읽어 검색을 수행한다.
    - 빈번하게 접근하는 inverted index를 cache memory에 저장하여 보다 빠르게 읽을 수 있도록 한다.
  - Segment가 불변성을 가짐으로써 얻는 이점
    - 불변성이 보장된다면, 다수의 스레드가 동시에 접근하여 수정하는 일이 없어지므로 Lock이 필요 없어진다.
    - 불변성이 보장되지 않을 경우 데이터가 변경될 때 마다 system cache를 갱신해야 하는데, 불변성이 보장된다면 system cache가 상대적으로 오랜 기간 동안 변동 없이 유지되므로 system cache를 적극적으로 활용이 가능하다.
    - 역색인을 만드는 과정에서 많은 resource(CPU, memory)를 사용하는데, segment의 변경을 허용할 경우 일부가 수정되더라도 segment file을 다시 작성해야 해서 많은 resource가 소모된다.
    - 따라서 변경 사항이 있을 때 마다 기존의 segment file을 수정하기 보다는 새로운 segment file을 생성하는 것이 낫다.
  - Elasticsearch의 모든 data가 inverted index에 저장되는 것은 아니다.
    - Elasticsearch의 모든 data는 각 field에 최적화된 자료구조에 저장된다.
    - 예를 들어 text field의 data는 inverted index에 저장되지만, numeric이나 geo field는 BKD tree 형태로 저장된다.
  - Term Dictionary
    - 특정 field에 대한 고유한 모든 term을 저장하고 있는 정렬된 skip list이다.
    - Skip list란 linked list와 유사하지만, 하나의 node가 다음 노드를 가리키는 pointer를 여러 개 가지고 있는 자료구조로 바로 다음 node만을 가리키는 pointer만 가지고 있는 linked list와 달리 여러 포인터를 가지고 있기에 중간에 있는 node를 skip할 수 있어 빠른 속도로 검색이 가능하다는 장점있다.
    - 모든 유일한 term을 저장하기 위한 자료구조이다.
    - Term과 해당 term 대한 meta data(예: 문서 빈도, 문서 위치 등)를 매핑하는 역할을 한다.
  - Posting List
    - Term dictionary와 마찬가지로 정렬된 skip list이다.
    - term과 관련된 document id들을 저장하고 있다.
    - 검색된 term들의 document id를 반환하기 위해 사용한다.



- fielddata

  - 집계, 정렬 등은 역인덱스를 통해서는 불가능하다.
    - 역인덱스를 사용하는 검색은 어떤 문서가 특정 키워드를 포함하는지 여부를 보는 것이다.
    - 그러나 집계 정렬 등은 특정 키워드를 포함하는지가 아닌 특정 field의 값이 무엇인지를 알아야 가능하다.
  - 따라서 Elasticsearch 집계, 정렬등을 위해 fielddata라는 자료 구조를 사용한다.
    - fielddata는 key를 document로, value를 field와 field value로 하는 자료구조이다.

  ```json
  [
      {
          "some_doc_id1": {
              "field1":"foo",
              "field2":"bar"
          }
      },
      {
          "some_doc_id2": {
              "field1":"baz",
              "field2":"qux"
          }
      }
  ]
  ```

  - text field는 기본적으로 검색이 가능하지만, 집계, 정렬, scripting은 불가능하다.
    - 만약 text field를 대상으로 집계, 정렬, 혹은 script를 사용하여 text field의 값에 접근해야한다면, `fielddata` 값을 true로 변경해줘야한다.
    - 이 경우 분리된 token 별로 집계가 가능하다.

  ```json
  PUT my-index-000001/_mapping
  {
    "properties": {
      "my_field": { 
        "type":     "text",
        "fielddata": true
      }
    }
  }
  ```

  - fielddata는 in-memory 구조로 동작하여 많은 heap memory를 소비한다.
    - 아마 이것이 text type의 fielddata의 기본값으로 false로 설정해둔 이유일 듯 하다.
    - text 필드는 token 단위로 저장을 해야하는데, field value가 조금만 길어져도 무수히 많은 token이 생성될 것이기에 훨씬 많은 heap memory를 소비하게 될 것이다.
    - 기본적으로 특정 field를 대상으로 fielddata를 생성해야하면, elasticsearch는 모든 document의 field value를 memory에 올린다.
    - 예를 들어 `subject`라는 필드를 대상으로 집계를 해야한다고 하면, elasticsearch는 모든 document의 subject field의 값을 전부 memory에 올린다.
    - 이는 매번 메모리에 적재하는 것 보다 미리 모두 적재해두고 다음 query에도 사용하는 것이 보다 효율적이기 때문이다. 
  - `fielddata_frequency_filter`
    - 메모리에서 불러오는 term의 수를 빈도를 기준으로 감소시켜 메모리 사용을 줄일 수 있다.
    - `min`, `max` 값을 지정하며 둘 사이의 빈도를 지닌 term들만 메모리에서 불러온다.
    - `min`, `max` 값은 양의 정수 혹은 0~1 사이의 소수로 지정한다.
    - 퍼센트는 세그먼트 내의 모든 문서가 아닌, 해당 field에 값이 있는 문서들만 대상으로 계산된다.
    - `min_segment_size` 옵션을 통해 일정 개수 이상의 문서를 가지지 못한 세그먼트를 제외시킬 수 있다.
  
  ```json
  PUT my-index-000001
  {
    "mappings": {
      "properties": {
        "tag": {
          "type": "text",
          "fielddata": true,
          "fielddata_frequency_filter": {
            "min": 0.001,	# 1%
            "max": 0.1,	# 10%
            "min_segment_size": 500
          }
        }
      }
    }
  }
  ```
  
  - fielddata 모니터링
  
  ```bash
  # 각 index 별로 전체적인 fielddata 상태를 출력
  $ curl -XGET 'localhost:9200/_stats/fielddata?fields=*&pretty'
  
  # 클러스터 내의 각 node 별로 사용되고 있는 fielddata 상태를 출력
  $ curl -XGET 'localhost:9200/_nodes/stats/indices/fielddata?fields=*&pretty'
  ```



- doc_values

  - Elasticsearch는 문서별로 field 값을 조회해야 하는 집계 등의 작업을 위해 `doc_values`라는 자료 구조를 사용한다.
    - `doc_values`는 on-disk 자료구조로, document가 색인될 때 생성된다.
    - ` _source`에 저장되는 것과 같은 값을 저장하지만, `_source`와는 달리 집계나 정렬을 효율적으로 하기 위해서 column 형(column-oriented)으로 저장한다.
    - `doc_values`는 거의 대부분의 field type을 지원하지만, text와 annotated_text type은 지원하지 않는다.
  - fielddata와의 차이
    - query time에 생성되는 fielddata와 달리 doc_value는 index time에 생성된다.
    - memory를 사용하는 fielddata와 달리 doc_value는 disk에 저장된다(따라서 속도는 doc_value가 더 느리다).
    - 또한 text type에는 사용할 수 없는 doc_values와 달리 fielddata는 text type에도 사용할 수 있다.
  - 구조 예시
    - key-value 기반이 아닌 column 기반임을 명심해야한다.

  | fieldA | fieldB |
  | ------ | ------ |
  | value1 | value1 |
  | value2 | value2 |
  | value3 | value3 |

  - Doc-value-only-fields
    - numeric, date, boolean, ip, geo_point, keyword type등은 index되지 않아도 doc values가 활성화 되었다면 검색이 가능하다.
    - 단, 검색 속도는 index되었을 때 보다 훨씬 느리다.
    - 그러나 disk 사용량은 훨씬 줄어든다는 장점이 있다.
    - 따라서 거의 검색되지 않는 필드를 대상으로는 아래와 같이 index는 false로 주고 doc value만 활성화(아무 옵션을 주지 않으면 기본적으로 활성화 된다)하여 사용하는 것도 좋은 선택이다.

  ```json
  PUT my-index-000001
  {
    "mappings": {
      "properties": {
        "session_id": { 
          "type":  "long",
          "index": false
        }
      }
    }
  }
  ```

  - doc values 비활성화하기
    - doc values를 지원하는 모든 field는 기본적으로 doc values가 활성화되어있다.
    - 만일 비활성화 시키고자 한다면 아래와 같이 하면 된다.

  ```json
  PUT my-index-000001
  {
    "mappings": {
      "properties": {
        "session_id": { 
          "type": "keyword",
          "doc_values": false
        }
      }
    }
  }
  ```

  - `doc_values`를 disable한 상태로 field를 생성하면 aggregation과 sorting이 불가능하다.

  ```json
  // PUT test
  {
    "mappings": {
      "properties": {
        "foo":{
          "type":"keyword",
          "doc_values": false
        }
      }
    }
  }
  
  // GET test/_search
  {
    "aggs": {
      "my_terms": {
        "terms": {
          "field": "foo",
          "size": 10
        }
      }
    }
  }
  
  // GET test/_search
  {
    "sort": [
      {
        "foo": {
          "order": "desc"
        }
      }
    ]
  }
  ```



- Global Ordinals

  - keyword field 등의 term 기반 field type들은 doc_value를 ordinal mapping을 사용하여 저장한다.

    - Mapping은 각 term에 증가하는 integer 혹은 사전순으로 정렬된 순서(ordinal)를 할당하는 방식으로 이루어진다.
    - Field의 doc value들은 각 document의 순서(ordinal)만을 저장하며, 원래 term들은 저장하지 않는다.

  - 예시

    - 아래와 같이 field value에 순서를 매기고

    | Ordinal | field_value |
    | ------- | ----------- |
    | 0       | apple       |
    | 1       | banana      |
    | 2       | watermelon  |
    | 3       | kiwi        |

    - 이를 기반으로 oridinal mapping을 생성한다.

    | doc_id | field   |
    | ------ | ------- |
    | doc_1  | 0, 1    |
    | doc_2  | 1, 3    |
    | doc_3  | 0, 3    |
    | doc_4  | 0, 2, 3 |

    - 위 표에서 doc_1은 apple, banana라는 문자열을 저장하는 대신, 0, 1이라는 순서만을 저장했는데, 나중에 field_value가 필요하면 해당 순서에 해당하는 문자열을 가져와서 사용하는 방식이다.

  - global ordinal이란
    - 각 index의 segment들은 각자 자신의 ordinal mapping을 정의한다.
    - 그러나 aggregation은 전체 shard를 대상으로 이루어져야 하므로, Elasticsearch는 global ordinal이라 부르는 ordinal mapping들의 결합체를 생성한다.
  - 아래와 같을 때 사용된다.
    - keyword, ip, falttend field를 대상으로 한 특정 bucket aggregation(terms, composite 등).
    - fielddata가 true로 설정된 text field에 대한 aggregation
    - join field를 대상으로 하는 연산(has_child query 혹은 parent aggregation 등)



- Stored fields
  
  - Elasticsearch에서 색인과 저장은 다르다.
    - 색인은 들어온 데이터로 역색인 구조를 만드는 것이다.
    - 저장은 들어온 데이터를 그대로 저장하는 것이다.
    - Elasticsearch는 indexing 요청이 들어올 때 모든 필드를 역색인구조로 색인한다.
    - 기본적으로 필드들은 색인되지만, 개별적으로 저장되지 않고 `_source`라 불리는 필드에 일괄적으로 저장된다.
  - Elasticsearch는 index된 데이터에 검색을 실행하고, store된 데이터를 반환한다.
    - 즉, 실제 검색은 `_source` 필드에 행해지는 것이 아니라 역색인 테이블에 행해진다.
  - `_source` 필드는 overhead를 불러올 수 있지만 아래와 같은 이유로 저장이 필요하다.
    - response에 원본 데이터를 함께 반환하기 위해서(response의 `_source` 필드에 담아 보낸다)
    - reindexing, update, update_by_query 등을 사용하기 위해서(당연하게도 원본 데이터가 없다면 reindexing, update 등이 불가능하다).
    - highlight 기능을 사용하기 위해서.
  - Mapping 설정시에 `store`를 true로 준 field는 Lucene의 stored fields형태로 저장된다.
    - `_id`와 `_source` field의 경우 stored field이다.
  - Stored fields는 모든 stored field를 연속적으로 포함한 row 형태로 저장된다.
    - 가장 앞에 있는 field가 `_id` field이며, `_source`가 가장 마지막 field이다.
    - Row 형태로 저장되기에 column 형태로 저장되는 doc_values에 비해 retrieve 속도가 느리다.
    - 아래와 같이 문서 x의 각 field들이 순차적으로 저장되고, 그 이후에 문서 x+1의 각 field들의 field들이 순차적으로 저장되는 형식이다.
    - 따라서 column기반으로 저장되는 doc_values에 비해 탐색 속도가 느릴 수 밖에 없다.
  
  | field1 | field2 | field3 | field4 | field1 | field2 | field3 | field4 | field5 | field6 |
  | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
  
  - Elasticsearch에서 stored fields는 압축된다.
    - 따라서 당연하게도, `_id` field와 `_source` field도 압축된다.





# Elasticsearch의 score 계산 방식

> https://wikidocs.net/31698 참고

- TF-IDF(Term Frequency-Inverse Document Frequency)

  - Term이 한 문서에서 얼마나 자주 반복되는지와 여러 문서들에서 얼마나 자주 등장하는 term인지가 점수에 영향을 미친다.

    - 하나의 단어가 한 문서 내에서 여러 번 반복되면 점수는 올라가고, 하나의 단어가 여러 문서에서 빈번히 발견될 수록 점수는 낮아진다.

  - 문서 하나를 d, 단어를 t, 문서의 총 개수를 D이라 할 때 TF, DF, IDF는 다음과 같이 정의된다.

    - tf(d, t): 특정한 단어가 문서 내에 얼마나 자주 등장하는지를 나타내는 값.

    - df(t): 특정 단어 t가 전체 문서군 내에서 얼마나 자주 등장하는지를 나타내는 값.
    - idf(d, t): df(t)에 반비례하는 수

  - tf(d, t)의 계산 방식(아래 방식 외에도 무수히 많은 변형이 존재한다)

    - 불린 빈도: t가 d에 한 번이라도 나타나면 1, 아니면 0. 간단하긴 하지만 문서에 단어가 1번 나타나나 1000번 나타나나 차이가 없다는 문제가 있다.
    - 로그 스케일 빈도: `log(f(t,d)+1)`, `f(t,d)`는 문서 d에 t가 등장하는 빈도 수로, 결과값의 크기가 너무 커지지 않게 하기 위해 log를 사용하고, d에 t가 없는 경우 값이 마이너스 무한대로 수렴하는 것을 막기 위해 1을 더해준다. 작은 빈도수 차이일 때는 tf값의 차이가 커지지만, 단어의 빈도가 무수히 늘어날수록 tf의 값의 차이가 크게 벌어지지 않게 된다.
    - 증가빈도: 특정 문서 d에 등장하는 모든 단어의(w) 빈도수를 계산 후 그 최댓값이 분모(문서 내에서 가장 많이 등장한 term의 등장 횟수)가 되고, `f(t,d)`(문서 `d`에서 term `t`의 등장 횟수)는 분자가 된다. 최소 0.5부터 최대 1까지의 값을 가진다. 문서의 길이가 길어 다양한 단어가 나올 때 주로 사용한다.

    $$
    tf(t,d) = 0.5+0.5*\frac{f(t,d)}{max\{f(w,d):w\in d\}} = 0.5+0.5*\frac{f(t,d)}{문서\ 내\ 단어들의\ freq(t,d)중\ 최대값}
    $$

  - idf(d, t)의 계산 방식

    - log로 계산하는 이유는 문서의 개수 n이 커질수록 IDF의 값이 기하급수적으로 커지는 것을 막기 위해서이다.
    - 분모에 1을 더해주는 이유는 특정 단어가 전체 문서에서 아예 등장하지 않을 경우 분모가 0이 되는 것을 방지하기 위해서다.

    $$
    idf(d,t)=log(\frac{D}{1+df(t)})
    $$

  - TF-IDF의 최종 계산식

    - tf(t, d) 값과 idf(t, D) 값을 곱한다.

    $$
    tfidf(t,d,D) = tf(t,d)*idf(t,D)
    $$

  - 예시(조사, 문장부호는 생략)

    - doc1: 식당에서 메뉴를 고민.
    - doc2: 메뉴가 치킨인 식당.
    - doc3: 오늘 저녁 치킨? 치킨!
    - doc4: 점심 식사는 초밥.

  |      | 점심 | 저녁 | 오늘 | 메뉴 | 치킨 | 고민 | 식당 | 초밥 | 식사 |
  | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  | doc1 | 0    | 0    | 0    | 1    | 0    | 1    | 1    | 0    | 0    |
  | doc2 | 0    | 0    | 0    | 1    | 1    | 0    | 1    | 0    | 0    |
  | doc3 | 0    | 1    | 1    | 0    | 2    | 0    | 0    | 0    | 0    |
  | doc4 | 1    | 0    | 0    | 0    | 0    | 0    | 0    | 1    | 1    |

  - TF 계산(증가빈도로 계산)
    - doc1에 등장하는 모든 단어(식당, 메뉴, 고민)는 각 1번씩만 등장하므로 분모는 1이 된다.
    - doc1에서 메뉴라는 단어는 문서 내에 1번만 등장하므로 분자는 1이 된다.
    - 따라서 doc1에서 메뉴의 tf(d, t)의 값은 1이다.
    - 나머지도 위 과정에 따라 계산하면 아래와 같이 나오게 된다(공백은 최소값인 0.5)
    - 아래에서 짧은 문장을 증가빈도로 계산했을 때의 문제를 알 수 있는데, doc3에서 두 번 등장한 치킨과 doc2에서 한 번 등장한 치킨이 동일한 TF 값을 갖게 된다.

  |      | 점심 | 저녁 | 오늘 | 메뉴 | 치킨 | 고민 | 식당 | 초밥 | 식사 |
  | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  | doc1 |      |      |      | 1    |      | 1    | 1    |      |      |
  | doc2 |      |      |      | 1    | 1    |      | 1    |      |      |
  | doc3 |      | 0.75 | 0.75 |      | 1    |      |      |      |      |
  | doc4 | 1    |      |      |      |      |      |      | 1    | 1    |

  - IDF계산
    - IDF 계산을 위해 사용하는 로그의 밑은 크기를 조절하는 상수의 역할을 하며, 사용자가 임의로 정한다.
    - TF-IDF를 계산하는 패키지는 언어와 무관하게 자연 로그(밑으로 자연상수(e, 2.7182...)를 사용하는 로그)를 사용하므로 예시에서도 자연 로그를 사용한다.(자연 로그는 보통 log가 아닌 ln으로 표현한다).
    - 문서의 개수는 총 4개이기에 분자는 4가 된다.

  | 단어 | 점심                   | 저녁                   | 오늘                   | 메뉴                   | 치킨                   | 고민                   | 식당                   | 허기                   | 식사                   |
  | ---- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- | ---------------------- |
  | IDF  | ln(4/(1+1)) = 0.693147 | ln(4/(1+1)) = 0.693147 | ln(4/(1+1)) = 0.693147 | ln(4/(2+1)) = 0.287682 | ln(4/(2+1)) = 0.287682 | ln(4/(1+1)) = 0.693147 | ln(4/(2+1)) = 0.287682 | ln(4/(1+1)) = 0.693147 | ln(4/(1+1)) = 0.693147 |

  - 이제 둘을 곱하면 TF-IDF 값을 얻을 수 있다.

  |      | 점심     | 저녁     | 오늘     | 메뉴     | 치킨     | 고민     | 식당     | 허기     | 식사     |
  | ---- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
  | doc1 |          |          |          | 0.287682 |          | 0.693147 | 0.287682 |          |          |
  | doc2 |          |          |          | 0.287682 | 0.287682 |          | 0.287682 |          |          |
  | doc3 |          | 0.519860 | 0.519860 |          | 0.287682 |          |          |          |          |
  | doc4 | 0.693147 |          |          |          |          |          |          | 0.693147 | 0.693147 |



- BM25(Okapi BM25)

  > https://blog.naver.com/shino1025/222240603533
  >
  > https://inyl.github.io/search_engine/2017/04/18/bm25_2.html

  - TF-IDF의 문제점
    - 한 단어가 반복적으로 등장하면 TF의 값이 지속적으로 증가한다.
    - 문서 길이가 길어질 수록 다양한 단어가 등장할 수 밖에 없으므로, 검색될 확률이 높아진다.
  - TF-IDF의 변형이다.
    - Elasticsearch 5.0부터 사용중인 계산 방법이다.
    - 원래 Lucene과 Elasticsearch 모두 TF-IDF 방식을 사용했으나 Lucene이 BM25로 계산 방식을 변경하면서 Elasticsearch도 같이 변경했다.
    - 보정 파리미터들을 추가해서 성능을 개선한 알고리즘이다.
  - 계산식
    - 토큰 q<sub>1</sub>, q<sub>2</sub>, ... q<sub>n</sub>을 포함하는 쿼리 Q가 주어질 때, 단일 문서 D에 대한 BM25 점수는 다음과 같이 구한다.

  $$
  score(D, Q) = \sum_{i=1}^nIDF(q_i) * \frac{f(q_i,D)*(k1+1)}{f(q_i,D)+k1*(1-b+b*\frac{|D|}{avgdl})}
  $$

  - Elasticsearch의 BM25 계산
    - BM25를 약간 변형하여 사용한다.
    - `boost * IDF * TF`로 계산한다.
  - Elasticsearch의 IDF 계산
    - `N`은 전체 문서의 개수, $n(q_i)$는 $q_i$라는 term을 포함하고 있는 문서의 개수이다.

  $$
  IDF(q_i) = ln(1+\frac{N-n(q_i)+0.5}{n(q_i)+0.5})
  $$

  - Elasticsearch의 TF 계산
    - f(q<sub>i</sub>, D) 부분은  단일 문서 D에서 토큰 q<sub>i</sub>의 term frequency를 계산하는 것이다.
    - k1는 쿼리에 똑같은 토큰이 여러 개 등장했을 때, 어느 정도의 패널티를 줄 것인지를 결정하는 파라미터이다.
    - 어떤 토큰의 TF가 k1보다 작다면, k1으로 인해 점수가 증가하게 되지만, 반대의 경우 k<sub>1</sub>으로 인해 점수가 낮아지게 된다.
    - b는 TF를 측정할 때, 문서의 길이에 따르는 패널티를 부여할 것인지를 뜻한다.
    - b가 높으면, 문서의 길이가 길어질수록 점수에 패털티를 준다.
    - dl은 단일 문서의 필드 길이를 뜻하고, avgdl은 전체 문서의 필드의 평균 길이를 뜻한다.

  $$
  TF(q_i)=\frac{f(q_i,D)}{f(q_i,D)+k1*(\frac{1-b+b*dl}{avgdl})}
  $$

  - 요약
    - 특정 단어가 문서에 많이 등장했다면 높은 점수를 준다.
    - 만일 해당 필드가 너무 길다면 점수를 약간 깎는다.
    - 같은 단어가 단일 문서에 여러 번 등장한다면 점수를 약간 깎는다
    - 만일 해당 단어가 여러 문서에 흔하게 등장한다면 점수를 많이 깎는다.



- Elasticsearch의 점수 계산 방식 변경하기

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html

  - Index 생성시에 각 field 별로 다른 similarity 계산을 사용하도록 변경할 수 있다.
  - 아래와 같이 settings에 similarity 계산 방식을 정의하고, mapping에서 field를 설정할 때 settings에서 정의한 계산 방식을 설정해주면 된다.

  ```json
  // PUT my-index
  {
      "settings": {
          "index": {
              "similarity": {
                  "my_similarity": {
                      "type": "DFR",
                      "basic_model": "g",
                      "after_effect": "l",
                      "normalization": "h2",
                      "normalization.h2.c": "3.0"
                  }
              }
          }
      },
      "mappings":{
          "properties" : {
              "title" : { 
                  "type" : "text", 
                  "similarity" : "my_similarity" 
              }
          }
      }
  }
  ```

  - Elasticsearch는 아래와 같은 similarity module을 지원한다.
    - BM25
    - DFR
    - DFI
    - IB
    - LM Jlinek Mercer

  - 혹은 script를 사용하여 직접 점수 계산 방식을 구현하는 것도 가능하다.
    - 아래 script는 TF-IDF를 script를 사용하여 구현한 것이다.
    - 주의할 점은 반환하는 score는 반드시 양수여야 한다는 것이다.

  ```json
  // PUT my-index
  {
      "settings": {
          "number_of_shards": 1,
          "similarity": {
              "scripted_tfidf": {
                  "type": "scripted",
                  "script": {
                      "source": "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
                  }
              }
          }
      }
  }
  ```

  - `weight_script`를 통해 가중치를 주는 script를 별도로 작성하는 것도 가능하다.
    - `weight_script`를 사용하지 않을 경우 가중치는 1로 고정된다.

  ```json
  {
      "settings": {
          "similarity": {
              "scripted_tfidf": {
                  "type": "scripted",
                  "weight_script": {
                      "source": "double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; return query.boost * idf;"
                  },
                  "script": {
                      "source": "double tf = Math.sqrt(doc.freq); double norm = 1/Math.sqrt(doc.length); return weight * tf * norm;"
                  }
              }
          }
      }
  }
  ```



- BM25 similarity 사용시 TF값의 계산 요소 중 term_frequency의 가중치 낮추기

  - BM25 similarity 사용시 term_frequency 값의 가중치를 낮춰야 한다면 중복 token을 제거하는 것도 고려해 볼 수 있다.
  - 예를 들어 아래와 같은 문서가 있다고 가정해보자.

  ```json
  // PUT test-index/_doc/1
  {
      "text":"brown fox playing with fox"
  }
  ```

  - 위 문서는 standard tokenizer 기준으로 아래와 같이 tokenizing된다.
    - "fox" 라는 token이 두 번 나왔으므로 `term_freq` 값은 2가 된다.

  ```json
  // GET test-index/_termvectors/1?fields=text
  {
    // ...
    "term_vectors": {
      "text": {
        // ...
          "fox": {
            "term_freq": 2,
            "tokens": [
              {
                "position": 1,
                "start_offset": 6,
                "end_offset": 9
              },
              {
                "position": 4,
                "start_offset": 23,
                "end_offset": 26
              }
            ]
          },
          // ...
        }
      }
    }
  }
  ```

  - 아래와 같이 추가 문서를 색인하고

  ```json
  // PUT test-index/_doc/2
  {
      "text":"brown fox playing with box"
  }
  ```

  - "fox"라는 검색어로 검색을 하면

  ```json
  // GET test-index/_search
  {
      "explain": true, 
      "query": {
          "match": {
              "text": "fox"
          }
      }
  }
  ```

  - "fox"라는 token을 두 개 가진 1번 문서의 tf 값이 더 크므로 1번 문서의 점수가 더 높게 나오는 것을 확인할 수 있다.
    - TF 값 계산에 포함되는 요소 중 `freq`를 제외한 다른 모든 값들은 동일한 것을 볼 수 있다.

  ```json
  {
    // ...
    "hits": {
      // ...
      "hits": [
        {
          // ...
          "_id": "1",
          "_score": 0.25069216,
          "_source": {
            "text": "brown fox playing with fox"
          },
          "_explanation": {
            "value": 0.25069216,
            "description": "weight(text:fox in 0) [PerFieldSimilarity], result of:",
            "details": [
              {
                "value": 0.25069216,
                "description": "score(freq=2.0), computed as boost * idf * tf from:",
                "details": [
                  // ...
                  {
                    "value": 0.625,
                    "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                    "details": [
                      {
                        "value": 2,
                        "description": "freq, occurrences of term within document",
                        "details": []
                      },
                      {
                        "value": 1.2,
                        "description": "k1, term saturation parameter",
                        "details": []
                      },
                      {
                        "value": 0.75,
                        "description": "b, length normalization parameter",
                        "details": []
                      },
                      {
                        "value": 5,
                        "description": "dl, length of field",
                        "details": []
                      },
                      {
                        "value": 5,
                        "description": "avgdl, average length of field",
                        "details": []
                      }
                    ]
                  }
                ]
              }
            ]
          }
        },
        {
          // ...
          "_id": "2",
          "_score": 0.18232156,
          "_source": {
            "text": "brown fox playing with box"
          },
          "_explanation": {
            "value": 0.18232156,
            "description": "weight(text:fox in 0) [PerFieldSimilarity], result of:",
            "details": [
              {
                "value": 0.18232156,
                "description": "score(freq=1.0), computed as boost * idf * tf from:",
                "details": [
                  // ...
                  {
                    "value": 0.45454544,
                    "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                    "details": [
                      {
                        "value": 1,
                        "description": "freq, occurrences of term within document",
                        "details": []
                      },
                      {
                        "value": 1.2,
                        "description": "k1, term saturation parameter",
                        "details": []
                      },
                      {
                        "value": 0.75,
                        "description": "b, length normalization parameter",
                        "details": []
                      },
                      {
                        "value": 5,
                        "description": "dl, length of field",
                        "details": []
                      },
                      {
                        "value": 5,
                        "description": "avgdl, average length of field",
                        "details": []
                      }
                    ]
                  }
                ]
              }
            ]
          }
        }
      ]
    }
  }
  ```

  - 이제 term_frequency의 가중치를 낮추기 위해 아래와 같이 `unique` token filter를 사용하여 중복 token을 제거한다.

  ```json
  // PUT unique-token
  {
      "settings": {
          "analysis": {
              "analyzer": {
                  "unique_analyzer": {
                      "type":"custom",
                      "tokenizer":"standard",
                      "filter": [
                          "unique"
                      ]
                  }
              }
          }
      },
      "mappings": {
          "properties": {
              "text": {
                  "type": "text",
                  "analyzer": "unique_analyzer"
              }
          }
      }
  }
  ```

  - 그 후 다시 2개의 문서를 색인한다.
    - 위와 동일하게 하나의 문서에만 fox가 2번 등장한다.

  ```json
  // PUT unique-token/_doc/1
  {
      "text":"brown fox playing with fox"
  }
  
  // PUT unique-token/_doc/2
  {
      "text":"brown fox playing with box"
  }
  ```

  - 1번 문서의 token을 확인해보면 아래와 같다.
    - 중복 token을 모두 제거했으므로 fox token의 `term_freq` 값이 1인 것을 볼 수 있다.

  ```json
  // GET unique-token/_termvectors/1?fields=text
  {
    // ...
    "term_vectors": {
      "text": {
        // ...
        "terms": {
          // ...
          "fox": {
            "term_freq": 1,
            "tokens": [
              {
                "position": 1,
                "start_offset": 6,
                "end_offset": 9
              }
            ]
          },
          // ...
        }
      }
    }
  }
  ```

  - 이제 다시 동일한 query로 검색을 해보면

  ```json
  // GET unique-token/_search
  {
      "explain": true, 
      "query": {
          "match": {
              "text": "fox"
          }
      }
  }
  ```

  - `term_freq` 값이 1이 된 것을 확인할 수 있다.

  ```json
  {
      // ...
      "hits": {
          // ...
          "max_score": 0.19100355,
          "hits": [
              {
                  // ...
                  "_id": "1",
                  "_score": 0.19100355,
                  // ...
                  "_explanation": {
                      "value": 0.19100355,
                      "description": "weight(text:fox in 0) [PerFieldSimilarity], result of:",
                      "details": [
                          {
                              "value": 0.19100355,
                              "description": "score(freq=1.0), computed as boost * idf * tf from:",
                              "details": [
                                  // ...
                                  {
                                      "value": 0.47619045,
                                      "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                                      "details": [
                                          {
                                              "value": 1,
                                              "description": "freq, occurrences of term within document",
                                              "details": []
                                          },
                                          {
                                              "value": 1.2,
                                              "description": "k1, term saturation parameter",
                                              "details": []
                                          },
                                          {
                                              "value": 0.75,
                                              "description": "b, length normalization parameter",
                                              "details": []
                                          },
                                          {
                                              "value": 4,
                                              "description": "dl, length of field",
                                              "details": []
                                          },
                                          {
                                              "value": 4.5,
                                              "description": "avgdl, average length of field",
                                              "details": []
                                          }
                                      ]
                                  }
                              ]
                          }
                      ]
                  }
              },
              {
                  // ...
                  "_id": "2",
                  "_score": 0.17439456,
                  // ...
                  "_explanation": {
                      "value": 0.17439456,
                      "description": "weight(text:fox in 0) [PerFieldSimilarity], result of:",
                      "details": [
                          {
                              "value": 0.17439456,
                              "description": "score(freq=1.0), computed as boost * idf * tf from:",
                              "details": [
                                  // ...
                                  {
                                      "value": 0.43478262,
                                      "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                                      "details": [
                                          {
                                              "value": 1,
                                              "description": "freq, occurrences of term within document",
                                              "details": []
                                          },
                                          {
                                              "value": 1.2,
                                              "description": "k1, term saturation parameter",
                                              "details": []
                                          },
                                          {
                                              "value": 0.75,
                                              "description": "b, length normalization parameter",
                                              "details": []
                                          },
                                          {
                                              "value": 5,
                                              "description": "dl, length of field",
                                              "details": []
                                          },
                                          {
                                              "value": 4.5,
                                              "description": "avgdl, average length of field",
                                              "details": []
                                          }
                                      ]
                                  }
                              ]
                          }
                      ]
                  }
              }
          ]
      }
  }
  ```

  - 주의 사항
    - 위 내용을 봤을 때 문서 1과 문서 2에서 token fox에 대한 `freq` 값이 1로 같으므로 두 문서의 점수가 같아야 할 것 같지만, 그렇지 않다.
    - 이는 field의 길이를 나타내는 `dl` 때문이다.
    - 문서 1의 token 들 중 중복된 fox token 하나가 날아가면서 문서 1의 `dl`이 5에서 4로 1 감소했다.
    - 이로 인해 TF 값은 올라가게 된다.
    - 따라서 위 방식을 사용할 때는, 사라진 token들로 인해 `dl` 값이 감소하여 TF값을 증가시킬 수 있다는 것을 염두에 둬야한다.

  





# 클러스터 성능 모니터링과 최적화

- Elasticsearch는 자체적으로 monitoring 기능을 지원한다.
  - Kibana에서 monitoring을 사용하면 자동으로 monitoring 데이터가 쌓이는데 이는 ES 내부의 monitoring 기능을 사용하는 것이다.
  - 아래와 같은 것들을 모니터링 할 수 있다.
    - cluster
    - node
    - index
  - 기본적으로 `_cat` API로 요청을 보냈을 때 응답으로 오는 데이터들이 포함되어 있다.
    - 다만, 모두 포함 된 것은 아니다.
  - 한 클러스터 뿐 아니라 다른 클러스터에서 monitoring 데이터를 가져오는 것도 가능하다.
  
  - `_cat` API에 대응되는 API들
    - `_cat` API는 대부분 사람이 command line이나 Kibana console을 통해 직접 사용하는 것을 의도하고 만들어졌다.
    - 따라서 application에서 사용하기는 적절하지 않다.
    - Application에서 사용해야 한다면 `_cat`에 대응되는 API를 사용하는 것을 권장한다.
  
  | _cat          | application용 API                                            |
  | ------------- | ------------------------------------------------------------ |
  | _cat/health   | [Cluster health API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-health.html) |
  | _cat/indicise | [Get index API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-index.html#indices-get-index) |
  | _cat/nodes    | [Nodes info API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-nodes-info.html) |
  | _cat/segments | [Index segments API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-segments.html) |



- monitoring data 저장하기

  - 아래와 같이 클러스터 설정만 변경해주면 된다.

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-settings.html
  >
  > https://www.elastic.co/guide/en/elasticsearch/reference/current/collecting-monitoring-data.html

  ```bash
  PUT _cluster/settings
  {
    "persistent": {
      "xpack.monitoring.collection.enabled": true
    }
  }
  ```



- 자체적으로 지원하는 모니터링 기능 외에도 metricbeat, filebeat 등을 사용 가능하다.





## 클러스터의 상태 확인하기

- `_cat/health`

  - 클러스터의 상태를 확인하는 API
  - 기본형

  ```http
  GET _cat/health
  ```

  - `v` 옵션을 추가
    - 결과 값에 header를 추가해서 보여준다.

  ```http
  GET _cat/health?v
  ```

  - format 옵션을 추가
    - 지정한 format으로 보여준다.

  ```http
  GET _cat/health?format=json
  ```



- 클러스터 상태 정보

  - `format=json` 옵션을 줬을 때의 응답

  ```json
  [
    {
      "epoch" : "1620718739",		// API를 호출한 시간을 UNIX 시간 형태로 표현한 숫자
      "timestamp" : "07:38:59",	// API를 호출한 시간
      "cluster" : "es-docker-cluster",	// 클러스터 이름
      "status" : "green",		// 클러스터 상태
      "node.total" : "4",		// 전체 노드의 개수
      "node.data" : "3",		// 데이터 노드의 개수
      "shards" : "6",			// 샤드의 개수
      "pri" : "3",			// 프라이머리 샤드의 개수
      "relo" : "0",			// 클러스터에서 재배치되고 있는 샤드의 개수
      "init" : "0",			// 초기화되고 있는 샤드의 개수
      "unassign" : "0",		// 배치되지 않은 샤드의 개수
      "pending_tasks" : "0",	// 클러스터의 유지, 보수를 위한 작업 중 실행되지 못하고 큐에 쌓여 있는 작업의 개수
      "max_task_wait_time" : "-",	// pending_tasks에서 확인한 작업이 실행되기까지 소요된 최대 시간
      "active_shards_percent" : "100.0%"	// 정상적으로 동작하는 샤드의 비율
    }
  ]
  ```

  - `relo`
    - 0이 아니라면 샤드들이 재배치 되고 있다는 의미이다.
    - 지나치게 많은 샤드들이 재배치 되고 있을 경우 색인이나 검색 성능에 악영향을 줄 수 있기 때문에 재배치 되는 원인을 확인해 봐야 한다.

  - `init`
    - 0이 아니라면 그만큼의 프라이머리 혹은 레플리카 샤드가 새롭게 배치되고 있다는 의미이다.

  - `pending_tasks`
    - 0이 아니라면 클러스터가 부하 상황이거나 특정 노드가 서비스 불능 상태일 가능성이 있다.
  - `max_task_wait_time`
    - 이 값이 클수록 작업이 실행되지 못하고 오랫동안 큐에 있었다는 뜻이다.
    - 클러스터의 부하 상황을 나타내는 지표로 활용된다.
  - `active_shards_percent`
    - 100%가 아니라면 초기화중이거나 배치되지 않은 샤드가 존재한다는 의미이다.



- 클러스터의 상탯값

  | 값                                       | 의미                                                         |
  | ---------------------------------------- | ------------------------------------------------------------ |
  | <span style="color:green">green</span>   | 모든 샤드가 정상적으로 동작하고 있는 상태                    |
  | <span style="color:orange">yellow</span> | 모든 프라이머리 샤드는 정상적으로 동작하고 있지만, 일부 혹은 모든 레플리카 샤드가 정상적으로 동작하고 있지 않은 상태 |
  | <span style="color:red">red</span>       | 일부 혹은 모든 프라이머리/레플리카 샤드가 정상적으로 동작하고 있지 않은 상태, 데이터 유실이 발생할 수 있다. |



- 미할당 샤드 수동으로 재할당하기

  ```http
  POST _cluster/reroute?retry_failed=true
  ```





## 노드의 상태와 정보 확인하기

- `_cat/nodes`

  - 노드의 상태를 확인하는 API
  - `v`, `format`등의 옵션을 사용 가능하다.
  - `h` 옵션을 사용 가능하다.

  ```bash
  # 아래 명령을 사용하면 h 옵션에서 사용 가능한 값들을 확인 가능하다.
  $ curl -XGET 'http://localhost:9200/_cat/nodes?help'
  
  # h 옵션은 아래와 같이 주면 된다.
  $ curl -XGET 'http://localhost:9200/_cat/nodes?h=id,name,disk.used_percent'
  ```



- 노드 상태 정보

  ```json
  [
    {
      "ip" : "123.123.456.4",	// 노드의 IP 주소
      "heap.percent" : "15",	// 힙 메모리의 사용률
      "ram.percent" : "49",	// 메모리 사용률
      "cpu" : "4",			// 노드의 CPU 사용률
      "load_1m" : "2.11",		// 각각 1,5,15분의 평균 Load Average를 의미한다.
      "load_5m" : "2.21",
      "load_15m" : "2.20",
      "node.role" : "dilm",	// 노드의 역할
      "master" : "-",			// 마스터 여부, 마스터 노드는 *로 표시된다.
      "name" : "node2"		// 노드의 이름
    }
  ]
  ```

  - `heap.percent`
    - 이 값이 크면 클수록 사용 중인 힙 메모리의 양이 많다는 뜻이다.
    - 일정 수준 이상 커지면  old GC에 의해서 힙 메모리의 사용률이 다시 내려간다.
    - 만약 이 값이 낮아지지 않고 85% 이상을 계속 유지하면 OOM(Out Of Memory)이 발생할 가능성이 크기 때문에 힙 메모리가 올라가는 이유를 확인해 봐야 한다.
  - `ram.percent`
    - `heap.percent`가 JVM이 할당받은 힙 메모리 내에서의 사용률이라면 `ram.percent`는 노드가 사용할 수 있는 전체 메모리에서 사용 중인 메모리의 사용률이다.
    - 이 값은 대부분 90% 이상의 높은 값을 나타내는데, JVM에 할당된 힙 메모리 외의 영역은 OS에서 I/O 부하를 줄이기 위한 페이지 캐시로 사용하기 때문이다.

  - `cpu`
    - 이 값이 크면 CPU를 많이 사용하고 있다는 뜻이며, 경우에 따라서는 클러스터에 응답 지연 현상이 발생할 수 있다.

  - `load_nm`
    - 이 값이 크면 노드에 부하가 많이 발생하고 있다는 뜻이며 클러스터의 응답 지연이 발생할 수 있다.
    - Load Average는 노드에 장착된 CPU 코어의 개수에 따라 같은 값이라도 그 의미가 다를 수 있기 때문에 CPU Usage와 함께 살펴보는 것이 좋다.
    - CPU Usage와 Load Average가 모두 높다면 부하를 받고 있는 상황이다.
  - `node.role`
    - d는 데이터, m은 마스터, i는 인제스트, l은 머신러닝을 의미한다.



## 인덱스의 상태와 정보 확인하기

- `_cat/indices`

  - 인덱스의 상태도 green, yellow, red로 표현된다.
    - 인덱스들 중 하나라도 yellow면 클러스터도 yellow, 하나라도 red면 클러스터도 red가 된다.
  - `v`, `h`, `format` 옵션을 모두 사용 가능하다.
  - 확인
  
  ```http
  GET _cat/indices
  ```
  
  - `s`로 정렬이 가능하다.
  
  ```http
  GET _cat/indices?s=<정렬 할 내용>
  
  #e.g.
  GET _cat/indices?s=docs.count:desc
  ```
  
  - size를 표시할 때 어떤 단위로 보여줄지 설정이 가능하다.
    - `bytes=<단위>`를 입력하면 된다.
  
  
  ```http
  GET _cat/indices?h=i,p,r,dc,ss,cds&bytes=kb
  ```
  
  - `expand_wildcards` 옵션을 통해 open 상태인 인덱스만 보는 것도 가능하다.
  
  ```http
  GET _cat/indices?h=i,status,p,r,dc,ss,cds&s=cds:desc&expand_wildcards=open
  ```



- 인덱스 상태 정보

  ```json
  // GET _cat/indices?format=json
  [
      {
          "health" : "green",	// 인덱스 상탯값
          "status" : "open",	// 사용 가능 여부
          "index" : "test",	// 인덱스명
          "uuid" : "cs4-Xw3WRM2FpT4bpocqFw",
          "pri" : "1",		// 프라이머리 샤드의 개수
          "rep" : "1",		// 레플리카 샤드의 개수
          "docs.count" : "0",		// 저장된 문서의 개수
          "docs.deleted" : "0",	// 삭제된 문서의 개수
          "store.size" : "566b",		// 인덱스가 차지하고 있는 전체 용량(프라이머리+레플리카)
          "pri.store.size" : "283b"	// 프라이머리 샤드가 차지하고 있는 전체 용량
        }
  ]
  ```





## 샤드의 상태 확인하기

- `_cat/shards`

  - 마찬가지로 `v`, `h`, `format` 모두 사용 가능하다.

  ```http
  GET _cat/shards
  ```

  - `grep`을 사용 가능하다.
    - 아래와 같이 입력하면 state가 `UNASSIGNED`인 샤드만을 반환한다.
    - kibana console에서는 사용 불가
  
  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/shards | grep UNASSIGNED'
  ```
  
  - 미할당 샤드가 있을 경우, `h` 옵션을 통해 미할당 된 원인을 확인할 수 있다.
    - `클러스터 운영하기`에서 살펴본  `explain`을 통해서도 확인이 가능하다.
    - 각 원인에 대한 설명은 [공식 가이드](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-shards.html#cat-shards-query-params) 참고
  
  ```bash
  # 어떤 인덱스의 어떤 샤드가 왜 미할당 상태인지 확인하는 명령어
  GET 'http://localhost:9200/_cat/shards?h=index,shard,prirep,unassigned.reason | grep -i UNASSIGNED'
  ```
  
  - 보다 정확한 원인을 알려주는 API
  
  ```http
  GET _cluster/allocation/explain
  ```



- 응답

  ```json
  [
  	{
          "index" : "test",		// 샤드가 속한 인덱스명
          "shard" : "0",			// 샤드 번호
          "prirep" : "p",			// 프라이머리인지 레플리카인지(레플리카는 r)
          "state" : "STARTED",	// 샤드의 상태
          "docs" : "0",			// 샤드에 저장된 문서의 수
          "store" : "283b",		// 샤드의 크기
          "ip" : "123.456.789.1",	// 샤드가 배치된 노드의 IP
          "node" : "node2"		// 샤드가 배치된 데이터 노드의 노드 이름
    	}
  ]
  ```

  - state

  | 값           | 의미                                                         |
  | ------------ | ------------------------------------------------------------ |
  | STARTED      | 정상적인 상태                                                |
  | INITIALIZING | 샤드를 초기화하는 상태. 최초 배치 시, 혹은 샤드에 문제가 발생하여 새롭게 배치할 때의 상태 |
  | RELOCATING   | 샤드가 현재의 노드에서 다른 노드로 이동하고 있는 상태. 새로운 데이터 노드가 추가되거나, 기존 데이터 노드에 문제가 생겨서 샤드가 새로운 노드에 배치되어야 할 때의 상태 |
  | UNASSIGNED   | 샤드가 어느 노드에도 배치되지 않은 상태. 해당 샤드가 배치된 노드에 문제가 생기거나 클러스터의 라우팅 정책에 의해 배치되지 않은 상태. |



- segment 상태 확인

  - `_cat` API
    - `v`, `h`, `format` 옵션을 모두 사용 가능하다.
  
  
  ```http
  GET _cat/segments[/<target>]
  ```
  
  - Index segments API
    - 특정 index에 속한 segments들만 확인할 수 있다.
    - Application에서 사용할 때는 이 API를 사용하는 것이 권장된다.
  
  ```http
  GET <index_name>/_segments
  ```
  
  - Index segments API의 response
    - Segment의 이름은 실제 file이름이다(`<data_dir>/indices/<index_uuid>/<shard>/index`에서 확인할 수 있다).
    - `num_docs`은 삭제된 문서는 포함하지 않으며, nested documents들도 별개의 문서로 집계한다.
    - `committed`가 true면 disk와 segment가 sync되었다는 것을 의미하며, false면 disk와 sync되어 있지 않다는 의미이다.
    - Disk와 sync되어 있다면(committed가 true면) ES가 reboot 되더라도 segment data에 유실이 없다.
    - `committed`가 false라고 하더라도, commit되지 않은 segment의 data들은 trans log에 기록되어 ES가 reboot될 때 trans log에서 data를 읽어올 수 있으므르로 유실이 발생할 일은 거의 없다.
    - `search`가 true면 검색이 가능하다는 의미이고, false이면 refresh를 통해 검색이 가능하게 해줘야한다는 의미이다.
    - `version`은 Lucene version을 의미한다.
    - `attributes`: 압축과 관련된 정보를 보여준다.
  
  ```json
  "shards": {
      "0": [
          {
              "routing": {
                  "state": "STARTED",
                  "primary": false,
                  "node": "5g4483g4g34gg5123T123"
              },
              "num_committed_segments": 1,
              "num_search_segments": 1,
              "segments": {
                  // segment의 이름
                  "_1v": {
                      "generation": 67,			// 새로운 segment가 생성될 때 마다 증가하는 숫자, segment name을 결정할 때 사용한다.
                      "num_docs": 1000000,		// segment에 저장된 문서의 수
                      "deleted_docs": 0,			// 삭제된 문서의 수(실제 삭제된 문서의 개수와 다를 수 있다)
                      "size_in_bytes": 1598215025,// segment의 크기
                      "committed": true,
                      "search": true,
                      "version": "9.4.2",
                      "compound": false,
                      "attributes": {
                          "Lucene90StoredFieldsFormat.mode": "BEST_SPEED"
                      }
                  }
              }
          }
      ]
  }
  ```
  
  - `compound`
    -  true면 Lucene이 file descriptor를 아끼기 위해 segment의 모든 파일들을 하나의 파일에 저장했다는 의미이다.
    - Lucene에서 segment는 compound 방식과 multifile 방식이라는 두 가지 방식 중 하나로 저장된다.
    - Multifile 방식은 segment를 여러 개의 file을 사용해서 저장하는 방식으로, term vector, inverted index, stored field 등을 모두 개별 file에 작성한다.
    - Multifile의 단점은 너무 많은 file을 관리해야 한다는 점이다. OS에서는 open file의 개수가 제한되어 있는데(linux의 경우 `ulimit -n <숫자>` 옵션으로 변경 가능), 너무 많은 segment file이 열려 있을 경우 `Too many open files` error가 발생할 수 있다.
    - Compound 방식은 segment의 여러 file들(term vector, inverted index, stored field 등)을 하나의 file에 저장하는 방식으로 file descriptor를 multifile 방식에 비해 덜 필요로 한다는 장점이 있다.




## stats API로 지표 확인하기

- GC(Garbage Collector)

  - 정의

    - Java로 만든 애플리케이션은 기본적으로 JVM이라는 가상 머신 위에서 동작하는데 OS는 JVM이 사용할 수 있도록 일정 크기의 메모리를 할당해준다.
    - 이 메모리 영역을 힙 메모리라고 부른다.
    - JVM은 힙 메모리 영역을 데이터를 저장하는 용도로 사용한다.
    - 시간이 갈수록 사용 중인 영역이 점점 증가하다가 어느 순간 사용할 수 있는 공간이 부족해지면 사용 중인 영역에서 더 이상 사용하지 않는 데이터들을 지워서 공간을 확보하는데 이런 일련의 과정을 가비지 컬렉션이라 부른다.

    - 사용 중인 영역은 young 영역과  old 영역 두 가지로 나뉜다.

  - Stop-The-World

    - GC 작업을 할 때, 즉 메모리에서 데이터를 지우는 동안에는 다른 스레드들이 메모리에 데이터를 쓰지 못하도록 막는다.
    - GC가 진행되는 동안에너는 다른 스레드들이 동작하지 못하기 때문에 애플리케이션이 응답 불가 현상을 일으키고 이를 Stop-The-World 현상이라 한다.
    - 특히 old GC는 비워야 할 메모리의 양이 매우 많기 때문에 경우에 따라서는 초 단위의 GC 수행 시간이 소요되기도 한다.
    - 이럴 경우 ES 클러스터가 초 단위의 응답 불가 현상을 겪게 된다.

  - Out Of Memory

    - GC를 통해 더 이상 메모리를 확보할 수 없는 상황에서 애플리케이션이 계속해서 메모리를 사용하고자 하면 가용할 메모리가 없다는 OOM 에러를 발생시킨다.
    - OOM  에러는 애플리케이션을 비정상 종료시키기 때문에 클러스터에서 노드가 아예 제외되는 현상이 발생한다.



- 클러스터 성능 지표 확인하기

  - 명령어

  ```bash
  $ curl -XGET 'http://localhost:9200/_cluster/stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_nodes" : {
      "total" : 4,
      "successful" : 4,
      "failed" : 0
    },
    "cluster_name" : "es-docker-cluster",
    "cluster_uuid" : "bOfgi147StyhjT2sOzdPYw",
    "timestamp" : 1620780055464,
    "status" : "green",
    "indices" : {
      // (...)
      "docs" : {
        "count" : 9,		// 색인된 전체 문서의 수
        "deleted" : 1		// 삭제된 전체 문서의 수
      },
      "store" : {
        "size_in_bytes" : 140628	// 저장 중인 데이터의 전체 크기를 bytes 단위로 표시
      },
      "fielddata" : {
        "memory_size_in_bytes" : 0,	// 필드 데이터 캐시의 크기
        "evictions" : 0
      },
      "query_cache" : {
        "memory_size_in_bytes" : 0,	// 쿼리 캐시의 크기
        // (...)
      },
      "completion" : {
        "size_in_bytes" : 0
      },
      "segments" : {
        "count" : 17,		// 세그먼트의 수
        "memory_in_bytes" : 28061,	// 세그먼트가 차지하고 있는 메모리의 크기
        // (...)
      }
    },
    // (...)
      "versions" : [	// 클러스터를 구성하고 있는 노드들의 버전
        "7.5.2"
      ],
      // (...)
      "jvm" : {
        "max_uptime_in_millis" : 69843238,
        "versions" : [	// 클러스터를 구성하고 있는 노드들의 JVM 버전
          {
            "version" : "13.0.1",
            "vm_name" : "OpenJDK 64-Bit Server VM",
            "vm_version" : "13.0.1+9",
            "vm_vendor" : "AdoptOpenJDK",
            "bundled_jdk" : true,
            "using_bundled_jdk" : true,
            "count" : 4
          }
        ],
     // (...)
  }
  ```

  - `fielddata.memory_size_in_bytes`
    - 필드 데이터는 문자열 필드에 대한 통계 작업을 할 때 필요한 데이터이다.
    - 필드 데이터의 양이 많으면 각 노드의 힙 메모리 공간을 많이 차지하기 때문에 이 값이 어느 정도인지 모니터링해야 한다.
    - 노드들의 힙 메모리 사용률이 높다면 우선적으로 필드 데이터의 유무를 확인하는 것이 좋다.

  - `query_cache.memory_size_in_bytes`
    - 모든 노드들은 쿼리의 결과를 캐싱하고 있다.
    - 이 값이 커지면 힙 메모리를 많이 차지하기에 이 값이 어느정도인지 모니터링해야 한다.

  - `segments.memory_in_bytes`
    - 세그먼트도 힙 메모리 공간을 차지하기 때문에 힙 메모리의 사용률이 높을 경우 세그먼트의 메모리가 어느 정도를 차지하고 있는지 살펴봐야 한다.
    - forcemerge API를 사용하여 세그먼트를 강제 병합하면 세그먼트의 메모리 사용량도 줄일 수 있다.



- 노드의 성능 지표

  - 명령어

  ```bash
  $ curl -XGET 'http://localhost:9200/_nodes/stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_nodes" : {
      "total" : 4,
      "successful" : 4,
      "failed" : 0
    },
    "cluster_name" : "es-docker-cluster",
    "nodes" : {
      "rrqnQp2mRUmPh8OGqTj0_w" : {	// 노드의 ID, 클러스터 내부에서 임의의 값을 부여한다.
        "timestamp" : 1620781452291,
        "name" : "node2",				// 노드의 이름
        "transport_address" : "192.168.240.5:9300",
        "host" : "192.168.240.5",
        "ip" : "192.168.240.5:9300",
        "roles" : [		// 노드가 수행할 수 있는 역할
          "ingest",
          "master",
          "data",
          "ml"
        ],
        "attributes" : {
          "ml.machine_memory" : "134840213504",
          "ml.max_open_jobs" : "20",
          "xpack.installed" : "true"
        },
        "indices" : {
          "docs" : {
            "count" : 9,		// 노드가 지니고 있는 문서의 수
            "deleted" : 1
          },
          "store" : {
            "size_in_bytes" : 70928	// 노드가 저장하고 있는 문서의 크기를 byte 단위로 표시
          },
          "indexing" : {
            "index_total" : 23,		// 지금까지 색인한 문서의 수
            "index_time_in_millis" : 192,	// 색인에 소요된 시간
            // (...)
          },
          "get" : {			// REST API의 GET 요청으로 문서를 가져오는 성능에 대한 지표(검색 성능보다는 문서를 가져오는 성능을 의미한다)
            // (...)
          },
          "search" : {		// 검색 성능과 관련된 지표
            // (...)
          },
          "merges" : {		// 세그먼트 병합과 관련된 성능 지표
            // (...)
          },
          // (...)
          "query_cache" : {		// 쿼리 캐시와 관련된 지표
            // (...)
          },
          "fielddata" : {			// 필드 데이터 캐시와 관련된 지표
            "memory_size_in_bytes" : 0,
            "evictions" : 0
          },
          "completion" : {
            "size_in_bytes" : 0
          },
          "segments" : {			// 노드에서 사용중인 세그먼트와 관련된 지표
            // (...)
          },
          // (...)
        },
        "os" : {
          "timestamp" : 1620781452298,
          "cpu" : {
            "percent" : 3,	// 노드의 CPU 사용률
            "load_average" : {	// 노드의 Load Average 사용률(각 1,5,15분 평균을 의미)
              "1m" : 1.99,
              "5m" : 1.9,
              "15m" : 1.9
            }
          },
          // (...)
          "gc" : {		// GC와 관련된 성능 지표
            "collectors" : {
              "young" : {
                "collection_count" : 317,
                "collection_time_in_millis" : 1595
              },
              "old" : {
                "collection_count" : 3,
                "collection_time_in_millis" : 53
              }
            }
          },
          // (...)
        },
        "thread_pool" : {		// 노드의 스레드 풀 상태
          // (...)
          "search" : {
            "threads" : 73,
            "queue" : 0,
            "active" : 0,
            "rejected" : 0,
            "largest" : 73,
            "completed" : 10917
          },
          // (...)
          "write" : {
            "threads" : 32,
            "queue" : 0,
            "active" : 0,
            "rejected" : 0,
            "largest" : 32,
            "completed" : 32
          }
        },
        "fs" : {
          "timestamp" : 1620781452302,
          "total" : {		// 디스크의 사용량을 의미한다.
            "total_in_bytes" : 1753355112448,
            "free_in_bytes" : 1117627813888,
            "available_in_bytes" : 1028490833920	// 현재 남아 있는 용량
          },
          // (...)
      }
    }
  }
  ```

  - `indexing.index_total`
    - 카운터 형식의 값으로 0부터 계속해서 값이 증가한다.
    - 지금 호출한 값과 1분 후에 호출한 값이 차이가 나며 이 값의 차이가 1분 동안 색인된 문서의 개수를 나타낸다.
    - 색인 성능을 나타내는 매우 중요한 지표 중 하나이다.

  - `thread_pool`
    - 검색에 사용하는 search 스레드, 색인에 사용하는 write 스레드 등  스레드들의 개수와 큐의 크기를 보여준다.
    - rejected가 매우 중요한데, 현재 노드가 처리할 수 있는 양보다 많은 요청이 들어오고 있기 때문에 더 이상 처리할 수 없어서 처리를 거절한다는 의미이기 때문이다.

 

- 인덱스 성능 지표

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-stats.html

  - 위 링크를 확인해보면 각종 parameter들이 있는데 확인을 원하는 파라미터를 입력하면 된다.
  - 쿼리 수, 쿼리 평균 시간 등도 확인 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/<인덱스명>/_stats'
  ```



## tasks API로 task 확인하기

- 진행중인 task 확인

  ```bash
  # 특정 task 조회
  $ curl -XGET 'http://localhost:9200/_tasks/<task_id>'
  
  # 전체 task 조회
  $ curl -XGET 'http://localhost:9200/_tasks'
  ```



- 파라미터

  - actions
    - 콤마로 구분 된 task명이나, 와일드카드 표현식을 사용해서 task를 필터링 할 때 사용한다.

  ```bash
  # 예시
  $ curl -XGET 'http://localhost:9200/_tasks?actions=*bulk'
  ```

  - detalied
    - Boolean 값을 주며, true를 줄 경우 shard recoveries에 대한상세 정보를 함께 반환한다.
    - 기본값은 false이다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_tasks?actions=*bulk&detailed=true'
  ```

  - group_by
    - task들을 grouping하기 위해 사용한다.
    - nodes(기본값): Node ID로 그룹핑한다.
    - parents: parent task ID로 그룹핑한다.
    - none: 그룹핑하지 않는다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_tasks?group_by=parents'
  ```

  - node_id
    - 콤마로 구분 된 노드 ID 또는 노드 이름을 인자로 받는다.
    - 리스트에 포함된 노드의 task만 반환한다.
  - parent_task_id
    - 입력한 Parent task ID에 해당하는 task들만 반환한다.
    - 이 파라미터를 넘기지 않거나 -1을 값으로 주면 모든 task를 반환한다.
  - master_timeout
    - 마스터 노드에 연결되기까지의 기간(기본값은 30s)을 설정한다.
    - 기간 내에 응답이 오지 않으면 errror를 반환한다.
  - wait_for_completion
    - Boolean값을 받으며, true로 줄 경우 operation이 완료될 때 까지 요청이 중단된다.
    - 기본값은 false이다.





## 성능 확인과 문제 해결

- 주요 성능
  - 색인 성능
    - 초당 몇 개의 문서를 색인할 수 있는지, 그리고 각 문서를 색인하는 데 소요되는 시간이 어느 정도인지
    - 클러스터 전체 성능과 노드의 개별 성능으로 나누어 측정한다.
  - 검색 성능
    - 초당 몇 개의 쿼리를 처리할 수 있는지, 그리고 각 쿼리를 처리하는 데 소요되는 시간이 어느 정도인지
    - 클러스터 전체 성능과 노드의 개별 성능으로 나누어 측정한다.
  - GC 성능
    - GC가 너무 자주, 오래 발생하면 Stop-The-World 같은 응답 불가 현상이 발생한다.
    - Stop-The-World가 얼마나 자주, 오래 발생하는지를 나타낸다.
  - rejected
    - 클러스터가 처리할 수 없는 수준의 요청이 들어오면 클러스터는 요청을 거절하게 되는데 그 횟수를 나타낸다.



- 색인 성능

  - `_stats` 를 통해 확인 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_shards" : {
      "total" : 14,
      "successful" : 14,
      "failed" : 0
    },
    "_all" : {
      "primaries" : {		// 프라이머리 샤드에 대한 색인 성능
        "docs" : {
          "count" : 10,
          "deleted" : 1
        },
        "store" : {
          "size_in_bytes" : 92866
        },
        "indexing" : {
          "index_total" : 24,
          "index_time_in_millis" : 209,
          // (...)
        },
        // (...)
      "total" : {		// 전체 샤드에 대한 색인 성능
       // 내용은 primaries와 동일하다.
       //(...)
      }
    }
  }
  ```

  - 성능 측정
    - 위 요청을 10초 간격으로 보냈을 때, 첫 번째 호출시 색인된 문서의 수는 0개, 두 번째 호출시 색인된 문서의 수는 200개 라고 가정
    - 10 초 동안 200개의 문서가 색인됐다고 할 수 있다.
    - 또한 첫 번째 호출시 색인 소요 시간이 0초, 두 번째 호출 시 색인 소요 시간이 100ms라고 가정
    - 즉 10초 동안 200개의 문서를 색인했고, 색인하는데 10ms가 걸렸기 때문에 각각의 문서를 색인하는데 에는 200/100=2ms의 시간이 소요되었음을 알 수 있다.
    - 즉, 이 클러스터의 프라이머리 샤드에 대한 색인 성능은 2ms이다.
    - 색인하는 양이 많으면 많을수록 색인에 소요되는 시간도 늘어나기 때문에 두 값의 절대적인 값보다는 하나의 문서를 색인하는 데 시간이 얼마나 소요되는지를 더 중요한 성능 지표로 삼아야 한다.



- 검색 성능

  - query와 fetch
    - A, B, C 노드가 있을 때 사용자가 search API를 통해 A 노드에 검색 요청을 입력했다고 가정한다.
    - 그럼 노드 A는 자신이 받은 검색 쿼리를 B, C 노드에 전달한다.
    - 각각의 노드는 자신이 가지고 있는 샤드 내에서 검색 쿼리에 해당하는 문서가 있는지 찾는 과정을 진행한다.
    - 이 과정이 query이다.
    - 그리고 이렇게 찾은 문서들을 리스트 형태로 만들어서 정리하는 과정이 fetch이다.
    - 검색은 이렇게 query와 fetch의 과정이 모두 끝나야 만들어지기 때문에 검색 성능을 측정할 때 두 과정을 모두 포함하는 것이 좋다.
  - `_stats`을 통해 확인 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_stats?pretty
  ```

  - 성능 지표

  ```json
  {
    "_shards" : {
      "total" : 14,
      "successful" : 14,
      "failed" : 0
    },
    "_all" : {
      // (...)
        "search" : {
          "open_contexts" : 0,
          "query_total" : 10916,	// 호출하는 시점까지 처리된 모든 query의 총합
          "query_time_in_millis" : 5496,
          "query_current" : 0,
          "fetch_total" : 10915,	// 호출하는 시점까지 처리된 모든 fetch의 총합
          "fetch_time_in_millis" : 476,
          "fetch_current" : 0,
          "scroll_total" : 9741,
          "scroll_time_in_millis" : 18944,
          "scroll_current" : 0,
          "suggest_total" : 0,
          "suggest_time_in_millis" : 0,
          "suggest_current" : 0
        },
      // (...)
      }
    }
  }
  ```

  - 성능 측정
    - 색인 성능 측정과 동일한 방식으로 진행하면 된다.
    - query와 fetch를 나눠서 진행한다.



- GC 성능 측정

  - 각 노드에서 발생하기 때문에 `_nodes/stats`를 통해 확인한다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_nodes/stats?pretty
  ```

  - 성능 지표

  ```json
  // (...)
  "jvm" : {
      // (...)
    "gc" : {
      "collectors" : {
          "young" : {
              "collection_count" : 333,
              "collection_time_in_millis" : 1697
          },
          "old" : {
              "collection_count" : 3,
              "collection_time_in_millis" : 53
          }
      }
  }
  // (...)
  ```

  - 성능 측정
    - 색인과 동일한 방법으로 측정한다.
    - old, young을 각각 측정한다.
    - 상황에 따라 다르지만 보통 수십에서 수백 ms 정도의 성능을 내는 것이 안정적이다.



- rejected 성능 측정

  - rejected 에러
    - ES는 현재 처리할 수 있는 양보다 많은 양의 요청이 들어올 경우 큐에 요청을 쌓아놓는다.
    - 하지만 큐도 꽉 차서 더 이상 요청을 쌓아놓을 수 없으면 rejected 에러를 발생시키며 요청을 처리하지 않는다.
    - 보통 요청이 점차 늘어나서 초기에 구성한 클러스터의 처리량이 부족한 경우나, 평상시에는 부족하지 않지만 요청이 순간적으로 늘어나서 순간 요청을 처리하지 못하는 경우에 발생한다.
  - node별로 측정이 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_nodes/stats?pretty
  ```

  - 성능 지표
    - 각 스레드 별로 확인할 수 있다.

  ```json
  // (...)
  "thread_pool" : {		// 노드의 스레드 풀 상태
      // (...)
      "search" : {
        "threads" : 73,
        "queue" : 0,
        "active" : 0,
        "rejected" : 0,
        "largest" : 73,
        "completed" : 10917
      },
      // (...)
      "write" : {
        "threads" : 32,
        "queue" : 0,
        "active" : 0,
        "rejected" : 0,
        "largest" : 32,
        "completed" : 32
      }
  },
  // (...)
  ```

  - rejected 문제 해결
    - 만일 초기에 구성한 클러스터의 처리량이 부족하다면 데이터 노드를 증설하는 방법 외에는 특별한 방법이 없다.
    - 그러나 순간적으로 밀려들어오는 요청을 처리하지 못한다면 큐를 늘리는 것이 도움이 될 수 있다.
    - ` elasticsearch.yml` 파일에 아래와 같이 설정하면 된다.

  | 스레드 이름         | 스레드 풀 타입        | 설정 방법                                | 예시                                    |
  | ------------------- | --------------------- | ---------------------------------------- | --------------------------------------- |
  | get, write, analyze | fixed                 | thread_pool.[스레드 이름].queue_size     | thread_pool.write.queue_size=10000      |
  | search              | fixed_auto_queue_size | thread_pool.[스레드 이름].max_queue_size | thread_pool.search.max_queue_size=10000 |





# 분석 엔진으로 활용하기

- Elastic Stack이란
  - Elastic Stack은 로그를 수집, 가공하고 이를 바탕으로 분석하는 데 사용되는 플랫폼을 의미한다.
    - 이전에는 Elastic Stack을 ELK Stack이라고 불렀다.
    - Elastic Stack은 가급적 모든 구성 요소의 버전을 통일시키는 것이 좋다.
  - Elastic Stack은 아래와 같다.
    - 로그를 전송하는 Filebeat
    - 전송된 로그를 JSON 형태의 문서로 파싱하는 Logstash
    - 파싱된 문서를 저장하는 Elasticsearch
    - 데이터를 시각화 할 수 있는 kibana
  - Filebeat
    - 지정된 위치에 있는 로그 파일을 읽어서 Logstash 서버로 보내주는 역할을 한다.
    - Filebeat은 로그 파일을 읽기만 하고 별도로 가공하지 않기 때문에, 로그 파일의 포맷이 달라지더라도 별도의 작업이 필요치 않다.
    - 로그 파일의 포맷이 달라지면 로그 파일을 실제로 파싱하는 Logstash의 설정을 바꿔주면 되기 때문에 Filebeat과 Logstash의 역할을 분명하게 나눠서 사용하는 것이 확장성이나 효율성 면에서 좋다.
  - Logstash
    - Filebeat으로부터 받은 로그 파일들을 룰에 맞게 파싱해서 JSON 형태의 문서로 만드는 역할을 한다.
    - 하나의 로그에 포함된 정보를 모두 파싱할 수도 있고, 일부 필드만 파싱해서 JSON 문서로 만들 수도 있다.
    - 파싱할 때는 다양한 패턴을 사용할 수 있으며 대부분 **grok 패턴**을 이용해서 파싱 룰을 정의한다.
    - grok: 비정형 데이터를 정형 데이터로 변경해 주는 라이브러리
  - Elasticsearch
    - Logstash가 파싱한 JSON 형태의 문서를 인덱스에 저장한다.
    - 이 때의 ES는 데이터 저장소 역할을 한다.
    - 대부분의 경우 날짜가 뒤에 붙는 형태로 인덱스가 생성되며 해당 날짜의 데이터를 해당 날짜의 인덱스에 저장한다.
  - Kibana
    - ES에 저장된 데이터를 조회하거나 시각화할 때 사용한다.
    - 데이터를 기반으로 그래프를 그리거나 데이터를 조회할 수 있다.
    - Elastic Stack에서 사용자의 인입점을 맡게 된다.





