# 컴포넌트의 라이프사이클

- 라이프사이클
  - 모든 리액트 컴포넌트에는 라이프사이클(수명주기)이 존재한다.
    - 컴포넌트의 수명은 페이지에 렌더링되기 전인 준비 과정에서 시작하여 페이지에서 사라질 때 끝난다.
  - 컴포넌트를 처음으로 렌더링 할 때 어떤 작업을 처리해야 하거나 컴포넌트를 업데이트하기 전후로 어떤 작업을 처리해야 할 수도 있고, 불필요한 업데이트를 방지해야 할 수도 있다.
    - 이럴 때 컴포넌트 라이프사이클 메서드를 사용한다.
    - 라이프사이클 메서드는 클래스형 컴포넌트에서만 사용이 가능하다.
    - Hooks 기능을 사용하면 함수형 컴포넌트에서도 비슷한 작업이 가능하다.



## 라이프 사이클과 메서드

- 라이프 사이클은 총 세 가지다.
  - 마운트
  - 업데이트
  - 언마운트



- 마운트
  - DOM이 생성되고 웹 브라우저상에 나타나는 것.
  - 이 때 호출되는 메서드는 다음과 같다(순서대로 호출된다).
    - `constructor`: 컴포넌트를 새로 만들 때마다 호출되는 클래스 생성자 메서드
    - `getDerivedStateFromProps`: props에 있는 겂을 state에 넣을 때 사용하는 메서드
    - `render`: UI를 렌더링 하는 메서드
    - `componentDidMount`: 컴포넌트가 웹 브라우저상에 나타난 후 호출하는 메서드



- 업데이트
  - 컴포넌트는 다음과 같은 4가지 경우에 업데이트가 발생한다.
    - props가 바뀔 때
    - state가 바뀔 때
    - 부모 컴포넌트가 리렌더링 될 때
    - `this.forceUpdate`로 강제로 렌더링을 트리거할 때
  - 이 때 호출되는 메서드는 다음과 같다(순서대로 호출된다).
    - `getDerivedStateFromProps`: 마운트 과정에서도 호출되며, 업데이트가 시작하기 전에도 호출된다. props의 변화에 따라 state 값에도 변화를 주고 싶을 때 사용한다.
    - `shouldComponeneUpdate`: 컴포넌트가 리렌더링을 해야 할지 말지를 결정하는 메서드. 이 메서드는 boolean 값을 반환하며, true를 반환하면 다음 라이프 사이클 메서드를 계속 실행하고, false를 반환하면 작업을 중지한다.
    - `render`: 컴포넌트를 리렌더링한다. `this.forceUpdate`로 강제 업데이트하면 이전 메소드들은 거치지 않고 여기서부터 호출된다.
    - `getSnapshotBeforeUpdate`: 컴포넌트 변화를 DOM에 반영하기 바로 직전에 호출하는 메서드.
    - `componentDidUpdate`: 컴포넌트의 업데이트 작업이 끝난 후 호출하는 메서드.



- 언마운트
  - 컴포넌트를 DOM에서 제거하는 것.
  - 아래 메서드를 호출한다.
    - `componentWillUnmount`: 컴포넌트가 웹 브라우저상에 사라지게 전에 호출하는 메서드.



