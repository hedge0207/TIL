# 컴포넌트

- 컴포넌트: 특정 부분이 어떻게 생길지 정하는 선언체.
  - 인터페이스를 설계할 때, 사용자가 볼 수 있는 요소는 여러 가지 컴포넌트들이 조합된 것이다.
  - 컴포넌트는 `파일 생성` - `코드 작성` - `모듈 내보내기 및 불러오기` 순으로 사용된다.



- 컴포넌트를 선언하는 방식은 두 가지이다.

  - 클래스형 컴포넌트

  ```react
  import "./App.css";
  import { Component } from "react";
  
  class App extends Component {
    render() {
      const name = "Cha";
      return <div>{name}</div>;
    }
  }
  
  export default App;
  ```

  - 함수형 컴포넌트

  ```react
  import "./App.css";
  
  function App() {
    const name = "Cha";
    return <div>{name}</div>;
  }
  
  export default App;
  ```



- 두 방식의 차이점

  - 클래스형 컴포넌트
    - state 기능 및 라이프사이클 기능 사용 가능
    - 클래스 내부에 커스텀 메서드 정의 가능(함수형 컴포넌트 내부의 함수들은 내부함수지 메서드가 아니다)
    - `render()` 함수가 반드시 있어야 하며 그 안에 보여 줘야 할 JSX를 반환해야 한다.
  - 함수형 컴포넌트
    - 클래스형 컴포넌트보다 선언하기 편하다.
    - 메모리도 덜 사용하며, 프로젝트를 완성하여 빌드한 후 배포할 때도 결과물 파일의 크기가 더 작다(큰 차이는 나지 않는다).
    - state와 라이프 사이클 API 사용이 불가능하다(Hooks의 도움으로 해결).

  - 리액트 공식 문서에서는 함수형 컴포넌트 사용을 권하고 있다.
    - 그러나 클래스형 컴포넌트도 알아야 하기에 일부 예시는 클래스형 컴포넌트로 작성한다.



- 컴포넌트 생성

  - `src` 디렉토리에 컴포넌트 파일 생성
  - 코드 작성하기
    - Reactjs Code Snippet을 설치했다면 `rsc`(클래스형 컴포넌트는 `rcc`) 입력 후 엔터를 누르면 자동으로 완성된다.
    - 일반 함수로 선언하는 것과 화살표 함수로 선언하는 것은 큰 차이는 없다.
    - 다만 화살표 함수가 좀 더 간결하기에 화살표 함수를 사용한다.

  ```react
  import React from "react";
  
  const myComponent = () => {
    return <div>First react component</div>;
  };
  
  export default myComponent;
  ```



- 모듈 내보내기 및 불러오기

  - 위에서 작성한 컴포넌트에서 맨 아래에 있는 코드가 모듈을 내보내겠다는 뜻이다.

  - 불러오기
    - 아래와 같이 `import`를 통해 불러온 후 사용한다.

  ```react
  import React from "react";
  import MyComponent from "./MyComponent";
  
  const App = () => {
    return <MyComponent />;
  };
  
  export default App;
  ```

  - VS Code 기준으로 다른 탭에 `import` 하려는 파일이 열려있다면 `<Component />`와 같이 바로 컴포넌트 태그를 작성하고 ctrl+space를 누르면  `import`문이 자동완성 된다.
    - 닫혀 있을 때도 자동 완성 되게 하려면 프로젝트 최상위 디렉토리에 `jsconfig.json` 파일을 생성한다.
    - 이후 ctrl+space를 누른 후 enter를 누르면 아래와 같은 코드가 자동완성 되고, 이제 불러오려는 컴포넌트가 닫혀 있을 때도 자동완성 된다.
  
  ```json
  {
      "compilerOptions": {
          "target": "es6"
      }
  }
  ```





## props

- properties를 줄인 표현으로 컴포넌트 속성을 설정할 때 사용하는 요소이다.
  - 컴포넌트가 사용되는 과정에서 부모 컴포넌트가 설정하는 값이며, 자식 컴포넌트는 해당 props를 읽기 전용으로만 사용할 수 있다.
  - props 값은 해당 컴포넌트를 불러와 사용하는 부모 컴포넌트에서 설정할 수 있다.
  - 컴포넌트 태그안에 들어가는 값들이 모두 props이다.



- JSX 내부에서 props 렌더링

  - props 값은 컴포넌트 함수의 파라미터로 받아 와서 사용할 수 있다.
  - props를 렌더링 할 때는 JSX 내부에 `{}` 기호로 감싸면 된다.

  ```react
  import React from "react";
  
  const MyComponent = (props) => {
    return <div>Hello! {props.name}</div>;
  };
  
  export default MyComponent;
  ```



