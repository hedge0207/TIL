# Redux 활용하기

- 리액트 프로젝트에서 리덕스 활용하기

  - Redux, react-redux 설치하기
    - 바닐라 JS에서 사용할 때와는 다르게 `store`의 내장함수인 `dispatch`와 `subscribe`대신 react-redux 라이브러리에서 제공하는 유틸 함수 `connect`와 컴포넌트 `Provider`를 사용하여 리덕스 관련 작업을 처리한다.

  ```bash
  $ yarn add redux react-redux
  ```

  - 리액트 프로젝트에서 리덕스를 사용할 때 가장 많이 사용하는 패턴은 프레젠테이셔널 컴포넌트와 컨테이너 컴포넌트를 분리하는 것이다.
    - **프레젠테이셔널 컴포넌트**: 상태 관리가 이루어지지 않고, 그저 props를 받아 와서 화면에 UI를 보여 주기만 하는 컴포넌트.
    - **컨테이너 컴포넌트**: 리덕스와 연동되어 있는 컴포넌트로, 리덕스로부터 상태를 받아 오기도 하고, 리덕스 스토어에 액션을 디스패치 하기도 하는 컴포넌트.
    - 이러한 패턴이 필수사항은 아니지만, 이 패턴을 사용하면 코드의 재사용성도 높아지고, 관심사의 분리가 이루어져 UI를 작성할 때 좀 더 집중할 수 있게 된다.



- 리덕스를 활용 할 컴포넌트 만들기

  - 프레젠테이셔널 컴포넌트는 components 폴더에, 컨테이너 컴포넌트는 containers 폴더에 저장한다.
  - 숫자를 더하고 뺄 수 있는 Counter컴포넌트 만들기

  ```react
  import React from "react";
  
  const Counter = ({ number, onIncrease, onDecease }) => {
    return (
      <div>
        <h1>{number}</h1>
        <div>
          <button onClick={onIncrease}>+1</button>
          <button onClick={onDecrease}>-1</button>
        </div>
      </div>
    );
  };
  
  export default Counter;
  ```

  - 할 일 목록 컴포넌트 만들기
    - 파일 하나에 TodoItem과 Todos라는 두 개의 컴포넌트를 선언했다.
    - 분리해서 선언해도 무관하다.

  ```react
  import React from "react";
  
  const TodoItem = ({ todo, onToggle, onRemove }) => {
    return (
      <div>
        <input type="checkbox" />
        <span>예제 테스트</span>
        <button>삭제</button>
      </div>
    );
  };
  
  const Todos = ({
    input,
    todos,
    onChangeInput,
    onInsert,
    onToggle,
    onRemove,
  }) => {
    const onSubmit = (e) => {
      e.preventDefault();
    };
    return (
      <div>
        <form onSubmit={onSubmit}>
          <input />
          <button type="submit">등록</button>
        </form>
        <div>
          <TodoItem />
          <TodoItem />
          <TodoItem />
          <TodoItem />
          <TodoItem />
        </div>
      </div>
    );
  };
  
  export default Todos;
  ```



## 리덕스 관련 코드 작성하기

- 리덕스를 사용할 때는 액션 타입, 액션 생성 함수, 리듀서 코드를 작성해야 한다. 이 코드들을 각자 다른 파일에 작성하는 방법도 있고, 기능별로 묶어서 파일 하나에 작성하는 방법도 있다.
  - 일반적인 구조
    - actions, constants, reducers라는 세 개의 디렉터리를 만들고 그 안에 기능별로 파일을 하나씩 만드는 방식. 
    - 새로운 액션을 만들 때마다 세 파일을 모두 수정해야 한다는 점 때문에 불편하지만, 정리하기는 편하다는 장점이 있다. 
    - 리덕스 공식문서에서 사용하는 방법이다.
  - Ducks 패턴
    - 액션 타입, 액션 생성 함수, 리듀서 함수를 기능별로 파일 하나에 몰아서 다 작성하는 방식이다. 
    - Ducks 패턴을 사용하여 액션 타입, 액션 생성 함수, 리듀서를 작성한 코드를 **모듈**이라 한다.
    - 아래 예시에서 사용할 방식이다. 



