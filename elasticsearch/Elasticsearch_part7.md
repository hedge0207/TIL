# Runtime field

- Runtime field
  - query time에 평가되는 필드
    - search API로 런타임 필드에 접근이 가능하다.
    - 인덱스 매핑이나 검색 요청에 런타임 필드를 정의할 수 있다.
  - 7.11부터 도입 되었다.
  - 런타임 필드를 활용하면 아래와 같은 것들이 가능해진다.
    - 재색인(reindexing)없이 문서에 필드를 추가할 수 있다.
    - 데이터의 구조를 몰라도 데이터 처리가 가능하다.
    - 색인 된 필드에서 반환 받은 값을 query time에 덮어쓸 수 있다.
    - schema 수정 없이 필드를 정의할 수 있다.
  - 사용시 이점
    - 런타임 필드는 인덱싱하지 않기에, index 크기를 증가시키지 안흔다.
    - Elasticsearch는 런타임 필드와 색인된 일반적인 필드를 구분하지 않기 때문에 런타임 필드를 색인시킨다고 하더라도 기존에 런타임 필드를 참조했던 쿼리를 수정 할 필요가 없다.
    - data를 모두 색인시킨 이후에도 런타임 필드를 추가할 수 있기 때문에, 데이터의 구조를 몰라도 일단 데이터를 색인시키고, 이후에 놓친 부분이 있다면 런타임 필드를 활용하면 된다. 



# Scripting

- Scripting

  - custom 표현식을 사용할 수 있다.

  - 기본 스크립트 언어는 Painless이다.

    - `lang` 플러그인을 설치하면 다른 언어로 스크립트를 작성할 수 있다.

  - ES는 새로운 스크립트를 발견하면 해당 스크립트를 컴파일한다.

    - 대부분의 context에서 5분당 75개의 스크립트를 컴파일한다.
    - ingest context의 경우 script compilation rate의 기본값은 제한 없음으로 되어 있다. 
    - script compilation rate은 동적으로 변경 가능하다.

    ```bash
    # 예시. field context에서 10분당 100개의 스크립트를 컴파일 하도록 설정
    script.context.field.max_compilations_rate=100/10m
    ```

    - 만일 단기간에 너무 많은 스크립트를 컴파일 할 경우 `circuit_breaking_exception` error 가 발생한다.
    
  - 스크립트의 크시는 65,535 bytes로 제한되어 있다.
  
    - `script.max_size_in_bytes`를 통해 제한을 늘릴 수 있다.
    - 만일 스크립트의 크기가 너무 크다면 [native script engine](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-engine.html)을 사용하는 것을 고려해볼만 하다.



- Painless 
  - Elasticsearch를 위해 설계된 스크립팅 언어
  - 장점
    - 허용 목록(allowlist)을 통해 클러스터의 보안이 보장된다.
    - JVM이 제공하는 최적화를 가능한한 모두 활용하기 위해 JVM 바이트 코드로 직접 컴파일하여 성능이 뛰어나다.
    - 다른 언어들과 유사한 문법을 제공하여 배우기 쉽다.



- scripts 작성하기

  - 기본 패턴
    - Elasticsearch API 중 어디에서 사용되더라도 아래와 같은 패턴을 따른다.
    - `script`는 JSON 오브젝트 형식으로 작성한다.

  ```json
  "script":{
      "lang":"<language>",	// 사용할 언어를 입력한다(기본값은 painless)
      "source" | <"id":"...">, // 인라인 script로 작성한 소스 혹은 저장된 스크립트의 id를 입력한다.
  	"params": <{...}> // script에 변수로 넘겨줄 parameters를 입력한다. 
  }
  ```

  - 사용 예시(Painless 기준)
    - `lang`을 따로 지정해 주지 않으면 기본값으로 Painless가 들어가게 된다.
    - Painless script에는 하나 이상의 선언문이 있어야 한다.

  ```bash
  # 데이터 삽입
  $ curl -XPUT "localhost:9200/script_test/_doc/1" -H "Content-type:application/json" -d '
  {
  	"my_field":5
  }' 
  
  # 스크립트 작성
  $ curl -XGET "localhost:9200/script_test/_search" -H "Content-type:application/json" -d '
  {
    "script_fields": {
      "my_doubled_field": {
        "script": {
          "source": "doc['my_field'].value * params['multiplier']", 
          "params": {
            "multiplier": 2
          }
        }
      }
    }
  }'
  
  # 응답
  {
  	# (...)
  	"hits" : [
        {
          "_index" : "scripts_practice",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 1.0,
          "fields" : {
            "my_doubled_field" : [
              10
            ]
          }
        }
      ]
  }
  ```

  - value를 하드코딩하는 것 보다 `params`에 작성하여 인자로 넘기는 것이 낫다.
    - ES가 새로운 스크립트를 발견하면, 스크립트를 컴파일하고 컴파일 된 버전을 캐시에 저장한다.
    - 컴파일은 무거운 과정일 수 있다.
    - 예를 들어 위 스크립트를 아래와 같이 바꿀 경우 숫자 2를 3으로 바꾼다면 ES는 다시 컴파일을 거친다.
    - 그러나 `params`의 값을 변경할 경우 script 자체를 수정한 것은 아니기 때문에 다시 컴파일하지 않는다.
    - 따라서 스크립트의 유연성이나 컴파일 시간을 고려할 때 `params`에 작성하는 것이 좋다.

  ```json
  "script": {
      "source": "doc['my_field'].value * 2", 
  }
  ```



- script를 더 짧게 작성하기

  - Painless에서 기본적으로 제공하는 문법.
  - 아래와 같은 script가 있을 때

  ```bash
  $ curl -XGET "localhost:9200/script_test/_search" -H "Content-type:application/json" -d '
  {
    "script_fields": {
      "my_doubled_field": {
        "script": {
          "lang":   "painless",
          "source": "return doc['my_field'].value * params.get('multiplier');",
          "params": {
            "multiplier": 2
          }
        }
      }
    }
  }
  ```

  - 아래와 같이 축약이 가능하다.
    - default 언어이기 때문에 `lang`을 선언하지 않아도 된다.
    - 자동으로 `return` 키워드를 붙여주기에 빼도 된다.
    - Map 타입에 한해서 `.get()` 메서드를 생략 가능하다.
    - `source`의 마지막에 세미콜론을 붙이지 않아도 된다.

  ```bash
  $ curl -XGET "localhost:9200/script_test/_search" -H "Content-type:application/json" -d '
  {
    "script_fields": {
      "my_doubled_field": {
        "script": {
          "source": "doc['my_field'].value * params['multiplier']",
          "params": {
            "multiplier": 2
          }
        }
      }
    }
  }'
  ```



