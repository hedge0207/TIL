# React란

- React
  - 프론트엔드 개발 도구
  - 페이스북에서 개발
  - Vue, Angular에 비해 월등히 높은 사용량



- 리액트는 라이브러리인가 프레임워크인가
  - Vue는 스스로 Framework이라고 소개한다.
  - React는 스스로 Library라고 소개한다.



- 리액트는 왜 만들었는가
  - 시간이 지나면서 변화하는 데이터를 표현하는 재사용 가능한 UI 컴포넌트를 만들기 위해서
  - UI 컴포넌트



- 리액트를 학습하는 방법
  - 리액트 공식 문서에서 제공하는 자습서를 참고
  - 리액트 공식 문서에서 제공하는 문서 카테고리를 참고



- 리액트의 Lifecycle
  - Mounting
    - 생성하는 단계
    - 렌더링(화면을 그리는) 단계
  - Updating
    - rerender 단계
    - props나 state가 변경되었을 때 다시 랜더링 한다.
  - Unmounting
    - 종료 단계



- 추가 학습 자료
  - Awesome React(https://github.com/enaqx/awesome-react)
  - Awesome React Components(https://github.com/brillout/awesome-react-components)
  - Awesome React Talks(https://github.com/tiaanduplessis/awesome-react-talks)





# JSX 소개

- JSX(Javascript XML): JS 코드 내에 HTML 태그를 넣는 방식으로 기존의 JS를 확장한 문법이다.
  - 기존 JS의 모든 기능을 포함하고 있다.
  - React를 꼭 JSX로 개발해야 하는 것은 아니지만, JSX로 개발하는 것이 권장된다.
  - 이벤트가 처리되는 방식, 시간에 따라 state가 변하는 방식, 화면에 표시하기 위해 데이터가 준비되는 방식 등 렌더링 로직이 본질적으로 다른 UI 로직과 연결되어 있기에 이러한 방식을 사용한다.
  - 마크업(HTML) 파일과 로직(JS)을 별도의 파일에 작성하여 기술을 인위적으로 분리하는 대신 둘 다 포함하는 컴포넌트라 부르는 느슨하게 연결된 유닛으로 관심사를 분리한다.



- 기초

  - JSX은 문자열도, HTML 태그도 아니다.
  - JSX는 HTML 보다는 JS에 가깝기 때문에 camelCase로 작성한다.
  - JSX에서는 `{}`안에 유효한 JavaScript 표현식을 넣을 수 있다.

  - JSX 태그는 자식을 포함할 수 있다.

  ```react
  function formatName(user){
    return user.firstName + ' ' + user.lastName;
  }
  
  const name = 'Cha';
  const user = {
    firstName: "GilDong",
    lastName: "Hong"
  };
  
  const element = (
    <div>		<!--<div>태그는 자식 태그들을 포함하고 있다.-->
      <h1>Hello! {name}</h1>  <!--{}안에 name이라는 변수를 비롯한 다양한 표현식(함수까지도)을 사용할 수 있다.-->
      <h1>2+2 = {2+2}</h1>
      <h1>Hello, {formatName(user)}</h1>
    </div>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - JSX는 주입 공격을 방지한다.
    - React DOM은 JSX에 삽입된 모든 값을 렌더링하기 전에 **이스케이프**하므로, 애플리케이션에서 명시적으로 작성되지 않은 내용은 주입되지 않는다.
    - **이스케이프**: 값을 에러 없이 제대로 전달하기 위해 제어 문자로 인식될 수 있는 특정 문자 왼쪽에 슬래시를 붙이거나 URI(URL) 혹은 HTML 엔티티 등으로 인코딩하여 제어 문자(스크립트)가 아닌 일반 문자로 인식시켜 에러 또는 에러를 이용한 부정행위를 방지하는 것.
    - 즉, 모든 항목은 렌더링 되기 전에 문자열로 변환되므로 **XSS** 공격을 방지할 수 있다.
    - **XSS(cross-site scripting)**: 웹 사이트 관리자가 아닌 자가 웹 페이지에 악성 스크립트를 삽입할 수 있는 취약점
  - JSX는 객체를 표현한다.
    - babel은 JSX를 `React.createElement()` 호출로 컴파일한다.
    - 아래 두 코드는 동일한 코드다.

  ```react
  const element = (
    <h1 className="greeting">
      Hello, world!
    </h1>
  );
  
  const element = React.createElement(
    'h1',
    {className: 'greeting'},
    'Hello, world!'
  );
  ```

  



- JSX도 하나의 표현식이다.

  - 변수에 할당할 수 있다.

  ```react
  const jsxVariable = <h1>JSX는 변수에 할당 가능합니다.</h1>;
  
  
  const element = (
    <h1>{jsxVariable}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - 인자로 받을 수 있다.

  ```react
  function getJsxParameter(jsx){
    return <div>{jsx} 를 인자로 받았습니다.</div>
  }
  
  const jsxVariable = <span>JSX는 변수에 할당 가능합니다.</span>;
  
  const element = (
    <h1>{getJsxParameter(jsxVariable)}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - 함수로 반환할 수 있다.

  ```react
  function returnJsx(){
    return <div>JSX를 반환합니다</div>
  }
  
  const element = (
    <h1>{returnJsx()}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  - if 구문 및 반복문 등에 사용 할 수 있다.

  ```react
  function useJsx(){
    if(jsxVariable){
      return "참인 조건입니다.";
    }else{
      return "거짓은 조건입니다.";
    }
  }
  
  const jsxVariable = <span>JSX는 변수에 할당 가능합니다.</span>
  
  
  const element = (
    <h1>{useJsx()}</h1>
  );
  
  ReactDOM.render(
    element,
    document.getElementById('root')
  );
  ```

  

- JSX 속성 정의

  - 속성에 따옴표를 이용해 문자열 리터럴을 정의할 수 있다.

  ```react
  const element = <div tabIndex="0"></div>;
  ```

  - 중괄호를 사용하여 어트리뷰트에 JS 표현식을 삽입할 수도 있다.
    - 어트리뷰트에 JS 표현식을 사용할 때 중괄호 주변에 따옴표를 입력해선 안된다. 
    - 따옴표 또는 중괄호 중 하나만 사용하고, 동일한 어트리뷰트에 두 가지를 동시에 사용해선 안된다.

  ```react
  const element = <img src={user.avatarUrl}></img>;
  ```

  



























