# alias

- Alias
  - Alias는 index 혹은 data stream에 별칭을 부여하는 기능이다.
    - Elasticsearch에서 제공하는 대부분의 API에서 index 혹은 data stream을 입력하는 자리에 alias를 입력할 수 있다.
  - Data stream alias와 index alias가 있으며, 하나의 alias가 index와 data stream을 모두 가리킬 수는 없다.
    - 또한 data stream의 backing index에 alias를 추가할 수 없다.



- Alias 추가 및 제거

  - 아래와 같이 `add` action을 사용하여 alias를 추가할 수 있다.
    - `index` parameter에 wildcard(`*`)를 사용할 수 있다.
    - 만약 wildcard가 index와 data stream을 모두 matching시킨다면 error가 반환된다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "logs-nginx.access-prod",
          "alias": "logs"
        }
      }
    ]
  }
  ```

  - Alias 제거
    - 아래와 같이 `remove` action을 사용하여 alias를 추가할 수 있다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "remove": {
          "index": "logs-nginx.access-prod",
          "alias": "logs"
        }
      }
    ]
  }
  ```

  - `actions`에 한 번에 여러 개의 action을 설정하는 것도 가능하다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "remove": {
          "index": "logs-nginx.access-prod",
          "alias": "logs"
        }
      },
      {
        "add": {
          "index": "logs-my_app-default",
          "alias": "logs"
        }
      }
    ]
  }
  ```

  - Index 생성시에 alias를 설정할 수도 있다.

  ```json
  // PUT alias-test
  {
    "aliases": {
      "my-alias": {}
    }
  }
  ```

  - Alias가 가리키는 index 혹은 data stream이 모두 삭제될 경우 alias도 함께 삭제된다.



- Alias 조회

  - 아래와 같이 조회할 수 있다.

  ```http
  GET _alias
  ```

  - 앞에 index 혹은 data stream을 입력하여 해당 index 혹은 data stream에 설정된 alias를 볼 수 있다.

  ```http
  GET <index | data_stream>/_alias
  ```

  - 뒤에 alias를 입력하여 alias에 해당하는 index와 data stream을 볼 수 있다.

  ```http
  GET _alias/<alias>
  ```



- 부가 기능

  - Write index
    - `is_write_index` parameter를 true로 줄 경우 alias로 보낸 write 요청을 해당 index 혹은 data stream으로 보낸다.
    - 만약 alias가 여러 개의 index 혹은 data stream을 가리키고 있으면서, `is_write_index`가 설정되어 있지 않을 경우, write 요청은 거절된다.
    - 만약 alias가 가리키는 index가 하나뿐일 경우 해당 index는 write index로 동작한다. 
    - 그러나 alias가 가리키는 data stream이 하나라고 하더라도 data stream은 write가 불가능하다. 
    - 따라서 alias가 가리키는 data stream이 하나라 할지라도 data stream은 반드시 `is_write_index`를 설정해야한다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "logs-my_app-default",
          "alias": "logs",
          "is_write_index": true
        }
      }
    ]
  }
  ```

  - `filter`를 통해 alias가 접근할 수 있는 문서를 제한할 수 있다.
    - 아래와 같이 설정할 경우 `my-alias`라는 alias는 `my-index-2099.05.06-000001` index의 전체 doucment 중 `user.id`가 "kimchy"인 doucment에만 접근이 가능하다.

  ```json
  POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "my-index-2099.05.06-000001",
          "alias": "my-alias",
          "filter": {
            "bool": {
              "filter": [
                {
                  "term": {
                    "user.id": "kimchy"
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
  ```

  - routing
    - `routing` 옵션을 사용하여 request를 특정 shard에 routing하는 것이 가능하다.
    - `routing`으로 검색과 색인에 동일한 routing 값을 사용할 수도 있고, `search_routing`과 `index_routing`을 따로 설정하는 것도 가능하다.

  ```json
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "my-index-2099.05.06-000001",
          "alias": "my-alias",
          "routing": "1"
        }
      }
    ]
  }
  
  // POST _aliases
  {
    "actions": [
      {
        "add": {
          "index": "my-index-2099.05.06-000001",
          "alias": "my-alias",
          "search_routing": "1",
          "index_routing": "2"
        }
      }
    ]
  }
  ```

  



# Security

