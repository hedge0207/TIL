# Lombok

- lombok: 자바 컴파일 시점에서 특정 어노테이션으로 해당 코드를 추가할 수 있는 라이브러리



- 사용법(IntelliJ, gradle 기준)

  - Lombok Plugin 설정 
    - File-Settings-Plugins에서 Lombok Plugin 설치
    - IntelliJ 재실행

  - Enable annotation 설정

    - File-Settings-Build, Execution, Deployment-Compiler-Annotation Processings
    - Enable annotation processing 체크

  - `build.gradle`에 `dependencies` 작성

    ```java
    provided group: 'org.projectlombok', name: 'lombok', version: '1.18.12'
    ```

  - 사용할 entitiy에 아래  annotation 중 필요한 것들 작성

    - `@NonNull`
    - `@Data`: 아래 5개를 모두 포함한 어노테이션, @Data는 사용을 지양하는 것이 좋다.
    - `@ToString`: class에 있는 필드들을 검사해서 문자열로 변환해주는 toString() 메소드를 생성.
    - `@EqualsAndHashCode`: 객체 비교 등의 용도로 사용되는 equals(), hashCode() 메소드의 코드를 생성, `exclude={}`를 통해 특정 필드 제외 가능
    - `@Getter`: Getter 메서드를 생성해준다.
    - `@Setter`: Setter 메서드를 생성해준다. 남용을 지양해야 한다.
    - `@RequiredArgsConstructor`
    - 예시

    ```java
    package com.web.backend.model.question;
    
    import lombok.Getter;
    import lombok.NoArgsConstructor;
    import lombok.Setter;
    
    @Entity
    @NoArgsConstructor
    @Getter
    @Setter
    public class Question {
    
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        @Column(name="question_id")
        private int questionId;
    }
    ```

    



# JPA

## getOne, findOne의 차이

- getOne: Lazy Evalueation을 적용하기 위해 참조만 리턴, 해당 엔티티가 없을 경우 EntityNotFoundException이 발생.
  - Lazy Evaluation: A가 B를 필드로 가지고 있을 때, B의 모든 엔티티가 당장 필요한 것이 아니라 A엔티티를 반환하기 위해 참조만 필요한 경우에 적용된다.
- findOne: db에 접근해서 해당 엔티티를 찾음, 없을 경우에 null을 반환



## JPA-Hibernate에서 db 자동 생성 방법

- `application.properties`파일에서 아래 두 속성값을 변경하여 서버를 실행할 때 마다 db를 자동으로 생성, 수정, 삭제 할 수 있다.

  - `spring.jpa.generate-ddl`: true로 설정 시 `@Entitiy`가 명시된 클래스를 찾아 ddl을 생성한다.

  - `spring.jpa.hiberante.ddl-auto`

    - none: 자동 생성 하지 않음
    - create: 항상 다시 생성
    - create-drop: 시작 시 생성 후 종료 시 제거
    - update: 시작 시 Entity 클래스와 DB 스키마 구조를 비교해 DB 쪽에 생성되지 않은 테이블, 컬럼 추가 (제거는 하지 않음)
    - validate: 시작 시 Entity 클래스와 DB 스키마 구조를 비교해서 같은지만 확인 (다르면 예외 발생)

    - create나 create-drop으로 설정 시 classpath 경로의 import.sql 파일이 있으면 파일 내의 query들을 hibernate가 자동으로 실행(spring boot와는 관계 없음)

  ​	



# 기타

- `build.gradle`의 `dependencies`에 작성한 `implementation`은 일단 작성 후 설치가 되면 해당 코드를 다시 삭제해도 실행이 된다.

  ```java
  //전략
  
  dependencies {
  	//...
      //아래와 같이 작성 후 설치가 완료되었다면 아래 코드를 삭제하거나 주석처리해도 해당 라이브러리를 그대로 사용이 가능하다.
  	implementation 'org.springframework.boot:spring-boot-starter-security'
  	//...
  }
  //후략
  ```

  





- `@NotNull`, `@NotEmpty`, `@NotBlank`의 차이
  - `@NotNull`: null만 허용하지 않음, ""(초기화된 문자열), " "(공백)은 허용
    - 모든 타입에 적용 가능
  -  `@NotEmpty`: null, "" 허용하지 않음, " "은 허용
    - CharSequence(문자 자료형들)
    - Collection
    - Map
    - Array
    - 위 타입에만 적용 가능
    - boolean은 적용 불가
  - `@NotBlank`: null, "", " "모두 허용하지 않음
    - CharSequence에만 적용 가능