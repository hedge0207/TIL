# configsync plugin

## 개요

> https://github.com/codelibs/elasticsearch-configsync

- 각 노드별로 파일을 sync시킬 수 있게 해주는 plugin
  - 현재는 기능 추가 없이 elasticsearch version에 맞추어 빌드만 이루어지고 있다.
  - fork한 repo가 몇 있으나 관리 되고 있는 곳은 없다.



- 설치

  > https://repo1.maven.org/maven2/org/codelibs/elasticsearch-configsync/

  - 위 링크에서 elasticsearch version과 일치하는 version을 다운 받는다.
  - default.policy 파일을 작성한다.
    - jdk 일정 버전 이상부터는 파일 쓰기 권한이 부여되지 않아 sync가 불가능해진다.
    - 따라서 아래와 같이 permission을 추가해준다.

  ```yaml
  // permissions needed by applications using java.desktop module
  grant {
      permission java.lang.RuntimePermission "accessClassInPackage.com.sun.beans";
      permission java.lang.RuntimePermission "accessClassInPackage.com.sun.beans.*";
      permission java.lang.RuntimePermission "accessClassInPackage.com.sun.java.swing.plaf.*";
      permission java.lang.RuntimePermission "accessClassInPackage.com.apple.*";
      // 아래 부분을 추가해준다.
      permission java.io.FilePermission "<<ALL FILES>>", "read,write,delete";
  };
  ```

  - 아래와 같이 dockerfile을 작성한다.
    - 위에서 작성한 default.policy 파일을 복사한다.
    - plugin을 복사하고, 설치한다.
    - 기본 사용자인 elasticsearch로는 /usr/share/elasticsearch/modules에 폴더 생성이 불가능하므로 root user로 변경한다.
    - root user로는 elasticsearch 생성이 불가능하므로 다시 elasticsearch user로 변경한다.
  
  ```dockerfile
  FROM docker.elastic.co/elasticsearch/elasticsearch:8.1.0
  
  USER root
  
  COPY ./default.policy /usr/share/elasticsearch/jdk/lib/security/default.policy
  
  COPY ./configsync-8.1.0.zip /tmp/configsync-8.1.0.zip
  RUN mkdir -p /usr/share/elasticsearch/modules/configsync
  RUN unzip -d /usr/share/elasticsearch/modules/configsync /tmp/configsync-8.1.0.zip
  
  USER elasticsearch
  ```



- 동작 과정

  - 임의의 위치(기본값은 /usr/share/elasticsearch/config)에 sync시킬 파일을 생성한다.
  - 생성한 파일을 `configsync`인덱스에 등록한다.
    - `configsync` 인덱스는 elasticsearch가 실행되면서 자동으로 생성된다.

  ```bash
  $ curl -XPOST -H 'Content-Type:application/json' localhost:9200/_configsync/file?path=<file_path> --data-binary @<file_path>
  ```

  - 인덱스에 등록된 파일을 각 노드들에 sync시킨다.
    - `configsync.flush_interval`에 설정된 시간 만큼이 지나면 자동으로 sync 된다.
    - 바로 sync시키려면 아래와 같이 요청을 보내면 된다.

  ```bash
  $ curl -XGET -H 'Content-Type:application/json' localhost:9200/_configsync/flush
  ```

  - 인덱스에 등록 된 모든 file list를 보려면 아래와 같이 요청을 보내면 된다.

  ```bash
  $ curl -XGET -H 'Content-Type:application/json' localhost:9200/_configsync/file
  ```

  - 특정 file만 보려면 아래와 같이 요청을 보내면 된다.

  ```bash
  $ curl -XGET -H 'Content-Type:application/json' localhost:9200/_configsync/file?path=<file_path>
  ```

  - index에 등록된 file을 삭제하려면 아래와 같이 요청을 보낸다.
    - index에서만 삭제될 뿐 실제 file이 삭제되지는 않는다.

  ```bash
  $ curl -XDELETE -H 'Content-Type:application/json' localhost:9200/_configsync/file?path=<file_path>
  ```

  - reset API도 있다.
    - scheduler를 초기화한다.

  ```bash
  $ curl -XPOST -H 'Content-Type:application/json' localhost:9200/_configsync/reset
  ```





