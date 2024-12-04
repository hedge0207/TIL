# Poetry

- Dependency 관리 및 packaging을 위한 Python package이다.
  - Python 3.8 이상이 요구된다.
  - Windows, Linux, macOS 등에서 모두 사용이 가능하다.
  - Poetry는 반드시 전용 가상환경에 설치해야 한다.
    - 그렇지 않을 경우 Poetry의 dependency들이 의도치 않게 삭제되거나 upgrade 될 수 있기 때문이다.



- pip가 있는 데 Poetry가 필요한 이유

  - Python은 기본적으로 pip라는 package manager(&dependency manager)를 제공한다.
    - 그런데, pip에는 몇 가지 문제들이 있다.

  - pip의 문제점들
    - Dependency 충돌이 발생했을 때 잘 처리하지 못 한다.
    - Lock file이 없어서 사용자가 requirements file을 잘 작성하는 수 밖에 없다.
    - 개발 환경과 운영 환경에서 필요한 package가 다를 경우(예를 들어 운영 환경에서는 black이나 pytest등의 package들은 사용하지 않을 확률이 높다) pip는 각 환경을 위한 requirements file을 따로 작성해야한다.
  - Poetry는 pip의 위와 같은 문제점들을 해결하고자 등장했다.



- 설치

  - Poetry를 설치할 가상 환경을 생성한다.
    - 가상환경을 venv package로 사용해도 되고, conda로 생성해도 된다.

  ```bash
  # venv 사용
  $ python -m venve <가상환경 이름>
  
  # conda 사용
  $ conda create -n <가상 환경 이름> (python=python 버전)
  ```

  - 가상 환경을 활성화한다.

  ```bash
  # venv 사용
  $ source ./<가상환경 이름>/bin/activate
  
  # conda 사용
  $ conda activate <가상환경 이름>
  ```

  - Poetry를 설치한다.

  ```bash
  $ pip install poetry
  ```

  - 자동 완성 활성화하기
    - Poetry는 `tab`을 눌렀을 때 자동완성이 되도록 설정할 수 있다.
    - Bash, Fixh, Zsh에서 자동완성을 지원한다.

  ```bash
  # bash의 경우 아래와 같이 활성화시키면 된다.
  $ poetry completions bash >> ~/.bash_completion
  ```



- 기본적인 사용법

  - 새로운 project 생성
    - `--name` option으로 project의 이름을 지정할 수 있다.
  
  
  ```bash
  $ poetry new <project-name>
  
  # 아래와 같은 구조로 project가 생성된다.
  <project-name>
  ├── pyproject.toml
  ├── README.md
  ├── <project_name>
  │   └── __init__.py
  └── tests
      └── __init__.py
  ```
  
  - `pyproject.toml`
    - Project의 dependency를 관리하기 위한 file이다.
    - 최초 생성시 아래와 같이 생성된다.
  
  ```toml
  [tool.poetry]
  name = "poetry-demo"
  version = "0.1.0"
  description = ""
  authors = ["foo <foo@42bar.com>"]
  readme = "README.md"
  
  [tool.poetry.dependencies]
  python = "^3.9"
  
  
  [build-system]
  requires = ["poetry-core"]
  build-backend = "poetry.core.masonry.api"
  ```

  - Project의 dependency들은 `tool.poetry.dependencies`에 작성하면 되며, 아래와 같이 명령어로도 추가할 수 있다.
  
  ```bash
  $ poetry add <dependency>
  ```

  - 위와 같이 새로운 project를 생성할 수도 있고, 기존 project에 적용할 수도 있는데, 기존 project에 적용하고자 하면 아래와 같이 하면 된다.
  
  ```bash
  $ cd pre-existing-project
  $ poetry init
  ```
  
  - Dependency 설치하기
    - 아래 명령어를 실행하면 `pyproject.toml` file을 읽어 필요한 package들을 설치한다.
    - 설치가 끝나고 나면  `poetry.lock` file을 생성하는데, 여기에는 다운 받은 package들과 각 package들의 version 정보를 작성한다.
    - `poetry.lock` file을 사용하여 project에 참여하는 모두가 동일한 version의 package를 사용할 수 있게 된다.
  
  ```bash
  $ poetry install
  ```
  
  - `poetry.lock` 파일이 있는 상태에서 `poetry install` 명령어를 실행할 경우
    - `poetry.lock` file은 project를 생성할 때 함께 생성되는 것이 아니라, `poetry install` 명령어를 최초로 실행했을 때 생성된다.
    - 따라서 `poetry.lock` file이 있다는 것은 기존에 `poetry install` 명령어를 실행한 적이 있다는 의미이다.
    - `poetry.lock` file이 있다면 `pyproject.toml`에서 설치해야 하는 dependency들을 확인하고, `poetry.lock` file에서 각 package들의 version 정보를 확인하여 정확히 일치하는 version을 설치한다.



- Dependency version 정의하기

  - 아래와 같은 다양한 방식으로 dependency의 version을 정의할 수 있다.
  - Caret requirements
    - Caret requirements는 SemVer(Semantic Versioning)과 호환되도록 version을 정의하는 방식이다.
    - 가장 왼쪽의 0이 아닌 숫자가 달라지지 않는 한 update를 수행한다.
    - 예시는 아래 표와 같다.

  | requirement | versions allowed | explanation                                                  |
  | ----------- | ---------------- | ------------------------------------------------------------ |
  | ^1.2.3      | >=1.2.3 < 2.0.0  | 가장 왼쪽의 0이 아닌 숫자인 major version 1이 변경되지 않는 한 update를 허용한다. |
  | ^1          | >=1.0.0 < 2.0.0  | -                                                            |
  | ^0.2.3      | >=0.2.3 <0.3.0   | 가장 왼쪽의 0이 아닌 숫자인 minor version 2가 변경되지 않는 한 update를 허용한다. |

  - Tilde requirements
    - 오직 patch level의 update만 허용하지만, major version만 입력하는 경우 minor version의 update도 허용한다.

  | requirment | versions allowed | explanation                                                  |
  | ---------- | ---------------- | ------------------------------------------------------------ |
  | ~1.2.3     | >=1.2.3 < 1.3.0  | patch level의 update만 허용한다.                             |
  | ~1.2       | \>=1.2.0 <1.3.0  | patch level의 update만 허용한다.                             |
  | ~1         | \>=1.0.0 <2.0.0  | major version만 입력할 경우, minor level의 update도 허용된다. |

  - Wildcard requirements
    - Wildcard가 허용하는 한 가장 최근 version으로 update한다.

  | requirment | versions allowed | explanation                                                  |
  | ---------- | ---------------- | ------------------------------------------------------------ |
  | *          | \>=0.0.0         | 모든 version이 허용된다.                                     |
  | 1.*        | >=1.0.0 <2.0.0   | 1 major version에 대한 모든 version이 허용된다.              |
  | 1.2.*      | \>=1.2.0 <1.3.0  | 1 major version과 2 minor version에 대한 모든 version이 허용된다. |

  - Exact requirements
    - 특정 version을 설정한다.
    - `==`를 사용한다.

  ```toml
  ==1.2.3
  ```

  - Inequality requirments
    - Version의 범위를 설정하거나, 특정 version을 피하도록 설정할 수 있다.

  ```toml
  >= 1.2.0
  > 1
  < 2
  != 1.2.3
  ```

  - Multiple requirements
    - 콤마로 구분하여 여러 version을 설정할 수 있다.

  ```toml
  >= 1.2, < 1.5
  ```



