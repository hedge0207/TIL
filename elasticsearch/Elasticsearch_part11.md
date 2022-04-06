

# Analyzer와 inverted index

> 아래의 내용은 모두 text type에 대한 것이다. keyword type은 analyze 과정을 거치지 않는다.

- inverted index(역색인)

  - "I am a boy", "You are a girl" 이라는 두 문자열이 있다고 가정한다.
    - 위 두 개의 문자열을 공백을 기준으로 나누면 각각의 문자열은 4개의 단어로 나뉜다.
    - I, am, a, boy
    - you, are, a girl
  - 토큰
    - 위와 같이 나뉜 단어들을 **토큰**이라 부른다. 
    - 토큰을 만들어 내는 과정을 **토크나이징**이라고 한다.
  - 특정한 기준에 의해 나뉜 토큰들은 아래와 같은 형태로 저장되는데 이것을 역색인이라 부른다.

  | Tokens | Documents |
  | ------ | --------- |
  | I      | 1         |
  | am     | 1         |
  | a      | 1, 2      |
  | boy    | 1         |
  | girl   | 2         |
  | you    | 2         |
  | are    | 2         |

  - 위와 같은 역색인이 생성된 상태에서 사용자가 "a boy"라는 문자열이 포함된 문서를 찾고 싶다고 가정한다.
    - 검색어로 a boy라는 문자열을 입력하면 이 문자열은 공백을 기준으로 a, boy라는 두 개의 토큰으로 나뉜다.
    - 이렇게 나뉜 토큰을 바탕으로 역색인을 검색한다.
    - 두 단어가 모두 포함되어 있는 문서 1번이 검색 결과로 반환된다.
  - 대소문자 구분
    - 검색 결과를 얻기 위해서는 토큰이 대소문자까지 정확하게 일치해야 한다.
    - 역색인에 대문자 I만 존재할 뿐 소문자 i는 존재하지 않는다.
    - 따라서 소문자 i로 검색하면 아무런 검색 결과를 얻지 못한다.



- ES는 어떻게 토크나이징을 하는가

  - ES는 `_analyze`라는 API를 제공한다.
    - analyzer에는 토크나이징에 사용할 analyzer를 입력한다.
    - text에는 토크나이징 할 문자열을 입력한다.

  ```bash
  $ curl -XPOST "localhost:9200/_analyze?pretty" -H 'Content-type:application/json' -d '{
  "analyzer":"standard",
  "text":"I am a boy"
  }'
  ```

  - 응답
    - 토크나이징의 결과로 토큰의 배열을 반환한다.
    - 아래 토큰을 보면 대문자 I가 아닌 소문자 i로 토크나이징 된 것을 볼 수 있는데, standard analyzer의 동작 중에 모든 문자를 소문자화하는 과정이 포함되어 있기 때문이다.

  ```json
  {
    "tokens" : [
      {
        "token" : "i",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "<ALPHANUM>",
        "position" : 0
      },
      {
        "token" : "am",
        "start_offset" : 2,
        "end_offset" : 4,
        "type" : "<ALPHANUM>",
        "position" : 1
      },
      {
        "token" : "a",
        "start_offset" : 5,
        "end_offset" : 6,
        "type" : "<ALPHANUM>",
        "position" : 2
      },
      {
        "token" : "boy",
        "start_offset" : 7,
        "end_offset" : 10,
        "type" : "<ALPHANUM>",
        "position" : 3
      }
    ]
  }
  ```



