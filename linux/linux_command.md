# 리눅스 기본 명령어

- top

  - 서버의 상태를 보여준다.
  - CPU, Memory, Load Average 등을 확인 가능하다.
    - CPU는 싱글 코어라는 가정하에 보여주므로 100%가 넘을 수 있다.

  ```bash
  $ top
  ```



- `history` 명령을 통해 기존에 사용했던 모든 명령을 볼 수 있다.

  - `-c` 옵션을 통해 저장된 모든 명령어를 삭제할 수 있다.

  ```bash
  $ history [옵션]
  ```



- 메뉴얼

  - 아래 명령어를 통해서 linux 명령어들의 설명을 볼 수 있다.

  ```bash
  $ man <설명을 보려는 명령어>
  ```

  - 명령어
    - 상, 하 이동은 화살표를 사용하거나 `k`/`j`키를 사용한다.
    - 페이지 단위의 이동은 `page up`/`down` 혹은 `spacebar`/`b`키를 사용한다.
    - `/찾으려는 단어`를 통해서 특정 단어를 찾는 것도 가능하며 `n`키를 통해 다음 단어로 넘어갈 수 있다.
    - `q`키로 종료한다.
  - `--help` 옵션을 통해서도 확인이 가능하다.

  ```bash
  $ <명령어> --help
  ```



- `ls`

  - 디렉토리 내부의 파일 목록을 보여준다.
  - 옵션
    - `-a`: 숨겨진 파일 보기
    - `-l`: 권한, 소유자, 갱신일 확인
    - `*`를 wildcard로 사용 가능하다.
  - file type
    - `-`: 일반 파일
    - `d`: directory
    - `b`: 블록 디바이스 파일(e.g. sda, CD-ROM)
    - `c`: 문자 디바이스 파일
    - `p`: 파이프 파일
    - `s`: 소켓 파일
    - `l`: 심볼릭 링크
  
  
  ```bash
  $ ls [옵션]
  ```
  
  - `ll`
    - `ls -l`과 동일한 명령어
    - 사용을 위해선 추가로 설치가 필요하다.
  
  ```bash
  $ ll
  ```



- cd

  ```bash
  cd <이동할 경로>
  ```



- pwd

  - 현재 디렉터리를 보여준다.
  - Print Working Directory의 약자이다.

  ```bash
  $ pwd
  ```



- rm

  - 파일이나 디렉터리를 삭제한다.
    - 해당 파일을 삭제할 권한이 있는 사용자만 삭제가 가능하다.
  - 옵션
    - `-r`: 디렉터리를 삭제.
    - `-i`: 삭제 시 정말 삭제할지를 묻는 메시지가 나온다.
    - `-f`: 삭제 시 확인하지 않고 바로 삭제한다.
  
  ```bash
  $ rm <파일 or 폴더>
  ```



- cp

  - 파일을 복사한다.

    - 복사한 파일은 기본적으로 복사한 사용자의 소유가 된다.
    - 명령 실행을 위해 해당 파일의 읽기 권한이 필요하다.
  - 옵션
    - `-r`: 디렉토리 전체 복사
    - `-p`: 소유주, 그룹, 권한, 시간 정보를 보존하여 복사
  

  ```bash
  $ cp <복사할 파일> <붙여넣을 폴더>
  ```



- touch

  - 빈 파일(크기가 0인 파일)을 생성한다.
    - 이미 존재할 경우 해당 파일의 최종 생성 시간을 명령이 실행된 시점으로 변경한다.

  ```bash
  $ touch <생성할 파일명>
  ```



- mv

  - 파일을 이동하거나 파일명을 변경한다.
    - 디렉터리가 다를 경우 파일이 이동되며, 같을 경우 파일 이름이 변경된다.

  ```bash
  $ mv <기존 파일 경로> <이동할 파일 경로>
  ```



- mkdir

  - 디렉터리를 생성한다.
  - 옵션
    - `-p`: 상위 디렉터리도 함께 생성

  ```bash
  $ mkdir [옵션] <생성할 디렉터리명>
  ```



- rmdir

  - 디렉터리를 삭제한다.
    - 비어있는 디렉터리만 삭제가 가능하다.
    - 삭제하려는 디렉터리에 대한 삭제 권한이 있어야 한다.

  ```bash
  $ rmdir <삭제할 디렉터리명>
  ```



- cat

  - 파일 내용을 화면에 보여 준다.
    - 여러 개의 파일을 나열하면 파일을 연결해서 보여준다.
    - conCATenate의 약자이다.

  ```bash
  $ cat <파일명> [파일명2] ...
  ```



- head, tail

  - 각기 파일의 맨 앞, 뒤의 10 행만 화면에 출력한다.
  - 옵션
    - `-n 숫자`: 숫자만큼 보여준다.
    - `-숫자`: 숫자만큼 보여준다.

  ```bash
  $ head [옵션] <파일명>
  $ tail [옵션] <파일명>
  ```