- 라이프 사이클 메서드 살펴보기

  - 라이프사이클 메서드는 총 9가지이다.
    - `Will`접두사가 붙은 메서드는 어떤 작업이 작동하기 전에 실행되는 메서드이다.
    - `Did` 접두사가 붙은 메서드는 어떤 작업이 작동한 후에 실행되는 메서드이다.
    - 이 메서드들은 컴포넌트 클래스에 덮어 써 선언함으로써 사용할 수 있다.

  - `render()`
    - 라이프사이클 중 유일한 필수 메서드
    - 컴포넌트의 모양새를 정의, 리액트 요소를 반환하는 메서드.
    - 반환하는 요소는 태그가 될 수도 있고 따로 선언한 컴포넌트가 될 수도 있으며 아무 것도 보여주고 싶지 않다면 null, false를 반환할 수도 있다.
    - 메서드 내부에서 `this.props`, `this.state`에 접근이 가능하다.
    - `render()` 메서드 내부에서는 이벤트 설정이 아닌 곳에서 `setState`를 사용해서는 안되며, DOM에 접근해서도 안된다.
    - DOM에 접근하거나 state에 변화를 주는 것은 `componentDidMount` 메서드 내부에서 처리해야한다.
  - `constructor`
    - 컴포넌트의 생성자 메서드로 컴포넌트를 만들 대 처음으로 실행된다.
    - state의 초깃값을 정하는 것이 가능하다.
  - `getDerivedStateFromProps`
    - 리액트 v16.3 이후에 새로 만들어진 라이프 사이클.
    - props로 받아온 값을 state에 동화시키는 용도로 사용한다.
    - 컴포넌트가 마운트될 때와 업데이트 될 때 호출된다.
  - `componentDidMount` 
    - 첫 렌더링을 다 마친 후 실행된다.
    - 이 내부에서 다른 JS 라이브러리 또는 프레임워크의 함수를 호출하거나 이벤트 등록, `setTimeout`, 네트워크 요청 같은 비동기 작업을 처리하면 된다.
  - `shouldComponeneUpdate`
    - props 또는 state를 변경하였을 때, 리렌더링을 할지 말지 여부를 boolean 값을 반환함으로써 알려주는 메서드.
    - 이 메서드를 따로 생성하지 않으면 기본적으로 true를 반환한다.
    - 이 메서드 안에서 현재 props와 state는 각기 `this.props`, `this.state`로 접근하고 새로 설정될 props 또는 state는 `nextProps`, `nextState`로 접근이 가능하다.
    - 프로젝트 성능을 최적화할 때, 리렌더링 방지를 위해서는 false값을 반환하게 한다.
  - `getSnapshotBeforeUpdate`
    - 리액트 v16.3 이후에 새로 만들어진 라이프 사이클.
    - `render`에서 만들어진 결과물이 브라우저에 실제로 반영되기 직전에 호출된다.
    - 이 메서드에서 반환하는 값은 `componentDidUpdate`의 세 번째 파라미터인 `snapshot` 값으로 전달이 가능하다.
    - 주로 업데이트 하기 직전의 값을 참고할 일이 있을 때 활용한다(e.g. 스크롤바 위치 유지를 위해 스크롤바 위치 정보를 참고).
  - `componentDidUpdate`
    - 리렌더링 완료 후 실행된다.
    - 업데이트가 끝난 직후이므로, DOM 관련 처리를 해도 무방하다.
    - `prevProps`, `prevState`를 사용하여 컴포넌트가 이전에 가졌던 데이터에 접근할 수 있다.
  - `componentWillUnmount`
    - 컴포넌트를 DOM에서 제거할 때 실행.
    - `componentDidMount`에서 등록한 이벤트, 타이머, 직접 생성한 DOM 이 있다면 여기서 제거 작업을 해야 한다.
  - `componentDidCatch`
    - 리액트 v16 이후에 새로 만들어진 라이프 사이클.
    - 컴포넌트 렌더링 도중 에러가 발생했을 때 애플리케이션이 먹통이 되지 않고 오류 UI를 보여 줄 수 있게 해준다.
    - 첫 번째 인자는 어떤 에러가 발생했는지에 대한 정보가 담고 있고, 두 번째 인자는 어디에 있는 코드에서 오류가 발생했는지에 대한 정보가 담고 있다.



## 라이프사이클 메서드 사용하기

- 주의
  - React.StrictMode가 적용되어 있으면 일부 라이프사이클이 두 번씩 호출된다.
    - 개발 환경에서만 두 번씩 호출되는 것이고 프로덕션 환경에서는 정상적으로 호출된다.
    - 만일 거슬린다면 `index.js`에서 React.StrictMode를 제거하면 된다.
  - 라이프사이클 메서드 내부의 `this`는 해당 메서드를 호출한 컴포넌트를 가리킨다.
  
  
  
- 명세
  - 각 라이프 사이클 메서드를 실행할 때마다 콘솔 디버거에 기록한다.
  - 부모 컴포넌트에서 props로 색상을 받는다.
  - 버튼을 누르면 `state.number`가 1씩 증가한다.
  - `getDerivedStateFromProps`은 부모에게 받은 color 값을 state에 동기화한다.
  - `getSnapshotBeforeUpdate`는 DOM에 변화가 일어나기 직전의 색상 속성을 snapshot 값으로 반환하여 이를 `componentDidUpdate`에서 조회할 수 있게 한다.
  - `shouldComponeneUpdate`는 `state.number` 값의 마지막 숫자가 4이면 리렌더링을 취소한다.



