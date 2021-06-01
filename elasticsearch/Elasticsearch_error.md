- `max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]`

  - 원인
    - 운영체제가 기본으로 사용하는 mmap 사이즈인 65530이 너무 작아서 발생
  - 해결
    - mmap 사이즈를 262144로 증가시킨다.
    - `/etc/sysctl.conf` 파일에 `vm.max_map_count=262144`를 추가 후 재부팅
    - 위 방식은 재부팅이 필요하기에, 라이브 서비스의 경우 아래 명령어를 통해 바로 적용이 가능하다(단, 재부팅시 초기화된다.)

  ```bash
  $ sudo sysctl -w vm.max_map_count=262144
  ```

  