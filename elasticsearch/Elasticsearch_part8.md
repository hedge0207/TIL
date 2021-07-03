# Field data types

## 기본 타입

- ES에서 선언 가능한 문자열 타입에는 text, keyword 두 가지가 있다.
  - 5.0 버전부터는 텍스트 분석의 적용 여부를 text 타입과 keyword 타입으로 구분한다.
    - 2.X 버전 이전에는 string이라는 하나의 타입만 있었고 텍스트 분석 여부, 즉 애널라이저 적용을 할 것인지 아닌지를 구분하는 설정이 있었다.
  - 인덱스를 생성할 때 매핑에 필드를 미리 정의하지 않으면 동적 문자열 필드가 생성될 때 text 필드와 keyword 필드가 다중 필드로 함께 생성된다.



- text
  - 입력된 문자열을 텀 단위로 쪼개어 역 색인 구조를 만든다.
  - 보통은 풀텍스트 검색에 사용할 문자열 필드들을 text 타입으로 지정한다.
  - text 필드에는 아래와 같은 옵션들을 설정 가능하다.
    - `"analyzer" : "애널라이저명"`:  색인에 사용할 애널라이저를 입력하며 디폴트로는 standard 애널라이저를 사용한다. 토크나이저, 토큰필터들을 따로 지정할 수가 없으며, 필요하다면 사용자 정의 애널라이저를 settings에 정의 해 두고 사용한다.
    - `"search_analyzer" : "애널라이저명"`: 기본적으로 text필드는 match 쿼리로 검색을 할 때 색인에 사용한 동일한 애널라이저로 검색 쿼리를 분석하는데, `search_analyzer`를 지정하면 검색시에는 색인에 사용한 애널라이저가 아닌 다른 애널라이저를 사용한다. 보통 NGram 방식으로 색인을 했을 때는 지정 해 주는 것이 바람직하다.
    - `"index" : <true | false>`: 디폴트는 true이고, false로 설정하면 해당 필드는 역 색인을 만들지 않아 검색이 불가능해진다.
    - `"boost" : 숫자 값`: 디폴트는 1이다. 값이 1 보다 높으면 풀텍스트 검색 시 해당 필드 스코어 점수에 가중치를 부여하고, 1 보다 낮은 값을 입력하면 가중치가 내려간다.
    - `"fielddata" : <true | false>`: 디폴트는 false이고, true로 설정하면 해당 필드의 색인된 텀들을 가지고 집계 또는 정렬이 가능하다. 이 설정은 동적으로 변경하는 것이 가능하다.