- 구현

  - App.js

  ```react
  import React, { Component } from "react";
  import ScrollBox from "./ScrollBox";
  import LifecycleSample from "./LifecycleSample";
  
  // state의 color 값을 랜덤 색상으로 설정.
  // 1677215는 hex로 표현하면 ffffff가 되므로 아래 코드는 000000부터 ffffff 까지의 값을 반환한다.
  function getRendomColor() {
    return "#" + Math.floor(Math.random() * 1677215).toString(16);
  }
  
  class App extends Component {
    state = {
      color: "#000000",
    };
  
    handleClick = () => {
      this.setState({
        color: getRendomColor(),
      });
    };
  
    render() {
      return (
        <div>
          <LifecycleSample color={this.state.color} />
          <button onClick={this.handleClick}>랜덤 색상</button>
        </div>
      );
    }
  }
  
  export default App;
  ```
  
  - LifecycleSample.js
  
  ```react
  import React, { Component } from "react";
  
  class LifecycleSample extends Component {
      state = {
          number: 0,
          color: null,
      };
  myRef = null;
  
  constructor(props) {
      super(props);
      console.log("constructor");
  }
  
  static getDerivedStateFromProps(nextProps, prevState) {
      console.log("getDerivedStateFromProps");
      if (nextProps.color !== prevState.color) {
          return { color: nextProps.color };
      }
      return null;
  }
  
  componentDidMount() {
      console.log("componentDidMount");
  }
  
  shouldComponentUpdate(nextProps, nextState) {
      console.log("shouldComponentUpdate");
      return nextState.number % 10 !== 4;
  }
  
  componentWillUnmount() {
      console.log("componentWillUnmount");
  }
  
  handleClick = () => {
      this.setState({
          number: this.state.number + 1,
      });
  };
  
  getSnapshotBeforeUpdate(prevProps, prevStte) {
      console.log("getSnapshotBeforeUpdate");
      if (prevProps.color !== this.prevState.color) {
          return this.myRef.style.color;
      }
      return null;
  }
  
  componentDidUpdate(prevProps, prevState, snapshot) {
      console.log("componentDidUpdate", prevProps, prevState);
      if (snapshot) {
          console.log("업데이트 되기 직전 생상:", snapshot);
      }
  }
  
  render() {
      console.log("render");
      const style = {
          color: this.props.color,
      };
      return (
          <div>
              <h1 style={style} ref={(ref) => (this.myRef = ref)}>
                  {this.state.number}
              </h1>
              <p>color: {this.state.color}</p>
              <button onClick={this.handleClick}>더하기</button>
          </div>
      );
  }
  }
  
  export default LifecycleSample;
  ```



- 에러 잡기

  - `render`에서 의도적으로 에러를 발생시칸다.

  ```react
  render() {
      console.log("render");
      const style = {
          color: this.props.color,
      };
      return (
          <div>
              {/* 존재하지 않는 값을 조회 */}
              {this.props.nothing.value}
              <h1 style={style} ref={(ref) => (this.myRef = ref)}>
                  {this.state.number}
              </h1>
              <p>color: {this.state.color}</p>
              <button onClick={this.handleClick}>더하기</button>
          </div>
      );
  }
  ```

  - 에러 페이지 우측 상단의 X 버튼을 누르면 에러 페이지가 사라진다.
      - 흰 화면이 나오게 된다(배포 환경에서 에러가 발생하면 보이는 화면이다).
      - 사용자 입장에서 에러가 발생했을 때 흰색 화면이 나오게 된다면 당황할 것이다.
    - 따라서 사용자에게 에러가 발생했다는 것을 인지시켜 줘야 한다.
  - `componentDidCatch`메서드 활용
      - 이 메서드는 에러가 발생하면 호출된다.

  ```react
  import React, { Component } from "react";
    
    class ErrorBoundary extends Component {
      state = {
        error: false,
      };
      componentDidCatch(error, info) {
        this.setState({
          error: true,
        });
        console.log({ error, info });
      }
      render() {
        // 에러가 발생하면 <div>에러가 발생했습니다.</div>를 반환.
        if (this.state.error) return <div>에러가 발생했습니다.</div>;
        // 에러가 발생하지 않으면 본래 보여주려던 것을 반환.
        return this.props.children;
      }
    }
    
    export default ErrorBoundary;
  ```

    - App.js 를 아래와 같이 수정
        - `children`은 태그 사이의 내용을 보여주므로 아래와 같이 `<ErrorBoundary>` 태그 사이에 원래 보여주려는 내용을 넣는다.
        - 이제 에러 페이지에서 X 버튼을 누르면 에러가 발생한 부분만 `ErrorBoundary.js`에서 설정한 내용이 출력된다.

  ```react
  import React, { Component } from "react";
  import ScrollBox from "./ScrollBox";
  import LifecycleSample from "./LifecycleSample";
  import ErrorBoundary from "./ErrorBoundary";
  
  //state의 color 값을 랜덤 색상으로 설정.
  //1677215는 hex로 표현하면 ffffff가 되므로 아래 코드는 000000부터 ffffff 까지의 값을 반환한다.
  function getRendomColor() {
      return "#" + Math.floor(Math.random() * 1677215).toString(16);
  }
  
  class App extends Component {
      state = {
          color: "#000000",
      };
  
  handleClick = () => {
      this.setState({
          color: getRendomColor(),
      });
  };
  
  render() {
      return (
          <div>
              {/* 불러온 뒤 태그로 에러가 발생할 부분을 깜싸준다. */}
              <ErrorBoundary>
                  <LifecycleSample color={this.state.color} />
              </ErrorBoundary>
              <button onClick={this.handleClick}>랜덤 색상</button>
          </div>
      );
  }
  }
  
  export default App;
  ```





