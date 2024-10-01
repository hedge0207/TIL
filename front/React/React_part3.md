# 이벤트 핸들링

- 이벤트
  - 사용자가 웹 브라우저에서 DOM 요소들과 상호 작용하는 것.
  - 리액트의 이벤트 핸들링은 HTML, JS의 이벤트 핸들링과 차이가 있다.



- React에서 이벤트 사용시 주의사항
  - 이벤트 이름은 카멜 표기법으로 작성한다.
  - 이벤트에서 실행할 JS코드를 전달하는 것이 아니라, 함수 형태의 값을 전달한다.
  - DOM 요소에만 이벤트를 설정할 수 있다.
      - 직접 만든 컴포넌트에는 이벤트를 설정할 수 없다.



- 이벤트에서 실행 할 JS를 전달하는 것이 아니라, 함수 형태의 값을 전달한다.

  - 함수를 전달해야지 함수를 호출하는 JS코드를 전달해선 안된다.
    -  JS코드를 전달할 경우 해당 이벤트가 발생할 때 함수가 실행되는 것이 아니라 렌더링 될 때 함수가 실행된다.
    - 즉, 최초 렌더링 될 때 `<button onClick={handleClick()}>버튼!!</button>`이 렌더링 되면서 `handleClick()` 함수가 실행된다.

  ```react
  import React from "react";
  
  const EventPracticeSelf = () => {
    const handleClick = () => {
      console.log("함수가 실행되었습니다.");
    };
    return (
      <div>
        {/* 함수를 전달 */}
        <button onClick={handleClick}>버튼!!</button>
        {/* 함수를 호출하는 JS 코드를 전달 */}
        <button onClick={handleClick()}>버튼!!</button>
      </div>
    );
  };
  
  export default EventPracticeSelf;
  ```

  - 만일 인자를 넘겨야 한다면 화살표 함수를 사용하여 콜백 함수로 호출한다.

  ```react
  import React from "react";
  
  const EventPracticeSelf = () => {
    const handleClick = (message) => {
      console.log(message);
    };
    return (
      <div>
        <button
          onClick={() => {
            handleClick("함수가 실행되었습니다!");
          }}
        >
          버튼!!
        </button>
      </div>
    );
  };
  
  export default EventPracticeSelf;
  ```

  



- React에서 지원하는 이벤트의 종류

  > https://ko.reactjs.org/docs/events.html#supported-events

  - 위 사이트에서 확인 가능하다.



- 이벤트 핸들링

  ```react
  import React, { Component } from "react";
  
  class EventPractice extends Component {
    state = {
      message: "",
    };
    render() {
      return (
        <div>
          <h1>이벤트 연습</h1>
          <input type="text" name="msg" placeholder="아무거나 입력하세요!"
            onChange={(e) => {
              this.setState({ message: e.target.value });
            }}
          />
          <button onClick={() => {
              alert(this.state.message);
              this.setState({
                message: "",
              });
            }}
          >
            확인
          </button>
        </div>
      );
    }
  }
  
  export default EventPractice;
  ```

  - `onChange` 이벤트에 있는 `e` 객체는 `SyntheticEvent`로 웹 브라우저의 네이티브 이벤트를 감싸는 객체다.
    - 네이티브 이벤트와 인터페이스가 같으므로 순수JS에서 HTML 이벤트를 다룰 때와 똑같이 사용하면 된다.
    - `SyntheticEvent`는 네이티브 이벤트와 달리 이벤트가 끝가고 나면 이벤트 객체가 초기화되므로 정보를 참조할 수 없다.
    - 만약 비동기적으로 이벤트 객체를 참조할 일이 있다면 `e.persist()` 함수를 호출해야 한다.
    - input 창의 내용이 변할 때 마다 `setState()` 함수가 실행되어 `state.message`의 내용이 변하게 된다.
  - 버튼을 클릭하면 현재 `state.message`값이 alert창에 표시되고, `state.message`가 다시 빈 문자열로 초기화 된다.