- Counter 모듈 작성하기

  - 최상위 디렉토리에 modules 디렉터리를 만들고, 그 내부에 counter.js 파일을 작성한다.
  - 액션 타입 정의하기
    - 액션 타입은 대문자로 정의하고, 문자열 내용은 `모듈이름/액션 이름`의 형태로 작성한다(이를 통해 액션 이름 충돌을 방지한다).

  ```javascript
  const INCREASE = "counter/INCREASE";
  const DECREASE = "counter/DECREASE";
  ```

  - 액션 생성 함수 만들기
    - `export`키워드를 사용하여 추후 액션 생성 함수를 다른 파일에서 불러올 수 있도록 한다.

  ```javascript
  export const increase = () => ({ type: INCREASE });
  export const decrease = () => ({ type: DECREASE });
  ```

  - 초기 상태 및 리듀서 함수 만들기
    - `export default` 키워드로 리듀서 함수를 내보내 준다.
    - `export`는 여러 개를 내보낼 수 있지만 `export default`는 단 한 개만 내보낼 수 있다는 차이가 있다. 또한 불러 올 때도 `export`는 `{}`로 묶어서 불러와야 하지만(`import {increase}`), `export default`는 그냥 불러올 수 있다(`import counter`).

  ```javascript
  // 초기 상태 생성
  const initialState = {
    number: 0,
  };
  
  // 리듀서 생성
  function counter(state = initialState, action) {
    switch (action.type) {
      case INCREASE:
        return {
          number: state.number + 1,
        };
      case DECREASE:
        return {
          number: state.number - 1,
        };
      default:
        return state;
    }
  }
  
  export default counter;
  ```



- todos 모듈 만들기

  - modules 디렉터리에 todos.js 파일을 작성한다.
  - 액션 타입 정의하기

  ```javascript
  const CHANGE_INPUT = "todos/CHANGE_INPUT";  // input 값을 변경
  const INSERT = "todos/INSERT";              // 새로운 todo를 등록
  const TOGGLE = "todos/TOGGLE";              // todo를 체크/체크 해제
  const REMOVE = "todos/REMOVE";              // todo를 제거
  ```

  - 액션 생성 함수 만들기
    - `insert` 함수는 인자로 받은 `text`외에 미리 선언한 `id`라는 값에도 의존한다.
    - `id`를 3으로 설정한 이유는, 초기 상태를 작성할 때 todo 객체 두 개를 사전에 미리 넣어둘 것이기 때문이다.

  ```javascript
  export const changeInput = (input) => ({
    type: CHANGE_INPUT,
    input,
  });
  
  let id = 3;  // insert가 호출될 때마다 1씩 더해진다.
  export const insert = (text) => ({
    type: INSERT,
    todo: {
      id: id++,
      text,
      done: false,
    },
  });
  
  export const toggle = (id) => ({
    type: TOGGLE,
    id,
  });
  
  export const remove = (id) => ({
    type: REMOVE,
    id,
  });
  ```

  - 초기 상태 및 리듀서 함수 만들기
    - 리듀서 함수를 만들 때는 상태의 불변성을 유지해 줘야 한다.

  ```javascript
  // 초기 상태 생성
  const initialState = {
    input: "",
    todos: [
      {
        id: 1,
        text: "리덕스 기초 배우기",
        done: true,
      },
      {
        id: 2,
        text: "리액트와 리덕스 사용하기",
        done: false,
      },
    ],
  };
  
  // 리듀서 함수 작성
  function todos(state = initialState, action) {
    switch (action.type) {
      case CHANGE_INPUT:
        return {
          ...state,
          input: action.input,
        };
      case INSERT:
        return {
          ...state,
          todos: state.todos.concat(action.todo),
        };
      case TOGGLE:
        return {
          ...state,
          // todos를 돌면서 변경할 id와 todos 배열 내부의 todo 객체의 id가 맞으면 해당 todo 객체의 done을 변경, 아니면 그냥 todo 객체를 반환.
          todos: state.todos.map((todo) =>
            todo.id === action.id ? { ...todo, done: !todo.done } : todo
          ),
        };
      case REMOVE:
        return {
          ...state,
          // todos를 돌면서 삭제할 id와 todos 배열 내부의 todo 객체의 id가 맞으면 거르고 아니면 포함시킨다.
          todos: state.todos.filter((todo) => todo.id !== action.id),
        };
      default:
        return state;
    }
  }
  
  export default todos;
  ```



- 루트 리듀서 만들기

  - 스토어를 만들 때는 리듀서를 하나만 사용해야 한다.
    - 따라서 기존에 만들었던 리듀서들을 하나로 합쳐 주어야 한다.
    - 리덕스에서 제공하는 `combineReducers` 함수로 쉽게 처리 가능하다.
  - modules 디렉터리에 index.js 파일을 생성

  ```javascript
  import { combineReducers } from "redux";
  import counter from "./counter";
  import todos from "./todos";
  
  const rootReducer = combineReducers({ counter, todos });
  
  export default rootReducer;
  ```