# Hooks

- Hooks
  - v16.8에서 새롭게 도입된 기능
  - 함수형 컴포넌트에서도 상태 관리를 할 수 있는 `useState`, 렌더링 직후 작업을 설정하는 `useEffect`등의 기능을 제공하여 기존의 함수형 컴포넌트에서 할 수 없었던 다양한 작업을 할 수 있게 해준다.



## useState

- 지금까지 사용해봤으므로 생략한다.



## useEffect

- 리액트 컴포넌트가 렌더링될 때마다 특정 작업을 수행하도록 설정할 수 있는 Hook.

  - 클래스형 컴포넌트의 `componentDidMount`, `componentDidUpdate`를 합친 형태로 보아도 무방하다.
  - 아래 코드를 작성하고 콘솔 창을 확인해보면 마운트 될 때와 업데이트 될 때 모두 실행되는 것을 확인 가능하다.

  ```react
  import React, { useState, useEffect } from "react";
  
  const Info = () => {
    const [name, setName] = useState("");
    const [nickname, setNickname] = useState("");
  
    useEffect(() => {
      console.log("렌더링이 완료되었습니다!");
      console.log({
        name,
        nickname,
      });
    });
  
    const onChangeName = (e) => {
      setName(e.target.value);
    };
    const onChangeNickname = (e) => {
      setNickname(e.target.value);
    };
    return (
      <div>
        <div>
          <input value={name} onChange={onChangeName} />
          <input value={nickname} onChange={onChangeNickname} />
        </div>
        <div>
          <div>
            <b>이름: </b> {name}
          </div>
          <div>
            <b>닉네임: </b> {nickname}
          </div>
        </div>
      </div>
    );
  };
  
  export default Info;
  ```



- 마운트될 때만 실행하고 싶을 때

  - 컴포넌트가 화면에 맨 처음 렌더링 될 때만 실행하고, 업데이트 할 때는 실행하지 않으려면, 즉 `componentDidMount`만 실행하려면
  - 함수의 두 번째 파라미터로 비어 있는 배열을 넣어주면 된다.
    - 함수 내부에서 상태 값에 의존해야 할 때는 그 값을 반드시 두 번째 인자에 포함시켜야 한다.
    - 아래의 경우 `name`, `nickname`을 `useEffect` 내부에서 사용하고 있어 콘솔 창을 열어보면 경고 메세지가 출력되지만 정상동작한다.
    - `name`, `nickname`을 `useEffect` 내부에서 사용하지 않도록 변경하면 경고 메세지도 사라진다.

  ```react
  import React, { useState, useEffect } from "react";
  
  const Info = () => {
    const [name, setName] = useState("");
    const [nickname, setNickname] = useState("");
  
    useEffect(() => {
      console.log("렌더링이 완료되었습니다!");
      console.log("마운트 될 때만 실행 됩니다.");
      console.log({
        name,
        nickname,
      },[]); // 빈 배열을 넣어준다.
    });
  
    (...)
    return (...)
  };
  
  export default Info;
  ```