- keyword

  - 입력된 문자열을 하나의 토큰으로 저장한다.
    - text 타입에 keyword 애널라이저를 적용한 것과 동일하다
  - 보통은 집계 또는 정렬에 사용할 문자열 필드를 keyword 타입으로 지정한다.
  - keyword 필드에는 다음과 같은 옵션들을 설정할 수 있다.
    - `index`,`boost` 옵션은 text와 동일하다.
    - `"doc_values" : <true | false>`: 디폴트는 true이며, keyword 값들은 기본적으로 집계나 정렬에 메모리를 소모하지 않기 위해 값들을 doc_values라고 하는 별도의 열 기반 저장소를 만들어 저장하는데, 이 값을 false로 하면 doc_values에 값을 저장하지 않아 집계나 정렬이 불가능해진다.
    - `"ignore_above" : 자연수`: 디폴트는 2,147,483,647이며 다이나믹 매핑으로 생성되면 256으로 설정된다. 설정된 길이 이상의 문자열은 색인을 하지 않아 검색이나 집계가 불가능하다. `_source`에는 남아있기 때문에 다른 필드 값을 쿼리해서 나온 결과로 가져오는 것은 가능하다.
    - `"normalizer" : 노멀라이저명`: keyword 필드는 애널라이저를 사용하지 않는 대신 노멀라이저의 적용이 가능하다. 노멀라이저는 애널라이저와 유사하게 settings에서 정의하며 토크나이저는 적용할 수 없고 캐릭터 필드와 토큰 필터만 적용해서 사용이 가능하다.
  - text와 keyword의 차이
    - 동적 매핑으로 문자열 필드를 생성하여 아래와 같이 text, keyword가 모두 생성된 경우, `필드`, `필드.keyword`로 모두 검색이 가능하다.
    - 그러나 text, keyword 필드에 검색했을 때 각기 다른 결과가 나오게 된다.
    - 상기했듯 text 필드는 문자열을 텀 단위로 쪼개기에 watching, movie 어느 것을 입력하든 watcing movie라는 문자열을 검색이 가능하다. 
    - 그러나 keyword 필드는 문자열을 하나의 토큰으로 저장하기에 watcing movie로 입력해야만 watcing movie라는 문자열을 검색이 가능하다.

  ```bash
  # 데이터 넣기
  $ curl -XPOST "localhost:9200/test/_doc" -H 'Content-type: application/json' -d '
  {
    "hobby":"watching movie"
  }'
  
  
  # 매핑 정보 확인
  $ curl -XGET "localhost:9200/nation3/_mapping"
  {
    "nation3" : {
      "mappings" : {
        "properties" : {
          "hobby" : {
            "type" : "text",		#  text 필드와
            "fields" : {
              "keyword" : {		# keyword 필드 모두 생성된다.
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          }
        }
      }
    }
  }
  
  
  # text 필드 검색
  $ curl -XGET "localhost:9200/test/_search" -H 'Content-type: application/json' -d '
  {
    "query":{
      "match": {
        "hobby": "watching"
      }
    }
  }'
  # 응답(검색 결과가 나온다)
  {
    ...
    "hits" : {
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.2876821,
      "hits" : [
        {
          "_index" : "nation2",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 0.2876821,
          "_source" : {
            "hobby" : "watching movie"
          }
        }
      ]
    }
  }
  
  
  # keyword 필드 검색
  $ curl -XGET "localhost:9200/test/_search" -H 'Content-type: application/json' -d '
  {
    "query":{
      "match": {
        "hobby.keyword": "watching"
      }
    }
  }'
  # 검색 결과가 나오지 않는다.
  
  
  # 아래와 같이 검색해야 결과가 나온다.
  $ curl -XGET "localhost:9200/test/_search" -H 'Content-type: application/json' -d '
  {
    "query":{
      "match": {
        "hobby.keyword": "watching movie"
      }
    }
  }'
  ```



