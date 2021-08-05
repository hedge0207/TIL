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




## 심볼릭 링크

- Python은 버전 관리가 필수다.
  - 버전별로 패키지가 관리된다.
    - 따라서 한 버전의 Python으로 잘 동작하는 스크립트가 다른 버전에서는 패키지 문제로 동작하지 않을 수 있다.
    - 예를 들어 3.7 버전을 설치하여 numpy 패키지를 받아서 사용하다가 2.5 버전으로 Python 버전을 변경하면, 해당 버전에서는 numpy를 설치한 적이 없고, 설치한다 하더라도 numpy가 2.5 버전과 호환될지도 미지수이다.
  - 문제 상황 예시
    - 현재 리눅스 서버에서는 python 2.7.5 버전을 사용중인데 python 3.7.5 버전인 가상 환경에서 작업을 하는 중인 경우
    - python 3.7.5 버전을 사용할 것을 가정하고 python  스크립트를 작성했는데 리눅스 서버의 python 버전이 2.7.5라 실행이 되지 않는 경우
    - jupyter notebook에서는 3.7.5 버전을 사용중인데 python 버전이 2.7.5인 리눅스 터미널에서 jupyter notebook으로 작성한 파일을 실행하려 할 경우 
    - 위와 같은 경우에 각기 다른 버전이므로 설치 된 패키지도 다르고 호환도 문제가 될 수 있다.



- 다른 버전의 python 파일을 실행하는 방법.

  - 리눅스에서 python을 실행하는 명령어는 아래와 같다.

  ```bash
  $ python <python 파일명>
  ```

  - 이는 사실 심볼릭 링크가 잡혀 있는 python을 실행하는 명령어로, 다른 python을 실행하고 싶다면 아래와 같이 입력한다.

  ```bash
  $ <다른 python 경로> <python 파일명>
  
  # e.g.1 venv를 통해 생성한 python을 사용하고자 할 경우
  $ /venv/bin/python3 <python 파일명>
  
  # e.g.2 jupyter에서 사용 중인 python 파일을 사용하고자 할 경우
  $ /usr/local/bin/python3.7 <python 파일명>
  ```

  - 만일 실행 할 때마다 위와 같이 python 경로를 일일이 지정해주는 것이 불편하다면, 기본 python을 가리키는 심볼릭 링크를 변경해주면 된다.



- 심볼릭 링크 변경하기(사용하고자 하는 python 버전이 이미 설치되어 있다고 가정)

  - 현재 사용중인 파이썬 위치 확인

  ```bash
  $ which python
  ```

  - 심볼릭 링크가 가리키는 파일 확인

  ```bash
  $ ls -al <위에서 확인한 경로>
  ```

  - 데비안 계열 리눅스에서 심볼릭 링크 변경하기
    - `update-alternatives` 명령어를 지원한다.
    - 사용하고자 하는 python 경로를 추가하고, 이후에 어떤 경로의 python을 사용할지 선택한다.

  ```bash
  # python 경로 추가(복수의 python 경로를 추가 가능하다)
  $ update-alternatives --install <위에서 확인한 경로> python <사용하고자 하는 python 경로>
  # 사용할 python 선택(아래 명령어를 입력하면 선택 창이 뜨는데 원하는 번호를 입력하면 된다)
  $ update-alternatives --config python
  ```

  - 이외의 리눅스에서 심볼릭 링크 걸기
    - 안될 경우 `rm <위에서 확인한 경로>`로 기존 경로를 지워준다.

  ```bash
  $ ln -s <사용하고자 하는 python 경로> <위에서 확인한 경로>
  ```






# ETC

- Python에서 리눅스 명령어 실행하기

  - subprocess 모듈을 사용한다.
    - 실행하려는 명령이 시스템에 설치되어 있어야 한다.
    - 따라서 이식성이 떨어진다.
  - 예시
    - subprocess의 run 메서드를 호출하면 명령이 실행되고, 결과가 PIPE에 저장된다.
    - result.stdout은 str이 아니고 byte이기 때문에 unicode로 변환을 해줘야 한다.

  ```python
  import subprocess
  
  
  result = subprocess.run(['ls'], stdout=subprocess.PIPE)
  result_as_string = result.stdout.decode('utf-8')
  
  print(result_as_string)
  
  result = subprocess.run(['wc', '-l', 'test.txt'], stdout=subprocess.PIPE)
  result_as_string = result.stdout.decode('utf-8')
  
  print(result_as_string)
  ```

  

- tqdm

  - python 코드를 실행 했을 때 진행 상황을 볼 수 있는 모듈이다.
    - 실행에 오랜 시간이 걸리는 코드의 경우 중간에 print나 logging 모듈로 로그를 남기는 방식을 사용하기도 한다.
    - tqdm은 print나 logging 모듈 없이도 진행 상황을 확인하게 도와준다.
  - 설치

  ```bash
  $ pip install tqdm
  ```

  - 사용
    - iterable을 tqdm에 넘겨 사용한다.

  ```python
  import time
  from tqdm import tqdm
  
  
  def long_time_job():
      time.sleep(0.1)
  
  for i in tqdm(range(100)):
      long_time_job()
  ```

  - 결과

  ```bash
  $ python main.py 
  74%|████████████████████████████████████████████████████████████████████████████████████████████████▉              | 74/100 [00:07<00:02,  9.49it/s]
  ```

  
