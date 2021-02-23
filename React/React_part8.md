# Context API

- 전역 데이터의 관리

  - Context API는 리액트 프로젝트에서 전역적으로 사용할 데이터가 있을 때 유용한 기능이다.
    - 사용자 로그인 정보, 애플리케이션 환경 설정, 테마 등.
  - Context API는 리액트 v16.3에서 보다 사용하기 쉽게 개선이 이루어졌다.
  - 리덕스, 리액트 라우터, styled-components등의 리액트 관련 라이브러리는 Context API를 기반으로 구현되었다.
  - Context API를 사용하지 않는 전역 상태 관리
    - 프로젝트 내에서 전역적으로 필요한 상태를 관리해야 할 때는 주로 최상위 컴포넌트인 App의 state에 넣어서 관리하고, props를 통해 다른 컴포넌트에 내려주는 방식으로 사용한다.
    - 그러나 이러한 방식은 거쳐야 할 컴포넌트가 많을 경우 비효율적이고 유지 보수도 힘들어진다.

  - Context API를 사용하면 여러 컴포넌트를 거치지 않고, 전역 데이터를 필요로 하는 컴포넌트로 데이터를 보낼 수 있다.



- Context API 사용법 

  - 새로운 Context를 만들 때는 `createContext` 함수를 사용한다.
    - 인자로 기본값을 넣어준다.
    - `Consumer`, `Provider` 등을 프로퍼티로 갖는 객체가 생성된다.

  ```react
  import { createContext } from "react";
  
  const ColorContext = createContext({ color: "black" });
  
  export default ColorContext;
  ```

  - Context API는 props로 데이터를 받아오는 것이 아니라 `Consumer`로 데이터를 받아온다.
    - 아래와 같이 `Consumer` 사이에 중괄호를 열어서 그 안에 함수를 넣어주는 패턴을 **Function as a child**, 혹은 **Render Props**라고 한다.
    - 컴포넌트의 children이 있어야 할 자리에 일반 JSX 혹은 문자열이 아닌 함수를 전달하는 것이다.
    - 꼭 Context API에서만 사용해야 하는 것은 아니다.

  ```react
  import React from "react";
  import ColorContext from "../contexts/color";
  
  const ColorBox = () => {
    return (
      <ColorContext.Consumer>
        {(value) => (
          <div
            style={{ width: "64px", height: "64px", background: value.color }}
          />
        )}
      </ColorContext.Consumer>
    );
  };
  
  export default ColorBox;
  ```

  - App에서 렌더링

  ```react
  import React from "react";
  import ColorBox from "./components/ColorBox";
  
  const App = () => {
    return (
      <div>
        <ColorBox />
      </div>
    );
  };
  
  export default App;
  ```

  - Render Props 예시
    - 상기했듯 반드시 Context API에서만 사용해야 하는 것은 아니다.

  ```react
  import React from 'react'
  
  const RenderPropsSample = ({children})=>{
      return <div>결과: {children(5)}</div>
  }
  export default RenderPropsSample
  
  // 위와 같은 컴포넌트가 있다면 나중에 렌더링할 때 아래와 같이 할 수 있다.
  <RenderPropsSample>{value => 2*value}</RenderPropsSample>  //<div>10</div>을 렌더링한다.
  ```

  - `Provider`를 사용하면 Context의 value를 변경할 수 있다.
    - 만약 `Provider`를 사용하는데 `value`를 설정하지 않는다면 오류가 발생한다(`<ColorContext.Provider>`).

  ```react
  import React from "react";
  import ColorBox from "./components/ColorBox";
  import ColorContext from "./contexts/color";
  
  const App = () => {
    return (
      <ColorContext.Provider value={{ color: "red" }}>
        <div>
          <ColorBox />
        </div>
      </ColorContext.Provider>
    );
  };
  
  export default App;
  ```