## 리액트 애플리케이션에 리덕스 적용하기

- Redux DevTools의 설치 및 적용

  - 아래 사이트에서 설치한다.

  > https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=ko

  - 적용 방법1. 리덕스 스토어를 만들 때 인자로 아래와 같이 넣어준다.

  ```react
  (...)
  import rootReducer from "./modules";
  import { createStore } from "redux";
  
  const store = createStore(
    rootReducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  );
  
  (...)
  ```

  - 적용 방법2. 패키지를 설치하여 적용한다.

  ```bash
  $ yarn add redux-devtools-extension
  ```

  - 패키지 설치 후 아래와 같이 적용한다.

  ```react
  (...)
  import rootReducer from "./modules";
  import { createStore } from "redux";
  import { composeWithDevTools } from "redux-devtools-extension";
  
  const store = createStore(rootReducer, composeWithDevTools());
  
  ReactDOM.render(
    <React.StrictMode>
      <Provider store={store}>
        <App />
      </Provider>
    </React.StrictMode>,
    document.getElementById("root")
  );
  
  reportWebVitals();
  ```

  - 적용이 완료되었으면 애플리케이션 실행 후 개발자 도구의 redux 탭에서 현재 state가 잘 보이는지 확인



- 스토어 만들기

  - src 디렉토리의 index.js에 스토어를 생성한다.

  ```react
  import React from "react";
  import ReactDOM from "react-dom";
  import "./index.css";
  import App from "./App";
  import reportWebVitals from "./reportWebVitals";
  import rootReducer from "./modules";
  import { createStore } from "redux";
  
  const store = createStore(rootReducer);
  
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById("root")
  );
  
  reportWebVitals();
  ```



- 리액트 컴포넌트에서 스토어를 사용할 준비하기

  - `Provider` 컴포넌트로 App 컴포넌트를 감싼다.
    - 이 컴포넌트를 사용할 때는 store를 props로 전달해 줘야 한다.

  ```react
  (...)
  import { Provider } from "react-redux";
  
  const store = createStore(rootReducer);
  
  ReactDOM.render(
    <React.StrictMode>
      <Provider store={store}>
        <App />
      </Provider>
    </React.StrictMode>,
    document.getElementById("root")
  );
  
  reportWebVitals();
  ```



## 컨테이너 컴포넌트 만들기