- scripts를 저장하고 불러오기

  - stored script APIs를 활용하여 cluster state에 script를 저장하고 불러올 수 있다.
  - script를 저장하면 스크립트를 컴파일 하는 시간이 감소되므로 검색이 보다 빨라진다.
  - script 저장하기

  ```bash
  $ curl -XPOST "localhost:9200/_scripts/<스크립트명>" -H "Content-type:application/json" -d '
  {
  	"script": {
  		<저장할 스크립트>
  		}
  	}
  }'
  ```

  - 스크립트 불러오기

  ```bash
  $ curl -XGET "localhost:9200/_scripts/<불러올 스크립트명>"
  ```

  - 저장된 script를 query에 사용하기

  ```bash
  $ curl -XGET "localhost:9200/script_test/_doc/1" -H "Content-type:application/json" -d '
  {
    "query": {
      # <쿼리식>,
        "script": {
          "id": "<저장한 스크립트의 id>", 
          "params": {
            [params에 맞는 값]
          }
        }
      }
    }
  }
  ```

  - 저장된 스크립트 삭제하기

  ```bash
  $ curl -XDELETE "localhost:9200/_scripts/<스크립트명>"
  ```



- 스크립트로 문서 update

  - `_update` API를 통해 script로 문서를 업데이트 할 수 있다.
    - `_update`  API는 문서를 부분적으로 수정할 수도 있다.
  - 필드의 값을 수정

  ```bash
  # 문서를 색인하고
  $ curl -XPUT "localhost:9200/my_index/_doc/1" -H "Content-type:application/json" -d '
  {
    "counter" : 1,
    "tags" : ["red"]
  }'
  
  # _update API를 통해 counter 필드의 값을 증가
  $ curl -XPUT "localhost:9200/my_index/_update/1" -H "Content-type:application/json" -d '
  {
    "script" : {
      "source": "ctx._source.counter += params.count",
      "lang": "painless",
      "params" : {
        "count" : 4
      }
    }
  }'
  
  # _update API를 통해 tag 필드에 값을 추가
  $ curl -XPUT "localhost:9200/my_index/_update/1" -H "Content-type:application/json" -d '
  {
    "script": {
      "source": "ctx._source.tags.add(params['tag'])",
      "lang": "painless",
      "params": {
        "tag": "blue"
      }
    }
  }'
  
  # 특정 tag 값이 존재할 때 해당 태그 값을 삭제
  $ curl -XPUT "localhost:9200/my_index/_update/1" -H "Content-type:application/json" -d '
  {
    "script": {
      "source": "if (ctx._source.tags.contains(params['tag'])) { ctx._source.tags.remove(ctx._source.tags.indexOf(params['tag'])) }",
      "lang": "painless",
      "params": {
        "tag": "blue"
      }
    }
  }'
  ```

  - 필드 자체를 수정

  ```bash
  # 새로운 필드 추가
  $ curl -XPUT "localhost:9200/my_index/_update/1" -H "Content-type:application/json" -d '
  {
    "script" : "ctx._source.new_field = 'value_of_new_field'"
  }'
  
  # 기존 필드 삭제
  $ curl -XPUT "localhost:9200/my_index/_update/1" -H "Content-type:application/json" -d '
  {
    "script" : "ctx._source.remove('new_field')"
  }'
  ```

  - 문서 자체를 수정
    - `ctx.op`를 통해 문서에 어떤 동작을 수행할 것인지를 입력한다.

  ```bash
  # 조건에 부합하면 특정 행동(operation)을 하고, 조건에 부합하지 않으면 아무 것도 하지 않는 스크립트(noop 사용)
  # 아래 스크립트의 경우 
  $ curl -XPUT "localhost:9200/my_index/_update/1" -H "Content-type:application/json" -d '
  {
    "script": {
      "source": "if (ctx._source.tags.contains(params['tag'])) { ctx.op = 'delete' } else { ctx.op = 'none' }",
      "lang": "painless",
      "params": {
        "tag": "green"
      }
    }
  }'
  ```



- 스크립트 캐싱
  - ES는 스크립트를 캐싱한다.
    - ES는 scripts를 가능한 빠르게 사용할 수 있도록 여러 방법으로 최적화를 수행하는데 캐싱도 그 중 하나다.
    - 컴파일 된 스크립트는 캐시에 저장되고 캐시에 저장된 스크립트를 참조하는 요청은 컴파일 되지 않는다.
  - cache size
    - cache size는 사용자들이 동시에 접근하는 모든 스크립트를 저장할 수 있을 만큼 커야 한다.
    - 만일 node stats에서 확인했을 때 많은 양의 cache가 삭제되거나 컴파일 수가 증가한다면, cache가 너무 작다는 뜻이다.
    - `script.cache.max_size`를 통해 캐시의 최대치를 설정할 수 있다.
    - 모든 스크립트는 기본적으로 캐싱이 되므로, 스크립트에 변경 사항이 있을 때만 recompile한다.
    - 캐시의 삭제는 일정 시간이 지나면 만료되는 방식이 **아니다.**
    - `script.cache.expire` 를 통해 캐시 만료 방식을 설정할 수 있다.



- 검색 속도 향상

  - 스크립트는 인덱스의 구조나 그와 관련된 최적화를 사용할 수 없다.
    - 따라서 떄떄로 검색 속도가 느려지게 된다.
  - 스크립트를 사용하여 인덱싱 된 데이터를 변환한다면, 수집(ingest) 중에 데이터를 변환하여 검색을 더 빠르게 할 수 있다.
    - 단, 이는 인덱싱 속도를 저하시킬 수 있다.

  - 일반적인 검색
    - 검색 시에 반환 되는 `math_score`와 `verbal_score` 값을 더한 값으로 검색 결과를 정렬하고자 한다.
    - 아래 request에는 스크립트가 포함되어 있으므로 느려지게 된다.

  ```bash
  $ curl -XGET "localhost:9200/my_index/_search" -H "Content-type:application/json" -d '
  {
    "query": {
      "term": {
        "name": "maru"	# name filed가 maru인 문서 검색
      }
    },
    "sort": [
      {
        "_script": {
          "type": "number",
          "script": {
            "source": "doc['math_score'].value + doc['verbal_score'].value"
          },
          "order": "desc"
        }
      }
    ]
  }'
  ```

  - 검색 속도 향상시키기
    - 작은 인덱스에서는 search query에 스크립트를 포함시는 것도 방법이 될 수 있다.
    - 일반적으로는 아래와 같이 ingest 시에 스크립트를 활용하는 방식을 사용한다.
    - ingest time을 증가시키긴 하지만 검색 속도는 증가헤 된다.

  ```bash
  # math_score 와 verbal_score의 합계를 저장할 새로운 필드를 추가한다.
  $ curl -XPUT "localhost:9200/my_index/_mapping" -H "Content-type:application/json" -d '
  {
    "properties":{
    	"total_score":{
    		"type":"long"
    	}
    }
  }'
  
  # ingest pipeline을 활용하여 math_score 와 verbal_score의 합계를 계산하고, 이를 total_score 필드에 인덱싱한다.
  $ curl -XPUT "localhost:9200/_ingest/pipeline/my_index_pipeline" -H "Content-type:application/json" -d '
  {
    "description": "Calculates the total test score",
    "processors": [
      {
        "script": {
          "source": "ctx.total_score = (ctx.math_score + ctx.verbal_score)"
        }
      }
    ]
  }'
  
  # 이미 있는 문서들을 업데이트 하기 위해서 reindex한다.
  $ curl -XPUT "localhost:9200/_reindex" -H "Content-type:application/json" -d '
  {
    "source": {
      "index": "my_index"
    },
    "dest": {
      "index": "my_index_2",
      "pipeline": "my_index_pipeline"
    }
  }
  
  # pipeline을 활용하여 새로운 문서를 인덱싱한다.
  $ curl -XPUT "localhost:9200/my_index/_doc/?pipeline=my_index_pipeline" -H "Content-type:application/json" -d '
  {
    "name": "maru",
    "hobby": "swimming"
  }'
  
  # 검색하기
  $ curl -XGET "localhost:9200/my_index/_search" -H "Content-type:application/json" -d '
  {
    "query": {
      "term": {
        "name": "maru"
      }
    },
    "sort": [
      {
        "total_score": {
          "order": "desc"
        }
      }
    ]
  }'
  ```



