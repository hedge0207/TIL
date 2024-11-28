# 개요

> https://docs.github.com/en/actions

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




- Github Actions의 필수적인 기능들

  - 환경 변수 사용하기
    - Github Action에는 기본적으로 등록되어 있는 환경변수 들이 있다.
    - 만일 새로운 환경 변수를 등록하고자 한다면 아래와 같이 `env` 필드에 환경변수를 정의하면 된다.
    - 아래와 같이 정의한 환경변수는 `client.js` 파일에서 사용이 가능하다.

  ```yaml
  jobs:
    example-job:
        steps:
          - name: Connect to PostgreSQL
            run: node client.js
            env:
              POSTGRES_HOST: postgres
              POSTGRES_PORT: 5432
  ```

  - Script 추가하기
    - 아래와 같이 script 혹은 실행시킬 명령어를 정의할 수 있다.

  ```yaml
  jobs:
    example-job:
      steps:
        - name: Run build script
          run: ./.github/scripts/build.sh
          shell: bash
  ```

  - Job들 간에 data 공유하기
    - workflow가 실행되는 과정에서 생성한 파일을 artifact라 부르며, 아래와 같이 공유가 가능하다.

  ```yaml
  # 업로드하기
  jobs:
    example-job:
      name: Save output
      steps:
        - shell: bash
          run: |
            expr 1 + 1 > output.log
        - name: Upload output file
          uses: actions/upload-artifact@v3
          with:
            name: output-log-file
            path: output.log
  
  # 다운로드하기
  jobs:
    example-job:
      steps:
        - name: Download a single artifact
          uses: actions/download-artifact@v3
          with:
            name: output-log-file
  ```







## 표현식

- 표현식에 literal을 사용하는 것이 가능하다.

  - boolean, null, number, string
  - number의 경우 JSON에서 유효한 숫자 형식이어야 한다.
  - String의 경우 표현식 없이도 표현 가능하다.
    - 단, 표현식에서 사용할 경우 반드시 작은 따옴표(`'`)로 묶어줘야한다.
    - 만일 작은 따옴표 자체를 사용하고자 한다면 앞에 작은 따옴표 하나를 더 붙여주면 된다(큰 따옴표로 묶으면 error가 발생한다).

  ```yaml
  env:
    myNull: ${{ null }}
    myBoolean: ${{ false }}
    myIntegerNumber: ${{ 711 }}
    myFloatNumber: ${{ -9.2 }}
    myHexNumber: ${{ 0xff }}
    myExponentialNumber: ${{ -2.99e-2 }}
    myString: Mona the Octocat
    myStringInBraces: ${{ 'It''s open source!' }}
  ```



- 연산자
  - JavaScript에서 사용 가능한 연산자의 대부분을 사용할 수 있다.



- 비교

  - Github은 loose equality 비교를 택한다.
    - 만일 두 data의 type이 같지 않으면, 그 둘을 숫자로 변형하여 비교한다.

  | Type    | Result                                                       |
  | ------- | ------------------------------------------------------------ |
  | Null    | 0                                                            |
  | Boolean | true면 1, false면 0                                          |
  | String  | JSON 형식에 맞는 숫자 형식이면 해당 숫자로 변환, 아니면 NaN으로 변환, 빈 string은 0으로 변환 |
  | Array   | NaN                                                          |
  | Object  | NaN                                                          |

  - NaN과 NaN의 동등 비교(==)는 False를 반환한다.
  - Object는 오직 같은 instance일 때만 같은 것으로 간주된다(Array도 마찬가지).
  - 대소문자를 구분하지 않는다.



