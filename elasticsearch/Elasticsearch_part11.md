

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





# auto completion

- java-cafe plugin

  > https://github.com/javacafe-project/elasticsearch-plugin

  - java-cafe plugin은 한글 text를 초성, 자모 단위로 분해해준다.
  - plugin 다운 받기
    - 사용중인 elasticsearch 버전에 맞는 플러그인을 위 사이트에서 찾아서 설치한다.
    - 지원하는현재 사용중인 elasticsearch 버전을 지원하는 plugin이 없을 경우 일단 plugin 내부의 `plugin-descriptor.properties` 파일에서 `elasticsearch.version` 옵션을 현재 사용중인 es 버전으로 변경한다.
    - plugin 자체를 수정하는 것이 아니라 es 버전만 변경해주는 것이므로 불완전할 수 있다.

  - 설치

  ```bash
  $ bin/elasticsearch-plugin install file://<plugin 파일 경로>
  ```



- 자동완성 구현하기

  - 주의사항
    - 아래 방식은 성능상으로 불완전한 방식이다.
    - `match_phrase_prefix` 쿼리의 옵션으로 `max_expansions`을 10000으로 줬는데 이는 기본값인 50보다 훨씬 큰 값으로, 성능상에 문제가 있을 수 있다.
    - 또한 ngram filter역시 min, max를 각각 2, 10으로 설정하여 토큰이 지나치게 많이 생성될 수 있다.
  - 자동완성을 위한 인덱스 생성
    - ngram filter의 min값과 max값은 기본적으로 2 이상으로 차이가 날 수 없으므로, 2 이상 차이가 나도록 설정하려면 `settings.index.max_ngram_diff` 옵션을 변경해야 한다.

  ```json
  {
      "settings": {
          "index": {
              "max_ngram_diff":8
          },
          "analysis": {
              "filter": {
                  "2_5_gram":{
                      "type":"ngram",
                      "min_gram": 2,
                      "max_gram": 10
                  }
              },
              "analyzer": {
                  "jamo-analyzer": {
                      "type": "custom",
                      "tokenizer": "standard",
                      "filter": [
                          "lowercase",
                          "2_5_gram",
                          "javacafe_jamo"
                      ]
                  },
                  "chosung-analyzer": {
                      "type": "custom",
                      "tokenizer": "standard",
                      "filter": [
                          "lowercase",
                          "2_10_edgegram",
                          "javacafe_chosung"
                      ]
                  },
                  "search-analyzer": {
                      "type": "custom",
                      "tokenizer": "standard",
                      "filter": [
                          "lowercase",
                          "javacafe_jamo"
                      ]
                  }
              }
          }
          
      },
      "mappings": {
          "properties": {
              "title": {
                  "type": "text",
                  "analyzer": "jamo-analyzer",
                  "search_analyzer": "search-analyzer",
                  "fields": {
                      "chosung": {
                          "type": "text",
                          "analyzer": "chosung-analyzer",
                          "search_analyzer": "search-analyzer"
                      },
                      "keyword": {
                          "type": "keyword"
                      }
                  }
              }
          }
      }
  }
  ```

  - 자동완성을 위한 쿼리
    - `slop`과 `max_expansions` 옵션은 데이터에 따라 다르게 주면 된다.
  
  
  ```json
  {
      "query": {
          "bool":{
              "should": [
                  {
                      "match_phrase_prefix": {
                          "title": {
                              "query":<search_input>,
                              "slop":6,
                              "max_expansions":10000
                          }
                      }
                  },
                  {
                      "match_phrase_prefix": {
                          "title.chosung": {
                              "query":<search_input>,
                              "slop":6,
                              "max_expansions":10000
                          }
                      }
                  }
              ]
          }
      }
  }
  ```



# completion suggester

- 이름은 completion suggester지만 자동완성보다는 연관 검색에 적합할 듯 하다.





# Elasticsearch 8