- 가상 환경을 생성하여 poetry를 설치한 후 해당 가상환경을 사용하면 poetry의 가상환경은 사용하지 않게된다.

  - 예를 들어 아래와 같이 poetry를 설치했다고 가정해보자.

  ```bash
  $ python -m venv test
  $ source test/bin/activate
  $ pip install -U pip
  $ pip install poetry
  ```

  - 이 상태에서 poetry를 아래와 같이 실행하고

  ```bash
  $ poetry new demo
  $ cd demo
  $ poetry add elasticsearch
  ```

  - 설치된 package 목록을 확인해보면 위에서 설치한 elasticsearch가 포함된 것을 확인할 수 있다.
    - 이는 poetry가 제공하는 가상 환경이 아닌 위에서 사용자가 직접 생성한 test라는 가상환경에 elasticsearch가 설치된 것이다.

  ```bash
  $ pip list
  ```

  - 만약 이 때 elasticsearch pakcage를 삭제하면 문제가 발생한다.
    - 아래 명령어를 실행하면 elasticsearch가 정상적으로 삭제되지만, 이후부터는 poetry 명령어 실행시 module not found error가 발생하면서 실행되지 않게 된다.

  ```bash
  $ poetry remove elasticsearch
  ```

  - 문제의 원인
    - 위에서 poetry를 통해 elasticsearch package를 설치하긴 했으나 이는 사실 poetry의 가상 환경이 아닌 사용자가 생성한 가상 환경에 설치된 것이다.
    - `poetry remove`를 통해 elasticsearch를 제거할 때 역시 poetry의 가상 환경에서 elasticsearch를 삭제한 것이 아닌 사용자가 생성한 가상 환경에 설치된 것이다.
    - poetry와 elasticsearch package는 동일한 dependency(e.g. urllib3, certifi)를 가지고 있다.
    - test라는 가상환경에서 elasticsearch가 삭제되면서 elasticsearch의 dependency들도 함께 삭제되는데, 이 때 poetry의 dependency들도 함께 삭제된다.
    - 따라서 poetry 실행시 module not found error가 발생하면서 poetry가 정상적으로 실행되지 않는다.
  - 해결 방법
    - poetry는 사용자가 생성한 가상 환경에 설치를 하고, poetry는 poetry의 가상환경에서 실행해야한다.
    - poetry의 가상환경에서 실행하기 위해서는 사용자가 생성한 가상 환경을 activate 하지 않아야한다.
    - 사용자가 생성한 가상 환경을 activate 하지 않고 poetry를 실행하기 위해 사용자가 생성한 가상 환경 내에서 poetry가 설치된 경로를 찾아 poetry를 바로 실행시켜준다.

  ```bash
  $ python -m venv test
  $ source test/bin/activate
  $ pip install -U upgrade pip
  $ pip install poetry
  
  # 여기서부터 달라진다.
  $ test/bin/poetry new demo
  $ cd demo
  $ ../test/bin/poetry add elasticsearch
  ```

  - 위 명령어를 실행하고 다시 사용자가 생성한 가상 환경을 실행시켜 package들을 확인해보면, 사용자가 생성한 가상 환경에는 elasticsearch가 포함되지 않은 것을 확인할 수 있다.

  ```bash
  $ source ../test/bin/activate
  $ pip list
  ```



- Dependency group

  - Dependency들을 group으로 묶을 수 있는 기능을 제공한다.
    - 이는 dependency들을 보다 편리하게 관리할 수 있게 해준다.
    - 또한 이를 통해 특정 상황에서만 필요한 dependency들을 따로 관리하는 것이 가능하다.
    - 예를 들어 test에 필요한 pytest 등의 dependency는 운영 환경에는 필요하지 않다.
    - 따라서 test에만 필요한 dependency들을 group으로 묶고 최종 배포에는 포함되지 않도록 관리하는 것이 좋다.

  - `pyproject.toml`에 아래와 같이 dependency group을 선언할 수 있다.
    - `tool.poetry.group.<group>` 형태로 선언한다.

  ```toml
  [tool.poetry.group.test]
  
  [tool.poetry.group.test.dependencies]
  pytest = "^6.0.0"
  pytest-mock = "*"
  ```

  - 모든 dependency들은 각 group간에 호환이 가능해야한다.
    - 어떤 dependency가 특정 group에서만 사용된다고 해서 다른 group의 dependency와 호환되지 않아도 되는 것이 아니다.
    - 모든 group의 dependency들은 group과 무관하게 호환되어야한다.
  - Optional한 group 선언하기
    - 아래와 같이 `optional = true`로 설정하면 해당 group은 optional group이 된다.

  ```toml
  [tool.poetry.group.docs]
  optional = true
  
  [tool.poetry.group.docs.dependencies]
  mkdocs = "*"
  ```



- Dependency synchronization

  - `peotry.lock`에 정의된 locked dependency들 중에서 불필요한 것들을 제거하는 과정이다.
    - 이를 통해 `poetry.lock` file에 있는 locked dependency들은 environment에 하나만 존재한다는 것이 보장된다.
  - `poetry install`시에 `--sync` option을 주면 된다.

  ```bash
  $ poetry install --sync
  ```

  - Dependency group과 관련된 option들과 함께 사용할 수 있다.

  ```bash
  $ poetry install --without dev --sync
  $ poetry install --with docs --sync
  $ poetry install --only dev
  ```

  - `--sync` option을 사용하지 않고 install할 경우 이미 설치된 optional group의 subset들을 삭제하지 않고도 이들을 설치할 수 있다.
    - 이는 multi-stage Docker build시에 굉장히 유용할 수 있다.





## 명령어

- `new`

  - 새로운 project를 생성하는 명령어이다.

  ```bash
  $ poetry new <package-name>
  ```

  - `--name` option을 통해 folder명과 package 명을 다르게 설정할 수 있다.

  ```bash
  $ poetry new <folder-name> --name <package-name>
  ```

  - 만약 depth가 있는 구조를 원한다면 아래와 같이 `.`을 사용하여 입력하면 된다.

  ```bash
  $ poetry new --name my.package my-package
  
  # 아래와 같이 project가 생성된다.
  my-package
  ├── pyproject.toml
  ├── README.md
  ├── my
  │   └── package
  │       └── __init__.py
  └── tests
      └── __init__.py
  ```

  - `src`  directory가 필요할 경우 `--src` option을 주면 된다.

  ```bash
  $ poetry new --src <package-name>
  
  # 아래와 같은 구조로 project가 생성된다.
  my-package
  ├── pyproject.toml
  ├── README.md
  ├── src
  │   └── my_package
  │       └── __init__.py
  └── tests
      └── __init__.py
  ```



- `init`

  - Poetry로 관리되고 있지 않던 project에 `pyproject.toml` file을 생성해준다.
    - Interactive shell로 `pyproject.toml` file을 생성할 때 필요한 정보들을 받는다.

  ```bash
  $ poetry init
  ```

  - Interactive shell에서 입력하지 않고, 아래와 같은 option들을 미리 지정해주는 것도 가능하다.
    - `--name`
    - `--description`
    - `--author`
    - `--python`
    - `--dependency`
    - `--dev-dependency`