- CounterContainer 만들기

  - src/containers 디렉터리를 생성하고 그 내부에 CounterContainer 컴포넌트를 만든다.

  ```react
  import React from "react";
  import Counter from "../components/Counter";
  
  const CounterContainer = () => {
    return <Counter />;
  };
  
  export default CounterContainer;
  ```
  - 리덕스와 연결하기 위해 react-redux에서 제공하는 `connect` 함수를 사용한다.
    - 첫 번째 인자로 리덕스 스토어 안의 상태를 현재 컴포넌트의 props로 넘겨주기 위한 함수를 받는다.
    - 첫 번째 인자로 받는 함수는 store의 상태를 가리키는 state를 파라미터로 받는다.
    - 두 번째 인자로 액션 생성 함수를 현재 컴포넌트의 props로 넘겨주기 위한 함수를 받는다.
    - 두 번째 인자로 받는 함수는 store의 내장 함수 dispatch를 파라미터로 받는다.
    - 첫 번째 인자와 두 번째 인자가 반환하는 객체 내부의 값들은 컴포넌트의 props로 전달된다.
    - `connet`함수는 또 다른 함수를 반환하는데, `connect`가 반환한 함수에 컴포넌트를 파리미터로 넣어 주면 리덕스와 연동된 컴포넌트가 만들어진다.

  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Counter from "../components/Counter";
  
  const CounterContainer = () => {
    return (
      <Counter/>
    );
  };
  
  const mapStateToProps = (state) => ({
    // counter는 모듈이름이다. store에 저장된 상태중 counter의 number에 접근하겠다는 뜻이다.
    number: state.counter.number,
  });
  
  const mapDispatchToProps = (dispatch) => ({
    // 테스트를 위한 임시 함수
    increase: () => {
      console.log("increase");
    },
    decrease: () => {
      console.log("decrease");
    },
  });
  export default connect(mapStateToProps, mapDispatchToProps)(CounterContainer);
  /* 아래 함수와 같은 원리
  function foo() {
    const bar = function (m) {
      console.log(m);
    };
    return bar;
  }
  foo()("hello!");
  */
  ```
  
  - 아래와 같이 `connect()`함수에 익명함수로 넘겨도 된다.
  
  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Counter from "../components/Counter";
  
  const CounterContainer = () => {
      return (
          <Counter />
      );
  };
  
  export default connect(
      (state) => ({ number: state.counter.number }),
      (dispatch) => ({
          increase: () => console.log("increase"),
          decrease: () => console.log("decrease"),
      })
  )(CounterContainer);
  ```
  
    - App 컴포넌트에서 Counter를 CounterContainer로 교체한다.
      - CounterContainer 컴포넌트는 결국 Counter 컴포넌트를 반환한다.
  
  ```react
  import React from "react";
  import CounterContainer from "./containers/CounterContainer";
  import Todos from "./components/Todo";
  
  const App = () => {
      return (
          <div>
              <CounterContainer number={0} />
              <hr />
              <Todos />
          </div>
      );
  };
  
  export default App;
  ```
  
    - 액션 생성 함수를 불러와서 액션 객체를 만들고 디스패치 하기
  
  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Counter from "../components/Counter";
  // 액션 생성 함수를 불러온다.
  import { increase, decrease } from "../modules/counter";
  
  // 코드 맨 아래에서 connect 함수를 사용하였기에
  // mapStateToProps의 number와 mapDispatchToProps의 increase, decrease를 props로 사용 가능해졌다.
  // 아래 props로 받은 increase, decrease는 위에서 import한 액션 생성자 함수가 아닌, 아래 connect 함수의 두 번째 인자로 들어간 함수의 반환 결과인 객체의 increase, decrease이다.
  const CounterContainer = ({ number, increase, decrease }) => {
      return (
          <Counter number={number} onIncrease={increase} onDecrease={decrease} />
      );
  };
  
  export default connect(
      (state) => ({ number: state.counter.number }),
      (dispatch) => ({
          increase: () => dispatch(increase()),
          decrease: () => dispatch(decrease()),
      })
  )(CounterContainer);
  ```
  
  - `bindActionCreators`
      - 컴포넌트에서 액션을 디스패치하기 위해 각 액션 함수를 호출하고, `dispatch`로 감싸는 작업은 액션 생성 함수의 개수가 많아질수록 번거롭다.
    - `bindActionCreators`는 이러한 번거로움을 덜어준다.
    - 첫 번째 인자로 액션 생성 함수로 이루어진 객체를 넣고, 두 번째 인자로 dispatch를 넣는다.
  
  ```react
  import React from "react";
  import { connect } from "react-redux";
  // 불러오고
  import { bindActionCreators } from "redux";
  import Counter from "../components/Counter";
  import { increase, decrease } from "../modules/counter";
  
  const CounterContainer = ({ number, increase, decrease }) => {
      return (
          <Counter number={number} onIncrease={increase} onDecrease={decrease} />
      );
  };
  
  export default connect(
      (state) => ({ number: state.counter.number }),
      // 아래와 같이 사용한다.
      (dispatch) => bindActionCreators({ increase, decrease }, dispatch)
  )(CounterContainer);
  ```
  
  - 더 편하게 하는 방법
    - `connect`의 두 번째 파라미터를 액션 생성 함수로 이루어진 객체만 넣으면 connect 함수가 내부적으로 `bindActionCreators` 작업을 대신해준다.
  
  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Counter from "../components/Counter";
  import { increase, decrease } from "../modules/counter";
  
  const CounterContainer = ({ number, increase, decrease }) => {
      return (
          <Counter number={number} onIncrease={increase} onDecrease={decrease} />
      );
  };
  
  export default connect(
      (state) => ({ number: state.counter.number }),
      { increase, decrease }
  )(CounterContainer);
  ```



