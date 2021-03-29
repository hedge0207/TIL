# Dockerfile

- Dockerfile
  - Docker 상에서 작동시킬 컨테이너의 구성 정보를 기술하기 위한 파일.
  - Dockerfile로 Docker 이미지를 생성하면 Dockerfile에 작성된 구성 정보가 담긴 이미지가 생성된다.



- Dockerfile의 기본 구문

  - Dockerfile은 텍스트 형식의 파일로, 에디터 등을 사용하여 작성한다.
  - Dockerfile 이외의 파일명으로도 동작하며, 확장자는 필요 없다.
  - 주석은 `#`을 사용하여 작성한다.
  - 주요 명령어
    - 소문자로 작성해도 동작하지만 관례적으로 대문자로 통일하여 사용한다.

  | 명령       | 설명               |      | 명령       | 설명                       |
  | ---------- | ------------------ | ---- | ---------- | -------------------------- |
  | FROM(필수) | 베이스 이미지 지정 |      | VOLUEM     | 볼륨 마운트                |
  | RUN        | 명령 실행          |      | USER       | 사용자 지정                |
  | CMD        | 컨테이너 실행      |      | WORKDIR    | 작업 디렉토리              |
  | LABEL      | 라벨 설정          |      | ARG        | Dockerfile 내의 변수       |
  | EXPOSE     | 포트 익스포트      |      | ONBUILD    | 빌드 완료 후 실행되는 명령 |
  | ENV        | 환경변수           |      | STOPSIGNAL | 시스템 콜 시그널 설정      |
  | ADD        | 파일/디렉토리 추가 |      | HEATHCHECK | 컨테이너의 헬스 체크       |
  | COPY       | 파일 복사          |      | SHELL      | 기본 쉘 설정               |
  | ENTRYPOINT | 컨테이너 실행 명령 |      |            |                            |




- FROM 명령어

  - Docker 컨테이너를 어떤 이미지로부터 생성할지 정의한다.
  - 다이제스트는 Docker Hub에 업로드하면 이미지에 자동으로 부여되는 식별자를 의미한다.
    - `docker image ls --digests ` 명령어를 통해 확인이 가능하다.

  ```dockerfile
  # 기본형
  FROM 이미지명
  # 태그를 생략할 경우 자동으로 latest 버전이 적용된다.
  FROM 이미지명:태그명
  # 다이제스트 사용
  FROM 이미지명@다이제스트
  ```



- ENV 명령어

  - Dockerfile 안에서 환경변수를 설정하고 싶을 때는 ENV 명령을 사용한다.
  - `key value`형으로 지정
    - 단일 환경변수에 하나의 값을 지정한다.
    - 첫 번째 공백 앞을 key로 설정하면 그 이후는 모두 문자열로 취급한다.
  - `key=value`로 지정
    - 한 번에 여러 개의 값을 설정할 때 사용한다.

  ```dockerfile
  ENV [key] [value]
  ENV [key]=[value]
  ```



- ARG 명령

  - Dockerfile 안에서 사용할 변수를 정의할 때 사용한다.

  - ENV로 생성한 환경변수와 달리  Dockerfile 내에서만 사용이 가능하다.

  ```dockerfile
  ARG <변수명>[=기본값]
  ```



-  ADD 명령

  - 이미지에 호스트 상의 파일 및 디렉토리를 추가할 때 사용한다.

  ```dockerfile
  ADD <호스트의 파일 경로> <Docker 이미지의 파일 경로>
  ```



- COPY 명령

  - 이미지에 호스트상의 파일이나 디렉토리를 복사할 때 사용한다.

  ```dockerfile
  COPY <호스트의 파일 경로> <Docker 이미지의 파일 경로>
  ```



- WORKDIR 명령
  -  dockerfile에서 정의한 명령을 실행하기 위한 작업용 디렉토리를 지정할 때 사용한다.
    -  RUN, CMD, ADD, ENTRYPOINT, COPY 등의 명령을 실행하기 위한 적업용 디렉토리를 지정한다.
    - 지정한 디렉토리가 존재하지 않으면 새로 작성한다.