- 보안 비활성화하기

  - `~/config/elastcsearch.yml`파일에서 아래 두 옵션을  false로 준다.

  ```yaml
  # disable security features
  xpack.security.enabled: false
  
  xpack.security.enrollment.enabled: false
  ```



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



## security 자동으로 적용하기

- Elasticsearch가 실행되면 아래와 같은 보안 작업들이 실행된다.
  - Transport and HTTP layers에 대해 TLS용 certificate와 key가 생성된다.
  - elasticsearh.yml 파일에 TLS 관련 설정이 작성된다.
  - elastic이라는 기본 사용자에 대한 비밀번호가 생성된다.
  - kibana에서 사용되는 enrollment token이 생성된다.
    - enrollment token의 유효기간은 30분이다.
    - node에서도 사용되지만, node를 위한 enrollment token은 자동으로 생성되지 않는다.
    - cluster에 합류시킬 node를 준비하는 데 상당한 시간이 걸릴 수 있고, 그러는 동안 enrollment token의 유효시간이 끝날 수 있기 때문이다.



- 보안 관련 설정이 자동으로 실행되지 않는 경우
  - Elasticsearch가 처음 실행될 때 아래와 같은 사항들을 체크하는데, 하나라도 fail이 된다면 보안 관련 설정이 자동으로 실행되지 않는다.
    - node가 처음 실행되는 것인지(처음 실행되는 것이 아니라면 실행되지 않는다).
    - 보안 관련 설정이 이미 설정되었는지(이미 설정되었다면 실행되지 않는다).
    - startup process가 node의 설정을 수정하는 것이 가능한지.
  - node 내부의 환경에 따라 실행되지 않기도 한다.
    - `/data` 디렉터리가 이미 존재하고, 비어있지 않은 경우.
    - `elasticsearch.yml` 파일이 존재하지 않거나 `elasticsearch.keystore`파일을 읽을 수 없는 경우
    - elasticsearch의 configuration 디렉터리가 writable 하지 않은 경우
  - setting에 따라 실행되지 않기도 한다.
    - `node.roles`에 해당 node가 master node로 선출될 수 없게 설정되었거나, data를 저장할 수 없게 설정된 경우
    - `xpack.security.autoconfiguration.enabled`가 false로 설정된 경우
    - `xpack.security.enabled`을 설정한 경우
    - `elasticsearch.keystore`또는 `elasticsearch.yml`에 `xpack.security.http.ssl.*` 또는 `xpack.security.transport.ssl.*`을 설정한 경우.
    - `discovery.type`, `discovery.seed_hosts`, 또는 `cluster.initial_master_nodes`에 값이 설정된 경우.
    - 단, `discovery.type`이 `single-node`이거나, `cluster.initial_master_nodes`의 값이 현재 노드 하나 뿐인 경우는 예외이다.



- 클러스터에 새로운 node 합류시키기

  > enrollment token은 security가 자동으로 설정되었을 때만 사용할 수 있다.

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

  - 새로 실행된 노드의 `config/certs` 폴더에 certificate와 key가 자동으로 생성된다.




-  PKCS#12
   - 사용자의 개인 정보 보호를 위한 포맷이다.
   - 바이너리 형식으로 저장되며 pkcs#12 포멧의 파일은 인증서, 개인키에 관한 내용을 하나의 파일에 모두 담고 있다.
   - 보통 `.pfx`, `.p12` 등의 확장자를 사용한다.
     - `.p12` 파일은 하나 이상의 certificate과 그에 대응하는 비공개키를 포함하고 있는 keystore 파일이며, 패스워드로 암호화되어 있다.