## 코드 분석

- 각 action별로 action, request, response, 그리고 node들 사이에 통신이 필요한 경우 transport action 등을 생성해줘야한다.

  > 아직 완전히 이해하지 못했으므로 아래 내용은 대부분이 추정이다.

  - response가 생성되면 해당 type의 response를 바라보고 있는 `ActionListner`에 의해서 `ActionListner`를 상속 받은 클래스의  `onResponse` 메서드가 실행된다.
  - `transportService.sendRequest`를 통해 다른 node로 요청을 보내면 요청을 받은 노드는 특정 규칙에 따라 `HandledTransportAction` Action class를 선정하고 해당 class가 override한 `doExecute` 함수를 실행시킨다.



- file을 인덱스에 등록하는 과정

  - `POST /_configsync/file?path=<file_path>`로 요청을 보내면 아래 코드가 실행된다.
  - `src.main.java.org.codelibs.elasticsearch.configsync.rest.RestConfigSyncFileAction`

  ```java
  @Override
  protected RestChannelConsumer prepareRequest(final RestRequest request, final NodeClient client) throws IOException {
      try {
          final BytesReference content = request.content();
          switch (request.method()) {
          // (...)
          case POST: {
              if (content == null) {
                  throw new ElasticsearchException("content is empty.");
              }
              final String path;
              byte[] contentArray;
              if (request.param(ConfigSyncService.PATH) != null) {
                  path = request.param(ConfigSyncService.PATH);
                  try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
                      content.writeTo(out);
                      contentArray = out.toByteArray();
                  }
              } else {
                  final Map<String, Object> sourceAsMap = SourceLookup.sourceAsMap(content);
                  path = (String) sourceAsMap.get(ConfigSyncService.PATH);
                  final String fileContent = (String) sourceAsMap.get(ConfigSyncService.CONTENT);
                  contentArray = Base64.getDecoder().decode(fileContent);
              }
              // file을 인덱스에 저장하는 store 메서드를 호출한다.
              return channel -> configSyncService.store(path, contentArray,
                      wrap(res -> sendResponse(channel, null), e -> sendErrorResponse(channel, e)));
          }
          // (...)
  }
  ```

  - `src.main.java.org.codelibs.elasticsearch.configsync.service.ConfigSyncService`

  ```java
  public void store(final String path, final byte[] contentArray, final ActionListener<IndexResponse> listener) {
      checkIfIndexExists(wrap(response -> {
          try {
              final String id = getId(path);
              final XContentBuilder builder = JsonXContent.contentBuilder();
              builder.startObject();
              builder.field(PATH, path);
              builder.field(CONTENT, contentArray);
              builder.field(TIMESTAMP, new Date());
              builder.endObject();
   	  //elasticsearch client에 색인 요청을 보낸다.
         client().prepareIndex(index).setId(id).setSource(builder).setRefreshPolicy(RefreshPolicy.IMMEDIATE).execute(listener);
          } catch (final IOException e) {
              throw new ElasticsearchException("Failed to register " + path, e);
          }
      }, listener::onFailure));
  }
  ```