- 임의 메서드 만들기

  - 이벤트에서 실행할 JS코드를 전달하는 것이 아니라, 함수 형태의 값을 전달한다.
    - 위 예제에서는 화살표 함수를 사용하여 정의한 함수를 바로 넘기는 방법을 사용했다.
    - 이 방법 대신 함수를 미리 선언한 함수를 넘기는 방법도 있다.
    - 성능상으로는 차이가 거의 없지만 가독성은 훨씬 높다.
  - 위에서 작성한 코드를 아래와 같이 작성하는 것이 가능하다(정석적인 방식).
    - `this`는 호출부에 따라 결정된다.
    - 아래의 경우 HTML 요소의 이벤트에 의해 호출된다.
    - 클래스의 임의 메서드(`handleChange`, `handleClick`)가 특정 HTML 요소의 이벤트로 등록되는 과정에서 메서드와 `this`의 연결이 끊기게 된다.
    - 이 때문에 임의 메서드가 이벤트로 등록되어도 this를 컴포넌트 자신으로 제대로 가리키기 위해서는 메서드를 `this`와 비인딩해야 한다.

  ```react
  import React, { Component } from "react";
  
  class EventPractice extends Component {
    state = {
      message: "",
    };
    constructor(props) {
      super(props);
      // 바인딩
      this.handleChange = this.handleChange.bind(this);
      this.handleClick = this.handleClick.bind(this);
    }
    
    /*메서드 단축 구문으로 아래와 같은 함수를
    handleChange: function(e){
    	...
    }
    아래와 같이 선언한 메서드다.
    */
    handleChange(e) {
      // 위에서 바인딩을 해줬기에, 이 메서드 내부에서 this는 컴포넌트 자신을 가리키게 된다.
      console.log(this)	// EventPractice {...}
      this.setState({
        message: e.target.value,
      });
    }
    handleClick() {
      alert(this.state.message);
      this.setState({
        message: "",
      });
    }
    render() {
      return (
        <div>
          <h1>이벤트 연습</h1>
          <input
            type="text"
            name="message"
            placeholder="아무거나 입력하세요!"
            value={this.state.message}
            onChange={this.handleChange}
          />
          <button onClick={this.handleClick}>확인</button>
        </div>
      );
    }
  }
  
  export default EventPractice;
  ```

  - Property Initializer Syntax를 사용한 메서드 작성
    - 메서드 바인딩은 생성자 메서드(`constructor`)에서 하는 것이 정석이다(위의 방식).
    - 하지만 위와 같은 방식이 불편할 경우 babel의 transform-class-properties 문법을 사용하여 화살표 함수 형태로 메서드를 정의할 수 있다.
    - 화살표 함수의 this는 항상 상위 스코프의 this를 가리킨다.

  ```react
  import React, { Component } from "react";
  
  class EventPractice extends Component {
    state = {
      message: "",
    };
  
    handleChange = (e) => {
      this.setState({
        message: e.target.value,
      });
    };
    handleClick = () => {
      console.log(this);
      alert(this.state.message);
      this.setState({
        message: "",
      });
    };
    render() {
      return (...);
    }
  }
  
  export default EventPractice;
  ```



- 복수의 input을 처리하기

  - 아래의 내용을 활용하여 복수의 input창을 활용할 수 있다.
    - `e.target.name`에는 `<input>`에서 설정한 `name` 속성을 가리킨다.
    - 객체 안에서 key를 `[]`로 감싸면 그 안에 넣은 레퍼런스가 가리키는 실제 값이 key로 사용된다.

  ```react
  import React, { Component } from "react";
  
  class EventPractice extends Component {
    state = {
      username: "",
      message: "",
    };
  
    handleChange = (e) => {
      this.setState({
        [e.target.name]: e.target.value,
      });
    };
    handleClick = () => {
      alert(this.state.username + ": " + this.state.message);
      this.setState({
        username: "",
        message: "",
      });
    };
    render() {
      return (
        <div>
          <h1>이벤트 연습</h1>
          <input
            type="text"
            name="username"
            placeholder="username을 입력하세요!"
            value={this.state.username}
            onChange={this.handleChange}
          />
          <input
            type="text"
            name="message"
            placeholder="message를 입력하세요!"
            value={this.state.message}
            onChange={this.handleChange}
          />
          <button onClick={this.handleClick}>확인</button>
        </div>
      );
    }
  }
  
  export default EventPractice;
  ```



