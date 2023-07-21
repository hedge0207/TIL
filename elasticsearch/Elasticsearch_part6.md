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
    - Wildcard를 사용할 수 있다.
  - `matched_fields`
    - 여러 field들에서 match된 결과를 하나의 field에 highlighting 할 수 있도록 해준다.
    - 같은 string을 서로 다르게 analyze하는 경우에 특히 유용하다.
    - `fvh` highlighter에서만 사용할 수 있으며, `term_vector`가 `with_positions_offsets`으로 설정되어 있어야한다.
  - `highlight_query`
    - 검색 query 이외에 검색 결과를 highlight하는데 사용할 query를 추가로 정의한다.
    - Elasticsearch는 `highlight_query`에 search query가 들어가 있는지 검사하지 않기에, search query를 `highlight_query`에 포함시키지 않으면 search query의 내용은 highlight되지 않는다.
    - 입력하지 않을 경우 search query가 적용된다.



- `matched_fields` 테스트

  - 테스트에 필요한 data를 생성한다.
    - standard analyzer에서 running은 running, scissors는 scissors로 tokenizing된다.
    - english analyzer에서 running은 run, scissors는 scissor로 tokenizing된다.

  ```json
  PUT highlight-test
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
  
  PUT highlight-test/_doc/1
  {
    "comment":"run with scissors"
  }
  
  PUT highlight-test/_doc/2
  {
    "comment":"running with scissors"
  }
  ```

  - running과 scissors가 포함된 문서를 검색하고, highlighting하기 위해 아래와 같이 query식을 작성했다.
    - "scissors"는 복수형 그대로 들어간 문서만 검색 됐으면 하고, `running`은 원형인 run이 들어가 있는 문서도 검색 됐으면 한다.

  ```json
  GET highlight-test/_search
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
  PUT highlight-test/_doc/1
  {
    "text":"foo bar baz"
  }
  ```

  - 아래와 같이 검색 query에서는 "foo"가 포함된 문서를 검색하고, `highlight_qurey`에서는 bar를 검색하도록 query를 작성한 후 검색하면

  ```json
  GET highlight-test/_search
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







# Stopword

- stopword 파일을 수정한 후 적용하려면 index를 close, open해줘야 한다.



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





# 색인 성능 최적화

- 색인 성능 최적화의 필요성
  - ES는 클러스터 환경으로 구축할 수 있기 때문에 노드 추가를 통해 색인 성능을 더 높일 수 있다.
  - 그러나 ES 설정을 변경함으로써 불필요한 리소스를 줄일 수 있고, 이를 통해 색인 성능을 향상시킬 수 있다.



- 정적 매핑 적용하기

  - 앞서(Elasticsearch_part1) 살펴본 동적 매핑과 정적 매핑을 다시 간단하게 표로 정리하면 다음과 같다.

  | 방식      | 장점                                   | 단점                            |
  | --------- | -------------------------------------- | ------------------------------- |
  | 동적 매핑 | 미리 매핑 정보를 생성하지 않아도 된다. | 불필요한 필드가 생길 수 있다.   |
  | 정적 매핑 | 필요한 필드만 정의해서 사용할 수 있다. | 미리 매핑 정보를 생성해야 한다. |

  - 정적 매핑의 이점
    - 동적 매핑을 사용하면 불필요한 매핑 정보가 생성될 수 있으며, 이러한 불필요한 매핑 정보는 불필요한 색인 작업을 유발하게 되어 색인 성능을 저하시킬 수 있다.
    - 반대로 정적 매핑을 사용하면 필요한 필드들만 정의해서 사용할 수 있고 불필요한 매핑 정보를 사용하지 않기 때문에 색인 성능을 향상시킬 수 있다.
  - 문자열 형태의 필드에서 색인 성능 차이가 더 크게 발생한다.
    - 기존에 정의되지 않은 필드에 문자열 데이터를 추가할 경우(즉 동적 매핑을 할 경우), text 타입으로 생성이 되지만 동시에 keyword 타입으로도 생성이 된다.
    - 즉 , 문자열 데이터에 대한 동적 매핑 결과는 text 타입과 keyword 타입 두개 의 타입을 만든다.
    - 또한 동적 매핑에 의해 생성되는 keyword 타입은 `ignore_above`라는 속성이 하나 더 붙는데 문자열 중 해당 길이 이상인 값은 색인에 포함하지 않는다는 뜻이다.
    - 정적 매핑으로 문자열 데이터에 대한 타입을 미리 text 혹은 keyword로 생성해 놓으면 두 번 해야 할 색인 작업이 한 번으로 줄어들게 된다.

  ```json
  // 정적 매핑으로 문자열 데이터를 담을 필드를 추가한 경우
  {
    "name" : {
      "type" : "text"
    }
  }
  // 동적 매핑으로 문자열 데이터를 추가한 경우
  "ename" : {
    "type" : "text",
    "fields" : {
        "keyword" : {
            "type" : "keyword",
            "ignore_above" : 256
        }
     }
  },
  ```



- refresh_interval 변경하기

  - refresh
    - ES는 색인되는 모든 문서들을 메모리 버퍼 캐시에 먼저 저장한 후 특정 조건이 되면 메모리 버퍼 캐시에 저장된 색인 정보나 문서들을 디스크에 세그먼트 단위로 저장한다.
    - 색인된 문서는 이렇게 세그먼트 단위로 저장되어야 검색이 가능해지며, 이런 일련의 작업들을 refresh라 한다.
  - refresh_interval
    - 이 refresh를 얼마나 주기적으로 할 것인지를 결정하는 값이 refresh_interval이다.
    - 기본값은 1초이다.
    - ES가 준 실시간 검색 엔진이라 불리는 것은 refresh_interval이 1초로 설정되어 있어 문서가 색인되고 1초 후에 검색이 가능하기 때문이다.
    - refresh 작업은 디스크 I/O를 발생시키기 때문에 성능을 저하시킬 수 있다.
    - 그렇다고 I/O 발생을 늦추기 위해 refresh_interval을 길게 주면 색인된 문서를 검색할 수 없어 ES 본연의 기능에 문제가 생길 수 있다.
  - refresh_interval 변경
    - 실시간 검색 엔진으로 사용하고자 한다면 1초로 설정해야 한다.
    - 그러나 대용량의 로그를 수집하는 것이 주된 목적이고 색인한 로그를 당장 검색해서 사용할 필요가 없다면 refresh_interval을 충분히 늘려서 색인 성능을 확보할 수 있다.
    - 만일 문서가 1초에 한 건씩 들어오고  refresh_interval이 1초라면 초당 한 건씩 디스크에 문서를 저장하게 되고 총 5 번의 Disk I/O가 발생한다.
    - 반면에 문서는 그대로 1초에 한 건씩 들어오지만 refresh_interval이 5초라면 5건의 문서를 한 번에 저장하게 되고 총 한 번의 Disk I/O만 발생한다.
    - 인덱스의 settings API를 통해 변경이 가능하다.

  ```bash
  # -1을 주면 아예 비활성화 하는 것이 가능하다.
  $ curl -XPUT "localhost:9200/my_index/_settings" -H 'Content-type: application/json' -d'{
  "index.refresh_interval":"2h"
  }
  ```



- bulk API

  - 복수의 요청을 한 번에 전송할 때 사용한다.
    - 동작을 따로따로 수행하는 것 보다 속도가 훨씬 빠르다.
    - 하나의 문서를 처리할 때 시스템은 클라이언트와 네트워크 세션을 맺고 끊기를 반복하기 때문에 여러 건의 문서를 처리할 때 단건으로 맺고 끊기를 반복하는 방식으로 처리하면 시스템이 부하를 일으킨다. 따라서 여러 건의 문서를 처리할 때는 bulk API를 통해 작업하는 것이 좋다.
    - 예를 들어 단 건씩 작업했을 때 112s가 걸리는데 bulk를 사용하면 1s가 채 걸리지 않을 정도로 차이가 많이 난다.
  - bulk API 동작
    - index: 문서 색인, 인덱스에 지정한 문서 아이디가 있으면 업데이트.
    - create: 문서 색인, 인덱스에 지정한 문서 아이디가 없을 때에만 색인 가능.
    - update: 문서 변경
    - delete: 문서 삭제
  - 형식
    - delete를 제외하고는 명령문과 데이터문을 한 줄씩 순서대로 입력한다.
    - delete는 내용 입력이 필요 없기 때문에 명령문만 있다.
    - `_bulk`의 명령문과 데이터문은 반드시 한 줄 안에 입력이 되어야 하며 줄바꿈을 허용하지 않는다.
  - 예시

  ```json
  POST _bulk
  {"index":{"_index":"learning", "_id":"1"}} // 생성
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}} // 생성
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}} // 삭제
  {"create":{"_index":"learning", "_id":"3"}} // 생성
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}} // 수정
  {"doc":{"field":"deep learning"}}
  ```

  - 응답

  ```json
  {
    "took" : 1152,
    "errors" : false,
    "items" : [
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 0,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "index" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 1,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "delete" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "2",
          "_version" : 2,
          "result" : "deleted",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 2,
          "_primary_term" : 1,
          "status" : 200
        }
      },
      {
        "create" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "3",
          "_version" : 1,
          "result" : "created",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 3,
          "_primary_term" : 1,
          "status" : 201
        }
      },
      {
        "update" : {
          "_index" : "learning",
          "_type" : "_doc",
          "_id" : "1",
          "_version" : 2,
          "result" : "updated",
          "_shards" : {
            "total" : 2,
            "successful" : 1,
            "failed" : 0
          },
          "_seq_no" : 4,
          "_primary_term" : 1,
          "status" : 200
        }
      }
    ]
  }
  ```

  - 인덱스명이 모두 동일할 경우에는 아래와 같이 하는 것도 가능하다.

  ```json
  POST learning/_bulk
  
  {"index":{"_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_id":"2"}}
  {"create":{"_id":"3"}}
  {"field":"docker"}
  {"update":{"_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```



- json 파일에 실행할 명령을 저장하고 curl 명령으로 실행시킬 수 있다.

  - bulk.json 파일

  ```json
  {"index":{"_index":"learning", "_id":"1"}}
  {"field":"elasticsearch"}
  {"index":{"_index":"learning", "_id":"2"}}
  {"field":"Fastapi"}
  {"delete":{"_index":"learning", "_id":"2"}}
  {"create":{"_index":"learning", "_id":"3"}}
  {"field":"docker"}
  {"update":{"_index":"learning", "_id":"1"}}
  {"doc":{"field":"deep learning"}}
  ```

  - 명령어
    - 파일 이름 앞에는 @를 입력한다.

  ```bash
  $ curl -XPOST "http://localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @bulk.json
  ```



- 그 외에 색인 성능을 확보하는 방법들
  - 문서의 id 없이 색인하기
    - PUT 메서드로 문서의 id를 지정하여 색인하는 것 보다 POST 메서드로 ES가 문서의 id를 임의로 생성하게 하는 것이 더 빠르게 색인 된다.
    - PUT의 경우 사용자가 입력한 id가 이미 존재하는지 검증하는 과정을 거쳐야 하지만 POST의 경우 기존에 동일한 id를 가진 문서가 없다는 전제 조건하에 색인되기 때문에 이미 존재하는 문서인지 확인하는 과정을 생략한다.
  - 레플리카 샤드 갯수를 0으로 설정하기
    - 프라이머리 샤드에 색인 된 후 레플리카에 복제하는 시간을 줄일 수 있다.
    - 클러스터를 운영하는 환경에 복제본이 꼭 필요하지 않거나 하둡과 같은 별도의 저장소에 사용자의 문서를 복제하는 경우라면 고려해 볼 만 하다.





# 검색 성능 최적화

## ES 캐시 활용하기

- ES 캐시의 종류와 특성

  - ES로 요청되는 다양한 검색 쿼리는 동일한 요청에 대해 좀 더 빠른 응답을 주기 위해 해당 쿼리의 결과를 메모리에 저장한다.
  - 결과를 메모리에 저장해 두는 것을 캐싱이라 하며 이 때 사용하는 메모리 영역을 캐시 메모리라 한다.
  - ES에서 제공하는 대표적인 캐시 영역들

  | 캐시 영역           | 설명                                                     |
  | ------------------- | -------------------------------------------------------- |
  | Node query cache    | 쿼리에 의해 각 노드에 캐싱되는 영역이다.                 |
  | Shard request cache | 쿼리에 의해 각 샤드에 캐싱되는 영역이다.                 |
  | Field data cache    | 쿼리에 의해 필드를 대상으로 각 노드에 캐싱되는 영역이다. |



- Node Query Cache

  - filter context에 의해 검색된 문서의 결과가 캐싱되는 영역
    - 사용자가 filter context로 구성된 쿼리로 검색하면 내부적으로 각 문서에 0과 1로 설정할 수 있는 bitset을 설정한다.
    - filter context로 호출한 적이 있는 문서는 bitset을 1로 설정하여 사용자가 호출한적이 있다는 것을 문서에 표시해둔다.
    - ES는 문서별로 bitset을 설정하면서, 사용자의 쿼리 횟수와 bitset이 1인 문서들 사이에 연관 관계를 지속적으로 확인한다.
    - bitset이 1인 문서들 중에 자주 호출되었다고 판단한 문서들을 노드의 메모리에 캐싱한다.
    - 다만 세그먼트 하나에 저장된 문서의 수가 1만개 미만이거나, 검색 쿼리가 인입되고 있는 인덱스가 전체 인덱스 사이즈의 3% 미만일 경우에는 filter context를 사용하더라도 캐싱되지 않는다.
  - 아래 명령어로 Query Cache Memory의 용량을 확인 가능하다.

  ```bash
  $ curl -XGET "http://localhost:9200/_cat/nodes?v&h=name,qcm"
  ```

  - 기본적으로 활성화되어 있으며, 아래와 같이 변경이 가능하다.
    - dynamic setting이 아니기에 인덱스를 close로 바꾸고 설정해줘야 한다.

  ```bash
  # 인덱스를 close 상태로 변경하고
  $ curl -XGET "http://localhost:9200/my_index/_close" -H 'Content-Type: application/json'
  
  # 바꿔준다.
  $ curl -XGET "http://localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'{
  "index.queries.cache.enable":true # false면 비활성화
  }'
  
  # 인덱스를 다시 open 상태로 변경한다.
  $ curl -XGET "http://localhost:9200/my_index/_open" -H 'Content-Type: application/json'
  ```

  - 많은 문서가 캐싱되어 허용된 캐시 메모리 영역이 가득 차면 LRU(Least Recently Used Algorithm) 알고리즘에 의해 캐싱된 문서를 삭제한다.
    - LRU: 캐시 영역에 저장된 내용들 중 가장 오래된 내용을 지우는 알고리즘
    - elasticsearch.yml 파일에서 `indices.queries.cache.size: 10%`와 같이 수정하여 Node Query Cache 영역을 조정할 수 있다.
    - 위와 같이 비율로도 설정할 수 있고, 512mb처럼 절댓값을 주는 것도 가능하다.
    - 수정 후 노드를 재시작해야한다.



- Shard Request Cache

  - Node Query Cache가 노드에 할당된 캐시 영역이라면 Shard Request Cache는 샤드를 대상으로 캐싱되는 영역이다.
    - 특정 필드에 의한 검색이기 때문에 전체 샤드에 캐싱된다.
    - Node Query Cache와 달리 문서의 내용을 캐싱하는 것이 아니라, 집계 쿼리의 집계 결과 혹은 ReqeustBody의 파라미터 중 size를 0으로 설정했을 때의 쿼리 응답 결과에 포함되는 매칭된 문서의 수(total hits)에 대해서만 캐싱한다.
    - Node Query Cache가 검색 엔진에 활용하기 적합한 캐시 영역이라면 Shard Request Cache는 분석 엔진에서 활용하기 적합한 캐시 영역이라고 할 수 있다.
    - 다만 이 영역은 refresh 동작을 수행하면 캐싱된 내용이 사라진다.
    - 즉, 문서 색인이나 업데이트를 한 후 refresh를 통해 샤드의 내용이 변경되면 기존에 캐싱된 결과가 초기화 된다.
    - 따라서 계속해서 색인이 일어나고 있는 인덱스에는 크게 효과가 없다.
  - 아래 명령으로 Shard Request Cache의 상황을 볼 수 있다.

  ```bash
  $ curl -XGET "http://localhost:9200/_cat/nodes?v&h=name,rcm"
  ```

  - Shard Request Cache도 ES 클러스터에 기본적으로 활성화되어 있다.
    - 다만 dynamic setting이어서 인덱스를 대상으로 온라인중에 설정이 가능하다.

  ```bash
  $ curl -XGET "http://localhost:9200/my_index/_settings" -H 'Content-Type: application/json' -d'{
  "index.requests.cache.enable":true # false면 비활성화
  }'
  ```

  - 검색시에도 활성/비활성화가 가능하다.
    - size를 0으로 줬으므로 본래 Shard Request Cache가 생성되어야 하지만 `request_cache=false`로 인해 생성되지 않는다.

  ```bash
  $ curl -XGET "http://localhost:9200/my_index/_search?request_cache=false" -H 'Content-Type: application/json' -d'{
  "size":0,	# size가 0일 때 Shard Request Cache가 생성된다.
  "aggs":{
  	"cityaggs":{
  		"terms":{"field":"city.keyword"}
  	}
  }
  }'
  ```

  - 가이드라인
    - Shard Request Cache 설정을 기본으로 활성화한 다음, 색인이 종료된 과거 인덱스는 request_cache를 true로 집계하고 색인이 한참 진행 중인 인덱스는 false로 집계하는 방식으로 사용한다 
    - 이렇게 하면 과거 인덱스에 대해서는 캐싱 데이터를 리턴해서 빠르게 결과를 전달 받고, 색인이 빈번하게 진행 중이어서 캐싱이 어려운 인덱스는 불필요하게 캐싱하는 낭비를 막을 수 있다.
    - 또한 과거 인덱스에 색인이 들어오면 캐싱된 데이터가 초기화되기 때문에 인덱스를 쓰지 못하도록 read only 처리하는 것도 캐싱 데이터를 유지시킬 수 있는 방법이다.

  - 각 노드의  elasticsearch.yml 파일에서 다음과 같이 Shard Request Cache 영역을 조정 가능하다.
    - `indices.requests.cache.size: 10%`
    - 이 경우 노드를 재시작해야 한다.



- Field Data Cache

  - 인덱스를 구성하는 필드에 대한 캐싱
    - 주로 검색 결과를 정렬하거나 집계 쿼리를 수행할 때 지정한 필드만을 대상으로 해당 필드의 모든 데이터를 메모리에 저장하는 캐싱 영역이다.
    - 예를 들어 A 노드에 a, b 샤드, B 노드에 c 샤드가 있다고 가정
    - a샤드에는 age:20이라는 데이터가, b 샤드에는 age:21이라는 데이터가, B 노드에는 age:22라는 데이터가 색인되어 있다고 할 때
    - age 필드를 대상으로 정렬하는 검색을 진행하면
    - A 노드에는 age 필드의 값이 20,21 인 데이터가, B 노드애는 age 필드의 값이 22인 데이터가 캐싱된다.
  - Field Data Cache 영역은 text 필드 데이터 타입에 대해서는 캐싱을 허용하지 않는다.
    - 다른 필드 데이터 타입에 비해 캐시 메모리에 큰 데이터가 저장되기 때문에 메모리를 과도하게 사용하게 되기 때문이다.

  - Field Data Cache 사용 현황 확인

  ```bash
  $ curl -XGET "http://localhost:9200/_cat/nodes?v&h=name,fm"
  ```

  - 마찬가지로 elasticsearch.yml 파일에서 다음과 같이 Field Data Cache 영역을 조정 가능하다.
    - `indices.fielddata.cache.size: 10%`
    - 역시 노드를 재시작해야 한다.



- 캐시 영역 클리어

  - 전체 클리어

  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear"
  ```

  - Node Query Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear?query=true" -H 'Content-type:application/json'
  ```

  - Shard Request Cache 클리어

  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear?request=true" -H 'Content-type:application/json'
  ```
  
  - Field Data Cache 클리어
  
  ```bash
  $ curl -XPOST "localhost:9200/<인덱스명>/_cache/clear?fielddata=true" -H 'Content-type:application/json'
  ```




## 검색 쿼리 튜닝하기

- copy_to

  - 쿼리를 어떻게 만드느냐가 검색 성능에 큰 영향을 미친다.
  - 검색 성능을 떨어뜨리는 요인 중 하나는 너무 많은 필드를 사용하는 것이다.
    - 처음에 인덱스의 매핑 정보를 생성할 때 우선적으로 불필요한 필드들을 제외해야 하지만 매핑 구조에 따라 필드가 많아지는 경우도 있다.
    - 이런 경우에는 별수 없이 많은 필드에 걸쳐 검색을 해야 하는 경우도 생긴다.
  - 여러 개의 필드를 대상으로 검색하는 예시
    - `first_name`과 `last_name`이라는 2개의 필드를 대상으로 검색하기
    - `match` 쿼리를 두 번 사용해서 검색해야 한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_search?pretty" -H 'Content-type:application/json' -d'
  {
  	"query":{
  		"bool":{
  			"must":[
  				{"match":{"first_name":"John"}},
  				{"match":{"last_name":"Doe"}}
  			]
  		}
  	}
  }
  '
  ```

  - 이렇게 많은 필드를 모아서 검색할 수 있는 기능이 copy_to 기능이다.
    - 가능하면 매핑 스키마 계획을 세울 때 최소한의 필드를 사용할 수 있도록 한다.
    - 그러나 불가피하게 많은 필드를 대상으로 검색해야 한다면 copy_to를 최대한 활용한다.



- copy_to를 활용하여 검색하기

  - mapping할 때 `copy_to`를 추가한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_mappings?pretty" -H 'Content-type:application/json' -d'
  {
  	"_doc":{
  		"properties":{
  			"first_name":{
  				"type":"text",
  				"copy_to":"full_name"	# copy_to 추가
  			},
  			"last_name":{
  				"type":"text",
  				"copy_to":"full_name"
  			},
  			"full_name":{		# copy_to를 위한 필드 생성
  				"type":"text"
  			}
  		}
  	}
  }
  ```

  - 색인할 때 copy_to를 위해 생성한 필드(`full_name`) 필드에는 따로 데이터를 넣어줄 필요가 없다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_mappings?pretty" -H 'Content-type:application/json' -d'
  {
  	"first_name":"John",
  	"last_name":"Doe"
  }
  ```

  - 검색
    - copy_to를 위해 생성한 필드(`full_name`)를 대상으로 검색한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index/_search?pretty" -H 'Content-type:application/json' -d'
  {
  	"query":{
  		"match":{
  			"full_name":"John Doe"
  		}
  	}
  }
  '
  ```



- 불필요하게 사용되는 쿼리 제거하기
  - Query Context와 Filter Context 구분하기
    - match 쿼리는 Query Context에 속하는 쿼리다.
    - Query Context는 analyzer를 통해 검색어를 분석하는 과정이 포함되기 때문에 분석을 위한 추가 시간이 필요하다.
    - 반면에 Filter Context에 속하는  term 쿼리는 검색어를 분석하는 과정을 거치지 않는다.
    - 따라서 match 쿼리보다 term 쿼리가 성능이 더 좋다.
  - keyword 필드 데이터 타입으로 매핑된 문자열 필드는 term 쿼리를 사용하는 것이 성능상 유리하다.
    - keyword 필드는 분석하지 않는 필드이다.
    - 따라서 검색할 때도 검색어를 분석하지 않는 term 쿼리가 더 적합하다.
  - ES에서는 수치 계산에 사용되지 않는 숫자형 데이터는 keyword 필드 데이터 타입으로 매핑하도록 권고한다.
    - 이 경우에도 keyword 타입으로 정의하고 term 쿼리를 사용하는 것이 적합하다.
    - 단, keyword 타입으로 저장된 숫자들은 계산이 되지 않는다.



## 그 외의 방법들

- 적절한 샤드 배치

  > 샤드 배치를 적절히 하지 못할 경우 아래와 같은 문제들이 발생할 수 있다.

  - 데이터 노드 간 디스크 사용량 불균형
    - 노드는 3대이고 프라이머리 샤드는 4개로 설정했다고 가정
    - 한 노드는 2개의 샤드를 가져갈 수 밖에 없다.
    - 시간이 흐를수록 2개의 샤드를 가져간 노드의 디스크 사용량이 높아지게 된다.
    - 따라서 노드의 개수에 맞게 샤드 개수를 설정해야 한다.
  - 색인/검색 성능 부족
    - 노드는 3대이고 프라이머리 샤드는 2개로 설정했다고 가정
    - 하나의 노드는 샤드를 할당받지 못한다.
    - 샤드를 할당받지 못한 노드는 클러스터에 속해 있어도 색인과 검색에 참여할 수 없다.
  - 데이터 노드 증설 후에도 검색 성능이 나아지지 않음
    - 최초에 노드의 개수와 샤드의 개수를 동일하게 클러스터를 구성했다고 가정
    - 이 상황에서 노드의 개수를 증가시킨다 하더라도 해당 노드에 할당할 샤드가 없으므로 노드 추가로 인한 성능 개선을 기대하기 어렵다.
    - 따라서 처음에 클러스터를 구성할 때 어느 정도의 증설을 미리 계획하여 최초 구성한 노드의 개수와 증설된 이후 노드의 개수의 최소공배수로 샤드의 개수를 설정하면 위와 같은 문제를 모두 예방할 수 있다.
  - 클러스터 전체의 샤드 개수가 지나치게 많음
    - 이 경우 마스터 노드를 고려해야 한다.
    - 샤드의 개수가 많아질수록 마스터 노드가 관리해야 하는 정보도 많아지게 된다.
    - 따라서 데이터 노드의 사용량에는 큰 문제가 없는데 클러스터의 성능이 제대로 나오지 않는 문제가 발생할 수 있다.
    - 하나의 노드에서 조회할 수 있는 샤드의 개수를 제한하는 것도 방법이다.

  ```bash
  $ curl -XPUT "localhost:9200/cluster/settings?pretty" -H 'Content-type:application/json' -d'
  {
  	"transient":{
  		"cluster.max_shards_per_node":2000	# 노드당 검색 요청에 응답할 수 있는 최대 샤드 개수를 2000개로 설정
  	}
  }
  ```



- forcemerge API

  - 세그먼트
    - 인덱스는 샤드로 나뉘고, 샤드는 다시 세그먼트로 나눌 수 있다.
    - 사용자가 색인한 문서는 최종적으로 가장 작은 단위인 세그먼트에 저장된다.
    - 또한 세그먼트는 작은 단위로 시작했다가 특정 시점이 되면 다수의 세그먼트들을 하나의 세그먼트로 합친다.
    - 세그먼트가 잘 병합되어 있으면 검색 성능도 올라간다.

  - forcemerge API와 검색 성능
    - 샤드에 여러 개의 세그먼트가 있다면 해당 세그먼트들이 모두 검색 요청에 응답을 주어야 한다.
    - 쿼리마다 많은 세그먼트에 접근해야 한다면 이는 곧 I/O를 발생시켜 성능 저하로 이어질 것이다.
    - 하지만 세그먼트가 하나로 합쳐져 있다면, 사용자의 검색 요청에 응답해야 하는 세그먼트가 하나이기 떄문에 성능이 더 좋아질 수 있다.
    - forcemerge를 통해 세그먼트를 병합하면 검색 성능이 더 좋아질 수 있다.
  - 가이드라인
    - 무조건 세그먼트가 적다고 좋은 것은 아니다.
    - 샤드 하나의 크기가 100GB 정도인데 세그먼트가 하나라면 작은 크기의 문서를 찾을 때에도 100GB 전체를 대상으로 검색해야 해서 병합 전보다 성능이 떨어질 수 있다.
    - 세그먼트를  병합했는데 이후에 색인이 발생하면 다시 세그먼트가 늘어나게 되어 병합 작업의 효과를 보기 어렵다.
    - 색인이 모두 끝난 인덱슨는 병합 작업을 진행하고 난 이후 readonly 모드로 설정하여 더 이상 세그먼트가 생성되지 못하게 하는 것이 좋다.



- ES 권고사항

  - 문서를 모델링할 때 가급적이면 간결하게 구성하도록 권고한다.
    - Parent/Child 구조의 join 구성이나, nested 타입 같이 문서를 처리할 때 문서 간의 연결 관계 처리를 필요로 하는 구성은 권장하지 않는다.

  - painless script를 사용하여 하나의 문서를 처리할 때마다 부가적으로 리소스를 사용하지 않도록 하는 것도 권고사항이다.
    - painless script: 쿼리만으로 원하는 데이터를 조회할 수 없을 때 사용하는 ES 전용 스크립트 언어

  - 레플리카 샤드를 가능한 한 충분히 두는 것이 좋다.
    - 노드 1에 프라이머리 샤드 0과 레플리카샤드 1이 있고, 노드 2에 프라이머리샤드 1과 레플리카샤드 0이 있다고 가정
    - 두 개의 검색 요청이 들어왔고 두 요청에 대한 응답을 줄 데이터가 모두 샤드 0번에 있을 경우
    - 한 요청을 노드1로, 다른 요청은 노드 2로 들어왔을 때, 두 노드 모두 0번 샤드를 지니고 있으므로 동시에 들어온 검색 요청에  서로 다른 노드가 응답해 줄 수 있다.
    - 다만 레플리카 샤드는 인덱싱 성능과 볼륨 사용량의 낭비가 발생하니 클러스터 용량을 고려해서 추가하는 것이 좋다.











