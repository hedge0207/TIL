# 가상환경

- pyenv

  - python 버전 관리 툴이다.
  - 다양한 버전의 python으로 쉽게 전환할 수 있게 해준다.
  - windows에서는 사용이 불가능하다.
    - 사용 가능하게 만들어주는 패키지가 있지만 아직 불안정하다.
  - 설치하기

  ```bash
  $ curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
  ```

  - pyenv 환경변수 설정

  ```bash
  $ vi ~/.bashrc
  
  # 맨 아래에 아래 내용 추가
  export PATH="~/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  ```

  - pyenv 필수 패키지 설치
    - 이 작업을 건너뛰고 그냥 사용할 경우 오류가 날 수 있다.

  ```bash
  $ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev
  ```



- 가상환경 생성 방법1. venv 사용하기

  - 생성하기
    - 이 명령을 실행한 경로에 `가상환경 이름`에 해당하는 디렉터리가 생성된다.

  ```bash
  $ python -m venv <가상환경 이름>
  ```

  - 가상환경 활성화 하기

  ```bash
  # 윈도우
  $ source <가상환경 이름>/Scripts/activate
  
  # 리눅스, MacOS
  $ source <가상환경 이름>/bin/activate
  ```

  - 비활성화 하기

  ```bash
  $ deactivate
  ```



- 가상환경 생성 방법2. virtualenv 사용하기

  - virtualenv 모듈 설치

  ```bash
  $ pip install virtualenv
  ```

  - 가상환경 생성하기
    - 역시 명령어를 실행한 디렉토리에 `가상환경 이름`에 해당하는 디렉터리가 생성된다.

  ```bash
  $ virtualenv <가상환경 이름>
  ```

  - 활성화 하기

  ```bash
  # 윈도우
  $ source <가상환경 이름>/Scripts/activate
  
  # 리눅스, MacOS
  $ <가상환경 이름>/bin/activate
  ```

  - 비활성화 하기

  ```bash
  $ deactivate
  ```



- 가상환경 생성 방법3. conda 사용하기

  > 아래 사이트에 들어가서 설치 파일을 다운로드 한다.
  >
  > https://www.anaconda.com/products/individual

  - 리눅스에서 anaconda 설치파일 다운
    - 위 사이트로 들어가 리눅스 설치 경로를 복사해서 아래와 같이 입력

  ```bash
  $ wget <설치 파일 다운로드 경로>
  
  # wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
  ```

  - 설치
    - 설치 중에 몇 가지 선택지가 있는데 모두 yes한다.
    - 설치가 끝나면 터미널 창을 재부팅한다.

  ```bash
  $ bash [위에서 다운 받은 설치 파일 이름]
  ```

  - PATH 설정

  ```bash
  $ source ~/.bashrc
  ```

  - 만일 위 명령어를 입력했음에도 정상적으로 동작하지 않으면 아래와 같이 bashrc를 직접 수정한다.

  ```bash
  $ vi ~/.bashrc
  
  # 아래 내용을 추가해준다.
  # $ export PATH="/home/username/anaconda3/bin:$PATH"
  ```

  - windows의 경우
    - 위 사이트에서 설치 파일을 다운 받아서 설치 해준다.
    - anaconda prompt를 실행한다.

  - 가상환경 생성하기

  ```bash
  $ conda create -n <가상 환경 이름> python=<python 버전>
  ```

  - 가상환경 목록 보기

  ```bash
  $ conda env list
  ```

  - 가상 환경 활성화

  ```bash
  $ conda activate <가상 환경 이름>
  ```

  - 비활성화

  ```bash
  $ conda deactivate
  ```

  - 가상 환경 삭제
    - `--all` 가상 환경 폴더까지 삭제된다.

  ```bash
  $ conda remove -n <가상 환경 이름>
  ```

  