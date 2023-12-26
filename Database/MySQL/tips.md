# Workbench 사용 방법

- Table을 우클릭 후 `Send to SQL Editor` - `Create Statement`를 클릭하면 해당 table을 생성하는 SQL문을 볼 수 있다.



- 설정들
  - `Edit` - `Format` - `UPCASE keywords`를 선택하면 예약어만 모두 대문자로 변경시켜준다.
  - `Edit` - `Preferences` - `SQL Editor` - `UPPERCASE keywords on completion`을 선택하면 자동완성 되는 예약어를 모두 대문자로 변경한다.



- Administration

  > Navigator에서 Administration 탭을 click하면 된다.

  - `Server Status`
    - 현재 접속된 서버의 상태를 보여준다.
  - `Client Connection`
    - 연결된 client들의 정보와 휴면(sleep) 상태인지 여부를 보여준다.
    - Client를 선택 후 우클릭하면 `Kill Connection(s)`로 connection을 끊을 수 있다.
  - `User and Privileges`
    - MySQL 사용자를 관리할 수 있다.
  - `Status and System Variables`
    - 서버에 설정된 system variable들을 확인할 수 있다.
    - `Value` 부분을 더블 클릭하여 값을 변경할 수 있다.
  - `Data export`와 `Data Import/Restore`
    - 백업 및 복원과 관련된 부분이다.
  - `Startup/Shutdown`
    - MySQL 서버의 현재 작동 상태를 확인할 수 있다.
    - MySQL 서버의 중지와 시작도 할 수 있다.
  - `Servers Logs`
    - 서버에 기록된 오류, 경고 등의 로그를 확인할 수 있다.
  - `Option File`
    - MySQL의 핵심 설정 파일인 my.ini file의 내용을 GUI 모드로 보여준다.
    - 설정을 변경해서 적용시키면 my.ini file을 에디터로 편집하는 것과 동일한 효과를 갖는다.
  - `DashBoard`
    - 네트워크, MySQL 서버, InnoDB의 상태를 그래픽으로 보여준다.
  - `Performance Reports`
    - 입출력이 오래 걸린 파일, 비용이 많이든 쿼리문, DB 통계 등의 항목을 조회하고 결과를 내보낼 수 있다.
  - `Performance Schema Setup`
    - 성능에 대한 설정을 할 수 있다.