- `config/certs`의 파일들

  - `http_ca.crt`: HTTP layer(elasticsearch와 client 사이의 통신)를 위한 인증서를 sign하는 CA certificate파일.
    - 만일 enrollment token을 사용하여 kibana와 elasticsearch를 연결할 경우 HTTP layer의 CA certificate는 kibana의 `/data` 디렉터리에도 저장되어, elasticsearch의 CA와 kibana 사이의 신뢰를 확립하는 데 사용된다.
  - `http.p12`: HTTP layer를 위한 certificate와 key(비공개키)를 담고 있는 파일
  - `transport.p12`: transport layer(cluster 내부의 node들 사이의 통신)를 위한 certificate와 key(비공개키)를 담고 있는 파일.
  - `http.p12`와  `transport.p12` 파일은 password로 보호되고 있는 PKCS#12 keystores 파일이다.
    - elasticsearch는 이 keystore 파일의 password를 [`secure_settings`](https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-settings.html#reloadable-secure-settings)에 저장하고 있다.
    - password 조회를 위해서는 `bin/elasticsearch-keystore`를 사용한다.

  ```bash
  # http.p12
  $ bin/elasticsearch-keystore show xpack.security.http.ssl.keystore.secure_password
  
  # transport.p12
  $ bin/elasticsearch-keystore show xpack.security.transport.ssl.keystore.secure_password
  ```



- SSL certificate API

  - certificate들에 대한 정보를 반환한다.

  ```bash
  GET /_ssl/certificates
  ```

  - 응답

  ```json
  [
    {
      "path" : "<certificate의 경로>",
      "format" : "<jks | PKCS12 | PEM 중 하나가 온다>",
      "alias" : null,
      "subject_dn" : "<certificate의 subject의 Distinguished Name>",
      "serial_number" : "<인증서의 일련번호가 16진수로 온다>",
      "has_private_key" : <elasticsearch가 certificate의 private key에 접근할 수 있는지 여부>,
      "expiry" : "<aksfy기한>"
    }
  ]
  ```



- `elasticsearch-certutil` tool

  - TLS에 사용되는 certificate를 보다 쉽게 생성할 수 있게 도와주는 툴이다.

  ```bash
  $ bin/elasticsearch-certutil
  (
  (ca [--ca-dn <name>] [--days <n>] [--pem])
  
  | (cert ([--ca <file_path>] | [--ca-cert <file_path> --ca-key <file_path>])
  [--ca-dn <name>] [--ca-pass <password>] [--days <n>]
  [--dns <domain_name>] [--in <input_file>] [--ip <ip_addresses>]
  [--multiple] [--name <file_name>] [--pem] [--self-signed])
  
  | (csr [--dns <domain_name>] [--in <input_file>] [--ip <ip_addresses>]
  [--name <file_name>])
  
  [-E <KeyValuePair>] [--keysize <bits>] [--out <file_path>]
  [--pass <password>]
  )
  
  | http
  
  [-h, --help] ([-s, --silent] | [-v, --verbose])
  ```

  - CA mode
    - 새로운 CA를 생성할 때 사용한다.
    - 기본적으로 CA certificate와 private key 정보를 담고 있는 PKCS#12 형식의 하나의 파일을 생성한다.
    - `--pem` 옵션을 함께 줄 경우 PEM 형식의 certificate와 private key를 압축한 파일을 생성한다.
  - CERT mode
    - X.509 certificate와 private key를 생성한다.
    - `--self-signed` 옵션을 주지 않았다면 `--ca` 옵션이나 `--ca-cert`와 `--ca-key` 옵션을 반드시 줘야 한다.
    - `--in` 옵션에 YAML 형식의 파일을 주면, 해당 파일에 작성된대로 복수의 certificate와 private key를 생성한다.
  - CSR mode
    - 신뢰할 수 있는 CA에 sign요청을 보내는 CSR을 생성한다.
    - CERT mode와 마찬가지로 `--in` 옵션을 줄 수 있다.
  - HTTP mode
    - HTTP(REST) interface를 위한 certificate를 생성한다.





### Kibana 연동하기

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





### Cleint를 elasticsearch에 연결하기

- Elasticsearch와 연결되는 모든 클라이언트는 검증 과정을 거친다.
  - Elasticsearch의 Client에는 대표적으로 아래와 같은 것들이 있다.
    - Kibana
    - Logstash
    - Beats
    - Python client
  - Client들은 모두 Elasticsearch가 HTTPS 를 위해 사용하는 certificate를 신뢰할 수 있는지 검증해야 한다.



- Client와 Elasticsearch를 연동하는 방법은 크게 두 가지가 있다.

  - Certificate를 사용하는 방법.
    - Security를 자동으로 설정할 경우 elasticsearch는 HTTP 계층 용 certificate(`http_ca.crt`)를 생성한다.
    - 해당 파일을 연결하고자 하는 client에 복사하여 사용하면 된다.
  - Fingerprint를 사용하는 방법.
    - 상기했듯 security를 자동으로 설정할 경우 elasticsearch는 HTTP 계층 용 certificate(`http_ca.crt`)를 생성한다.
    - 그와 동시에 해당 certificate의 fingerprint도 터미널에 출력되는데, 해당 fingerprint를 복사하여 client의 confiuration에 추가하면 된다.
    - 만일 terminal에서 fingerprint를 찾기 어렵다면 아래와 같이 얻을 수 있다.

  ```bash
  $ openssl x509 -fingerprint -sha256 -in config/certs/http_ca.crt
  ```







## security 수동으로 적용하기

### Transport layer 보안

- 가장 기본적인 보안은 악의적인 노드가 클러스터에 합류하는 것을 막는 것이다.

  - transport 계층(node들 사이의 통신에 사용되는 계층)은 노드들 사이의 암호화와 인증에 모두 TLS(Transport Layer Secuirty)를 사용한다.
  - 정확히 적용된 TLS는 악의적인 노드가 클러스터에 합류하는 것을 막고, 다른 노드들로부터 데이터를 가져가는 것을 막을 수 있다.

  - username과 password기반 인증이 HTTP 계층에서 local cluster의 보안을 높이는 것에는 도움이 되지만 노드들 사이의 보안을 위해서는 TLS가 필요하다.



- TLS
  - Trasnport Layer Security는 산업 표준 protocol의 이름이다.
    - 이전에는 Secure Socket Layer(SSL)이라 불렸다.
  - 네트워크 통신에 (암호화 같은)보안 제어를 위해 사용된다.
  - Transport Protocol
    - Elasticsearch의 노드들이 cluster 내의 다른 노드들과 통신하기 위해 사용하는 protocol의 이름이다.
    - Elasticsearch에서만 사용하는 이름이며, Elasticsearch에서는 transport port와 HTTP port를 구분한다.
    - Node들은 서로 다른 노드와 transport port를 통해 통신하고, REST client들은 HTTP port를 통해 elasticsearch와 통신한다.
    - transport라는 단어는 TLS와 elasticsearch의 transport protocol에 모두 사용되지만 서로 다른 의미를 가진다.
    - TLS는 transport port와 HTTP port에 모두 적용될 수 있다.
  - TLS를 통해 노드들 사이의 통신이 암호화되고, 검증되도록 할 수 있다.
    - Elasticsearch의 노드들은 다른 노드들과 통신할 때, 자신들의 신원 확인을 위해 certificates를 사용한다.
    - 새로운 노드가 cluster에 추가되려면 반드시 같은 CA로부터 sign 받은 certificate가 필요하다.
    - Transport layer에 대해서는, 기존에 이미 존재하는, 공유 가능한 CA대신에 노드들이 보다 엄격하게 통제될 수 있도록 별도의 CA를 사용하는 것이 추천된다.
  - TLS를 사용하도록 설정된 노드와. 그렇지 않은 노드 사이의 통신은 불가능하다.



- CA 생성하기

  - Elasticsearch를 시작하기 전에 elasticsearch tool 중 하나인 elasticsearch-certutil을 사용하여 CA를 생성한다.
    - prompt에 파일명을 입력할 수 있는데 입력하지 않을 경우 기본값은 `elastic-stack-ca.p12`이다.
    - 그 후 비밀번호를 설정할 수 있는 데, production 환경이 아니라면 공백으로 두는 것도 가능하다.
  - 결과 파일에는 CA를 위한 public certificate과 certificate을 sign하는데 필요한 private key가 포함되어 있다.

  ```bash
  $ bin/elasticsearch-certutil ca
  ```



- certificate과 private key 생성하기

  - prompt가 뜨면 위에서 설정한 password를 입력하고, 생성할 certificate의 비밀번호와 파일경로를 입력한다.
  - 아래 명령어로 생성되는 파일은 keystore 파일로, node certificate과 node key, 그리고 CA certificate를 포함하고 있다.

  ```bash
  $ bin/elasticsearch-certutil cert --ca <위에서 생성한 CA 파일>
  ```

  - output으로 나온 keystore 파일을 모든 노드의 `$ES_PATH_CONF` 디렉터리에 복사한다.



- TLS를 사용하여 노드들 사이의 통신을 암호화하기

  - Elasticsearch는 TLS와 관련된 모든 파일들(certificate, key, keystore, truststore 등)을 모니터링한다.
    - Elasticsearch는 `resource.reload.interval.high`에 설정된 주기로 변경 사항을 폴링한다.
    - 만일 TLS관련 파일을 업데이트 할 경우 Elasticsearch가 파일을 다시 로드한다.
  - 설정 변경하기
    - 하나의 cluster로 묶으려는 모든 node들의 `elasticsearch.yml` 파일을 아래와 같이 변경한다.
    - 같은 certificate file을 사용하기에, `verification_mode`를 `certificate`로 설정한다.

  ```yaml
  cluster.name: my-cluster
  # 각 노드별로 다르게 준다.
  node.name: node-1
  xpack.security.transport.ssl.enabled: true
  xpack.security.transport.ssl.verification_mode: certificate 
  xpack.security.transport.ssl.client_authentication: required
  xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
  xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
  ```

  - 만일 certificate 파일을 생성할 때 password를 설정했다면, 아래 명령어를 통해 password를 elasticsearch keystore에 저장한다.
    - 마찬가지로 모든 노드에서 실행해준다.

  ```bash
  $ bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
  $ bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
  ```



- TLS 관련 설정
  - `xpack.security.transport.ssl.verification_mode`
    - certificate의 검증 방식을 설정한다.
    - `full`: certificate가 믿을 수 있는 CA에 의해 sign 된 것인지와, 서버의 hostname(또는 IP)가 certificate 내부에 있는 값과 일치하는지도 검증한다.
    - `certificate`: certificate가 믿을 수 있는 CA에의해 sign된 것인지만 검사한다.
    - `none`: certificate에 대한 검증을 수행하지 않는다. 절대 production 환경에서 사용해선 안된다. 



### HTTP layer 보안

- CSR
  - `elasticsearch-certutil` tool을 실행하면 어떻게 certificate을 생성할 것인지에 대한 여러 질문을 던진다. 
  - 가장 중요한 질문은 Certificate Signing Reqeust(CSR)을 생성할지 여부이다.
    - CSR은 CA에게 certificate에 sign해줄 것을 요청하는 것이다.
  - 만일 `bin/elasticsearch-certutil ca` 명령어를 통해서 CA를 생성했다면 `n`을 입력한다.
    - 그 후 CA 파일의 경로를 입력한다.
  - 사내에 이미 구축되어 있는 CA로 sign하길 원한다면 `y`를 입력한다.
    - 만일 사내에 security 팀이 있을 경우, 신뢰할만한 CA가 존재할 것이므로 CSR을 사용하고, 해당 요청을 CA를 제어하는 팀에 보내면 된다.



- HTTP 통신을위한 certificate와 key 생성하기

  - `elasticsearch-certutil`에 http 옵션을 줘서 실행한다.

  ```bash
  $ elasticsearch-certutil http
  ```

  - 생성 과정 예시
    - CSR을 생성하지를 물으면 `n`을 입력한다.
    - 기존에 생성한 CA를 사용할지를 물으면 `y`를 입력한다.
    - CA와 key의 경로를 입력한다.
    - CA의 password를 입력한다.
    - certificate의 만료 기한을 설정한다. 년, 월, 일로 설정 가능하며 기본값은 90D이다.
    - 노드별로 certificate를 생성할지 물으면 `y`를 입력한다.
    - node에 연결할 때 사용할 hostname들을 입력한다. 여기서 입력한 hostname들은 DNS name으로 certificate의 Subject Alternative name(SAN) 필드에 추가된다.
    - 각 노드의 IP를 입력한다.
    - certificate를 생성할 때 필요한 설정값들 중 변경할 것이 있는지 물으면 `n`을 입력한다.
    - 마지막으로 certificate의 password를 입력한다.
  - 위 과정을 모두 마치면 `.zip`파일(기본 파일명은 `elasticsearch-ssl-http.zip`)이 생성된다.
    - 파일의 압축을 풀면 `elasticsearch` 폴더와 `kibana` 폴더가 생성된다.
    - `elasticsearch` 폴더의 `http.p12` 파일은 PKCS#12 포맷의 keystore로, certificate의 복사본과 private key가 담겨 있다.
    - `kibana` 폴더의 `elasticsearch-ca.pem`은 HTTP layer에 대해서 elasticsearch CA를 신뢰할 수 있게 해주는데 사용한다.



- Cluster 내의 모든 node에 아래 과정을 실행한다.

  - `http.p12` 파일을 `$ES_PATH_CONF`에 복사한다.
  - `elasticsearch.yml` 파일을 아래와 같이 수정한다.

  ```yaml
  xpack.security.http.ssl.enabled: true
  xpack.security.http.ssl.keystore.path: http.p12
  ```

  - 아래 명령어를 실행한다.

  ```bash
  $ bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
  ```

  - 노드를 다시 시작한다.



#### Kibana HTTP client 암호화하기.

- Browser는 kibana로 traffic을 보내고, kibana는 elasticsearch에 trafic을 보낸다.
  - 이 두 개의 채널은 TLS를 사용하기 위해 개별적으로 설정을 해줘야한다.



- Kibana와 Elasticsearch 사이의 traffic 암호화하기

  - `elasticsearch-certutil http` 명령어의 결과로 생성된 압축 파일을 풀면 `kibana` 디렉터리가 생성된다.
    - 이 디렉터리 내부의 `elasticsearch-ca.pem` 파일을 포함하고 있다.
    - 해당 파일을 `$KBN_PATH_CONF` 폴더에 복사한다.

  - `kibana.yml` 파일을 아래와 같이 수정한다.

  ```yaml
  elasticsearch.username: kibana_system
  elasticsearch.password: <kibana_system의 password>
  elasticsearch.ssl.certificateAuthorities: $KBN_PATH_CONF/elasticsearch-ca.pem
  elasticsearch.hosts: https://<elasticsearch_host>:<port>
  ```

  - kibana를 재실행한다.
    - 만일 login을 해도 계속 login 창으로 redirect가 된다면 브라우저를 완전히 종료하고 다시 열면 된다.



- Kibana와 Browser 사이의 traffic을 암호화하기

  - Kibana를 위한 server certificate와 private key를 생성한다.
    - Browser가 kibana로 통신을 보내면, kibana는 이 server certificate와 private key를 사용한다.
    - Server certificate를 얻으면, 브라우저가 신뢰할 수 있도록 subject alternative name(SAN)을 정확히 설정해야한다.
    - 하나 이상의 SAN을 kibana 서버의 FQDN(Fully Quailified Domain Name), hostname, IP로 설정할 수 있다.
    - SAN을 선택할 때, browser와 kibana가 통신하기 위해 사용할 속성(FQDN, hostanme, IP)을 선택한다.
  - Kibana용 CSR
    - CSR은 certificate를 생성하고 sign하는데 사용되는 CA에 대한 정보를 담고 있다.
    - Certificate는 신뢰할 수도(public, trusted CA에 의해 sign된 경우)있고 신뢰할 수 없을 수도(internal CA에 의해 sign된 경우) 있다.
    - self-sign하거나 internally-sign된 certificate는 development 환경에서는 사용 가능하지만 production 환경에서는 사용할 수 없다.
  - 인증되지 않은 server certificate와 암호화되지 않은 private key 생성하기
    - CSR에 사용할 인증되지 않은 server certificate와 암호화되지 않은 private key 생성한다.
    - 아래 명령의 결과로 생성된 certificate는 kibana-server라는 common name(CN)과, `example.com`, `www.example.com`이라는 SAN을 가진다.

  ```bash
  $ bin/elasticsearch-certutil csr -name kibana-server -dns example.com,www.example.com
  ```

  - 위 명령어의 결과 `csr-bundle.zip`이라는 파일이 생성된다.
    - `kibana-server.csr`: sign되지 않은 certificate
    - `kibana-server.key`: 암호화되지 않은 private key
  - internal CA 또는 믿을 수 있는 CA에 CSR 요청을 보낸다.
    - 인증을 받은 후의 certificate는 다른 `.crt` 등의 다른 format으로 format이 변경될 수 있다.
  - `kibana.yml`파일 수정하기

  ```yaml
  server.ssl.enabled: true
  
  server.ssl.certificate: $KBN_PATH_CONF/kibana-server.crt
  server.ssl.key: $KBN_PATH_CONF/kibana-server.key
  ```

  - kibana를 실행한다.



#### Beats 보안

> https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html#configure-beats-security 참고





## 비밀번호 설정하기

- Build-in users
  - Elastic Stack은 built-in user를 제공한다.
    - 각 user들은 고정된 권한을 가지고 있으며, password가 설정되기 전에는 인증될 수 없다.
    - `elastic`이라는 build-in user는 build-in user들의 password를 설정하는데 사용할 수 있다.
  - `elastic` user를 사용해선 안된다.
    - Cluster에 대한 모든 접근 권한이 필요한 경우를 제외하고는 `elastic` user를 사용해선 안된다.
    - `elastic` user를 사용하여 최소한의 필수적인 역할과 권한을 지닌 user들을 생성하여 사용하는 것이 좋다.
  - 아래와 같은 built-in user들이 있다.
    - `elastic`: built-in super user.
    - `kibana_system`: Kibana와 Elasticsearch가 통신하기위해 Kibana에서 사용하는 user.
    - `logstash_system`: monitoring한 정보를 elasticsearch에 저장하기 위해 logstash가 사용하는 user.
    - `beats_system`: monitoring한 정보를 elasticsearch에 저장하기 위해 beats가 사용하는 user.
    - `apm_system`: monitoring한 정보를 elasticsearch에 저장하기 위해 APM server가 사용하는 user.
    - `remote_monitoring_user`: monitoring 정보를 수집하고 elasticsearch에 저장하기위해 metricbeat에서 사용하는 user.
  - built-in user들은 `.secuity`라는 index에 저장되어 있다.
    - 만일 built-in user가 비활성화되거나 비밀번호가 변경될 경우, 클러스터 내부의 모든 노드에 변경사항이 자동으로 반영된다.
    - 만일 `.security`가 삭제되거나 snapshot으로부터 재생성되었을 경우, 변경사항은 유실된다.



- Bootstrap password
  - Elasticsearch가 실행될 때, `elastic` user에 password가 설정되어있지 않다면, elasticsearchs는 bootstrap password를 사용한다.
  - Bootstrap password는 모든 built-in user의 password를 설정할 수 있는 tool을 실행하는 데 사용된다.
    - 만일 super user인 `elastic`의 password를 설정했다면, bootsrap password는 더 이상 쓸 곳이 없다.
  - Bootstrap password를 변경하거나 알 필요는 없다.
    - `bootstrap.password` 세팅을 입력하면 해당 값으로 bootstrap password가 설정된다.



- Password 설정하기

  - `elasticsearch-reset-password` tool 사용하기
    - `-u` 옵션으로 사용자명을 입력한다.
    - `-i` 옵션으로 변경할 password를 입력한다.

  ```bash
  $ bin/elasticsearch-reset-password -u <user name>
  ```

  - API로 변경하기

  ```json
  // POST /_security/user/<user name>/_password
  {
      "password":"<변경할 password>"
  }
  ```





# Elasticsearch UUID

```java
package org.example;

import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.Base64;
import java.security.SecureRandom;
import java.util.Enumeration;
import java.util.concurrent.atomic.AtomicInteger;
/**
 * These are essentially flake ids but we use 6 (not 8) bytes for timestamp, and use 3 (not 2) bytes for sequence number. We also reorder
 * bytes in a way that does not make ids sort in order anymore, but is more friendly to the way that the Lucene terms dictionary is
 * structured.
 * For more information about flake ids, check out
 * https://archive.fo/2015.07.08-082503/http://www.boundary.com/blog/2012/01/flake-a-decentralized-k-ordered-unique-id-generator-in-erlang/
 */

class MacAddressProvider {

    private static byte[] getMacAddress() throws SocketException {
        Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces();
        if (en != null) {
            while (en.hasMoreElements()) {
                NetworkInterface nint = en.nextElement();
                if (!nint.isLoopback()) {
                    // Pick the first valid non loopback address we find
                    byte[] address = nint.getHardwareAddress();
                    if (isValidAddress(address)) {
                        return address;
                    }
                }
            }
        }
        // Could not find a mac address
        return null;
    }

    private static boolean isValidAddress(byte[] address) {
        if (address == null || address.length != 6) {
            return false;
        }
        for (byte b : address) {
            if (b != 0x00) {
                return true; // If any of the bytes are non zero assume a good address
            }
        }
        return false;
    }

    public static byte[] getSecureMungedAddress() {
        byte[] address = null;
        try {
            address = getMacAddress();
        } catch (SocketException e) {
            // address will be set below
        }

        if (!isValidAddress(address)) {
            address = constructDummyMulticastAddress();
        }

        byte[] mungedBytes = new byte[6];
        SecureRandomHolder.INSTANCE.nextBytes(mungedBytes);
        for (int i = 0; i < 6; ++i) {
            mungedBytes[i] ^= address[i];
        }

        return mungedBytes;
    }

    private static byte[] constructDummyMulticastAddress() {
        byte[] dummy = new byte[6];
        SecureRandomHolder.INSTANCE.nextBytes(dummy);
        /*
         * Set the broadcast bit to indicate this is not a _real_ mac address
         */
        dummy[0] |= (byte) 0x01;
        return dummy;
    }


}

class SecureRandomHolder {
    // class loading is atomic - this is a lazy & safe singleton to be used by this package
    public static final SecureRandom INSTANCE = new SecureRandom();
}

class TimeBasedUUIDGenerator {

    // We only use bottom 3 bytes for the sequence number.  Paranoia: init with random int so that if JVM/OS/machine goes down, clock slips
    // backwards, and JVM comes back up, we are less likely to be on the same sequenceNumber at the same time:
    private final AtomicInteger sequenceNumber = new AtomicInteger(SecureRandomHolder.INSTANCE.nextInt());

    // Used to ensure clock moves forward:
    private long lastTimestamp;

    private static final byte[] SECURE_MUNGED_ADDRESS = MacAddressProvider.getSecureMungedAddress();

    static {
        assert SECURE_MUNGED_ADDRESS.length == 6;
    }

    // protected for testing
    protected long currentTimeMillis() {
        return System.currentTimeMillis();
    }

    // protected for testing
    protected byte[] macAddress() {
        return SECURE_MUNGED_ADDRESS;
    }

    public String getBase64UUID() {
        final int sequenceId = sequenceNumber.incrementAndGet() & 0xffffff;
        long timestamp = currentTimeMillis();

        synchronized (this) {
            // Don't let timestamp go backwards, at least "on our watch" (while this JVM is running).  We are still vulnerable if we are
            // shut down, clock goes backwards, and we restart... for this we randomize the sequenceNumber on init to decrease chance of
            // collision:
            timestamp = Math.max(lastTimestamp, timestamp);

            if (sequenceId == 0) {
                // Always force the clock to increment whenever sequence number is 0, in case we have a long time-slip backwards:
                timestamp++;
            }

            lastTimestamp = timestamp;
        }

        final byte[] uuidBytes = new byte[15];
        int i = 0;

        // We have auto-generated ids, which are usually used for append-only workloads.
        // So we try to optimize the order of bytes for indexing speed (by having quite
        // unique bytes close to the beginning of the ids so that sorting is fast) and
        // compression (by making sure we share common prefixes between enough ids),
        // but not necessarily for lookup speed (by having the leading bytes identify
        // segments whenever possible)

        // Blocks in the block tree have between 25 and 48 terms. So all prefixes that
        // are shared by ~30 terms should be well compressed. I first tried putting the
        // two lower bytes of the sequence id in the beginning of the id, but compression
        // is only triggered when you have at least 30*2^16 ~= 2M documents in a segment,
        // which is already quite large. So instead, we are putting the 1st and 3rd byte
        // of the sequence number so that compression starts to be triggered with smaller
        // segment sizes and still gives pretty good indexing speed. We use the sequenceId
        // rather than the timestamp because the distribution of the timestamp depends too
        // much on the indexing rate, so it is less reliable.

        uuidBytes[i++] = (byte) sequenceId;
        // changes every 65k docs, so potentially every second if you have a steady indexing rate
        uuidBytes[i++] = (byte) (sequenceId >>> 16);

        // Now we start focusing on compression and put bytes that should not change too often.
        uuidBytes[i++] = (byte) (timestamp >>> 16); // changes every ~65 secs
        uuidBytes[i++] = (byte) (timestamp >>> 24); // changes every ~4.5h
        uuidBytes[i++] = (byte) (timestamp >>> 32); // changes every ~50 days
        uuidBytes[i++] = (byte) (timestamp >>> 40); // changes every 35 years
        byte[] macAddress = macAddress();
        assert macAddress.length == 6;
        System.arraycopy(macAddress, 0, uuidBytes, i, macAddress.length);
        i += macAddress.length;

        // Finally we put the remaining bytes, which will likely not be compressed at all.
        uuidBytes[i++] = (byte) (timestamp >>> 8);
        uuidBytes[i++] = (byte) (sequenceId >>> 8);
        uuidBytes[i++] = (byte) timestamp;

        assert i == uuidBytes.length;

        return Base64.getUrlEncoder().withoutPadding().encodeToString(uuidBytes);
    }
}


class Main {
    public static void main(String[] args) {
        TimeBasedUUIDGenerator uuidGenerator = new TimeBasedUUIDGenerator();
        for (int i = 0; i < 10; i++) {
            System.out.println(uuidGenerator.getBase64UUID());
        }
    }
}
```