- file이 각 node에 sync되는 과정

  - `src.main.java.org.codelibs.elasticsearch.configsync.rest.RestConfigSyncFlushAction`

  ```java
  @Override
  protected RestChannelConsumer prepareRequest(final RestRequest request, final NodeClient client) throws IOException {
      try {
          switch (request.method()) {
          case POST:
              return channel -> configSyncService
                  	// flush 메서드가 실행된다.
                      .flush(wrap(response -> sendResponse(channel, null), e -> sendErrorResponse(channel, e)));
          default:
              return channel -> sendErrorResponse(channel, new ElasticsearchException("Unknown request type."));
          }
      } catch (final Exception e) {
          return channel -> sendErrorResponse(channel, e);
      }
  }
  ```

  - `src.main.java.org.codelibs.elasticsearch.configsync.service.ConfigSyncService`

  ```java
  public void flush(final ActionListener<ConfigFileFlushResponse> listener) {
      checkIfIndexExists(wrap(response -> {
          final ClusterState state = clusterService.state();
          // cluster를 구성 중인 모든 노드들에 대한 정보를 받아온다.
          final DiscoveryNodes nodes = state.nodes();
          // node들을 Iterator로 생성한다.
          final Iterator<DiscoveryNode> nodesIt = nodes.getDataNodes().values().iterator();
          flushOnNode(nodesIt, listener);
      }, listener::onFailure));
  }
  
  public void flushOnNode(final Iterator<DiscoveryNode> nodesIt, final ActionListener<ConfigFileFlushResponse> listener) {
      // 각 node를 순회하면서 다음 node가 있으면 sendRequest, 더 이상 없으면 onResponse를 실행시킨다.
      if (!nodesIt.hasNext()) {
          listener.onResponse(new ConfigFileFlushResponse(true));
      } else {
          fileFlushAction.sendRequest(nodesIt, listener);
      }
  }
  ```

  - `src.main.java.org.codelibs.elasticsearch.configsync.action.TransportFileFlushAction`

  ```java
  public class TransportFileFlushAction extends HandledTransportAction<FileFlushRequest, FileFlushResponse> {
  
      private final TransportService transportService;
  
      private final ConfigSyncService configSyncService;
  
      @Inject
      public TransportFileFlushAction(final TransportService transportService, final ActionFilters actionFilters,
              final ConfigSyncService configSyncService) {
          super(FileFlushAction.NAME, transportService, actionFilters, FileFlushRequest::new);
          this.transportService = transportService;
          this.configSyncService = configSyncService;
          configSyncService.setFileFlushAction(this);
      }
  	
      // 다른 node로부터 요청이 오면 실행되는 함수.
      @Override
      protected void doExecute(final Task task, final FileFlushRequest request, final ActionListener<FileFlushResponse> listener) {
          // elasticsearch에 검색 요청을 보내 configsync 인덱스의 정보를 받아오는 execute 함수를 실행한다.
          // 검색이 성공하면 ConfigFileWriter class의 onResponse 메서드가 실행된다.
          configSyncService.newConfigFileWriter().execute(wrap(response -> {
              listener.onResponse(new FileFlushResponse(true));
          }, e -> {
              listener.onFailure(e);
          }));
      }
  
      public void sendRequest(final Iterator<DiscoveryNode> nodesIt, final ActionListener<ConfigFileFlushResponse> listener) {
          // iterator에서 다음 node에 대한 정보를 받아온다.
      	final DiscoveryNode node = nodesIt.next();
      	// 해당 node에 request를 보낸다.
          transportService.sendRequest(node, FileFlushAction.NAME, new FileFlushRequest(), new TransportResponseHandler<FileFlushResponse>() {
  
              @Override
              public FileFlushResponse read(final StreamInput in) throws IOException {
                  System.out.println("READ");
                  return new FileFlushResponse(in);
              }
  
              @Override
              public void handleResponse(final FileFlushResponse response) {
                  System.out.println("HANDLE RESPONSE");
                  configSyncService.flushOnNode(nodesIt, listener);
              }
  
              @Override
              public void handleException(final TransportException exp) {
                  System.out.println("HANDLE EXCEPT");
                  listener.onFailure(exp);
              }
  
              @Override
              public String executor() {
                  System.out.println("EXE");
                  return ThreadPool.Names.GENERIC;
              }
          });
      }
  }
  ```

  - `src.main.java.org.codelibs.elasticsearch.configsync.service.ConfigSyncService`

  ```java
  public void onResponse(final SearchResponse response) {
      if (terminated.get()) {
          if (logger.isDebugEnabled()) {
              logger.debug("Terminated {}", this);
          }
          listener.onFailure(new ElasticsearchException("Config Writing process was terminated."));
          return;
      }
      // 응답으로 부터 hits를 가져온다.
      final SearchHits searchHits = response.getHits();
      final SearchHit[] hits = searchHits.getHits();
      for (final SearchHit hit : hits) {
          final Map<String, Object> source = hit.getSourceAsMap();
      }
      if (hits.length == 0) {
          listener.onResponse(null);
      } else {
          for (final SearchHit hit : hits) {
              final Map<String, Object> source = hit.getSourceAsMap();
              // 실제 file을 생성, 수정하는 메서드를 실행시킨다.
              updateConfigFile(source);
          }
          final String scrollId = response.getScrollId();
          client().prepareSearchScroll(scrollId).setScroll(scrollForUpdate).execute(this);
      }
  }
  ```