- TodosContainer 만들기

  - TodosContainer.js 파일 작성

  ```react
  import React from "react";
  import { connect } from "react-redux";
  import Todos from "../components/Todo";
  import { changeInput, insert, toggle, remove } from "../modules/todos";
  
  const TodosContainer = ({
    input,
    todos,
    changeInput,
    insert,
    toggle,
    remove,
  }) => {
    return (
      <Todos
        input={input}
        todos={todos}
        onChangeInput={changeInput}
        onInsert={insert}
        onToggle={toggle}
        onRemove={remove}
      />
    );
  };
  
  export default connect(
    // 비구조화 할당을 통해 todos를 분리하여 state.todos.input 대신 todos.input을 사용
    ({ todos }) => ({ input: todos.input, todos: todos.todos }),
    { changeInput, insert, toggle, remove }
  )(TodosContainer);
  ```

  - App 컴포넌트의 Todos 컴포넌트를 TodosContainer 컴포넌트로 변경

  ```react
  import React from "react";
  import CounterContainer from "./containers/CounterContainer";
  import TodosContainer from "./containers/TodosContainer";
  
  const App = () => {
    return (
      <div>
        <CounterContainer number={0} />
        <hr />
        <TodosContainer />
      </div>
    );
  };
  
  export default App;
  ```

  - Todos 컴포넌트가 받아 온 props를 사용하도록 구현

  ```react
  import React from "react";
  
  const TodoItem = ({ todo, onToggle, onRemove }) => {
    return (
      <div>
        <input
          type="checkbox"
          onClick={() => onToggle(todo.id)}
          checked={todo.done}
          readOnly={true}
        />
        <span style={{ textDecoration: todo.done ? "line-through" : "none" }}>
          {todo.text}
        </span>
        <button onClick={() => onRemove(todo.id)}>삭제</button>
      </div>
    );
  };
  
  const Todos = ({
    input,
    todos,
    onChangeInput,
    onInsert,
    onToggle,
    onRemove,
  }) => {
    const onSubmit = (e) => {
      e.preventDefault();
      onInsert(input);
      onChangeInput("");
    };
  
    const onChange = (e) => onChangeInput(e.target.value);
    return (
      <div>
        <form onSubmit={onSubmit}>
          <input value={input} onChange={onChange} />
          <button type="submit">등록</button>
        </form>
        <div>
          {todos.map((todo) => (
            <TodoItem
              todo={todo}
              key={todo.id}
              onToggle={onToggle}
              onRemove={onRemove}
            />
          ))}
        </div>
      </div>
    );
  };
  
  export default Todos;
  ```




## 리덕스 더 편하게 사용하기