- 숫자

  - ES는 JAVA에서 사용되는 숫자 타입들을 지원한다.
  - 또한 half_float, scaled_float과 같이 ES에서만 사용되는 타입들도 존재한다.
  - 종류
    - JAVA에서 사용되는 숫자 타입들: long, integer, short, byte, double, float
    - ES에서만 지원하는 숫자 타입들: half_float, scaled_float

  - 사용 가능한 옵션들
    - `"index"`, `"doc_values"`, `"boost"` 등의 옵션들은 text, keyword 필드의 옵션들과 동일하다.
    - `"cource": <true | false>`: 디폴트는 true이며, 숫자 필드들은 기본적으로 숫자로 이해될 수 잇는 값들은 숫자로 변경해서 저장한다. 이를 false로 설정하면 정확한 타입으로 입력되지 않으면 오류가 발생한다. 
    - `"null_value": 숫자값`: 필드값이 입력되지 않거나 null인 경우 해당 필드의 디폴트 값을 지정한다. 
    - `"ignore_malformed": <true | false>`: 디폴트는 false로, 기본적으로 숫자 필드에 숫자가 아닌 불린 값이 들어오면 ES는 오류를 반환하는데, true로 설정하면 숫자가 아닌 값이 들어와도 도큐먼트를 정상적으로 저장한다. 해당 필드의 값은 `_source`에만 저장되고 겁색이나 집계에는 무시된다.
    - `"scaling_fator": 10의 배수`: scaled_float을 사용하려면 필수로 지정해야 하는 옵션으로 소수점 몇 자리까지 저장할지를 지정한다. 12.345라는 값을 저장하는 경우 `scaling_fator:10`과 같이 설정하면 실제로는 12.3이 저장되고, `scaling_fator:100`과 같이 설정했으면 12.34가 저장된다.

  - 전처리된 데이터가 아니면 항상 `_source`의 값은 변경되지 않는다.
    - `"cource": true`로 "4.5"라는 숫자가 integer 필드에 정상적으로 저장 되어도 `_source`의 값은 그대로 "4.5"이다.
    - `"null_value"`를 설정해도 역시 마찬가지로 `_source`에는 여전히 null로 표시된다.
  - `_source`에 저장된 값과 필드에 저장된 값이 다를 수 있다.
    - 예를 들어 byte 타입을 가진 필드에 4.5를 저장하는 경우에 byte는 오직 정수만을 저장하므로 4가 들어가게 된다.
    - 그러나 `_source`에는 4.5로 값이 들어가 있다.
    - 이 때 집계를 위해 3보다 크고 4.1보다 작은 값을 검색하면 4.5는 4.1보다 큼에도 필드에는 4로 저장되어 있으므로 검색이 되게 된다.
    - 이러한 이유로 숫자 필드를 동적으로 생성하는 것은 매우 위험하다.



- 날짜

  - ES에서 날짜 타입은 ISO8601 형식을 따라 입력한다.
    - "2021-03-18"
    - "2021-03-18T10:08:40"
    - "2021-03-18T10:08:40+09:00"
    - "2021-03-18T10:08:40.428Z"
    - ISO8601 형식을 따르지 않을 경우 text,keyword로 저장된다.
  - ISO8601외에도 long 타입 정수인 epoch_millis 형태의 입력도 가능하다.
    - epoch_millis는 1970-01-01 00:00:00부터의 시간을 밀리초 단위로 카운트 한 값이다.
    - 필드가 date 형으로 정의 된 이후에는 long 타입의 정수를 입력하면 날짜 형태로 저장이 가능하다.
    - epoch_millis외에도 epoch_second의 사용이 가능하다.
    - 사실 날짜 필드는 내부에서는 모두 long 형태의 epoch_millis로 저장한다.
  - 그 외에 사용 가능한 포맷들
    - 매핑의 format 형식만 지정 해 놓으면 지정된 어떤 형식으로도 색인 및 쿼리가 가능하다.
    - basic_date, strict_date_time과 같이 미리 정의 된 포맷들
    - [joda.time.format](https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html) 심볼을 사용하여 지정 가능하다.
    - 정의된 포맷들은  [Elastic 홈페이지의 공식 도큐먼트](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html#built-in-date-formats)에서 볼 수 있으며 joda 심볼 기호들은 다음과 같다.

  | 심볼 | 의미                 | 예시) 2019-09-12T17:13:07.428+09.00 |
  | ---- | -------------------- | ----------------------------------- |
  | yyyy | 년도                 | 2019                                |
  | MM   | 월-숫자              | 09                                  |
  | MMM  | 월-문자(3자리)       | Sep                                 |
  | MMMM | 월-문자(전체)        | September                           |
  | dd   | 일                   | 12                                  |
  | a    | 오전/오후            | PM                                  |
  | HH   | 시각(0~23)           | 17                                  |
  | kk   | 시각(01-24)          | 17                                  |
  | hh   | 시각(01-12)          | 05                                  |
  | h    | 시각(1-12)           | 5                                   |
  | mm   | 분(00~59)            | 13                                  |
  | m    | 분(0~59)             | 13                                  |
  | ss   | 초(00~59)            | 07                                  |
  | s    | 초(0~59)             | 7                                   |
  | SSS  | 밀리초               | 428                                 |
  | Z    | 타임존               | +0900/+09:00                        |
  | e    | 요일(숫자 1:월~7:일) | 4                                   |
  | E    | 요일(텍스트)         | Thu                                 |

  - 사용 가능한 옵션들
    - `"doc_values"`, `"index"`, `"null_value"`, `"ignore_malformed"` 옵션들은 문자열, 숫자 필드와 기능이 동일하다.
    - `"format": "문자열 || 문자열..."`: 입력 가능한 날짜 형식을 ||로 구분해서 입력한다.



