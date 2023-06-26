# Jenkins

- Jenkins Docker로 설치하기

  - Docker hub에서 Jenkins official image를 다운 받는다.
    - 아래 image에는 blue ocean이 설치되어 있지 않으므로, blue ocean을 사용하려면, jenkins instance 생성 후 설치하거나, image를 다시 빌드해서 사용해야한다.

  ```bash
  $ docker pull jenkins/jenkins
  ```

  - docker-compose 파일 작성하기.
    - Jenkins는 브라우저를 통해 관리용 UI를 제공하는데 8080은 해당 페이지를 위한 port이다.
    - volume을 잡을 때 `/var/jenkins_home`의 권한 문제가 생길 수 있는데, 이때는 host 경로의 소유자를 1000으로 변경하면 된다.
    - 즉 아래 예시의 경우 `sudo chown 1000 jenkins-home`과 같이 변경하면 된다.

  ```yaml
  version: '3.2'
  
  
  services:
    theo-jenkins:
      image: jenkins/jenkins:latest
      container_name: theo-jenkins
      volumes:
        - ./jenkins-home:/var/jenkins_home
      restart: always
      ports:
        - 2376:2376
        - 8080:8080
  ```

  - 실행

  ```bash
  $ docker compose up
  ```

  - 관리 page 접속하기
    - 관리 page 용 port로 `<host>:<port>`와 같이 접속하면 Getting Started page로 연결되고, administrator password를 입력하라고 나온다.
    - Administrator password는 docker를 실행시킬 때 log에 출력이 되며, 만일 이 때 보지 못했다면, `/var/jenkins_home/secrets/initialAdminPassword` 경로에서 확인하면 된다.
    - Jenkins 실행시 자동으로 관리자 권한을 가진 admin이라는 이름의 user를 생성하는데, 해당 user의 password도 administrator password를 사용하면 된다.
    - 그 후 설치할 plugin을 선택하는 화면이 나오는데, 그냥 건너 뛰거나 suggested pluin만 설치하면 된다.
    - 만일 이 때 설치하지 못 한 plugin이 있더라도 추후에 관리 page의 `Manage Jenkins` - `Plugins`에서 설치가 가능하다.
    - 만일 그냥 건너뛰지 않고 plugin을 설치했다면, Admin 계정을 생성하는 창이 나오고, 그 이후에는 URL을 설정하는 창이 나오는데 모두 설정하고 나면 관리 page로 이동된다.



- Jenkins pipeline 생성하기

  - Jenkins Pipline(Pipeline)이란
    - Jenkins에서 CD(Continuous delivery) pipeline을 구현하고 통합하는 플러그인들의 모음이다.
  - Docker Pipeline plugin을 설치한다.
    - `Manage Jenkins`> `Plugins` page에서 설치할 수 있다.
    - 설치후 Jenkins를 재실행해야한다.
  - 아래 내용을 `Jenkinsfile`에 입력한 후 저장한다.
    - Jenkins home directory에 저장하면 된다(docker로 설치했을 경우 `/var/jenkins_home`)


  ```yaml
  pipeline {
      agent { docker { image 'python:3.8.0' } }
      stages {
          stage('build') {
              steps {
                  sh 'python --version'
              }
          }
      }
  }
  ```

  - `New Item`을 클릭한 후 `Multibranch Pipeline`을 선택한다.
    - `Branch Sources`에서 Add Source를 눌러 github credential 설정과 repository를 설정한다.
    - Credentials의 Username에는 github username입력하고, password에는 github access token을 입력하면 된다.
    - 그 후 Save를 누르면 자동으로 실행된다.