- input 창에서 enter를 눌렀을 때 이벤트 발생시키기

  - `onKeyPress` 이벤트를 사용한다.

  ```react
  import React, { Component } from "react";
  
  class EventPractice extends Component {
    state = {
      username: "",
    };
  
    handleChange = (e) => {
      this.setState({
        [e.target.name]: e.target.value,
      });
    };
    handleClick = () => {
      alert(this.state.username);
      this.setState({
        username: "",
      });
    };
    handleKeyPress = (e) => {
      if (e.key === "Enter") {
        this.handleClick();
      }
    };
  
    render() {
      return (
        <div>
          <h1>이벤트 연습</h1>
          <input
            type="text"
            name="username"
            placeholder="username을 입력하세요!"
            value={this.state.username}
            onChange={this.handleChange}
            onKeyPress={this.handleKeyPress}
          />
          <button onClick={this.handleClick}>확인</button>
        </div>
      );
    }
  }
  
  export default EventPractice;
  ```



- 함수형 컴포넌트로 구현하기

  - 위 코드를 함수형 컴포넌트로 똑같이 구현하면 아래와 같다.
    - 아래 예제에서는 `e.target.name`을 활용하지 않고 `onChange` 관련 함수를 두 개 생성했다.

  ```react
  import React, { useState } from "react";
  
  const EventPractice = () => {
    const [username, setUsername] = useState("");
    const [message, setMessage] = useState("");
    const onChangeUsername = (e) => setUsername(e.target.value);
    const onChangeMessage = (e) => setMessage(e.target.value);
  
    const onClick = () => {
      alert(username + ": " + message);
      setUsername("");
      setMessage("");
    };
    const onKeyPress = (e) => {
      if (e.key === "Enter") {
        onClick();
      }
    };
    return (
      <div>
        <h1>이벤트 연습-함수형 컴포넌트</h1>
        <input
          type="text"
          name="username"
          placeholder="username을 입력하세요"
          value={username}
          onChange={onChangeUsername}
        />
        <input
          type="text"
          name="message"
          placeholder="message를 입력하세요"
          value={message}
          onChange={onChangeMessage}
          onKeyPress={onKeyPress}
        />
        <button onClick={onClick}>확인</button>
      </div>
    );
  };
  
  export default EventPractice;
  ```

  - `e.target.name`을 활용하면 아래와 같이 작성 가능하다.

  ```react
  import React, { useState } from "react";
  
  const EventPractice = () => {
    const [form, setForm] = useState({
      username: "",
      message: "",
    });
    // 객체 디스트럭쳐링
    const { username, message } = form;
    const onChange = (e) => {
      //Spread 문법, React에서는 객체를 변경할 때 복사본을 생성후 해당 복사본으로 교체해야 한다.
      const nextForm = { ...form, [e.target.name]: e.target.value };
      setForm(nextForm);
    };
  
    const onClick = () => {
      alert(username + ": " + message);
      setForm({
        username: "",
        message: "",
      });
    };
    const onKeyPress = (e) => {
      if (e.key === "Enter") {
        onClick();
      }
    };
    return (
      <div>
        <h1>이벤트 연습-함수형 컴포넌트</h1>
        <input
          type="text"
          name="username"
          placeholder="username을 입력하세요"
          value={username}
          onChange={onChange}
        />
        <input
          type="text"
          name="message"
          placeholder="message를 입력하세요"
          value={message}
          onChange={onChange}
          onKeyPress={onKeyPress}
        />
        <button onClick={onClick}>확인</button>
      </div>
    );
  };
  
  export default EventPractice;
  ```