- boolean
  - true, false 두 가지 값을 갖는 필드 타입이다.
  - "true"와 같이 문자열로 입력되어도 boolean으로 해석되어 저장된다.
  - 불리언 필드를 사용할 때는 일반적으로 term 쿼리를 이용해서 검색을 한다.
  - 사용 가능한 옵션들
    - `"doc_values"`, `"index"` 옵션들은 문자열, 숫자 필드와 기능이 동일하다.
    - `"null_value": true|false`: 필드가 존재하지 않거나 값이 null일 때 디폴트 값을 지정한다. 지정하지 않으면 불리언 필드가 없가나 값이 null인 경우 존재하지 않는 것으로 처리되어 true/false 모두 쿼리나 집계에 나타나지 않는다.



- Object

  - JSON에서는 한 필드 안에 하위 필드를 넣는 object, 즉 객체 타입의 값을 사용할 수 있다.
    - 보통은 한 요소가 여러 하위 정보를 가지고 있는 경우 object 타입 형태로 사용한다.
  - object 필드를 선언할 때는 다음과 같이 `"properties"`를 입력하고 그 아래에 하위 필드 이름과 타입을 지정한다.

  ```bash
  $ curl -XPUT 'localhost:9200/movies?pretty' -H 'Content-Type: application/json' -d '{
    "mappings": {
      "properties": {
        "characters": {
          "properties": {
            "name": {
              "type": "text"
            },
            "age": {
              "type": "byte"
            },
            "side": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }
  ```

  - object 필드를 쿼리로 검색하거나 집계를 할 때는 `.`를 이용해서 하위 필드에 접근한다.

  ```bash
  $ curl "http://localhost:9200/movie/_search" -H 'Content-Type: application/json' -d'
  {  
  	"query": {    
  		"match": { 
  			"characters.name": "Iron Man" 
          }
      }
  }'
  ```

  - 역색인 방식
    - 역 색인은 필드 별로 생성된다.
    - 즉 object 필드 내부의 값이 각기 따로 따로 역색인 구조를 갖는 것이 아니라 하나의 역색인 구조를 갖게 된다.
    - 아래와 같이 데이터를 입력하고, 검색을 하면 `characters.name`이 Loki 이면서 `characters.side`가 villain인 1번 문서만 검색 될 것 같지만 막상 검색을 해보면 둘 다 검색된다.

  ```bash
  # 아래와 같이 2개의 문서를 삽입
  curl -XPUT 'localhost:9200/movies/_doc/1?pretty' -H 'Content-Type: application/json' -d '
  {
    "title": "The Avengers",
    "characters": [
      {
        "name": "Iron Man",
        "side": "superhero"
      },
      {
        "name": "Loki",
        "side": "villain"
      }
    ]
  }
  
  curl -XPUT 'localhost:9200/movies/_doc/2?pretty' -H 'Content-Type: application/json' -d '
  {
    "title": "Avengers: Infinity War",
    "characters": [
      {
        "name": "Loki",
        "side": "superhero"
      },
      {
        "name": "Thanos",
        "side": "villain"
      }
    ]
  }'
  
  # 위에서 삽입한 문서를 검색
  $ curl "http://localhost:9200/movie/_search" -H 'Content-Type: application/json' -d'
  {
    "query": {
      "bool": {
        "must": [
          {
            "match": {
              "characters.name": "Loki"
            }
          },
          {
            "match": {
              "characters.side": "villain"
            }
          }
        ]
      }
    }
  }'
  ```



