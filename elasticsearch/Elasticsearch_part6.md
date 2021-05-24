# Aggregations

- aggregations
  - ES에서 데이터의 다양한 연산을 가능하게 해주는 기능
  - aggregations 또는 aggs로 표기한다.



- 기본형

  - search API에서 query 문과 같은 수준에 지정자 `aggregations ` 또는 `aggs`를 명시한다.
  - 꼭 query문을 함께 사용할 필요는 없다.

  ```bash
  $ curl -XGET "localhost:9200/<인덱스명>/_search" -H 'Content-type:application/json' -d'
  {
    "query": {
      # [query 문]
    },
    "aggs": {
      "[사용자가 지정한 aggs 이름]": {
        "[aggregation 종류(type)]": {
          # [aggs 문]
        }
      }
    }
  }
  '
  ```

  - 종류
    - Metric: 수학적 계산을 위한 aggregation
    - Bucket: 필드의 값을 기준으로 문서들을 그룹화해주는 aggregation
    - Pipeline: 문서나 필드가 아닌 다른 aggregation 데이터를 가지고 집계를 해주는 aggregation
  - 응답
    - search API의 응답으로 오는 object 중 `aggregations`라는 key와 묶여서 온다.

  ```json
  {
    "took": 78,
    "timed_out": false,
    "_shards": {
      "total": 1,
      "successful": 1,
      "skipped": 0,
      "failed": 0
    },
    "hits": {
      "total": {
        "value": 5,
        "relation": "eq"
      },
      "max_score": 1.0,
      "hits": [...]
    },
    "aggregations": {		// aggregations 응답
      "my-agg-name": {    // 사용자가 설정한 aggs 이름    
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": []
      }
    }
  }
  ```

  - aggregations만 응답으로 받기
    - `size`를 0으로 설정하면 aggregations만 응답으로 받을 수 있다.

  ```bash
  $ curl -XGET "localhost:9200/<인덱스명>/_search" -H 'Content-type:application/json' -d'
  {
    "size": 0,
    "aggs": {
      "[사용자가 지정한 aggs 이름]": {
        "[aggregation 종류(type)]": {
          # [aggs 문]
        }
      }
    }
  }
  '
  ```

  - aggregations type도 응답으로 받기
    - aggregations은 기본값으로 aggregation의 이름만 반환한다.
    - type도 함께 반환받기 위해서는 아래와 같이 `typed_keys`를 요청에 포함시키면 된다.
    - `type#aggs 이름` 형태로 이름과 타입을 함께 반환한다.

  ```bash
  $ curl -XGET "localhost:9200/<인덱스명>/_search?typed_keys" -H 'Content-type:application/json' -d'
  {
    "size": 0,
    "aggs": {
      "my-aggs": {
        "histogram": {	# histogram type
          "field":"my-field",
          "interval":1000
        }
      }
    }
  }
  '
  
  # 응답
  {
    ...
    "aggregations": {
      "histogram#my-agg-name": {                 
        "buckets": []
      }
    }
  }
  ```



- multiple & sub  aggregations

  - 여러 개의 aggregations 실행하기

  ```bash
  $ curl -XGET "localhost:9200/<인덱스명>/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "[사용자가 지정한 aggs 이름1]": {
        "[aggregation 종류(type)]": {
          # [aggs 문]
        }
      },
      "[사용자가 지정한 aggs 이름2]": {
        "[aggregation 종류(type)]": {
          # [aggs 문]
        }
      }
    }
  }
  '
  ```

  - sub-aggregations 실행하기
    - Bucket aggregations는 Bucket 혹은 Metric sub-aggregations을 설정 가능하다.
    - 깊이에 제한이 없이 Bucket aggregations이기만 하면 sub-aggregations을 설정 가능하다.

  ```bash
  $ curl -XGET "localhost:9200/<인덱스명>/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "my-bucket-aggs": {
        "[aggregation 종류(type)]": {
          # [aggs 문]
        },
        "my-sub-aggs": {	# sub-aggregations 설정
          "[aggregation 종류(type)]": {
            # [aggs 문]
          }
        }
      }
    }
  }
  '
  ```



- metadata를 추가하기

  - `meta` 오브젝트를 사용하여 metadata를 추가하는 것이 가능하다.

  ```bash
  $ curl -XGET "localhost:9200/<인덱스명>/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "[사용자가 지정한 aggs 이름]": {
        "[aggregation 종류(type)]": {
          # [aggs 문]
        }
      },
      "meta":{
      	"my-metadata-field":"foo"
      }
    }
  }
  '
  ```



- script 사용하기

  - field 중 집계에 원하는 필드가 없을 경우 runtime field에서 script를 사용할 수 있다.
    - runtime field: 쿼리를 처리할 때 평가되는 필드
    - reindexing 하지 않고도 문서에 필드를 추가할 수 있게 해준다.
    - 단, script를 사용할 경우 aggregation에 따라 성능에 영향을 줄 수 있다.
  - 예시

  ```bash
  $ curl -XGET "localhost:9200/<인덱스명>/_search" -H 'Content-type:application/json' -d'
  {
    "runtime_mappings": {
      "message.length": {
        "type": "long",
        "script": "emit(doc['message.keyword'].value.length())"
      }
    },
    "aggs": {
      "message_length": {
        "histogram": {
          "interval": 10,
          "field": "message.length"
        }
      }
    }
  }
  '
  ```



