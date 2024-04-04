- Iceberg Docker로 실행하기

  - 아래와 같이 docker-compose 파일을 작성한다.

  ```yaml
  version: "3"
  
  x-minio-common: &minio-common
    image: minio/minio:latest
    command: server --console-address ":9001" http://minio{1...2}/data{1...2}
    environment:
      MINIO_ROOT_USER: "foo"
      MINIO_ROOT_PASSWORD: "foo_auth"
      MINIO_STORAGE_CLASS_STANDARD: "EC:1"
      MINIO_DOMAIN: "minio"
    restart: always
  
  services:
    spark-iceberg:
      image: tabulario/spark-iceberg
      container_name: spark-iceberg
      depends_on:
        - rest
      environment:
        - AWS_ACCESS_KEY_ID=foo
        - AWS_SECRET_ACCESS_KEY=foo_auth
        - AWS_REGION=us-east-1
      ports:
        - 8888:8888
        - 8080:8080
        - 10000:10000
        - 10001:10001
      networks:
        iceberg_net:
    
    rest:
      image: tabulario/iceberg-rest
      container_name: iceberg-rest
      ports:
        - 8181:8181
      environment:
        - AWS_ACCESS_KEY_ID=foo
        - AWS_SECRET_ACCESS_KEY=foo_auth
        - AWS_REGION=us-east-1
        - CATALOG_WAREHOUSE=s3://test
        - CATALOG_IO__IMPL=org.apache.iceberg.aws.s3.S3FileIO
        # 아직 원인은 모르겠지만 CATALOG_S3_ENDPOINT 값을 container network의 내부 주소로 설정하면 동작하지 않는다.
        # 즉 http://minio1:9000과 같이 설정하면 동작하지 않는다.
        - CATALOG_S3_ENDPOINT=http://<host_ip>:9020
      networks:
        iceberg_net:
  
    minio1:
      <<: *minio-common
      container_name: minio1
      networks:
        iceberg_net:
          aliases:
            - test.minio
      ports:
        - 9020:9000
        - 9021:9001
  
    minio2:
      <<: *minio-common
      container_name: minio2
      networks:
        iceberg_net:
      ports:
        - 9030:9000
        - 9031:9001
  
  networks:
    iceberg_net:
  ```

  - Container를 실행한다.

  ```bash
  $ docker compose up
  ```

  - MinIO console로 접속해서 bucket을 생성한다.
    - 주의할 점은 bucket의 이름을 `CATALOG_WAREHOUSE`에 설정한 값(예시의 경우 `test`)과 동일하게 설정해줘야 한다는 점이다.
    - Bucket 이름과 `CATALOG_WAREHOUSE`에 설정한 경로, 그리고 `minio1` container의 `networks.iceberg_net.aliases`의 값(예시의 경우 `test.minio`)의 `.` 앞에 오는 값(예시의 경우 `test`)는 동일해야한다.
    - 그리고, `networks.iceberg_net.aliases`의 값 중 `.` 뒤에 오는 값은 `MINIO_DOMAIN`의 값과 같아야한다.
  - MinIO console에서 생성한 bucket을 클릭 후 `Access Policy`를 public으로 변경한다.



- 테스트 해보기

  - `spark-iceberg` container에서 `spark-sql`을 실행한다.

  ```bash
  $ docker exec -it spark-iceberg spark-sql
  ```

  - Table 생성

  ```sql
  CREATE TABLE prod.db.sample (
      id bigint NOT NULL COMMENT 'unique id',
      data string)
  USING iceberg;
  ```

  - Data 삽입

  ```sql
  INSERT INTO prod.db.sample
  VALUES (1, "Hello World!")
  ```