- 동적 Context 사용하기

  - Context의 value에는 무조건 상태 값만 있어야 하는 것은 아니다. 함수를 전달해 줄 수도 있다.
  - 아래 코드에서 `ColorProvider`라는 컴포넌트를 새로 작성했다.
    - 그리고 해당 컴포넌트는 Render Props를 사용하는 `<ColorContext.Provider>`를 렌더링한다.
    - 이 `Provider`의 `value`에는 상태는 `state`로, 업데이트 함수는 `actions`로 묶어서 전달한다.
    - Context에서 값을 동적으로 사용할 때 반드시 묶어줄 필요는 없지만, 이렇게 state와 actions 객체를 따로 분리해 주면 나중에 다른 컴포넌트에서 Context의 값을 사용할 때 편하다.
  - 또한 `createContext`를 사용할 때 기본값으로 사용할 객체도 수정했다.
    - `createContext`의 기본값은 실제 Provider의 value에 넣는 객체의 형태와 일치시켜 주는 것이 좋다.
    - 일치시켜주면 Context 코드를 볼 때 내부 값이 어떻게 구성되어 있는지 파악하기도 쉽고, 실수로 Provider를 사용하지 않았을 때 리액트 애플리케이션에서 에러가 발생하지 않는다.

  ```react
  import { createContext, useState } from "react";
  
  const ColorContext = createContext({
    state: { color: "black", subcolor: "red" },
    actions: {
      setColor: () => {},
      setSubcolor: () => {},
    },
  });
  const ColorProvider = ({ children }) => {
    const [color, setColor] = useState("black");
    const [subcolor, setSubcolor] = useState("red");
  
    const value = {
      state: { color, subcolor },
      actions: { setColor, setSubcolor },
    };
  
    return (
      <ColorContext.Provider value={value}>{children}</ColorContext.Provider>
    );
  };
  // const ColorConsumer = ColorContext.Consumer와 같은 의미(디스트럭처링, Java_part14.디스트럭처링-중첩 객체에서의 활용 참고)
  // 결국 ColorContext.Consumer는 ColorConsumer가 된다.
  const { Consumer: ColorConsumer } = ColorContext;
  export { ColorProvider, ColorConsumer };
  
  export default ColorContext;
  ```

  - 기존의 `ColorContext.Provider`를 `ColorProvider`로 대체한다.
    - `ColorProvider`는 `<ColorContext.Provider>`를 리턴한다.

  ```react
  import React from "react";
  import ColorBox from "./components/ColorBox";
  import ColorContext, { ColorProvider } from "./contexts/color";
  
  const App = () => {
    return (
      <ColorProvider>
        <div>
          <ColorBox />
        </div>
      </ColorProvider>
    );
  };
  
  export default App;
  ```

  - 기존의 `ColorContext.Consumer`를 `ColorConsumer`로 변경한다.
    - 마찬가지로 Render Props를 활용한다.

  ```react
  import React from "react";
  import ColorContext, { ColorConsumer } from "../contexts/color";
  
  const ColorBox = () => {
    return (
      <ColorConsumer>
        {(value) => (
          <>
            <div
              style={{
                width: "64px",
                height: "64px",
                background: value.state.color,
              }}
            />
            <div
              style={{
                width: "32px",
                height: "32px",
                background: value.state.subcolor,
              }}
            />
          </>
        )}
      </ColorConsumer>
    );
  };
  
  export default ColorBox;
  ```

  - 위 코드의 `value`에 비구조화 할당 문법(디스트럭처링)을 사용하면 아래와 같이 쓸 수 있다.
    - 아래 화살표 함수에서 인자로 받는 `value`라 이름 붙인 객체는 `state`를 키로 갖는 프로퍼티를 갖고 있다.
    - 따라서 `value.state`는 `{state}`로 표현이 가능하다. 
    - JavaScript_part14.디스트럭처링-매개변수로 활용 참고

  ```react
  import React from "react";
  import { ColorConsumer } from "../contexts/color";
  
  const ColorBox = () => {
    return (
      <ColorConsumer>
        {({ state }) => (
          <>
            <div
              style={{
                width: "64px",
                height: "64px",
                background: state.color,
              }}
            />
            <div
              style={{
                width: "32px",
                height: "32px",
                background: state.subcolor,
              }}
            />
          </>
        )}
      </ColorConsumer>
    );
  };
  
  export default ColorBox;
  ```

  - Context에 넣은 함수 호출하기
    - 마우스 좌클릭시 큰 정사각형의 색상을 변경.
    - 마우스 우클릭시 작은 정사각형의 색상을 변경, 우클릭은 `onContextMenu`이벤트로 구현한다.

  ```react
  import React from "react";
  import { ColorConsumer } from "../contexts/color";
  const colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"];
  
  const SelectColor = () => {
    return (
      <div>
        <h2>색상을 선택하세요.</h2>
        <ColorConsumer>
          {({ actions }) => (
            <div style={{ display: "flex" }}>
              {colors.map((color) => (
                <div
                  key={color}
                  style={{
                    background: color,
                    width: "24px",
                    height: "24px",
                    cursor: "pointer",
                  }}
                  onClick={() => actions.setColor(color)}
                  onContextMenu={(e) => {
                    // 우클릭하면 메뉴가 뜨는 것을 막기
                    e.preventDefault();
                    actions.setSubcolor(color);
                  }}
                />
              ))}
            </div>
          )}
        </ColorConsumer>
        <hr />
      </div>
    );
  };
  
  export default SelectColor;
  ```