# Elasticsearch plugin 개발

- Elasticsearch plugin
  - Elasticsearch는 Elasticsearch에 기능을 추가할 수 있게 해주는 모듈이다.
  - Elasticsearch source code에 정의되어 있는 Java interface를 구현하는 방식으로 개발한다.
  - JAR file과 metadata file들로 구성되며, zip file로 압축하여 배포한다.
  - Plugin을 개발하는 방식은 2가지가 있다.
    - Stable plugin API를 통해 text analysis plugin을 개발하는 방식(8.7.0부터 지원).
    - Classic plugin API를 통해 custom authentication, autorization, scoring mechanisms 등을 개발하는 방식.



## Text analysis plugin 개발

- Stable plugin API를 사용하여 Text analysis plugin을 개발할 수 있다.

  - Classic plugin으로도 text analysis plugin을 개발할 수는 있다.
    - 그러나 classic plugin은 Elasticsearch의 특정 version에 종속되게 된다.
    - 이는 classic plugin이 변경 가능한  internal API를 가지고 구현하는 것이기 때문이다.
    - 따라서 Elasticsearch를 update할 때 마다 plugin을 recompile해야한다.
  - Stable plugin API로 개발한 plugin은 같은 Elasticsearch major version 내에서 호환이 가능하다.
    - 따라서 major version만 같다면 Elasticsearch를 update했다고 해도 plugin을 recompile할 필요가 없다.
  - Stable plugin API는 아래와 같은 dependency를 가지고 있다.
    - `plugin-api`: Elasticsearch plugin을 구현하기 위해 사용하는 API
    - `plugin-analysis-api`: analysis plugin을 개발하고 이를 Elasticsearch에 통합하기 위해 사용하는 API.
    - `lucene-analysis-common`: `plugin-analysis-api`의 dependency이며, `Tokenizer`, `Analyzer`, `TokenStream` 등 Lucene analysis interface를 포함하고 있다.
  - Text analysis plugin은 anaysis plugin API에 정의된 아래 4개의 factory class를 구현하는 방식으로 개발한다.
    - `AnalyzerFactory`: Lucene analyzer를 생성하기 위한 factory.
    - `CharFilterFactory`: Character filter를 개발하기 위한 factory.
    - `TokenFilterFactory`: Lucene token filter를 개발하기 위한 factory.
    - `TokenizerFactory`: Lucene tokenizer를 개발하기 위한 factory.

  - `@NamedComponent` annotation
    - Stable plugin 구현의 핵심이다.
    - Elasticsearch의 많은 component들은 configuration에서 사용하는 이름이 있다.
    - 예를 들어 keyword analyzer는 configuration에서 `"keyword"`라는 이름으로 참조된다.
    - Custom plugin이 cluster에 설치되면, named component는 configuration에서 이름으로 참조된다.
  - Stable plugin의 file 구조
    - Stable plugin은 JAR file들과 두 개의 metadata로 구성된 ZIP file이다.
    - 두 metadata file은 아래와 같다. 
    - `stable-plugin-descriptor.properties`: plugin에 대해 묘사한 Java properties file.
    - ``named_components.json`: component name들을 key로 구현 class들을 value로 하는 JSON file이다.
    - Plugin의 root에 있는 JAR file들만 plugin의 classpath에 추가된다는 점을 유의해야한다.



- 개발 과정

  - Elasticsearch는 plugin을 보다 쉽게 개발하고 packaging할 수 있도록 `elasticsearch.stable-esplugin`라는 Gradle plugin을 제공한다.
    - 꼭 plugin을 사용해야하는 것은 아니지만, 사용하면 보다 편하게 plugin을 개발할 수 있다.
  - Project를 위한 directory를 생성한다.
  - Project directory에 `build.gradle` 파일을 생성하고 작성한다.
    - 아래는 가장 기본적인 `build.gradle`의 예시이다.
    - `pluginApiVersion`과 `luceneVersion`을 정의해야한다.
    - `esplugin` section을 작성하면, `elasticsearch.stable-esplugin` Gradle plugin이 plugin descriptor file을 자동으로 작성하는데, 만일 해당 plugin을 사용하지 않는다면 수동으로 작성해야한다.

  ```groovy
  apply plugin: 'elasticsearch.stable-esplugin'
  apply plugin: 'elasticsearch.yaml-rest-test'
  
  esplugin {
    name 'stable-analysis-plugin'
    description 'An example analysis plugin using stable plugin api'
  }
  //TODO write module-info
  
  dependencies {
  
    // 아래 3개의 dependency들은 compile-time에만 사용되는데, 이는 runtime에는 Elasticsearch가 이 library들을 제공해주기 때문이다.
    compileOnly "org.elasticsearch.plugin:elasticsearch-plugin-api:${pluginApiVersion}"
    compileOnly "org.elasticsearch.plugin:elasticsearch-plugin-analysis-api:${pluginApiVersion}"
    compileOnly "org.apache.lucene:lucene-analysis-common:${luceneVersion}"
  
    // Test를 위한 dependency도 작성해준다.
    testImplementation "org.elasticsearch.plugin:elasticsearch-plugin-api:${pluginApiVersion}"
    testImplementation "org.elasticsearch.plugin:elasticsearch-plugin-analysis-api:${pluginApiVersion}"
    testImplementation "org.apache.lucene:lucene-analysis-common:${luceneVersion}"
  
    testImplementation ('junit:junit:4.13.2'){
      exclude group: 'org.hamcrest'
    }
    testImplementation 'org.mockito:mockito-core:4.4.0'
    testImplementation 'org.hamcrest:hamcrest:2.2'
  
  }
  ```

  - Analysis plugin API의 interface를 구현하고 `Namedcomponent` annotation을 붙인다.
  - 아래 명령어를 실행하여 plugin을 ZIP file로 생성한다.
    - 결과 file은 `build/distributions`에 생성된다.

  ```bash
  $ gradle bundlePlugin
  ```



- YAML REST test
  - `elasticsearch.yaml-rest-test` Gradle plugin은 Elasticsearch yamlRestTest framework를 사용하여 plugin을 테스트할 수 있게 해준다.
  - Test는 새로 개발한 plugin이 설치된 Elasticsearch cluster에 REST request를 보내고, 응답을 검사하는 방식으로 실행된다.
    - REST request는 YAML format으로 작성한다.
  - YAML REST test의 directory 구조는 아래와 같다.
    - `src/yamlRestTest/java`에 test suit class를 작성하며, 이 class들은 `ESClientYamlSuiteTestCase`를 extend해야한다.
    - `src/yamlRestTest/resources/test`에 YAML test를 작성한다.



- 간단한 plugin 개발해보기

  - foo와 bar를 제외한 모든 token을 제외시키는 Lucene token filter를 개발할 것이다.
    - Elasticsearch version: 8.7.0
    - Lucene version: 9.5.0
    - Java version: 17.0.7
    - Gradle vesion: 7.4
  - 새로운 project를 생성하고 file 구조를 잡는다.

  ```
  ├── src
  │   ├── main/java/org/example
  |   |   ├── FooBarTokenFilter.java
  |   |   └── FooBarTokenFilterFactory.java
  │   └── yamlRestTest
  |       ├── java/org/example/FooBarPluginClientYamlTestSuiteIT.java
  |       └── resources/rest-api-spec/test/plugin/10_token_filter.yml
  └── build.gralde
  ```
  
  - build.gradle file을 아래와 같이 작성한다.
  
  ```groovy
  ext.pluginApiVersion = '8.7.0'
  ext.luceneVersion = '9.5.0.'
  
  buildscript {
    ext.pluginApiVersion = '8.7.0'
    repositories {
      mavenCentral()
    }
    dependencies {
      classpath "org.elasticsearch.gradle:build-tools:${pluginApiVersion}"
    }
  }
  
  // gradle plugin을 적용한다.
  apply plugin: 'elasticsearch.stable-esplugin'
  apply plugin: 'elasticsearch.yaml-rest-test'
  
  esplugin {
    name 'my-first-plugin'
    description 'My first analysis plugin'
  }
  
  group 'org.example'
  version '1.0-SNAPSHOT'
  
  repositories {
    mavenLocal()
    mavenCentral()
  }
  
  dependencies {
  
    compileOnly "org.elasticsearch.plugin:elasticsearch-plugin-api:${pluginApiVersion}"
    compileOnly "org.elasticsearch.plugin:elasticsearch-plugin-analysis-api:${pluginApiVersion}"
    compileOnly "org.apache.lucene:lucene-analysis-common:${luceneVersion}"
  
    testImplementation "org.elasticsearch.plugin:elasticsearch-plugin-api:${pluginApiVersion}"
    testImplementation "org.elasticsearch.plugin:elasticsearch-plugin-analysis-api:${pluginApiVersion}"
    testImplementation "org.apache.lucene:lucene-analysis-common:${luceneVersion}"
  
    testImplementation ('junit:junit:4.13.2'){
      exclude group: 'org.hamcrest'
    }
    testImplementation 'org.mockito:mockito-core:4.4.0'
    testImplementation 'org.hamcrest:hamcrest:2.2'
  
  }
  ```
  
  - `FooBarTokenFilter.java` file을 아래와 같이 작성한다.
  
  ```java
  package org.example;
  
  import org.apache.lucene.analysis.FilteringTokenFilter;
  import org.apache.lucene.analysis.TokenStream;
  import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
  
  import java.util.Arrays;
  
  public class FooBarTokenFilter extends FilteringTokenFilter {
      private final CharTermAttribute term = addAttribute(CharTermAttribute.class);
  
      public FooBarTokenFilter(TokenStream input) {
          super(input);
      }
  
      @Override
      public boolean accept() {
          if (term.length() != 3) return false;
          return Arrays.equals(term.buffer(), 0, 3, "foo".toCharArray(), 0, 3)
                  || Arrays.equals(term.buffer(), 0, 3, "bar".toCharArray(), 0, 3);
      }
  
  }
  ```
  
  - `FooBarTokenFilterFactory.java` file을 아래와 같이 작성한다.
    - `@NamedComponent` annotation을 사용하여 filter의 이름을 설정한다.
  
  ```java
  package org.example;
  
  import org.apache.lucene.analysis.TokenStream;
  import org.elasticsearch.plugin.analysis.TokenFilterFactory;
  import org.elasticsearch.plugin.NamedComponent;
  
  @NamedComponent(value = "foo_bar")
  public class FooBarTokenFilterFactory implements TokenFilterFactory {
  
      @Override
      public TokenStream create(TokenStream tokenStream) {
          return new FooBarTokenFilter(tokenStream);
      }
  
  }
  ```
  
  - `src/test` directory에 test code를 추가한다(optional)
  - 아래 명령어를 실행한다.
    - JAR file을 build하고, metadata file을 생성하며, 이들을 ZIP file로 묶는다.
    - 결과 file은 `build/dstributions`에 생성된다.
  
  ```bash
  $ gradle bundlePlugin
  ```
  
  - Elasticsearch에 plugin을 설치한다.
    - Plugin file이 Elasticsearch가 plugin을 보관하는 `${es_home}/plugins`(Elasticsearch Docker 공식 image 기준 `/usr/share/elasticsearch/plugins`)에 저장되어 있으면 설치 도중 error가 발생한다.
  
  ```bash
  $ elasticsearch-plugin install file:///<path>/<to>/<plugin_file>.zip
  ```
  
  - Plugin이 잘 설치 되었는지 확인.
    - 잘 설치 되었다면 `build.gradle` file의 `version`에 작성한 version 정보와 `esplugin`에 작성한 `name`이 보이게 된다.
  
  ```http
  GET _cat/plugins
  ```
  
  - 사용해보기
  
  ```json
  // GET /_analyze
  {
    "text": "foo bar baz qux",
    "tokenizer": "standard",
    "filter":  ["foo_bar"]
  }
  
  // output
  {
      "tokens": [
          {
              "token": "foo",
              "start_offset": 0,
              "end_offset": 3,
              "type": "<ALPHANUM>",
              "position": 0
          },
          {
              "token": "bar",
              "start_offset": 4,
              "end_offset": 7,
              "type": "<ALPHANUM>",
              "position": 1
          }
      ]
  }
  ```



- YAML REST test

  > 테스트 해봤으나 제대로 실행되지 않는다.
  >
  >  `gradle yamlRestTest` 실행시 gradle에서 unable to find method error가 발생하면서 build가 실패한다.
  >
  > gradle과 jdk 사이의 version이 맞지 않아 발생하는 문제로 추정되는데, 둘의 version을 변경해봐도 계속 실패한다.
  >
  > 추후 다시 시도해볼것.
  
  - `elasticsearch.stable-esplugin` Gradle plugin을 사용한다면, Elasticsearch의 YAML Rest Test framework를 사용할 수 있다.
    - 실행 중인 test 용 cluster에 custom plugin을 load 하여 REST API query를 test해 볼 수 있다.
  - `FooBarPluginClientYamlTestSuiteIT.java` file을 아래와 같이 작성한다.
  
  ```java
  package org.example;
  
  import com.carrotsearch.randomizedtesting.annotations.Name;
  import com.carrotsearch.randomizedtesting.annotations.ParametersFactory;
  import org.elasticsearch.test.rest.yaml.ClientYamlTestCandidate;
  import org.elasticsearch.test.rest.yaml.ESClientYamlSuiteTestCase;
  
  public class FooBarPluginClientYamlTestSuiteIT extends ESClientYamlSuiteTestCase {
  
      public FooBarPluginClientYamlTestSuiteIT(
              @Name("yaml") ClientYamlTestCandidate testCandidate
      ) {
          super(testCandidate);
      }
  
      @ParametersFactory
      public static Iterable<Object[]> parameters() throws Exception {
          return ESClientYamlSuiteTestCase.createParameters();
      }
  }
  ```
  
  - `src/yamlRestTest/resources/rest-api-spec/test/plugin`에  `10_token_filter.yml` file을 아래와 같이 작성한다.
  
  ```yaml
  "foo_bar plugin test - removes all tokens except foo and bar":
    - do:
        indices.analyze:
          body:
            text: foo bar baz qux
            tokenizer: standard
            filter:
              - type: "foo_bar"
    - length: { tokens: 2 }
    - match:  { tokens.0.token: "foo" }
    - match:  { tokens.1.token: "bar" }
  ```
  
  - 아래 명령어를 통해 test를 수행한다.
  
  ```bash
  $ gradle yamlRestTest
  ```





## REST API plugin 개발

- Elasticsearch에 REST endpoint를 추가하는 plugin 개발하기
  - Test analysis plugin과는 달리 class plugin이므로 Elasticsearch version이 변경될 때 마다 plugin도 update해야한다.



- 간단한 REST API plugin 개발하기.

  - 개발 환경
    - Elasticsearch 8.7.0
    - jdk 19.0.2
    - gradle 8.3

  - 프로젝트 구조

  ```
  ├── src
  │   └── main/java/org/example/resthandler
  |       ├── ExampleCatAction.java
  |       └── ExampleRestHandler.java
  └── build.gralde
  ```

  - `build.gradle` file을 아래와 같이 작성한다.

  ```groovy
  buildscript {
      repositories {
          mavenCentral()
      }
      dependencies {
          classpath "org.elasticsearch.gradle:build-tools:8.7.0"
      }
  }
  
  repositories {
      mavenCentral()
  }
  
  version '1.0-SNAPSHOT'
  
  apply plugin: 'elasticsearch.esplugin'
  
  esplugin {
      name 'first-rest-handler'
      description 'My first plugin'
      classname 'org.elasticsearch.example.resthandler.ExampleRestHandlerPlugin'
  }
  ```

  - `ExampleCatAction.java` file을 아래와 같이 작성한다.
    - 주의할 점은 한글로 작성된 주석이 있으면 안되므로, 아래에서 주석은 제거해야한다.

  ```java
  package org.elasticsearch.example.resthandler;
  
  import org.elasticsearch.client.internal.node.NodeClient;
  import org.elasticsearch.common.Table;
  import org.elasticsearch.rest.RestRequest;
  import org.elasticsearch.rest.RestResponse;
  import org.elasticsearch.rest.action.cat.AbstractCatAction;
  import org.elasticsearch.rest.action.cat.RestTable;
  
  import java.util.List;
  
  import static org.elasticsearch.rest.RestRequest.Method.GET;
  import static org.elasticsearch.rest.RestRequest.Method.POST;
  
  public class ExampleCatAction extends AbstractCatAction {
  
      @Override
      public List<Route> routes() {
          // 새로운 route를 등록한다.
          return List.of(
                  new Route(GET, "/_cat/ping"),
                  new Route(POST, "/_cat/ping"));
      }
  
      @Override
      public String getName() {
          return "rest_handler_ping_pong";
      }
  
      @Override
      protected RestChannelConsumer doCatRequest(final RestRequest request, final NodeClient client) {
          // 위에서 등록한 endpoint로 요청을 보낼 시 "pong"이라는 message가 반환되도록 한다.
          final String message = request.param("message", "pong");
  
          Table table = getTableWithHeader(request);
          table.startRow();
          table.addCell(message);
          table.endRow();
          return channel -> {
              try {
                  channel.sendResponse(RestTable.buildResponse(table, channel));
              } catch (final Exception e) {
                  channel.sendResponse(new RestResponse(channel, e));
              }
          };
      }
  
      @Override
      protected void documentation(StringBuilder sb) {
          sb.append(documentation());
      }
  
      public static String documentation() {
          return "/_cat/ping\n";
      }
  
      @Override
      protected Table getTableWithHeader(RestRequest request) {
          final Table table = new Table();
          table.startHeaders();
          table.addCell("test", "desc:test");
          table.endHeaders();
          return table;
      }
  }
  ```

  - `ExampleRestHandler.java` file을 아래와 같이 작성한다.
    - `ExampleRestHandlerPlugin`은 `ActionPlugin` interface를 구현한다.
    - `getRestHandlers()` method를 override한다. 

  ```java
  package org.elasticsearch.example.resthandler;
  
  import org.elasticsearch.cluster.metadata.IndexNameExpressionResolver;
  import org.elasticsearch.cluster.node.DiscoveryNodes;
  import org.elasticsearch.common.settings.ClusterSettings;
  import org.elasticsearch.common.settings.IndexScopedSettings;
  import org.elasticsearch.common.settings.Settings;
  import org.elasticsearch.common.settings.SettingsFilter;
  import org.elasticsearch.plugins.ActionPlugin;
  import org.elasticsearch.plugins.Plugin;
  import org.elasticsearch.rest.RestController;
  import org.elasticsearch.rest.RestHandler;
  
  import java.util.List;
  import java.util.function.Supplier;
  
  import static java.util.Collections.singletonList;
  
  public class ExampleRestHandlerPlugin extends Plugin implements ActionPlugin {
  
      @Override
      public List<RestHandler> getRestHandlers(final Settings settings,
                                               final RestController restController,
                                               final ClusterSettings clusterSettings,
                                               final IndexScopedSettings indexScopedSettings,
                                               final SettingsFilter settingsFilter,
                                               final IndexNameExpressionResolver indexNameExpressionResolver,
                                               final Supplier<DiscoveryNodes> nodesInCluster) {
  
          return singletonList(new ExampleCatAction());
      }
  }
  ```

  - 아래 명령어를 통해 plugin을 build한다.

  ```bash
  $ gradle bundlePlugin
  ```

  - Elasticsearch에 plugin을 설치한다.

  ```bash
  $ elasticsearch-plugin install file:///<path>/<to>/<plugin_file>.zip
  ```

  - Plugin이 잘 설치 되었는지 확인한다.

  ```http
  GET _cat/plugins
  ```

  - Plugin을 실행해본다.

  ```http
  GET _cat/ping
  ```