- Nested

  - 만약에 object 타입 필드에 있는 여러 개의 object 값들이 서로 다른 역 색인 구조를 갖도록 하려면 nested 타입으로 지정해야 한다.
  - nested 타입으로 지정하려면 매핑이 다음과 같이 `"type":"nested"`를 명시한다.
  - 다른 부분은 object와 동일하다.

  ```bash
  curl -XPUT "http://localhost:9200/movie" -H 'Content-Type: application/json' -d'{
  "mappings":{    
    "properties":{      
      "characters":{        
        "type": "nested",        
          "properties": {          
            "name": {            
              "type": "text"          
            },          
            "side": {            
              "type": "keyword"          
            }        
          }      
        }    
      }   
    }
  }'
  ```

  - nested 필드를 검색 할 때는 반드시 nested 쿼리를 써야 한다. 
    - nested 쿼리 안에는 path 라는 옵션으로 nested로 정의된 필드를 먼저 명시하고 그 안에 다시 쿼리를 넣어서 입력한다.
    - nested 쿼리로 검색하면 nested 필드의 내부에 있는 값 들을 모두 별개의 도큐먼트로 취급한다.
    - object 필드 값들은 실제로 하나의 도큐먼트 안에 전부 포함되어 있다.
    - nested 필드 값들은 내부적으로 별도의 도큐먼트로 분리되어 저장되며 쿼리 결과에서 상위 도큐먼트와 합쳐져서 보여지게 된다.

  - 역색인 방식
    - Object 타입과 달리 필드 내부의 값들이 각각 역색인 된다.
    - 따라서 아래와 같은 검색 쿼리를 보내면 `characters.name`이 Loki 이면서 `characters.side`가 villain인 1번 문서만 검색되게 된다.

  ```bash
  # 인덱스 생성
  curl -XPUT 'localhost:9200/movies' -H 'Content-Type: application/json' -d '
  {
    "mappings": {
      "properties": {
        "characters": {
          "type": "nested",
          "properties": {
            "name": {
              "type": "text"
            },
            "side": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }'
  
  # 데이터 삽입
  curl -XPUT 'localhost:9200/movies/_doc/1?pretty' -H 'Content-Type: application/json' -d '
  {
    "title": "The Avengers",
    "characters": [
      {
        "name": "Iron Man",
        "side": "superhero"
      },
      {
        "name": "Loki",
        "side": "villain"
      }
    ]
  }
  
  curl -XPUT 'localhost:9200/movies/_doc/2?pretty' -H 'Content-Type: application/json' -d '
  {
    "title": "Avengers: Infinity War",
    "characters": [
      {
        "name": "Loki",
        "side": "superhero"
      },
      {
        "name": "Thanos",
        "side": "villain"
      }
    ]
  }'
  
  # nested query를 사용하여 검색
  $ curl -XGET "http://localhost:9200/movie/_search" -H 'Content-Type: application/json' -d'
  {
    "query": {
      "nested": {
        "path": "characters",
        "query": {
          "bool": {
            "must": [
              {
                "match": {
                  "characters.name": "Loki"
                }
              },
              {
                "match": {
                  "characters.side": "villain"
                }
              }
            ]
          }
        }
      }
    }
  }'
  ```



## 심화 타입

- histogram
  - 도수분포표를 그림으로 나타낸 것
  - ES에서의 histogram은 사전 집계된 숫자 데이터들을 저장하는 필드이다.
  - 두 쌍의 배열로 정의된다.
    - `values` 배열은 히스토그램의 버킷을 나타내는 `double` 타입의 숫자값들로, 반드시 오름차순으로 정렬되어 있어야 한다.
    - `counts` 배열은 각 버킷에 얼마나 많은 값들이 들어 있는지를 나타내는 `integer` 타입의 숫자값들로, 0 이상의 정수여야 한다.
    - 두 배열의 각 요소는 위치를 기반으로 대응하므로, 두 배열의 길이는 항상 같아야 한다.



