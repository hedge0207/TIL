# More Like This Query

- More like this query(MLT query)
  - 주어진 문서들의 집합과 가장 유사한 문서를 찾는 기능이다.
  - 동작 방식
    - Input으로 들어온 문서들에서 모든 text를 추출하고, text를 analyzer로 분석 한 뒤, 가장 높은 tf-idf 값을 가지는 term들을 선택한다.
    - 이 term들로 query를 생성하고, 생성한 query로 검색을 수행한다.
    - 사용자는 어떤 문서들을 input으로 사용할지, 어떤 term들로 집합을 구성할지, query가 어떻게 구성될지를 설정할 수 있다.
  - MLT query 제약사항
    - 검색 대상 필드는 반드시 text나 keyword type이어야한다.
    - `_source`,  `stored`, `term_vector` 중 하나는 enable 되어있어야한다.
    - 분석 속도를 높이기 위해서는 term_vector를 저장하는 것이 좋다.



- 실행 예시

  - 아래와 같이 단순히 text만 입력하는 것도 가능하다.

  ```json
  // GET /_search
  {
      "query": {
          "more_like_this" : {
              "fields" : ["title", "description"],
              "like" : "Once upon a time",
              "min_term_freq" : 1,
              "max_query_terms" : 12
          }
      }
  }
  ```

  - 혹은 아래와 같이 document와 text를 함께 주는 것도 가능하다.
    - 아래와 같이 `_index`와 `_id`(특정 index를 대상으로 검색 할 경우에는 `_id`만)를 줄 경우 해당 문서의 field들 중 `fields`에 정의된 field들의 값을 가지고 유사 문서를 찾는다.
    - 아래 query는 imdb index의 1번 문서와 2번 문서의 title과 description과 유사한 title과 description값을 가지거나 title이나 description field에 input으로 주어진 text("and potentially some more text here as well")와 유사한 값을 가지는 문서를 찾는다.

  ```json
  // GET /_search
  {
      "query": {
          "more_like_this": {
              "fields": [ "title", "description" ],
              "like": [
                  {
                      "_index": "imdb",
                      "_id": "1"
                  },
                  {
                      "_index": "imdb",
                      "_id": "2"
                  },
                  "and potentially some more text here as well"
              ],
              "min_term_freq": 1,
              "max_query_terms": 12
          }
      }
  }
  ```

  - 마지막으로, 아래와 같이 특정 색인 내에서만 text를 함께 검색하는 것도 가능하다.
    - 혹은 `doc`을 통해 임의의 문서를 만들어서 유사한 문서를 찾는 것도 가능하다.
    - 이 경우 `doc`에 정의된 field들을 가지고 유사 문서를 찾는다.
    - 아래 query는 imdb index의 문서 중에서 genre가 horror인 문서나 전체 인덱스 중에서 title이나 description의 값이 input으로 주어진 text("and potentially some more text here as well")와 유사한 문서를 찾는다.

  ```json
  GET /_search
  {
      "query": {
          "more_like_this": {
              "fields": [ "title", "description" ],
              "like": [
                  {
                      "_index": "imdb",
                      // 가상의 문서를 생성한다.
                      "doc": {
                          "genre":"horror"
                      }
                  },
                  "and potentially some more text here as well"
              ],
              "min_term_freq": 1,
              "max_query_terms": 12
          }
      }
  }
  ```



- Parameters

  - `like`
    - 유일한 required field이다.
    - 이 parameter에 설정된 문서 집합 혹은 텍스트 집합 혹은 이 둘을 합한 집합과 가장 유사한 문서를 찾는다.
    - 위에서 살펴본대로 다양한 형식으로 설정하는 것이 가능하다.

  - `unlike`
    - 이 parameter에 설정된 문서 집합 혹은 텍스트 집합 혹은 이 둘을 합한 집합과 유사하지 않은 문서를 찾는다.
    - 형식은 `like`와 동일하다.
  - `fields`
    - Text를 분석할 field들의 list이다.
    - 기본값은 `index.query.default_field` setting에 설정 된 값이다(`index.query.default_field`의 기본 값은 모든 field이다).
  - `max_query_terms`
    - 선택될 term의 최대 개수를 설정한다.
    - 이 값을 증가시킬수록 정확도는 올라가지만, query 실행 속도는 감소한다.
    - 기본값은 25이다.
  - `min_term_freq`
    - 문서에서 이 값 보다 적게 등장하는 term은 문서를 대표하는 term으로 선정되지 못한다.
    - 기본값은 2이다.
  - `min_doc_freq`
    - 전체 문서 중에서 이 값 보다 적은 수의 문서에서 등장하는 term은 문서를 대표하는 term으로 선정되지 못한다.
    - 기본 값은 5이다.
  - `max_doc_freq`
    - 문서에서 이 값 보다 많이 등장하는 term은 문서를 대표하는 term으로 선정되지 못한다.
    - 조사와 같이 매우 빈번하게 등장하는 term 들을 무시하기 위한 설정이다.
    - 기본값은 Intger type의 max 값인 2147483647(2^31-1)이다.
  - `min_word_length`
    - 문서를 대표하는 term으로 선택되기 위한 term의 최소 길이를 설정한다.
    - 기본값은 0이다.
  - `max_word_length`
    - 문서를 대표하는 term으로 선택되기 위한 term의 최대 길이를 설정한다.
    - 0으로 줄 경우 제한이 없다는 것을 의미하며, 기본값이 0이다.
  - `stop_words`
    - Stop word로 사용할 것들을 배열 형태로 줄 수 있다.
    - 여기에 설정된 term들은 문서를 대표하는 term으로 선택되지 않는다.
  - `analyzer`
    - Text를 분석하기 위한 analyzer를 설정한다.
    - 기본값은 `fields`에 설정된 첫 번째 field의 analyzer이다.
  - `minimum_should_match`
    - 추출한 term들로 생성된 query 중 최소 몇 개의 query가 맞아야 유사한 문서로 판단할지를 설정한다.
    - 기본값은 30%이다.
  - `fail_on_unsupported_field`
    - 만약 검색 대상 field들 중 text나 keyword type이 아닌 field가 있을 경우 exception을 throw할지를 설정한다.
    - 기본값은 true로, 부적절한 field가 포함되어 있을 경우 exception이 발생한다.
  - `boost_terms`
    - 생성된 query의 각 term들을 boosting하기 위한 옵션이다.
    - 기본값은 0으로 boosting하지 않는다.
  - `include`
    - Input으로 받은 document들을 결과에 포함시킬지를 설정한다.
    - 기본값은 false이다.
  - `boost`
    - 전체 query의 boost value를 설정한다.
    - 기본값은 1.0이다.







# minimum_should_match