- 함수

  - Github은 표현식 내부에서 사용할 수 있는 내장 함수들을 제공한다.
    - 일부 내장 함수들은 비교를 위해 값을 string으로 변환한다.

  | Type    | Result                                                |
  | ------- | ----------------------------------------------------- |
  | Null    | ''                                                    |
  | Booelan | 'true', 'false'                                       |
  | Number  | 10진수 형식의 문자열, 큰 수의 경우 지수 형식의 문자열 |
  | Array   | 문자열로 변환하지 않는다.                             |
  | Object  | 문자열로 변환하지 않는다.                             |

  - `contains(search, item)`
    - `search`에 `item`이 있으면 true, 없으면 false를 반환한다.
    - 대소문자를 구분하지 않고 찾는다.
    - `search`에는 array나 string이 올 수 있다.

  ```yaml
  # 특정 evnet와 관련된 github issue 중에 bug라는 라벨이 있는지 확인
  contains(github.event.issue.labels.*.name, 'bug')
  ```

  - `startsWith(searchString, searchValue)`
    - `searchString`이 `searchValue`로 시작하면 true, 아니면 false를 반환한다.
    - `endsWith`도 있다.

  ```yaml
  startsWith('Hello world', 'He')
  ```

  - `format(string, replaceValue0, replaceValue1, ..., replaceValueN)`
    - python의 `format()`메서드와 유사하다.

  ```yaml
  format('Hello {0} {1} {2}', 'Mona', 'the', 'Octocat') 	# Hello Mona the Octocat
  ```

  - `join(array, optionalSeparator)`
    - Array 내부의 모든 값들을 string으로 합한다.
    - `optionalSeparator`는 string으로 합할 때 각 요소를 어떤 것으로 구분하여 합할지를 설정하는 것이다(기본값은 `,`).

  ```yaml
  join(github.event.issue.labels.*.name, '| ')	# bug| help wanted
  ```

  - `toJSON(value)`
    - value를 pretty-print JSON representation으로 변환하여 반환한다.
  - `fromJSON(value)`
    - JSON 형식의 데이터를 읽어서 JSON object로 변환하여 반환한다.
  - `hashFiles(path)`
    - file의 hash를 반환한다.

  ```yaml
  hashFiles('**/package-lock.json', '**/Gemfile.lock')
  ```



- Status check 함수들

  - `success()`
    - 이전의 step들이 fail되거나 cancel되지 않았으면 true를 반환한다.

  ```yaml
  steps:
    ...
    - name: The job has succeeded
      if: ${{ success() }}
  ```

  - `always()`
    - 어떠한 경우에도 step이 실행되도록 하기위해 사용한다.

  ```yaml
  if: ${{ always() }}
  ```

  - `failure()`
    - 이전의 step들 중 하나라도 fail이거나 cancel인 경우 true를 반환한다.
    - 의존하고 있는 작업이 있는 경우, 해당 작업이 fail되면 true를 반환한다.

  ```yaml
  steps:
    ...
    - name: The job has failed
      if: ${{ failure() }}
  ```



- Context

  - 표현식에 context를 사용할 수 있다.
  - 지원하는 context 목록은 다음과 같다.

  > https://docs.github.com/en/actions/learn-github-actions/contexts



## Docker 실행시키기

- Github actions에서 docker를 실행하고자 한다면 아래 조건을 만족해야 한다.
  - Github-hosted runner라면 반드시 ubuntu runner를 사용해야 한다.
  - Self-hosted runner라면 반드시 Docker가 설치된 linux를 사용해야 한다.



- 사전 준비

  - Dockerfile 작성하기

  ```dockerfile
  FROM alpine:3.10
  
  COPY entrypoint.sh /entrypoint.sh
  
  ENTRYPOINT ["/entrypoint.sh"]
  ```

  - Action metadata file 작성하기
    - `image`에는 repository 내의 dockerfile의 경로나 dockerhub의 url을 적어야 한다.

  ```yaml
  name: 'Hello World'
  description: 'Greet someone and record the time'
  inputs:
    who-to-greet:  # id of input
      description: 'Who to greet'
      required: true
      default: 'World'
  outputs:
    time: # id of output
      description: 'The time we greeted you'
  runs:
    using: 'docker'
    image: 'Dockerfile'
    args:
      - ${{ inputs.who-to-greet }}
  ```

  - Action code 작성하기

  ```bash
  # entrypoint.sh
  #!/bin/sh -l
  
  echo "Hello $1"
  time=$(date)
  echo "::set-output name=time::$time"
  ```

  - 작성한 파일에 실행 권한 추가하기

  ```bash
  $ chmod +x entrypoint.sh
  ```

  - commit하고 tag달고 push하기

  ```bash
  $ git add action.yml entrypoint.sh Dockerfile README.md
  $ git commit -m "My first action is ready"
  $ git tag -a -m "My first action release" v1
  $ git push --follow-tags
  ```



