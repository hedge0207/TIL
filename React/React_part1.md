# React란

- React 개요
  - 프론트엔드 개발 도구
  - 페이스북에서 개발
  - Vue, Angular에 비해 월등히 높은 사용량



- 리액트는 라이브러리인가 프레임워크인가
  - Vue는 스스로 Framework이라고 소개한다.
  - React는 스스로 Library라고 소개한다.
  - 기존의 MVC, MVVM 등의 아키텍처에서 V에 해당하는 View에만 집중한 라이브러리



- 리액트는 왜 만들었는가
  - 시간이 지나면서 변화하는 데이터를 표현하는 재사용 가능한 UI 컴포넌트를 만들기 위해서
  - 기존에 데이터가 변형되면 해당 페이지의 어떤 부분이 변경되었는지를 찾아 해당 부분을 변경해야 했다.
    - 애플리케이션 규모가 클수록 복잡해지고 제대로 관리하지 않으면 성능도 떨어지게 된다.
  - 페이스북 개발 팀은 데이터가 변화하면 그냥 기존 뷰를 날려버리고 처음부터 새로 렌더링 하는 방식을 고안했다.
    - 이를 통해 애플리케이션 구조는 간단해지고, 작성해야 할 코드도 줄어들었다.
  - 그러나 DOM은 느리기에 이러한 방식은 CPU, 메모리 사용량이 증가한다는 문제가 생긴다.
    - 리액트는Virtual DOM를 사용하여 이러한 문제를 해결한다.



- 초기 렌더링
  - 컴포넌트: 특정 부분이 어떻게 생길지 정하는 선언체.
  - 렌더링: 사용자 화면에 View를 보여주는 것.
  - 모든 UI 관련 프레임워크, 라이브러리는 맨 처음 어떻게 보일지를 정하는 초기 렌더링이 필요하다.
  - 리액트에서 초기 렌더링을 담당하는 것은 `render()` 함수다.
    - 이 함수는 컴포넌트가 어떻게 생겼는지 정의하는 역할을 한다.
    - 이 함수는 html 형식의 문자열을 반환하지 않고, 뷰가 어떻게 생겼고 어떻게 동작하는지에 대한 정보를 지닌 **객체를 반환**한다.
    - 컴포넌트 내부에는 또 다른 컴포넌트들이 들어갈 수 있는데 이 때 `render()` 함수를 실행하면 그 내부에 있는 컴포넌트들도 재귀적으로 렌더링한다.
    - 이렇게 최상위 컴포넌트의 렌더링 작업이 끝나면 지니고 있는 정보들을 사용하여 HTML 마크업을 만들고 이를 우리가 정하는 실제 페이지의 DOM 요소 안에 주입한다.
  - 컴포넌트를 실제 페이지에 렌더링 할 때는 분리된 두 가지 절차를 따른다.
    - 먼저 문자열 형태의 HTML 코드를 생성한다.
    - 그 후 생성된 HTML 코드를 특정 DOM에 주입하면 이벤트가 적용된다.



- 조화 과정
  - 리액트에서 뷰를 업데이트 할 때는 업데이트한다고 하기보다는 조화 과정(reconciliation)을 거친다는 것이 더 정확한 표현이다.
    - 컴포넌트에 데이터 변화가 있을 때 우리가 보기에는 변화에 따라 뷰가 변형되는 것 같지만 사실은 새로운 요소로 갈아 끼우는 것이다.
  - 조화 과정 또한 `render()` 함수가 담당한다.
    - 컴포넌트는 데이터에 변경이 있을 때 단순히 변경된 데이터 값을 수정하여 보여주는 것이 아니라, 새로운 데이터를 가지고 `render()` 함수를 다시 호출한다.
    - 그 결과 변경된 데이터를 지닌 뷰를 반환한다.
    - 이 반환된 뷰를 곧바로 DOM에 반영하지 않고, 이전에 `render()` 함수가 만들었던 컴포넌트 정보(초기 렌더링 결과)와 현재 `render()` 함수가 만든 컴포넌트 정보를 비교한다.
  - JS를 사용하여 두 가지 뷰(돔 트리)를 최소한의 연산으로 비교한 후, 둘의 차이를 알아내 최소한의 연산으로 DOM 트리를 업데이트 한다.
    - 방식 자체는 루트 노드부터 시작하여 전체 컴포넌트를 처음부터 다시 렌더링하는 것 처럼 보이지만 사실 최적의 자원을 이용해 이를 수행한다.



