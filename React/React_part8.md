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
  
  // 위와 같은 컴포넌트가 있다면 나중에 사용할 때 아래와 같이 할 수 있다.
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
    - 그리고 해당 컴포넌트는 `<ColorContext.Provider>`를 렌더링한다.
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
  console.log(ColorContext);
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

  



