- Geo
  - 위치 정보를 저장할 수 있는 Geo Point와 Geo Shape 같은 타입들이 있다.
  - Geo Point
    - 위도(latitude)와 경도(longitude) 두 개의 실수 값을 가지고 지도 위의 한 점을 나타내는 값이다.
  - Geo point는 다양한 방법으로 입력이 가능하다.





### Join filed type

- 한 인덱스의 documents 내부에서 부모/자식 관계를 생성하는 필드

  - `relations` 부분은 문서 내부의 관계를 설정하는 부분이다.
    - 각각의 관계는 `<부모 이름>:<자식 이름>`의 형태로 정의된다.
    - 만일 복수의 자식을 설정 할 경우 `<부모 이름>:<[자식 이름1, 자식 이름2, ...]>`와 같이 정의한다.
  - parent-join은 인덱스에 필드를 하나 생성한다(하나의 관계 당 하나의 필드가 생성된다).
    - 생성되는 필드의 이름은 `<관계 이름>#<부모 이름>` 형식이다.
    - 자식 문서의 경우, 필드는 해당 문서와 연결된 parent `_id` 값을 포함한다.

  - 예시

  ```bash
  # 하나의 부모와 하나의 자식
  $ curl -XPUT "http://localhost:9200/my-index" -H 'Content-Type: application/json' -d'
  {
    "mappings": {
      "properties": {
        "my_id": {
          "type": "keyword"
        },
        "my_join_field": {
          "type": "join",
          "relations": {
            "question": "answer" # 부모인 question과 자식인 answer로 관계를 정의
          }
        }
      }
    }
  }'
  
  # 하나의 부모와 복수의 자식
  $ curl -XPUT "http://localhost:9200/my-index" -H 'Content-Type: application/json' -d'
  {
    "mappings": {
      "properties": {
        "my_id": {
          "type": "keyword"
        },
        "my_join_field": {
          "type": "join",
          "relations": {
            "question": ["answer","comment"]
          }
        }
      }
    }
  }'
  
  # 더 높은 레벨의 부모와 자식 관계 설정
  $ curl -XPUT "http://localhost:9200/my-index" -H 'Content-Type: application/json' -d'
  {
    "mappings": {
      "properties": {
        "my_join_field": {
          "type": "join",
          "relations": {
            "question": ["answer", "comment"],  
            "answer": "vote" 
          }
        }
      }
    }
  }'
  
  # 위의 경우 아래와 같은 관계가 설정 된 것이다.
  # question → answer → vote
  #          ↘ comment
  ```



- 색인

  - 부모 문서를 색인하기 위해서는 관계의 이름과 부모의 이름을 입력해야 한다.
    - 아래 예시는 2 개의 부모 문서를 색인하는 예시이다.
    - 부모 문서를 색인할 때에는 축약하는 것이 가능하다.

  ```bash
  $ curl -XPUT "http://localhost:9200/my-index/_doc/1" -H 'Content-Type: application/json' -d'
  {
    "my_id": "1",
    "text": "This is a question",
    # 관계의 이름을 입력
    "my_join_field": {
      "name": "question" # 부모를 입력
    }
    # 아래와 같이 축약하는 것이 가능하다.
    # "my_join_field": "question"
  }'
  
  $ curl -XPUT "http://localhost:9200/my-index/_doc/1" -H 'Content-Type: application/json' -d'
  {
    "my_id": "2",
    "text": "This is another question",
    # 관계의 이름을 입력
    "my_join_field": {
      "name": "question" # 부모를 입력
    }
  }'
  ```

  - 자식 문서를 색인할 때는 관계의 이름과 부모 문서의 parent id, 그리고 자식의 이름이 입력되어야 한다.
    - 또한 부모 문서와 같은 샤드에 할당되어야 하므로 `routing=`을 통해 같은 샤드에 할당될 수 있도록 설정해준다.
    - 아래 예시는 두 개의 자식 문서를 색인하는 예시이다.

  ```bash
  $ curl -XPUT "http://localhost:9200/my-index/_doc/3?routing=1" -H 'Content-Type: application/json' -d'{  "my_id": "3",  "text": "This is an answer",  "my_join_field": {    "name": "answer",     "parent": "1" # parent id를 입력  }}'$ curl -XPUT "http://localhost:9200/my-index/_doc/4?routing=1" -H 'Content-Type: application/json' -d'{  "my_id": "4",  "text": "This is another answer",  "my_join_field": {    "name": "answer",    "parent": "1"  }}'
  ```