- Virtual DOM
  - DOM이 느리다는 말은 반은 사실이고 반은 거짓이다.
    - DOM 자체는 빠르다. DOM 자체를 읽고 쓸 때의 성능은 JS 객체를 처리할 때의 성능과 비교하여 다르지 않다.
    - 단, 웹 브라우저 단에서 DOM에 변화가 일어나면 웹 브라우저가 CSS를 다시 연산하고, 레이아웃을 구성하고, 페이지를 리페인트하는데 이 과정에서 시간이 허비된다.
  - 리액트의 주요 특징 중 하나는 Virtual DOM을 사용한다는 것이다.
    - 리액트는 Virtual DOM 방식을 사용하여 DOM 업데이트를 추상화함으로써 DOM 처리 횟수를 최소화하고 효율적으로 진행한다.
  - Virtual DOM
    - 변화가 일어났을 때 브라우저의 DOM과 비교를 하기 위해, JS로 만들어진 가상의 DOM
  - Virtual DOM 사용 방식
    - 데이터를 업데이트 한다.
    - 전체 UI를 Virtual DOM에 리렌더링한다.
    - 이전 Virtual DOM에 있던 내용과 현재 내용을 비교한다(초기 렌더링도 Virtual DOM을 거친다).
    - 바뀐 부분만 실제 DOM에 적용한다.
  - 오해
    - Virtual DOM을 사용한다고 해서 사용하지 않을 때와 비교하여 무조건 빠른 것은 아니다.
    - Virtual DOM을 사용하지 않아도 코드 최적화를 열심히 하면 DOM 작업이 느려지는 것을 개선 가능하다.
    - 또한 간단한 정적 페이지를 제작할 때는 Virtual DOM를 사용하지 않는 편이 더 나은 성능을 보이기도 한다.



# 작업 환경 설정

- Node.js

  - Nodejs란
    - 크롬 V8 자바스크립트 엔진으로 빌드한 자바스크립트 런타임(특정 언어로 만든 프로그램을 실행할 수 있는 환경)
    - 이를 통해 웹 브라우저 환경이 아닌 곳에서도 JS 사용이 가능해졌다.
  - React와 Node.js
    - React는 Node.js와 직접적인 연관은 없지만, 프로젝트를 개발하는데 필요한 주요 도구들이 Node.js를 사용한다.
    - babel: JS를 호환시켜준다.
    - webpack: 모듈화된 코드를 한 파일로 합치고(번들링), 코드를 수정할 때마다 웹 브라우저를 리로딩하는 등의 여러 기능을 지녔다.

  - npm
    - Node.js의 패키지 매니저 도구
    - 수 많은 개발자가 만든 패키지(재사용 가능한 코드)를 설치하고 설치한 패키지의 버전을 관리할 수 있다.



- yarn
  - npm 같은 패키지 관리 도구.
  - npm을 대체할 수 있는 도구로 npm보다 빠르고 효율적인 캐시 시스템과 부가기능을 제공한다.



- VScode 확장 프로그램
  - ESLint: JS 문법 및 코드 스타일 검사
  - Reactjs Code Snippets: 리액트 컴포넌트 및 라이프사이클 함수를 작성할 때 단축 단어를 사용하여 간편하게 코드를 자동으로 생성해 낼 수 있는 코드 스니펫 모음(charalampos karypidis가 업로드)
  - Prettier-Code formatter: 코드 스타일을 자동으로 정리
    - 코드 마지막의 세미 콜론, 따옴표 통일, 코드 정렬 등의 기능을 지원한다.
    - 윈도우 기준 `shift`+`alt`+`f`로 실행한다.
    - 커스텀이 가능하다.
    - 설정에서 format on save 옵션을 체크하면 저장할 때마다 자동으로 코드가 정리된다.



- 리액트 개발자 도구

  > https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=ko

  - 크롬 확장 프로그램
  - 브라우저에 나타난 리액트 컴포넌트를 심층 분석할 수 있도록 리액트 개발 팀이 제작



# 프로젝트 생성하기