- more, less

  - 둘 다 파일을 페이지 단위로 화면에 출력한다
    - `spacebar`를 누르면 다음 페이지로 이동하며 `b`를 누르면 이전 페이지로 이동한다.
    - `q`를 누르면 종료된다.
    - 한 페이지는 터미널 창의 크기이다.
  - less는 more에서 기능을 더 확장시킨 것이다.
    - `page up`, `page down`도 사용이 가능하다.
  - 옵션
    - `+숫자`: 해당 행 부터 출력한다.

  ```bash
  $ more [옵션] <파일명>
  $ less [옵션] <파일명>
  ```



- file

  - 해당 파일이 어떤 종류의 파일인지 표시해준다.

  ```bash
  $ file <파일명>
  ```



- clear

  - 현재 사용 중인 터미널 화면을 전부 지운다.

  ```bash
  $ clear
  ```



- alias

  - 자주 입력하는 긴 명령어를 매번 입력하지 않고 짧은 문자열로 바꿔주는 기능.
    - 명령어의 옵션까지 포함시켜 저장이 가능하다.
  - 목록 확인하기

  ```bash
  $ alias
  ```

  - alias 등록하기

  ```bash
  $ alias <alias로 등록할 명령어>='<등록할 명령어>'
  ```

  - alias 삭제하기

  ```bash
  $ unalias <삭제할 명령어>
  ```

  - 파일로 등록하기
    - alias를 설정한 명령어는 재부팅시 모두 초기화된다.
    - 재부팅시 자동으로 등록되도록 할 수 있다.
    - `/etc/profile`에 등록하면 전체 사용자가 사용할 수 있도록 등록
    - `/home/<계정>/.bash_profile`에 등록하면 해당 계정의 사용자만 사용이 가능하다.



- tar 명령어

  - `-c`: 파일을 tar로 묶는다.
  - `-p`: 파일 권한을 저장
  - `-v`: 묶거나 파일을 풀 때 과정 출력
  - `-f`: 파일 이름을 지정
    - 지정해주지 않을 경우 제대로 실행이 되지 않으므로 왠만하면 필수로 지정해준다.
  - `-x`: tar 압축 풀기
  - `-z`:  gzip으로 압축하거나 해제함

  ```bash
  # 이름 지정하여 압축
  $ tar -cf <압축파일명.tar> <압축할 폴더 또는 파일>
  # 압축 풀기
  $ tar -xf <압축을 풀 파일 또는 폴더>
  ```



- 서버-로컬, 서버-서버 사이에 파일 복사하기.

  - 목적 디렉토리 끝에 `/`를 붙이지 않으면 해당 이름으로 파일이 복사된다.

  ```bash
  # 로컬->리모트
  $ scp 목적파일명(경로) 유저명@IP주소:목적디렉토리
  
  # 리모트->로컬
  $ scp 유저명@IP주소:파일디렉토리 목적디렉토리(경로)
  # scp theo@127.0.0.1:/home/theo/test.txt C:\Users\user\Desktop
  
  # 리모트->리모트
  $ scp 유저명@IP주소:파일디렉토리 유저명@IP주소:파일디렉토리
  ```



- sftp 활용하기

  - 우선 원격 서버에 sftp로 연결한다.
  - 아래 명령어를 입력 후 해당 계정의 비밀번호를 입력하면 연결된다.

  ```bash
  $ sftp <원격 서버 계정>@<ip>
  ```

  - 원격 서버에 파일 업로드하기(전송하기)

  ```bash
  $ put <전송할 파일 경로>
  ```

  - 원격 서버에서 파일 받아오기

  ```bash
  $ get <받아올 파일 경로(원격 서버 경로)>
  ```



- 디렉토리 구조 보기

  ```bash
  $ tree 디렉토리명
  ```



- 사용 중인 포트 확인하기

  - `-a`:  모든 연결 및 수 신 대기 포트를 표시
  - `-n`: 주소나 포트 형식을 숫자로 표현한다.
  - `-t`: TCP로 연결 된 포트를 보여준다.
  - `-u`: UDP로 연결된 포트를 보여준다.
  - `-p`: 해당 프로세스를 사용하고 있는 프로그램 이름을 보여준다.
  - `-r`: 라우팅 테이블을 보여준다.
  - `-l`: listen하고 있는 포트를 보여준다.
  - `-c`: 현재 명령을 매 초마다 실행한다.
  
  ```bash
  $ sudo netstat -antop
  ```



- 프로세스 PID로 어느 프로그램에서 사용중인지 확인하기

  ```bash
  $ ls -l /proc/<PID>/exe
  ```




- 특정 폴더 찾기

  ```bash
  # 전체 폴더에서 찾기
  $ find / -name <폴더명> -type d	# 작은 따옴표, 큰 따옴표 모두 가능하며, 안 쓰는 것도 가능하다.
  
  # 현재 폴더 및 하위 폴더에서 찾기
  $ find ./ -name <폴더명> -type d
  ```



- 특정 파일 찾기

  ```bash
  # 전체 폴더에서 찾기
  $ find / -name <'파일명'>  # 작은 따옴표, 큰 따옴표 모두 가능하며, 안 쓰는 것도 가능하다.
  
  # 현재 폴더 및 하위 폴더에서 찾기
  $ find ./ -name <'파일명'>
  ```