- Action 테스트 하기

  - `.github/workflows/main.yml`에 아래와 같이 workflow를 정의한다.

  ```yaml
  on: [push]
  
  jobs:
    hello_world_job:
      runs-on: ubuntu-latest
      name: A job to say hello
      steps:
        - name: Hello world action step
          id: hello
          uses: <계정>/<repository명>@v1
          with:
            who-to-greet: 'Mona the Octocat'
        # Use the output from the `hello` step
        - name: Get the output time
          run: echo "The time was ${{ steps.hello.outputs.time }}"
  ```

  - 이제 push가 발생할 때마다 위 workflow가 실행된다.



- Container 내부에서 job 실행하기

  - Job을 container 내부에서 실행하도록 할 수 있다.
    - `jobs.<job-id>.container`에 job을 실행시킬 container를 지정해준다.
    - docker hub에 등록된 image만 사용이 가능하다.

  ```yaml
  name: container test
  on: push
  
  jobs:
    container-job:
      runs-on: ubuntu-latest
      container: python:3.8.0
  
      steps:
        - name: check python version
          run: python --version
  ```

  - 위와 같이 단순히 image만 설정하는 것 외에도 세부 설정도 가능하다.

    > https://docs.docker.com/engine/reference/commandline/create/#options

    - 위 링크에 나와 있는 옵션 중 `--network`만 제외하고 모든 옵션을 사용 가능하다.

  ```yaml
  name: container test
  on: push
  
  jobs:
    container-job:
      runs-on: ubuntu-latest
      container:
        image: python:3.8.0
        volumes:
          - my_docker_volume:/volume_mount
          - /data/my_data
          - /source/directory:/destination/directory
  
      steps:
        - name: check python version
          run: python --version
  ```





## Self-hosted runner

- Self-hosted runner

  - github은 기본적으로 테스트를 위한 runner를 제공한다.
  - github이 제공하는 runner가 아닌, 직접 구성한 runner를 self-hosted runner라 한다.
    - Hardware, OS, software 적으로 github-hosted runner보다 자유도가 높다.
  - 물리적 hardware, 가상 hardware, 컨테이너, 클라우드 등으로 구성이 가능하다.

  - Github Actions와 30일 동안 연결된 적이 없으면 자동으로 삭제된다.



- Self-hosted runner의 조건
  - Self-hosted runner application을 설치하고 실행할 수 있어야한다.
  - Github Action과 communication이 가능해야한다.
  - Workflow를 실행할 수 있는 충분한 자원이 있어야한다.
    - Self-hosted runner application 자체는 약간의 자원만 있으면 된다.
    - 그러나 이를 통해 실행시킬 Workflow의 종류에 따라 필요한 자원의 양이 달라지게 된다.
  - Docker를 사용하는 workflow를 실행하고자 한다면 반드시 Linux를 사용해야하며, Docker가 설치되어 있어야 한다.



- 보안
  - Self-hosted runner는 private repository에만 사용하는 것을 권장한다.
  - 만일 누군가가 repository를 fork해서 악의적인 action을 넣은 후 해당 action을 실행하면 self-hosted runner로 사용하는 장치에 문제가 생길 수 있기 때문이다.
  - 항상 독립적인 가상 머신에서 workflow를 실행하고, workflow가 종료된 후에는 가상머신을 삭제하는 github-hosted runner는 이런 문제가 없다.