- Consumer 대신 Hook 또는 static contextType 사용하기

  - `useContext` Hook 사용하기
    - 함수형 컴포넌트에서 Context를 보다 쉽게 사용하는 방법
    - 리액트 내장 Hooks 중 useContext를 사용한다.
    - 아래와 같이 훨씬 간편하게 사용 가능하다.
    - 인자로 Context를 받는다.

  ```react
  import React, { useContext } from "react";
  import ColorContext from "../contexts/color"; //Consumer가 아닌 Context를 불러온다.
  
  const ColorBox = () => {
    // 디스트럭처링을 통해 ColorContext 내부의 state에 접근.
    const { state } = useContext(ColorContext);
    return (
      <>
        <div
          style={{
            width: "64px",
            height: "64px",
            background: state.color,
          }}
        />
        <div
          style={{
            width: "32px",
            height: "32px",
            background: state.subcolor,
          }}
        />
      </>
    );
  };
  
  export default ColorBox;
  ```
  - `static contextType` 사용하기
    - 클래스형 컴포넌트에서 Context를 보다 쉽게 사용하는 방법
    - 클래스 상단에 `static contextType` 값을 지정하면 `this.context`를 조회했을 때 `static contextType`에 값으로 할당된  Context 객체(예시의 경우 `ColorContext`)의 value를 가리키게 된다.
    - 클래스 메서드에서도 Context에 넣어 둔 함수를 호출할 수 있다는 장점이 있지만, 한 클래스에서 하나의 Context 밖에 사용하지 못한다는 단점이 존재한다.

  ```react
  import React, { Component } from "react";
  import ColorContext from "../contexts/color";
  
  const colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"];
  
  class SelectColors extends Component {
    static contextType = ColorContext;
  
    handleSetColor = (color) => {
      this.context.actions.setColor(color);
    };
  
    handleSetSubcolor = (subcolor) => {
      this.context.actions.setSubcolor(subcolor);
    };
  
    render() {
      return (
        <div>
          <h2>색상을 선택하세요.</h2>
          <div style={{ display: "flex" }}>
            {colors.map((color) => (
              <div
                key={color}
                style={{
                  background: color,
                  width: "24px",
                  height: "24px",
                  cursor: "pointer",
                }}
                onClick={() => this.handleSetColor(color)}
                onContextMenu={(e) => {
                  e.preventDefault();
                  this.handleSetSubcolor(color);
                }}
              />
            ))}
          </div>
          <hr />
        </div>
      );
    }
  }
  
  export default SelectColors;
  ```





# Redux 이해하기

- Redux

  - 리액트 상태 관리 라이브러리.

    - 그렇다고 리덕스가 리액트에 종속된 라이브러리는 아니다.
    - 컴포넌트의 상태 업데이트 관련 로직을 다른 파일로 분리시켜 더욱 효율적으로 관리할 수 있다.

    - 또한 컴포넌트끼리 똑같은 상태를 공유해야 할 때도 여러 컴포넌트를 거치지 않고 손쉽게 상태 값을 전달하거나 업데이트 할 수  있다.

  - 프로젝트 규모가 클 경우 리덕스를 사용하는 것이 좋다.
    - 단순히 전역 상태 관리만 한다면 Context API를 사용하는 것만으로도 충분하다.
    - 하지만 리덕스를 사용하면 상태를 더욱 체계적으로 관리할 수 있다.
    - 또한 코드의 유지 보수성도 높여주고 작업 효율도 극대화해준다.
  - 상태 관리 뿐 아니라 개발자 도구, 미들웨어 기능 등도 제공한다.