- RUN 명령어

  - FROM 명령에서 지정한 베이스 이미지에 대해 애플리케이션/미들웨어를 설치 및 설정하거나 환경 구축을 위한 명령을 실행할 떄 사용한다.
  - Shell 형식으로 기술
    - 명령의 지정을 쉘에서 실행하는 방식으로 기술하는 방법.

  ```dockerfile
  # elasticsearch에 노리 형태소 분석기를 설치하는 예시
  RUN bin/elsticsearch-plugin install analysis-nori
  ```

  - Exec 형식으로 기술
    - Shell  형식으로 명령을 기술하면 /bin/sh에서 실행되지만, Exec 형식으로 기술하면 쉘을 경유하지 않고 직접 실행한다.
    - 따라서 명령 인수에 환경변수를 지정할 수 없다.
    - 실행하고 싶은 명령을  JSON  배열로 지정한다.

  ```dockerfile
  # elasticsearch에 노리 형태소 분석기를 설치하는 예시
  RUN ["bin/elasitcsearch-plugin", "-c", "install analysis-nori"]
  ```



- CMD 명령어
  - RUN 명령은 이미지를 작성하기 위해 실행하는 명령을 기술하는 반면 CMD 명령은 이미지를 바탕으로 생성된 컨테이너 안에서 실행할 명령을 기술한다.
  - 하나의  CMD 명령만을 기술할 수 있으며 복수의 명령을 작성하면 마지막 명령만 적용된다.
  - Exec  형식으로 기술
    - RUN 명령의 구문과 동일하다.
  - Shell  형식으로 기술
    - RUN 명령의 구문과 동일하다.
  - ENTRYPOINT 명령의 파라미터로 기술
    - ENTRYPOINT 명령의 인수로 CMD 명령을 사용할 수 있다.



- ENTRYPOINT 명령어
  - 데몬 실행
  - ENTRYPOINT 명령에서 지정한 명령은 `docker run` 명령을 실행했을 때 실행된다.
  - Exec  형식으로 기술
    - RUN 명령의 구문과 동일하다.
  - Shell  형식으로 기술
    - RUN 명령의 구문과 동일하다
  - CMD  명령과의 차이
    - `docker run` 명령 실행 시의 동작에 차이가 있다.
    -  CMD 명령의 경우는 컨테이너 시작 시에 실행하고 싶은 명령을 정의해도 `docker run` 명령 실행 시에 인수로 새로운 명령을 지정한 경우 이것을 우선 실행한다.
    - 반면 ENTRYPOINT 에서 지정한 명령은 반드시 컨테이너에서 실행되는데, 실행 시에 명령 인수를 지정하고 싶을 때는 CMD 명령과 조합하여 사용한다.
    - ENTRYPOINT 명령으로는 실행하고 싶은 명령 자체를 지정하고 CMD 명령으로는 그 명령의 인수를 지정하면, 컨테이너를 실행했을 때의 기본 작동을 결정할 수 있다.



- ONBUILD 명령
  - 빌드 완료 후, 다음 빌드에서 실행할 명령을 이미지 안에 설정하기 위한 명령이다.
    - ONBUILD 명령이 포함된 이미지를 빌드한다.
    - 빌드된 이미지를 베이스 이미지로 하여 다른 이미지를 빌드한다.
    - 이 때 ONBUILD에서 지정한 명령을 실행한다.



- Dockerfile의 빌드와 이미지 레이어 구조

  - Docker 이미지 만들기

  ```bash
  $ docker build -t [생성할 이미지명]:[태그명] [Dockerfile의 위치]
  ```

  - 이미지 레이어 구조
    - Dockerfile을 빌드하여 Docker 이미지를 작성하면 Dockerfile의 명령별로 이미지를 작성한다.
    - 작성된 여러 개의 이미지는 레이어 구조로 되어 있다.
    - 즉 이전 명령으로 생성된 이미지 파일 위에 다음 명령으로 생성된 이미지가 덮이는 형식이다.



- 멀티스테이지 빌드
  - 제품 환경에 필요한 것들만 빌드하기
    - 애플리케이션 개발 시에 개발 환경에서 사용한 라이브러리나 개발 지원 툴 등이 제품 환경에서 모두 사용되는 것은 아니다.
    - 제품 환경에서는 애플리케이션을 실행하기 위한 최소한의 실행 모듈만 배치하는 것이 리소스 관리나 보안 관점에서 볼 때 바람직하다.
  - Docker 파일 작성하기
    - Dockerfile 을 작성할 때 개발용과 제품용 2가지 이미지를 생성하도록 작성한다.
    - 예시는 p.165 참고





# Docker Compose

- Docker Compose
  - 여러 개의 Docker 컨테이너를 모아서 관리하기 위한 툴



