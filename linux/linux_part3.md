## system 등록하기

> centos:7 기준

- 시스템 등록하기

  - 실행할 스크립트를 작성한다.
    - shebang(`#!/bin/bash`)을 반드시 넣어줘야한다.

  ```bash
  #!/bin/bash
  
  echo -e " Start Systemd Test " | logger -t Testsystemd
  
  while :
  do
  	echo -e "Running systemd"
  	sleep 30
  done
  ```

  - 시스템에 등록한다.
    - `/usr/lib/systemd/system` 디렉터리로 이동한다.
    - `service명.service`라는 파일을 아래와 같이 작성한다.

  ```bash
  [Unit]
  Description=Systemd Test
  
  [Service]
  Type=simple
  ExecStart=/home/theo/hello.sh	# 위에서 작성한 shell script 파일 경로
  Restart=on-failure
  
  [Install]
  WantedBy=multi-user.target
  ```

  - 아래 명령어로 등록 된 서비스들을 확인 가능하다.

  ```bash
  $ systemctl list-units --type=service
  ```
  
  - `.service` 파일을 수정했을 경우 아래 명령어로 변경 사항을 적용한다.
  
  ```bash
  $ systemctl daemon-reload
  ```
  
  - 등록된 service를 실행한다.
  
  ```bash
  $ systemctl start <서비스명>
  ```
  
  - 특정 서비스의 상태 확인
  
  ```bash
  $ systemctl status <서비스명>
  ```
  
  



- 옵션들

  > Unit, Service, Install로 나뉘며 아래 옵션들 외에도 많은 옵션이 존재한다.

  - Description

    - 해당 유닛에 대한 설명
- Type
  
  - 유닛 타입을 선언한다.
    - simple: 기본값으로, 유닛이 시작된 즉시 systemd는 유닛의 시작이 완료됐다고 판단한다.
  
  - forking: 자식 프로세스 생성이 완료되는 단계까지를 systemd가 시작이 완료됐다고 판단한다.
  - ExecStart

    - 시작 명령을 정의한다.
- ExecStop
  
  - 중지 명령을 정의한다.
  - WorkingDirectory
  - 해당 동작을 수행할 Directory를 지정한다.




- 실행이 안 될 경우
  - status 203이 뜨면서 실행이 안 될 경우 원인은 아래와 같다.
    - shebang을 추가하지 않은 경우.
    - 실행 파일 경로가 잘못된 경우.
    - 실행 파일에 실행 권한이 없을 경우.



- root 사용자가 아닌 사용자로 실행하려고 할 경우

  - `systemctl`은 기본적으로 root 권한이 있어야한다.
  - 만일 root 유저가 아닌 다른 사용자로 실행하고자 한다면 아래와 같이 `/etc/sudoers`에 추가해줘야한다.
    - `ALL=NOPASSWD`는 매번 아래 명령어들을 입력할 때마다 비밀번호를 입력하지 않아도 실행되도록 해준다.
    - 실행할 명령어를 `,`로 구분하여 나열해준다.

  ```bash
  <사용자명> ALL=NOPASSWD:/bin/systemctl start <service 명>, /bin/systemctl stop <service 명>, /bin/systemctl status <service 명>, /bin/systemctl restart <service 명>
  ```

  - 등록이 완료된 후에는 sudo를 붙여서 명령어를 실행하면 된다.
  - 또한 `/usr/lib/systemd/system` 내부의 파일들을 root 권한이 있어야 수정이 가능하므로 아래와 같이 root 이외의 사용자에게 읽고 쓰는 권한을 준다.

  ```bash
  setfacl -m u:<사용자명>:rw <service 파일 경로>
  ```



# etc

> 추후 필요할 때 공부 할 것들의 목록



- 응급복구

  > p.260~

  - root 계정의 비밀번호를 잊어버렸을 때 사용할 수 있는 방법



- GRUB

  > p.263

  - 우분투를 부팅할 때 처음 나오는 선택화면



- 커널 업그레이드

  > p.268

  - 커널 컴파일과 업그레이드



- X 윈도

  > p.283



- 하드디스크 관리

  > p.335

  - 하드디스크, 파티션, 사용자별 공간 할당