- Self-hosted runner 추가하기

  - 다양한 계층의 runner가 존재한다.
    - Repository-level runner는 하나의 repository에서 사용되는 runner이다.
    - Organization-level runner는 organization 내부의 모든 repository에서 사용되는 runner이다.
    - Enterprise-level runner는 enterprise account의 여러 organization에서 사용되는 runner이다.

  - 각 계층별 runner를 추가하기 위해 필요한 권한.
    - organization와 enterprise에 runner를 추가하려면 administrator여야 한다.
    - Repository에 runner를 추가하려면 repository owner여야 한다.

  - Repository-level runner 추가하기
    - repository의 메인 페이지에서 Settings를 클릭한다.
    - 왼쪽 sidebar에서 Actions-Runners를 클릭한다.
    - New self-hosted runner를 클릭한다.
    - 운영체제를 선택후 적혀 있는 안내를 따른다.

  ```bash
  # runner application을 설치할 폴더를 생성한다.
  $ mkdir actions-runner && cd actions-runner
  
  # runner application의 installer 다운 받는다.
  $ curl -o actions-runner-linux-x64-2.294.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.294.0/actions-runner-linux-x64-2.294.0.tar.gz
  
  # (선택) hash를 검증한다.
  $ echo "a19a09f4eda5716e5d48ba86b6b78fc014880c5619b9dba4a059eaf65e131780  actions-runner-linux-x64-2.294.0.tar.gz" | shasum -a 256 -c
  
  # 압축을 해제해 installer를 꺼낸다.
  $ tar xzf ./actions-runner-linux-x64-2.294.0.tar.gz
  
  # runner를 생성하고, configuration을 설정한다.
  $ ./config.sh --url <repository_url> --token <안내문에 나와 있는 token>
  
  # 실행한다.
  $ ./run.sh
  
  
  # 아래와 같은 메시지가 나오면 제대로 연결된 것이다.
  √ Connected to GitHub
  
  2019-10-24 05:45:56Z: Listening for Jobs
  ```

  - Workflow YAML 파일에 `runs-on`키워드의 값을 `self-hosted`로 변경한다.

  ```yaml
  jobs:
    hello_world_job:
      runs-on: self-hosted
      # (...)
  ```






## Workflow

- Workflow에는 아래의 세 가지가 반드시 포함되어야 한다.
  - Workflow를 trigger 시킬 event.
  - 하나 이상의 job.
  - Job의 각 step에서 실행 시킬 스크립트나 action.



- Workflow command

  - Workflow command로는 대표적으로 아래와 같은 것들을 할 수 있다.

    - 환경변수를 설정하여 action이 runner와 소통할 수 있도록 해준다.
    - 한 action의 output을 다른 action에서 사용할 수 있게 해준다.
    - debug message를 output log에 추가한다.

  - actions/toolkit

    > https://github.com/actions/toolkit
    >
    > https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#example-setting-a-value

    - Workflow command에서 사용할 수 있는 여러 함수들을 모아놓은 패키지다.
    - `::` 를 사용하여 workflow command를 사용할 수 있게 해준다.

  ```yaml
  # 예시 output parmeter 설정하기
  echo "::set-output name=<키>::<값>"
  # 실제 사용
  echo "::set-output name=action_fruit::strawberry"
  ```





## Job

- 개요

  - Job은 기본적으로 병렬적으로 실행된다.
    - `jobs.<job_id>.needs`를 통해 의존성을 추가함으로써 순차적으로 실행되게 할 수 있다.
    - 아래 예시에서 job3는 job1, job2가 성공적으로 실행 됐는지 여부와 관계 없이 완료만 되면 실행되고, job2는 job1이 성공적으로 실행이 완료되어야만 실행된다.

  ```yaml
  jobs:
    job1:
    job2:
      needs: job1
    job3:
      if: ${{ always() }}
      needs: [job1, job2]
  ```

  - 각 job들은 `runs-on`에 설정된 runner에서 실행된다.
  - 모든 job은 job_id라 불리는 고유한 식별자로 구별된다.
    - job_id는 숫자, 영문, `-`, `_`만 사용이 가능하다.
    - 첫 글자는 반드시 영문 또는 `_`여야한다.
    - 대소문자를 구분하지 않는다.
    - `jobs.<job_id>.name`을 통해 설정하는 것은 github UI 상에 보이는 이름이지 job_id가 아니다.