- 리덕스 개념 정의

  - 액션(action)
    - 상태에 어떠한 변화가 필요하면 액션이 발생한다.
    - 액션은 하나의 객체로 표현되는데 형식은 아래 예시와 같다.
    - 액션 객체는 type 필드를 반드시 가지고 있어야 한다. 이 값을 액션의 이름이라고 보면 된다.
    - 그 외의 값들은 상태 업데이트를 할 때 참고해야 할 값이며 작성자 마음대로 넣을 수 있다.

  ```json
  {
      type:'ADD_TODO',
      data: {
          id:1,
          text:'리덕스 학습'
      }  
  }
  ```

  - 액션 생성 함수(action creator)
    - 액션 객체를 만들어 주는 함수.
    - 어떤 변화를 일으켜야 할 때마다 액션 객체를 만들어야 하는데 매번 액션 객체를 직접 작성하기 번거로울 수 있고, 만드는 과정에서 실수로 정보를 놓칠수도 있기에 함수를 만들어서 관리한다.

  ```react
  // 일반 함수
  function addTodo(data){
      return {
          type:'ADD_TODO',
          data: {
            id:1,
            text:'리덕스 학습'
          }
      }
  }
  
  // 화살표 함수
  const addTodo = data => {
    type:'ADD_TODO',
    data: {
      id:1,
      text:'리덕스 학습'
      }
  }
  ```
  
  - 리듀서(reducer)
      - 변화를 일으키는 함수.
      - 액션을 만들어서 발생시키면 리듀서가 현재 상태와 전달받은 액션 객체를 파라미터로 받아 온다.
      - 그리고 두 값을 참고하여 새로운 상태를 만들어 반환해준다.
  
  ```javascript
  const initialState = {
      conter:1
  }
  
  function reducer(state = initialState,action){
      switch(action,type){
          case INCREMENT:
              return {
                  counter:state.counter+1
              }
          default:
              return state;
      }
  }
  ```
  
    - 스토어(store)
      - 프로젝트에 리덕스를 적용하기 위해 스토어를 만든다.
      - 한 개의 프로젝트는 단 하나의 스토어만 가질 수 있다.
      - 스토어 안에는 현재 애플리케이션 상태와 리듀서가 들어가 있으며, 그 외에도 몇 가지 중요한 내장 함수를 지닌다.
    - 디스패치(dispatch)
      - 스토어의 내장 함수 중 하나.
      - 액션을 발생시키는 것.
      - 액션 객체를 인자로 받는다.
      - 이 함수가 호출되면 스토어는 리듀서 함수를 실행시켜 새로운 상태를 만들어 준다.
    - 구독(subscribe)
      - 스토어 내중 함수 중 하나.
      - 리스너 함수를 인자로 넣어서 호출하면, 인자로 받은 리스너 함수가 액션이 디스패치되어 상태가 업데이트 될 때마다 호출 된다.
  
  ```javascript
  const listener = () => {
      console.log('상태가 업데이트 되었습니다.')
  }
  const unsubscribe = store.subscribe(listener);
  
  unsubscribe(); // 추후 구독을 비활성화할 때 함수를 호출
  ```
  
  



- Redux의 세 가지 규칙
  - 단일 스토어
    - 하나의 애플리케이션에는 하나의 스토어가 들어 있다.
    - 여러 개의 스토어를 사용하는 것이 불가능하지는 않으나, 상태 관리가 복잡해질 수 있으므로 권장하지 않는다.
  - 읽기 전용 상태
    - 리덕스 상태는 읽기 전용이다.
    - 리덕스도 상태를 업데이트 할 때 기존의 객체는 건드리지 않고 새로운 객체를 생성해 주어야 한다.
    - 리덕스에서 불변성을 유지해야 하는 이유는 내부적으로 데이터가 변경되는 것을 감지하기 위해 얕은 비교를 하기 때문이다.
    - 객체의 변화를 감지할 때 객체의 깊숙한 안쪽까지 비교하는 것이 아니라 겉핥기 식으로 비교하여 좋은 성능을 유지할 수 있는 것이다.
  - 리듀서는 순수한 함수
    - 아래 4가지는 리듀서가 순수한 함수이기 위한 조건이다.
    - 리듀서 함수는 이전 상태와 액션 객체를 파라미터로 받는다.
    - 파라미터 외의 값에 의존해선 안된다.
    - 이전 상태는 절대로 건드리지 않고, 변화를 준 새로운 상태 객체를 만들어서 반환한다.
    - 똑같은 파라미터로 호출된 리듀서 함수는 언제나 똑같은 값을 반환해야 한다.
    - 따라서 리듀서 함수 내부에서 랜덤 값을 만들거나, Date 함수를 사용하여 시간을 가져오거나, 네트워크에 요청을 하는 등의 코드를 작성해선 안된다.