- 컴포넌트를 사용할 때 props값 지정하기

  - 아래와 같이 컴포넌트 태그 내부에 지정해준다.

  ```react
  import React from "react";
  import MyComponent from "./MyComponent";
  
  const App = () => {
    // name이라는 props를 내린다.
    return <MyComponent name="Cha" />;
  };
  
  export default App;
  ```
  
  - props를 설정할 때 값을 지정하지 않으면 true가 기본 값으로 들어가게 된다.
  
  ```react
  import React, { Component } from "react";
  import MyComponent from "./EventPracticeSelf";
  
  
  class App extends Component {
    render() {
      return <MyComponent bool />
    }
  }
  
  export default App;
  ```
  
  ```react
  import React from "react";
  
  const MyComponent = (props) => {
    console.log(props.bool);	// true
    return (...);
  };
  
  export default MyComponent;
  ```



- props 기본값 설정하기

  - `defaultProps` 를 사용한다.

  ```react
  import React from "react";
  
  const MyComponent = (props) => {
    return <div>Hello! {props.name}</div>;
  };
  
  MyComponent.defaultProps = {
    name: "기본 이름",
  };
  
  export default MyComponent;
  ```



- 태그 사이의 내용을 보여 주는 children

  - 컴포넌트 태그 사이의 내용을 보여 주는 props.
  - 아래와 같이 컴포넌트 태그 사이에 내용을 입력한다.

  ```react
  import React from "react";
  import MyComponent from "./MyComponent";
  
  const App = () => {
    return <MyComponent>리액트</MyComponent>;
  };
  
  export default App;
  ```

  - children 값을 확인한다.

  ```react
  import React from "react";
  
  const MyComponent = (props) => {
    return (
      <div>
        Hello! {props.name}. <br />
        children 값은 {props.children} 입니다.
      </div>
    );
  };
  
  MyComponent.defaultProps = {
    name: "default name",
  };
  
  export default MyComponent;
  ```



- 비구조화 할당 문법을 통해 props 내부 값 추출하기

  - 지금까지 props 값을 조회할 때마다 `props.name`, `props.children` 등과 같이 props를 붙여줬다.
  - ES6의 비구조화(Destructuring) 할당 문법을 사용하여 내부 값을 바로 추출하는 것이 가능하다.

  ```react
  import React from "react";
  
  const MyComponent = (props) => {
    const { name, children } = props;
    return (
      <div>
        Hello! {name}. <br />
        children 값은 {children} 입니다.
      </div>
    );
  };
  
  MyComponent.defaultProps = {
    name: "default name",
  };
  
  export default MyComponent;
  ```

  - 더 간략히 하면 다음과 같이 하면 된다.

  ```react
  import React from "react";
  
  const MyComponent = ({ name, children }) => {
    return (
      <div>
        Hello! {name}. <br />
        children 값은 {children} 입니다.
      </div>
    );
  };
  
  MyComponent.defaultProps = {
    name: "default name",
  };
  
  export default MyComponent;
  ```