- Dissecting data

  - Dissect는 정의된 패턴과 일치하는 single text filed를 찾는다.
    - 정규표현식을 사용하지 않을 경우, 뒤에서 설명할 grok 대신 disset 패턴을 사용하면 된다.
    - disset이 grok 보다 문법도 훨씬 간단하고, 일반적으로 더 빠르다.
  - Dissect patterns
    - disset 패턴은 변수 (variables)와 구분자(separators)로 구성된다.
    - `%{}`안에 들어간 모든 값은 변수로 간주된다.
    - 구분자는 변수 사이에 있는 어떤 값이든 될 수 있다.

  ```bash
  # 아래와 같은 문자열은
  247.37.0.0 - - [30/Apr/2020:14:31:22 -0500]  
  
  # 아래와 같은 패턴으로 표시될 수 있다.
  # %{}안에 변수를 넣고, 그 사이에 스페이스를 구분자로 넣은 형태이다.
  %{clientip} %{ident} %{auth} [%{@timestamp}]
  
  # 아래와 같은 문자열은
  \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0
  
  # 아래와 같은 패턴으로 표시할 수 있다.
  "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}
  
  
  # 두 패턴을 결합하면 아래와 같다.
  %{clientip} %{ident} %{auth} [%{@timestamp}] \"%{verb} %{request} HTTP/%{httpversion}\" %{status} %{size}
  ```

  - Painless 스크립트에서 dissect 패턴 사용하기
    - Painless execute API의 field contexts를 사용하거나 스크립트를 포함하는 runtime 필드를 생성함으로써 스크립트를 테스트 해 볼 수 있다.

  ```bash
  # 인덱스 생성
  $ curl -XPUT "localhost:9200/my_index" -H "Content-type:application/json" -d '
  {
    "mappings": {
      "properties": {
        "message": {
          "type": "wildcard"
        }
      }
    }
  }'
  
  # Painless execute API를 활용하여 스크립트 테스트하기
  $ curl -XPOST "localhost:9200/_scripts/painless/_execute" -H "Content-type:application/json" -d '
  {
    "script": {
      # dissect 패턴 정의
      "source": """
        String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
          if (response != null) emit(Integer.parseInt(response)); 
      """
    },
    "context": "long_field", 
    "context_setup": {
      "index": "my-index",
      "document": {          
        "message": """247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] "GET /images/hm_nbg.jpg HTTP/1.0" 304 0"""
      }
    }
  }'
  ```

  - dissect 패턴과 스크립트를 런타임 필드에서 사용하기
    - disscet 패턴을 런타임 필드에 추가할 수 있다.

  ```bash
  # 인덱스 생성하기
  $ curl -XPUT "localhost:9200/my_index" -H "Content-type:application/json" -d '
  {
    "mappings": {
      "properties": {
        "@timestamp": {
          "format": "strict_date_optional_time||epoch_second",
          "type": "date"
        },
        "message": {
          "type": "wildcard"
        }
      }
    }
  }'
  
  # 런타임 필드 생성
  $ curl -XPUT "localhost:9200/my_index/_mappings" -H "Content-type:application/json" -d '
  {
    "runtime": {
    	# http.response라는 런타임 필드 생성
      "http.response": {
        "type": "long",
        "script": """
          String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
          if (response != null) emit(Integer.parseInt(response));
        """
      }
    }
  }'
  
  # 데이터 추가
  $ curl -XPOST "localhost:9200/my_index/_bulk?refresh=true" -H "Content-type:application/json" -d '
  {"index":{}}
  {"timestamp":"2020-04-30T14:30:17-05:00","message":"40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:30:53-05:00","message":"232.0.0.0 - - [30/Apr/2020:14:30:53 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:12-05:00","message":"26.1.0.0 - - [30/Apr/2020:14:31:12 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:19-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:19 -0500] \"GET /french/splash_inet.html HTTP/1.0\" 200 3781"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:22-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:27-05:00","message":"252.0.0.0 - - [30/Apr/2020:14:31:27 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:28-05:00","message":"not a valid apache log"}'
  
  # 확인하기
  $ curl -XGET "localhost:9200/my-index/_search" -H "Content-type:application/json" -d '
  {
    "query": {
      "match": {
        "http.response": "304"
      }
    },
    "fields" : ["http.response"]
  }'
  ```

  - search request에 런타임 필드 정의하기

  ```bash
  $ curl -XGET "localhost:9200/my-index/_search" -H "Content-type:application/json" -d '
  {
    "runtime_mappings": {
      "http.response": {
        "type": "long",
        "script": """
          String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
          if (response != null) emit(Integer.parseInt(response));
        """
      }
    },
    "query": {
      "match": {
        "http.response": "304"
      }
    },
    "fields" : ["http.response"]
  }'
  ```



