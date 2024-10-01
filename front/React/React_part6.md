# 컴포넌트 성능 최적화

> `todo-app`을 기반으로 예시를 설명한다.

## 문제 발생 및 원인 분석

- 문제 발생시키기

  - 대량의 데이터를 추가했을 때에도 이상 없이 동작하는지 확인하기 위해 데이터를 추가한다.
    - 데이터를 일일이 추가할 수는 없으므로 아래와 같이 반복문을 사용해서 추가한다.

  ```react
  import React, { useCallback, useRef, useState } from "react";
  import TodoInsert from "./components/TodoInsert";
  import TodoList from "./components/TodoList";
  import TodoTemplate from "./components/TodoTemplate";
  
  function createBulkTodos() {
    const array = [];
    for (let i = 1; i <= 2500; i++) {
      array.push({
        id: i,
        text: `할 일 ${i}`,
        checked: false,
      });
    }
    return array;
  }
  
  const App = () => {
    const [todos, setTodos] = useState(createBulkTodos);
  
    (...)
  
    return (...);
  };
  
  export default App;
  ```



- 문제 확인 및 원인 분석
  - 문제 확인
    - 개발자 도구의 Performance 탭으로 이동한다.
    - 녹화 버튼이 있는데 녹화 버튼 클릭 후 할 일 목록 중 하나를 제거하고 제거되면 중지 버튼을 누른다.
    - 이후 결과 화면이 나오는데 위 작업을 처리하는 데 걸린 시간을 알 수 있다.
    - 현재 대량의 데이터를 처리하여 시간이 오래 걸리는 것을 확인 가능하다.
  - 원인 분석
    - 컴포넌트는 state가 변경되면 리렌더링이 발생한다.
    - App 컴포넌트의 state가 변경되면서 App 컴포넌트가 리렌더링 된다.
    - 컴포넌트는 부모 컴포넌트가 리렌더링 될 때 리렌더링 된다.
    - App 컴포넌트가 리렌더링 되면서 자식 컴포넌트인 TodoList도 리렌더링 된다.
    - 할 일 하나를 지우면 지워진 할 일만 리렌더링 하면 되는데 나머지 2499개의 할 일들도 리렌더링 되어 느린 것이다.
    - 따라서 불필요한 리렌더링이 원인이다.



## 문제 해결

- `React.memo`를 사용하여 리렌더링 방지

  - 리렌더링을 방지할 때는 `shouldComponentUpdate`라는 라이프사이클을 사용한다.
  - 그러나 함수형 컴포넌트에서는 라이프사이클 메서드를 사용할 수 없으므로 `React.memo`를 사용한다.
  - 이제 TodoListItem 컴포넌트는 props(`todo`, `onRemove`, `onToggle`)가 변경되지 않는 한 리렌더링 되지 않는다.

  ```react
  import React from "react";
  import {
    MdCheckBoxOutlineBlank,
    MdCheckBox,
    MdRemoveCircleOutline,
  } from "react-icons/md";
  import cn from "classnames";
  import "./TodoListItem.scss";
  
  const TodoListItem = ({ todo, onRemove, onToggle }) => {
    const { id, text, checked } = todo;
    return (...);
  };
  
  export default React.memo(TodoListItem);
  ```