- `preventDefault()`

  
  - 태그 혹은 이벤트의 기본적인 동작 방식(a 태그의 경우 설정된 url로 이동 등)을 막는 함수이다.
  - `<form>`의 `onSubmit` 이벤트는 새로고침을 발생시킨다.
  
  - `preventDefault()`로 새로 고침이 일어나는 것을 막아줘야 한다.
  - 새로고침이 발생하는 것을 막아야 하는 데도 굳이 `<form>`을 쓰는 이유
    - `<form>` 태그는 태그 내부에 `submit` 속성을 가진 `<button>`이 있을 경우(`<button type="submit">`) 버튼을 눌러도 onSubmit 이벤트가 발생하고, `<form>` 내부의 `<input>`에서 enter를 눌러도 `onSubmit` 이벤트가 발생한다.
    - 만일 input 태그와 button 태그로 구현한다면 `onKeypress`(input 태그), `onClick`(button 태그) 이라는 2개의 이벤트를 헨들링 해야 하지만 form 태그를 사용하면 `onSubmit` 이벤트만 핸들링 하면 되기에 더 편하다.
  
  ```react
  import React, { useCallback, useState } from "react";
  import { MdAdd } from "react-icons/md";
  import "./TodoInsert.scss";
  
  const TodoInsert = () => {
    const [value, setValue] = useState("");
    const onChange = useCallback((e) => {
      setValue(e.target.value);
    }, []);
  
    const onSubmit = useCallback(
      (e) => {
        setValue("");
        // onSubmit 이벤트는 새로고침을 발생시키기에 이를 방지하기 위해 아래와 같이 해준다.
        e.preventDefault();
      },
      [value],
    );
  
    return (
      <form className="TodoInsert" onSubmit={onSubmit}>
        <inpu
          value={value}
          onChange={onChange}
        />
        <button type="submit">
          <MdAdd />
        </button>
      </form>
    );
};
  
  export default TodoInsert;
  ```
  
  

# ref