- Grokking grok

  - Grok은 재사용 가능한 aliased 표현을 지원하는 정규표현식이다.
    - 시스템 로그를 확인할 때 매우 유용하다.
    - Oniguruma 정규표현식 라이브러리 기반이다.
    - 이미 존재하는 패턴에 이름을 붙이고, 패턴들을 결합하여 보다 복잡한 패턴을 만드는데 사용 가능하다.
  - Grok 패턴
    - ES는 grok을 보다 쉽게 사용할 수 있도록, 이미 정의된 다양한 grok 패턴을 제공한다.
    - grok 패턴의 문법은 아래의 형식 중 하나의 형태를 띈다.
    - `%{SYNTAX}`: 텍스트와 매치될 패턴의 이름을 넣는다. 만일 `%{NUMBER}`와 같이 적으면 텍스트 내의 숫자 형식의 텍스트와 매칭이 되고, `%{IP}`와 같이 적으면 텍스트 내의 IP 형식의 텍스트와 매칭이 된다.
    - `%{SYNTAX:ID}`: 매칭 된 텍스트에 지정할 식별자이다. 예를 들어 `%{IP:client}`와 같이 적으면  IP 형식의 텍스트와 매칭 된 해당 텍스트를 clinet라고 부르겠다는 뜻이다.
    - `%{SYNTAX:ID:TYPE}`: 매칭된 텍스트에 int, long, float, boolean과 같은 타입을 지정해준다.

  ```bash
  # 예를 들어 아래와 같은 텍스트가 있을 때
  3.44 55.3.244.1
  
  # 아래와 같이 grok 표현식으로 표현이 가능하다.
  %{NUMBER:duration} %{IP:client}
  # durationd에는 3.44가, IP에는 55.3.244.1가 담기게 된다.
  ```

  - Painless 스크립트에서 grok 패턴 사용하기
    - 기존에 정의한 grok 패턴을 Painless 스크립트와 결합하여 사용하는 것이 가능하다.
    - Painless execute API의 field contexts를 사용하거나 스크립트를 포함하는 runtime 필드를 생성함으로써 스크립트를 테스트 해 볼 수 있다.
  
  ```bash
  # 아래와 같은 apache log에서 ip를 추출한다고 가정
  "timestamp":"2020-04-30T14:30:17-05:00","message":"40.135.0.0 - -
  [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
  
  # 테스트 인덱스 생성
  $ curl -XPUT "localhost:9200/my-index" -H "Content-type:application/json" -d '
  {
    "mappings": {
      "properties": {
        "@timestamp": {
          "format": "strict_date_optional_time||epoch_second",
          "type": "date"
        },
        "message": {
          "type": "wildcard"
        }
      }
    }
  }'
  
  # 테스트 데이터 인덱싱
  $ curl -XPOST "localhost:9200/my-index/_bulk" -H "Content-type:application/json" -d '
  {"index":{}}
  {"timestamp":"2020-04-30T14:30:17-05:00","message":"40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:30:53-05:00","message":"232.0.0.0 - - [30/Apr/2020:14:30:53 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:12-05:00","message":"26.1.0.0 - - [30/Apr/2020:14:31:12 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:19-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:19 -0500] \"GET /french/splash_inet.html HTTP/1.0\" 200 3781"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:22-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:27-05:00","message":"252.0.0.0 - - [30/Apr/2020:14:31:27 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
  {"index":{}}
  {"timestamp":"2020-04-30T14:31:28-05:00","message":"not a valid apache log"}'
  
  # %{COMMONAPACHELOG} 문법과 Painless 스크립트를 결합하여 런타임 필드 생성.
  $ curl -XPUT "localhost:9200/my-index/_mappings" -H "Content-type:application/json" -d '
  {
    "runtime": {
      "http.clientip": {
        "type": "ip",
        "script": """
        	# 만일 일치하는 패턴이 있을 경우 IP주소를 emit하고. 없을 경우 field value를 반환한다.
          String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
          if (clientip != null) emit(clientip);
        """
      }
    }
  }
  
  # 검색
  $ curl -XGET "localhost:9200/my-index/_mappings" -H "Content-type:application/json" -d '
  {
    "query": {
      "match": {
        "http.clientip": "40.135.0.0"
      }
    },
    "fields" : ["http.clientip"]
  }'
  ```
  
  - search request에 런타임 필드 정의하기
    - 위 방식과 결과는 같다.
  
  ```bash
  $ curl -XGET "localhost:9200/my-index/_search" -H "Content-type:application/json" -d '
  {
    "runtime_mappings": {
      "http.clientip": {
        "type": "ip",
        "script": """
          String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
          if (clientip != null) emit(clientip);
        """
      }
    },
    "query": {
      "match": {
        "http.clientip": "40.135.0.0"
      }
    },
    "fields" : ["http.clientip"]
  }'
  ```





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



## Bucket aggregations

- Bucket aggregations
  - 주어진 조건으로 분류된 버킷을 만들고, 각 버킷에 속하는 문서들을 모아 그룹으로 구분하는 것.
    - 각 버킷에 들어 있는 문서 수를 반환한다.
  - sub-aggregation을 사용 가능하다.



###  terms

- keyword 필드의 문자열 별로 버킷을 나누어 집계한다.
  - text 필드 값도 사용은 가능하지만 성능이 매우 떨어진다.
  - 아래의 경우 continent 필드의 값(`key`)이 4개 밖에 없지만, 값이 많을 경우에는 많이 집계된 순(기본값은 상위 10개)으로 반환하고, 반환하지 않은 값들은 `sum_other_doc_count`에 count된다.
  
  ```bash
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "size":0,	# 검색 결과는 보지 않기 위해서 0을 준다.
    "aggs":{
      "continents":{    # aggs 이름
        "terms":{
          "field":"continent.keyword" # 적용 할 필드
        }
      }
    }
  }'
  
  # 응답
  "aggregations" : {
    "continents" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "아시아",
          "doc_count" : 4
        },
        {
          "key" : "유럽",
          "doc_count" : 3
        },
        {
          "key" : "북아메리카",
          "doc_count" : 2
        },
        {
          "key" : "아프리카",
          "doc_count" : 1
        }
      ]
     }
  }
  ```



- `size`
  
  - terms aggs는 기본값으로 상위 10개의 버킷만 반환하지만, `size` 파라미터를 통해 이를 조정할 수 있다.
  - term의 동작 과정
    - 노드에 검색 요청이 들어오면, 노드는 각 샤드에 요청을 보내 샤드별로 `shard_size`에 해당하는 만큼의 버킷을 받아온다.
    - 모든 샤드가 노드로 버킷을 보내면, 노드는 버킷을 클라이언트에 보내기 전에 해당 결과값들을 취합하여  `size`에 설정된 크기의 최종 버킷 리스트를 만든다.
    - 따라서 `size`파라미터 보다 `shard_size`의 수가 더 클 경우, 클라이언트가 반환 받은 버킷 리스트는 실제 결과와는 약간 다르다.
    - 심지어 실제로 개수가 더 많더라도 반환되지 않을 수 있다.
    - 예를 들어 아래 표에서 key1의 총 개수는 40, key2의 총 개수는 34이다.
    - `shard_size`가 1일 경우 A,B,D 샤드는 key1, C샤드는 key2를 노드에 반환한다.
    - 노드가 반환된 값을 취합하면 key1은 20, key2는 25이므로 노드는 클라이언트에 key2를 반환하게 된다.
    - 실제 개수는 key1이 더 많음에도 key2가 반환되는 것이다.
  
  |      | shard A | shard B | shard C | shard D |
  | ---- | ------- | ------- | ------- | ------- |
  | key1 | 10      | 5       | 20      | 5       |
  | key2 | 5       | 2       | 25      | 2       |
  | key3 | 1       | 3       | 1       | 1       |