- `onToggle`, `onRemove` 함수가 바뀌지 않게 하기

  - 현재 코드상으로는 `todos` 배열이 변경되면 `onToggle`, `onRemove` 함수도 새롭게 바뀌게 된다.
    - 두 함수는 배열 상태를 업데이트 하는 과정에서 최신 상태의 `todos`를 참조하기 때문에 `todos`가 변경될 때마다 함수가 새로 만들어지기 때문이다.
    - `useState`의 함수형 업데이트 기능을 사용하거나 `useReducer`를 사용하면 해결 된다.
    - 두 방식 모두 성능은 비슷하다.
  - `useState`의 함수형 업데이트
    - 새로운 상태를 인자로 넣는 대신, 상태 업데이트를 어떻게 할지 정의해 주는 업데이트 함수를 넣는 방식.
    - 기존에는 `setTodos(todos.filter((todo) => todo.id !== id));`와 같이 새로운 상태(`filter`로 걸러진 새로운 배열)를 넣어주고, `useCallBack`의 두 번째 인자로 `[todos]`를 줬다.
    - 아래 코드는 `setTodos((todos) => todos.filter((todo) => todo.id !== id));`와 같이 새로운 상태가 아닌, 상태 업데이트를 어떻게 할지 정의해주는 업데이트 함수를 넣고, `useCallBack`의 두 번째 인자로 빈 배열을 줘 더 이상 `onToggle`, `onRemove` 함수가 `todos`의 최신 상태를 참조하지 않도록 변경하였다.
    - `seInsert`도 마찬가지로 수정해주었다.

  ```react
  import React, { useCallback, useRef, useState } from "react";
  import TodoInsert from "./components/TodoInsert";
  import TodoList from "./components/TodoList";
  import TodoTemplate from "./components/TodoTemplate";
  
  (...)
  
  const App = () => {
    (...)
     
    const onInsert = useCallback((text) => {
      const todo = {
        id: nextId.current,
        text,
        checked: false,
      };
      setTodos((todos) => todos.concat(todo));
      nextId.current += 1;
    }, []);
     
    const onRemove = useCallback((id) => {
      setTodos((todos) => todos.filter((todo) => todo.id !== id));
    }, []);
  
    const onToggle = useCallback((id) => {
      setTodos((todos) =>
        todos.map((todo) =>
          todo.id === id ? { ...todo, checked: !todo.checked } : todo,
        ),
      );
    }, []);
  
    return (...);
  };
  
  export default App;
  ```

  - `useReducer` 사용하기
    - `useReducer`를 사용할 때는 원래 두 번째 파라미터에 초기 상태를 넣어 주어야 한다. 
    - 아래 코드는 그 대신 두 번째 파라미터에 undefined를 넣고, 세 번째 파라미터에 초기 상태를 만들어 주는 함수를 넣어줬다.
    - 이렇게 하면 컴포넌트가 맨 처음 렌더링 될 때만 `createBulkTodos` 함수가 호출된다.

  ```react
  import React, { useCallback, useRef, useReducer } from "react";
  import TodoInsert from "./components/TodoInsert";
  import TodoList from "./components/TodoList";
  import TodoTemplate from "./components/TodoTemplate";
  
  function createBulkTodos() {
    const array = [];
    for (let i = 1; i <= 2500; i++) {
      array.push({
        id: i,
        text: `할 일 ${i}`,
        checked: false,
      });
    }
    return array;
  }
  
  function todoReducer(todos, action) {
    switch (action.type) {
      case "INSERT":
        return todos.concat(action.todo);
      case "REMOVE":
        return todos.filter((todo) => todo.id !== action.id);
      case "TOGGLE":
        return todos.map((todo) =>
          todo.id === action.id ? { ...todo, checked: !todo.checked } : todo,
        );
    }
  }
  
  const App = () => {
    const [todos, dispatch] = useReducer(todoReducer, undefined, createBulkTodos);
  
    const nextId = useRef(2501);
  
    const onInsert = useCallback((text) => {
      const todo = {
        id: nextId.current,
        text,
        checked: false,
      };
      dispatch({ type: "INSERT", todo });
      nextId.current += 1;
    }, []);
  
    const onRemove = useCallback((id) => {
      dispatch({ type: "REMOVE", id });
    }, []);
  
    const onToggle = useCallback((id) => {
      dispatch({ type: "TOGGLE", id });
    }, []);
  
    return (...);
  };
  
  export default App;
  ```



- 불변의 중요성

  - 리액트 컴포넌트에서 상태를 업데이트 할 때 불변성을 지키는 것은 매우 중요하다.
    - 기존 데이터를 수정할 때 직접 수정하지않고, 새로운 배열을 만든 다음 새로운 객체를 만들어서 필요한 부분을 교체해 주는 방식으로 구현했다.
    - 업데이트가 필요한 곳에서는 아예 새로운 배열 또는 객체를 만들기에 `React.memo`를 사용했을 때 props가 변경되었는지 여부를 알아내서 리렌더링 성능을 최적화해 줄 수 있다.

  - 불변성이 지켜지지 않으면 객체 내부의 값이 새로워져도 바뀐 것을 감지하지 못한다.
    - 따라서 `React.memo`에서 서로 비교하여 최적화하는 것이 불가능해진다.

  ```javascript
  const arr = [1,2,3]
  
  // 배열을 복사하는 것이 아니라 똑같은 배열을 가리키게 된다.
  const sameArr = arr;
  sameArr[0]=9
  console.log(arr===sameArr) // true
  
  // 배열 내부의 값을 복사
  const otherArr = [...arr]
  otherArr[0] = 8
  console.log(arr===otherArr) // false
  
  const obj = {
      name:'Cha',
      age:28
  }
  
  // 객체를 복사하는 것이 아니라 똑같은 객체를 가리키게 된다.
  const sameObj = obj
  sameObj.age+=1
  console.log(obj===sameObj) // true
  
  // 객체 내부의 값을 복사
  const = {
      ...obj,age=obj.age+1
  }
  console.log(obj===sameObj) // false
  ```

  - 전개 연산자는 깊은 복사를 하지는 못한다.
    - 내부의 값이 완전히 복사되는 것이 아니라 가장 바깥쪽에 있는 값만 복사된다.
    - 따라서 내부의 값이 객체나 배열이라면 내부의 값 또한 따로 복사해줘야 한다.
    - 뒤에서 배울 `immer`를 통해 쉽게 할 수 있다.

  ```javascript
  const arr = [0, 1, 2, { name: "Cha", age: 28 }];
  const shallowCopy = [...arr];
  console.log(arr === shallowCopy); // false
  console.log(arr[3] === shallowCopy[3]); // true
  shallowCopy[3] = { ...arr[3] };
  console.log(arr[3] === shallowCopy[3]); // false
  ```

  