- 아래 명령어를 입력하여 프로젝트를 생성한다.

  - create-react-app: babel, webpack 설치 및 설정 과정을 생략하고 간편하게 프로젝트 작업 환경을 구축해주는 도구.

  ```bash
  # yarn
  $ yarn create react-app <프로젝트명> 
  
  # npm
  $ npm init react-app <프로젝트명>
  ```



- 성공적으로 생성 되었는지 확인

  - 프로젝트 폴더로 이동하여 아래 명령어를 입력하여 실행한다.

  ```bash
  # yarn
  $ yarn start
  
  #npm
  $ npm start
  ```



- `node_modules`
  - 리액트 프로젝트를 생성하면 `node_modules` 폴더가 함께 생성된다.
    - 이 내부에 react 모듈도 설치되고, `import`를 통해 사용할 수 있게 된다.
  - 모듈을 불러와서 사용하는 것은 원래 브라우저에는 없는 기능으로 Node.js를 통해 가능하다.
    - 이러한 기능을 사용하기 위해서 번들러를 사용한다.
    - webpack등의 번들러를 통해 다양한 모듈을 하나의 JS파일로 만들 수 있다.
    - 브라우저에서도 가능하긴 하지만 이는 번들링이 아닌 단순히 해당 경로에 있는 JS파일을 불러오는 것이다.
  - webpack의 로더(loader)
    - `import`를 통해 이미지, css 등의 파일을 불러 오는 것은 webpack의 로더(loader)가 해준다.
    - css-loader: CSS 파일을 불러 온다.
    - file-loader: 웹 폰트나 미디어 파일 등을 불러 온다.
    - babel-loader: Js 파일을 불러오면서 최신 JS 문법으로 작성된 코드를 babel을 사용하여 ES5문법으로 변환한다.
    -  원래 직접 설치해야 하지만 `create react app` 명령어로 프로젝트를 생성하면 알아서 설치 된다.



# JSX

- JSX(Javascript XML): JS 코드 내에 HTML 태그를 넣는 방식으로 기존의 JS를 확장한 문법이다.
  - 기존 JS의 모든 기능을 포함하고 있다.
  - React를 꼭 JSX로 개발해야 하는 것은 아니지만, JSX로 개발하는 것이 권장된다.
  - 이벤트가 처리되는 방식, 시간에 따라 state가 변하는 방식, 화면에 표시하기 위해 데이터가 준비되는 방식 등 렌더링 로직이 본질적으로 다른 UI 로직과 연결되어 있기에 이러한 방식을 사용한다.
  - 마크업(HTML) 파일과 로직(JS)을 별도의 파일에 작성하여 기술을 인위적으로 분리하는 대신 둘 다 포함하는 컴포넌트라 부르는 느슨하게 연결된 유닛으로 관심사를 분리한다.
  - 자바스크립트 객체이다.



- JSX 형식으로 작성한 코드는 브라우저에서 실행되기 전에 코드가 번들링 되는 과정에서 바벨을 사용하여 일반 JS 형태의 코드로 변환된다.

  - 아래와 같은 코드가

  ```jsx
  function App(){
      return (
      	<div>
              Hello <b>react</b>
          </div>
      )
  }
  ```

  - 아래와 같이 변형된다.

  ```javascript
  function App(){
      return React.createElement("div",null,"Hello",React.createElement("b",null,"react"));
  }
  ```

  - 변형된 것과 같은 코드를 바로 입력해도 React 개발이 가능하다.
    - 그러나 매우 불편하기 때문에 JSX를 사용한다.



- index.js

  - `ReactDOM.render()`
    - 컴포넌트를 페이지에 렌더링하는 역할을 한다.
    - 첫 번째 파라미터로 렌더링할 내용을 JSX 형태로 받고, 두 번째 파라미터로 JSX를 렌더링할 document 내부 요소를 설정한다.
  - `React.StrictMode`
    - 리액트의 레거시 기능들을 사용하지 못하게 하는 기능이다.
    - 나중에는 사라지게 될 기능들을 사용했을 때 경고를 출력한다.

  ```react
  import React from 'react';
  import ReactDOM from 'react-dom';
  import './index.css';
  import App from './App';
  import reportWebVitals from './reportWebVitals';
  
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById('root')
  );
  
  reportWebVitals();
  ```