- aggregation cache
  - 빈번하게 실행되는 aggregations의 결과는 shard request cache에 캐싱한다.
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-shard-routing.html#shard-and-node-preference 참고



-  집계 예시를 위한 데이터 추가

  - nations라는 인덱스에 bulk API를 활용하여 데이터 추가

  ```bash
  $curl -XPUT "localhost:9200/nations/_bulk?pretty" -H 'Content-type:application/json' -d'
  {"index": {"_id": "1"}}
  {"date": "2019-06-01", "continent": "아프리카", "nation": "남아공", "population": 4000}
  {"index": {"_id": "2"}}
  {"date": "2019-06-01", "continent": "아시아", "nation": "한국", "population": 5412}
  {"index": {"_id": "3"}}
  {"date": "2019-07-10", "continent": "아시아", "nation": "싱가폴", "population": 3515}
  {"index": {"_id": "4"}}
  {"date": "2019-07-15", "continent": "아시아", "nation": "중국", "population": 126478}
  {"index": {"_id": "5"}}
  {"date": "2019-08-07", "continent": "아시아", "nation": "일본", "population": 12821}
  {"index": {"_id": "6"}}
  {"date": "2019-08-18", "continent": "북아메리카", "nation": "미국", "population": 21724}
  {"index": {"_id": "7"}}
  {"date": "2019-09-02", "continent": "북아메리카", "nation": "캐나다", "population": 9912}
  {"index": {"_id": "8"}}
  {"date": "2019-09-11", "continent": "유럽", "nation": "영국", "population": 7121}
  {"index": {"_id": "9"}}
  {"date": "2019-09-20", "continent": "유럽", "nation": "프랑스", "population": 9021}
  {"index": {"_id": "10"}}
  {"date": "2019-10-01", "continent": "유럽", "nation": "독일", "population": 1271}
  '
  ```



## Metrics aggregations

- Metrics aggregations
  - 집계된 문서에서 추출된 값을 기반으로 수학적 계산을 수행한다.
    - 일반적으로 문서에서 추출한 값을 기반으로 계산을 수행하지만 script를 활용하여 생성한 필드에서도 수행이 가능하다.
  - Numeric metrics aggregations
    - 숫자를 반환하는 특별한 타입의 metrics aggregations
  - single/muli-value numeric metrics aggregation
    - single-value numeric metrics aggregation: 단일 숫자 값을 반환하는 aggregations을 말한다.
    - multi-value numeric metrics aggregation: 다중 metrics을 생성하는 aggregation을 말한다.
    - 둘의 차이는 bucket aggregations의 서브 aggregation으로 사용될 때 드러난다.



- Avg 

  - 집계된 문서에서 추출한 숫자의 병균을 계산하는 single-value numeric metrics aggregation
  - 사용하기
    - 검색 결과는 반환하지 않도록 `size=0`을 입력한다.

  ```bash
  $ curl -XGET "localhost:9200/nations/_search?size=0" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "avg_population": {
        "avg": {
          "field": "population"
        }
      }
    }
  }
  '
  ```

  - 응답

  ```json
  {
    "took" : 2,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 10,
        "relation" : "eq"
      },
      "max_score" : null,
      "hits" : [ ]
    },
    "aggregations" : {
      "avg_grade" : {
        "value" : 20127.5	// 평균값은 20127.5
      }
    }
  }
  ```

  - missing 파라미터
    - 집계 하려는 필드에 값이 존재하지 않을 경우 기본적으로는 해당 값을 제외하고 집계를 진행한다.
    - 그러나 만일 특정 값을 넣어서 집계하고 싶을 경우 missing 파라미터를 사용하면 된다.

  ```bash
  $ curl -XGET "localhost:9200/nations/_search?size=0" -H 'Content-type:application/json' -d '
  {
    "aggs": {
      "avg_population": {
        "avg": {
          "field": "population",
          "missing": 1000
        }
      }
    }
  }'
  ```

  - histogram
    - histogram 필드의 평균은 `counts` 배열에서 동일한 위치에 있는 수를 고려한  `values` 배열의 모든 요소들의 가중 평균이다.
    - 아래 예시의 경우, 각 히스토그램 필드에 대해 평균을 계산할 때, <1>에 해당하는 `values` 배열의 각 요소들과 <2>에 해당하는 `counts` 배열의 각 요소들을 위치에 따라 곱한 값을 더한 후, 이 값들로 평균을 구한다. 
    - 0.2~0.3에 해당하는 값이 가장 많으므로 0.2X가 결과값으로 나올 것이다.
  
  ```bash
  $ curl -XPUT "localhost:9200/my_index/_doc/1
  {
    "network.name" : "net-1",
    "latency_histo" : {
        "values" : [0.1, 0.2, 0.3, 0.4, 0.5], # <1>
        "counts" : [3, 7, 23, 12, 6] 			# <2>
     }
  }
  
  $ curl -XPUT "localhost:9200/my_index/_doc/2
  {
    "network.name" : "net-2",
    "latency_histo" : {
        "values" :  [0.1, 0.2, 0.3, 0.4, 0.5], # <1>
        "counts" : [8, 17, 8, 7, 6] 			 # <2>
     }
  }
  
  $ curl -XPOST "localhost:9200/my_index/_search?size=0
  {
    "aggs": {
      "avg_latency":
        { "avg": { "field": "latency_histo" }
      }
    }
  }
  ```



- Max

