- 리스트와 관련된 컴포넌트 최적화하기

  - 리스트에 관련된 컴포넌트를 최적화할 때는 리스트 내부에서 사용하는 컴포넌트도 최적화해야 하고, 리스트로 사용되는 컴포넌트 자체도 최적화해 주는 것이 좋다.
    - 예를 들어 `TodoList.js`를 최적화 할 때는 `TodoListItem.js`도 함께 최적화 하는 것이 좋다.
  - 그러나 데이터 수가 적거나 업데이트가 자주 발생하지 않으면 반드시 해줄 필요는 없다.
  - 앞에서 `TodoListItem`을 최적화했으므로 `TodoList.js`도 최적화한다.
    - 단 현시점에서 부모 컴포넌트인 App 컴포넌트가 리렌더링 되는 유일한 이유가 `todos` 배열이 업데이트될 때이기 때문에, 아래와 같은 작업을 하지 않아도 TodoList 컴포넌트에는 불필요한 리렌더링이 발생하지 않는다.
    - 그러나, 나중에 App 컴포넌트에 다른 state가 추가되어 해당 값들이 업데이트 될 때는 TodoList 컴포넌트가 불필요한 렌더링을 할 수도 있기에 미리 최적화 해주는 것이다.

  ```react
  import React from "react";
  import TodoListItem from "./TodoListItem";
  import "./TodoList.scss";
  
  const TodoList = ({ todos, onRemove, onToggle }) => {
    return (
      <div className="TodoList">
        {todos.map((todo) => (
          <TodoListItem
            todo={todo}
            key={todo.id}
            onRemove={onRemove}
            onToggle={onToggle}
          />
        ))}
      </div>
    );
  };
  
  export default React.memo(TodoList);
  ```