- gz 파일 압축 풀기

  ```bash
  $ gzip -d <압축파일명>
  ```



- 현재 디렉토리 파일별 용량 확인

  - `-s`: 디렉토리의 전체 사용량 표시
  - `-h` 파일 크기의 단위를 kb,mb,gb 단위로 표시

  ```bash
  $ du -sh *
  ```




- 시스템 전체 디스크 용량 확인
  - 옵션
    - `-a`: 모든 파일 시스템 출력
    - `-h`: 읽기 쉬운 형태로 출력



- vim

  - 리눅스의 에디터 중 하나
  - 설치

  ```bash
  $ apt-get install vim
  ```
  
  - 실행
  
  ```bash
  $ vi <파일명>
  ```
  
  - 종료
    - `esc`누른 후
    - `:w`: 저장
    - `:q`: 닫기
    - `:q!`: 저장하지 않고 닫기
    - `:wq!`: 강제 저장 후 종료




- sudo 권한 주기
  - /etc/sudousers에 아래와 같이 추가한다.
  
  ```bash
  $ sudo vi /etc/sudousers
  
  <계정명>    ALL=(ALL:ALL) ALL
  ```



- 계정

  - 계정 변경
    - 변경할 계정을 입력하지 않으면 자동으로  root 계정으로 변경된다.

  ```bash
  $ su <변경할 계정>
  ```

  - password 변경
    - 아래 명령어 입력 후 현재 비밀번호, 변경할 비밀번호 순으로 입력하면 된다.

  ```bash
  $ passwd
  ```



- 파일 수정

  - 특정 파일(들)을 찾고 해당 파일의 내용을 수정하기
  - `sed`와 `find`를 사용
    - `-i`는 변경한 내용이 실제 파일에 적용되도록 한다.

  ```bash
  find [변경할 파일의 경로] -exec sed -i 's/이전 내용/바꿀 내용/g' {} \;
  ```



- 파일의 줄 수를 계산하기

  ```bash
  $ cat <파일 경로> |  wc -l
  ```



- 파일을 분할하기

  - 정확히는 분할 보다는 대상 파일에서 지정해준 부분을 복사해서 새로운 파일을 만드는 것이다.
  - `>`을 사용한다.
  
  ```bash
  $ <조건> <파일명> > <새로 생성할 파일명>
  ```