## 리액트 없이 쓰는 리덕스

- 리덕스는 리액트에 종속되는 라이브러리가 아니다.
  - 리액트에서 사용하려고 만들어졌지만 다른 UI 라이브러리/프레임워크와 함께 사용할 수 있다.
  - 바닐라 JS와 함께 사용할 수도 있다.



- Parcel로 프로젝트 만들기

  - Parcel 설치하기

  ```bash
  $ yarn global add parcel-bundler
  # yarn global로 설치가 되지 않는다면 npm으로 설치
  $ npm install -g parcel-bundler
  ```
  
  - package.json 생성하기
  
  ```bash
  $ yarn init -y
  ```
  
  - index.html 생성
  
  ```html
  <html>
      <head>
          <link rel='stylesheet' type="text/css" href="index.css">
      </head>
      <body>
          <div class="toggle"></div>
          <hr>
          <h1>0</h1>
          <button id="increase">+1</button>
          <button id="decrease">-1</button>
          <script src="./index.js"></script>
      </body>
  </html>
  ```
    - DOM 레퍼런스 만들기
      - UI를 관리할 때 별도의 라이브러리를 사용하지 않기 때문에 DOM을 직접 수정해 줘야 한다.
      - index.js 파일에 아래와 같이 작성한다.
  
  ```javascript
  const divToggle = document.querySelector(".toggle");
  const counter = document.querySelector("h1");
  const btnIncrease = document.querySelector("#increase");
  const btnDecrease = document.querySelector("#decrease");
  ```
  
    - index.css 생성
  
  ```css
  .toggle {
      border: 2px solid black;
      width: 64px;
      height: 64px;
      border-radius: 32px;
      box-sizing: border-box;
  }
  
  .toggle.active {
      background: yellow;
  }
  ```
  
    - 실행하기
  
  ```bash
  $ yarn parcel index.html
  ```
  
    - 리덕스 모듈 설치
  
  ```bash
  $ yarn add redux
  ```





- 액션 타입과 액션 생성 함수 정의

  - 액션은 프로젝트 상태에 변화를 일으키는 것이다.
  - 액션 이름은 문자열 형태로, 주로 대문자로 작성하며, 액션 이름은 고유해야 한다.

  ```javascript
  const divToggle = document.querySelector(".toggle");
  const counter = document.querySelector("h1");
  const btnIncrease = document.querySelector("#increase");
  const btnDecrease = document.querySelector("#decrease");
  
  const TOGGLE_SWITCH = "TOGGLE_SWITCH";
  const INCREASE = "INCREASE";
  const DECREASE = "DECREASE";
  ```

  - 이 액션 이름을 사용하여 액션 객체를 만드는 액션 생성 함수를 작성한다.

  ```javascript
  const toggleSwitch = () => ({ type: TOGGLE_SWITCH });
  // 어차피 +1만 가능하므로 굳이 difference를 안 받아도 된다. 그러나 인자를 받는 것이 가능하다는 것을 보여주는 것이다.
  const increase = (difference) => ({ type: INCREASE, difference }); 
  const decrease = () => ({ type: DECREASE });
```
  
- 이 프로젝트에서 사용할 초깃값을 정의한다.
  
  ```javascript
  const initialState = {
    toggle: false,
    counter: 0,
  };
  ```