- `react-virtualized`를 사용한 렌더링 최적화

  - 아직까지 렌더링 방식은 비효율적이다.
    - 위에서 2500개의 데이터를 넣었지만 실제 나오는 데이터는  9개 뿐이고 나머지는 스크롤 해야 볼 수 있다.
    - 현재 컴포넌트가 맨 처음 렌더링 될 때 2,491개의 데이터는 스크롤 하기 전에는 보이지 않음에도 렌더링이 발생한다.
    - 또한 `todos`배열에 변동이 생길 때도 TodoList 컴포넌트 내부의 `map` 함수에서 배열의 처음부터 끝까지 컴포넌트를 변환해 주는데 이 중에서 2,491개는 보이지 않으므로 시스템 자원 낭비다.

  - `react-virtualized`를 사용하면 리스트 컴포넌트에서 스크롤되기 전에 보이지 않는 컴포넌트는 렌더링하지 않고 크기만 차지하게끔 할 수 있다.
    - 만약 스크롤되면 해당 스크롤 위치에서 보여줘야 할 컴포넌트를 자연스럽게 렌더링시킨다.
    - 이를 통해 낭비되는 자원을 아낄 수 있다.
  - 설치하기

  ```bash
  $ yarn add react-virtualized
  ```

  - 사전 준비
    - 각 항목의 실제 크기를 px 단위로 알아내야 한다.
    - 크롬 개발자 도구를 통해 정확한 px 값을 찾아낸다.
  - TodoList 수정
    - `List` 컴포넌트를 사용하기 위해 `rowRenderer`라는 함수를 새로 작성해 준다.
    - 이 함수는 `react-virtualized`의 `List` 컴포넌트에서 각 TodoItem을 렌더링 할 때 사용하며, 이 함수를 List 컴포넌트의 props로 설정해 줘야 한다.
    - 이 함수는 파라미터에 `index`,`key`,`style` 값을 객체 타입으로 받아 와서 사용한다.
    - `List` 컴포넌트를 사용할 때는 해당 리스트의 전체 크기와 각 항목의 높이, 각 항목을 렌더링할 때 사용해야 하는 함수, 그리고 배열을 props로 넣어 주어야 한다. 이 컴포넌트가 전달 받은 props를 사용하여 자동으로 최적화해준다.

  ```react
  import React from "react";
  import { List } from "react-virtualized";
  import TodoListItem from "./TodoListItem";
  import "./TodoList.scss";
  
  const TodoList = ({ todos, onRemove, onToggle }) => {
    const rowRenderer = useCallback(
      ({ index, key, style }) => {
        const todo = todos[index];
        return (
          <TodoListItem
            todo={todo}
            key={key}
            onRemove={onRemove}
            onToggle={onToggle}
            style={style}
          />
        );
      },
      [onRemove, onToggle, todos],
    );
    return (
      <List
        className="TodoList"
        width={495.2}
        height={495.2}
        rowCount={todos.length}
        rowHeight={57}
        rowRenderer={rowRenderer}
        list={todos}
        style={{ outline: "none" }}
      />
    );
  };
  
  export default React.memo(TodoList);
  ```

  - TodoListItem 수정 
    - TodoListItem까지 수정해줘야 스타일이 깨지지 않는다.
    -  기존에 보여 주던 내용을 `div`로 한 번 감싸고, 해당 `div`에 `TodoListItem-virtualized`라는 className을 설정하고, props로 받아온 style을 적용시킨다.
    - `TodoListItem-virtualized`라는 클래스를 만든 것은 최적화와는 무관하게, 컴포넌트 사이사이에 테두리를 제대로 쳐 주고, 홀수 번째, 짝수 번째 항목에 다른 배경 색상을 설정하기 위함이다.

  ```scss
  .TodoListItem-virtualized {
    & + & {
      border-top: 1px solid #dee2e6;
    }
    &:nth-child(even) {
      background: #f8f9fa;
    }
  }
  ```

  ```react
  import React from "react";
  import {
    MdCheckBoxOutlineBlank,
    MdCheckBox,
    MdRemoveCircleOutline,
  } from "react-icons/md";
  import cn from "classnames";
  import "./TodoListItem.scss";
  
  const TodoListItem = ({ todo, onRemove, onToggle, style }) => {
    const { id, text, checked } = todo;
    return (
      <div className="TodoListItem-virtualized" style={style}>
        <div className="TodoListItem">
          <div
            className={cn("checkbox", { checked })}
            onClick={() => {
              onToggle(id);
            }}
          >
            {checked ? <MdCheckBox /> : <MdCheckBoxOutlineBlank />}
            <div className="text">{text}</div>
          </div>
          <div className="remove" onClick={() => onRemove(id)}>
            <MdRemoveCircleOutline />
          </div>
        </div>
      </div>
    );
  };
  
  export default React.memo(TodoListItem);
  ```



# immer

- `immer`

  - 상태를 변경할 때는 불변성을 유지해야 한다.
    - 대부분의 방법은 얕은 복사만을 지원한다.
    - 객체의 구조가 깊어질수록 불변성을 유지하면서 이를 업데이트 하는 것이 힘들어진다.
  - `immer`는 구조가 복잡한 객체도 매우 쉽고 짧은 코드를 사용하여, 불변성을 유지하면서 상태를 변경할 수 있게 도와주는 라이브러리다.
    - 단, `immer`를 사용하지 않는 것이 더 간결하고 깔끔한 코드가 될 때는 사용하지 않아도 된다.
  - 설치

  ```bash
  $ yarn add immer
  ```

  - 사용 방법
    - `produce` 함수는 첫 번째 파라미터로 수정하고 싶은 상태를 받고, 두 번째 파라미터로 상태를 어떻게 변경할지를 정의하는 함수를 받는다.
    - 두 번째 파라미터로 전달되는 함수 내부에서 원하는 값을 변경하면, `produce` 함수가 불변성 유지를 대신해 주면서 새로운 상태를 생성해 준다.
    - 두 번째 파라미터로 전달되는 함수는 인자(draft)로 `produce()`함수의 첫 번째 인자를 받는다.
  
  ```react
  import produce from 'immer'
  
  const changedState = produce(originalState, draft=>{
      // 바꾸려는 값 바꾸기
      draft.somewhere.deep.inside=5
  }
  ```



