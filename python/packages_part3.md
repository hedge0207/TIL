# Shorts

- faker

  - 언어를 한국어로 설정하고 `catch_phrase()`를 사용하면 무작위로 생성된 짧은 문자열을 얻을 수 있다.

  ```python
  from faker import Faker
  
  fake = Faker("ko-KR")
  print(fake.catch_phrase())
  ```



- Python StateMachine

  - Python을 사용하여 직관적으로 finite state machine(FSM)을 구현할 수 있게 해주는 package

  - 설치

  ```bash
  $ pip install python-statemachine
  ```

  - 실행해보기
    - state와 event를 구현한다.
    - `send()` method에 event로 선언한 변수명을 string 형태로 넣으면 transition이 발생한다.
    - `before_<evnet>` method를 통해 transition이 발생하기 전에 실행할 action을 설정 가능하다.
    - `on_enter_<state>`, `on_exit_<state>` method를 통해 state로 transition될 때, state에서 다른 state로 transition 될 때 실행할 action을 설정 할 수 있다.

  ```python
  from statemachine import StateMachine, State
  
  
  class TrafficLightMachine(StateMachine):
      # state를 정의한다.
      green = State(initial=True)
      yellow = State()
      red = State()
  
      # event를 정의한다.
      cycle = (
          green.to(yellow)
          | yellow.to(red)
          | red.to(green)
      )
      
      def before_cycle(self, event: str, source: State, target: State, message: str = ""):
          message = ". " + message if message else ""
          return f"Running {event} from {source.id} to {target.id}{message}"
      
      def on_enter_red(self):
          print("Don't move.")
      
      def on_exit_red(self):
          print("Go ahead!")
  
  state_machine = TrafficLightMachine()
  print(state_machine.current_state)		# State('Green', id='green', value='green', initial=True, final=False)
  print(state_machine.send("cycle"))		# Running cycle from green to yellow
  print(state_machine.current_state)		# State('Yellow', id='yellow', value='yellow', initial=False, final=False)
  print(state_machine.send("cycle"))		# Don't move.
  										# Running cycle from yellow to red
  print(state_machine.current_state)		# State('Red', id='red', value='red', initial=False, final=False)
  										# Go ahead!
  print(state_machine.send("cycle"))		# Running cycle from red to green
  ```