- redux-actions

  - 기능
    - 액션 생성 함수를 더 짧은 코드로 작성하는 것이 가능해진다.
    - 리듀서를 작성할 때도 `switch/case`문이 아닌 `handleActions`라는 함수를 사용하여 각 액션마다 업데이트 함수를 설정하는 형식으로 작성이 가능해진다.

  - 설치

  ```bash
  $ yarn add redux-actions
  ```

  - 액션 생성 함수를 더욱 짧은 코드로 작성하기
    - `createAction` 함수를 사용

  ```react
  import { createActions } from "redux-actions";
  
  const INCREASE = "counter/INCREASE";
  const DECREASE = "counter/DECREASE";
  
  /* redux-actions 사용 전
  export const increase = () => ({ type: INCREASE });
  export const decrease = () => ({ type: DECREASE });
  */
  
  // redux-actions 사용
  export const increase = createAction(INCREASE);
  export const decrease = createAction(DECREASE);
  ```

  - `createAction` 사용시 액션에 필요한 추가 데이터가 있을 경우
    - `createAction` 의 결과로 반환되는 액션 생성자 함수를 사용해 값을 추가한다.
    - 액션 생성자 함수의 인자로 추가하고자 하는 값을 넣으면 된다.
    - `payload:추가한 값`의 형태로 들어가게 된다.
    - 만일 인자로 받은 값에 함수 처리를 해주고 싶다면 `createAction` 함수의 두 번째 인자로 해당 함수를 넣어주면 된다.

  ```react
  const MY_ACTION = "sample/MY_ACTION";
  // myAction에는 액션 생성자 함수가 담기게 된다.
  const myAction = createAction(MY_ACTION);
  const action = myAction("Hello!");
  console.log(action); // Object {payload: "Hello!", type: "sample/MY_ACTION"}
  
  // 함수 처리 후 추가하기
  const MY_ACTION = "sample/MY_ACTION";
  const myAction = createAction(MY_ACTION, (num) => num * 3);
  const action = myAction(3);
  console.log(action); // {type: "sample/MY_ACTION", payload: 9}
  ```

  - 리듀서 함수를 더 간단하고 가독성 높게 작성하기
    - `handleActions` 함수 사용
    - 첫 번째 인자로 각 액션에 대한 업데이트 함수를 넣어 주고, 두 번째 인자로 초기 상태를 넣어준다.

  ```react
  import { createActions, handleAction } from "redux-actions";
  
  const INCREASE = "counter/INCREASE";
  const DECREASE = "counter/DECREASE";
  
  export const increase = createActions(INCREASE);
  export const decrease = createActions(DECREASE);
  
  const initialState = {
    number: 0,
  };
  
  const counter = handleAction(
    {
      [INCREASE]: (state, action) => ({ number: state.number + 1 }),
      [DECREASE]: (state, action) => ({ number: state.number - 1 }),
    },
    initialState
  );
  
  export default counter;
  ```

  - todos 모듈에 적용하기(`createAction`으로 액션 생성자 함수 생성하기 )

  ```react
  import { createAction } from "redux-actions";
  
  const CHANGE_INPUT = "todos/CHANGE_INPUT"; // input 값을 변경
  const INSERT = "todos/INSERT"; // 새로운 todo를 등록
  const TOGGLE = "todos/TOGGLE"; // todo를 체크/체크 해제
  const REMOVE = "todos/REMOVE"; // todo를 제거
  
  export const changeInput = createAction(CHANGE_INPUT, (input) => input);
  
  let id = 3;
  export const insert = createAction(INSERT, (text) => ({
    id: id++,
    text,
    done: false,
  }));
  
  export const toggle = createAction(TOGGLE, (id) => id);
  export const remove = createAction(REMOVE, (id) => id);
  
  // 위의 경우 결국 파라미터로 받은 값을 다시 반환하는데, 아래와 같이 써도 똑같이 동작한다.
  // import한 곳에서 toggle(1)와 같이 함수를 호출하면 payload에 1이 들어가기 때문이다.
  // 그러나 파라미터로 받은 값을 다시 반환하는 코드를 넣는 것이 이 액션 생성 함수가 어떤 파라미터를 받는지 쉽게 파악할 수 있기에 적어준다.
  // export const toggle = createAction(TOGGLE);
  // export const remove = createAction(REMOVE);
  (...)
  ```
  
  - todos 모듈에 적용하기(`handleActions`로 리듀서 작성하기)
  
  ```react
  (...)
    
  const todos = handleActions(
    {
      [CHANGE_INPUT]: (state, action) => ({ ...state, input: action.payload }),
      [INSERT]: (state, action) => ({
        ...state,
        todos: state.todos.concat(action.payload),
      }),
      [TOGGLE]: (state, action) => ({
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.payload ? { ...todo, done: !todo.done } : todo
        ),
      }),
      [REMOVE]: (state, action) => ({
        ...state,
        todos: state.todos.filter((todo) => todo.id !== action.payload),
      }),
    },
    initialState
  );
    
  export default todos;
  ```
    - 객체 비구조화 할당 문법 적용
      - 모든 추가 데이터가 값을 `action.payload`로 사용하기 때문에 나중에 리듀서 코드를 다시 볼 때 헷갈릴 수 있다.
        - 객체 비구조화 할당 문법으로 `action` 값의 `payload` 이름을 새로 설정해 주면 `action.payload`가 정확히 어떤 값을 의미하는지 더 쉽게 파악 가능해진다.
      - JavaScript_part14.디스트럭처링-키와 값을 함께 디스트럭처링 하는 것도 가능하다.
  
  ```react
  const todos = handleActions(
    {
      [CHANGE_INPUT]: (state, { payload: input }) => ({
        ...state,
        input,
      }),
      [INSERT]: (state, { payload: todo }) => ({
        ...state,
        todos: state.todos.concat(todo),
      }),
      [TOGGLE]: (state, { payload: id }) => ({
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === id ? { ...todo, done: !todo.done } : todo
        ),
      }),
      [REMOVE]: (state, { payload: id }) => ({
        ...state,
        todos: state.todos.filter((todo) => todo.id !== id),
      }),
    },
    initialState
  );
  
  export default todos;
  ```



- immer

  - 여러 차례 강조했듯 상태를 변경할 때는 불변성을 지켜야 한다.
    - 리듀서에서 상태를 업데이트 할 때 불변성을 지켜야 하기에 spread 문법과 배열의 내장 함수를 사용했다.
    - 그러나 모듈의 상태가 복잡해질수록 불변성을 지키기가 까다로워진다.
    - 따라서 모듈의 상태를 설계할 때는 객체의 깊이가 너무 깊어지지 않도록 주의해야 한다.
    - immer를 사용하면 훨씬 편리하게 불변성을 지키면서 상태를 관리할 수 있다.
  - 설치하기

  ```bash
  $ yarn add immer
  ```

  - todos 모듈에 적용하기
  - immer의 `produce` 함수는 첫 번째 인자로 변경 대상 상태, 두 번째 인자로 상태를 어떻게 업데이트 할지 정의한 함수를 받는다.
    - 두 번째 인자인 상태를 어떻게 업데이트 할지 정의한 함수는, `produce` 함수의 첫 번째 인자를 인자로 받는다.
  
  ```react
  import produce from 'immer';
  
  (...)
  const todos = handleActions(
    {
      [CHANGE_INPUT]: (state, { payload: input }) =>
        produce(state, (draft) => {
          draft.input = input;
        }),
      [INSERT]: (state, { payload: todo }) =>
        produce(state, (draft) => {
          draft.todos.push(todo);
        }),
      [TOGGLE]: (state, { payload: id }) =>
        produce(state, (draft) => {
          const todo = draft.todos.find((todo) => todo.id === id);
          todo.done = !todo.done;
        }),
      [REMOVE]: (state, { payload: id }) =>
        produce(state, (draft) => {
          const index = draft.todos.findIndex((todo) => todo.id === id);
          draft.todos.splice(index, 1);
        }),
    },
    initialState
  );
  ```