- 백그라운드에서 실행하기

  - `nohup` 명령어를 사용한다.
  - nohup.out 파일이 생성되며 여기에 로그가 입력되게 된다.

  ```bash
  $ nohup <명령어> &
  ```

  - 종료
    - 프로세스 아이디 확인 후 종료한다.

  
  ```bash
  # 프로세스 id 확인
  $ ps -ef | grep <위에서 입력한 명령어>
  
  # 종료
  $ kill -9 <프로세스 id>



- 실행중인 프로세스 확인

  - `ps` 명령어(Process Status의 약자)를 사용한다.
    - `-e`: 모든 프로세스를 출력한다.
    - `-f`: 모든 포맷을 보여준다.
    - `-l`: 긴 포맷으로 보여준다.
    - `-p`: 특정 PID의 프로세스를 보여준다.
    - `-u`: 특정 사용자의 프로세스를 보여준다.
  
  ```bash
  $ ps <옵션>
  ```
  
    - 출력
      - UID: 실행 유저
      - PID: 프로세스 ID
      - PPID: 부모 프로세스 ID
      - C: CPU 사용률(%)
      - STIME: Start Time
      - TTY: 프로세스 제어 위치
      - TIME: 구동 시간
      - CMD: 실행 명령어
  
  ```bash
  UID        PID  PPID  C STIME TTY          TIME CMD
  root     13723 13008  1 Sep26 ?        08:43:35 python3.7 /svc/main.py
  ```



- free

  - 메모리 사용량을 체크할 수 있는 명령어
    - 메모리와 swap 메모리를 확인 가능하다.
  - swap 메모리
    - 메모리 사용량이 늘어났을 때 하드 디스크의 일부를 확장된 RAM 처럼 사용할 수 있게 해주는 기술
    - SSD 하드 디스크를 쓴다 하더라도 데이터를 읽어들이는 속도는 메모리에 비해 현저히 떨어지게 된다.
  - 옵션
    - `-m`,  `-g` 각각 mb, gb 단위로 출력한다(기본은 kb).
    - `-h`는 사람이 읽기 편한 형태로 출력한다.
  
  ```bash
  $ free
  ```



- 파일 합치기

  - 두 파일 합치기

  ```bash
  $ cat <합칠 파일명1> <합칠 파일명2> > <합친 파일명>
  ```

  - 패턴에 맞는 파일 전부 합치기
    - xargs는 앞 명령어의 실행 결과를 다음 명령어의 입력으로 사용하게 해준다.

  ```bash
  $ ls <파일명 패턴> | xargs cat > <합친 파일명>
  ```

  - 예시
    - test1.txt, test2.txt, test3.txt 가 있다고 할 때 아래 명령어를 입력하면
    - `ls test*`의 결과인 test1.txt, test2.txt, test3.txt가 xargs에 담기게 되고
    - cat을 통해 위 세 파일이 출력되면서, 출력 리다이렉션(`>`)을 통해 출력 내용을 하나의 파일로 합치게 된다.

  ```bash
  $ ls test* | xargs cat > test.txt
  ```



- 특정 행 삭제

  ```bash
  $ sed -i <숫자>d <파일명>
  ```




- 매개변수 지정

  - 쉘 스크립트에 매개 변수를 넘길 수 있다.
    - 공동으로 사용하는 쉘 스크립트의 경우 쉘 스크립트 자체를 변경시키는 것 보다 매개변수를 넘기는 것이 바람직하다.
  - 위치 매개 변수(아규먼트 변수)
    - 띄어쓰기를 기준으로 각 위치에 해당하는 값들을 가져온다.
    - `$숫자` 형태로 사용한다.
    - 10번째 부터는 중괄호로 감싸 줘야 한다(e.g`${10}`)
    - `$0`에는 실행된 쉘 스크립트명이 온다.

  ```bash
  # test.sh 파일
  echo $1 $2
  
  # 명령어
  $ sh test.sh hello world	# hello world
  ```

  - 특수 매개 변수
    - `$!`: 실행을 위해 백그라운드로 보내진 마지막 프로그램 프로세스 번호
    - `$$`: 쉘 스크립트의 PID
    - `$?`: 실행한 뒤의 반환 값(백그라운드로 실행된 것 제외)
    - `$_`: 지난 명령의 마지막 인자로 설정된 특수 변수
    - `$-`: 현재 쉘이 호출될 때 사용한 옵션들



- 운영체제 정보 확인

  ```bash
  $ cat /etc/issue
  
  # 또는
  $ cat /etc/*release*
  
  # 또는
  $ cat /etc/os-release
  ```



- 중복 행 제거

  - uniq 사용
    - 연속으로 중복 된 행이 있을 경우 중복된 행을 삭제한다.

  ```bash
  # test.txt
  orange
  apple
  apple
  watermelon
  watermelon
  apple
  orange
  (빈 줄)
  
  # 중복 제거
  $ cat test.txt | uniq
  
  # out
  orange
  apple
  watermelon
  apple
  orange
  ```

  - sort
    - 연속되지 않은 중복 행을 삭제하려 할 경우 먼저 정렬 후에 사용한다.

  ```bash
  $ cat test.txt | sort | uniq
  
  # out
  apple
  orange
  watermelon
  ```

  - `-c`
    - 몇 개가 중복되었는지 확인하기 위해 사용한다.

  ```bash
  $ cat test.txt | sort | uniq -c
  
  # out
  3 apple
  2 orange
  2 watermelon
  ```

  - 정렬하려는 대상 파일의 마지막에 빈 줄이 없으면 제대로 동작하지 않는다.
    - 항상 마지막 행은 어떤 행과도 중복되지 않는 고유한 행으로 취급된다.

  ```bash
  # test.txt
  orange
  apple
  apple
  watermelon
  watermelon
  apple
  orange
  
  # 중복 제거
  $ cat test.txt | sort | uniq -c
  
  # out
  3 apple
  1 orange
  1 orange
  2 watermelon
  ```



- 링크 설정하기

  - 링크 확인하기
    - `ls` 명령어에 `l` 옵션을 준다.
    - 링크가 생성되면 다음과 같이 맨 앞에 `l`이 붙고, `link -> original/` 처럼 링크 표시가 뜬다.
  
  ```bash
  $ ls -l
  total 4
  lrwxrwxrwx 1 root root    9 Jul 26 12:12 link -> original/
  ```
  
  - 심볼릭 링크 생성하기
    - window 환경에서는 bash 등을 사용해도 링크가 제대로 잡혔는지 나오지 않으므로 리눅스 환경에서 테스트 해봐야 한다.
    - 심볼릭 링크는 기본 명령어인 `ln`에 `-s` 옵션을 추가하여 생성한다.
  
  ```bash
  $ ln -s <원본 파일 또는 폴더 경로> <링크를 생성할 파일 또는 폴더>
  ```
  
  - git 관련
    - vscode의 변경 사항 추적은 적용되지 않는다.
    - 그러나 git status로 확인해보면 실제로는 변경 사항이 그대로 추적되는 것을 확인 가능하다.
    - 따라서 링크 디렉토리에서도 그냥 사용하면 된다.



- crontab

  > https://crontab.guru/  corntab 설정을 해볼 수 있는 사이트
  
  - 특정 시간에 특정 프로그램을 특정 주기로 실행시키는 프로그램
  - 설치
  
  ```bash
  $ apt-get install cron
  ```
  
  - 크론탭 설정하기
    - vi 에디터를 사용하여 크론탭 설정을 입력한다.
    - `*` , 숫자,  `,`, `-`를 조합해서 설정한다.
  
  ```bash
  $ corntab -e
  
  *			*			*			*			*
  분(0-59)	   시간(0-23)   일(1-31)	 월(1-12)	요일(0-7, 0과 7은 일요일, 1-6은 월-토요일 순이다.)
  
  # 만일 아래와 같이 설정하면 test.sh를 매분 실행하겠다는 뜻이다.
  * * * * * test.sh
  # 매월 5,15,25일 10시 정각, 20분, 30분에 test.sh를 실행하겠다는 뜻이다.
  0,20,30 10 5,15,25 * * test.sh
  # 매월 10~20일 매 20분마다 test.sh를 실행하겠다는 뜻이다.
  */20 * 10-20 * * test.sh
  
  # 로그 남기기
  * * * * * test.sh > test.sh.log 2>&1
  ```

  - 크론탭 설정 내용 확인
  
  ```bash
  $ crontab -l
  ```

  - 크론탭 설정 내용 삭제
  
  ```bash
  $ crontab -d
  ```



- 리눅스 특수 문자

  - 표준출력
    - `>`, `>>`을 사용한다.
    - `>`는 새로운 파일을 쓰는 것이고, `>>`는 기존 파일에 추가하는 것이다.

  ```bash
  $ <명령어> > <저장할 파일>
  $ <명령어> >> <저장할 파일>
  ```

  - 표준 입력
    - `<`를 사용한다.

  ```bash
  $ cat < text.txt
  ```

  - 와일드 카드
    - `*`, `?`가 있다.
    - `*`는 복수의 문자를 대체하는 와일드 카드이고, `?`는 하나의 문자를 대체하는 와일드 카드이다.

  ```bash
  # test.txt, text.txt
  $ ls te*.txt
  $ ls te?t.txt
  ```

  - 파이프 문자
    - 특정 프로세스의 표준 출력을 다른 프로세스의 표준 입력으로 보내는 문자

  ```bash
  $ cat ll | grep txt
  ```

  - 명령 문자
    - 명령에 괸련된 문자들
    - `;` : 명령의 끝을 나타낸다.
    - `||`: 이전 명령이 실패하면 실행하는 조건문 문자
    - `&&`: 이전 명령이 성공하면 실행하는 조건문 문자
    - `&`: 명령을 백그라운드에서 실행
    - `$`: 변수에 접근할 수 있는 문자
  - 변수 접근 기호
    - `0`: 표준 입력
    - `1`: 표준 출력
    - `2`: 에러 출력

  ```bash
  # 로그 파일 출력하기
  $ ./test.sh >> ./test.log 2>&1
  ```



- 리눅스에서 공백 문자 표현

  - 리눅스에서 공백 문자, 괄호 등은 `\+공백문자`, `\+괄호`를 통해 표현한다.
  - 예를 들어 파일명이 `Hello World(EN).txt`인 경우 `Hello\ World\(EN\).txt`로 표현한다.

  ```bash
  $ mv Hello\ World\(EN\).txt Hello\ World\(KR\).txt
  ```




- 리눅스에서 현재 날짜 구하기

  - `date` 명령어를 입력한다.

  ```bash
  $ date
  Thu Sep 16 09:17:49 KST 2021
  ```

  - 포맷

  | 포맷 | 설명                                                |
  | ---- | --------------------------------------------------- |
  | %%   | % 기호를 출력한다.                                  |
  | %a   | 요일을 약어로 출력                                  |
  | %A   | 요일을 전체 단어로 출력                             |
  | %b   | 월 이름을 약어로 출력                               |
  | %B   | 월을 전체 단어로 출력                               |
  | %y   | 년도의 뒤의 두 자리를 출력한다.                     |
  | %Y   | 전체 년도를 출력한다.                               |
  | %m   | 월을 출력한다.                                      |
  | %d   | 일을 출력한다.                                      |
  | %H   | 시간을 24시간 표현법으로 출력한다.                  |
  | %M   | 분을 출력한다.                                      |
  | %S   | 초를 출력한다.                                      |
  | %s   | 1970-01-01 00:00:00 UTC로부터 경과된 초를 출력한다. |
  | %D   | %m/%d/%y 형태로 날짜를 보여준다.                    |
  | %T   | %H:%M:%S 형태로 시간을 보여준다.                    |
  | %p   | AM, PM 출력                                         |
  | %r   | 00:00:00 AM 형태로 시간을 출력한다.                 |
  | %j   | 년을 기준으로 며칠이 지났는지 출력한다.             |
  | %n   | 출력 시에 줄을 바꾼다.                              |
  | %z   | 타임존 값을 출력한다.                               |
  | %Z   | 시간 대역의 이름을 출력한다.                        |

  - 예시
    - 포맷의 맨 앞에 `+`를 넣어야 한다.

  ```bash
  $ date +%Y-%m-%d
  2021-09-16
  ```

  - 과거 날짜 구하기

  | 명령어                 | 결과           |
  | ---------------------- | -------------- |
  | yesterday              | 어제           |
  | 1 day ago              | 어제           |
  | 2 day ago              | 2일 전         |
  | 35 day ago             | 35일 전        |
  | 1 week ago             | 일주일 전      |
  | 2 month ago            | 두 달 전       |
  | 4 year ago             | 4년 전         |
  | 10 second ago          | 10초 전        |
  | 10 minute ago          | 10분 전        |
  | 10 hour ago            | 10 시간 전     |
  | 1 year 1month 1day ago | 1년 1달 1일 전 |

  - 미래 날짜 구하기
    - 과거 날짜 구하기에서 ago를 빼면 된다.
    - 내일 날짜는 tomorrow를 쓴다.
  - 예시
    - `-d` 옵션을 붙여줘야 한다.

  ```bash
  # 이틀 전 출력하기
  $ date -d '2 day ago'
  
  # 1년 전을 특정 포맷으로 출력하기
  date -d '1 year ago' +%Y-%m-%d
  ```

  - 특정 시간을 기준으로 날짜 더하고 빼기

  ```bash
  $ date -d '2020-01-01 00:00:00 + 1 day 12 hour'
  ```



- ping

  - 네트워크가 살아있는지 확인하는 명령어
    - 네트워크가 살아있는지만 확인하는 것이므로 ping이 성공한다고해서 해당 주소로 접근할 수 있는 것은 아니다.
    - port가 닫혀 있는 등의 이유로 접근이 불가능할 수 있다.
    - 따라서 정말 접근이 가능한지는 ssh(`ssh <계정>@<주소>`)를 사용하여 테스트해야 한다.
  - 옵션
    - `-i`: 응답을 체크할 주기를 설정한다(sec)
    - `-c`: ping을 보낼 전체 횟수를 설정한다.

  ```bash
  $ ping <옵션> <확인하려는 주소>
  ```



- curl
  - Command line용 data transfer protocel
  - 주요 옵션들
    - `--request`(`-X`): HTTP method를 설정한다.
    - `-H`: 전송할 header를 설정한다.
    - `--data`(`-D`): 요청과 함께 보낼 data를 설정한다.
  - cors 설정이 제대로 되었는지 확인할 때 사용할 수 있다.



- 대상 서버의 포트가 열려 있는지 확인하는 방법

  > https://meetup.toast.com/posts/204

  - telnet
    - 연결 된 후 `ctrl+]`를 통해 텔넷 프롬프트창을 띄운 후 `quit`하면 연결을 끊을 수 있다.
    - 기본으로 설치되어 있지 않아 설치해야 사용 가능하다.

  ```bash
  $ telnet <IP> <PORT>
  ```

  - `echo`를 활용한 방법
    - bash의 bulit-in 기능이다.
    - 포트가 열려있는 경우 아무 메시지도 나오지 않고 끝난다.
    - `echo $?`를 입력했을 때 0이 나오면 정상 실행을, 1이 나오면 정상적으로 실행되지 않았다는 것을 의미한다.

  ```bash
  $ echo dev/tcp/<ip>/<port>
  
  # 이전 명령이 정상적으로 끝났는지 확인하는 명령어
  $ echo $?
  ```




- ulimit
  - linux에서 사용자별(user) 프로세스의 자원 한도(limit)을 설정하는 명령어.
    - 프로세스가 열 수 있는 파일 수, 사용자가 만들 수 있는 파일 크기, 스택, 메모리 등 다양한 자원에 대해 제한을 걸 수 있다.
  - Soft와 Hard로 나뉜다.
    - soft: 새로운 프로그램을 생성함녀 기본으로 적용되는 한도.
    - hard: soft한도에서 최대로 늘릴 수 있는 한도.
  - ulimit 명령어를 사용하여 설정하거나, `/etc/security/limits.conf` 파일을 수정하여 설정할 수 있다.
    - 명령어를 사용하는 방법은 세션이 끊어지면 초기화된다.
    - 파일을 수정하는 방법은 설정 후 세션을 한 번 끊었다가 다시 로그인해야 적용된다.



- default shell 변경하기

  ```bash
  $ usermod --shell <shell 종류> <user명>
  ```




- SSH(Secure SHell)

  - 네트워크 상의 다른 컴퓨터에 로그인하거나 원격 시스템에서 명령을 실행하고 다른 시스템으로 파일을 복사할 수 있도록 해주는 소프트웨어 혹은 그 프로토콜을 의미한다.

    - 핀란드의 Tatu Ylönen이 개발하였다.
    - 유저 인증, 명령어, 출력 결과, 파일 전송이 모두 암호회되어 network상에서 탈취되더라도 쉽게 내용을 볼 수 없게 해준다.

    - OpenSSH라는 SSH protocol을 open source로 구현한 프로그램이 있다.
    - 서버 인증과 사용자 인증에는 비대칭키 방식을 사용하고, client와 server간의 통신에는 대칭키 방식을 사용한다.

  - 설치 및 실행
    - Ubuntu 기준이다.
  
  
  ```bash
  # 설치
  $ apt install ssh
  
  # 실행
  $ service ssh start
  ```
  
  - 동작 과정
  
    - Client가 server의 22번 포트로 접속을 요청한다.
    - Client의 요청을 받은 server는 server에서 보관중인 public key(host key)를 client에게 전송한다.
    - Client와 server는 parameter들을 주고 받으며 연결 방식에 대해 협의한 후 접속 채널을 연다.
    - 모든 인증이 무사히 완료되면, client는 SSH 프로토콜로 server에 접속하게 된다.
  
  - 서버 인증 과정

    - Client가 자신이 접속하고자 하는 server가 올바른 서버인지 확인하는 과정이다.
    - 서버 인증에는 host keys라 불리는 비대칭키(public key와 private key)가 사용된다.
    - Host keys는 일반적으로 `/etc/ssh` directory에 저장되며, `ssh_host_<rsa/dsa/ecdsa/ed25519>_key`와 같은 prefix를 가지고 있다.
    - Host keys는 일반적으로 OpenSSH가 최초로 설치될 때 함께 생성되며, 이후에 추가로 생성할 수도 있다.
    - Host keys의 private key는 server가 보관하고, public key는 client가 보관한다.
    - Server가 client로부터 접속 요청을 받으면, client에게 host keys 중 public key를 전송한다.
    - Client는 server로부터 받은 public key를 `<home>/.ssh/known_hosts`파일에 저장한다.
    - Client는 `known_hosts` file에 저정해둔 server의 public key를 가지고, 자신이 접속하려는 server가 정상적인 서버인지 아래와 같은 과정을 통해 확인한다.
    - Clinet는 난수값을 생성하고 해당 난수값으로 해시를 생성해 저장한 뒤, 난수값을 server가 전달한 public key로 암호화하여 server에 전송한다.
    - Server는 암호화된 데이터를 private key(host key)로 복호화하여 난수값을 얻어낸 뒤, 해당 난수값을 해시로 만들어 다시 client로 전송한다.
    - Server로부터 해시를 전달 받은 client는 자신이 저장했던 해시와 비교하여 두 해시가 동일하면, 올바른 서버에 접속하는 것이라 판단한다.
  
  - 서버 인증이 필요한 이유
  
    - Client가 server에 최초로 접속 요청을 보낸 후 둘 사이에 안전한 채널이 열리기 전에, client가 server로 보낸 요청이 network상에서 악의적인 공격으로 다른 server로 납치될 수 있다.
    - 그럼 client는 자신이 접속하려던 server가 아닌 악의적인 다른 server에 데이터를 전송하게 된다.
    - 따라서 client는 중간에 다른 서버에게 자신의 요청이 가로채진 것은 아닌지 확인하는 과정이 필요하다.
  
  - 사용자 인증 과정
  
    > Password를 사용한 인증 방법도 있고 아예 인증을 하지 않는 방법도 있지만 SSH key를 사용하는 것이 권장되므로, SSH key를 사용할 경우만 다룬다.
  
    - Server가 자신에게 접속을 요청한 client user의 identity를 확인하는 과정이다.
    - 사용자 인증에는 비대칭키(public key와 private key)가 사용된다(서버 인증에 사용된 host keys와는 다르다).
    - Client는 비대칭키를 생성하여 public key는 서버의 `<home>/.ssh/authorized_keys`에 저장하고, private key만 자신이 가지고 있는다.
    - Client가 인증할 key 쌍의 ID를 서버에 전송한다.
    - Server는 `.ssh/authorized_keys`파일을 확인하여 ID에 매칭되는 public key가 있을 시 아래 과정을 진행한다.
    - Server는 무작위 문자열을 생성하고 해당 문자열로 만든 해시를 저장한 뒤, 난수는 client에게 전달 받은 public key로 암호화하여 client에게 전송한다.
    - Client는 priavate key를 사용하여 server가 전달한 암호화된 난수를 복호화하고, 복호화된 난수와 세션키를 결합하여 해시를 생성한 후 server로 전송한다.
    - Server는 저장된 난수와 세션키를 결합하여 해시를 생성하고, 해당 해시와 client에게 전달 받은 해시를 비교하여 두 해시가 동일하면 client에게 권한이 있다고 판단한다.
  
  - Server와 client간의 통신
  
    - Server와 client간의 통신에는 대칭키인 session key가 사용된다.
    - 대칭키 방식은 비대칭키 방식에 비해 리소스도 적게 들고 속도도 빠르다는 장점이 있지만, 대칭키가 유출될 경우 암호화된 통신을 복호화 할 수 있다는 단점이 있다.
    - SSH는 대칭키기 유출되지 않도록 하기 위해 키 교환 알고리즘을 사용하여 대칭키를 교환한다.
    - 키 교환 알고리즘에는 주로 디피-헬먼(Diffie-Hellman) 알고리즘 혹은 타원 곡선 디피 헬먼(Elliptic-curve Diffie–Hellman) 알고리즘이 사용된다.



- `ssh`를 통해 다른 컴퓨터로 접속하기 위한 사용자 인증 과정

  - 위에서 살펴본 SSH의 동작 과정 중에서 사용자가 신경써야 할 부분은 사용자 인증과 관련된 부분 뿐이다.
    - 접속 대상 컴퓨터에 OpenSSH가 설치되어 있다면, 서버 인증에 필요한 host keys는 이미 생성된 상태일 것이므로 굳이 생성할 필요는 없다.
    - 그리고 대부분의 OS에서 OpenSSH는 기본으로 설치되어 있다.
    - 따라서 사용자 인증을 위한 절차만 살펴볼 것이다.
  - 먼저 key pair를 생성한다.
    - `ssh-keygen` 명령어를 통해 key pair를 생성할 수 있다.
    - Key pair는 client 컴퓨터의 `<user_home_dir>/.ssh` directory에 저장해야한다.
    - Unix 계열 운영체제가 아닌 Windows에서도 cmd 창을 열어 동일한 명령어로 생성이 가능하다.
    - 여러 가지 key type을 선택할 수 있는데, OpenSSH 8.8부터 SHA-1 알고리즘으로 작성한 RSA 인증은 사용할 수 없게 되었으므로 다른 타입을 사용해야한다.

  ```bash
  $ ssh-keygen -t <key-type>
  ```

  - Public key를 접속하려는 컴퓨터의 `<user_home_dir>/.ssh/authorized_keys`에 추가한다.
    - 별도의 파일명을 설정하지 않고 위 명령어를 실행하면 `id_rsa.pub`라는 public key가 저장된 파일과 `id_rsa`라는 private key가 저장된 파일이 생성된다.
    - 이 중 public key가 저장된 `id_rsa` file의 내용을 읽어서 `<user_home_dir>/.ssh/authorized_keys`에 추가하면 된다.
  - `ssh`를 통해 접속한다.

  ```bash
  $ ssh -i <private_key_file_path> <user>@<IP>
  ```

  - 만약 매 번 `-i` option을 통해 키를 지정하는 것이 번거롭다면 아래와 같이 하면 된다.
    - `<user_home_dir>/.ssh` 경로에 `config` 파일을 생성한다.
    - config file에 아래와 같이 작성한다.

  ```bash
  Host test
    HostName <IP>
    IdentityFile <private_key_path>
    User <user>
  ```



- SSHFS

  - 다른 서버에 위치한 directory와 file을 일반 SSH 연결을 통해 client가 mount할 수 있게 하는 파일 시스템이다.
    - FUSE(Filesystem in Userspace)를 기반으로 한다.
    - Linux에서는 일반적으로 `/mnt` 경로에 mount한다.
    
  - 설치
  
  ```bash
  $ sudo apt install sshfs
  ```
  
  - Mount하기
    - 대상 서버에 SSH 접속이 가능해야한다.
  
  ```bash
  $ sshfs <user>@<remote_IP>:<remote_path> <local_path>
  ```
  
  - 읽기 전용으로 마운트하기
    - `-o ro` 옵션을 주면 읽기 전용으로 마운트가 가능하다.
  
  ```bash
  $ ssfs -o ro <user>@<remote_IP>:<remote_path> <local_path>
  ```
  
  - 원격 서버 접속 시 비밀번호가 필요할 경우, 아래와 같이 한 번에 실행할 수 있다.
    - `sshpass` 등의 package가 있으면 보다 깔끔하게 실행할 수 있으나, 만약 패키지 설치가 불가능할 경우 아래 방법을 시도해보면 된다.
    - 모든 시스템에서 동작하지는 않는다.
  
  ```bash
  $ sshfs -o password_stdin <user>@<remote_IP>:<remote_path> <local_path> <<< '<password>'
  ```
  
  - Mount 해제하기
    - `unmount`가 아닌 `umount`이다.
    - 앞서 말했듯, SSHFS는 FUSE 기반이기에 `fusermount -u`로도 가능하다.
  
  ```bash
  $ umount <local_path>
  $ fusermount -u <local_path>
  ```
  
  - 주의사항
    - Copy가 아닌 mount이므로 mount한 server에서 변경 사항이 생길 경우 mount 대상 서버에도 그대로 반영된다.
    - Mount한 server의 권한과 상관없이 추가, 수정, 삭제가 가능하다.
    - 중간에 연결 된 서버가 종료될 경우 mount는 해제된다.
  - "Transport endpoint is not connected" error
    - 만약 사용 중 위와 같은 error가 발생할 경우 아래와 같이 `fusermount -u` 명령어를 통해 mount를 해제한 후 다시 연결하면 된다.
  
  ```bash
  $ fusermount -u <mount_path>
  ```
  
  - Python으로 실행하기
  
  ```python
  import subprocess
  
  command = ["sshfs", "user@remote_IP:/remote_path", "/local_path"]
  subprocess.run(command, check=True)
  
  # read only로 설정
  command = ["sshfs", "-o", "ro", "user@remote_IP:/remote_path", "/local_path"]
  res = subprocess.run(command, check=True)
  
  # password 입력
  command = ["sshfs", "-o", "password_stdin", "user@remote_IP:/remote_path", "/local_path"]
  # input에 password를 encoding한 값을 넣어준다.
  subprocess.run(command, input="password".encode(), check=True)
  ```