- analyzer 
  - analyzer는 역색인을 만들어주는 것이다.
    - analyzer는 운영 중에 동적으로 변경할 수 없다. 
    - 따라서 기존 인덱스에 설정한 analyzer를 바꾸고 싶을 때는 인덱스를 새로 만들어서 재색인(reindex)해야 한다.
  - ES의 analyzer는 다음과 같이 구성된다.
    - character filter
    - tokenizer
    - token filter
  - character filter
    - analyzer를 통해 들어온 문자열들은 character filter가 1차로 변형한다.
    - 예를 들어 <, >, ! 등과 같은 의미 없는 특수 문자들을 제거한다거나 HTML 태그들을 제거하는 등 문자열을 구성하고 있는 문자들을 특정한 기준으로 변경한다.
  - tokenizer
    - tokenizer는 일정한 기준(공백이나 쉼표)에 의해 문자열은 n개의 토큰으로 나눈다.
    - analyzer를 구성할 때는 tokenizer를 필수로 명시해야 하며, 하나의 tokenizer만 설정할 수 있다.
    - 반면 character filter와 token filter는 필요하지 않을 경우 기술하지 않거나, 여러 개의 character filter와 token filter를 기술할 수 있다.
  - token filter
    - tokenizer에 의해 분리된 각각의 텀들을 지정한 규칙에 따라 처리해주는 필터들이다.
    - `filter` 항목에 배열로 나열해서 지정하며, 나열된 순서대로 처리되기에 순서를 잘 고려해서 입력해야한다.
    - 토큰을 전부 소문자로 바꾸는 lowercase token filter가 대표적인 token filter이다.



- standard analyzer

  - 아무 설정을 하지 않을 경우 디폴터로 적용되는 애널라이저
  - filter
    - character filter가 정의되어 있지 않다.
    - standard tokenizer가 정의되어 있다.
    - lowercase token filter가 정의되어 있다.
    - stopwords로 지정한 단어가 토큰들 중에 존재 한다면 해당 토큰을 없애는 stop token filter가 존재하지만 기본값으로 비활성화 되어 있다.
  - standard tokenizer 요청
    - `analyzer`가 아닌 `tokenizer`를 입력한다.
    - 아직 token filter를 거치지 않았기에 I가 대문자이다.

  ```json
  $ curl -XPOST "localhost:9200/_analyze?pretty" -H 'Content-type:application/json' -d '{
  "tokenizer":"standard",
  "text":"I am a boy"
  }'
  
  
  {
    "tokens" : [
      {
        "token" : "I",
        "start_offset" : 0,
        "end_offset" : 1,
        "type" : "<ALPHANUM>",
        "position" : 0
      },
      {
        "token" : "am",
        "start_offset" : 2,
        "end_offset" : 4,
        "type" : "<ALPHANUM>",
        "position" : 1
      },
      {
        "token" : "a",
        "start_offset" : 5,
        "end_offset" : 6,
        "type" : "<ALPHANUM>",
        "position" : 2
      },
      {
        "token" : "boy",
        "start_offset" : 7,
        "end_offset" : 10,
        "type" : "<ALPHANUM>",
        "position" : 3
      }
    ]
  }
  ```