- protoTypes를 통한 props 검증

  - 컴포넌트의 필수 props를 지정하거나 props의 타입을 지정할 때는 `propTypes`를 사용한다.
  - 컴포넌트의 propsTypes를 지정하는 방법은 `defaultProps`를 설정하는 것과 유사하다.
  - `import`를 통해 불러와야 한다.

  ```react
  import React from "react";
  import PropTypes from "prop-types";
  
  const MyComponent = ({ name, children }) => {
    return (
      <div>
        Hello! {name}. <br />
        children 값은 {children} 입니다.
      </div>
    );
  };
  
  MyComponent.defaultProps = {
    name: "default name",
  };
  
  MyComponent.propTypes = {
    name: PropTypes.string,
  };
  
  export default MyComponent;
  ```

  - props 값이 위에서 설정한 타입과 다르면 콘솔창에 error메세지가 출력된다.
    - 정상적으로 동작은 한다.
    - 다른 타입을 넘긴다고 자동으로 형변환이 일어나는 것도 아니다.
    - 값을 아예 넘기지 않으면 error 메세지도 출력되지 않는다.

  ```react
  import React from "react";
  import MyComponent from "./MyComponent";
  
  const App = () => {
    // 위에서는 string을 지정해줬지만 number인 3을 넘겨 error가 발생
    return <MyComponent name={3}>리액트</MyComponent>;
  };
  
  export default App;
  ```

  - `isRequired`를 사용하여 필수 `propTypes` 설정
    - `propTyeps`에 지정한 변수를 받지 않으면  error 메세지가 출력된다.

  ```react
  import React from "react";
  import PropTypes from "prop-types";
  
  const MyComponent = ({ name, favoriteFruit, children }) => {
    return (
      <div>
        Hello! {name}. <br />
        children 값은 {children} 입니다.
        <br />
        제가 좋아하는 과일은 {favoriteFruit}입니다.
      </div>
    );
  };
  
  MyComponent.defaultProps = {
    name: "default name",
  };
  
  MyComponent.propTypes = {
    name: PropTypes.string,
    favoriteFruit: PropTypes.string.isRequired,
  };
  
  export default MyComponent;
  ```

  ```react
  import React from "react";
  import MyComponent from "./MyComponent";
  
  const App = () => {
    return (
      <MyComponent name="Cha" favoriteFruit="사과">
        리액트
      </MyComponent>
    );
  };
  
  export default App;
  ```

  - PropTypes의 종류
    - `array`: 배열
    - `arrayOf(특정 PropType)`: 특정 PropType으로 이루어진 배열을 의미한다.
    - `bool`: boolean
    - `func`: 함수
    - `number`: 숫자
    - `object`: 객체
    - `string`: 문자열
    - `symbol`: ES6의 symbol
    - `node`: 렌더링 할 수 있는 모든 것(숫자, 문자열, JSX코드, children 등)
    - `instanceOf(클래스)`: 특정 클래스의 인스턴스
    - `oneOf([ ])`:주어진 배열 요소 중 하나
    - `oneOfType([React.PropTypes.string, PropTypes.number])`: 주어진 배열 안의 타입 중 하나
    -  `objectOf(React.protoTypes.number)`: 객체의 모든 키 값이 인자로 주어진 PropType인 객체
    - `shape({ name:PropTypes.string, num:PropTypes.number })`: 주어진 스키마를 가진 객체
    - `any`: 아무 종류



- 클래스형 컴포넌트에서 props 사용하기

  - 클래스형 컴포넌트에서는 `render()` 함수에서 `this.props`를 조회하면 된다.
  - `defaultProps`와 `propTypes`는 유사한 방식으로 설정 가능하다.

  ```react
  import React, { Component } from "react";
  import PropTypes from "prop-types";
  
  class MyComponent extends Component {
    static defaultProps = {
      name: "default name",
    };
    static propTypes = {
      name: PropTypes.string,
      favoriteFruit: PropTypes.string.isRequired,
    };
    render() {
      const { name, favoriteFruit, children } = this.props;
      return (
        <div>
          Hello! {name}. <br />
          children 값은 {children} 입니다.
          <br />
          제가 좋아하는 과일은 {favoriteFruit}입니다.
        </div>
      );
    }
  }
  
  export default MyComponent;
  ```



## state

- state
  - 부모 컴포넌트에서만 변경 가능한 props와는 다르게 컴포넌트 내부에서 바뀔 수 있는 값.
  - 리액트에는 두 가지 종류의 state가 있다.
    - 클래스형 컴포넌트가 지니고 있는 state.
    - 함수형 컴포넌트에서 `useState`라는 함수를 통해 사용하는 state.



### 클래스형 컴포넌트의 state

- 클래스형 컴포넌트의 state

  ```react
  import React, { Component } from "react";
  
  class Counter extends Component {
    constructor(props) {
      super(props);
      // state의 초깃값 설정
      this.state = {
        number: 0,
      };
    }
    render() {
      const { number } = this.state;
      return (
        <div>
          <h1>{number}</h1>
          <button
            onClick={() => {
              this.setState({ number: number + 1 });
            }}
          >
            +1
          </button>
        </div>
      );
    }
  }
  
  export default Counter;
  ```

  - 컴포넌트에 state를 설정할 때는 `constructor` 메서드를 사용한다.
    - 컴포넌트의 생성자 메서드이다.
    - 클래스형 컴포넌트에서 `constructor`를 작성할 때는 반드시 `super(props)`를 호출해 주어야 한다. 이 함수가 호출되면 현재 클래스형 컴포넌트가 상속받고 있는 Component 클래스가 지닌 생성자 함수를 호출해 준다.
    - `this.state`로 초기값을 설정해준다. 
    - 컴포넌트의 state는 객체여야 한다.
  - `render()` 함수 부분
    - `render()`  함수 내부에서 state를 조회할 때는 `this.state`를 조회하면 된다.
    - `<button>` 태그 내부에 `onClick`을 props로 넣었는데 이는 버튼이 클릭될 때 호출시킬 함수를 설정할 수 있게 해준다.
    - 이벤트가 호출할 함수를 넣어줄 때는 화살표 함수를 사용하여 넣어 주어야 한다.
    - `this.setState` 함수로 state 값을 변경할 수 있다.