- mininum_should_match는 반드시 matching되어야 하는 should 절의 개수를 변경하는 것이다.

  - should 절
    - should 절은 query string syntax에서  `+` operator가 붙어있지 않은 절을 의미한다.
    - 예를 들어 `name:foo name:bar name:baz +name:qux`와 같은 query string이 있을 때, should 절에 해당하는 것은 `+`가 붙어있지 않은 `name:foo`, `name:bar`, `name:baz`이다.
    - 또한 `((text:qwe text:asd text:zxc)~2)`와 같이 그룹으로 묶인 절이라 하더라도 `+`가 붙지 않았으므로 should절이다.
    - mininum_should_match를 n으로 변경하면 should 역시 적어도 n개는 포함되어야 하지만, n개만 포함된다면 나머지는 포함하지 않아도 되도록 변경된다.
  - 예시 데이터 색인하기

  ```json
  // PUT test/_doc/1
  {
    "name":"foo bar"
  }
  
  // PUT test/_doc/2
  {
    "text":"foo baz"
  }
  ```

  - 이는 bool query 내부의 should 절 안에서만 동작한다는 의미가 아니다.
    - 예를 들어 아래는 query는 should 절을 사용했음에도 minimum_should_match가 예상대로 동작하지 않는다.
    - 아래 query는 `(+text:foo +text:bar)~1`로 변환되는데, text에 foo나 bar 중 하나만 포함되어 있으면 검색 될 것 같지만 검색되지 않는다.
    - 이는 query에 should절이 없기 때문에 should 절이 1개 이상 포함될 수가 없기 때문이다.
    - 비록 query 자체는 should절에 작성되었다고 하더라도 분석된 query는 `+text:foo +text:bar`로 should가 존재하지 않는다.

  ```json
  // GET test/_search
  {
    "profile": true,
    "query": {
      "bool": {
        "should": [
          {
            "match": {
              "text": {
                "query": "foo bar",
                "operator": "and", 
                "minimum_should_match": 1
              }
            }
          }
        ]
      }
    }
  }
  ```

  - 반대로 아래 query는 bool query의 should 절과 아무 상관 없는데도 minimum_should_match가 예상대로 동작한다.
    - 아래 쿼리는 `(text:baz text:bar)~1`로 분석된다.
    - 여기서 `text:baz text:bar`가 should 절로, `text` field에 `baz`, `bar`중 하나라도 포함되는 문서는 모두 검색된다. 

  ```json
  // GET test/_search
  {
    "profile": true,
    "query": {
      "match":{
        "text":{
          "query":"baz bar",
          "minimum_should_match": 1
        }
      }
    }
  }
  ```

  - 아래도 마찬가지로 must는 무시하고 should 맥락에서만 적용된다.
    - 아래 쿼리는 `(+text:foo text:qwe)~1`와 같이 분석된다.
    - 위 쿼리에서 should의 맥락은 `text:qwe`부분인데, `text` field에 `qwe`를 포함하는 문서는 존재하지 않는다.
    - 그러므로 `minimum_should_match`의 조건을 충족시키지 못했고, 아무 문서도 검색되지 않는다.
    - 만약 `minimum_should_match`가 must절까지 고려한다면 foo가 포함된 두 문서 모두 검색이 되어야 할 것이다.

  ```json
  GET test/_search
  {
    "profile": true,
    "query": {
      "bool": {
        "must": [
          {
            "match": {
              "text": "foo"
            }
          }
        ],
        "should": [
          {
            "match": {
              "text": {
                "query": "qwe"
              }
            }
          }
        ],
        "minimum_should_match": 1
      }
    }
  }
  ```

  - 반면에 should 절에 문서가 matching되는 query를 추가하면 검색 결과가 나오게 된다.
    - 아래 쿼리는 `(+text:foo text:qwe text:bar)~1`로 분석된다.
    - 이 중에서 query 맥락은 `text:qwe text:bar`인데 `text` field에 `bar`를 포함하는 문서가 있으므로, `minimum_should_match`의 조건이 충족되어 검색 결과가 나오게 된다.

  ```json
  // GET test/_search
  {
    "profile": true,
    "query": {
      "bool": {
        "must": [
          {
            "match": {
              "text": "foo"
            }
          }
        ],
        "should": [
          {
            "match": {
              "text": {
                "query": "qwe"
              }
            }
          },
          {
            "match": {
              "text": {
                "query": "bar"
              }
            }
          }
        ],
        "minimum_should_match": 1
      }
    }
  }
  ```



- multi_match의 type이 `best_field`거나 `most_field`일 경우 `operator`와 `minimum_should_match` 옵션이 각 filed마다 개별적으로 적용된다.

  - 예를 들어 아래와 같은 문서가 있다고 가정한다.

  ```json
  {
    "foo":"hungry brown fox",
    "bar":"quick brown fox",
  }
  ```

  - 아래와 같은 query에 `cross_field`일 때와 `best_field`일 때 검색 결과가 달라지게 된다.
    - `type`이 `cross_fields`일 때는 검색이 되지만, `best_fields`일 때는 검색이 되지 않는다.

  ```json
  {
    "query": {
      "multi_match" : {
        "query":      "hungry quick",
        "type":       "best_fields",		// cross_fields
        "fields":     [ "foo", "bar" ],
        "operator":   "and" 
      }
    }
  }
  ```

  - `profile`을 통해 쿼리 식을 확인해보면 다음과 같다.

  ```json
  // best_fields일 경우
  "((+bar:hungry +bar:quick) | (+foo:hungry +foo:quick))"
  
  // cross_fields일 경우
  "+(bar:hungry | foo:hungry) +(bar:quick | foo:quick)"
  ```

  - 둘의 차이
    - `best_fields`일 경우 field 단위로 and가 적용되어 `foo`  **field**에 `hungry`와 `quick`이 포함되어있거나, `bar` **field**에 `hungry`와 `quick`이 포함되어야 한다.
    - 두 field 중 하나라도 두 term을 전부 포함하는 field가 있으면 해당 문서가 검색된다.
    - 반면에 `cross_field`의 경우 `hungry`와 `quick`이라는 **term**이 두 field중 어디에라도 모두 포함되어 있기만 하면 된다.
  - `minimum_should_match`도 마찬가지다.
    - `type`이  `cross_fields`일 때는 검색이 되지만, `best_fields`일 때는 검색이 되지 않는다.

  ```json
  {
    "query": {
      "multi_match" : {
        "query":      "hungry quick pretty",
        "type":       "best_fields",		// cross_fields
        "fields":     [ "foo", "bar" ],
        "minimum_should_match": "2" 
      }
    }
  }
  ```

  - `profile`을 통해 쿼리 식을 확인해보면 다음과 같다.

  ```json
  // best_fields일 경우
  "(((bar:hungry bar:quick bar:pretty)~2) | ((foo:hungry foo:quick foo:pretty)~2))"
  
  // cross_fields일 경우
  "((bar:hungry | foo:hungry) (bar:quick | foo:quick) (bar:pretty | foo:pretty))~2"
  ```

  - 둘의 차이
    - `best_fields`일 경우 field 단위로 `minimum_should_match`가 적용되어 `foo`  **field**에 `hungry`와 `quick`, `pretty` 중 둘 이상이 포함되어 있거나 , `bar` **field**에 세 term 중 둘 이상이 포함되어야 한다.
    - 두 field 중 하나라도 둘 이상의 term을 포함하는 field가 있으면 해당 문서가 검색된다.
    - 반면에 `cross_field`의 경우 `hungry`와 `quick`, `pretty`의 세 개의 **term** 중 두 개의 term이 field중 어디에라도 포함되어 있기만 하면 된다.



- match query

  - match 되어야 하는 최소 token의 개수를 설정한다.

  ```json
  // title에 a, b, c 중 최소 2개 이상의 토큰이 있는 문서를 검색한다.
  {
    "query": {
      "match": {
        "title": {
          "query": "a b c",
          "minimum_should_match": "2"
        }
      }
    }
  }
  ```



- bool query

  - `should` clauses들 중 반드시 match해야 하는 clauses의 수를 설정한다.
    - 예를 들어 아래 query를 통해 검색하려는 문서는 must, filter, must_not을 만족 하면서 should가 생성하는 2개의 clauses 중 최소 하나는 만족해야 한다.

  ```json
  {
    "query": {
      "bool" : {
        "must" : {
          "term" : { "user.id" : "kimchy" }
        },
        "filter": {
          "term" : { "tags" : "production" }
        },
        "must_not" : {
          "range" : {
            "age" : { "gte" : 10, "lte" : 20 }
          }
        },
        "should" : [
          { "term" : { "tags" : "env1" } },
          { "term" : { "tags" : "deployed" } }
        ],
        "minimum_should_match" : 1,
        "boost" : 1.0
      }
    }
  }
  ```




- `minimum_should_match`의 type

  - `N < M[%]`
    - 만일 전체 clauses의 개수가 N보다 작거나 같으면 전체 clauses의 개수 만큼 match되야 한다.
    - 만일 전체 clauses의 개수가 N보다 크면 M만큼이 match 되야 한다.
    - 만일 `3<3`과 같이 동일한 값을 줄 경우 clause의 개수가 3 이하면 전체 clause의 개수 만큼 match되어야 하고, cluase의 개수가 4 이상이면 3만큼 match되어야 한다.
    - 만일 그냥 3으로 줄 경우, clause의 개수가 3개 미만일 아예 검색이 되지 않게 된다는 문제가 있는데, `3<3`으로 설정하면 이러한 문제를 해결할 수 있다.

  ```json
  // 아래 query는 minimum_should_match를 3<9로 설정했고, clauses의 개수는 2이다. 
  // clauses의 개수인 2는 3보다 작으므로 최대 2개가 match되야 한다.
  {
    "profile": true,
    "query": {
      "bool": {
        "minimum_should_match": "3<9", 
        "should": [
          {
            "match": {
              "foo": "a"
            }
          },
          {
            "match": {
              "foo": "b"
            }
          }
        ]
      }
    }
  }
  
  // 검색식은 아래와 같다.
  (foo:a foo:b)~2
  
  
  // 아래 query는 위 query에서 clauses의 개수만 10개로 변경했다.
  // clauses의 개수인 10은 3보다 크기에 최대 9개가 match되야 한다.
  {
    "profile": true,
    "query": {
      "bool": {
        "minimum_should_match": "3<9", 
        "should": [
          {
            "match": {
              "foo": "a"
            }
          },
          {
            "match": {
              "foo": "b"
            }
          },
          {
            "match": {
              "foo": "c"
            }
          },
          {
            "match": {
              "foo": "d"
            }
          },
          {
            "match": {
              "foo": "e"
            }
          },
          {
            "match": {
              "foo": "f"
            }
          },
          {
            "match": {
              "foo": "g"
            }
          },
          {
            "match": {
              "foo": "h"
            }
          },
          {
            "match": {
              "foo": "i"
            }
          },
          {
            "match": {
              "foo": "j"
            }
          }
        ]
      }
    }
  }
  
  // 검색식은 아래와 같다.
  (foo:a foo:b foo:c foo:d foo:e foo:f foo:g foo:h foo:i foo:j)~9
  ```





