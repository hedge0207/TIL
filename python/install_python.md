# 오프라인 환경에서 linux에 Python 설치하기

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
  
  - `make`를 통해 소스 파일을 컴파일한다.
    - make과정이 끝나면 `setup.py` 파일이 생성된다.
    - `test`를 통해 test도 가능하다.
  
  
  ```bash
  $ make [test]
  ```
  
  - 설치하기
    - `altinstall` 옵션은 기존에 설치된 Python과의 충돌을 피하기 위한 옵션이다.
    - `install`을 입력해도 되지만, 이 경우 기존 Python에 덮어 씌워진다.
  
  ```bash
  $ make altinstall
  ```




- 심볼릭 링크 설정하기

  ```bash
  $ ln -s <설치한 Python 경로> </bin/링크생성할 경로>
  ```

  