- ref

  - HTML에서 id를 사용하여 DOM에 이름을 다는 것 처럼 리액트 프로젝트 내부에서 DOM에 이름을 다는 방법이 ref(reference)라는 개념이다.
  - DOM을 꼭 직접적으로 건드려야 할 때 사용한다.
    - 특정 input에 포커스 주기
    - 스크롤 박스 조사하기
    - Canvas 요소에 그림 그리기 등
  - 아래와 같은 HTML의 경우 굳이 DOM에 접근하지 않아도 state로 구현이 가능하다.

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
      <style>
          .success{
              background-color: green;
          }
          .failure{
              background-color: red;
          }
      </style>
      <script>
          function validate(){
              // DOM에 접근
              var input = document.getElementById('password')
              input.className=''
              if(input.value==="0000"){
                  input.className='success'
              } else {
                  input.className='failure'
              }
          }
      </script>
  </head>
  <body>
      <input type="password" id="password">
      <button onclick="validate()">Validate</button>
  </body>
  </html>
  ```

  - state로 구현

  ```react
  // state를 활용하여 구현 가능하다.
  import React, { Component } from "react";
  import "./ValidationSample.css";
  
  class ValidationSample extends Component {
    state = {
      password: "",
      clicked: false,
      validated: false,
    };
    handleChange = (e) => {
      this.setState({
        password: e.target.value,
      });
    };
    handleButtonClick = () => {
      this.setState({
        clicked: true,
        validated: this.state.password === "0000",
      });
    };
    render() {
      return (
        <div>
          <input
            type="password"
            value={this.state.password}
            onChange={this.handleChange}
            className={
              this.state.clicked
                ? this.state.validated
                  ? "success"
                  : "failure"
                : ""
            }
          />
          <button onClick={this.handleButtonClick}>검증하기</button>
        </div>
      );
    }
  }
  
  export default ValidationSample;
  ```

  - ref은 두 가지 방식으로 사용 가능하다.
    - 콜백 함수를 통한 ref 설정
    - createRef을 통한 ref 설정

  - 지금은 class형 컴포넌트에서 ref을 사용하는 방법만 알면 된다.
    - 함수형 컴포넌트에서 ref을 사용하기 위해서는 Hooks에 대한 지식이 있어야 한다.



- 콜백 함수를 통한 ref 설정

  - ref을 만드는 가장 기본적인 방법
  - ref을 달고자 하는 요소에 ref라는 콜백 함수를 props로 전달해 주면 된다.
  - 이 콜백 함수는 ref 값을 파라미터로 전달 받는다.
  - 함수 내부에서 파라미터로 받은 ref를 컴포넌트의 멤버 변수로 설정해준다.

  ```react
  // 예시
  // 이제 this.input은 input 요소의 DOM을 가리킨다.
  // ref 이름은 꼭 DOM 타입과 일치시켜야 하는 것은 아니다.
  // this.something = ref와 같이 지정하는 것도 가능하다.
  <input ref={(ref)=>{this.input=ref}} />
  ```



- `createRef`을 통한 ref 설정

  - 리액트에 내장되어 있는 `createRef` 함수를 사용하는 방법
  - 리액트 v16.3부터 도입되었다.
  - 우선 `React.creatRef()`를 멤버 변수로 담아줘야 한다.
  - 그리고 해당 변수를 ref를 달고자 하는 요소에 ref props로 넣어 주면 ref 설정이 완료된다.
  - 이후 `this.input.current`를 조회하여 ref를 설정해준 DOM에 접근한다.

  ```react
  import React, { Component } from "react";
  
  class RefSample extends Component {
    input = React.createRef();
  
    handleFocus = () => {
      //this.input은 input DOM요소를 가리키고 있다.
      this.input.current.focus();
    };
    render() {
      return (
        <div>
          <input ref={this.input} />
        </div>
      );
    }
  }
  
  export default RefSample;
  ```

  

- ref 적용

  - 구현할 내용
    - 위에서 state로 구현한 코드를 보면 input창을 클릭하면 input 창에 포커스가 넘어가고 텍스트 커서가 깜빡인다.
    - 버튼을 누르면 포커스가 버튼으로 옮겨가고 input창의 텍스트 커서가 더 이상 깜빡이지 않는다.
    - 버튼을 한 번 눌렀을 때, 포커스가 다시 input 쪽으로 자동으로 넘어가도록 코드를 작성할 것이다.
  - 구현
    - `<input>`에 ref를 달고
    - 버튼에 달린  `onClick` 이벤트 코드를 수정한다.

  ```react
  import React, { Component } from "react";
  import "./ValidationSample.css";
  
  class ValidationSample extends Component {
    state = {
      password: "",
      clicked: false,
      validated: false,
    };
    handleChange = (e) => {
      this.setState({
        password: e.target.value,
      });
    };
    handleButtonClick = () => {
      this.setState({
        clicked: true,
        validated: this.state.password === "0000",
      });
      this.inputRef.focus();
    };
    render() {
      return (
        <div>
          <input
            ref={(ref) => (this.inputRef = ref)}
            type="password"
            value={this.state.password}
            onChange={this.handleChange}
            className={
              this.state.clicked
                ? this.state.validated
                  ? "success"
                  : "failure"
                : ""
            }
          />
          <button onClick={this.handleButtonClick}>검증하기</button>
        </div>
      );
    }
  }
  
  export default ValidationSample;
  ```



- 컴포넌트에 ref 달기

  - 컴포넌트에도 ref를 다는 것이 가능하다.
    - 이 방법은 주로 컴포넌트 내부에 있는 DOM을 컴포넌트 외부에서 사용할 때 사용한다.
  - 아래와 같이 달 수 있다.
    - `MyComponent` 내부의 메서드 및 멤버 변수에도, 즉 내부의 ref에도 접근이 가능해진다.

  ```react
  <MyComponent ref={(ref) => {this.myComponent=ref}}>
  ```

  - 컴포넌트를 생성한다.

  ```react
  import React, { Component } from "react";
  
  class ScrollBox extends Component {
    // 컴포넌트 메서드 생성
    scrollToBottom = () => {
      // 디스트럭처링을 사용
      // scrollHeight,clientHeight 등은 DOM 노드가 가진 값들이다.
      const { scrollHeight, clientHeight } = this.box;
      this.box.scrollTop = scrollHeight - clientHeight;
    };
  
    render() {
      const style = {
        border: "1px solid black",
        height: "300px",
        width: "300px",
        overflow: "auto",
        position: "relative",
      };
      const innerStyle = {
        width: "100%",
        height: "650px",
        background: "linear-gradient(white, black)",
      };
      return (
        <div
          style={style}
          ref={(ref) => {
            this.box = ref;
          }}
        >
          <div style={innerStyle} />
        </div>
      );
    }
  }
  export default ScrollBox;
  ```

  - 부모 컴포넌트에서 사용하기
    - 클래스형으로 아래와 같이 작성한다.

  ```react
  import React, { Component } from "react";
  import ScrollBox from "./ScrollBox";
  
  class App extends Component {
    render() {
      return (
        <div>
          {/* 자식 컴포넌트를 this.scrollBox에 담고*/}
          <ScrollBox ref={(ref) => (this.scrollBox = ref)} />
          {/* 자식 컴포넌트의 메서드를 사용*/}
          <button onClick={() => this.scrollBox.scrollToBottom()}>
            맨 밑으로
          </button>
        </div>
      );
    }
  }
  
  export default App;
  ```

  