## JSX 문법

- JSX는 문자열도, HTML 태그도 아니다.
  - JSX는 HTML 보다는 JS에 가깝기 때문에 camelCase로 작성한다.
  - JSX 태그는 자식을 포함할 수 있다.



- JSX는 주입 공격을 방지한다.
  - React DOM은 JSX에 삽입된 모든 값을 렌더링하기 전에 **이스케이프**하므로, 애플리케이션에서 명시적으로 작성되지 않은 내용은 주입되지 않는다.
    - **이스케이프**: 값을 에러 없이 제대로 전달하기 위해 제어 문자로 인식될 수 있는 특정 문자 왼쪽에 슬래시를 붙이거나 URI(URL) 혹은 HTML 엔티티 등으로 인코딩하여 제어 문자(스크립트)가 아닌 일반 문자로 인식시켜 에러 또는 에러를 이용한 부정행위를 방지하는 것.
  - 즉, 모든 항목은 렌더링 되기 전에 문자열로 변환되므로 **XSS** 공격을 방지할 수 있다.
    - **XSS(cross-site scripting)**: 웹 사이트 관리자가 아닌 자가 웹 페이지에 악성 스크립트를 삽입할 수 있는 취약점



- 감싸인 요소

  - 컴포넌트에 여러 요소가 있다면 반드시 부모 요소 하나로 감싸야 한다.

  ```react
  function App() {
    return (
        <div>
            <h1>안녕! 리액트!</h1>
            <h2>잘 동작합니다!</h2>
        </div>
    );
  }
  
  export default App;
  ```

  - 아래와 같이 하나의 요소로 감싸지 않으면 오류가 발생한다.

  ```react
  function App() {
    return (
        <h1>안녕! 리액트!</h1>
        <h2>잘 동작하지 않습니다.</h2>
    );
  }
  
  export default App;
  ```

  - 하나의 요소로 감싸야 하는 이유
    - Virtual DOM은 하나의 DOM 트리 구조로 이루어져야 한다는 규칙 때문이다.
    - 이는 컴포넌트 변화를 감지해 낼 때 효율적으로 비교할 수 있도록 하기 위함이다.
  - `<div>`로 감싸고 싶지 않다면 `<Fragment>`로 감쌀 수 있다.
    - `<>`로 축약이 가능하다.

  ```react
  function App() {
    return (
        <>
            <h1>안녕! 리액트!</h1>
            <h2>잘 동작합니다!</h2>
        </>
    );
  }
  
  export default App;
  ```

  

- JavaScript 표현

  - JSX 내부에서 JS 표현식을 쓸 수 있다.

  - 코드를 `{}`로 감싸면 사용이 가능하다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    return (
      <>
        <h1>안녕! {name}!</h1>
        <h2>잘 동작합니다!</h2>
      </>
    );
  }
  
  export default App;
  ```



- if문 대신 조건부 연산자(삼항 연산자)

  - JSX 내부의 JS 표현식에서 if문은 사용 불가능하다.
  - 조건에 따라 다른 내용을 렌더링해야 할 때는 JSX 밖에서 if문을 사용하여 사전에 값을 설정하거나, `{}` 내부에 조건부 연산자를 사용하면 된다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    return (
      <>
        {name==='Cha' ? (
         <h1>참 입니다!</h1>
         ) : (
         <h1>거짓 입니다!</h1>
        )}
      </>
    );
  }
  
  export default App;
  ```

  

- AND 연산자(`&&`)를 사용한 조건부 렌더링

  - 특정 조건을 만족할 때 내용을 보여주고, 만족하지 않을 때 아무것도 렌더링 하지 않아야 하는 상황에서 사용한다.
    - `false && "참인 값"`이라는 표현식은 `참인 값`이라는 문자열을 반환하는 것 처럼 단축평가를 이용한 것이다. 
    - **React는 false를 렌더링 할 때는 null과 마찬가지로 아무것도 보여주지 않는다.**
    - 단, falsy한 값인 0은 예외적으로 화면에 나타난다.
  - 조건부 연산자를 사용해서도 구현 가능하다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    return (
      <div>{name==="Cha" ? <h1>보입니다!</h1> : null}</div>;
    );
  }
  
  export default App;
  ```

  - 하지만 AND 연산자를 사용하는 것이 훨씬 짧은 코드로 구현이 가능하다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    // 단축평가에 의해 <h1>보입니다!</h1>를 반환한다.
    return (
      <div>{name==="Cha" && <h1>보입니다!</h1>}</div>;
    );
  }
  
  export default App;
  ```



