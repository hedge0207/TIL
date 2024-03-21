#  유용한 사이트

- https://caniuse.com/: 각종 기능을 어떤 웹 브라우저에서 사용 가능한지 보여주는 사이트



- koreanjson.com: dummy 데이터를 제공



- https://jsonplaceholder.typicode.com/ : koreanjson보다 더 많은 데이터를 제공
  - Resource에서 원하는 것을 클릭 후 URL을 복사해서 사용
  - https://github.com/typicode/json-server에 가면 pagination 관련 코드가 있다.



- https://github.com/stutrek/scrollMonitor : 무한스크롤 구현을 도와준다.
  - https://cdnjs.com/libraries/scrollmonitor : cdn 주소



- picsum.photos: 랜덤 이미지를 보여주는 사이트



- https://www.favicon-generator.org/: favicon을 생성해주는 사이트



- https://dog.ceo/api/breeds/image/random:랜덤한 강아지 이미지를 보여주는 API



- https://api.thecatapi.com/v1/images/search: 랜덤한 고양이 이미지를 보여주는 API



- Pantone Color: 올해의 색을 알려주는 사이트



- google font: HTML,CSS에 적용 가능한 폰트 제공



- animate.css: css로 구현한 각종 애니메이션 효과



- https://fontawesome.com/: 각종 아이콘과 이미지가 있는 사이트



- gtthub-pages: repositroy명을 유저명.github.io로 생성하면 된다.
  - jekyll 참고할만한 사이트
  - gatsby 참고할만한 사이트



- Octotree: 깃헙을 볼 때 편리한 chrome app



- gravatar



- 복사 금지된 글을 복사하는 방법:  F12-우측 상단 .3개 수직으로 있는 버튼 클릭-settings-Enable JavaScript source maps 체크 해제



- https://react-icons.github.io/react-icons/icons?name=md : react에서 사용 가능한 icon들을 모아 놓은 사이트





# Jupyter Notebook 

- 설치

  - cmd 창에 아래 명령어 입력

  ```bash
  $ pip install jupyter
  ```

  - 이후 실행하려는 폴더에서 cmd창을 열고 아래 명령어를 입력

  ```bash
  $ jupyter notebook
  ```

  

- 사용

  - cell 실행
    - ctrl+enter: 해당 cell을 실행
    - shift+enter: 해당 cell을 실행하고 새로운 cell을 생성
  - cmd 창에 입력할 내용을 jupyter에 입력하고자 한다면 명령어 맨 앞에 `!`를 붙이면 된다.

  ```python
  ! pip install bs4
  ```







# 초기화시 해야 할 것들

## 환경변수

- 환경변수: 운영체제가 참조하는 변수, 변수를 프로그램이 실행되는 환경에 저장하여 해당 시스템의 모든 프로그램들이 사용할 수 있게 하는 변수.



- Path
  - 환경 변수의 하나로 운영체제가 어떤 프로세스를 실행시킬 때, 그 경로를 찾는데 이용된다. Path를 등록해놓으면 해당 파일을 어떤 경로에서든 사용 가능하게 된다.
  - 예시
    - `C:\Users\사용자명\Desktop\a\b` 경로에 `Hello.txt` 파일 생성
    - cmd창 실행 후 `C:\Users\사용자명\Desktop\a\b`이 아닌 곳에서 `Hello.txt`를 입력하면 "'hello.txt'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다."라는 메세지가 출력된다.
    - 환경 변수(사용자 변수나 시스템 변수 중 아무 곳에서나)의 Path에 `C:\Users\사용자명\Desktop\a\b`를 추가.
    - 이후 다시 cmd창을 열고  `Hello.txt`를 입력하면 Hello.txt 파일이 실행되는 것을 확인 가능하다.

<br/>

<br/>

<br/>

<br/>

## Python 설치하기

> https://www.python.org/

- 위 사이트에서 파이썬 설치 파일 다운로드하기
  - 버전 선택 후 OS에 따라 맞는 설치 파일을 다운로드 하면 된다.
  - 윈도우의 경우 `Windows x86-64 executable installer`를 선택



- 설치하기
  - `Add Python X.X to Path` 체크한 후 설치
  - 위 설정은 환경변수에 파이썬을 추가하는 것이다.



