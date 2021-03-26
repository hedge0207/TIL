# Dockerfile

- Dockerfile
  - Docker 상에서 작동시킬 컨테이너의 구성 정보를 기술하기 위한 파일.
  - Dockerfile로 Docker 이미지를 생성하면 Dockerfile에 작성된 구성 정보가 담긴 이미지가 생성된다.



- Dockerfile의 기본 구분

  - Dockerfile은 텍스트 형식의 파일로, 에디터 등을 사용하여 작성한다.
  - Dockerfile 이외의 파일명으로도 동작하며, 확장자는 필요 없다.
  - 주석은 #을 사용하여 작성한다.
  - 명령어
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
    - 다이제스트는 Docker Hub에 업로드하면 이미지에 자동으로 부여되는 식별자를 의미한다.
    - `docker image ls --digests ` 명령어를 통해 확인이 가능하다.

  ```bash
  # 기본형
  FROM 이미지명
  # 태그를 생략할 경우 자동으로 latest 버전이 적용된다.
  FROM 이미지명:태그명
  # 다이제스트 사용
  FROM 이미지명@다이제스트
  ```



- Dockerfile의 빌드와 이미지 레이어

  - Docker 이미지 만들기

  ```bash
  $ docker build -t [생성할 이미지명]:[태그명] [Dockerfile의 위치]
  ```

  