- Join filed 와 성능

  - 관계형 DB의 join과  동일하게 사용하는 것이 아니다.
    - ES에서 성능 향상의 핵심은 데이터를 비정규화하는 것이다.
    - 각각의 join field에서 `has_child`나 `has_parent` 쿼리를 추가하는 것은 쿼리 성능에 상당한 악영향을 미친다.
  - join field를 사용할만한 유일한 경우는 한 인터티가 다른 엔터티보다 훨씬 많은 일대 다 관계가 포함된 경우뿐이다.
    - 예를 들어 환자와 병원의 수가 있을 때, 환자의 수가 병원의 수 보다 훨씬 많다면 병원을 parent로, 환자를 child로 설정할 수 있다. 



- Parent-join의 제약사항
  - 한 인덱스에 오직 하나의 join field만 정의해야한다.
  - 이미 존재하는 join 필드에 새로운 관계를 추가하는 것은 가능하다.
  - 부모 문서와 자식 문서는 반드시 같은 샤드에 색인되어야 한다. 따라서 자식 문서를 색인, 조회, 삭제, 수정시에 같은 routing value가 입력되어야 한다.
  - 각 요소는 여러 자식을 가질 수 있지만, 부모는 오직 하나만 지닐 수 있다.
  - 부모 요소에 자식 요소를 추가하는 것이 가능하다.



