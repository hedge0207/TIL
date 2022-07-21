# 개요

- Github Actions
  - CI(Continuous Intergration)과 CD(Continuous Delivery)를 위한 platform이다.
    - build, test, deployment pipeline을 자동화해준다.
    - Workflow를 생성하여 build, test, deply 등을 할 수 있다.
  - Workflow를 실행시킬 수 있도록 Linux, macOS, Windows의 가상 머신을 제공한다.
    - github에서 제공하는 가상 머신을 사용하지 않고 self-hosted runner를 사용하는 것도 가능하다.



- Github Action의 구성 요소들
  - Workflows
    - 하나 이상의 job을 실행시킬 수 있는 자동화 프로세스이다.
    - YAML 파일에 정의되며, 각 workflow는 개별적인 YAML 파일에 정의되어야 한다.
    - repository에 특정 event가 발생했을 때 trigger되어 실행된다.
    - 수동으로 trigger 시킬 수도 있고, 일정 주기로 trigger시킬 수도 있다.
    - repository의 `.github/workflows` 폴더에 정의된다.
    - 하나의 repository는 복수의 workflow를 가질 수 있다.
  - Events
    - Workflow가 실행되도록 trigger 시키는 repository 내의 특정한 행동이다.
  - Jobs
    - Workflow 내에서 같은 runner 상에서 실행되는 여러 step들의 집합이다.
    - 각 step은 shell script나 실행시킬 수 있는 action이다.
    - 각 step은 순차적으로 실행되고, 다른 step들에 의존적이다.
    - 같은 runner에서 각 step은 data를 공유할 수 있다.
    - 기본적으로 job은 다른 job에 독립적이지만, 의존적일수도 있다.
    - job이 다른 job에 독립적일 경우 각 job은 병렬적으로 실행되지만, 하나의 job이 다른 job에 의존적일 경우, 각 job은 순차적으로 실행된다. 예를 들어 A가 B에 의존적이라면, B가 먼저 실행되고, B의 실행이 끝나면 A가 실행된다.
  - Actions
    - Github action에서 반복적으로 수행되는 작업을 처리하기 위한 custom application이다.
    - 직접 작성할 수도 있고 Github Marketplace에서 가져와서 사용할 수도 있다.
  - Runner
    - Workflow를 실행할 server이다.
    - 각 runner는 동시에 하나의 job만을 실행시켜야 한다.
    - Github action에서는 Linux, macOS, Windows 등을 제공(Github-hosted runner)하는데, 제공하는 runner를 사용하지 않고, 직접 runner를 구성(Self-hosted runner)할 수도 있다.



- Workflow 생성해보기

  - `.github/workflows` 폴더 내부에 YAML 파일을 생성한다.

  ```yaml
  # learn-github-actions.yml
  
  name: learn-github-actions
  on: [push]
  jobs:
    check-bats-version:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-node@v3
          with:
            node-version: '14'
        - run: npm install -g bats
        - run: bats -v
  ```

  - 위 파일을 작성한 상태에서 commit하고 push한다.
  - 설정
    - `name`(Optional): Workflow의 이름을 설정한다.
    - `on`: Workflow를 trigger시킬 event를 설정한다.
    - `jobs`: WorkFlow에서 실행시킬 job들을 정의한다.
    - `check-bats-version`: Job의 이름이다.
    - `runs-on`: Job을 실행시킬 runner를 정의한다.
    - `steps`: `check-bats-version` job에서 실행시킬 step들을 정의한다. 이 section 아래에 정의된 모든 설정들은 각각 하나의 action들이다.
    - `uses`: 어떤 action을 실행시킬지를 정의한다.
    - `run`: runner에서 실행시킬 명령어를 정의한다.
  - 위 workflow를 도식화하면 아래와 같다.

  ![Workflow overview](github_actions.assets/overview_actions_event.png)



- Github Actions의 필수적인 기능들

  - Workflow에서 변수 사용하기

  



# Action 사용하기

- 다른 사람이 만든 action 사용하기

  - Github Marketplace

    > https://github.com/marketplace?type=actions

    - 다른 사람이 정의한 action들을 모아 둔 공간이다.
    - 보안을 위해 action을 만든 사람이나 repository가 변경되면, 해당 action을 사용하는 모든 workflow가 실패하도록 설계되어 있다.

  - 위 사이트에 접속해서 사용하고자 하는 action을 선택 후 사용하면 된다.



- Action 추가하기

  - Action은 아래와 같은 곳들에 정의될 수 있다.
    - Workflow file과 같은 repository
    - Public repository
    - Docker hub에 배포된 docker image
  - Workflow file과 같은 repository에 추가하기
    - 이 경우 `<owner>/{repo}@{ref}`와 같이 적어주거나, action이 정의된 폴더의 위치를 적어준다.

  ```yaml
  # 만일 구조가 아래와 같다면
  |-- hello-world (repository)
  |   |__ .github
  |       └── workflows
  |           └── my-first-workflow.yml
  |       └── actions
  |           |__ hello-world-action
  |               └── action.yml		# action.yml에는 해당 action의 metadata가 담겨 있다.
  
  # 아래와 같이 action이 정의된 폴더의 위치를 적어준다.
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: ./.github/actions/hello-world-action
  ```

  - 다른 repository에 추가하기
    - 만일 workflow 파일이 있는 repository와 다른 repository에 action을 정의했다면 `<owner>/{repo}@{ref}`의 형태로 적어준다.

  ```yaml
  jobs:
    my_first_job:
      steps:
        - name: My first step
          uses: actions/setup-node@v3
  ```

  - Docker hub에 있는 action 사용하기
    - `docker://{image}:{tag}` 형태로 적어준다.

  ```yaml
  jobs:
    my_first_job:
      steps:
        - name: My first step
          uses: docker://alpine:3.8
  ```



- Action의 버전 정보 표기법

  - tags

  ```yaml
  steps:
    - uses: actions/javascript-action@v1.0.1
  ```

  - SHAs

  ```yaml
  steps:
    - uses: actions/javascript-action@172239021f7ba04fe7327647b213799853a9eb89
  ```

  - Branch

  ```yaml
  steps:
    - uses: actions/javascript-action@main
  ```

  

  

























































# 참고

- https://docs.github.com/en/actions