- `install`

  - `pyproject.toml` file을 읽어서 dependency들을 resolve하고 설치한다.
    - 만약 `poetry.lock` file이 있다면, version을 resolve하는 대신 해당 file에 정의된 정확한 version들을 설치한다.

  ```bash
  $ poetry install
  ```

  - `--without`
    - 설치시에 제외할 dependency group들을 설정할 수 있게 해준다.

  ```bash
  $ poetry install --without foo,bar
  ```

  - `--with`
    - 설치시에 함께 설치할 optional dependency group들을 설정할 수 있게 해준다.
    - `--without`과 함께 쓸 경우 `--without`이 우선권을 가진다.

  ```bash
  $ poetry install --with foo,bar
  ```

  - `--only`
    - 특정 dependency group들만 설치하도록 설정할 수 있게 해준다.

  ```bash
  $ poetry install --only foo,bar
  ```

  - `--only-root`
    - Dependency는 설치하지 않고, project만 설치할 수 있게 해준다.

  ```bash
  $ poetry install --only-root
  ```

  - `--no-root`
    - Package(project) 자체는 설치하지 않는다.

  ```bash
  $ poetry install --no-root
  ```

  - `--no-directory`
    - Directory path를 설정한 dependency들은 설치하지 않는다.

  ```bash
  $ poetry install --no-directory
  ```

  - `--sync`
    - Environment를 동기화할 수 있게 해준다.

  ```bash
  $ poetry install --sync
  ```

  - `--extras`(`-E`)
    - extras들을 설치할 수 있게 해준다.
    - `--all-extras`를 입력하면 모든 extra들을 설치한다.

  ```bash
  $ poetry install --extras "mysql pgsql"
  $ poetry install -E mysql -E pgsql
  $ poetry install --all-extras
  ```

  - `--compile`
    - 기본적으로 `poetry install`시에는 Python source file을 bytecode로 compile하지 않는데, 이를 통해 설치 속도를 올릴 수 있기 때문이다.
    - 그러나 첫 실행시에는 Python이 자동으로 source code를 compile한다.
    - 만약 설치시에 source file을 compile하고자 한다면 `--compile` option을 주면 된다.
    - 만약 `installer.modern-installation`이 `false`로 설정되어 있다면 `--compile` option은 아무 영향도 미치지 못하는데, 이는 이전 installer는 항상 source file을 compile하기 때문이다.

  ```bash
  $ poetry install --compile
  ```

  - `--dry-run`
    - 실행 결과만 보여주고 실제 실행하지는 않는다.
  - `--without dev`
    - Dev dependency 들은 설치하지 않는다(`--only main`도 동일하다).
    - 이전 버전에서는 `--no-dev` 였으나 현재는 deprecated 됐다.
  
  ```bash
  $ poetry install --no-dev



- `lock`

  - `pyproject.toml` 파일에 있는 dependency들을 lock한다.
    - Lock file을 갱신한다.
  - `--no-update`
    - 기본적으로 `lock`이 실행되면, dependency들은 호환 가능한 가장 최근 버전으로 lock된다.
    - 만약 최신 버전으로 update를 원하지 않는다면 이 옵션을 주면 된다.

  ```bash
  $ poetry lock --no-update
  ```



- `update`

  - Dependency를 가장 최신 version으로 update하기 위해 사용한다.

    - 실행시에 `poetry.lock` file도 자동으로 update된다.
    - 일부 package들만 update하고자 할 경우 아래와 같이 뒤에 update할 package들을 입력하면 된다.

    - 주의할 점은 `pyproject.toml`에 정의한 version을 넘어서 update하지는 않는다는 점이다.

  ```bash
  $ poetry update [package1 package2 ...]
  ```

  - `--lock`
    - 실제 Update는 실행하지 않고, lockfile만 update한다.

  ```bash
  $ poetry update --lock
  ```

  - 아래와 같은 option들은 `install`과 공유한다.
    - `--without`
    - `--with`
    - `--only`
    - `--dry-run`



- `add`

  - `pyproject.toml` file에 dependency를 추가한다.
    - `@` 등을 사용하여 제약 조건을 추가할 수 있다.
    - 만약 이미 있는 dependency를 추가하려 할 경우 error가 발생한다.
    - 그러나 constraint를 정의할 경우 정의한 constraint에 따라 `pyproject.toml` file이 update된다.

  ```bash
  $ poetry add <pacakge> [package2 ...]
  
  # 예시
  $ poetry add pendulum@^2.0.5
  
  $ poetry add pendulum@~2.0.5
  
  $ poetry add "pendulum>=2.0.5"
  
  $ poetry add pendulum==2.0.5
  ```

  - `git` dependency는 아래와 같이 추가가 가능하다.

  ```bash
  $ poetry add git+https://github.com/sdispater/pendulum.git
  
  # ssh connection을 사용해야 할 경우
  $ poetry add git+ssh://git@github.com/sdispater/pendulum.git
  
  # 특정 branch, tag 등에서 가져와야 할 경우 
  $ poetry add git+https://github.com/sdispater/pendulum.git#develop
  $ poetry add git+https://github.com/sdispater/pendulum.git#2.0.5
  
  # 특정 sub dir에서 가져와야 할 경우
  $ poetry add git+https://github.com/myorg/mypackage_with_subdirs.git@main#subdirectory=subdir
  ```

  - Local directory에서 추가할 경우 아래와 같이 경로를 입력하면 된다.

  ```bash
  $ poetry add ./my-package/
  $ poetry add ../my-package/dist/my-package-0.1.0.tar.gz
  ```

  - Extra를 설치해야 할 경우

  ```bash
  $ poetry add "requests[security,socks]"
  ```

  - `--editable`
    - Dependency를 editable mode로 설치하게 해준다.
    - `pyproject.toml` file에서 package를 추가할 때 `develop` option에 대응한다.

  ```bash
  $ poetry add --editable ./my-package/
  ```

  - `--group`
    - 특정 group에 추가할 수 있게 해준다.

  ```bash
  $ poetry add mkdocs --group docs
  ```

  - `--extras`(`-E`)
    - Extra를 지정할 수 있다.
  - `--optional`
    - Optional dependency로 추가할 수 있게 해준다.

  - `--python`
    - Dependency가 설치되기 위한 Python version을 설정할 수 있게 해준다.
  - `--platform`
    - Dependency가 설치되기 위한 platform을 설정할 수 있게 해준다.
  - `--source`
    - Package를 설치할 때 사용할 source의 이름을 설정할 수 있게 해준다.

  - `--allow-prereleases`
    - Prerelease를 설치할 수 있게 해준다.
  - `--lock`
    - Install 은 실행하지 않고, lockfile만 update한다.
  - `--dry-run`
    - 실제 실행은 하지 않고, 실행 결과만 보여준다.



- `remove`

  - 설치된 dependency들 중에서 특정 dependency를 삭제한다.

  ```bash
  $ poetry remove <package>
  ```

  - `--group`(`-G`)
    - 특정 group에서 dependency를 제거한다.



- `show`

  - 사용 가능한 package들의 목록을 보여준다.

  ```bash
  $ poetry show
  ```

  - 특정 package의 상세한 정보를 보고싶다면 아래와 같이 package를 입력하면 된다.

  ```bash
  $ poetry show <package>
  ```



- `config`

  - Poetry의 설정을 변경할 때 사용한다.

  ```bash
  $ poetry config [options] [setting-key] [setting-value1] ... [setting-valueN]
  ```

  - `--list`
    - 설정을 확인할 수 있게 해준다.

  ```bash
  $ poetry config --list
  ```
  
  - `--unset`
    - 특정 설정을 제거한다.
  
  ```bash
  $ poetry config <제거할 설정> --unset
  ```
  
  - 설정 적용하기
  
  ```bash
  $ poetry config <설정> <설정 내용
  
  # e.g.
  $ poetry config virtualenvs.path /path/to/cache/directory/virtualenvs
  ```
  
  - 설정 확인하기
  
  ```bash
  $ poetry config <설정>
  
  # e.g.
  $ poetry config virtualenvs.path		# /path/to/cache/directory/virtualenvs
  ```
  
  - `virtualenvs.in-project`
    - Project의 root directory에 virtualenv를 생성할지 여부를 설정한다.
    - 기본값은 None이며, true로 줄 경우 project의 root directory `.venv`라는 이름으로 생성하고, 주지 않을 경우 `{cahce-dir}/virtualenvs` 또는 `{project-dir}/.venv` 중 이미 존재하는 directory에 생성한다.
  
  ```bash
  $ poetry config virtualenvs.in-project true
  ```



- `check`

  - `pyproject.toml` file의 유효성을 검증하고, `poetry.lock` 파일과 일관성이 있는지를 검증한다.

  ```bash
  $ poetry check
  ```



- `export`

  - Lockfile을 다른 format으로 export한다.

  ```bash
  $ poetry export -f requirements.txt --output requirements.txt
  ```

  - `-f`를 통해 format을 설정할 수 있다.
    - 현재는 `requirements.txt`와 `constraints.txt` 두 format만 지원한다.
  - `--output`
    - Output file의 이름을 지정한다.
    - 지정하지 않을 경우 standard output으로 출력한다.





## pyproject.toml

- `tool.poetry`

  - `name`(required)
    - Package의 name을 설정한다.
    - [PEP 508](https://peps.python.org/pep-0508/#names)에 정의된 유효한 이름이어야한다.
  - `version`(required)
    - Pacakage의 version을 설정한다.
    - [PEP 440](https://peps.python.org/pep-0440/)에 정의된 유효한 version이어야한다.
  - `description`(required)
    - Package에 대한 짧은 설명을 설정한다.
  - `license`
    - Package의 license를 설정한다.
    - 필수는 아니지만 설정하는 것을 강하게 권장한다.
  - `authors`(required)
    - Package의 작성자를 설정한다.
    - 모든 작성자를 배열 형태로 입력할 수 있으며, 반드시 한 명의 작성자는 들어가야한다.
    - `name <email>` 형태로 작성한다.
  - `maintainers`
    - Package의 maintainer를 설정한다.
    - `authors`와 마찬가지로 여러 명을 입력할 수 있으며, `name <email>` 형태로 작성한다.
  - `readme`
    - README file의 경로를 입력한다.
    - `pyproject.toml` file을 기준으로 상대 경로를 입력할 수  있다.
    - 배열 형태로 여러 개의 README file의 경로를 입력할 수도 있다.
  - `homepage`
    - Project의 website URL을 입력한다.

  - `repository`
    - Project의 repository의 URL을 입력한다.
  - `documentation`
    - Project의 documentation의 URL을 입력한다.
  - `keywords`
    - Package와 관련된 keyword들을 입력한다.
    - 배열 형태로 입력한다.
  - `classifiers`
    - Project의 PyPI trove classifier를 입력한다.
  - `packages`
    - 최종 배포에 포함될 package들과 module들을 배열 형태로 입력한다.
    - `from`을 입력하여 package의 위치를 지정할 수 있다.
    - `format`을 사용하여 build format을 설정할 수도 있다(예를 들어 아래의 경우 `sdist` build만이 `my_other_package`라는 package를 포함시켜 배포한다).

  ```toml
  [tool.poetry]
  # ...
  packages = [
      { include = "my_package" },
      { include = "extra_package/**/*.py" },
      { include = "my_package", from = "lib" },
      { include = "my_other_package", format = "sdist" },
  ]
  ```

  - `include`
    - 최종 package에 포함될 package들을 정의한다.

  ```toml
  [tool.poetry]
  # ...
  include = [
      { path = "tests", format = "sdist" },
      { path = "for_wheel.txt", format = ["sdist", "wheel"] }
  ]
  ```

  - `exclude`
    - 최종 package에서 제외 할 package들을 정의한다.
    - VCS의 ignore setting이 있을 경우(git의 경우 `.gitignore` file) `exclude`는 이 내용을 기본적으로 사용한다.
    - 만약 VCS의 `ignore setting`에는 포함되어 있는데, `exclude`에서는 제외시키고자 할 경우 `include`에 정의해주면 된다.

  ```toml
  [tool.poetry]
  exclude = ["my_package/excluded.py"]
  ```



- Dependency 관련 section

  - `tool.poetry.dependencies`
    - 아래와 같이 dependency들을 입력한다.

  ```toml
  [tool.poetry.dependencies]
  requests = "^2.13.0"
  ```

  - Local directory에 위치한 library를 지정해줘야 하는 경우 아래와 같이 설정할 수 있다.

  ```toml
  [tool.poetry.dependencies]
  # directory
  my-package = { path = "../my-package/", develop = false }
  
  # file
  my-package = { path = "../my-package/dist/my-package-0.1.0.tar.gz" }
  ```

  - 만약 특정 git repository에서 package를 설치해야 하는 경우 아래와 같이 설정할 수 있다.

  ```toml
  [tool.poetry.dependencies]
  # 기본형
  requests = { git = "https://github.com/requests/requests.git" }
  
  # branch 지정
  requests = { git = "https://github.com/kennethreitz/requests.git", branch = "next" }
  
  # coomit hash 사용
  flask = { git = "https://github.com/pallets/flask.git", rev = "38eb5d3b" }
  
  # tag 사용
  numpy = { git = "https://github.com/numpy/numpy.git", tag = "v0.13.2" }
  
  # pacakage가 특정 directory에 있을 경우
  subdir_package = { git = "https://github.com/myorg/mypackage_with_subdirs.git", subdirectory = "subdir" }
  
  # ssh connection을 사용하는 경우
  requests = { git = "git@github.com:requests/requests.git" }
  ```

  - Editable mode로 설치하고자 한다면 아애롸 같이 `develop=true` 옵션을 주면 된다.
    - 이 경우 설치 file의 변경 사항이 environment에 바로 반영된다.
  
  ```toml
  [tool.poetry.dependencies]
  my-package = {path = "../my/path", develop = true}
  ```
  
  - 만약 Python version에 따라 dependency의 version이 달라져야 한다면 아래와 같이 설정하면 된다.

  ```toml
  [tool.poetry.dependencies]
  foo = [
      {version = "<=1.9", python = ">=3.6,<3.8"},
      {version = "^2.0", python = ">=3.8"}
  ]
  ```
  
  - `tool.poetry.source`
    - Poetry는 기본적으로 PyPI에서 package들을 찾는다.
    - 만일 다른 저장소에서 package를 설치한다면 아래와 같이 `tool.poetry.source`에 지정해주면 된다.
  
  ```toml
  [[tool.poetry.source]]
  name = "private"
  url = "http://example.com/simple"
  
  # 그 후 tool.poetry.dependencies에 dependency를 입력할 때 아래와 같이 source를 설정해준다.
  [tool.poetry.dependencies]
  requests = { version = "^2.13.0", source = "private" }
  ```
  
  - Dependency들을 group으로 묶는 것도 가능하다.
  
  ```toml
  [tool.poetry.group.test.dependencies]
  pytest = "*"
  
  [tool.poetry.group.docs.dependencies]
  mkdocs = "*"
  ```



- `tool.poetry.scripts`

  - Package를 설치할 때 설치될 script 혹은 실행 파일에 대한 설명을 작성한다.
    - 예를 들어 아래의 경우 `my_pacakge` package의 `console` module에서 `run` function을 실행할 것이라는 의미이다.

  ```toml
  [tool.poetry.scripts]
  my_package_cli = 'my_package.console:run'
  ```

  - 아래와 같이 `extras`와 `type`도 설정할 수 있다.
    - `extras`는 아래 `tool.poetry.extras` 참고

  ```toml
  [tool.poetry.scripts]
  devtest = { reference = "mypackage:test.run_tests", extras = ["test"], type = "console" }
  ```

  - Script에 추가나 변경 사항이 있을 경우 `poetry install` 명령어를 실행해야 project의 가상환경이 이를 사용할 수 있게 된다.



- `tool.poetry.extras`

  - 아래와 같은 것들을 표현하기 위한 section이다.
    - 필수는 아닌 dependency들을 나열
    - Optional한 dependency들을 묶기
  - 예시

  ```toml
  [tool.poetry.dependencies]
  # mandatory는 이 package를 배포할 때 반드시 포함되어야하는 package이다.
  mandatory = "^1.0"
  
  # 반면에 아래 두 개는 반드시 포함되지는 않아도 되는 package이다.
  psycopg2 = { version = "^2.9", optional = true }
  mysqlclient = { version = "^1.3", optional = true }
  
  [tool.poetry.extras]
  # 반드시 포함되지는 않아도 되는 package들을 나열하고
  mysql = ["mysqlclient"]
  pgsql = ["psycopg2"]
  # 반드시 포함되지는 않아도 되는 package들을 묶을 때 extras를 사용한다.
  databases = ["mysqlclient", "psycopg2"]
  ```

  - `poetry install` 명령어 실행시에 `-E`(`--extras`) 옵션으로 package를 설치할지 여부를 결정할 수 있다.

  ```bash
  $ poetry install --extras "mysql pgsql"
  $ poetry install -E mysql -E pgsql
  ```

  - 모든 extra dependency들을 함께 설치하려면 아래와 같이 실행하면 된다.

  ```bash
  $ poetry install --all-extras
  ```

  - 만일 Poetry로 build된 package를 pip로 설치한다면 [PEP 508](https://peps.python.org/pep-0508/#extras)에 따라 아래와 같이 extra를 지정해줄 수 있다.

  ```bash
  $ pip install awesome[databases]
  ```







# Dependency Injector

- Dependency injector

  - 의존성 주입을 보다 간편하게 할 수 있게 해주는 package이다.
  - 마지막 commit이 2022년으로 관리가 되지 않고 있는 것 처럼 보이지만, [github issue](https://github.com/ets-labs/python-dependency-injector/issues/742)에 따르면 지속적으로 update 예정인 package이다.
  - 설치

  ```bash
  $ pip install dependency-injector
  ```



- Dependency injector를 사용하는 이유

  - Dependency들을 container로 묶어서 관리하여 보다 간편하게 관리할 수 있다.
    - `providers.Singlton`과 같이 주입 대상이 되는 객체의 life cycle을 관리할 수 있는 기능을 제공한다.
    - `override`를 통해 코드의 큰 수정 없이도 테스트를 진행할 수 있게 해준다.
    - 의존성 주입을 보다 명시적으로 정의하여 코드를 보다 쉽게 이해할 수 있도록 해준다.
  
  - 아래 코드는 의존성 주입을 하지 않는 코드다.
  
  ```python
  import os
  
  
  class ApiClient:
  
      def __init__(self) -> None:
          self.api_key = os.getenv("API_KEY")  # <-- dependency
          self.timeout = int(os.getenv("TIMEOUT"))  # <-- dependency
  
  
  class Service:
  
      def __init__(self) -> None:
          self.api_client = ApiClient()  # <-- dependency
  
  
  def main() -> None:
      service = Service()  # <-- dependency
      ...
  
  
  if __name__ == "__main__":
      main()
  ```
  
  - 위 코드에 의존성 주입을 적용하면 아래와 같다.
    - 기존 코드 보다는 유연한 코드가 됐지만, `main`을 실행시키기 위한 코드가 알아보기 힘들어 졌고, 구조를 변경하기도 힘들어졌다.
  
  ```python
  import os
  
  
  class ApiClient:
  
      def __init__(self, api_key: str, timeout: int) -> None:
          self.api_key = api_key  # <-- dependency is injected
          self.timeout = timeout  # <-- dependency is injected
  
  
  class Service:
  
      def __init__(self, api_client: ApiClient) -> None:
          self.api_client = api_client  # <-- dependency is injected
  
  
  def main(service: Service) -> None:  # <-- dependency is injected
      ...
  
  
  if __name__ == "__main__":
      main(
          service=Service(
              api_client=ApiClient(
                  api_key=os.getenv("API_KEY"),
                  timeout=int(os.getenv("TIMEOUT"))
              )
          )
      )
  ```
  
  - 위 코드에 `dependency_injector`를 도입하면 아래와 같이 바뀐다.
  
  ```python
  from dependency_injector import containers, providers
  from dependency_injector.wiring import Provide, inject
  
  
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration()
  
      api_client = providers.Singleton(
          ApiClient,
          api_key=config.api_key,
          timeout=config.timeout,
      )
  
      service = providers.Factory(
          Service,
          api_client=api_client,
      )
  
  
  @inject
  def main(service: Service = Provide[Container.service]) -> None:
      ...
  
  
  if __name__ == "__main__":
      container = Container()
      container.config.api_key.from_env("API_KEY", required=True)
      container.config.timeout.from_env("TIMEOUT", as_=int, default=5)
      container.wire(modules=[__name__])
  
      main()  # 이존성이 자동으로 주입된다.
  
      with container.api_client.override(mock.Mock()):
          main()	# override된 의존성이 자동으로 주입된다.
  ```



- FastAPI + Elasticsearch client를 사용하는 예시

  - FastAPI에 요청을 보내 Elasticsearch를 사용하는 app을 만들고자 한다.
    - App의 특성상 FastAPI app은 Elasticsearch Python client에 강하게 의존할 수 밖에 없다.
    - 따라서 dependency injector를 사용하여 의존성을 주입해줄 것이다.
  - 먼저 Elasticsearch client를 사용하여 Elasticearch로 요청을 보내는 service를 작성한다.
    - `Service`는 Elasticsearch client에 의존한다.

  ```python
  from elasticsearch import Elasticsearch
  
  
  class Service:
      def __init__(self, es_client: Elasticsearch) -> None:
          self.es_client = es_client
  
      def get_indices(self) -> list:
          result = self.es_client.cat.indices()
          return result.split("\n")
  ```

  - 다음으로 의존성 주입을 위한 container를 작성한다.
    - Elasticsearch client에 의존하는 `Service`에 의존성(Elasticsearch client)를 주입한다.

  ```python
  # containers.py
  
  from dependency_injector import containers, providers
  from elasticsearch import Elasticsearch
  
  import services
  
  
  class Container(containers.DeclarativeContainer):
      config = providers.Configuration()
  
      es_client = providers.Singleton(
          Elasticsearch,
          hosts=config.es_hosts
      )
  	
      service = providers.Factory(
          services.Service,
          es_client=es_client
      )
  ```

  - 마지막으로 FastAPI app을 작성한다.
    - FastAPI app은 `Service`에 의존한다.
    - FastAPI app이 의존하는 `Service`를 `@inject`와 marker, `.wire()`를 사용하여 주입해준다.

  ```python
  from dependency_injector.wiring import inject, Provide
  from fastapi import FastAPI, Depends
  import uvicorn
  
  from containers import Container
  from services import Service
  
  
  app = FastAPI()
  
  
  @app.get("/indices")
  @inject
  def get_indices(service: Service = Depends(Provide[Container.service])):
      indices = service.get_indices()
      return {"indices": indices}
  
  
  if __name__ == "__main__":
      container = Container()
      container.config.es_hosts.from_env("ES_HOSTS", "http://localhost:9200")
      container.wire(modules=[__name__])
      uvicorn.run(app, port=8080)
  ```






## Provider

- Provider
  - 의존성 혹은 객체들을 모아주는 역할을 한다.
    - Provider는 dependency들을 모아서 생성된 object에 주입한다.
    - 한 provider를 다른 provider로 override하는 것이 가능하다.
  - 다양한 종류의 provider를 지원하며, custom provider를 만드는 것도 가능하다.



- Factory Provider

  - 새로운 object를 생성할 때 사용하는 provider이다.
    - 첫 번째 인자로는 class, factory function 또는 object를 생성하는 method를 받는다.
    - 나머지 인자들은 object가 생성될 때 주입해줄 dependency들을 받는다.

  ```python
  from dependency_injector import containers, providers
  
  
  class Group:
      ...
  
  
  class User:
      def __init__(self, group:Group):
          self.group = group
  
  class Container(containers.DeclarativeContainer):
  
      user_factory = providers.Factory(User, group=Group())
  
  
  if __name__ == "__main__":
      container = Container()
  
      user1 = container.user_factory()
      user2 = container.user_factory()
  
      assert isinstance(user1, User)
      assert isinstance(user2, User)
      assert isinstance(user1.group, Group)
      assert isinstance(user2.group, Group)
  ```

  - 주입되는 dependency들은 아래와 같은 규칙을 따른다.
    - 만약 dependency가 provider일 경우 provider가 호출되고 그 결과가 주입된다.
    - 만약 provider 자체를 주입해야하는 경우, `.provider` attribute를 사용해야한다.
    - 다른 모든 dependency들은 그대로(as is) 주입된다.
    - Positional argument들은 `Factory` postional dependency 뒤에 와야 한다.
    - Keyword argument과 `Factory` keyword dependency가 같은 이름으로 주입될 경우 keyword argument에 우선권이 있다.

  ```python
  from typing import Callable, List
  
  from dependency_injector import containers, providers
  
  
  class User:
      def __init__(self, uid: int) -> None:
          self.uid = uid
  
  
  class UserRepository:
      def __init__(self, user_factory: Callable[..., User]) -> None:
          self.user_factory = user_factory
  
      def get_all(self) -> List[User]:
          return [
              self.user_factory(**user_data)
              for user_data in [{"uid": 1}, {"uid": 2}]
          ]
  
  
  class Container(containers.DeclarativeContainer):
  
      user_factory = providers.Factory(User)
  	
      # provider 자체를 주입하려면 .provider attribute를 주입하면 된다.
      user_repository_factory = providers.Factory(
          UserRepository,
          user_factory=user_factory.provider,
      )
  
  
  if __name__ == "__main__":
      container = Container()
  
      user_repository = container.user_repository_factory()
  
      user1, user2 = user_repository.get_all()
  
      assert user1.uid == 1
      assert user2.uid == 2
  ```

  - Attribute도 주입할 수 있다.
    - `.add_attributes()` method를 사용하여 주입이 가능하다.

  ```python
  from dependency_injector import containers, providers
  
  
  class Client:
      ...
  
  
  class Service:
      def __init__(self) -> None:
          self.client = None
  
  
  class Container(containers.DeclarativeContainer):
  
      client = providers.Factory(Client)
  
      service = providers.Factory(Service)
      service.add_attributes(client=client)
  
  
  if __name__ == "__main__":
      container = Container()
  
      service = container.service()
  
      assert isinstance(service.client, Client)
  ```

  - Factory provider를 사용하면 object 내부의 object에도 의존성을 주입할 수 있다.
    - 예를 들어 아래와 같은 class들이 있다고 가정해보자.
    - 연쇄의 마지막에 해당하는 `Regularizer` class는 `alpha`에 dependency가 걸려 있으며, `alpha` 값은 algorithm에 따라 달라질 수 있다.
    - Factory provider를 사용하면 이와 같은 경우를 간단하게 처리할 수 있다.
    - `__`를 사용하여 object 내부의 object에 의존성을 주입할 수 있다.

  ```python
  from dependency_injector import containers, providers
  
  
  class Regularizer:
      def __init__(self, alpha: float) -> None:
          self.alpha = alpha
  
  
  class Loss:
      def __init__(self, regularizer: Regularizer) -> None:
          self.regularizer = regularizer
  
  
  class ClassificationTask:
      def __init__(self, loss: Loss) -> None:
          self.loss = loss
  
  
  class Algorithm:
      def __init__(self, task: ClassificationTask) -> None:
          self.task = task
  
  
  class Container(containers.DeclarativeContainer):
  
      algorithm_factory = providers.Factory(
          Algorithm,
          task=providers.Factory(
              ClassificationTask,
              loss=providers.Factory(
                  Loss,
                  regularizer=providers.Factory(
                      Regularizer,
                  ),
              ),
          ),
      )
  
  
  if __name__ == "__main__":
      container = Container()
  	
      # __를 통해 내부의 object에 의존성을 주입한다.
      algorithm_1 = container.algorithm_factory(
          task__loss__regularizer__alpha=0.5,
      )
      assert algorithm_1.task.loss.regularizer.alpha == 0.5
  
      algorithm_2 = container.algorithm_factory(
          task__loss__regularizer__alpha=0.7,
      )
      assert algorithm_2.task.loss.regularizer.alpha == 0.7
  ```

  - 특정 type만을 제공하는 provider 생성하기
    - Factory provider를 상속받는 class를 정의하고, `provided_type` class attribute에 type을 정의하면 된다.

  ```python
  from dependency_injector import containers, providers, errors
  
  
  class BaseService:
      ...
  
  
  class SomeService(BaseService):
      ...
  
  # factory provider를 상속 받고
  class ServiceProvider(providers.Factory):
  	# provided_type class attribute에 type을 설정한다.
      provided_type = BaseService
  
  
  class Services(containers.DeclarativeContainer):
  
      some_service_provider = ServiceProvider(SomeService)
  
  
  # 지정해주지 않은 type으로 생성하려 할 경우 error가 발생한다.
  try:
      class Container(containers.DeclarativeContainer):
          some_service_provider = ServiceProvider(object)
  except errors.Error as exception:
      print(exception)
      # <class "__main__.ServiceProvider"> can provide only
      # <class "__main__.BaseService"> instances
  ```

  - Abstract factory
    - Base class의 provider를 생성하거나, 구체적인 구현을 아직 모를 때 도움을 준다.
    - Abstract factory provider는 아래와 같은 특징이 있다.
    - 특정 type의 object만 제공할 수 있다.
    - 사용하기 전에 override해야한다.

  ```python
  import abc
  import dataclasses
  import random
  from typing import List
  
  from dependency_injector import containers, providers
  
  
  class AbstractCacheClient(metaclass=abc.ABCMeta):
      ...
  
  
  @dataclasses.dataclass
  class RedisCacheClient(AbstractCacheClient):
      host: str
      port: int
      db: int
  
  
  @dataclasses.dataclass
  class MemcachedCacheClient(AbstractCacheClient):
      hosts: List[str]
      port: int
      prefix: str
  
  
  @dataclasses.dataclass
  class Service:
      cache: AbstractCacheClient
  
  
  class Container(containers.DeclarativeContainer):
  
      cache_client_factory = providers.AbstractFactory(AbstractCacheClient)
  
      service_factory = providers.Factory(
          Service,
          cache=cache_client_factory,
      )
  
  
  if __name__ == "__main__":
      container = Container()
  
      cache_type = random.choice(["redis", "memcached"])
      if cache_type == "redis":
          # 사용 전에 override한다.
          container.cache_client_factory.override(
              providers.Factory(
                  RedisCacheClient,
                  host="localhost",
                  port=6379,
                  db=0,
              ),
          )
      elif cache_type == "memcached":
          # 사용 전에 override한다.
          container.cache_client_factory.override(
              providers.Factory(
                  MemcachedCacheClient,
                  hosts=["10.0.1.1"],
                  port=11211,
                  prefix="my_app",
              ),
          )
  
      service = container.service_factory()
      print(service.cache)
  ```

  - Factory aggregate
    - 여러 개의 factory들을 모으는 역할을 한다.
    - 모아진 factory들을 호출할 때는 반드시 첫 번째 인자로 key라 불리는 string을 넘겨야한다.
    - `FactoryAggregate`는 key를 사용하여 matching되는 factory를 찾는다.
    - `.providers` attribute로 묶인 proivder들의 목록을 볼 수 있다.
    - `FactoryAggregate`는 override가 불가능하다.
    - 만약 string이 아닌 key를 사용해야 하거나 `.` 또는 `-`가 포함된 string key를 사용해야 하면 dirctionary 형태로 넘겨야한다.

  ```python
  import dataclasses
  
  from dependency_injector import containers, providers
  
  
  @dataclasses.dataclass
  class Game:
      player1: str
      player2: str
  
      def play(self):
          print(
              f"{self.player1} and {self.player2} are "
              f"playing {self.__class__.__name__.lower()}"
          )
  
  
  class Chess(Game):
      ...
  
  
  class Checkers(Game):
      ...
  
  
  class Ludo(Game):
      ...
  
  
  class Container(containers.DeclarativeContainer):
  
      game_factory = providers.FactoryAggregate(
          chess=providers.Factory(Chess),
          checkers=providers.Factory(Checkers),
          ludo=providers.Factory(Ludo),
      )
  
  
  if __name__ == "__main__":
      game_type = "chess"
      player1 = "foo"
      player2 = "bar"
  
      container = Container()
      
      # .providers attribute로 묶인 proivder들의 목록을 볼 수 있다.
      print(container.game_factory.providers)
  
      selected_game = container.game_factory(game_type, player1, player2)
      selected_game.play()
  ```



- Configuration provider

  - 다른 provider에거 configuration을 주입하는 역할을 한다.
    - `es_client_factory`라는 provider에게 configuration을 주입하는 configuration provider의 예시.
    - 아래는 Python dictionary로 설정한 configuration을 주입하는 것이다.

  ```python
  from dependency_injector import containers, providers
  from elasticsearch import Elasticsearch
  
  
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration()
  
      es_client_factory = providers.Factory(
          Elasticsearch,
          hosts=config.es.hosts,
          max_retries=config.es.max_retries,
      )
  
  if __name__ == "__main__":
      container = Container()
      container.config.from_dict(
          {
              "es": {
                   "hosts": ["http://localhost:9200"],
                   "max_retries": 10,
               },
          },
      )
      es_client = container.es_client_factory()
  
      print(es_client.ping())
  ```

  - JSON file에 설정된 configuration을 주입하는 예시
    - JSON뿐 아니라 ini, YAML 등도 method 명만 다르고 모두 동일한 기능을 지원한다.

  ```python
  """
  예를 들어 아래와 같은 json file이 있을 때
  {
      "es": {
          "hosts": ["http://localhost:9200"],
          "max_retries": 10
      }
  }
  """
  
  
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration()
  
  
  if __name__ == "__main__":
      container = Container()
      # 아래와 같이 file을 읽어 configuration을 불러온다.
      container.config.from_json("./config.json")
      print(container.config())		# {'es': {'hosts': ['http://localhost:9200'], 'max_retries': 10}}
      print(container.config.es())	# {'hosts': ['http://localhost:9200'], 'max_retries': 10}
  ```

  - 혹은 아래와 같은 방식으로도 가능하다.

  ```python
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration(json_files=["./config.json"])
  
  
  if __name__ == "__main__":
      container = Container()
  ```

  - 환경 변수 interpolation을 지원한다.
    - JSON file을 아래와 같이 작성하면 먼저 `MAX_RETRIES`라는 환경 변수가 있는지 확인 후 있으면 그 값을 사용하고, 없으면 `:` 뒤에 있는 기본 값을 사용한다.

  ```json
  {
      "es": {
          "hosts": ["http://localhost:9200"],
          "max_retries": "${MAX_RETRIES:5}"
      }
  }
  ```

  - Pydantic `BaseSettings`에서 configuration을 불러오는 예시

  ```python
  from dependency_injector import containers, providers
  from pydantic import BaseSettings, Field
  
  
  class ElasticsearchSettings(BaseSettings):
  
      hosts: str = Field(default="http://localhost:9200")
      max_retires: str = Field(default=5)
  
  
  class Settings(BaseSettings):
  
      es: ElasticsearchSettings = ElasticsearchSettings()
      optional: str = Field(default="default_value")
  
  
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration()
  
  
  if __name__ == "__main__":
      container = Container()
  
      container.config.from_pydantic(Settings())
  ```

  - 혹은 아래와 같이 불러오는 것도 가능하다.

  ```python
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration(pydantic_settings=[Settings()])
  
  
  if __name__ == "__main__":
      container = Container()
  ```

  - `strict` option
    - Configuration provider는 error에 관대한 편으로, configuration에 없는 값에 접근하려 한다던가 없는 file을 읽어서 configuration을 생성하려해도 error가 발생하지 않는다.
    - `strict`를 True로 주면 보다 엄격하게 error를 raise한다.

  ```python
  from dependency_injector import containers, providers
  
  
  class Container(containers.DeclarativeContainer):
  	
      # strict를 True로 주면
      config = providers.Configuration(strict=True)
  
  
  if __name__ == "__main__":
      container = Container()
      # 없는 file을 읽으려 하면 exception이 발생한다.
      container.config.from_json("./not-exist-file.json")
  ```

  - `required()` method
    - 만약 strict로 쓰고 싶지는 않지만 특정 configuration이 포함되지 않았을 때는 exception을 발생시키고자 한다면 아래와 같이 `required()`를 사용하면 된다.
    - `required()`를 사용한 configuration이 존재하지 않을 경우 exception이 발생한다.

  ```python
  from dependency_injector import containers, providers
  from elasticsearch import Elasticsearch
  
  
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration()
  
      es_client_factory = providers.Factory(
          Elasticsearch,
          hosts=config.es.hosts,
          max_retries=config.es.not_exists_configuration.required()
      )
  
  
  if __name__ == "__main__":
      container = Container()
      container.config.from_json("./config.json")
      es_client = container.es_client_factory()
  ```

  - Value의 type을 설정하기
    - 기본적으로 configuration에 설정된 값을 int(`.as_int()`)나 float(`.as_float()`) type으로 변경하는 methoe를 지원한다.
    - 만일 다른 type으로 변경하고자 한다면 ` .as_(callback, *args, **kwargs)`메서드를 사용하여 첫 번째 인자로 type을 변환시키기 위한 함수를 지정하면 된다.

  ```python
  class Container(containers.DeclarativeContainer):
  
      config = providers.Configuration()
  
      calculator_factory = providers.Factory(
          Calculator,
          pi=config.pi.as_(decimal.Decimal)
      )
  ```



- Singleton provider

  - 단일 객체를 제공하는 provider이다.
    - 처음 생성된 객체를 기억하고 있다가 이후에 생성 요청이 들어올 때 마다 처음 생성된 객체를 반환한다.
    - Singleton provider는 오직 생성될 때만 dependency injection을 수행하며, 이미 생성된 후에는 생성된 객체를 반환하기만 하고 injection을 적용하지는 않는다.

  ```python
  from dependency_injector import containers, providers
  
  
  class UserService:
      ...
  
  
  class Container(containers.DeclarativeContainer):
  
      user_service_provider = providers.Singleton(UserService)
  
  
  if __name__ == "__main__":
      container = Container()
  
      user_service1 = container.user_service_provider()
      user_service2 = container.user_service_provider()
      assert user_service1 is user_service2
  ```

  - Singleton provider의 scope는 container 단위이다.
    - 즉 서로 다른 container에서 생성된 singleton object는 서로 다르다.

  ```python
  from dependency_injector import containers, providers
  
  
  class UserService:
      ...
  
  
  class Container(containers.DeclarativeContainer):
  
      user_service_provider = providers.Singleton(UserService)
  
  
  if __name__ == "__main__":
      container1 = Container()
      user_service1 = container1.user_service_provider()
  
      container2 = Container()
      user_service2 = container2.user_service_provider()
  
      assert user_service1 is not user_service2
  ```

  - 기억하고 있는 객체를 초기화하기
    - `reset()` method를 통해 기억하고 있는 객체(처음 생성 된 객체)를 초기화 할 수 있다.

  ```python
  from dependency_injector import containers, providers
  
  
  class UserService:
      ...
  
  
  class Container(containers.DeclarativeContainer):
  
      user_service = providers.Singleton(UserService)
  
  
  if __name__ == "__main__":
      container = Container()
  
      user_service1 = container.user_service()
  
      container.user_service.reset()
  
      user_service2 = container.user_service()
      assert user_service2 is not user_service1
  ```

  - `reset()` method는 context manager로도 사용할 수 있다.
    - 이 경우 context에 진입할 때와 나올 때 기억하고 있는 객체가 초기화된다.

  ```python
  from dependency_injector import containers, providers
  
  
  class UserService:
      ...
  
  
  class Container(containers.DeclarativeContainer):
  
      user_service = providers.Singleton(UserService)
  
  
  if __name__ == "__main__":
      container = Container()
  
      user_service1 = container.user_service()
  
      with container.user_service.reset():
          user_service2 = container.user_service()
  
      user_service3 = container.user_service()
  
      assert user_service1 is not user_service2
      assert user_service2 is not user_service3
      assert user_service3 is not user_service1
  ```

  - `full_reset()` method를 사용하여 해당 singleton provider가 의존하는 singleton provider가 기억하고 있는 객체를 초기화 할 수 있다.
    - `reset()` method는 현재 provider가 기억하고 있는 객체만 초기화한다.
    - 예를 들어 아래 예시에서 `user_service` provider는 `database` provider에 의존한다.
    - 이 때 `user_service` provider가 기억하고 있는 객체 뿐 아니라 `database` provider가 기억하고 있는 객체까지 초기화하고자 한다면 `full_reset()` method를 사용해야한다.
    - `full_reset()` method도 context manager로 사용하는 것이 가능하다.

  ```python
  from dependency_injector import containers, providers
  
  
  class Database:
      ...
  
  
  class UserService:
      def __init__(self, db: Database):
          self.db = db
  
  
  class Container(containers.DeclarativeContainer):
  
      database = providers.Singleton(Database)
  
      user_service = providers.Singleton(UserService, db=database)
  
  
  if __name__ == "__main__":
      container = Container()
  
      user_service1 = container.user_service()
  
      container.user_service.full_reset()
  
      user_service2 = container.user_service()
      assert user_service2 is not user_service1
      assert user_service2.db is not user_service1.db
  ```



- Provider override

  - 한 provider를 다른 provider로 override할 수 있다.
    - Test시에 유용하게 사용할 수 있는데, 실제 API client를 개발용 stub으로 변경하는 등과 같이 사용할 수 있기 때문이다.
  - Override를 위해서는 `Provider.override()` method를 호출해야한다.
    - 이 method는 overriding이라 불리는 하나의 argument를 받는다.
    - 만약 overriding에 provider를 넘길 경우 provider 호출 시 원래 provider 대신 이 provider가 호출된다.
    - 만약 overriding에 provider가 아닌 값을 넘길 경우 원래 provider 호출 시 원래 provider가 호출되는 대신 이 value가 반환된다.

  - 예시

  ```python
  import dataclasses
  import unittest.mock
  
  from dependency_injector import containers, providers
  
  
  class ApiClient:
      ...
  
  
  class ApiClientStub(ApiClient):
      ...
  
  
  @dataclasses.dataclass
  class Service:
      api_client: ApiClient
  
  
  class Container(containers.DeclarativeContainer):
  
      api_client_factory = providers.Factory(ApiClient)
  
      service_factory = providers.Factory(
          Service,
          api_client=api_client_factory,
      )
  
  
  if __name__ == "__main__":
      container = Container()
  
      # 운영 환경에서 사용할 ApiClient 대신 ApiClientStub을 생성하도록 override한다.
      container.api_client_factory.override(providers.Factory(ApiClientStub))
      service1 = container.service_factory()
      assert isinstance(service1.api_client, ApiClientStub)
  
      # 2. override를 context manager로 사용하여 APIClient의 mock object를 override한다.
      with container.api_client_factory.override(unittest.mock.Mock(ApiClient)):
          service2 = container.service_factory()
          assert isinstance(service2.api_client, unittest.mock.Mock)
  
      # 3. .reset_override()룰 사용하여 override를 해제한다.
      container.api_client_factory.reset_override()
      service3 = container.service_factory()
      assert isinstance(service3.api_client, ApiClient)
  ```





## Container

- Container
  - Provider들의 집합이다.
  - 아래와 같은 기준으로 Provider들을 묶는다.
    - 모든 Provider들이 한 container에 있도록 한다(가장 흔한 경우이다).
    - 같은 계층에 있는 provider들을 묶는다.
    - 기능에 따라 함께 사용되는 provider들을 묶는다.



- Declarative container

  - `DeclarativeContainer`를 상속 받는 class를 container로 사용하는 방식이다.
    - Class attribute로 provider들을 나열한다.
    - Declarative container는 provider를 제외한 어떤 attribute나 method도 가져선 안된다.

  ```python
  from dependency_injector import containers, providers
  
  # DeclarativeContainer를 상속 받는 class를 생성하고
  class Container(containers.DeclarativeContainer):
  
      factory1 = providers.Factory(object)
  
      factory2 = providers.Factory(object)
  
  
  if __name__ == "__main__":
      # 해당 class의 instance를 생성한다.
      container = Container()
  
      object1 = container.factory1()
      object2 = container.factory2()
  ```

  - Declarative container는 어래와 같은 attribute들을 제공한다.
    - `providers`: 모든 container provider들이 dictionary 형태로 저장되어 있다.
    - `cls_providers`: 현재 container의 provider들이 dictionary 형태로 저장되어 있다.
    - `inheritd_providers`: 자신이 상속 받은 container의 container provider 들이 dictionary 형태로 저장되어 있다.

  ```python
  from dependency_injector import containers, providers
  
  
  class ContainerA(containers.DeclarativeContainer):
  
      provider1 = providers.Factory(object)
  
  
  class ContainerB(ContainerA):
  
      provider2 = providers.Singleton(object)
  
  
  assert ContainerA.providers == {
      "provider1": ContainerA.provider1,
  }
  assert ContainerB.providers == {
      "provider1": ContainerA.provider1,
      "provider2": ContainerB.provider2,
  }
  
  assert ContainerA.cls_providers == {
      "provider1": ContainerA.provider1,
  }
  assert ContainerB.cls_providers == {
      "provider2": ContainerB.provider2,
  }
  
  assert ContainerA.inherited_providers == {}
  assert ContainerB.inherited_providers == {
      "provider1": ContainerA.provider1,
  }
  ```

  - Container 내에서의 의존성 주입은 아래와 같이 이루어진다.

  ```python
  from dependency_injector import containers, providers
  from elasticsearch import Elasticsearch
  
  
  class UserService:
      ...
  
  
  class AuthService:
      def __init__(self, es_client: Elasticsearch, user_service: UserService):
          self.es_client = es_client
          self.user_service = user_service
  
  
  class Container(containers.DeclarativeContainer):
  
      es_client = providers.Singleton(Elasticsearch, ["http://localhost:9200"])
  
      user_service = providers.Factory(
          UserService
      )
  
      auth_service = providers.Factory(
          AuthService,
          es_client=es_client,
          user_service=user_service,
      )
  
  
  if __name__ == "__main__":
      container = Container()
  
      user_service = container.user_service()
      auth_service = container.auth_service()
  
      assert isinstance(auth_service.es_client, Elasticsearch)
      assert isinstance(auth_service.user_service, UserService)
  ```

  - Container instance를 생성할 때 container provider를 override 할 수 있다.

  ```python
  from unittest import mock
  
  from dependency_injector import containers, providers
  from elasticsearch import Elasticsearch
  
  
  class Container(containers.DeclarativeContainer):
  	# 실제 es_client provider를 선언하고
      es_client = providers.Singleton(Elasticsearch, ["http://localhost:9200"])
  
  
  if __name__ == "__main__":
      # container instance 생성시에 mock으로 교체한다.
      container = Container(es_client=mock.Mock(Elasticsearch))
      es_client = container.es_client()
      assert isinstance(es_client, mock.Mock)
  ```

  - 혹은 아래와 같이 container instance를 생성하고 난 후에 `override_providers()` method를 사용하여 override하는 것도 가능하다.

  ```python
  from unittest import mock
  
  from dependency_injector import containers, providers
  from elasticsearch import Elasticsearch
  
  
  class Container(containers.DeclarativeContainer):
      es_client = providers.Singleton(Elasticsearch, ["http://localhost:9200"])
  
  
  if __name__ == "__main__":
      # container instance는 그냥 생성하고
      container = Container()
      # override_providers method를 사용하여 override한다.
      container.override_providers(es_client=mock.Mock(Elasticsearch))
      es_client = container.es_client()
      assert isinstance(es_client, mock.Mock)
  ```

  - 혹은 아래와 같이 `override_providers()` method를 context manager로 사용할 수도 있다.

  ```python
  from unittest import mock
  
  from dependency_injector import containers, providers
  from elasticsearch import Elasticsearch
  
  
  class Container(containers.DeclarativeContainer):
      es_client = providers.Singleton(Elasticsearch, ["http://localhost:9200"])
  
  
  if __name__ == "__main__":
      container = Container()
      # override_providers method를 context manager로 사용한다.
      with container.override_providers(es_client=mock.Mock(Elasticsearch)):
          assert isinstance(container.es_client(), mock.Mock)
      
      # context가 종료되면 다시 원래 object를 가리키게 된다.
      assert isinstance(container.es_client(), Elasticsearch)
  ```





## Wiring

- Wiring

  - Function이나 method에 container provider들을 주입할 수 있게 해주는 기능이다.
  - 사용법은 아래와 같다.
    - Dependency들을 주입시킬 method에 `@inject` decorator를 작성한다.
    - 주입시킬 dependency들을 정의하는 wiring marker를 작성한다.
    - `container.wire()` method를 호출하여 marker를 통해 주입하고자 하는 module과 container를 연결(wiring)한다(호출하지 않을 경우 주입 되지 않는다).

  ```python
  from dependency_injector import containers, providers
  from dependency_injector.wiring import Provide, inject
  
  
  class Service:
      ...
  
  
  class Container(containers.DeclarativeContainer):
  
      service = providers.Factory(Service)
  
  # depenency를 주입시킬 method에 decorator를 작성한다.
  @inject
  # wiring marker를 작성한다. 예시에서는 Provide[Container.service]가 wiring marker이다.
  def main(service: Service = Provide[Container.service]) -> None:
      ...
  
  
  if __name__ == "__main__":
      container = Container()
      # wire method를 호출하여 연결하고자 하는 module을 지정해준다.
      container.wire(modules=[__name__])
  
      main()
  ```



- Decorator `@inject`

  - `@inject` decorator는 dependency들을 주입한다.
    - 정상적으로 동작하게 하기 위해서는 반드시 첫 번째 decorator로 작성해야한다.
  - 이는 FastAPI에서도 마찬가지로, FastAPI에서 사용할 때도 `@app` decorator보다 번저 작성해야한다.

  ```python
  app = FastAPI()
  
  
  @app.api_route("/")
  @inject
  async def index(service: Service = Depends(Provide[Container.service])):
      value = await service.process()
      return {"result": value}
  ```



- Markers

  - Wiring에서는 의존성 주입을 위해 marker를 사용한다.
    - 아래와 같이 method의 argument에 기본 값 형태로 작성하면 된다.
    - Annotation은 꼭 입력하지 않아도 된다.

  ```python
  from dependency_injector.wiring import inject, Provide
  
  
  @inject
  def foo(bar: Bar = Provide[Container.bar]):
      ...
  ```

  - 만약 provider 자체를 주입해야 할 경우 아래와 같이 하면 된다.
    - `Container.bar.provider`와 같이 `.provider` attribute를 사용한다.

  ```python
  from dependency_injector.providers import Factory
  from dependency_injector.wiring import inject, Provide
  
  
  @inject
  def foo(bar_provider: Factory[Bar] = Provide[Container.bar.provider]):
      bar = bar_provider(argument="baz")
      ...
  ```

  - 아래와 같이 attribute를 사용하지 않고 string identifier를 사용할 수도 있다.
    - 이 경우 container를 입력할 필요가 없다.

  ```python
  from dependency_injector import containers, providers
  from dependency_injector.wiring import Provide, inject
  
  
  class Service:
      ...
  
  
  class Container(containers.DeclarativeContainer):
  
      service = providers.Factory(Service)
  
  
  @inject
  def main(service: Service = Provide["service"]) -> None:
      ...
  
  
  if __name__ == "__main__":
      container = Container()
      container.wire(modules=[__name__])
  
      main()
  ```



- `WiringConfiguration`을 사용하면 `.wire()` method를 자동으로 호출하도록 만들 수 있다.

  - 아래와 같이 `containers.WiringConfiguration`를 사용하면 된다.

  ```python
  from dependency_injector import containers
  
  
  class Container(containers.DeclarativeContainer):
  
      wiring_config = containers.WiringConfiguration(
          modules=[
              "yourapp.module1",
              "yourapp.module2",
          ],
          packages=[
              "yourapp.package1",
              "yourapp.package2",
          ],
      )
  
  if __name__ == "__main__":
      container = Container()  # Container instance 생성시에 .wire() method가 자동으로 호출된다.
  ```

  - Container instance가 생성될 때 자동으로 `.wire()` method가 호출된다.

