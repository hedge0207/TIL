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



# Elasticsearch의 score 계산 방식

> https://wikidocs.net/31698 참고

- TF-IDF(Term Frequency-Inverse Document Frequency)

  - term이 한 문서에서 얼마나 자주 반복되는지와 여러 문서들에서 얼마나 자주 등장하는 term인지가 점수에 영향을 미친다.

    - 하나의 단어가 한 문서 내에서 여러 번 반복되면 점수는 올라가고, 하나의 단어가 여러 문서에서 빈번히 발견될 수록 점수는 낮아진다.

  - 문서 하나를 d, 단어를 t, 문서의 총 개수를 D이라 할 때 TF, DF, IDF는 다음과 같이 정의된다.

    - tf(d, t): 특정한 단어가 문서 내에 얼마나 자주 등장하는지를 나타내는 값.

    - df(t): 특정 단어 t가 전체 문서군 내에서 얼마나 자주 등장하는지를 나타내는 값.
    - idf(d, t): df(t)에 반비례하는 수

  - tf(d, t)의 계산 방식(아래 방식 외에도 무수히 많은 변형이 존재한다)

    - 불린 빈도: t가 d에 한 번이라도 나타나면 1, 아니면 0. 간단하긴 하지만 문서에 단어가 1번 나타나나 1000번 나타나나 차이가 없다는 문제가 있다.
    - 로그 스케일 빈도: `log(f(t,d)+1)`, `f(t,d)`는 문서 d에 t가 등장하는 빈도 수로, 결과값의 크기가 너무 커지지 않게 하기 위해 log를 사용하고, d에 t가 없는 경우 값이 마이너스 무한대로 수렴하는 것을 막기 위해 1을 더해준다. 작은 빈도수 차이일 때는 tf값의 차이가 커지지만, 단어의 빈도가 무수히 늘어날수록 tf의 값의 차이가 크게 벌어지지 않게 된다.
    - 증가빈도: 특정 문서 d에 등장하는 모든 단어의(w) 빈도수를 계산 후 그 최댓값이 분모가 되고, `f(t,d)`는 분자가 된다. 최소 0.5부터 최대 1까지의 값을 가진다. 문서의 길이가 길어 다양한 단어가 나올 때 주로 사용한다.

    $$
    tf(t,d) = 0.5+0.5*\frac{f(t,d)}{max\{f(w,d):w\in d\}} = \frac{f(t,d)}{문서\ 내\ 단어들의\ freq(t,d)중\ 최대값}
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
    - doc1의 메뉴라는 단어는 문서 내에 1번만 등장하므로 분자는 1이 된다.
    - 따라서 doc1에서 메뉴의 tf(d, t)의 값은 1이다.
    - 나머지도 위 과정에 따라 계산하면 아래와 같이 나오게 된다(공백은 최소값은 0.5)
    - 아래에서 짧은 문장에 증가빈도로 계산했을 때의 문제를 알 수 있는데, doc3에서 두 번 등장한 치킨과 doc2에서 한 번 등장한 치킨이 동일한 TF 값을 갖게 된다.

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



- BM25

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
    - bm25를 약간 변형하여 사용한다.
    - `boost * IDF * TF`로 계산한다.
  - Elasticsearch의 IDF 계산
    - `N`은 전체 문서의 개수, `n`은 term을 포함하고 있는 문서의 개수이다.

  $$
  IDF(q_i) = log(1+\frac{N-n+0.5}{n+0.5})
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

  ```bash
  curl -XGET 'http://localhost:9200/_cat/health'
  ```

  - `v` 옵션을 추가
    - 결과 값에 header를 추가해서 보여준다.

  ```bash
  curl -XGET 'http://localhost:9200/_cat/health?v'
  ```

  - format 옵션을 추가
    - 지정한 format으로 보여준다.

  ```bash
  curl -XGET 'http://localhost:9200/_cat/health?format=json'
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

  ```bash
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
  
  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/indices'
  ```
  
  - `s`로 정렬이 가능하다.
  
  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/indices?s=<정렬 할 내용>'
  
  #e.g.
  $ curl -XGET 'http://localhost:9200/_cat/indices?s=docs.count:desc'
  ```
  
  - size를 표시할 때 어떤 단위로 보여줄지 설정이 가능하다.
    - `bytes=<단위>`를 입력하면 된다.
  
  
  ```json
  GET _cat/indices?h=i,p,r,dc,ss,cds&bytes=kb
  ```
  
  - `expand_wildcards` 옵션을 통해 open 상태인 인덱스만 보는 것도 가능하다.
  
  ```json
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

  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/shards'
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
  $ curl -XGET 'http://localhost:9200/_cat/shards?h=index,shard,prirep,unassigned.reason | grep -i UNASSIGNED'
  ```
  
  - 보다 정확한 원인을 알려주는 API
  
  ```bash
  $ curl -XGET 'http://localhost:9200/_cluster/allocation/explain'
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

  - `v`, `h`, `format` 옵션을 모두 사용 가능하다.

  ```bash
  $ curl -XGET 'http://localhost:9200/_cat/segments'
  ```




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



- Elastic Stack의 이중화
  - Elastic Stack의 어느 한 구성 요소에 장애가 발생하더라도 나머지 요소들이 정상적으로 동작할 수 있도록 이중화하는 작업이 반드시 필요하다.
  - 추후 추가