- 특정 값이 업데이트 될 때만 실행하고 싶을 때

  - `componentDidUpdate`만 실행하려면
  - 함수의 두 번째 파라미터로 빈 배열이 아닌 검사하고 싶은 값을 넣어주면 된다. 
  - 배열 안에는 state뿐만 아니라 props로 전달 받은 값을 넣어도 된다.
  - 아래의 경우 배열에 `name`만 넣었기에 `name`이 변경될 때만 실행된다.
    - `nickname`을 `useEffect` 내부에서 사용하고 있어 콘솔 창을 열어보면 경고 메세지가 출력되지만 정상동작한다.
    - `nickname`을 `useEffect` 내부에서 사용하지 않도록 변경하면 경고 메세지도 사라진다.

  ```react
  import React, { useState, useEffect } from "react";
  
  const Info = () => {
    const [name, setName] = useState("");
    const [nickname, setNickname] = useState("");
  
    useEffect(() => {
      console.log("name이 업데이트 될 때만 실행됩니다.");
      console.log({
        name,
        nickname,
      });
    }, [name]);
  
    (...)
    return (...);
  };
  
  export default Info;
  ```



- 뒷정리 하기

  - 컴포넌트가 언마운트 되기 전이나 업데이트 되기 직전에 어떤 작업을 수행하고 싶다면, 뒷정리(cleanup) 함수를 반환하면 된다.
    - 언마운트 될 때만 뒷정리 함수를 호출하고 싶다면 `useEffect` 함수의 두 번째 인자로 빈 배열을 넣으면 된다.
  - `Info.js`
    - 아래 코드를 작성 후 브라우저에서 보이기를 누르면 effect가 출력되고 숨기기(언마운트)를 누르면 cleanup이 출력되는 것을 확인 가능하다.
    - 또한 input 창에 name을 넣을 때에도 name이 변경되기 전에 cleanup이 실행되는 것을 확인 가능하다.

  ```react
  import React, { useState, useEffect } from "react";
  
  const Info = () => {
    const [name, setName] = useState("");
    const [nickname, setNickname] = useState("");
  
    useEffect(() => {
      console.log("effect");
      console.log(name);
      return () => {
        console.log("cleanup");
        console.log(name);
      };
    }, [name]);
  
    (...)
    return (...);
  };
  
  export default Info;
  ```

  - `App.js`

  ```react
  import React, { useState } from "react";
  import Info from "./Info";
  
  const App = () => {
    const [visible, setVisible] = useState(false);
    return (
      <div>
        <button
          onClick={() => {
            setVisible(!visible);
          }}
        >
          {visible ? "숨기기" : "보이기"}
        </button>
        <hr />
        {visible && <Info />}
      </div>
    );
  };
  
  export default App;
  ```



## useReducer

- `useState`보다 더 다양한 컴포넌트 상황에 따라 다양한 상태를 다른 값으로 업데이트 하고자 할 때 사용하는 Hook
  - 리듀서라는 개념은 리덕스와 관련되어 있으므로 리덕스를 공부할 때 더 자세히 알아본다.
  - 현재 상태(state)와 업데이트를 위해 필요한 정보를 담은 액션 값(action)을 전달받아 새로운 상태를 반환하는 함수이다.
    - 리덕스에서 사용하는 액션 객체는 어떤 액션인지 알려주는 type 필드가 꼭 있어야 하지만, `useReducer`에서 사용하는 액션 객체는 type을 지니지 않아도 된다.
  - 새로운 상태를 만들 때는 반드시 불변성을 지켜줘야 한다.



- `useReducer` 메소드
  - 첫 번째 인자는 리듀서 함수를, 두 번째 인자는 해당 리듀서의 기본 값을 받는다.
  - 이 Hook을 사용하면 state 값과 dispatch 함수를 받아오게 된다.
  - state는 현재 가리키고 있는 상태를 의미한다.
  - dispatch는 액션을 발생시키는 함수이다.