- `sum_other_doc_count`와 `doc_count_error_upper_bound`

  - `sum_other_doc_count`
    - 결과에 포함되지 않은 버킷들에 속하는 모든 문서의 수.
  - `doc_count_error_upper_bound`
    - 각 샤드가 반환한 term들 중 최종 결과에는 포함되지 않은 모든 문서의 수
  - 문제가 없는 경우
    - 만일 `size`가 5라면 `sum_other_doc_count`와 `doc_count_error_upper_bound`는 0이 나올 것이다.

  |              | shard A | shard B | shard C | shard D | shard E | total |
  | ------------ | ------- | ------- | ------- | ------- | ------- | ----- |
  | 모짜르트     | 55      | 50      | 40      | 60      | 45      | 250   |
  | 베토벤       | 45      | 40      | 35      | 40      | 40      | 200   |
  | 차이코프스키 | 20      | 15      | 25      | 30      | 10      | 100   |
  | 바흐         | 10      | 5       | 15      | 5       | 5       | 40    |
  | 쇼팽         | 5       | 3       | 5       | 2       | 3       | 18    |

  - 문제가 있는 경우
    - 전체 term의 개수는 6개이고, `shard_size`가 6일 경우, 집계를 합산하는 노드에는 아래와 같은 결과가 모이게 된다.
    - shard A의 경우 Lenovo의 doc_count가 LG의 doc_count인 5 이하일 경우 아예 집계가 되지 않는다.
    - shard B 역시 마찬가지로 LG의 doc_count가 ASUS의 doc_count인 5 이하일 경우 아예 집계가 되지 않으며, 나머지 샤드들도 마찬가지다.

  |        | shard A | shard B | shard C | shard D | shard E | total |
  | ------ | ------- | ------- | ------- | ------- | ------- | ----- |
  | Mac    | 55      | 50      | 40      | 60      | 45      | 250   |
  | Dell   | 45      | 40      | 35      | 40      | 40      | 200   |
  | HP     | 20      | 15      | 25      | 30      | 10      | 100   |
  | ASUS   | 10      | 5       | 15      | -       | 5       | 35    |
  | Lenovo | -       | 8       | 10      | 2       | -       | 20    |
  | LG     | 5       | -       | -       | 7       | 3       | 15    |

  - 위 예시에서 집계에 포함되지 않은 문서들의 개수의 최댓값 추정치는 아래 표와 아래와 같다.

  |                         | shard A | shard B | shard C | shard D | shard E | total |
  | ----------------------- | ------- | ------- | ------- | ------- | ------- | ----- |
  | HP worst case error     | -       | -       | -       | 2       | -       | 2     |
  | Lenovo worst case error | 5       | -       | -       | -       | 3       | 8     |
  | LG worst case error     | -       | 5       | 10      | -       | -       | 15    |

  - 상위 5개의 문서만 반환되므로 total이 가장 적은 LG는 포함되지 않는다.
    - `sum_other_doc_count`는 최종 결과에 포함되지 않은 버킷에 속하는 문서의 수이므로 최종 결과에 포함되지 않은 LG의 total인 15가 된다.
    - 만일 samsung이라는 term이 존재하고, 각 샤드별로 (1, 1, 1, 1, 1) 씩 존재했다면, total은 5로 역시 최종 결과에 포함되지 못한다. 
    - 따라서 이 경우 `sum_other_doc_count`는 15(LG)+5(samsung)으로 20이 된다.
  - `doc_count_error_upper_bound`는 모든 샤드가 반환한 각 텀들의 문서 중 최종 집계 결과에 합산되지 못한 문서들의 개수의 최댓값을 합산한 값이다.
    - LG는 버킷 전체가 집계 결과에 합산되지 못했고, HP, Lenovo는 각기 2, 8이 합산되지 못했다.
    - 따라서 `doc_count_error_upper_bound`는 15+2+8=25이다.
    - 만일 samsung이라는 term이 존재하고, 각 샤드별로 (1, 1, 1, 1, 1) 씩 존재했다면, 각 샤드가 반환한 6개의 텀에도 포함되지못한다. 
    - 따라서 `doc_count_error_upper_bound`에는 변화가 없다.



- `shard_size`
  - 노드가 shard에 버킷을 반환하라는 요청을 보낼 때 각 샤드가 반환할 버킷의 수이다.
    - `size`보다 작을 수 없으며, `size`보다 작게 설정할 경우 ES가 자동으로 `size`와 동일한 값을 가지게 조정한다.
    - 기본값은 `size*1.5+10` 이다.
  - `size`가 커질수록 정확도는 올라가지만, 결과를 계산하는 비용과 보다 많은 데이터를 클라이언트로 보내는 비용이 커지게 된다.
    - 따라서 `size`를 늘리는 대신에 `shard_size`를 증가시키면 설정하면 보다 많은 데이터를 클라이언트로 보내는 비용을 최소화 할 수 있다.



- `show_term_doc_count_error`

  - `show_term_doc_count_error`를 true로 설정하면 각  term별로 집계 에러의 개수를 worst case 기준으로 보여준다.
    - `shard_size`를 설정하는데 참고할 수 있다.
  - term을 반환하지 않은 모든 샤드들에서 가장 낮은 counts를 합산하여 계산한다.
    - counts가 내림차순으로 정렬되어 있어야 위와 같이 계산이 가능하다.
    - counts가 오름차순으로 정렬되어 있거나 sub-aggregation을 기준으로 정렬되었다면, 계산이 불가능하고, 이럴 경우 -1을 반환한다.

  ```bash
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "size":0,	# 검색 결과는 보지 않기 위해서 0을 준다.
    "aggs":{
      "continents":{
        "terms":{
          "field":"continent.keyword",
          "show_term_doc_count_error": true
        }
      }
    }
  }'
  ```



- `order`

  - 버킷의 순서를 설정할 수 있는 파라미터.
  - 기본값으로는 `doc_count`를 기준으로 내림차순으로 정렬된다.
  - 정렬 방식
    - pipeline aggs는 정렬에 사용할 수 없다.

  ```bash
  # counts를 기준으로 오름차순으로 정렬
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "size":0,
    "aggs":{
      "continents":{
        "terms":{
          "field":"continent.keyword",
          "order": { "_count": "asc" }
        }
      }
    }
  }'
  
  # term을 알파벳 기준으로 오름차순으로 정렬(6.0 이전까지는 "_term"을 사용)
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "size":0,
    "aggs":{
      "continents":{
        "terms":{
          "field":"continent.keyword",
          "order": { "_key": "asc" }  
        }
      }
    }
  }'
  
  # single value metrics sub-aggregation을 기준으로 정렬(아래의 경우 max 집계 값을 기준으로 대륙 버켓을 정렬)
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "continents": {
        "terms": {
          "field": "continent.keyword",
          "order": { "max_population": "desc" }
        },
        "aggs": {
          "max_population": { "max": { "field": "population" } }
        }
      }
    }
  }'
  
  # multi value metrics sub-aggregation을 기준으로 정렬(아래의 경우 stats 집계갑 중 max 값을 기준으로 대륙 버켓을 정렬)
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "continents": {
        "terms": {
          "field": "continent.keyword",
          "order": { "population_stats.max": "desc" }
        },
        "aggs": {
          "population_stats": { "stats": { "field": "population" } }
        }
      }
    }
  }'
  ```

  - 보다 계층적인(sub aggs의 깊이가 깊은) aggs에서도 사용이 가능하다.
    - aggs 경로가 계층의 마지막 aggs가 single-bucket이거나 metrics일 경우에 한해서 사용이 가능하다.
    - single-bucket type일 경우 버킷에 속한 문서의 수에 의해 순서가 결정된다.
    - single-value metrics aggregation의 경우 aggs의 결괏값을 기준으로 정렬이 적용된다.
    - multi-value metrics aggregation의 경우 aggs 경로는 정렬 기준으로 사용할 metric 이름을 나타내야 한다.

  | 설명             | 기호                                                         |
  | ---------------- | ------------------------------------------------------------ |
  | AGG_SEPARATOR    | >                                                            |
  | METRIC_SEPARATOR | .                                                            |
  | AGG_NAME         | <AGG_NAME>                                                   |
  | METRIC           | <metric 이름(multi-value metrics aggs의 경우)>               |
  | PATH             | <AGG_NAME> [<AGG_SEPARATOR>, <AGG_NAME>] * [ <METRIC_SEPARATOR>, \<METRIC> ] |

  ```bash
  # nation버킷을 continent가 아시아인 국가들의 population을 기준으로 정렬한다.
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "countries": {
        "terms": {
          "field": "nation.keyword",
          "order": { "asia>population_stats.avg": "desc" }
        },
        "aggs": {
          "asia": {
            "filter": { "term": { "continent": "아시아" } },
            "aggs": {
              "population_stats": { "stats": { "field": "population" } }
            }
          }
        }
      }
    }
  }
  '
  ```