## Hooks를 사용하여 컨테이너 컴포넌트 만들기

- 리둑스 스토어와 연동된 컨테이너 컴포넌트를 만들 때 `connect` 함수를 사용하는 대신 react-redux에서 제공하는 Hooks를 사용할 수도 있다.



- `useSelector`

  - `useSelector` Hook을 사용하면 `connect` 함수를 사용하지 않고도 리덕스의 상태를 조회할 수 있다.
  - 사용법

  ```javascript
  const 결과 = useSelector(상태 선택 함수)
  ```

  - 적용

  ```react
  import React from "react";
  import { useSelector } from "react-redux";
  import Counter from "../components/Counter";
  import { increase, decrease } from "../modules/counter";
  
  const CounterContainer = () => {
    const number = useSelector((state) => state.counter.number);
    return <Counter number={number} />;
  };
  
  export default CounterContainer;
  ```



- `useDispatch`

  - 컴포넌트 내부에서 스토어의 내장함수 dispatch를 사용할 수 있게 해준다.
  - 사용법

  ```javascript
  const dispatch = useDispatch()
  // 인자로 액션을 받는다.
  dispatch({type:'SAMPLE_ACTION'})
  ```

  - 적용

  ```react
  import React from "react";
  import { useSelector, useDispatch } from "react-redux";
  import Counter from "../components/Counter";
  import { increase, decrease } from "../modules/counter";
  
  const CounterContainer = () => {
    const number = useSelector((state) => state.counter.number);
    const dispatch = useDispatch();
    return (
      <Counter
        number={number}
        // 인자로 액션 생성자 함수를 받는데 결국 액션 생성자 함수는 액션을 반환한다.
        onIncrease={() => dispatch(increase())}
        onDecrease={() => dispatch(decrease())}
      />
    );
  };
  
  export default CounterContainer;
  ```

  - `useCallback` 적용하기
    - 숫자가 바뀌어서 컴포넌트가 리렌더링될 때마다 `onIncrease`, `onDecrease` 함수가 새롭게 만들어진다.
    - 만약 컴포넌트 성능을 최적화해야 한다면 `useCallBack`으로 액션을 디스패치하는 함수를 감싸주는 것이 좋다.
    - `useCallback` 의 두 번째 인자로 `[dispatch]`를 넘겨줬는데 이는 `useCallBack` 내부에서 `dispatch`를 사용하고 있기 때문이다.

  ```react
  import React, { useCallback } from "react";
  import { useSelector, useDispatch } from "react-redux";
  import Counter from "../components/Counter";
  import { increase, decrease } from "../modules/counter";
  
  const CounterContainer = () => {
    const number = useSelector((state) => state.counter.number);
    const dispatch = useDispatch();
    const onIncrease = useCallback(() => dispatch(increase()), [dispatch]);
    const onDecrease = useCallback(() => dispatch(decrease()), [dispatch]);
    return (
      <Counter number={number} onIncrease={onIncrease} onDecrease={onDecrease} />
    );
  };
  
  export default CounterContainer;
  ```



- `useStore`

  - 컴포넌트 내부에서 리덕스 스토어 객체를 직접 사용할 수 있게 해준다.
    - 정말 어쩌다 스토어에 직접 접근해야 하는 상황에만 사용한다. 사용할 일은 별로 없다.
  - 사용법

  ```javascript
  const store = useStore()
  store.dispatch({type:'SAMPLE_ACTION'})
  store.getState()
  ```