- `useReducer`의 가장 큰 장점은 컴포넌트 업데이트 로직을 컴포넌트 바깥으로 빼낼 수 있다는 것이다.

  - 아래 코드와 같이 컴포넌트 업데이트 로직(리듀서 함수)를 컴포넌트 바깥으로 빼낼 수 있다.

  ```react
  import React, { useReducer } from "react";
  
  // 리듀서 함수
  // 컴포넌트 업데이트 로직을 컴포넌트 바깥으로 빼내었다.
  function reducer(state, action) {
    switch (action.type) {
      case "INCREMENT":
        // state를 반환한다.
        return { value: state.value + 1 };
      case "DECREMENT":
        return { value: state.value - 1 };
      case "RESET":
        return { value: 0 };
      default:
        return state;
    }
  }
  
  const Counter = () => {
    const [state, dispatch] = useReducer(reducer, { value: 0 });
    return (
      <div>
        <p>
          현재 카운터 값은 <b>{state.value}</b>입니다.
        </p>
        <button onClick={() => dispatch({ type: "INCREMENT" })}>+1</button>
        <button onClick={() => dispatch({ type: "DECREMENT" })}>-1</button>
        <button onClick={() => dispatch({ type: "RESET" })}>초기화</button>
      </div>
    );
  };
  
  export default Counter;
  ```
  
  - 위 코드를 `useState`를 사용하면 아래와 같이 구현 할 수 있다.
  
  ```react
  import React, { useState } from "react";
  
  const CounterUseState = () => {
      const [value, setValue] = useState(0);
      return (
          <div>
              <p>
                  현재 카운터 값은 <b>{value}</b>입니다.
              </p>
              <button onClick={() => setValue(value + 1)}>+1</button>
              <button onClick={() => setValue(value - 1)}>-1</button>
              <button onClick={() => setValue(0)}>초기화</button>
          </div>
      );
  };
  
  export default CounterUseState;
  ```





- 복수의 상태 관리하기

  - `useState`를 사용할 때는 관리해야 할 상태가 여러 개면 `useState`를 여러개 사용 했다.
  - `useReducer`를 사용하면 보다 깔끔하게 처리가 가능하다.
    - `useEffect`의 예시로 사용한 `Info.js`에서는 `useState`를 사용하여 복수의 상태를 관리하였다.
    - `useReducer`를 사용하면 아래와 같이 보다 깔끔해진다.
  - redux와는 달리 `useReducer`는 꼭 type을 갖지 않아도 된다.
  
  ```react
  import React, { useReducer } from "react";
  
  function reducer(state, action) {
    // spread 문법을 사용하여 복사한 객체
    return {
      ...state,
      [action.name]: action.value,
    };
  }
  
  const Info = () => {
    const [state, dispatch] = useReducer(reducer, {
      name: "",
      nickname: "",
    });
    const { name, nickname } = state;
    const onChange = (e) => {
      dispatch(e.target);
    };
    return (
      <div>
        <div>
          <input name="name" value={name} onChange={onChange} />
          <input name="nickname" value={nickname} onChange={onChange} />
        </div>
        <div>
          <div>
            <b>이름: </b> {name}
          </div>
          <div>
            <b>닉네임: </b> {nickname}
          </div>
        </div>
      </div>
    );
  };
  
  export default Info;
  ```
  - `useReducer`의 액션은 어떤 값이든 사용이 가능하다.
    - 위 예시에서는 이벤트 객체가 지니고  있는 `e.target` 값 자체를 액션 값으로 사용했다.





## useMemo

- 함수형 컴포넌트 내부에서 발생하는 연산을 최적화하는데 사용한다.
  - 렌더링 하는 과정에서 특정 값이 바뀌었을 때만 연산을 실행한다.
  - 값이 바뀌지 않았다면 이전에 연산한 결과를 다시 사용한다.