- 리듀서 함수 정의

  - 리듀서는 변화를 일으키는 함수이다.
  - 파라미터로 state와 action 값을 받아 온다.
    - 리듀서 함수가 맨 처음 호출돨 때는 state 값이 undefined이므로, 이를 위해 state에 기본값을 준다.
  - 변환된 state를 반환한다.
  
  ```javascript
  const divToggle = document.querySelector(".toggle");
  const counter = document.querySelector("h1");
  const btnIncrease = document.querySelector("#increase");
  const btnDecrease = document.querySelector("#decrease");
  
  const TOGGLE_SWITCH = "TOGGLE_SWITCH";
  const INCREASE = "INCREASE";
  const DECREASE = "DECREASE";
  
  const toggleSwitch = () => ({ type: TOGGLE_SWITCH });
  const increase = (difference) => ({ type: INCREASE, difference });
  const decrease = () => ({ type: DECREASE });
  
  const initialState = {
    toggle: false,
    counter: 0,
  };
  
  // state가 undefined일 때는initialState를 기본값으로 사용
  function reducer(state = initialState, action) {
    switch (action.type) {
      case TOGGLE_SWITCH:
        // state를 반환
        return {
          ...state, // 불변성 유지를 위해 spread 문법 사용
          toggle: !state.toggle,
        };
      case INCREASE:
        return {
          ...state,
          counter: state.counter + action.difference,
        };
      case DECREASE:
        return {
          ...state,
          counter: state.counter - 1,
        };
      default:
        return state;
    }
  }
  ```



- 스토어 만들기

  - 스토어를 만들 때는 createStore 함수를 불러와서 사용한다.
  - 파라미터로 reducer 함수를 받는다.
  - 스토어는 상태를 저장한다.
    - 위에서 `reducer` 함수를 정의할 때 첫 번째 인자인 state에 기본값을 설정해 줬다.
    - 이는 `reducer`를 실행시킬 때 따로 state 인자를 받지 못하기 때문에 undefined가 첫 번째 인자로 들어가기 때문이다.
    - 따라서 초깃값만 설정해 놓으면,  store는 두 번째 실행 부터는 state의 상태를 기억하여 첫 번째 인자에 자신이 기억하는 state가 정상적으로 들어가게 된다.

  ```javascript
  // index.js
  import { createStore } from "redux";
  (...)
  const store = createStore(reducer);
  ```



- render 함수 만들기

  - 구독을 통해 상태가 업데이트 될 때마다 호출될 함수.
  - 리액트의 render와는 달리 이미 html을 사용하여 만들어진 UI의 속성을 상태에 따라 변경해준다.

  ```javascript
  import { createStore } from "redux";
  
  (...)
  
  const store = createStore(reducer);
  const render = () => {
    // store의 getState 메서드를 통해 현재 상태를 불러온다.
    const state = store.getState();
    // 토글 처리
    if (state.toggle) {
      divToggle.classList.add("active");
    } else {
      divToggle.classList.remove("active");
    }
    // 카운터 처리
    counter.innerText = state.counter;
  };
  
  render();
  ```



- 구독하기

  - 스토어의 상태가 바뀔 때마다 위에서 만든 render 함수가 호출되도록 작성한다.
    - 스토어의 상태가 바뀔때마다 리렌더링 되도록 해준다.
    - 스토어의 내장 함수 `subscribe`를 사용.
  - `subscribe`는 파라미터로 함수 형태의 값을 받는다.
    - 전달된 함수는 추후 액션이 발생하여 상태가 업데이트 될 때마다 호출된다.
  - 바닐라 JS에서는 `subscribe` 함수를 사용하지만 react 프로젝트에서는 사용하지 않는다.
  - 컴포넌트에서 리덕스 상태를 조회하는 과정에서 react-redux라는 라이브러리가 이 작업을 대신해준다.
  
  ```javascript
  (...)
  const render = () => {
    // 현재 상태를 불러온다.
    const state = store.getState();
    // 토글 처리
    if (state.toggle) {
      divToggle.classList.add("active");
    } else {
      divToggle.classList.remove("active");
    }
    // 카운터 처리
    counter.innerText = state.counter;
  };
  
  render();
  store.subscribe(render);
  ```



- 디스패치

  - 액션을 발생시키는 것을 디스패치라 한다.
  - 스토어의 내장 함수 `dispatch`를 사용한다.
  - 이 함수가 호출되면 액션이 생성되고, 스토어는 리듀서 함수를 실행시켜 새로운 상태를 만들어준다.

  ```javascript
  divToggle.onclick = () => {
    store.dispatch(toggleSwitch());
  };
  btnIncrease.onclick = () => {
    store.dispatch(increase(1));
  };
  btnDecrease.onclick = () => {
    store.dispatch(decrease());
  };
  ```

  

  







