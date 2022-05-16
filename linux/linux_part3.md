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

  - 등록된 service를 실행한다.

  ```bash
  $ systemctl start hello
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