- `useMemo` 사용

  - 첫 번째 인자로 실행할 동작을 받고, 두 번째 인자로 변화를 감지할 상태를 배열 형태로 받는다.
  - `useMemo`를 사용하지 않았을 때
    - 아래 코드를 실행해보면 숫자를 등록할 때뿐만 아니라 인풋 내용이 수정될 때도 `getAverage` 함수가 호출되는 것을 확인 가능하다.
    - 인풋 내용이 바뀔 때는 평균값을 계산할 필요가 없으므로 이는 낭비다.

  ```react
  import React, { useState } from "react";
  
  const getAverage = (numArr) => {
      console.log("평균값 계산");
      if (numArr.length === 0) return 0;
      const sum = numArr.reduce((a, b) => a + b);
      return sum / numArr.length;
  };
  
  const Average = () => {
      const [list, setList] = useState([]);
      const [number, setNumber] = useState("");
  
      const onChange = (e) => {
          setNumber(e.target.value);
      };
  
      const onInsert = (e) => {
          const nextList = list.concat(parseInt(number));
          setList(nextList);
          setNumber("");
      };
      return (
          <div>
              <input value={number} onChange={onChange} />
              <button onClick={onInsert}>등록</button>
              <ul>
                  {list.map((v, i) => {
                      <li key={i}>{v}</li>;
                  })}
              </ul>
              <div>
                  <b>평균값</b> {getAverage(list)}
              </div>
          </div>
      );
  };
  
  export default Average;
  ```

    - `useMemo`를 사용했을 때
      - `list`가 변화하면 `getAverage`함수를 실행한다.

  ```react
  import React, { useState, useMemo } from "react";
  
  const getAverage = (numArr) => {
      console.log("평균값 계산");
      if (numArr.length === 0) return 0;
      const sum = numArr.reduce((a, b) => a + b);
      return sum / numArr.length;
  };
  
  const Average = () => {
      const [list, setList] = useState([]);
      const [number, setNumber] = useState("");
  
      const onChange = (e) => {
          setNumber(e.target.value);
      };
  
      const onInsert = (e) => {
          const nextList = list.concat(parseInt(number));
          setList(nextList);
          setNumber("");
      };
  
      // useMemo를 사용한다.
      const avg = useMemo(() => getAverage(list), [list]);
  
      return (
          <div>
              <input value={number} onChange={onChange} />
              <button onClick={onInsert}>등록</button>
              <ul>
                  {list.map((v, i) => {
                      <li key={i}>{v}</li>;
                  })}
              </ul>
              <div>
                  <b>평균값</b> {avg}
              </div>
          </div>
      );
  };
  
  export default Average;
  ```





## useCallback

- 렌더링 성능을 최적화해야 하는 경우 사용.
  - 만들어 놨던 함수를 재사용 하는 것이 가능하다.
  - `useMemo` 예시에서 사용한 `onChange`, `onInsert`라는 함수들은 컴포넌트가 리렌더링 될 때마다 새로 만들어지게 된다.
  - 대부분의 경우 특별히 문제가 되지 않지만 컴포넌트의 렌더링이 자주 발생하거나 렌더링해야 할 컴포넌트의 개수가 많아지면 최적화 해주는 것이 좋다.
  - props로 전달해야 할 함수를 만들 때는 `useCallback`을 사용하여 함수를 감싸는 것을 습관화 하는 것이 좋다.



- `useCallBack` 사용

  - 첫 번째 인자로 생성하고 싶은 함수를 받고, 두 번째 인자로 변화를 감지할 상태를 배열 형태로 받는다.
    - 비어 있는 배열을 두 번째 인자로 받을 경우 컴포넌트가 렌더링 될 때 만들었던 함수를 계속해서 재사용한다.
    - 상태가 담긴 배열을 받으면 해당 상태가 변경될 때 새로 만들어진 함수를 사용한다.
  - 함수 내부에서 상태 값에 의존해야 할 때는 그 값을 반드시 두 번째 인자에 포함시켜야 한다.
    - 예를 들어 `onChange`는 내부에서 상태 값을 하나도 사용하지 않아 상관 없다.
    - 그러나 `onInsert`는 내부에서 `list`, `number`라는 상태값을 사용하므로 두 번째 인자인 배열에 반드시 포함시켜야 한다.

  ```react
  import React, { useState, useMemo,useCallback } from "react";
  
  const getAverage = (numArr) => {
    console.log("평균값 계산중..");
    if (numArr.length === 0) return 0;
    const sum = numArr.reduce((a, b) => a + b);
    return sum / numArr.length;
  };
  
  const Average = () => {
    const [list, setList] = useState([]);
    const [number, setNumber] = useState("");
  
    // 첫 번째 인자로 함수를 받고, 두 번째 인자로 변화를 감지할 상태를 배열로 받는다.
    const onChange = useCallback((e) => {
      setNumber(e.target.value);
    }, []); // 컴포넌트가 처음 렌더링 될 때만 함수 생성
    
    const onInsert = useCallback(() => {
      const nextList = list.concat(parseInt(number));
      setList(nextList);
      setNumber("");
    }, [number, list]); // number 혹은 list 가 바뀌었을 때만 함수 생성
  
    const avg = useMemo(() => getAverage(list), [list]);
  
    return (...);
  };
  
  export default Average;
  ```