- 복수의 기준으로 정렬하기

  - 정렬 기준을 배열에 담으면 된다.
  - 예시
    - nation버킷을 continent가 아시아인 국가들의 population을 기준으로 정렬한 후, doc_count를 기준으로 내림차순으로 정렬한다.
  
  ```bash
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "countries": {
        "terms": {
          "field": "nation.keyword",
          "order": [{ "asia>population_stats.avg": "desc" },{"_count":"desc"}]
        },
        "aggs": {
          "asia": {
            "filter": { "term": { "continent": "아시아" } },
            "aggs": {
              "population_stats": { "stats": { "field": "population" } }
            }
          }
        }
      }
    }
  }'
  ```



- doc_count의 최솟값을 설정하기

  - `min_doc_count` 옵션을 사용하면 count가 `min_doc_count`에서 설정해준 값 이상인 term만 반환된다.
    - 기본값은 1이다.
    - 아래 예시의 경우 continent의 term이 3 이상인 값만 반환되게 된다.

  ```bash
  $curl -XGET "localhost:9200/nations/_search" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "min_doc_count_test": {
        "terms": {
          "field": "continent.keyword",
          "min_doc_count": 3
        }
      }
    }
  }'
  
  # 응답
  "aggregations" : {
    "min_doc_count_test" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "아시아",
          "doc_count" : 4
        },
        {
          "key" : "유럽",
          "doc_count" : 3
        }
      ]
    }
  }
  ```

  - doc_count를 내림차순으로 정렬하지 않고, `min_doc_count`에 높은 값을 주면, `size`보다 작은 수의 버킷이 반환될 수 있다.
    - 샤드에서 충분한 데이터를 얻지 못했기 때문이다.
    - 이 경우 `shard_size`를 높게 주면 된다.

  - `shard_min_doc_count`
    - `shard_size`를 높이는 것은 보다 많은 데이터를 클라이언트로 보내는 비용은 줄일 수 있지만, 메모리 소모도 증가된다는 문제가 있다.
    - `shard_min_doc_count`은 샤드별로 `min_doc_count`를 설정함으로써 이러한 비용을 줄여준다.
    - 각 샤드는 term의 빈도가 `shard_min_doc_count` 보다 높을 때만 해당 term을 집계시에 고려한다.
    - 기본값은 0이다.
    - `shard_min_doc_count`을 지나치게 높게 주면 term이 샤드 레벨에서 걸러질 수 있으므로, `min_doc_count/shard 개수`보다 한참 낮은 값으로 설정해야 한다. 



- Script

  - 만일 문서의 데이터 중 집계하려는 필드가 존재하지 않는 경우에 runtime field를 사용할 수 있다.

  ```bash
  GET /_search
  {
    "size": 0,
    "runtime_mappings": {
      "normalized_genre": {
        "type": "keyword",
        "script": """
          String genre = doc['genre'].value;
          if (doc['product'].value.startsWith('Anthology')) {
            emit(genre + ' anthology');
          } else {
            emit(genre);
          }
        """
      }
    },
    "aggs": {
      "genres": {
        "terms": {
          "field": "normalized_genre"
        }
      }
    }
  }
  ```



- 필터링
  - 어떤 버킷이 생성될지 필터링하는 것이 가능하다.
    - `include`와 `declude` 파라미터를 사용한다.
    - 정규표현식 문자열이나 배열을 값으로 사용 가능하다.
  
  - 정규표현식으로 필터링하기
  
  ```bash
  ```
  



### rare_terms

- 지정한 숫자 미만으로 존재하는 term들을 집계한다.

  - `field`
    - 집계 할 필드를 지정한다.
    - keyword 필드여야한다.
  - `max_doc_count`
    - 최대 몇 개 까지 존재하는 값을 rare한 값으로 볼 것인지를 지정한다.
    - 기본값은 1이다.
  - 그 밖의 옵션은 아래 링크 참조

  > https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-rare-terms-aggregation.html



- 예시

  - 데이터 색인하기

  ```json
  // PUT test-index/_bulk
  {"index":{"_id":"1"}}
  {"family_name":"kim"}
  {"index":{"_id":"2"}}
  {"family_name":"kim"}
  {"index":{"_id":"3"}}
  {"family_name":"kim"}
  {"index":{"_id":"4"}}
  {"family_name":"lee"}
  {"index":{"_id":"5"}}
  {"family_name":"lee"}
  {"index":{"_id":"6"}}
  {"family_name":"park"}
  ```

  - 집계1. `max_doc_count`값을 기본값(1)로 줄 경우
    - 1개 밖에 존재하지 않는 park 만 집계된다.

  ```json
  // GET test-index/_search
  {
    "query": {
      "match_all": {}
    },
    "aggs": {
      "genres": {
        "rare_terms": {
          "field": "family_name.keyword"
        }
      }
    },
    "size":0
  }
  
  // output
  "aggregations" : {
      "genres" : {
        "buckets" : [
          {
            "key" : "park",
            "doc_count" : 1
          }
        ]
      }
    }
  ```

  - 집계2. `max_doc_count`값을 2로 줄 경우
    - 2개 이하로 존재하는 lee와 park이 집계된다.

  ```json
  // GET test-index/_search
  {
    "query": {
      "match_all": {}
    },
    "aggs": {
      "genres": {
        "rare_terms": {
          "field": "family_name.keyword",
          "max_doc_count": 2
        }
      }
    },
    "size":0
  }
  
  // output
  "aggregations" : {
      "genres" : {
        "buckets" : [
          {
            "key" : "park",
            "doc_count" : 1
          },
          {
            "key" : "lee",
            "doc_count" : 2
          }
        ]
      }
    }
  ```



### composite