## Upgrade

- 7.17 미만 version에서 8 version으로 바로 업그레이드는 불가능
  - 7.17 미만일 경우 7.17로 업그레이드 후 8로 업그레이드 해야 한다.
  - Upgrade Assistant를 통해 issue를 해결하고 기존에 색인된 index들을 재색인하는 과정을 거친다.
  - Kibana -> Stack Management -> Upgrade Assistant



- `node.<role>` setting이 deprecate 됐다.
  - 대신 `node.roles` 옵션을 사용해야한다.



## Kibana 연동하기

- enrollment token 기반 연동으로 변경되었다.

  - enrollment token
    - enrollment token은 kibana를 elasticsearch에 **등록**하거나 새로운 node를 cluster에 **등록**할 때 사용한다.
    - enrollment token에는 cluster에 대한 정보가 담겨 있다.

  - 기존에는 `kibana.yml`파일에 kibana와 연결할 elasticsearch의 host를 아래와 같이 적어주었다.

  ```yaml
  elasticsearch.hosts:["http:localhost:9200"]
  ```

  - 그러나 enrollment token 기반 연동에서는 `elasticsearch.hosts`를 설정할 경우 error가 발생한다.
    - elasticsearch가 생성한 enrollment token을 kibana에 입력하면 알아서 elasticsearch url을 찾아 연결된다.

  ```yaml
  version: '3.2'
  
  services:
    single-node:
      image: docker.elastic.co/elasticsearch/elasticsearch:8.1.3
      container_name: single-node
      environment:
        - node.name=single-node
        - cluster.name=my-cluster
        - bootstrap.memory_lock=true
        - discovery.type=single-node
        - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      ulimits:
        memlock:
          soft: -1
          hard: -1
      restart: always
      ports:
        - 9210:9200
      networks:
        - elasticsearch_elastic
    
    kibana:
      image: docker.elastic.co/kibana/kibana:8.1.3
      container_name: single-kibana
      ports:
        - "5602:5601"
      # elasticsearch.hosts를 설정하지 않는다.
      # environment:
      #   ELASTICSEARCH_HOSTS: https://192.168.112.10:9200
      networks:
        - elasticsearch_elastic
      depends_on:
        - single-node
  
  
  networks:
    elasticsearch_elastic:
      external:
        name: elasticsearch_elastic
  ```

  - enrollment token 생성

    - docker가 아니라면 elasticsearch를 최초로 실행할 때 enrollment token과 username, password가 터미널 창에 출력되지만, docker의 경우 자동으로 생성되지 않으므로 수동으로 초기화해줘야한다.
    - elasticsearch의 home 디렉토리로 이동하여 아래 명령어를 입력한다.
    - 터미널 창에 생성된 enrollment token의 정보가 출력되고, 이를 복사하여 입력하면 된다.
    - enrollment token의 유효기간은 30m이다.

    ```bash
    $ bin/elasticsearch-create-enrollment-token -s kibana
    ```

  - enrollment token 입력하기

    - kibana를 실행하면 터미널 창에 `Go to http://0.0.0.0:5601/?code=<code> to get started.`와 같은 메시지가 뜬다.
    - 위 링크로 접속하면 enrollment token을 입력하는 창이 뜨는데 여기에 enrollment token을 입력하면 된다.
    - 예시로 든 docker-compose.yml 파일의 경우 kibana의 port를 5602와  bind 했으므로 `<서버의 host>:5602/?code=<code>`로 접속해야한다

  - username과 password 입력하기

    - elasticsearch는 실행과 동시에 `elastic`이라는 user를 자동으로 생성한다.
    - enrollment token과 마찬가지로 elasticsearch를 최초로 실행할 때 username과 password를 출력하지만, docker의 경우 password를 자동으로 생성하지 않으므로 password를 초기화해야한다.

  ```bash
  $ bin/elasticsearch-reset-password -u elastic
  ```

  - kibana에 `elastic`이라는 username과, 위 명령어를 통해 초기화한 password를 입력하면 elasticsearch와의 연동이 완료된다.