- matrix

  - 하나의 job에 여러 변수를 줌으로써 여러 개의 job을 생성한 것과 같은 효과를 주는 기능이다.
  - 예시
    - 아래와 같이 `version`과 `os`라는 두 개의 metrix를 생성했을 경우 그 둘을 조합하여 총 6개의 조합을 생성한다.
    - 그 후 github action은 해당 조합을 가지고 각각 job을 실행한다.
    - 즉 6번이 실행된다.

  ```yaml
  jobs:
    example_matrix:
      strategy:
        matrix:
          os: [ubuntu-18.04, ubuntu-20.04]
          version: [10, 12, 14]
      runs-on: ${{ matrix.os }}
      steps:
        - uses: actions/setup-node@v3
          with:
            node-version: ${{ matrix.version }}
  ```

  - `include`를 통해 matrix 추가하기
    - 이미 존재하는 matrix를 확장하거나, 새로운 설정을 추가할 때 사용할 수 있다.
    - `include`를 통해 추가되는 값들은  {key:value} 쌍의 형태며, 아래의 규칙에 따라 추가된다.
    - 기존 matrix들 중 key와 value가 한 쌍이라도 같은 값이 있다면 해당 matrix에만 추가된다.
    - 기존 matrix들의  key에 존재하지 않는 key라면 모든 matrix에 추가된다.
    - 기존 matrix에 key는 있는데 value는 같은 것이 없다면 새로운 조합으로 추가된다.
    - 기존 matrix의 value는 덮어씌워지지 않지만, `include`로 추가된 value는 덮어씌워진다.
    - `include`를 통해 새롭게 생성된 matrix는 확장이 불가능하다.
  - `include` 예시

  ```yaml
  strategy:
    matrix:
      fruit: [apple, pear]
      animal: [cat, dog]
      include:
        - color: green
        - color: pink
          animal: cat
        - fruit: apple
          shape: circle
        - fruit: banana
        - fruit: banana
          animal: cat
          
  
  # fruit와 animal을 조합한 기존 조합은 아래와 같다.
  {fruit: apple, animal: cat}
  {fruit: apple, animal: dog}
  {fruit: pear, animal: cat}
  {fruit: pear, animal: dog}
  
  # 여기에 첫 번째 object({color: green})가 추가되면 다음과 같이 변한다.
  # color는 기존 조합의 어디에도 존재하지 않는 key이므로 모든 matrix에 추가된다.
  {fruit: apple, animal: cat, color: green}
  {fruit: apple, animal: dog, color: green}
  {fruit: pear, animal: cat, color: green}
  {fruit: pear, animal: dog, color: green}
  
  # 두 번째 object({color:pink, animal: cat})
  # {animal: cat}이 일치하는 matrix에만 추가되며, color는 include를 통해 추가된 것이므로 덮어씌우는 것이 가능하다.
  {fruit: apple, animal: cat, color: pink}
  {fruit: apple, animal: dog, color: green}
  {fruit: pear, animal: cat, color: pink}
  {fruit: pear, animal: dog, color: green}
  
  # 세 번째 object({fruit:apple, shape:circle})
  # {fruit:apple}이 일치하는 matrix에만 추가된다.
  {fruit: apple, animal: cat, color: pink, shape: circle}
  {fruit: apple, animal: dog, color: green, shape: circle}
  {fruit: pear, animal: cat, color: pink}
  {fruit: pear, animal: dog, color: green}
  
  # 네 번째 object({fruit: banana})
  # matrix 중 key:value 쌍이 일치하는 metrix가 없으므로 새로운 matrix를 생성한다.
  {fruit: apple, animal: cat, color: pink, shape: circle}
  {fruit: apple, animal: dog, color: green, shape: circle}
  {fruit: pear, animal: cat, color: pink}
  {fruit: pear, animal: dog, color: green}
  {fruit: banana}
  
  # 다섯 번 째 object({fruit: banana, animal:cat})
  # {animal:cat}이 있긴 하지만 기존의 key인 fruit를 덮어쓰지 않고는 추가가 불가능하다.
  # 또한 {fruit: banana}는 include를 통해 추가된 matrix이므로 확장이 불가능하다.
  # 따라서 새로운 matrix를 생성한다.
  {fruit: apple, animal: cat, color: pink, shape: circle}
  {fruit: apple, animal: dog, color: green, shape: circle}
  {fruit: pear, animal: cat, color: pink}
  {fruit: pear, animal: dog, color: green}
  {fruit: banana}
  {fruit: banana, animal: cat}
  ```

  - `exclude`를 통해 특정 조합을 제외하는 것도 가능하다.
    - `jobs.<job_id>.strategy.matrix.exclude`를 통해 제외할 것들을 설정한다.
    - 아래의 경우 총 12개의 matrix가 생성되는 데 `os`가 windows-latest이면서 `version`이 16인 matrix 2가지와 `os`가 macos-latest, `version`이 12, `emvironment`가 production인 경우 1가지가 빠져 9번만 실행된다.

  ```yaml
  strategy:
    matrix:
      os: [macos-latest, windows-latest]
      version: [12, 14, 16]
      environment: [staging, production]
      exclude:
        - os: macos-latest
          version: 12
          environment: production
        - os: windows-latest
          version: 16
  runs-on: ${{ matrix.os }}
  ```

  - 한번에 실행할  job의 개수 제한하기
    - 기본적으로 `matrix`를 통해 생성된 모든 조합을 병렬적으로 실행한다.
    - 만일 동시에 실행되는 job의 개수에 제한을 두고자 하면 `jobs.<job_id>.strategy.max-parallel` 값을 설정해주면 된다.