- state 객체 안에 여러 값이 있을 때

  - state 객체 안에는 여러 값이 있을 수 있다.
  - `this.setState()`함수는 인자로 전달된 객체 안에 들어 있는 값만 바꾼다.
  
  ```react
  import React, { Component } from "react";
  
  class Counter extends Component {
    constructor(props) {
      super(props);
      // state의 초깃값 설정
      this.state = {
        number: 0,
        fixedNumber: 0,
      };
    }
    render() {
      const { number, fixedNumber } = this.state;
      return (
        <div>
          <h1>{number}</h1>
          <h2>{fixedNumber}</h2>
          <button
            onClick={() => {
              this.setState({ number: number + 1 });
            }}
          >
            +1
          </button>
        </div>
      );
    }
  }
  
  export default Counter;
  ```



- constructor 없이 state의 초깃값 설정하기

  - `constructor` 메서드 선언 없이 state의 초깃값 설정하기

  ```react
  import React, { Component } from "react";
  
  class Counter extends Component {
    state = {
      number: 0,
      fixedNumber: 0,
    };
  
    render() {
      const { number, fixedNumber } = this.state;
      return (
        <div>
          <h1>{number}</h1>
          <h2>{fixedNumber}</h2>
          <button
            onClick={() => {
              this.setState({ number: number + 1 });
            }}
          >
            +1
          </button>
        </div>
      );
    }
  }
  
  export default Counter;
  ```



- `this.setState`에 객체 대신 함수 인자 전달하기

  - `this.setState`를 사용하여 state 값을 업데이트할 때는 상태가 비동기적으로 업데이트 된다.
  - 아래 코드에서 `this.setState({ number: number + 1 })`를 2번 실행했음에도 숫자는 여전히 1씩 더해진다.
    - 이는 `setState`가 실행된다고 바로 state 값이 변경되는 것은 아니기 때문이다.

  ```react
  import React, { Component } from "react";
  
  class Counter extends Component {
    state = {
      number: 0,
      fixedNumber: 0,
    };
  
    render() {
      const { number, fixedNumber } = this.state;
      return (
        <div>
          <h1>{number}</h1>
          <h2>{fixedNumber}</h2>
          <button
            onClick={() => {
              this.setState({ number: number + 1 });
              this.setState({ number: number + 1 });
            }}
          >
            +1
          </button>
        </div>
      );
    }
  }
  
  export default Counter;
  ```

  - 이를 해결하는 방법이 `setState` 에 함수를 첫 번째 인자로 전달하는 것이다.
  - `setState`에 함수를 인자로 전달 할 때 는 다음과 같은 형식으로 작성한다.
    - `this.setState((prevState,props)=>{ return { 업데이트 할 내용 } })`
    - `prevState`는 기존 상태, `props`는 내려 받은 props를 의미하는데 `props`는 꼭 인자로 받지 않아도 된다.
  
  ```react
  import React, { Component } from "react";
  
  class Counter extends Component {
    state = {
      number: 0,
      fixedNumber: 0,
    };
  
    render() {
      const { number, fixedNumber } = this.state;
      return (
        <div>
          <h1>{number}</h1>
          <h2>{fixedNumber}</h2>
          <button
            onClick={() => {
              this.setState((prevState) => {
                return { number: prevState.number + 1 };
              });
              this.setState((prevState) => {
                return { number: prevState.number + 1 };
              });
            }}
          >
            +1
          </button>
        </div>
      );
    }
  }
  
  export default Counter;
  ```



- `this.setState`가 끝난 후 특정 작업 하기

  - `setState`를 사용하여 값을 업데이트하고 난 다음 특정 작업을 하고 싶을 때는 `setState`의 두번째 파라미터로 콜백 함수를 등록하여 작업을 처리할 수 있다.

  ```react
  import React, { Component } from "react";
  
  class Counter extends Component {
    state = {
      number: 0,
      fixedNumber: 0,
    };
  
    render() {
      const { number, fixedNumber } = this.state;
      return (
        <div>
          <h1>{number}</h1>
          <h2>{fixedNumber}</h2>
          <button
            onClick={() => {
              this.setState(
                (prevState) => {
                  return { number: prevState.number + 1 };
                },
                () => {
                  console.log("setState가 실행되었습니다!");
                }
              );
            }}
          >
            +1
          </button>
        </div>
      );
    }
  }
  
  export default Counter;
  ```



### 함수형 컴포넌트의 state