- TodosContainer를 Hooks로 전환하기

  ```react
  import React, { useCallback } from "react";
  import { useDispatch, useSelector } from "react-redux";
  import Todos from "../components/Todo";
  import { changeInput, insert, toggle, remove } from "../modules/todos";
  
  const TodosContainer = () => {
    const { input, todos } = useSelector(({ todos }) => ({
      input: todos.input,
      todos: todos.todos,
    }));
    const dispatch = useDispatch();
    const onChangeInput = useCallback((input) => dispatch(changeInput(input)), [
      dispatch,
    ]);
    const onInsert = useCallback((text) => dispatch(insert(text)), [dispatch]);
    const onToggle = useCallback((id) => dispatch(toggle(id)), [dispatch]);
    const onRemove = useCallback((id) => dispatch(remove(id)), [dispatch]);
  
    return (
      <Todos
        input={input}
        todos={todos}
        onChangeInput={onChangeInput}
        onInsert={onInsert}
        onToggle={onToggle}
        onRemove={onRemove}
      />
    );
  };
  
  export default TodosContaine;
  ```



- `useActions` 유틸 Hook을 만들어서 사용하기

  - `useActions`는 원래 react-redux에 내장된 상태로 릴리즈될 계획이었으나 리덕스 개발 팀에서 꼭 필요하지 않다고 판단하여 제외된 Hook이다.
    - 그 대신 공식문서에서 그대로 복사하여 사용할 수 있도록 제공하고 있다.
  - 본래 connect 함수가 해주던 역할을 대신한다.
  - src/lib 디렉토리를 만들고 그 안에 useActions.js파일을 작성한다.
  
  ```react
  import { useMemo } from "react";
  import { useDispatch } from "react-redux";
  import { bindActionCreators } from "redux";
  
  export default function useActions(actions, deps) {
    const dispatch = useDispatch();
    // 액션을 디스패치 하는(액션을 발생시키는) 함수(들)을 반환한다.
    return useMemo(
      () => {
        if (Array.isArray(actions)) {
          return actions.map((a) => bindActionCreators(a, dispatch));
        }
        return bindActionCreators(actions, dispatch);
      },
      // deps가 true면(빈 배열이 아니면) 해당 배열의 원소가 바뀌면 액션을 디스패치하는 함수를 새로 생성한다.
      deps ? [dispatch, ...deps] : deps
    );
  }
  ```
  
  - 위에서 작성한 `useActions` Hook은 액션 생성 함수를 액션을 디스패치 하는 함수로 변환해 준다.
    
      - 액션 생성 함수를 사용하여 액션 객체를 만들고, 이를 스토어에 디스패치하는 작업을 해 주는 함수를 자동으로 만들어주는 것이다.
      
      - 첫 번째 파라미터는 액션 생성 함수로 이루어진 배열이다.
    - 두 번째 파리미터는 `deps`배열로 이 배열 안에 들어 있는 원소가 바뀌면 액션을 디스패치하는 함수를 새로 만들게 된다.
  - 적용
  
  ```react
  import { useSelector } from "react-redux";
  import Todos from "../components/Todo";
  import useActions from "../lib/useActions";
  import { changeInput, insert, toggle, remove } from "../modules/todos";
  
  // useActions에서 useDispatch를 사용했으므로, props로 받지 않는다.
  const TodosContainer = () => {
      const { input, todos } = useSelector(({ todos }) => ({
          input: todos.input,
          todos: todos.todos,
      }));
      // 반환 값을 디스트럭처링으로 할당한다.
      const [onChangeInput, onInsert, onToggle, onRemove] = useActions(
          [changeInput, insert, toggle, remove],
          []
      );
  
      return (
          <Todos
              input={input}
              todos={todos}
              onChangeInput={onChangeInput}
              onInsert={onInsert}
              onToggle={onToggle}
              onRemove={onRemove}
              />
      );
  };
  
  export default TodosContainer;
  ```



- `connect` 함수를 사용하는 것과 주요 차이점
  - `connect` 함수를 사용하여 컨테이너 컴포넌트를 만들었을 경우, 해당 컨테이너 컴포넌트의 부모 컴포넌트가 리렌더링될 때 해당 컨테이너 컴포넌트의 props가 바뀌지 않았다면 리렌더링이 자동으로 방지되어 성능이 최적화 된다.
  - 반면 `useSelector`를 사용하여 리덕스 상태를 조회하면, 이 최적화 작업이 자동으로 이루어지지 않으므로 성능 최적화를 위해서는 `React.memo`를 컨테이너 컴포넌트에 사용해 줘야 한다.
  
  ```react
  import { useSelector } from "react-redux";
  import Todos from "../components/Todo";
  import useActions from "../lib/useActions";
  import { changeInput, insert, toggle, remove } from "../modules/todos";
  
  const TodosContainer = () => {
      (...)};
  
  export default React.memo(TodosContainer);
  ```
  
  