- 서로 다른 데이터를 합해 하나의 버킷을 만들어주는 aggregation이다.

  - 예를 들어 아래와 같은 데이터를 만들어주는 것이다.

  ```json
  // 원본
  {
    "keyword": ["foo", "bar"],
    "number": [23, 65, 76]
  }
  
  // composite aggs
  { "keyword": "foo", "number": 23 }
  { "keyword": "foo", "number": 65 }
  { "keyword": "foo", "number": 76 }
  { "keyword": "bar", "number": 23 }
  { "keyword": "bar", "number": 65 }
  { "keyword": "bar", "number": 76 }
  ```

  - 합 할 서로 다른 source를 지정해주면 된다.

  ```json
  // 예시 데이터 생성
  PUT time-test/_bulk
  {"index":{"_id":"1"}}
  {"test_time":"2021-12-08T23:59:59", "family_name":"kim", "age":11}
  {"index":{"_id":"2"}}
  {"test_time":"2021-12-09T00:00:00", "family_name":"kim", "age":12}
  {"index":{"_id":"3"}}
  {"test_time":"2021-12-09T05:51:00", "family_name":"kim", "age":13}
  {"index":{"_id":"4"}}
  {"test_time":"2021-12-09T13:00:00", "family_name":"lee", "age":14}
  {"index":{"_id":"5"}}
  {"test_time":"2021-12-09T14:00:00", "family_name":"lee", "age":15}
  {"index":{"_id":"6"}}
  {"test_time":"2021-12-09T23:59:59", "family_name":"park", "age":13}
  {"index":{"_id":"7"}}
  {"test_time":"2021-12-10T08:59:59", "family_name":"park", "age":12}
  
  
  // 집계
  GET time-test/_search
  {
    "size": 0,
    "aggs": {
      "my_buckets": {
        "composite": {
          "sources": [
             { "date": { "date_histogram": { "field": "test_time", "calendar_interval": "1d", "order": "desc" } } },
            { "product": { "terms": { "field": "age"} } }
          ]
        }
      }
    }
  }
  ```

  - 결과
    - 날짜별 family name이 몇 명인지 출력된다.

  ```json
  "aggregations" : {
      "my_buckets" : {
        "after_key" : {
          "date" : 1638921600000,
          "product" : 11
        },
        "buckets" : [
          {
            "key" : {
              "date" : 1639094400000,
              "product" : 12
            },
            "doc_count" : 1
          },
          {
            "key" : {
              "date" : 1639008000000,
              "product" : 12
            },
            "doc_count" : 1
          },
          {
            "key" : {
              "date" : 1639008000000,
              "product" : 13
            },
            "doc_count" : 2
          },
          {
            "key" : {
              "date" : 1639008000000,
              "product" : 14
            },
            "doc_count" : 1
          },
          {
            "key" : {
              "date" : 1639008000000,
              "product" : 15
            },
            "doc_count" : 1
          },
          {
            "key" : {
              "date" : 1638921600000,
              "product" : 11
            },
            "doc_count" : 1
          }
        ]
      }
    }
  ```