## Checkout

> https://www.daleseo.com/github-actions-checkout/

- Checkout
  - Git에서의 checkout은 코드 저장소에서 특정 브랜치로 전환하는 작업을 의미한다.
  - Github actions에서의 chekcout은 github의 코드 저장소에 올려둔 코드를 runner에 내려 받은 후 특정 브랜치로 전환하는 행위를 말한다.



- git에서 제공하는 checkout action

  > https://github.com/actions/checkout

  - Checkout 작업을 모든 workflow에서 매번 쉘 스크립트로 작성해줘야 한다면, 매우 불편할 것이다.
  - Github이 제공하는 checkout action은 checkout을 훨씬 간편하게 할 수 있도록 도와준다.

  - 사용하기
    - Workflow 설정 파일에 아래와 같이 action을 지정해준다.
    - 실행이 완료되면 working directory에 코드 저장소의 코드가 받아진다.
  
  ```yaml
  on: [push]
  jobs:
    production-deploy:
      runs-on: ubuntu-latest
      steps:
        # checkout action을 설정해준다.
        - uses: actions/checkout@v3
  ```
  



## Containerized services

- 하나의 job에서 여러 개의 docker container를 실행할 수 있도록 도와주는 기능이다.

  - Job이 시작될 때 container를 생성하며, job이 종료되면 container를 삭제한다.
    - 하나의 Job 내부에 있는 모든 step에서 service container에 접근 가능하다.
  - `jobs.<job_id>.services` 아래에 실행 시킬 docker container들을 입력한다.

  ```yaml
  name: services test
  on: push
  
  jobs:
    services-test-job:
      runs-on: ubuntu-latest
      container: python:3.8.0
  
      services:
        # elasticsearch라는 label을 설정
        elasticsearch:
          # container를 생성할 docker image를 입력한다.
          image: elasticsearch:8.1.3
          # 다 띄워질 때 까지 대기하도록 healthcheck를 실행한다.
          options: >-
            --health-cmd "curl localhost:9200"
            --health-interval 10s
            --health-timeout 5s
            --health-retries 5
  
      steps:
        - uses: actions/checkout@v3
        - name: check elasticsearch connection
          run: curl elasticsearch:9200
  ```