- 16.8부터는 `useState` 함수를 사용하여 컴포넌트에서도 state를 사용할 수 있게 되었다.
  - 리액트 16.8 이전 버전에서는 함수형 컴포넌트에서 state 사용이 불가능했다.
  - 이 과정에서 Hooks이라는 것을 사용하게 된다.
    - Hook에는 여러 종류가 있지만 현재는 `useState`만 알면 된다.



- `useState` 사용하기

  - `useState` 함수의 인자에는 상태의 초깃값을 넣어준다.
    - 클래스형 컴포넌트의 state 초깃값은 객체여야 하지만 `useState`에서는 객체가 아니어도 된다.
  - `useState` 함수를 호출하면 배열이 반환된다.
    - 배열의 첫 번째 원소는 현재 상태이고, 두 번째 원소는 상태를 바꾸어주는 함수(Setter)이다.
    - 배열 비구조화 할당을 통해 할당이 가능하다.

  ```react
  import React, { useState } from "react";
  
  const Say = () => {
    const [message, setMessage] = useState("초깃값");
    const onClickEnter = () => setMessage("안녕하세요!!");
    const onClickLeave = () => setMessage("안녕히 가세요!!");
    return (
      <div>
        <button onClick={onClickEnter}>입장</button>
        <button onClick={onClickLeave}>퇴장</button>
        <h1>{message}</h1>
      </div>
    );
  };
  
  export default Say;
  ```

  

- 한 컴포넌트에서 `useState` 여러 번 사용하기

  - 한 컴포넌트에서 `useState`를 여러 번 사용하는 것도 가능하다.

  ```react
  import React, { useState } from "react";
  
  const Say = () => {
    const [message, setMessage] = useState("초깃값");
    const onClickEnter = () => setMessage("안녕하세요!!");
    const onClickLeave = () => setMessage("안녕히 가세요!!");
    const [color, setColor] = useState("black");
  
    return (
      <div>
        <button onClick={onClickEnter}>입장</button>
        <button onClick={onClickLeave}>퇴장</button>
        <h1 style={{ color: color }}>{message}</h1>
        <button style={{ color: "red" }} onClick={() => { setColor("red"); }}>
          빨간색
        </button>
        <button style={{ color: "blue" }} onClick={() => { setColor("blue"); }}>
          파란색
        </button>
        <button style={{ color: "green" }} onClick={() => { setColor("green"); }}>
          초록색
        </button>
      </div>
    );
  };
  
  export default Say;
  ```

  



### state 사용시 주의 사항

- state 값을 바꿔야 할 때는 `setState` 혹은 `useState`를 통해 전달받은 세터 함수를 사용해야 한다.

  - 클래스형 컴포넌트
    - 아래와 같이 `setState`를 거치지 않고 변경해선 안된다.

  ```react
  import React, { Component } from "react";
  
  class Counter extends Component {
    state = {
      number: 0,
      fixedNumber: 0,
    };
  
    render() {
      this.state.number=7;
      this.state.fixedNumber=8;
      (...)
    }
  
  export default Counter;
  ```

  - 함수형 컴포넌트
    - 아래와 같이 setter를 사용하지 않고 변경해선 안된다.

  ```react
  import React, { useState } from "react";
  
  const Say = () => {
    const [message, setMessage] = useState("초깃값");
    const onClickEnter = () => setMessage("안녕하세요!!");
    const onClickLeave = () => setMessage("안녕히 가세요!!");
    const [color, setColor] = useState("black");
  
    return (
      message = "김밥";
      color = "white";
      (...)
    );
  };
  
  export default Say;
  ```

  

- 배열이나 객체를 변경해야 할 경우

  - 배열이나 객체의 사본을 만들고, 그 사본의 값을 변경한 후, 그 사본의 상태를 setState 혹은 setter를 통해 업데이트한다.

  ```react
  import React, { useState } from "react";
  
  const Pract = () => {
    const [arr, setArr] = useState([
      { id: 1, name: "Cha" },
      { id: 2, name: "Kim" },
      { id: 3, name: "Lee" },
    ]);
    const [obj, setObj] = useState({ a: 1, b: 2, c: 3 });
    return (
      <div>
        <p>{obj.b}</p>
        <button
          onClick={() => {
            // 사본을 만든다.
            const copyObj = { ...obj, b: 9 };
            return setObj(copyObj);
          }}
        >
          오브젝트 변경
        </button>
        <p>{arr[2].name}</p>
        <button
          onClick={() => {
            // 사본을 만든다.
            const copyArr = arr.concat({ id: 4 });
            copyArr[2].name = "Park";
            return setArr(copyArr);
          }}
        >
          배열 변경
        </button>
      </div>
    );
  };
  
  export default Pract;
  ```