- bucket pagination

  - 위 예시에서 응답을 보면 `after_key`가 포함된 것을 볼 수 있는데 이를 활용하여 bucket pagination이 가능하다.

  - 예시 data bulk

  ```json
  PUT time-test/_bulk
  {"index":{"_id":"1"}}
  {"test_time":"2021-12-08T23:59:59", "family_name":"kim", "age":11}
  {"index":{"_id":"2"}}
  {"test_time":"2021-12-09T00:00:00", "family_name":"lee", "age":12}
  {"index":{"_id":"3"}}
  {"test_time":"2021-12-09T05:51:00", "family_name":"park", "age":13}
  {"index":{"_id":"4"}}
  {"test_time":"2021-12-09T13:00:00", "family_name":"choi", "age":14}
  {"index":{"_id":"5"}}
  {"test_time":"2021-12-09T14:00:00", "family_name":"jeong", "age":15}
  {"index":{"_id":"6"}}
  {"test_time":"2021-12-09T23:59:59", "family_name":"shin", "age":13}
  {"index":{"_id":"7"}}
  {"test_time":"2021-12-10T08:59:59", "family_name":"moon", "age":12}
  {"index":{"_id":"8"}}
  {"test_time":"2021-12-10T09:00:00", "family_name":"won", "age":13}
  {"index":{"_id":"9"}}
  {"test_time":"2021-12-10T09:01:00", "family_name":"jang", "age":13}
  {"index":{"_id":"10"}}
  {"test_time":"2021-12-10T09:59:59", "family_name":"cha", "age":14}
  {"index":{"_id":"11"}}
  {"test_time":"2021-12-10T10:00:00", "family_name":"an", "age":14}
  {"index":{"_id":"12"}}
  {"test_time":"2021-12-10T10:30:55", "family_name":"yun", "age":15}
  {"index":{"_id":"13"}}
  {"test_time":"2021-12-10T11:00:00", "family_name":"kang", "age":15}
  {"index":{"_id":"14"}}
  {"test_time":"2021-12-10T11:00:12", "family_name":"jo", "age":16}
  ```

  - 집계하기
    - source에 terms aggs를 넣는다.

  ```json
  GET time-test/_search
  {
    "size": 0,
    "aggs": {
      "my_buckets": {
        "composite": {
          "sources": [
            { "product": { "terms": { "field": "family_name.keyword"} } }
          ]
        }
      }
    }
  }
  ```

  - 결과
    - 아래 결과의 `after_key`를 pagination에 사용한다.

  ```json
  "aggregations" : {
      "my_buckets" : {
        "after_key" : {
          "product" : "moon"
        },
        "buckets" : [
          {
            "key" : {
              "product" : "an"
            },
            "doc_count" : 1
          },
          // ...
          {
            "key" : {
              "product" : "moon"
            },
            "doc_count" : 1
          }
        ]
      }
    }
  ```

  - 다음 페이지 검색
    - `after`를 추가하고, 그 값으로 위에서 받은  `after_key` 값을 넣는다.

  ```json
  GET time-test/_search
  {
    "size": 0,
    "aggs": {
      "my_buckets": {
        "composite": {
          "sources": [
            { "product": { "terms": { "field": "family_name.keyword"} } }
          ],
          "after":{"product" : "moon"}
        }
      }
    }
  }
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
  
  # 응답
  "aggregations" : {
    "avg_population" : {
      "value" : 20127.5	# 평균값은 20127.5
    }
  }
  ```

  - runtime field
    - 단일 필드가 아닌, 더 복합적인 값들의 평균을 얻을 때 사용한다.
  
  ```bash
  $ curl -XPOST "localhost:9200/exams/_search?size=0" -H 'Content-type:application/json' -d'
  {
    "runtime_mappings": {
      "grade.corrected": {
        "type": "double",
        "script": {
          "source": "emit(Math.min(100, doc['grade'].value * params.correction))",
          "params": {
            "correction": 1.2
          }
        }
      }
    },
    "aggs": {
      "avg_corrected_grade": {
        "avg": {
          "field": "grade.corrected"
        }
      }
    }
  }
  '
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
    - histogram 필드의 평균 동일한 위치에 있는 `counts` 배열의 요소와  `values` 배열의 요소를 곱한 값들의 평균이다.
    - 아래 예시의 경우, 각 히스토그램 필드에 대해 평균을 계산할 때, <1>에 해당하는 `values` 배열의 각 요소들과 <2>에 해당하는 `counts` 배열의 각 요소들을 위치에 따라 곱한 값을 더한 후, 이 값들로 평균을 구한다. 
    - 0.2~0.3에 해당하는 값이 가장 많으므로 0.2X가 결과값으로 나올 것이다.
  
  ```bash
  $ curl -XPUT "localhost:9200/my_index/_doc/1" -H 'Content-Type: application/json' -d'
  {
    "network.name" : "net-1",
    "latency_histo" : {
        "values" : [0.1, 0.2, 0.3, 0.4, 0.5], # <1>
        "counts" : [3, 7, 23, 12, 6] 			# <2>
     }
  }'
  
  $ curl -XPUT "localhost:9200/my_index/_doc/2" -H 'Content-Type: application/json' -d'
  {
    "network.name" : "net-2",
    "latency_histo" : {
        "values" :  [0.1, 0.2, 0.3, 0.4, 0.5], # <1>
        "counts" : [8, 17, 8, 7, 6] 			 # <2>
     }
  }'
  
  $ curl -XPOST "localhost:9200/my_index/_search?size=0" -H 'Content-Type: application/json' -d'
  {
    "aggs": {
      "avg_latency":
        { "avg": { "field": "latency_histo" }
      }
    }
  }'
  
  # 응답
  {
    ...
    "aggregations": {
      "avg_latency": {
        "value": 0.29690721649
      }
    }
  }
  ```



- Sum

  - 집계된 문서에서 추출한 숫자의 합계를 계산하는 single-value metrics aggregation
  - 사용하기

  ```bash
  curl -XGET "http://localhost:9200/nations/_search?size=0" -H 'Content-Type: application/json' -d'
  {  
    "aggs":{    
      "sum_population":{      
        "sum":{        
          "field": "population"      
        }    
      }  
    }
  }'
  
  # 응답
  {
    "aggregations" : {
      "sum_population" : {
        "value" : 201275.0
      }
    }
  }
  
  ```

  - runtime field
    - 단일 필드가 아닌, 더 복합적인 값들의 합계를 구할 때 사용한다.

  ```bash
  curl -XPOST "http://localhost:9200/sales/_search?size=0" -H 'Content-Type: application/json' -d'
  {
    "runtime_mappings": {
      "price.weighted": {
        "type": "double",
        "script": """
          double price = doc['price'].value;
          if (doc['promoted'].value) {
            price *= 0.8;
          }
          emit(price);
        """
      }
    },
    "query": {
      "constant_score": {
        "filter": {
          "match": { "type": "hat" }
        }
      }
    },
    "aggs": {
      "hat_prices": {
        "sum": {
          "field": "price.weighted"
        }
      }
    }
  }'
  ```

  - avg와 마찬가지로 missing 파라미터를 사용할 수 있다.

  - histogram
    - histogram 필드의 합계는 동일한 위치에 있는 `counts` 배열의 요소와  `values` 배열의 요소를 곱한 값들의 합계이다.

  ```bash
  curl -XPUT "http://localhost:9200/metrics_index/_doc/1" -H 'Content-Type: application/json' -d'
  {
    "network.name" : "net-1",
    "latency_histo" : {
        "values" : [0.1, 0.2, 0.3, 0.4, 0.5], 
        "counts" : [3, 7, 23, 12, 6] 
     }
  }'
  
  curl -XPUT "http://localhost:9200/metrics_index/_doc/2" -H 'Content-Type: application/json' -d'
  {
    "network.name" : "net-2",
    "latency_histo" : {
        "values" :  [0.1, 0.2, 0.3, 0.4, 0.5], 
        "counts" : [8, 17, 8, 7, 6] 
     }
  }'
  
  curl -XPOST "http://localhost:9200/metrics_index/_search?size=0" -H 'Content-Type: application/json' -d'
  {
    "aggs" : {
      "total_latency" : { "sum" : { "field" : "latency_histo" } }
    }
  }'
  
  # 응답
  {
    ...
    "aggregations": {
      "total_latency": {
        "value": 28.8
      }
    }
  }
  ```



- Max, Min

  - 숫자 값들의 최댓(최솟)값을 구하는 single-value metrics aggregation
  - 사용하기
    - 반환 값은 double 타입이다.

  ```bash
  $ curl -XGET "localhost:9200/nations/_search?size=0" -H 'Content-type:application/json' -d'
  {
    "aggs": {
      "max_population": {
        "max": {
          "field": "population"
        }
      }
    }
  }
  '
  
  # 응답
  "aggregations" : {
    "max_population" : {
      "value" : 126478.0
    }
  }
  ```

  - runtime field
    - 단일 필드가 아닌, 더 복합적인 값들의 최댓(최솟)값을 얻을 때 사용한다.

  ```bash
  $ curl -XPOST "localhost:9200/exams/_search?size=0" -H 'Content-type:application/json' -d'
  {
    "size": 0,
    "runtime_mappings": {
      "price.adjusted": {
        "type": "double",
        "script": """
          double price = doc['price'].value;
          if (doc['promoted'].value) {
            price *= 0.8;
          }
          emit(price);
        """
      }
    },
    "aggs": {
      "max_price": {
        "max": { "field": "price.adjusted" }
      }
    }
  }
  ```

  - avg와 마찬가지로 missing 파라미터를 사용할 수 있다.

  - histogram
    - avg와 달리 counts 배열은 무시하고 values중 최댓(최솟)값을반환한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_doc/1" -H 'Content-Type: application/json' -d'
  {
    "network.name" : "net-1",
    "latency_histo" : {
        "values" : [0.1, 0.2, 0.3, 0.4, 0.5], # <1>
        "counts" : [3, 7, 23, 12, 6] 			# <2>
     }
  }'
  
  $ curl -XPUT "localhost:9200/my_index/_doc/2" -H 'Content-Type: application/json' -d'
  {
    "network.name" : "net-2",
    "latency_histo" : {
        "values" :  [0.1, 0.2, 0.3, 0.4, 0.5], # <1>
        "counts" : [8, 17, 8, 7, 6] 			 # <2>
     }
  }'
  
  $ curl -XPOST "localhost:9200/my_index/_search?size=0" -H 'Content-Type: application/json' -d'
  {
    "aggs": {
      "max_latency":
        { "max": { "field": "latency_histo" }
      }
    }
  }'
  
  # 응답
  {
    ...
    "aggregations": {
      "max_latency": {
        "value": 0.5
      }
    }
  }
  ```





## Pipeline aggregations

### Bucket sort(pagination)

- 상위의 multi-bucket aggregation을 정렬하는데 사용한다.
  - `_key`, `_count` 혹은 sub aggs를 기준으로 정렬된다.
  - `from`, `size`를 통해 pagination이 가능하다.



- parameters
  - `sort`(List, Optional): 정렬할 필드들의 목록 
  - `from`(int, Optional): pagination을 시작 할 번호
  - `size`(int, Optional): 반환 할 bucket의 개수(기본 값은 모든 버킷을 반환)
  - `gap_policy`(Optional): data 사이에 gaps이 존재할 경우 적용할 정책(기본값은 `skip`)



- 예시

  - 기본형

  ```json
  GET test-index/_search
  {
    "bucket_sort": {
      "sort": [
        { "sort_field_1": { "order": "asc" } },   
        { "sort_field_2": { "order": "desc" } },
        "sort_field_3"
      ],
      "from": 1,
      "size": 3
    }
  }
  ```

  - sort 없이 pagination만 하는 것도 가능하다.

  ```json
  POST /test-index/_search
  {
    "size": 0,
    "aggs": {
      "sales_per_month": {
        "date_histogram": {
          "field": "date",
          "calendar_interval": "month"
        },
        "aggs": {
          "bucket_truncate": {
            "bucket_sort": {
              "from": 1,
              "size": 1
            }
          }
        }
      }
    }
  }
  ```

  





























