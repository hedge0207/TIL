# Index File Formats

> https://lucene.apache.org/core/9_10_0/core/org/apache/lucene/codecs/lucene99/package-summary.html#package.description

- Lucene의 index에는 아래와 같은 것들이 저장된다.

  - Segment Info
    - Segement에 대한 metadata를 저장한다.
    - 문서의 개수, 사용되는 파일, segment가 저장된 방식 등이 저장되어 있다.
  - Field names
    - Index에서 사용하는 field들이 metadata가 저장되어 있다.
  - Stored Field values
    - 각 문서에 대한 field name-value 쌍의 목록이 저장되어 있다.
    - 저장된 쌍들은 검색시에 결과로 반환된다.
  - Term dictionary
    - 색인된 문서에 있는 term들에 대한 정보를 저장한다.
    - 각 Term을 가지고 있는 document의 개수와 term의 frequency 등에 대한 정보도 저장되어 있다.
  - Term Frequency data
    - Term dictionary에 있는 각각의 term을 포함하고 있는 document의 개수나 document 내에서 term이 등장하는 빈도 등이 저장된다.
  - Term Proximity data
    - Term dictionary에 있는 각각의 term이 document 내에서 어느 위치에 있는지를 저장한다.
  - Normalization factors
    - Document 내부의 각 field에 대해 검색시에 부여되는 가중치가 저장되어 있다.
  - Term Vectors
    - Document 내부의 각 field에 대해 term vector(==document vector)가 저장되어 있다.
    - Term vector는 term text와 term frequency로 구성된다.
  - Per-document values
    - Stored value와 유사하지만, per-document values의 경우 빠른 접근을 위해 main memory에 load된다.
    - Stored value는 일반적으로 검색 결과를 요약하기 위해 사용되지만, per-document values는 scoring에 사용된다.
  - Live documents
    - 어떤 document가 삭제되지 않고 남아있는지를 저장한다.

  - Point values
    - 큰 숫자 값(BigInteger, BigDecimal)이나 지리적 데이터를 다루기 위해 여러 차원으로 색인된 field을 저장한다.
  - Vector values
    - 고차원의 최근접 이웃 검색을 위해 random access와 연산에 최적화 된 vector 값들을 저장한다.



- Lucene에서 사용하는 파일들

  - 만약 Compound File format을 사용하면 아래 file들을 다 사용하지는 않고, 아래 파일들이 하나의 `.cfs` 파일로 합쳐진다.
  - Compound File format을 사용하더라도 Segment info file, Lock file, Deleted documents file등은 합쳐지지 않는다.

  | Name                | Extension              | Description                                                  |
  | ------------------- | ---------------------- | ------------------------------------------------------------ |
  | Segments File       | segments_N             | Commit point에 대한 정보를 저장한다.                         |
  | Lock File           | write.lock             | 여러 IndexWriter가 같은 파일에 쓰는 것을 방지하기 위한 lock file이다. |
  | Segment Info        | .si                    | Segment에 대한 metadata를 저장한다.                          |
  | Compound Fike       | .cfs, .cfe             | 다른 모든 index file들을 합쳐서 만드는 파일이다.             |
  | Fields              | .fnm                   | Field들에 대한 정보를 저장한다.                              |
  | Field Index         | .fdx                   | Field data에 대한 pointer를 저장한다.                        |
  | Field data          | .fdt                   | Stored field를 저장한다.                                     |
  | Term Dictionary     | .tim                   | Term dictionary를 저장한다.                                  |
  | Term index          | .tip                   | Term dictionary의 색인을 저장한다.                           |
  | Frequencies         | .doc                   | Term이 등장하는 document들의 목록을 frequency와 함께 저장한다. |
  | Positions           | .pos                   | Term이 index의 어느 위치에 등장하는지에 대한 정보를 저장한다. |
  | Payloads            | .pay                   | 추가적인 per-position metadata를 저장한다.                   |
  | Norms               | .nvd, .nvm             | Documents와 fields에 대한 길이 정보와 boost factor를 인코딩하여 저장한다. |
  | Per-document Values | .dvd, .dvm             | 추가적인 scoring factor와 per-document 정보를 인코딩하여 저장한다. |
  | Term Vector Index   | .tvx                   | Offset을 저장한다.                                           |
  | Term Vector Data    | .tvd                   | Term vector를 저장한다.                                      |
  | Live Documents      | .liv                   | 각 문서들의 삭제 여부를 저장한다.                            |
  | Point values        | .dii, dim              | 색인된 point들을 저장한다.                                   |
  | Vector values       | .vec, .vem, .veq, .vex | 색인된 vector 정보를 저장한다.                               |



- Lucene 색인 파일 생성해보기

  - 아래 코드를 실행한다.
    - Lucene에서는 `IndexWriter`를 사용하여 문서를 색인한다.
    - 문서를 색인한 후에 `commit`을 해준다.

  ```java
  package org.apache.lucene;
  
  import org.apache.lucene.document.Document;
  import org.apache.lucene.document.Field;
  import org.apache.lucene.document.StringField;
  import org.apache.lucene.document.TextField;
  import org.apache.lucene.index.*;
  import org.apache.lucene.search.*;
  import org.apache.lucene.store.Directory;
  import org.apache.lucene.store.NIOFSDirectory;
  
  import java.io.IOException;
  import java.nio.file.Paths;
  
  public class MyTest {
      public static void main(String[] args) throws IOException {
          String index_dir = "/path/to/create/index/files";
          Directory index = new NIOFSDirectory(Paths.get(index_dir));
          IndexWriterConfig config = new IndexWriterConfig();
          IndexWriter writer = new IndexWriter(index, config);
  
          // create a document
          Document doc = new Document();
          doc.add(new TextField("title", "Lucene - IndexWriter", Field.Store.YES));
          doc.add(new StringField("author", "aliyun", Field.Store.YES));
  
          //index a document
          writer.addDocument(doc);
          writer.commit();
      }
  }
  ```

  - 설정한 경로에 아래 파일들이 생성된다.
    - `.cfs`, `.cfe`, `.si`, `segments_`, `write.lock`
    - Segment의 크기가 작을 경우 Compound File format이 기본값이므로 `.cfs`, `.cfe` 파일이 생성된다.