- custom analyzer

  > https://esbook.kimjmin.net/06-text-analysis/6.3-analyzer-1/6.4-custom-analyzer
  >
  > https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html

  - 내장 애널라이저로 충분하지 않을 경우 직접 애널라이저를 만들 수 있다.
  - 애널라이저 정의 하기
    - type: `custom`을 입력하거나 아예  type 자체를 입력하지 않는다.
    - tokenizer: 애널라이저에 사용할 토크나이저를 입력한다(필수).
    - char_filter: 사용할 character filter들을 입력한다.
    - filter: 사용할 token filter들을 입력한다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index" -H 'Content-type:application/json' -d '{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {	# 커스텀 애널라이저의 이름
          "type": "custom",
          "tokenizer": "standard",
          "char_filter": [
            "html_strip"
          ],
          "filter": [
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  }
  }'
  ```

  - 위에서 적용한 tokenizer, char_filter, filter도 custom해서 적용하는 것이 가능하다.

  ```bash
  $ curl -XPUT "localhost:9200/my_index" -H 'Content-type:application/json' -d '
  {
    "settings": {
      "analysis": {
        "analyzer": {
          "my_custom_analyzer": { 
            "char_filter": [
              "emoticons"	# 아래에서 custom한 emoticons라는 char_filter를 적용
            ],
            "tokenizer": "punctuation",	# 아래에서 custom한 punctuation이라는 tokenizer 적용
            "filter": [
              "lowercase",
              "english_stop"	# 아래에서 custom한 english_stop이라는 filter 적용
            ]
          }
        },
        "tokenizer": {
          "punctuation": { 
            "type": "pattern",
            "pattern": "[ .,!?]"
          }
        },
        "char_filter": {
          "emoticons": { 
            "type": "mapping",
            "mappings": [
              ":) => _happy_",
              ":( => _sad_"
            ]
          }
        },
        "filter": {
          "english_stop": { 
            "type": "stop",
            "stopwords": "_english_"
          }
        }
      }
    }
  }
  ```



- analyzer와 검색의 관계

  - analyze의 중요성
    - analyzer를 통해 생성한 토큰들이 역색인에 저장되고, 검색할 때는 이 역색인에 저장된 값을 바탕으로 문서를 찾는다.
    - 따라서 검색 니즈를 잘 파악해서 적합한 analyzer를 설정해야 한다.
  - 테스트 인덱스 생성

  ```bash
  $ curl -XPUT "localhost:9200/books?pretty" -H 'Content-type:application/json' -d '{
  	"mappings":{
  		"properties":{
  			"title":{"type":"text"},
  			"content":{"type":"keyword"}
  		}
  	}
  }'
  ```

  - 테스트 문서 색인

  ```bash
  $ curl -XPUT "localhost:9200/books/_doc/1?pretty" -H 'Content-type:application/json' -d '{
  "title":"Elasticsearch Training Book",
  "content":"Elasticsearch is open source search engine"
  }'
  ```

  - title로 검색하기
    - 정상적으로 검색이 된다.

  ```json
  $ curl "localhost:9200/books/_search?pretty&q=title:Elasticsearch"
  
  {
    "took" : 743,
    "timed_out" : false,
    "_shards" : {
      "total" : 1,
      "successful" : 1,
      "skipped" : 0,
      "failed" : 0
    },
    "hits" : {
      "total" : {
        "value" : 1,
        "relation" : "eq"
      },
      "max_score" : 0.6931471,
      "hits" : [
        {
          "_index" : "books",
          "_type" : "_doc",
          "_id" : "1",
          "_score" : 0.6931471,
          "_source" : {
            "title" : "Elasticsearch Training Book",
            "content" : "Elasticsearch is open source search engine"
          }
        }
      ]
    }
  }
  ```

  - content로 검색하기

  ```bash
  $ curl "localhost:9200/books/_search?pretty&q=content:Elasticsearch"
  
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
        "value" : 0,
        "relation" : "eq"
      },
      "max_score" : null,
      "hits" : [ ]
    }
  }
  ```

  - content 필드는 검색이 정상적으로 이루어지지 않았다.
    - title 필드는 text, content 필드는 keyword 타입으로 정의했다.
    - text 타입의 기본 analyzer는 standard analyzer이고, keyword 타입의 기본 analyzer는 keyword analyzer이다.
    - keyword analyzer는 standard analyzer와는 달리 analyze를 하지 않는다.
    - 즉 역색인에는 "Elasticsearch is open source search engine"라는 토큰만 존재한다.



- 색인된 문서의 역 인덱스 내용 확인하기

  - `_termvectors ` API를 사용한다.

  - `<인덱스명>/_termvectors/<doc_id>?fields=<확인할 필드>`

  ```bash
  $ curl "localhost:9200/test-index/_termvectors/1?fields=title"
  ```



## token filter

- stopword(불용어)

  - 검색에 불필요한 조사나 전치사 등을 처리하기 위한 token filter
    - `stopwords` 항목에 적용된 단어들은 tokenizing 된 텀에서 제거된다.
    - 예를 들어 "아버지가 방에" 라는 문장을 `nori_tokenizer`로 token화하면 `아버지 / 가 / 방 / 에`로 분리되는데, 만일 "가"와 "에"를 `stopwords`에 추가했다면 `아버지 / 방`만 추출된다.
    - settings에 추가할 수도 있고, 파일로 관리할 수도 있다.
  - settings에 추가하기

  ```json
  {
    "settings": {
      "analysis": {
        "filter": {
          "test_stop_filter": {
            "type": "stop",
            "stopwords": [
              "가",
              "에"
            ]
          }
        }
      }
    }
  }
  ```

  - 일일이 지정하지 않고 언어별로 지정하기

    > https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stop-tokenfilter.html

    - 위 페이지에서 지원하는 언어팩을 확인 가능하다(아직까지 한국어는 없다).

  ```json
  {
    "settings": {
      "analysis": {
        "filter": {
          "test_stop_filter": {
            "type": "stop",
            "stopwords": "_french_"
          }
        }
      }
    }
  }
  ```

  - 파일로 관리하기
    - 각각의 stopword는 파일 내에서 줄바꿈으로 구분된다.
    - 사전 파일의 경로는 config 디렉터리를 기준으로 상대 경로를 지정해야 한다.
    - 텍스트 인코딩은 반드시 UTF-8이어야한다.

  ```json
  {
    "settings": {
      "analysis": {
        "filter": {
          "test_stop_filter": {
            "type": "stop",
            "stopwords_path": "user_dict/stopword_dict.txt"
          }
        }
      }
    }
  }
  ```

  - 파일로 관리할 경우 주의사항
    - 파일로 관리할 때, 파일의 내용이 변경되었다면 해당 파일을 사용하는 인덱스를 close/open 해주어야 적용된다.
    - 또한, 파일이 변경되면, 그 이후로 색인되는 문서들에만 적용되고 이미 색인된 문서들에는 적용되지 않는다.
    - 따라서 기존에 색엔된 문서들에도 적용하려면 재색인 해야한다.



- N-gram

  - tokenizing 결과를 정해진 길이만큼 잘라서 다시 token을 생성한다.

  - 옵션

    - `max_ngram`: 각 토큰의 최대 길이를 지정한다(기본값은 2).
    - `min_ngram`: 각 토큰의 최소 길이를 지정한다(기본값은 1).

    - `preserve_original`: ngram filter가 적용되기 전의 토큰을 보존한다.

  - 예시

  ```json
  // ngram-example
  {
    "settings": {
      "index": {
        "max_ngram_diff": 2
      },
      "analysis": {
        "analyzer": {
          "default": {
            "tokenizer": "whitespace",
            "filter": [ "3_5_grams" ]
          }
        },
        "filter": {
          "3_5_grams": {
            "type": "ngram",
            "min_gram": 3,
            "max_gram": 5
          }
        }
      }
    }
  }
  ```



- Edge n-gram

  - 각 토큰의 시작부분만 정해진 길이만큼 잘라서 토큰을 생성한다.

  - 옵션

    - `max_ngram`: 각 토큰의 최대 길이를 지정한다(기본값은 2).
    - `min_ngram`: 각 토큰의 최소 길이를 지정한다(기본값은 1).

    - `preserve_original`: ngram filter가 적용되기 전의 토큰을 보존한다.

  - 예시

  ```json
  // edge-ngram-example
  {
    "settings": {
      "analysis": {
        "analyzer": {
          "default": {
            "tokenizer": "whitespace",
            "filter": [ "3_5_edgegrams" ]
          }
        },
        "filter": {
          "3_5_edgegrams": {
            "type": "edge_ngram",
            "min_gram": 3,
            "max_gram": 5
          }
        }
      }
    }
  }
  ```



- nori

  > https://lucene.apache.org/core/9_1_0/analysis/nori/org/apache/lucene/analysis/ko/POS.Tag.html