- 실행하기
  - cmd 창에 `python`을 입력했을 때 버전 정보가 뜨면 제대로 설치된 것이다.
  - 안될 경우 컴퓨터를 다시 시작하거나 `Add Python X.X to Path` 를 체크했는지 확인 후 체크하지 않았다면 체크 후 재설치한다.

<br/>

<br/>

<br/>

<br/>

## Java 설치하기

> https://www.oracle.com/java/technologies/javase-downloads.html

- 위 사이트에서 버전과 운영체제 선택 후 설치 파일 다운로드



- cmd 창에 `javac -version` 입력 후 버전이 제대로 뜨면 잘 설치 된 것이다.



- 환경 변수 설정이 필요한 경우
  - 시스템 변수에서 새로 만들기 클릭 
    - 변수이름: `JAVA_HOME`
    - 변수 값: jdk 설치 경로(기본값은 `C:\Program Files\Java\jdk-11.0.9)`
  - 시스템 변수의 Path에 `%JAVA_HOME%bin` 추가

<br/>

<br/>

<br/>

<br/>

## IDE 설치하기

### VSCode 설치

> https://code.visualstudio.com/

- 위 사이트에서 VS Code 설치 파일 다운로드 후 설치하기
  - 파일 탐색기에서 vscode로 열기 체크 후 설치하는 것이 편하다.

<br/>

- 설치 완료 후 Extensions에서 설치할 것들
  - python
  - open in browser: 웹 개발 시 브라우저로 바로 열어볼 수 있도록 해준다.
  - Live server: 소스코드를 수정할 때마다 수정 사항을 자동으로 반영해준다.
  - Vetur: Vue.js 사용시 Vue 코드를 하이라이팅 해준다.
  - Code Runner:  JS파일을 웹이 아닌 VSCode로 실행해준다.

<br/>



- VScode extension 중 `remote-ssh`가 `downloading vs code server locally...`에서 막힌 경우 해결 방법

  - `remote-ssh` extension은 원격 서버의 `~/.vscode-server/bin/<commit_id>` 폴더에 원격 연결에 필요한 파일들을 다운 받는다.
  - 만일 원격 서버의 network가 막혀 있다면 다운 받을 수 없어 지속적으로 error가 발생하게 된다.
  - 따라서 이 경우 network 연결이 가능한 환경에서 필요한 파일을 download 후 해당 파일을 위 경로에 옮겨줘야 한다.
  - 아래 명령어로 다운 받는다.

  ```bash
  $ curl -sSL "https://update.code.visualstudio.com/latest/server-linux-x64/stable" -o vscode-server-linux-x64.tar.gz
  ```

  - 다운 받은 후 위 파일을 원격 서버의 `~/.vscode-server/bin/<commit_id>` 폴더로 옮긴 후 압축을 푼다.
    - 압축 폴더는 제외하고 압축 폴더 내부의 파일이 `~/.vscode-server/bin/<commit_id>` 경로에 위치해야 한다.

<br/>

<br/>

### PyCham 설치

> https://www.jetbrains.com/ko-kr/

- Pycham 설치 파일 다운로드 및 설치

<br/>

- 실행시 파이썬 콘솔창과 함께 실행되는데 이를 막기 위해서는 다음과 같이 하면 된다.
  - 코드 창 우클릭
  - Modify run configuration 클릭
  - Execution에서 Run with Python Console 체크 해제

<br/>

<br/>

### IntelliJ 설치

> https://www.jetbrains.com/ko-kr/

- IntelliJ 설치 파일 다운로드 및 설치



- 실행시 자동으로 현재 설치된 jdk 파일을 찾아서 등록한다.

<br/>

<br/>

<br/>

<br/>

# 단축키

## IntelliJ

- 배열등이 있을 때 `iter`을 입력하면 for문을 자동 완성해준다.



- soutv: 출력할 변수명과 "변수명 = "을 함께 완성해준다.



- soutm: 메소드명을 출력문과 함께 완성해준다.



- ctrl+shift+enter: 바로 다음 줄로 넘어가기



- 클래스명 드래그 후 ctrl+shift+T를 누르면 해당 클래스의 테스트 파일을 생성 가능하다. 