# Security

- 보안 비활성화하기

  - `~/config/elastcsearch.yml`파일에서 아래 두 옵션을  false로 준다.

  ```yaml
  # disable security features
  xpack.security.enabled: false
  
  xpack.security.enrollment.enabled: false
  ```



- Elasticsearch가 처음 실행 될 때 아래와 같은 보안과 관련된 기능들이 실행된다.
  - trasnport(node들 사이의 통신)와 HTTP 계층(client와의 통신)의 TLS를 위한 certificate와 key가 생성된다.
    - `http_ca.crt`: 
  - TLS 설정이 `elasticsearch.yml`파일에 작성된다.
  - `elastic`이라는 user를 위한 password가 생성된다.
  - kibana와 연결하기 위한 enrollment token이 생성된다.



- Elasticsearch는 크게 아래 3가지 방식으로 보안 기능을 제공한다.
  - 인가되지 않은 접근을 막는다.
    - role-base로 접근을 통제한다.
    - 사용자와 password를 통해 인증을 진행한다.
  - SSL/TLS encryption을 통해 데이터를 온전히 보존한다.
  - 누가 cluster에 어떤 동작을 실행했는지를 기록한다.



- Elasticsearch security의 원칙
  - 절대 security 기능을 비활성화한 상태로 cluster를 운영해선 안된다.
  - 지정된 non-root user로 elasticsearch를 운영해라.
    - 절대 root user로 운영해선 안된다.
  - 절대 elasticsearch를 public internet traffic에 노출시키지 마라.
  - role-base로 접근을 통제해라.



- Elasticsearch가 실행되면 아래와 같은 보안 작업들이 실행된다.
  - Transport and HTTP layers에 대해 TLS용 certificate와 key가 생성된다.
  - elasticsearh.yml 파일에 TLS 관련 설정이 작성된다.
  - elastic이라는 기본 사용자에 대한 비밀번호가 생성된다.
  - kibana에서 사용되는 enrollment token이 생성된다.
    - enrollment token의 유효기간은 30분이다.
    - node에서도 사용되지만, node를 위한 enrollment token은 자동으로 생성되지 않는다.
    - cluster에 합류시킬 node를 준비하는 데 상당한 시간이 걸릴 수 있고, 그러는 동안 enrollment token의 유효시간이 끝날 수 있기 때문이다.



- 클러스터에 새로운 node 합류시키기

  - Elasticsearch가 최초로 실행되면 security auto-configuration process는 HTTP layer를 0.0.0.0에 바인드한다.
    - transport layer만 localhost에 바인드한다.
    - 이는 추가적인 설정 없이도 보안 기능을 활성화 한 상태로 single node를 실행할 수 있도록 하기 위함이다.
  - 다른 node를 합류시키기 위한 enrollment token 생성하기

  ```bash
  # 이미 cluster에 합류한 node
  $ bin/elasticsearch-create-enrollment-token -s node
  ```

  - kibana와 달리 node용 enrollment token을 자동으로 생성하지 않는 이유
    - production 환경에 새로운 node를 cluster에 합류시킬 때에는 합류 전에 address를 localhost가 아닌 다른 address에 binding하거나 bootstrap check등의 작업이 필요하다.
    - 만일 enrollment token을 자동으로 발급할 경우 위 작업을 하는 도중에 enrollment token이 만료될 수 있으므로, 자동으로 생성하지 않는다.

  - 합류시킬 node를 실행시킬 때 아래와 같이 enrollment token을 넣어준다.
    - 만일 다른 host에 존재하는 경우 `transport.host` 설정을 해줘야한다.

  ```bash
  # cluster에 합류할 node
  $ bin/elasticsearch --enrollment-token <enrollment-token>
  ```

