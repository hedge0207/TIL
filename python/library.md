# click

> https://click.palletsprojects.com/en/8.0.x/

- Python CLI를 보다 쉽게 사용할 수 있게 해주는 library

  - Command Line Interface Creation Kit의 줄임말이다.
  - Python 내장 패키지인 argparse와 유사한 역할을 한다.
  - 설치

  ```bash
  $ pip install click
  ```



- 커맨드 생성하기

  - `@click.command` decorator를 함수에 추가하면 해당 함수는 command line tool이 된다.
    - `echo`는 `print` 함수 대신 사용하는 것으로, Python2와의 호환을 위해 만든 것이다.
    - `echo` 대신 `print`를 사용해도 된다.

  ```python
  import click
  
  
  @click.command()
  def hello():
      click.echo('Hello World!')
  
  if __name__ == '__main__':
      hello()
  ```

  - nested command 추가하기

  ```python
  import click
  
  
  @click.group()
  def cli():
      pass
  
  @click.command()
  def initdb():
      click.echo('Initialized the database')
  
  @click.command()
  def dropdb():
      click.echo('Dropped the database')
  
  cli.add_command(initdb)
  cli.add_command(dropdb)
  ```

  - 보다 간단하기 nested command 생성하기

  ```python
  # 혹은 아래와 같이 보다 간단하게 만들 수 있다.
  @click.group()
  def cli():
      pass
  
  # group decorator를 붙인 함수의 이름을 decorator로 쓴다.
  @cli.command()
  def initdb():
      click.echo('Initialized the database')
  
  @cli.command()
  def dropdb():
      click.echo('Dropped the database')
  ```

  - `--help` 명령어를 입력했을 때 나오는 값들도 자동으로 생성해준다.

  ```bash
  $ python test.py --help
  ```



- 파라미터 추가하기

  - `argument`와 `option`이 존재하는데 `option`이 더 많은 기능을 제공한다.

  ```python
  @click.command()
  @click.option('--count', default=1, help='number of greetings')
  @click.argument('name')
  def hello(count, name):
      for x in range(count):
          click.echo('Hello %s!' % name)
  ```

  - parameter의 type 설정하기

    > 지원하는 type 목록은 https://click.palletsprojects.com/en/7.x/options/#choice-opts에서 확인 가능하다.

    - 다음과 같이 type을 지정해준다.
    - 예시로 든 `click.Choice`은 list 안에 있는 값들 중 하나를 받는 것이며, `case_sensitive` 옵션은 대소문자 구분 여부를 결정하는 것이다.

  ```python
  @click.command()
  @click.option('--hash-type',
                type=click.Choice(['MD5', 'SHA1'], case_sensitive=False))
  def digest(hash_type):
      click.echo(hash_type)
  ```



- Option의 충돌

  - locust와 같이 자체적으로 cli을 사용하는 패키지와 함께 사용할 경우 충돌이 발생할 수 있다.
  - 이 경우 click으로 추가한 option들을 충돌이 발생한 패키지에도 추가해주거나, 충돌이 난 패키지에서 삭제해줘야 한다.
  - 삭제
    - `sys.argv`에는 option 값들이 List[str] 형태로 저장되어 있는데, 여기서 삭제해주면 된다.

  ```python
  import sys
  
  sys.argv.remove("<삭제할 옵션 이름>")
  ```

  - 추가
    - 충돌이 발생한 패키지에서 command line option을 추가하는 기능을 제공하면 click으로 받은 옵션 값들을 해당 패키지의 cli에도 추가해준다.