- Runner machine과 Docker container

  - Service를 runner machine에서 직접 실행하도록 할 수도 있고, Docker Container에서 실행되도록 할 수 있다.
    - Service container가 어디서 실행되냐에 따라  network 설정이 달라지게 된다.
    - 위 예시의 경우 Python container 내부에서 elasticsearch container service를 실행하는 것이다.
    - 만일 container를 따로 지정해주지 않았다면 runner container에서 실행될 것이다.
  - Container에서 실행될 경우
    - Github이 Docker의 bridge network를 사용하여 container와 service container를 연결해준다.
    - 따라서 위 예시에서와 같이 step에서 접근할 때는 service container의 label을 host로 해서 접근하면 된다.
    - 기본적으로, 같은 docker network에 속한 모든 컨테이너는 모든 port를 다른 컨테이너들에게 노출하기 때문에, port 설정도 추가적으로 해줄 필요가 없다. 
  - Runner machine에서 실행할 경우
    - `localhost:<port>` 혹은 `127.0.0.1:<port>`를 통해 접근 가능하다.
    - 이 경우 service container는 port를 노출시키지 않기 때문에 직접 port를  mapping해줘야한다.

  ```yaml
  name: Redis Service Example
  on: push
  
  jobs:
    runner-job:
      runs-on: ubuntu-latest
  
      services:
        nginx:
          image: nginx
          ports:
            - 8080:80
        redis:
          image: redis
          ports:
            - 6379/tcp
  ```










# Github Container Registry

- Container Registry
  - 조직 또는 개인 계정 내에 container image를 저장할 수 있게 해주는 기능이다.
    - Image를 특정 repository와 연결하는 것도 가능하다.
    - Github Packages를 통해 사용이 가능하다.
  - Personal access token 발급이 필요하다.
    - Github Packages는 personal access token(classic)을 통해서만 인증이 가능하므로, personal access token(classic)을 발급 받아야 한다.
    - Personal access token(classic)의 생성은 Github profile → Settings → Developer Settings → Personal access tokens → Tokens(classic)에서 할 수 있다.



- 테스트용 이미지 생성하기

  - FastAPI application 작성

  ```python
  from fastapi import FastAPI
  import uvicorn
  
  
  app = FastAPI()
  
  @app.get("/ping")
  def ping():
      return "pong"
  
  if __name__ == "__main__":
      uvicorn.run(app, host="0.0.0.0", port=8098)
  ```

  - `requirements.txt` 작성

  ```txt
  pydantic==2.5.3
  pydantic_core==2.14.6
  pydantic-settings==2.1.0
  uvicorn==0.27.0.post1
  fastapi==0.109.0
  requests==2.31.0
  ```

  - Dockerfile 작성

  ```dockerfile
  FROM python:3.12.0
  
  COPY ./main.py /main.py
  COPY ./requirements.txt /requirements.txt
  
  RUN pip install -r requirements.txt
  
  ENTRYPOINT ["/bin/bash", "-c", "python -u main.py"]
  ```

  - Image build
    - Image의 이름은 `ghcr.io/<user_name>/<image_name>[:<tag>]` 형식이어야 한다.

  ```bash
  $ docker build -t ghcr.io/<user_name>/test-app:1.0.0 .
  ```




- Github Container Registry 사용하기

  - Github Container Registry에 로그인하기
    - 위에서 발급 받은 토큰으로 로그인한다.

  ```bash
  $ docker login ghcr.io -u <user_name> -p <token>
  ```

  - Image push하기

  ```bash
  $ docker push ghcr.io/<user_name>/test-app:1.0.0
  ```

  - Image pull하기

  ```bash
  $ docker pull ghcr.io/<user_name>/test-app:1.0.0
  ```