- Global ordinals

  - join field는 join의 속도 향상을 위해서 [global ordinals](https://www.elastic.co/guide/en/elasticsearch/reference/current/eager-global-ordinals.html)을 사용한다.
    - global ordinals은 샤드에 변경이 있을 때마다 리빌드된다.
    - 따라서 더 많은 parent id가 샤드에 저장될 수록, 리빌드에도 더 많은 시간이 걸리게 된다.
    - 만약 인덱스가 변경되면,  global ordinals 역시 refresh의 일부로서 리빌드 된다.
    - 이는 refresh 시간에 상당한 영향을 미치게 된다.
    - 그러나 이는 어쩔 수 없다.
  - 만일 join 필드를 자주 사용하지는 않지만, join 필드에 값을 빈번하게 추가해야 할 경우 아래와 같이 `eager_global_ordinals`를 false로 주는 것이 좋다.

  ```bash
  $ curl -XPUT "http://localhost:9200/my-index" -H 'Content-Type: application/json' -d'{  "mappings": {    "properties": {      "my_join_field": {        "type": "join",        "relations": {           "question": "answer"        },        "eager_global_ordinals": false      }    }  }}
  ```

  - global ordinals의 heap 사용량을 체크

  ```bash
  # Per-indexGET _stats/fielddata?human&fields=my_join_field#question# Per-nodeGET _nodes/stats/indices/fielddata?human&fields=my_join_field#question
  ```



- 검색

  - 일반적인 쿼리로 검색

  ```bash
  $ curl -XGET "http://localhost:9200/my-index/_search" -H 'Content-Type: application/json' -d'{  "query": {    "match_all": {}  }}'# 응답{  (...),    "hits" : [      {        "_index" : "test-join-field",        "_type" : "_doc",        "_id" : "2",        "_score" : null,        "_source" : {          "my_id" : "1",          "text" : "This is another question",          "my_join_field" : {            "name" : "question"  # question join에 속해 있다.          }        }      },      {(...)},      {        "_index" : "test-join-field",        "_type" : "_doc",        "_id" : "3",        "_score" : null,        "_routing" : "1",        "_source" : {          "my_id" : "3",          "text" : "This is a answer",          "my_join_field" : {            "name" : "answer",	# answer join에 속해 있다.            "parent" : "1"		# parent id          }        }      },      {(...)}    ]  }}
  ```

  - Parent ID query
    - 특정 parent document와 연결되어 있는 child documents를 반환하는 쿼리
    - `type`에는 자식의 이름을, `id`에는 부모 문서의 id를 적는다.
    - `ignore_unmapped` 파라미터를 줄 수 있는데(선택), 만일 이를 True로 줄 경우 `type`에 자식의 이름이 아닌 값을 줄 경우 error가 발생하고, False로 줄 경우에는 아무 문서도 반환하지 않는다(기본값은 False)

  ```bash
  $ curl -XGET "http://localhost:9200/my-index/_search" -H 'Content-Type: application/json' -d'{  "query": {      "parent_id": {          "type": "answer",          "id": "1"      }  }}'
  ```

  - Has child query
    - 쿼리에 일치하는 child documents와 연결 된 부모 document를 반환한다.
    - `type`, `ignore_unmapped`는 Parent ID query와 동일하다.
    - `max_children`: 쿼리와 일치하는 child documents의 최댓값을 지정, 만일 이 값보다 쿼리와 일치하는 child documents의 수가 많다면, 해당 child documents의 parent document는 반환되지 않는다.
    - `min_children`: 쿼리와 일치하는 child documents의 최솟값을 지정, 만일 이 값보다 쿼리와 일치하는 child documents의 수가 적다면, 해당 child documents의 parent document는 반환되지 않는다.
    - `score_mode`: 쿼리에 매칭된 child documents들의 점수가 어떻게 parent documents들의 관련성 점수에 영향을 줄 것인지를 결정한다. 기본 값은 None으로, avg, sum, min, max 등을 설정 가능하다.
    - `has_child` 쿼리는 일반적인 정렬로는 정렬할 수 없고, function_score를 사용하여 정렬해야 한다.

  ```bash
  $ curl -XGET "http://localhost:9200/my-index/_search" -H 'Content-Type: application/json' -d'{  "query": {    "has_child": {      "type": "answer",      "query": {        "match_all": {}      },      "max_children": 10,      "min_children": 2,      "score_mode": "min"    }  }}'
  ```

  - Has parent  query
    - 쿼리와 일치하는 parent document와 연결된 child documents를 반환한다.
    - `parent_type`에는 부모의 이름을 입력한다.
    - `ignore_unmapped`는 Parent ID query와 동일하다.
    - `score`: 쿼리와 일치하는 parent document의 관련성 점수가 child documents에서 집계 될지를 결정한다(기본값은 False)
    - 마찬가지로 일반적인 정렬로는 정렬할 수 없고, function_score를 사용하여 정렬해야 한다.

  ```bash
  $ curl -XGET "http://localhost:9200/my-index/_search" -H 'Content-Type: application/json' -d'{  "query": {    "has_parent": {      "parent_type": "question",      "query": {        "match_all": {}      }    }  }}
  ```

  - Parent-join 쿼리와 집계
    - join 필드의 값은 aggs와 scripts에서 접근이 가능하다.

  ```bash
  $ curl -XGET "http://localhost:9200/my-index/_search" -H 'Content-Type: application/json' -d'{  "query": {    "parent_id": {       "type": "answer",      "id": "1"    }  },  "aggs": {    "parents": {      "terms": {        "field": "my_join_field#question",         "size": 10      }    }  },  "runtime_mappings": {    "parent": {      "type": "long",      "script": """        emit(Integer.parseInt(doc['my_join_field#question'].value))      """    }  },  "fields": [    { "field": "parent" }  ]}'
  ```