# Profile API

- 검색 요청이 row level에서 어떻게 처리되는지를 보여준다.

  - 요청 보내기
    - 검색 API를 보낼 때 `profile` 옵션을 true로 주면 된다.

  ```json
  GET /my-index-000001/_search
  {
    "profile": true,
    "query" : {
      "match" : { "message" : "GET /search" }
    }
  }
  ```

  - Kibana의 `Management`- `Dev Tools` - `Search Profiler`에서도 확인 가능하다.



- query string syntax

  > https://www.elastic.co/guide/en/elasticsearch/reference/8.5/query-dsl-query-string-query.html#query-string-syntax
  >
  > Lucene의 query syntax를 기반으로 한다.

  - Profile API의 결과값에는 description이 포함되어 있는데, 이는 검색 API에 사용된 query를 query string syntax로 변환한 것이다.

  - 기본

    - `<field>:<term>`: field에 term이 포함되어 있다.
    - `<field>:(<term1> OR <term2>)`: term1 또는 term2가 field에 포함되어 있다.

    - `<field>:"term1 term2"`: term1, term2가 정확히 주어진 순서대로 field에 포함되어 있다.

    - `<field>.\*:term`: `*`는 와일드 카드, `\`는 escape를 위해 사용된 것이고, field의 모든 sub 필드중 하나에 term이 포함되어 있다는 뜻이다.
    - `_exists_:<field>`: field에 값이 존재하는 문서만 검색하겠다는 뜻이다.

    

  - `~`

    - fuzzy query에 사용한다.
    - `<term>~[숫자]` 형태로 사용한다. 
    - `[숫자]`에는 edit distance를 입력하며, 입력하지 않을 경우 기본값은 2이다.

  - `TO`

    - 범위를 구하기 위해 사용한다.
    - `[<range1> TO <range2>]`: range1과 range2를 포함하여, 둘 사이에 있는 값들을 검색한다.
    - `{<range1> TO <range2>}`: range1과 range2를 제외하고, 둘 사이에 있는 값들을 검색한다.
    - `{<range1> TO <range2>]`: range1이상, range2 미만의 값을 검색한다.
    - `[ TO *]`: range 이상인 값을 검색
    - `[* TO <range>]`: range 이하인 값을 검색
    - `>`, `>=`, `<`, `<=`도 사용 가능하다.

  - `^`

    - boosting에 사용한다.
    - `^[양수]`: 0이상의 값을 주는 것이 가능하며, 주지 않을 경우 기본 값은 1이다.
    - 0~1 사이의 값을 줄 경우 관련성을 감소시킨다.

  - `+`, `-`

    - `+`:는 해당 term이 반드시 포함되어야 함을 의미한다.
    - `-`는 해당 term이 포함되어선 안 된다는 것을 의미한다.
    - 예를 들어 `quick brown +fox -news`는, quick과 brown은 포함 되든 안되는 상관 없고, fox는 반드시 포함되어야 하며, news는 포함되어선 안 된다.



# kNN search

- query로 들어온 vector값과 가장 가까운 k개의 문서를 찾아준다.

  - Elasticsearch에서 vector화 시키는 기능을 제공하지는 않기에 vector화는 다른 방법을 이용하여 진행한 뒤, vector 값을 색인해야 한다.
  - 검색 대상이 되는 vector와 검색할 vector 값은 같은 차원이어야 한다.
  - Elasticsearch는 2 종류의 kNN search method를 제공한다.
    - Exact, brute-force kNN
    - Approximate kNN(ES 8.4 기준으로 아직 preview 상태)

  - Approximate kNN의 경우 아래와 같은 장단점이 있다.
    - 검색 속도가 Exact kNN에 비해 빠르다.
    - 인덱싱 속도는 Exact kNN에 비해 느리다.
    - 정확도가 떨어질 수 있다.



- Exact kNN search

  - 정확한 결과를 보장하지만, 데이터의 크기가 커질수록 정확도가 떨어질 수 있다.

  - vector data 색인하기
    - `dense_vector` type으로 색인한다.
    - `dims` 옵션에 검색할 query와 같은 차원을 입력한다(`index` 옵션을 true로 줬을 경우 1024를 넘을 수 없고, false로 주더라도 2048을 넘을 수 없다).
    - 만일 approximate kNN을 사용할 것이 아니라면 `index` 옵션을 false로 주거나 아예 빼버리면 된다(text type과 달리 dense_vector의 index 옵션의 기본값은 false이다).

  ```json
  PUT product-index
  {
    "mappings": {
      "properties": {
        "product-vector": {
          "type": "dense_vector",
          "dims": 5,
          "index": false
        },
        "price": {
          "type": "long"
        }
      }
    }
  }
  ```

  - vector 값을 색인한다.

  ```json
  POST product-index/_bulk?refresh=true
  { "index": { "_id": "1" } }
  { "product-vector": [230.0, 300.33, -34.8988, 15.555, -200.0], "price": 1599 }
  { "index": { "_id": "2" } }
  { "product-vector": [-0.5, 100.0, -13.0, 14.8, -156.0], "price": 799 }
  { "index": { "_id": "3" } }
  { "product-vector": [0.5, 111.3, -13.0, 14.8, -156.0], "price": 1099 }
  ```

  - `script_score` query를 사용하여 검색한다.

  ```json
  POST product-index/_search
  {
    "query": {
      "script_score": {
        "query" : {
          "bool" : {
            "filter" : {
              "range" : {
                "price" : {
                  "gte": 1000
                }
              }
            }
          }
        },
        "script": {
          "source": "cosineSimilarity(params.queryVector, 'product-vector') + 1.0",
          "params": {
            "queryVector": [-0.5, 90.0, -10, 14.8, -156.0]
          }
        }
      }
    }
  }
  ```



- Approximate kNN
  - `dense_vector` 필드를 대상으로 kNN search를 수행한다.
    - 색인시에 `dense_vector` 필드의  `index` prameter를 true로 줘야 한다(ES 8부터 지원).
    - 또한 `similarity` parameter에도 값을 설정해야 한다.
  - `similarity` parameter
    - 유사도 판별의 기준을 설정하는 것으로, `l2_norm`, `dot_product`, `cosine` 중 하나를 선택해야한다.
    - 공식문서에서는 `cosine` 보다 `dot_product`를 사용하는 것을 권장한다.
    - `dot_product`를 사용하려면, 모든 vector의 길이가 1로 정규화되어야 한다.
    - 따라서 `dot_product`를 사용할 경우 vector의 길이를 계산하는 연산을 수행할 필요가 없기에, 성능상 `cosine` 보다 낫다.





# Highlight

- 검색시에 어떤 query가 match되었는지를 확인할 수 있게 해주는 기능이다.
  - 복잡한 boolean query의 경우에는 정확히 highlight되지 않을 수도 있다.
  - Elasticsearch는 아래 3가지 종류의 highlighter를 제공한다.
    - unified(default highlighter)
    - plain
    - fvh(fast vector highlighter)



- unified
  - Lucene Unified highlighter를 사용하는 highlighter이다.
  - Text를 문장 단위로 쪼갠 뒤 BM25 algorithm을 사용해 각 sentence들의 점수를 매기는 방식을 사용한다.
  - fuzzy, prefix, regex 등의 multi-term highlighting도 지원한다.
  - 기본 highlighter이다.



- plain highlighter
  - Standard Lucene highlighter를 사용하는 highlighter이다.
  - 단일 fileld에 대해 단일 query를 match 시킬 때는 잘 동작하지만, 많은 document를 대상으로 여러 field에 복잡한 query로 highlight를 적용해야 할 경우 사용하지 않는 것이 좋다.
  
  - 동작 방식
    - Matching된 document에 대해 작은 in-memory index를 생성한다.
    - In-memory index를 대상으로 original query를 실행하여 low-level의 matching에 대한 정보를 받아온다.
    - 이 정보를 바탕으로 highlighting을 실행한다.
    - 이 과정을 matching된 모든 document를 대상으로 실행한다.
  
  - 한계
    - 위 과정을 모든 matching된 모든 document를 대상으로 실행하므로 memory를 많이 사용하게 된다.
    - 또한 original query를 실행하므로 original  query가 복잡해지 수록 실행에 들어가는 비용도 커진다.
    - 따라서 많은 field들을 가진 많은 양의 document들을 대상으로 plain highlighter를 사용할 경우 성능이 떨어질 수 있다.



- fvh(fast vector highlighter)
  - Lucene Fast Vector highlighter를 사용하는 highlighter이다.
  - `term_vector`가 `with_positions_offsets`으로 설정된 filed에 사용할 수 있다.
    - 이렇게 설정할 경우 index의 크기가 증가하게 된다.
  - span query를 지원하지 않는다.



- Offset stategy
  - Query로 들어온 term으로부터 의미있는 snippet들을 찾기 위해서, highlighter는 각 단어의 시작과 끝 offset을 알아야한다.
  - 이 offset에 대한 정보는 아래와 같은 방식으로 얻을 수 있다.
  - Posting list(inverted index)
    - Mapping 설정시에 `index_options`를 `offsets`으로 설정할 경우, unified highlighter는 text를 재분석하지 않고 문서를 highlight하기 위해서 postings list를 사용한다.
    - 원본 query를 postings list에 재실행하여 index로부터 offset을 추출하고, highlight된 문서들의 집합을 제한한다.
    - Text를 reanalyzing하지 않기 때문에, 큰 filed를 대상으로 highlight를 해야 할 때 특히 중요하다.
    - 또한 `term_vectors`에 비해 memory를 덜 필요로한다.
  - Term vectors
    - Mapping 설정시에 `term_vector`가 `with_positions_offsets`으로 설정되어 있을 경우, unified highlighter는 `term_vector`를 사용하여 highlighting한다.
    - 1MB 이상의 큰 field나 prefix나 wildcard 등의 multi-term query의 결과에 highlighting이 필요할 경우 특히 빠르다.
    - fvh highlighter의 경우 항상 term_vector를 사용한다.
  -  Plain highlighting
    - 다른 대안이 없을 경우 unified highlighter에 의해 사용되는 mode이다.
    - 작은 in-memory index를 생성하고, 해당 index를 대상으로 원본 query를 Lucene의 query execution planner를 통해 실행하여  document에 대한 low-level match 정보를 가져온다.
    - 이는 highlight되어야 하는 모든 문서의 모든 field에 반복 실행된다.
    - `plain` highlighter는 항상 이 mode를 사용한다.



- Highlight와 관련된 settings
  - `boundary_chars`
    - Boundary character들을 string으로 받는다.
    - 기본값은 `.,!? \t\n`이다.
  - `boundary_max_scan`
    - Boundary character를 scan할 거리를 입력한다.
    - 기본값은 20이다.
  - `boundary_scanner`
    - Highlighting된 fragments들을 어떻게 자를지를 설정한다.
    - `chars`, `sentence`, `word` 중 하나를 선택할 수 있다.
    - `unified`, `fvh` highlighter에서만 사용할 수 있으며, `unified`의 경우 `sentence`가 기본 값, `fvh`의 경우 `chars`가 기본값이다.
    - `chars`: `boundary_chars`에 설정된 character들을 highlighting boundary로 사용하며, `fvh` highlighter에서만 사용할 수 있다.
    - `sentencce`: highlight된 fragment들을 다음 sentence boundary에서 끊는다.
    - `word`: highlight된 fragment들을 다음 word boundary에서 끊는다.
  - `fields`
    - Highlights할 field들을 설정한다.
    - Wildcard를 사용할 수 있으며, 이 경우 `query`에 포함된 모든 field들을 대상으로 highlighting한다.
  - `matched_fields`
    - 여러 field들에서 match된 결과를 하나의 field에 highlighting 할 수 있도록 해준다.
    - 같은 string을 서로 다르게 analyze하는 경우에 특히 유용하다.
    - `fvh` highlighter에서만 사용할 수 있으며, `term_vector`가 `with_positions_offsets`으로 설정되어 있어야한다.
  - `highlight_query`
    - 검색 query 이외에 검색 결과를 highlight하는데 사용할 query를 추가로 정의한다.
    - Elasticsearch는 `highlight_query`에 search query가 들어가 있는지 검사하지 않기에, search query를 `highlight_query`에 포함시키지 않으면 search query의 내용은 highlight되지 않는다.
    - 입력하지 않을 경우 search query가 적용된다.
  - `number_of_fragments`(`fvh` highlighter에서만 사용 가능)
    - 반환될 fragment들의 최대 개수를 설정한다.
    - 기본 값은 0으로, 아무 fragment도 반환하지 않고, 전체 문서를 반환한다.



- `matched_fields` 테스트

  - 테스트에 필요한 data를 생성한다.
    - standard analyzer에서 running은 running, scissors는 scissors로 tokenizing된다.
    - english analyzer에서 running은 run, scissors는 scissor로 tokenizing된다.

  ```json
  // PUT highlight-test
  {
    "mappings": {
      "properties": {
        "comment":{
          "type":"text",
          "analyzer": "standard",
          "term_vector": "with_positions_offsets",
          "fields": {
            "plain":{
              "type":"text",
              "analyzer":"english",
              "term_vector": "with_positions_offsets"
            }
          }
        }
      }
    }
  }
  
  // PUT highlight-test/_doc/1
  {
    "comment":"run with scissors"
  }
  
  // PUT highlight-test/_doc/2
  {
    "comment":"running with scissors"
  }
  ```

  - running과 scissors가 포함된 문서를 검색하고, highlighting하기 위해 아래와 같이 query식을 작성했다.
    - "scissors"는 복수형 그대로 들어간 문서만 검색 됐으면 하고, `running`은 원형인 run이 들어가 있는 문서도 검색 됐으면 한다.

  ```json
  // GET highlight-test/_search
  {
      "query": {
          "bool": {
              "filter": [
                  {
                      "match": {
                          "comment": "scissors"
                      }
                  },
                  {
                      "match": {
                          "comment.plain": "running"
                      }
                  }
              ]
          }
      },
      "highlight": {
          "order":"score",
          "fields": {
              "comment": {
                  "type": "fvh"
              },
              "comment.plain": {
                  "type": "fvh"
              }
          }
      }
  }
  ```

  - 아래와 같은 결과가 나온다.
    - 결국 서로 다른 두 필드에서 highlighting된 결과를 직접 합쳐야한다.

  ```json
  "hits": [
      {
  		// ...
          "highlight": {
              "comment": [
                  "run with <em>scissors</em>"
              ],
              "comment.plain": [
                  "<em>run</em> with scissors"
              ]
          }
      },
      {
          // ...
          "highlight": {
              "comment": [
                  "running with <em>scissors</em>"
              ],
              "comment.plain": [
                  "<em>running</em> with scissors"
              ]
          }
      }
  ]
  ```

  - `matched_fields`를 적용하면 위와 같은 수고를 덜 수 있다.
    - highlight 부분을 아래와 같이 변경한다.

  ```json
  {
      // ...
      "highlight": {
          "order":"score",
          "fields": {
              "comment": {
                  "type": "fvh",
                  "matched_fields": ["comment","comment.plain"]
              }
          }
      }
  }
  ```

  - 아래와 같이 highlighting 결과가 한 필드에 모여서 나오게 된다.

  ```json
  [
      {
      	// ...
          "highlight": {
              "comment": [
                  "<em>run</em> with <em>scissors</em>"
              ]
          }
      },
      {
          // ...
          "highlight": {
              "comment": [
                  "<em>running</em> with <em>scissors</em>"
              ]
          }
      }
  ]
  ```



- `highlight_query` 테스트

  - 테스트에 필요한 data를 색인한다.

  ```json
  // PUT highlight-test/_doc/1
  {
    "text":"foo bar baz"
  }
  ```

  - 아래와 같이 검색 query에서는 "foo"가 포함된 문서를 검색하고, `highlight_qurey`에서는 bar를 검색하도록 query를 작성한 후 검색하면

  ```json
  // GET highlight-test/_search
  {
      "query": {
          "match": {
              "text": "foo"
          }
      },
      "highlight": {
          "fields": {
              "text": {
                  "highlight_query": {
                      "match": {
                          "text": "bar"
                      }
                  }
              }
          }
      }
  }
  ```

  - 다음과 같이 "foo"는 highlighting되지 않고, "bar"만 highlighting된다.

  ```json
  {
      "highlight": {
          "text": [
              "foo <em>bar</em> baz"
          ]
      }
  }
  ```

  - 주로 여러 fragments들 중 어떤 fragment를 상단으로 올릴지 결정하기 위해 사용한다.



- `query`에 포함되지 않은 field, 즉 검색 대상이 아닌 field는 `highlight.fields`에 명시하더라도 highlight가 되지 않는다.

  - 아래와 같이 색인을 했을 때.

  ```json
  // PUT highlight_test/_doc/1
  {
    "title":"foo",
    "content":"foo bar baz"
  }
  ```

  - 다음과 같이 검색하면

  ```json
  // GET highlight_test/_search
  {
    "query": {
      "term": {
        "title": "foo"
      }
    },
    "highlight": {
      "fields":{
        "content": {}
      }
    }
  }
  ```

  - 아래와 같은 결과가 나온다.
    - `content` field에도 foo가 포함되어 있음에도 highlight가 반환되지 않는다.

  ```json
  {
      // ...
      "hits": [
        {
          "_index": "highlight_test",
          "_id": "1",
          "_score": 0.18232156,
          "_source": {
            "title": "foo",
            "content": "foo bar baz"
          }
        }
      ]
  }
  ```

  - 따라서 아래와 같이 `highlight_query`를 사용해야한다.

  ```json
  {
    "query": {
      "term": {
        "title": "foo"
      }
    },
    "highlight": {
      "fields":{
        "content": {
          "highlight_query": {
            "match": {
              "content": "foo"
            }
          }
        }
      }
    }
  }
  ```



- `fragment_size`

  - 각 fragment의 character들의 최대 길이를 정한다.
    - 기본값은 100이며, 18미만으로 줄 수 없다.
  - Character들의 최대 길이를 설정하는 옵션이지만, 반환된 fragment의 character 길이는 설정 값 보다 클 수 있다.
    - 만약 단어가 중간에 잘리게 될 경우, 해당 단어를 전부 포함시켜 실제는 `fragment_size`에 설정한 값 보다 커질 수 있다.
    - 예를 들어 "An apple is a round, edible fruit produced by an apple tree (Malus domestica). "와 같은 문장이 있을 때, "edible"의  e는 21번째 character이다.
    - 이 때, `fragment_size`를 21로 주면 "An \<em>apple\</em> is a round, e"와 같이 highlighting되지 않고, "An \<em>apple\</em> is a round, edible"과 같이 마지막 character가 포함된 단어까지가 포함된다.
  - 문서상에 `boundary_scanner`가 `sentence`일 때만 유효하다는 설명은 없지만, `sentence`이외의 값을 줬을 때는 아예 validation을 안하는 것으로 봐서 `sentence`일 때만 유효한 것으로 보인다.
    - 이는 위에서 말한 것과 같이 단어의 일부 character가 `fragment_size`의 범위 안에 포함된 경우, 해당 character가 포함된 단어까지가 highlight 결과에 포함되는 것과 관련이 있다.
    - `boundary_scanner`를 `word`로 줄 경우 단어 단위로 highlighting을 하는데, `fragment_size`를 1로만 줘도 단어 전체가 포함될 것이기 때문이다.
    - 따라서 정확히는 `sentence` 이외의 `boundary_scanner` 옵션에 대해서는 `fragment_size`가 의미가 없다.
  - 테스트 data 생성

  ```json
  // PUT highlight-test
  {
      "mappings": {
          "properties": {
              "text": {
                  "type": "text",
                  "analyzer": "standard",
                  "term_vector": "with_positions_offsets"
              }
          }
      }
  }
  
  // PUT highlight-test/_doc/1
  {
    "text":"""An apple is a round, edible fruit produced by an apple tree (Malus domestica). Apple trees are cultivated worldwide and are the most widely grown species in the genus Malus. The tree originated in Central Asia, where its wild ancestor, Malus sieversii, is still found. Apples have been grown for thousands of years in Asia and Europe and were introduced to North America by European colonists. Apples have religious and mythological significance in many cultures, including Norse, Greek, and European Christian tradition."""
  }
  ```

  - 기본값으로 검색하기

  ```json
  // GET highlight-test/_search
  {
      "query": {
          "match": {
              "text": "apple"
          }
      },
      "highlight": {
          "fields": {
              "text":{}
          }
      }
  }
  
  // output
  {
      // ...
      "highlight": {
          "text": [
              "An <em>apple</em> is a round, edible fruit produced by an <em>apple</em> tree (Malus domestica).",
              "<em>Apple</em> trees are cultivated worldwide and are the most widely grown species in the genus Malus."
          ]
      }
  }
  ```

  - fragment size를 최솟값인 18로 주기
    - 각 fragment들의 길이가 줄어든 것을 확인할 수 있다.

  ```json
  // GET highlight-test/_search
  {
      "query": {
          "match": {
              "text": "apple"
          }
      },
      "highlight": {
          "boundary_scanner": "sentence",
          "fragment_size":18,
          "fields": {
              "text":{}
          }
      }
  }
  
  // output
  {
      "highlight": {
          "text": [
              "An <em>apple</em> is a round",
              "fruit produced by an <em>apple</em>",
              "<em>Apple</em> trees are cultivated"
          ]
      }
  }
  ```



- 아래와 같이 synonym을 사용해도 highlighting이 가능하다.

  - Synonym filter를 사용하는 index를 생성한다.

  ```json
  // PUT highlight_test
  {
      "settings": {
          "index": {
              "analysis": {
                  "analyzer": {
                      "synonym": {
                          "tokenizer": "standard",
                          "filter": [
                              "synonym"
                          ]
                      }
                  },
                  "filter": {
                      "synonym": {
                          "type": "synonym",
                          "lenient": true,
                          "synonyms": [
                              "foo => bar"
                          ]
                      }
                  }
              }
          }
      },
      "mappings": {
          "properties": {
              "title":{
                  "type": "text",
                  "analyzer": "synonym"
              }
          }
      }
  }
  ```

  - 검색한다.
    - 응답으로 synonym이 적용된 결과가 오는 것을 볼 수 있다.

  ```json
  // GET highlight_test/_search
  {
      "query": {
          "term": {
              "title": "bar"
          }
      },
      "highlight": {
          "fields":{
              "title": {}
          }
      }
  }
  
  // response
  {
      // ...
      "hits": [
          {
              "_index": "highlight_test",
              "_id": "1",
              "_score": 0.2876821,
              "_source": {
                  "title": "foo"
              },
              "highlight": {
                  "title": [
                      "<em>foo</em>"
                  ]
              }
          }
      ]
  }
  ```




- `required_field_match`

  - 기본적으로 `fields`에 field를 추가했다고 하더라도, query에 match된 field들만을 highlighting한다.
  - `required_field_match`는 `fields`에 추가된 fields들이 query에 match되지 않았어도, highlight를 할지를 결정한다.
    - true로 줄 경우 `fields`에 설정된 field들 중 오직 query에 match된 field만을 highlighting한다(기본값).
    - false로 줄 경우 `fields`에 설정된 field들 모두를 highlighting한다.

  - 테스트 데이터 생성

  ```json
  PUT highlight-test
  {
    "mappings": {
      "properties": {
        "foo": {
          "type": "text",
          "analyzer": "standard",
          "term_vector": "with_positions_offsets"
        },
        "bar": {
          "type": "text",
          "analyzer": "standard",
          "term_vector": "with_positions_offsets"
        }
      }
    }
  }
  
  PUT highlight-test/_doc/1
  {
    "foo":"An apple is a round, edible fruit produced by an apple tree (Malus domestica).",
    "bar":"An apple is a round, edible fruit produced by an apple tree (Malus domestica)."
  }
  ```

  - `required_field_match`를 true로 두고 검색하기
    - `highlight.fields`에는 `foo`, `bar` 두 field를 모두 지정해주었지만, query는 `foo` field 만을 대상으로 검색했으므로, 아래와 같이 검색 대상 field인 `foo`만 highlighting된다.

  ```json
  // GET highlight-test/_search
  {
      "query": {
          "match": {
              "foo": "apple"
          }
      },
      "highlight": {
          "boundary_scanner": "sentence",
          "fields": {
              "foo":{},
              "bar":{}
          }
      }
  }
  
  // output
  {
      "highlight": {
          "foo": [
              "An <em>apple</em> is a round, edible fruit produced by an <em>apple</em> tree (Malus domestica)."
          ]
      }
  }
  ```

  - `required_field_match`를 false로 두고 검색하기
    - 검색 대상 field가 아닌 `bar` field까지도 highlighting된 것을 볼 수 있다.

  ```json
  // GET highlight-test/_search
  {
      "query": {
          "match": {
              "foo": "apple"
          }
      },
      "highlight": {
          "boundary_scanner": "sentence",
          "require_field_match": false, 
          "fields": {
              "foo":{},
              "bar":{}
          }
      }
  }
  
  // output
  {
      "highlight": {
          "bar": [
              "An <em>apple</em> is a round, edible fruit produced by an <em>apple</em> tree (Malus domestica)."
          ],
          "foo": [
              "An <em>apple</em> is a round, edible fruit produced by an <em>apple</em> tree (Malus domestica)."
          ]
      }
  }
  ```



- Highlighter의 동작 방식
  - Highlighter의 목표는 query에 대한 최적의 fragment를 찾아내서, 찾아낸 fragment 내에서 검색어를 highlighting하는 것이다.
    - 이를 위해 highlighter는 아래와 같은 정보를 처리해야한다.
  - Text를 어떻게 fragment로 쪼갤 것인가.
    - `fragment_size`, `fragmenter`, `type`, `boundary_chars`, `boundary_max_scan`, `boundary_scanner`, `boundary_scanner_locale` 설정들과 관련이 있다.
    - Plain highlighter의 경우 주어진 analyzer를 활용하여 text를 analyze하여 token stream을 생성한다.
    - Plain highlighter는 token stream을 fragment로 쪼개기 위해 매우 단순한 algorithm을 사용한다.
    - Token stream을 term 단위로 순회하면서, 현재 term의 end_offset이, `fragment_size`와 생성된 fragment의 개수를 곱한 값을 초과할 경우 새로운 fragment를 생성한다(즉 `end_offset > fragment_size * num_of_created_fragment`이면 새로운 fragment를 생성한다).
    - Unified와 FVH highlighter의 경우 Java의 `BreakIterator`를 사용하여 text를 fragment로 쪼갠다.
  - 최적의 fragment는 어떻게 찾을 것인가.
    - `number_of_fragments` 설정과 관련이 있다.
    - 가장 관련이 있는 fragment들을 찾기 위해서 highlighter는 주어진 query를 반영하여 각 fragment의 점수를 매긴다.
    - Plain highlighter는 token-stream을 가지고 in-memory index를 생성하여 원본 query를 in-memory index에 재실행한다.
    - 이 결과를 가지고 각 fragment들에 점수를 매기는데, 점수 산정 fragment에 포함된 고유한 term의 개수를 세는 방식으로 이루어진다.
    - 예를 들어 "foo bar foo"라는 term으로 검색했을 때, "foo bar"라는 fragment와 "foo bar foo"라는 fragment의 점수는 동일하게 매겨진다.
    - "foo bar foo"에는 foo가 2번 포함되어 있기는 하지만, 고유한 term의 개수만 세기에, 몇 번 나왔는지는 점수에 영향을 미치지 않는다.
    - FVH의 경우에는 이미 색인된 term vectors를 사용하기에, analyzing과 in-memory index를 필요로하지 않는다.
    - 점수를 매기는 방식은 Plain highlighter와 유사하지만, 고유한 term의 개수가 아닌, 모든 개별 term을 가지고 점수를 계산한다.
    - Unified highlighter는 이미 색인된 term vectors와 미리 색인된 terms offsets를 사용하며, 만일, 미리 색인된 term vectors와 terms offset이 없다면, Plain highlighter와 마찬가지로 text로부터 in-memory index를 생성한다.
    - Unified highlighter의 경우 점수를 계산하기 위해 BM25를 사용한다.



- Highlighter 동작 방식 예시

  - Data 색인하기

  ```json
  // PUT test_index
  {
      "mappings": {
          "properties": {
              "content": {
                  "type": "text",
                  "analyzer": "english"
              }
          }
      }
  }
  
  // PUT test_index/_doc/1
  {
    "content" : "An apple is a round, edible fruit produced by an apple tree (Malus domestica)."
  }
  ```

  - 검색하기

  ```json
  // GET test_index/_search
  {
      "query": {
          "match_phrase" : {
              "content" : "apple tree"
          }
      },
      "highlight": {
          "type" : "unified",
          "number_of_fragments" : 3,
          "fields": {
              "content": {}
          }
      }
  }
  
  ```

  - In-memoery index 생성
    - 1번 문서가 query에 hit되고, unified highlighter에 넘겨진다.
    - `content` field는 offset이나 term vectors가 색인되지 않았기에, field value가 analyze되고, in-memory index가 생성된다.

  ```json
  [
      {"token":"apple","start_offset":3,"end_offset":8,"position":1},
      {"token":"apple","start_offset":49,"end_offset":54,"position":10},
      {"token":"tree","start_offset":55,"end_offset":59,"position":11}
  ]
  ```

  - 위에서 작성한 match_phrase query는 `spanNear([text:apple, text:tree], 0, true)` 형태의 span qeury로 전환된다.
    - 이는 apple과 term이 0 distance 이내에 있으면서, 주어진 순서대로 나와야 함을 의미한다.
    - 이전에 생성한 in-memory index에 위 span query를 실행하면, 아래와 같은 match를 얻을 수 있다.

  ```json
  [
      {"token":"apple","start_offset":49,"end_offset":54,"position":10},
      {"token":"tree","start_offset":55,"end_offset":59,"position":11}
  ]
  ```

  - Text를 passage로 쪼갠다.
    - 각 passage는 적어도 하나의 match를 포함해야한다.
    - Java의 `BreakIterator`는 각 passage가 `fragment_size`를 초과하지 않는한, 전체 문장이 되도록 쪼갠다.
  - 각 passage의 점수를 BM25로 계산하여 `number_of_fragments` 만큼의 passage를 선정한다.
  - 마지막으로, 각 passage와 일치하는 일치하는 string을 text로부터 추출한다.



- Highlighting은 오직 반환 대상 문서들을 대상으로만 실행된다.

  - 따라서 highlighting에 문제가 있는 문서가 있다고 하더라도 해당 문서가 반환 대상 문서가 아니라면 error가 발생하지 않는다.
  - Test를 위한 data를 색인한다.
    - "foo"를 검색했을 때 둘 다 검색될 수 있도록 두 문서 모두 foo를 포함시킨다.

  ```json
  // PUT highlighting_test/_doc/1
  {
    "text":"foo bar"
  }
  
  // PUT highlighting_test/_doc/2
  {
    "text":"foo"
  }
  ```

  - Data와 함께 생성된 index의 `index.highlight.max_analyzed_offset` 값을 변경해 1번 문서를 highlighting할 때 error가 발생하도록 조작한다.
    - 아래와 같이 변경하면 highlighting시에 최대 3개의 chacater까지만 분석 대상으로 하기 때문에 `text` field가 3글자로 이루어진 2번 문서는 문제가 없지만 7글자로 이루어진 1번 문서는 error가 발생하게 된다.

  ```json
  // PUT highlighting_test/_settings
  {
    "index": {
      "highlight": {
        "max_analyzed_offset":3
      }
    }
  }
  ```

  - 두 문서가 모두 반환되도록 highlight를 포함하여 검색을 실행한다.
    - 아래 query를 실행하면 `text`field의 값의 길이가 `index.highlight.max_analyzed_offset`에 설정된 값을 초과했다는 message와 함께 `search_phase_execution_exception` error가 발생한다.

  ```json
  // GET highlighting_test/_search
  {
      "query": {
          "match": {
              "text": "foo"
          }
      },
      "highlight": {
          "fields": {
              "text": {}
          }
      }
  }
  ```

  - 반면에 2번 문서만 반환되도록 highlight를 포함하여 검색을 실행하면 결과는 정상적으로 나온다.
    - `size`를 1로 주면 tf값이 더 커 점수가 커진 2번 문서가 반환되며, highlgiht가 error 없이 정상 실행되는 것을 볼 수 있다. 
    - 아래에서는 `size`를 조절했지만, `sort` 등 반환 문서를 변경하는 어떤 조작이든 마찬가지다.

  ```json
  // GET highlighting_test/_search
  {
      "size":1,
      "query": {
          "match": {
              "text": "foo"
          }
      },
      "highlight": {
          "fields": {
              "text": {}
          }
      }
  }
  ```

  - 결론
    - Highlighting이 불가능한 문서가 있다고 하더라도, 해당 문서가 검색 되고 반환 대상에 포함되지 않는 한 문제가 발생하지는 않는다.
    - 그러나 오히려 이러한 점 때문에 문제가 발생했을 때 원인을 파악하는 것이 까다로울 수 있다.
    - 따라서 highlighting을 실행해야 할 경우 관련 설정을 정확히 확인해야 한다.





# Collapse

- 검색 결과에서 중복되는 문서를 하나로 묶고 싶을 때 사용하는 parameter이다.
  - 중복 여부는 특정 필드를 기준으로 판단한다.
    - 대상 필드는 `doc_values`가 활성화 된 keyword 필드나 numeric 필드여야 한다.
    - 여러 개의 필드를 기준으로 묶는 것은 불가능하다.
    - 그러나 묶인 필드 내에서 또 다른 필드로 다시 묶는 것은 가능하다.
  - 정렬 결과 가장 최상단에 있는 것이 대표 문서가 된다.



- 예시

  - 예시 데이터 색인

  ```json
  // POST collapse-test/_bulk
  { "index": { "_id": "1" } }
  { "name":"John", "age":28}
  { "index": { "_id": "2" } }
  { "name":"John", "age":28}
  { "index": { "_id": "3" } }
  { "name":"John", "age":27}
  { "index": { "_id": "4" } }
  { "name":"John", "age":26}
  { "index": { "_id": "5" } }
  { "name":"Tom", "age":55}
  { "index": { "_id": "6" } }
  { "name":"Tom", "age":37}
  { "index": { "_id": "7" } }
  { "name":"Henry","age":22}
  ```

  - 검색
    - 이름을 검색으로 중복 여부를 판단하며, 나이를 기준으로 오름차순 정렬하여, 나이가 가장 어린 사람의 문서가 대표 문서가 되도록 한다.

  ```json
  // GET collapse-test/_search
  {
    "collapse": {
      "field": "name.keyword"
    },
    "sort": [
      {
        "age": {
          "order": "asc"
        }
      }
    ]
  }
  ```

  - 결과
    - name 필드의 값이 John인 문서들 중, age 값이 가장 낮은 4번 문서가 대표 문서가 된다.

  ```json
  {
      "hits": [
          {
              "_index": "collapse-test",
              "_type": "_doc",
              "_id": "7",
              "_score": null,
              "_source": {
                  "name": "Henry",
                  "age": 22
              },
              "fields": {
                  "name.keyword": [
                      "Henry"
                  ]
              },
              "sort": [
                  22
              ]
          },
          {
              "_index": "collapse-test",
              "_type": "_doc",
              "_id": "4",
              "_score": null,
              "_source": {
                  "name": "John",
                  "age": 26
              },
              "fields": {
                  "name.keyword": [
                      "John"
                  ]
              },
              "sort": [
                  26
              ]
          },
          {
              "_index": "collapse-test",
              "_type": "_doc",
              "_id": "6",
              "_score": null,
              "_source": {
                  "name": "Tom",
                  "age": 37
              },
              "fields": {
                  "name.keyword": [
                      "Tom"
                  ]
              },
              "sort": [
                  37
              ]
          }
      ]
  }
  ```



- `inner_hits`를 통해 어떤 문서들이 묶였는지 확인이 가능하다.

  - query

  ```json
  // GET collapse-test/_search
  {
    "collapse": {
      "field": "name.keyword",
      "inner_hits":{
        "name": "test-inner-hits"
      }
    },
    "sort": [
      {
        "age": {
          "order": "asc"
        }
      }
    ]
  }
  ```

  - 결과

  ```json
  // 생략
  {
      "_index": "collapse-test",
      "_type": "_doc",
      "_id": "6",
      "_score": null,
      "_source": {
          "name": "Tom",
          "age": 37
      },
      "fields": {
          "name.keyword": [
              "Tom"
          ]
      },
      "sort": [
          37
      ],
      "inner_hits": {
          "test-inner-hits": {
              "hits": {
                  "total": {
                      "value": 2,
                      "relation": "eq"
                  },
                  "max_score": 0.0,
                  "hits": [
                      {
                          "_index": "collapse-test",
                          "_type": "_doc",
                          "_id": "5",
                          "_score": 0.0,
                          "_source": {
                              "name": "Tom",
                              "age": 55
                          }
                      },
                      {
                          "_index": "collapse-test",
                          "_type": "_doc",
                          "_id": "6",
                          "_score": 0.0,
                          "_source": {
                              "name": "Tom",
                              "age": 37
                          }
                      }
                  ]
              }
          }
      }
  }
  ```



- 중첩해서 사용하는 것도 가능하다.

  - 예시
    - `inner_hits` 내부에 `collapse` parameter를 추가한다.

  ```json
  GET collapse-test/_search
  {
    "collapse": {
      "field": "name.keyword",
      "inner_hits":{
        "name": "test-inner-hits",
        "collapse": { 
          "field": "age" 
        }
      }
    },
    "sort": [
      {
        "age": {
          "order": "asc"
        }
      }
    ]
  }
  ```

  - 결과
    - name과 age가 같은 2번 문서가 그룹핑 됐다.

  ```json
  {
      "_index": "collapse-test",
      "_type": "_doc",
      "_id": "4",
      "_score": null,
      "_source": {
          "name": "John",
          "age": 26
      },
      "fields": {
          "name.keyword": [
              "John"
          ]
      },
      "sort": [
          26
      ],
      "inner_hits": {
          "test-inner-hits": {
              "hits": {
                  "total": {
                      "value": 4,
                      "relation": "eq"
                  },
                  "max_score": null,
                  "hits": [
                      {
                          "_index": "collapse-test",
                          "_type": "_doc",
                          "_id": "1",
                          "_score": 0.0,
                          "_source": {
                              "name": "John",
                              "age": 28
                          },
                          "fields": {
                              "age": [
                                  28
                              ]
                          }
                      },
                      // 후략
                  ]
              }
          }
      }
  }
  ```



- 둘 이상의 field로 중복 문서를 grouping하는 것은 불가능하다.
  - 둘 이상의 field로 중복 문서를 그룹핑하는 방법에는 아래와 같은 방법들이 있다.
    - aggregation 사용
    - collpase 내의 inner_hits를 받아서 수동으로 grouping
    - 중복 여부를 판단하려는 두 필드의 값을 결합한 필드를 생성하여 색인
  - aggregation의 경우 문서의 크기에 따라 자원을 많이 사용할 수 있다는 문제가 있다.
  - inner_hits 를 받아서 수동으로 grouping하는 것도 검색 이후에 모든 문서를 수동으로 확인해야 하므로 비효율적이다.
  - 따라서 그나마 효율적인 방법은 중복 여부를 판단하려는 필드들을 조합하여 hash 값을 만들고, 그 hash 값을 색인하여 hash값 기반으로 중복 여부를 판단하는 것이다.



# 여러 index 대상 검색

- 여러 index를 대상으로 검색하기

  - Elasticsearch는 여러 index 혹은 data stream을 대상으로 검색하는 기능을 제공한다.
    - 아래와 같이 검색 API 요청시에 검색하고자 하는 index 혹은 data stream들을 콤마(`,`)로 구분하여 넘기면 된다.
    - 혹은 asterisk(`*`)를 사용하여 pattern matching 방식도 사용할 수 있다.

  ```json
  // GET foo,bar/_search
  {
    "query": {
      "match": {
        "title": "world"
      }
    }
  }
  
  // GET test-*/_search
  {
    "query": {
      "match": {
        "title": "world"
      }
    }
  }
  ```

  - Cluster 내의 모든 index를 대상으로 검색하려면 아래와 같은 방법들을 사용하면 된다.
    - Search API에서 index를 뺀다.
    - Index를 입력하는 위치에 `*` 혹은 `_all`을 입력한다.

  ```json
  // GET /_search
  {
    "query": {
      "match": {
        "title": "world"
      }
    }
  }
  
  // GET _all/_search
  {
    "query": {
      "match": {
        "title": "world"
      }
    }
  }
  
  // GET */_search
  {
    "query": {
      "match": {
        "title": "world"
      }
    }
  }
  ```

  - 특정 index에 boost를 주는 것도 가능하다.
    - 아래 index에도 pattern matching을 사용할 수 있다.

  ```json
  // GET /_search
  {
    "indices_boost": [
      { "foo": 1.4 },
      { "bar": 1.3 }
    ]
  }
  ```



- 여러 index를 대상으로 검색할 때 일부 index에서만 검색에 실패할 경우

  - 아래와 같이 2개의 index를 준비한다.
    - `foo` index는 아무런 mapping도 설정하지 않고 그대로 설정하고, `bar` index는 text field를 keyword type으로 설정하여 생성한다.

  ```json
  // PUT foo
  
  // PUT bar
  {
    "mappings": {
      "properties": {
        "text":{
          "type":"keyword"
        }
      }
    }
  }
  ```

  - 두 index에 동일한 data를 색인한다.

  ```json
  // PUT foo/_doc/1
  {
    "text":"hello"
  }
  
  // PUT bar/_doc/1
  {
    "text":"hello"
  }
  ```

  - 두 index를 대상으로 aggregation을 실행한다.
    - `terms` aggregation은 keyword field에만 실행이 가능하다.
    - `bar` index의 경우 text field를 keyword type으로 설정하여 생성했으므로 aggregation이 가능하지만, `foo` field의 경우 text field가 text type으로 동적으로 설정되어 aggregation이 불가능하다.

  ```json
  // GET foo,bar/_search
  {
    "aggs": {
      "qwe": {
        "terms": {
          "field": "text"
        }
      }
    }
  }
  ```

  - 결과
    - Aggregation이 가능한 `bar` index만을 대상으로 aggregation이 실행된 것을 확인할 수 있다.
    - Aggregation으로 인해 error가 발생했지만, foo index는 검색 결과도 반환하지 않는다.

  ```json
  {
    "took": 16,
    "timed_out": false,
    "_shards": {
      "total": 2,
      "successful": 1,
      "skipped": 0,
      "failed": 1,
      "failures": [
        {
          "shard": 0,
          "index": "foo",
          "node": "3g2e2-er2-er323gweg33g",
          "reason": {
            "type": "illegal_argument_exception",
            "reason": "Fielddata is disabled on [text] in [foo]. Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [text] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
          }
        }
      ]
    },
    "hits": {
      "total": {
        "value": 1,
        "relation": "eq"
      },
      "max_score": 1,
      "hits": [
        {
          "_index": "bar",
          "_id": "1",
          "_score": 1,
          "_source": {
            "text": "hello"
          }
        }
      ]
    },
    "aggregations": {
      "qwe": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "hello",
            "doc_count": 1
          }
        ]
      }
    }
  }
  ```



- 여러 index를 대상으로 검색할 때 aggregation

  - 여러 index를 대상으로 검색할 때 aggregation 결과도 합쳐지는지 확인하기 위해 아래와 같이 3개의 index를 동일한 mapping으로 생성한다.

  ```json
  // PUT index1
  {
    "mappings": {
      "properties": {
        "text":{
          "type":"keyword"
        }
      }
    }
  }
  
  // PUT index2
  {
    "mappings": {
      "properties": {
        "text":{
          "type":"keyword"
        }
      }
    }
  }
  
  // PUT index3
  {
    "mappings": {
      "properties": {
        "text":{
          "type":"keyword"
        }
      }
    }
  }
  ```

  - 3개의 index에 data를 색인한다.

  ```json
  // PUT index1/_doc/1
  {
      "text":"foo"
  }
  
  // PUT index2/_doc/1
  {
      "text":"foo"
  }
  
  // PUT index3/_doc/1
  {
      "text":"foo"
  }
  ```

  - 세 개의 index를 대상으로 aggregation을 실행한다.

  ```json
  // GET index*/_search
  {
    "size": 0,
    "aggs": {
      "my_terms": {
        "terms": {
          "field": "text"
        }
      }
    }
  }
  ```

  - 결과 확인
    - 아래와 같이 세 개의 index를 대상으로 aggregation이 실행된 것을 확인할 수 있다.

  ```json
  {
      // ...
      "aggregations": {
      "my_terms": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
          {
            "key": "foo",
            "doc_count": 3
          }
        ]
      }
    }
  }
  ```

  

  



# 엘라스틱서치 모니터링

## Head

- Head
  - 클러스터의 상태를 모니터링 할 수 있는 모니터링 도구 중 하나.
  - 가장 큰 장점 중 하나는 샤드 배치 정보를 확인할 수 있다는 점이다.



- 설치하기
  - 기존에는 플러그인 방식을 사용했지만 ES6 이상부터는 보안상의 이유로 플러그인 방식을 사용하지 않는다.
  - https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm 에서 확장 프로그램을 추가하여 사용이 가능하다.



- Overview
  - 클러스터를 구성하는 노드들의 이름과 인덱스 이름, 인덱스를 구성하는 샤드와 인덱스에 저장된 문서의 건수를 살펴볼 수 있다.
  - 노드의 Info 버튼
    - Cluster Node Info는 해당 노드의 호스트명과 아이피 등의 여러 가지 설정을 확인 가능하다. 
    - Node Stats는 노드의 기본 정보와 클러스터에서 수행된 동작들의 통계 정보를 확인할 수 있다. 간단한 수치이기 때문에 특별히 유의미한 정보는 아니다.
  - 노드의 Actions 버튼
    - Shutdown 메뉴는 동작하지 않는다.
    - 프로세스의 종료는 가급적이면 시스템에 접근하여 실행하는 것이 로그나 클러스터 상태를 살피기에 좋다.
  - 인덱스의 Info 버튼
    - Index Status는 해당 인덱스의 문서 개수나 삭제된 문서 개수, 사이즈, 해당 인덱스를 대상으로 수행한 동작들의 통계 정보를 보여준다. 이 값도 단순한 수치이기 때문에 특별히 유의미한 정보는 아니다.
    - Index Metadata는 인덱스의 open/close 여부와 함께 인덱스를 구성하는 정보인 settings, mappings, aliases 정보를 보여준다. 해당 정보는 인덱스가 어떻게 구성되어 있는지 한 눈에 확인할 때 유용하다.
  - 인덱스의 Actions 버튼
    - New Alias, Refresh, Flush 등의 드롭다운 메뉴가 존재한다.
    - 인덱스 alias, refresh, forcemerge, close, delete 등 인덱스에 수행할 수 있는 다양한 작업을 진행 가능하다.



- Indices
  - 클러스터 내에 생성한 인덱스의 이름과 크기, 문서의 개수를 요약하여 보여준다.
  - Overview 탭에서도 확인 가능하지만 인덱스가 많아져 전체 인덱스를 한 눈에 확인하기 어려울 때 사용한다.



- Browser
  - 생성한 인덱스와 타입, 문서의 필드에 해당하는 내용들을 확인 가능하다.
  - 검색 API를 사용하지 않고도 인덱스내에 어떤 문서들이 어떤 타입으로 생성되어 있는지 하나씩 확인 가능하다.



- Structured Query
  - 특정 인덱스를 선택하여 간단하게 쿼리를 해볼 수 있는 탭이다.
  - 드롭다운 메뉴에서 항목들을 선택하고 Search 버튼을 누르면 원하는 검색 결과를 확인할 수 있다.'



- Any Request
  - Head에 연결시킨 클러스터에 쿼리를 요청할 수 있다.
  - Structured Query가 구조화된 검색 쿼리만 요청할 수 있는 반면, 다양한 요청을 전달할 수 있다.
  - 기본으로는 POST 메서드로 _search API를 호출하도록 되어 있다.
  - 하단의 Request를 클릭하면 정의한 사항들을 클러스터에 요청한다.





## X-Pack

- X-Pack
  - 베이직 라이선스로 활용할 수 있으며, 베이직 라이선스는 무료로 사용할 수 있다.
  - 6.3 이전 버전은 1년에 한 번 베이직 라이선스를 재활성화하기 위해 클러스터의 노드를 전부 삭제해야 한다.
  - 6.3 이후 버전부터 라이선스를 규칙적으로 갱신하지 않아도 모니터링 기능을 사용할 수 있다.



- 설치하기
  - ES 6.3 버전 이후부터는 ES 를 설치하면 자동으로 설치된다.
  - Kibana를 설치해야 한다.

    - Kibana는 ES에 저장된 로그를 검색하거나 그래프 등으로 시각화할 때 사용하는 도구다.
    - 사실상 ES의 웹 UI와 같은 역할을 하는 도구라고 생각하면 된다.

    - 공식 홈페이지에서 다운로드 가능하다.



- 프로메테우스
  - 위의 두 가지 외에도 프로메테우스를 사용해서도 모니터링이 가능하다.
    - 오픈 소스 기반의 모니터링 시스템.
    - 데이터를 시간의 흐름대로 저장할 수 있는 시계열 데이터베이스의 일종.
    - 수집된 데이터를 바탕으로 임계치를 설정하고 경고 메세지를 받을 수 있는 오픈소스 모니터링 시스템이다.
    - ES 외에도 많은 시스템을 모니터링할 수 있게 해준다.
  - 컴포넌트 구성
    - 중앙에 TSDB(Time Series Data Base)의 역할을 하는 Prometheus Server가 존재한다.
    - 각종 지표들을 Exporter라는 컴포넌트를 통해서 가져올 수 있다.
    - Push Gateway를 통해서 입력할 수도 있다.
    - 각 항목에 대한 임계치를 설정하여 Alert Manager를 통해 경고 메시지를 받을 수도 있다.