## useRef

- 함수형 컴포넌트에서 ref을 보다 쉽게 사용할 수 있도록 해준다.

  - `useRef`를 사용하여 ref를 설정하면 useRef를 통해 만든 객체 안의 current 값이 실제 엘리먼트를 가리킨다.
  - 아래 코드를 실행하면 등록 버튼을 눌렀을 때 포커스가 인풋 쪽으로 넘어가게 된다.

  ```react
  import React, { useState, useMemo, useRef, useCallback } from "react";
  
  const getAverage = (numArr) => {
    console.log("평균값 계산중..");
    if (numArr.length === 0) return 0;
    const sum = numArr.reduce((a, b) => a + b);
    return sum / numArr.length;
  };
  
  const Average = () => {
    const [list, setList] = useState([]);
    const [number, setNumber] = useState("");
    // useRef를 사용한다.
    const inputEl = useRef(null);
      
    const onChange = useCallback((e) => {
      setNumber(e.target.value);
    }, []);
      
    const onInsert = useCallback(() => {
      const nextList = list.concat(parseInt(number));
      setList(nextList);
      setNumber("");
      // inputEl.current는 input을 가리킨다.
      inputEl.current.focus();
    }, [number, list]);
  
    (...)
  
    return (
      <div>
        <input value={number} onChange={onChange} ref={inputEl} />
        (...)
      </div>
    );
  };
  
  export default Average;
  ```



- 로컬 변수 사용하기

  - 컴포넌트 로컬 변수를 사용해야 할 때도 `useRef`를 사용 가능하다.
    - 로컬 변수란 렌더링과 상관없이 바뀔 수 있는 값을 의미한다.
    - 즉, 굳이 setter, setState 등으로 변경하지 않아도 되는 값을 의미한다.
  - 클래스 형태로 작성된 컴포넌트의 경우 로컬 변수를 사용해야 할 때 아래와 같이 작성한다.
  
  ```react
  import React, { Component } from "react";
  
  class LocalValueClass extends Component {
    id = 1;
    setId = (n) => {
      this.id = n;
    };
    printId = () => {
      console.log(this.id);
    };
    render() {
      return <div></div>;
    }
  }
  
  export default LocalValueClass;
  ```
  
  - 함수형 컴포넌트에서는 아래와 같이 작성한다.
  
  ```react
  import React, { useRef } from "react";
  
  const RefSample = () => {
      const id = useRef(1);
      const setId = (n) => {
          id.current = n;
      };
      const printId = () => {
          console.log(id.current);
      };
      return <div></div>;
  };
  
  export default RefSample;
  ```





## Hook을 따로 분리하기

- 여러 컴포넌트에서 비슷한 기능을 공유할 경우, Hook을 분리하여 로직을 재사용할 수 있다.

  - `Info.js`에서 사용했던 `useReducer` Hook을 별도의 js파일에 따로 분리

  ```js
  // useInputs.js
  import { useReducer } from "react";
  
  function reducer(state, action) {
    return {
      ...state,
      [action.name]: action.value,
    };
  }
  
  export default function useInputs(initialForm) {
    const [state, dispatch] = useReducer(reducer, initialForm);
    const onChange = (e) => {
      dispatch(e.target);
    };
    // 상태와 onChange 함수를 반환
    return [state, onChange];
  }
  ```
  
  - 위에서 분리한 Hook을 사용
  
  ```react
  import React from "react";
  import useInputs from "./useInput";
  
  const Info = () => {
      const [state, onChange] = useInputs({
          name: "",
          nickname: "",
      });
      const { name, nickname } = state;
  
      return (
          <div>
              <div>
                  <input name="name" value={name} onChange={onChange} />
                  <input name="nickname" value={nickname} onChange={onChange} />
              </div>
              <div>
                  <div>
                      <b>이름: </b> {name}
                  </div>
                  <div>
                      <b>닉네임: </b> {nickname}
                  </div>
              </div>
          </div>
      );
  };
  
  export default Info;
  ```





- 다른 개발자가 만든 Hooks도 라이브러리로 설치하여 사용이 가능하다.

  > https://nikgraf.github.io/react-hooks/
  >
  > https://github.com/rehooks/awesome-react-hooks



