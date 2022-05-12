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
    - 기본 사용자인 elasticsearch로는 /usr/share/elasticsearch/modules에 폴더 생성이 불가능하므로 root 사용자로 변경한다.

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
  $ curl -XGET -H 'Content-Type:application/json' localhost:9200/_configsync/file?path=<file_path>
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

  

  

