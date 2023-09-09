# 오프라인 환경에서 linux에 Python 설치하기

- linux library 설치

  - Python을 실행하기 위해 운영체제에 필요한 라이브러리들을 먼저 설치해야 한다.
    - yum으로 설치할 경우 의존성이 있는 라이브러리들을 함께 설치해주지만, 아래와 같이 source file로 설치할 경우 직접 설치해야 한다.
  - 온라인 환경에서 필요한 라이브러리들을 설치한다(centos 기준).
    - --downloadonly로 필요한 라이브러리들의 설치 파일만 받는다.
    - 옮기기 쉽도록 `--downloaddir`을 현재 디렉토리로 설정한다.

  ```bash
  $ yum install -y --downloadonly --downloaddir=. gcc openssl-devel bzip2-devel libffi-devel
  ```

  - 위에서 다운 받은 라이브러리 설치 파일들을 오프라인 환경으로 옮긴 후 설치한다.

  ```bash
  $ yum install -y <파일명 혹은 *(디렉토리 내의 rpm 파일 전부 설치)>
  ```



- python 설치 파일 다운

  > https://www.python.org/downloads/

  - 위 사이트에서 버전 선택 후 `Gzipped source tarball`나 `XZ compressed source tarball`를 설치한다.
    - 두 파일은 압축 방식에 차이가 있을 뿐 실제 사용에는 어떠한 차이도 없으므로 아무거나 받으면 된다.
  - 받은 후 scp 등의 명령어를 통해 Python을 설치하려는 linux 서버로 옮겨준다.



- 설치하기

  - 압축 풀기
    - tar 명령어를 통해 위에서 받은 압축 파일을 푼다.

  ```bash
  $ tar -xvf <압축파일 경로>
  ```

  - 압축 풀기가 완료되면 풀린 폴더 내부로 이동해 `./configure` 를 실행한다.
    - `./configure`는 소스 파일에 대한 환경 설정을 해주는 명령어이다.
    - `--enable-optimizations` 옵션은 Python을 최적화하여 실행 속도를 높여준다.
    - `--with-ensurepip=install`은 pip를 함께 설치할지를 설정하는 것이다.
    - `--prefix`를 통해 설치 경로를 설정 가능하다.
  
  ```bash
  $ ./configure [--enable-optimizations] [--with-ensurepip=install] [--prefix=설치 경로]
  ```
  
  - `make`를 통해 소스 파일을 컴파일한다(skip 가능).
    - make과정이 끝나면 `setup.py` 파일이 생성된다.
    - `test`를 통해 test도 가능하다.
  
  
  ```bash
  $ make [test]
  ```
  
  - `command not found`가 뜰 경우 make를 설치한다.
  
  ```bash
  $ yum install make
  ```
  
  - 설치하기
    - `altinstall` 옵션은 기존에 설치된 Python과의 충돌을 피하기 위한 옵션이다.
    - `install`을 입력해도 되지만, 이 경우 기존 Python에 덮어 씌워진다.
  
  ```bash
  $ make altinstall
  ```
  
  - 만일 리눅스 library를 설치하지 않고 Python을 먼저 설치했다면 아래 과정을 통해 재설치해야 한다.
  
  ```bash
  $ make clean
  $ ./configure [--enable-optimizations] [--with-ensurepip=install] [--prefix=설치 경로]
  $ make install
  ```



- Python 설치 후 기본 Python을 새로 설치한 버전으로 변경

  - 설정 변경

  ```bash
  $ vi ~/.bashrc
  
  # alias python="<Python 설치 경로>" 추가
  ```

  - 적용

  ```bash
  source ~/.bashrc
  ```




- 심볼릭 링크 설정하기

  ```bash
  $ ln -s <설치한 Python 경로> </bin/링크생성할 경로>
  ```

  

- 폐쇄망에 패키지 설치
  - 일단 폐쇄망이 아닌 곳에서 필요한 라이브러리들을 설치한다.
  - 기본적으로 라이브러리는 Python 설치 경로, 혹은 venv의 `lib/python<버전>/site-packages`에 설치된다.
  - 라이브러리가 설치된 폴더로 이동해서 필요한 라이브러리들을 tar 파일로 묶는다.
  - 폐쇄망으로 tar 파일을 옮긴 후 압축을 푼다.
  - 압축이 풀린 파일들을 폐쇄망에 설치된 Python 라이브러리 경로, 혹은 venv의 `lib/python<버전>/site-packages`에 넣는다.





# Docker로 설치하기

> https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8
>
> https://pythonspeed.com/articles/base-image-python-docker-images/
>
> https://pythonspeed.com/articles/alpine-docker-python/

- 어떤 image를 선택해야하는가?

  - Docker hub에는 아래와 같이 다양한 Python image가 존재한다.
    - python
    - python-alpine
    - python-slim
  - 가장 나은 선택은 ubuntu image에 python을 설치해서 사용하는 것이다.
    - Alpine이나 slim의 경우 경량화를 위해 성능을 어느 정도 포기해야하므로, 성능이 중요한 작업을 실행해야 할 경우 적절하지 않을 수 있다.
    - 기본 python image의 경우도 마찬가지로 ubuntu에 python을 설치하는 것 보다 성능이 나오지 않는다.

  - Alpine linux image를 사용하면 되지 않나?
    - Apline linux는 다른 image를 생성할 때는 좋은 base image일 수 있다.
    - 그러나 Python image를 생성할 때에는 부적절 할 수 있다.
    - 이는 PyPI에 있는 Python library들이 일반적으로 `Wheel` 포맷을 사용하는데 alpine linux의 경우 `Wheel` 포맷을 지원하지 않아 library의 source code를 직접 내려 받아 compile해야하는 경우가 있기 때문이다.
    - 따라서 build시에 시간이 훨씬 오래걸리게 된다.



- Ubuntu를 base image로 Python image 생성하기

  - Ubuntu image를 받아온다.

  ```bash
  $ docker pull ubuntu:20.04
  ```

  - Python image를 생성하기 위해 아래와 같이 Dockerfile을 생성한다.

  ```dockerfile
  FROM ubuntu:20.04
  
  RUN apt-get update && apt-get install -y \
      python3.8 \
      python3-pip
  ```

  - Python image를 build한다.

  ```bash
  $ docker build -t my-python:3.8.0 .
  ```

  - Python app을 생성한다.

  ```python
  import time
  
  while 1:
      try:
          print("Hello World!")
          time.sleep(3)
      except KeyboardInterrupt:
          print("Bye!")
          break
  ```

  - Python app을 build하기 위한 Dockerfile을 생성한다.

  ```dockerfile
  FROM python:3.8.3
  
  ENV HOME /app
  WORKDIR ${HOME}
  COPY . ${HOME}
  
  ENTRYPOINT ["python3", "-u", "main.py"]
  ```

  - Python app을 build하고, container를 실행시킨다.

  ```bash
  $ docker build -t my-python-app .
  $ docker run --name my-python-app my-python-app
  ```

  

  

  

  

  