- undefined를 렌더링하지 않기

  - 리액트 컴포넌트에서 함수는 undefined를 반환하여 렌더링해선 안된다.

  ```react
  // 아래 코드는 error를 발생시킨다.
  import './App.css';
  
  function App() {
    const name = undefined;
    return name;
  }
  
  export default App;
  ```

  - 따라서 undefined를 반환할 수도 있으면 아래와 같이 OR 연산자(`||`)를 사용하여 에러를 방지해야 한다.
    - 단축평가를 이용한다.

  ```javascript
  // 아래 코드는 error를 발생시킨다.
  import './App.css';
  
  function App() {
    const name = undefined;
    return name || "값이 undefined 입니다!";
  }
  
  export default App;
  ```

  - 그러나 JSX 내부에서 undefined를 렌더링 하는 것은 괜찮다.

  ```react
  import './App.css';
  
  function App() {
    const name = undefined
    return (
      <div>{name}</div>
    );
  }
  
  export default App;
  ```



- 인라인 스타일링

  - 리액트에서 DOM 요소에 스타일을 적용할 때는 문자열 형태로 넣는 것이 아니라 객체 형태로 넣어 주어야 한다.
  - 스타일 이름 중에 `background-color`와 같이 `-`  문자가 포함되는 이름이 있다면 `-`를 없애고 camelCase로 작성해야 한다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    const style = {
        backgroundColor: 'green',
        color: 'pink',
        fontSize: '32px',
        fontWeight: 'bold',
        padding: 16
    }
    return (
      <div style={style}>{name}</div>
    );
  }
  
  export default App;
  ```

  - 위와 같이 스타일을 미리 선언하지 않고, 바로 지정하고 싶다면 아래와 같이 하면 된다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    return (
      <div style={{
        backgroundColor: 'green',
        color: 'pink',
        fontSize: '32px',
        fontWeight: 'bold',
        padding: 16
    }}>{name}</div>
    );
  }
  
  export default App;
  ```



- class 대신 className

  - 일반 HTML에서 class를 사용할 때는 `<div class="myclass">`와 같이 class 속성을 설정했다.
  - JSX에서는 class가 아닌 className으로 설정해야 한다.
    - 이전 버전에서는 class를 사용하면 오류가 발생했으나 최신 버전에서는 class를 사용해도 적용 된다.
    - 다만 경고문을 띄운다.

  ```css
  /*CSS 파일 작성*/
  .react {
    background-color: green;
    color: pink;
    font-size: 32px;
    font-weight: bold;
    padding: 16;
  }
  ```

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    return (
      <div className="react">{name}</div>
    );
  }
  
  export default App;
  ```

  

- 태그는 꼭 닫아야 한다.

  - 일반 HTML에서는 `<input>`, `<br>` 등의 태그는 꼭 닫는 태그 표시를 해주지 않아도 되었다.
  - JSX는 모든 태그에 반드시 닫는 태그를 작성해 줘야한다.
    - 태그 사이에 별도의 내용이 들어가지 않는 경우 **self-closing** 태그를 사용할 수 있다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    return (
      <>
        <div className="react">{name}</div>
        <input />
      </>
    );
  }
  
  export default App;
  ```



- 주석

  - JSX 내부에서 주석을 작성할 때는 `{/**/}`와 같은 형식으로 작성한다.
  - 여는 태그를 여러 줄로 작성할 때는 그 내부에서 `//`와 같은 형태의 주석도 작성 가능하다.
  - `//`, `/**/`와 같은 일반 JS 주석은 화면에 그대로 나타난다.

  ```react
  import './App.css';
  
  function App() {
    const name = 'Cha'
    return (
      <>
        {/* 주석입니다. */}
        <div className="react">{name}</div>
        <input />
        <div>
            {/* 화면에 나타나지 않는다. */}
            /* 화면에 나타난다. */
            // 화면에 그대로 나타난다.
        </div>
      </>
    );
  }
  
  export default App;
  ```

  