- 불변성 유지하기

  - `immer`를 사용하지 않고 불변성 유지하기

  ```react
  import React, { useCallback, useRef } from "react";
  
  const App = () => {
    const nextId = useRef(1);
    const [form, setForm] = useState({ name: "", username: "" });
    const [data, setData] = usestate({
      array: [],
      uselessValue: null,
    });
  
    const onChange = useCallback(
      (e) => {
        const { name, value } = e.target;
        setForm({ ...form, [name]: [value] });
      },
      [form]
    );
  
    const onSubmit = useCallback(
      (e) => {
        e.preventDefault();
        const info = {
          id: nextId.current,
          name: form.name,
          username: form.username,
        };
        setData({
          ...data,
          array: data.array.concat(info),
        });
  
        setForm({
          name: "",
          username: "",
        });
        nextId.current += 1;
      },
      [data, form.name, form.username]
    );
  
    const onRemove = useCallback(
      (id) => {
        setData({ ...data, array: data.array.filter((info) => info.id !== id) });
      },
      [data]
    );
    return (
      <div>
        <form onSubmit={onSubmit}>
          <input
            name="username"
            placeholder="아이디를 입력하세요"
            value={form.username}
            onChange={onChange}
          />
          <input
            name="name"
            placeholder="이름을 입력하세요"
            value={form.name}
            onChange={onChange}
          />
          <button type="submit">등록</button>
        </form>
        <div>
          <ul>
            {data.array.map((info) => (
              <li key={info.id} onClick={() => onRemove(info.id)}>
                {info.username}({info.name})
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  };
  
  export default App;
  ```

  - `immer`를 사용하여 불변성 유지
    - `immer`를 사용할 때는 `push`, `splice`등 배열에 직접적 변화를 일으키는 함수를 사용해도 무방하다. 

  ```react
  import React, { useCallback, useRef, useState } from "react";
  import produce from "immer";
  
  const App = () => {
    const nextId = useRef(1);
    const [form, setForm] = useState({ name: "", username: "" });
    const [data, setData] = useState({
      array: [],
      uselessValue: null,
    });
  
    const onChange = useCallback(
      (e) => {
        const { name, value } = e.target;
        setForm(
          produce(form, (draft) => {
            draft[name] = value;
          })
        );
      },
      [form]
    );
  
    const onSubmit = useCallback(
      (e) => {
        e.preventDefault();
        const info = {
          id: nextId.current,
          name: form.name,
          username: form.username,
        };
        setData(
          produce(data, (draft) => {
            draft.array.push(info);
          })
        );
  
        setForm({
          name: "",
          username: "",
        });
        nextId.current += 1;
      },
      [data, form.name, form.username]
    );
  
    const onRemove = useCallback(
      (id) => {
        setData(
          produce(data, (draft) => {
            draft.array.splice(
              draft.array.findIndex((info) => info.id === id),
              1
            );
          })
        );
      },
      [data]
    );
    return (...);
  };
  
  export default App;
  ```



- `useState`의 함수형 업데이트와 `immer`함께 쓰기

  - `immer`에서 제공하는 `produce` 함수를 호출할 때, 첫 번째 파라미터가 함수 형태라면 변환 된 상태가 아닌, 업데이트 함수를 반환한다.
  - 이러한 `immer`의 속성과 `useState`의 함수형 업데이트를 함께 활용하면 코드를 더욱 깔끔하게 만들 수 있다.

  ```react
  import React, { useCallback, useRef, useState } from "react";
  import produce from "immer";
  
  const App = () => {
    const nextId = useRef(1);
    const [form, setForm] = useState({ name: "", username: "" });
    const [data, setData] = useState({
      array: [],
      uselessValue: null,
    });
  
    const onChange = useCallback((e) => {
      const { name, value } = e.target;
      setForm(
        produce((draft) => {
          draft[name] = value;
        })
      );
    }, []);
  
    const onSubmit = useCallback(
      (e) => {
        e.preventDefault();
        const info = {
          id: nextId.current,
          name: form.name,
          username: form.username,
        };
        setData(
          produce((draft) => {
            draft.array.push(info);
          })
        );
  
        setForm({
          name: "",
          username: "",
        });
        nextId.current += 1;
      },
      [form.name, form.username]
    );
  
    const onRemove = useCallback((id) => {
      setData(
        produce((draft) => {
          draft.array.splice(
            draft.array.findIndex((info) => info.id === id),
            1
          );
        })
      );
    }, []);
    return (
      <div>
        <form onSubmit={onSubmit}>
          <input
            name="username"
            placeholder="아이디를 입력하세요"
            value={form.username}
            onChange={onChange}
          />
          <input
            name="name"
            placeholder="이름을 입력하세요"
            value={form.name}
            onChange={onChange}
          />
          <button type="submit">등록</button>
        </form>
        <div>
          <ul>
            {data.array.map((info) => (
              <li key={info.id} onClick={() => onRemove(info.id)}>
                {info.username}({info.name})
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  };
  
  export default App;
  ```

  











