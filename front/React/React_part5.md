# 컴포넌트 내부의 반복

- 웹 어플리케이션을 만들다보면  반복되는 내용을 보여줘야 할 경우가 있다.

  - 반복이 늘어날 수록 코드 양은 증가하고 파일 용량도 증가할 것이다.
  - 또한 보여 주어야 할 데이터가 유동적이라면 관리하기도 힘들다.
    - 아래의 경우 `<li>코코아</li>`의 내용을 변경해야 한다면 반복되는 `<li>`태그 중에서 해당 내용을 찾아야 한다.

  ```react
  import React from "react";
  
  const IterationSample = () => {
    return (
      <div>
        <ui>
          <li>겨울</li>
          <li>눈</li>
          <li>코코아</li>
          <li>눈사람</li>
        </ui>
      </div>
    );
  };
  
  export default IterationSample;
  ```



- JS의 `map()`함수를 사용하여 위와 같은 문제를 해결 가능하다.
  - `arr.map(callback, [thisArg])`
    - `callback`은 원본 배열을 가지고 새로운 배열을 생성하는 함수로, `currentValue`(현재 처리하고 있는 요소), `index`(현재 처리하고 있는 요소의 index 값), `array`(현재 처리하고 있는 원본 배열)를 인자로 받는다.
    - `thisArg`는 옵션으로 callback함수 내에서 사용할 this 레퍼런스를 받는다.
  - 이를 활용하여 컴포넌트 내부의 반복된 코드를 축약해 작성할 수 있다.



- React에 적용

  - `map()` 함수에서 JSX를 작성하여 사용한다.
  - 아래 코드를 실행하면 정상적으로 동작은 하지만 콘솔 창을 열어보면 아래와 같은 경고가 뜬다.
    - `Warning: Each child in a list should have a unique "key" prop.`
    - key 값을 설정해 줘야 한다.

  ```react
  import React from "react";
  
  const IterationSample = () => {
    const keywords = ["겨울", "눈", "코코아", "눈사람"];
    const keywordList = keywords.map((k) => <li>{k}</li>);
    return (
      <div>
        <ul>{keywordList}</ul>
      </div>
    );
  };
  
  export default IterationSample;
  ```



- key

  - 리액트에서 key는 컴포넌트 배열을 렌더링했을 때 어떤 원소에 변동이 있었는지 알아내려고 사용한다.
    - 예를 들어 유동적인 데이터를 다룰 때는 원소를 생성, 제거, 수정할 수 있는데 key가 없을 때는 Virtual DOM을 비교하는 과정에서 리스트를 순차적으로 비교하면서 변화를 감지한다.
    - key가 있다면 어디서 변화가 일어났는지 더욱 빠르게 알아낼 수 있다.
  - key 설정하기
    - key 값을 설정할 때는 `map()` 함수의 인자로 전달되는 callback 함수 내부에서 설정하면 된다.
    - key 값은 언제나 유일해야 한다.
    - 아래 예시에서는 index 값을 key로 사용하였는데 사실 리렌더링할 때 index 값은 key로 적절하지는 않다.

  ```react
  import React from "react";
  
  const IterationSample = () => {
    const keywords = ["겨울", "눈", "코코아", "눈사람"];
    // index는 유일한 값이므로 key로 설정
    const keywordList = keywords.map((k, index) => <li key={index}>{k}</li>);
    return (
      <div>
        <ul>{keywordList}</ul>
      </div>
    );
  };
  
  export default IterationSample;
  ```

  

- 동적인 배열 렌더링하기

  - 데이터를 변경할 때는 배열에 직접 접근하여 수정하는 것이 아니라 배열의 복제본을 만든 뒤 이를 새로운 상태(state)로 설정해줘야 한다.
    - 리액트에서 상태를 변경할 때는 기존 상태를 그대로 두면서 새로운 값을 상태로 설정해야 한다.
    - 이를 **불변성 유지**라 하는데 불변성 유지가 이루어져야 리액트 컴포넌트의 성능을 최적화 할 수 있다.
  - 데이터 추가하기
    - 아래에서 배열에 데이터를 추가할 때 `push()`가 아닌 `concat()`을 사용했는데 이는 `push()`는 기존 배열 자체를 변경하지만 `concat()`은 새로운 배열을 만들어 준다는 차이가 있다.
    - 불변성 유지를 위해 `concat()`을 사용한다.

  ```react
  import React, { useState } from "react";
  
  const IterationSample = () => {
    const [keywords, setKeywords] = useState([
      { id: 1, keyword: "겨울" },
      { id: 2, keyword: "눈" },
      { id: 3, keyword: "코코아" },
      { id: 4, keyword: "눈사람" },
    ]);
    const [inputText, setInputText] = useState("");
    const [nextId, setNextId] = useState(5);
  
    const onChange = (e) => setInputText(e.target.value);
  
    const onClick = () => {
      // concat을 사용한다.
      const nextKeywords = keywords.concat({
        id: nextId,
        keyword: inputText,
      });
      setNextId(nextId + 1);
      setKeywords(nextKeywords);
      setInputText("");
    };
  
    const keywordList = keywords.map((k) => <li key={k.id}>{k.keyword}</li>);
    return (
      <div>
        <input value={inputText} onChange={onChange} />
        <button onClick={onClick}>추가</button>
        <ul>{keywordList}</ul>
      </div>
    );
  };
  
  export default IterationSample;
  ```
  
  - 데이터 제거하기
    - 불변성을 유지하면서 배열의 특정 항목을 지우기 위해 `filter()` 함수를 사용한다.
  
  ```react
  import React, { useState } from "react";
  
  const IterationSample = () => {
      const [keywords, setKeywords] = useState([
          { id: 1, keyword: "겨울" },
          { id: 2, keyword: "눈" },
          { id: 3, keyword: "코코아" },
          { id: 4, keyword: "눈사람" },
      ]);
  
      const onRemove = (id) => {
          const nextKeywords = keywords.filter((k) => k.id !== id);
          setKeywords(nextKeywords);
      };
  
      const keywordList = keywords.map((k) => (
          <li
              key={k.id}
              onDoubleClick={() => {
                  onRemove(k.id);
              }}
              >
              {k.keyword}
          </li>
      ));
      return (
          <div>
              <ul>{keywordList}</ul>
          </div>
      );
  };
  
  export default IterationSample;
  ```








# 컴포넌트 스타일링

- 리액트에서 컴포넌트를 스타일링 할 때는 다양한 방식을 사용 가능하다.
  - 일반CSS: 컴포넌트를 스타일링 하는 가장 기본적인 방식
  - Sass: 자주 사용되는 CSS 전처리기 중 하나로, 확장된 CSS 문법을 사용하여 CSS 코드를 더욱 쉽게 작성할 수 있도록 해준다.
  - CSS Module: 스타일을 작성할 때 CSS 클래스가 다른 CSS 클래스의 이름과 절대 충돌하지 않도록 파일마다 고유한 이름을 자동으로 생성해준다.
  - styled-components: 스타일을 JS파일에 내장시키는 방식으로 스타일을 작성함과 동시에 해당 스타일이 적용된 컴포넌트를 만들 수 있게 해준다.



## 일반 CSS

- 아래의 경우 일반 CSS를 계속 사용해도 무관하다.
  - 소규모 프로젝트를 진행.
  - 기존의 CSS 스타일링이 딱히 불편하지 않다고 생각.



- CSS를 작성할 때 가장 중요한 점은 CSS 클래스를 중복되지 않게 만드는 것이다.
  - 이름을 지을 때 특별한 규칙을 사용하여 짓는다.
    - 대표적으로 BEM 네이밍이 있다.
    - BEM 네이밍은 CSS 방법론 중 하나로, 이름을 지을 때 일종의 규칙을 준수하여 해당 클래스가 어디에서 어떤 용도로 사용되는지 명확하게 작성하는 방식이다.
    - `.card_title-primary`
    - 혹은 `컴포넌트명-클래스` 형식으로 짓는 방법도 있다.
  - CSS Selector를 활용한다.
    - CSS 셀렉터를 활용하면 CSS 클래스가 특정 클래스 내부에 있는 경우에만 스타일을 적용할 수 있다.
    - 예를 들어 `.App` 내부의 `.logo` 스타일을 적용하고자 한다면 아래와 같이 하면 된다.
    - `.App .logo {height: 40px}`
    - 태그에 직접 지정하고자 할 때는 아래와 같이 `.`을 생략하면 된다.
    - `.App header {height: 40px}`



## Sass 사용하기

- Sass(Syntactically Awesome Style Sheets)

  - CSS 전처리기

    - 복잡한 작업을 쉽게 할 수 있도록 해준다. 
    - 스타일 코드의 재활용성을 높여준다. 
    - 코드의 가독성을 높여 유지보수를 쉽게 해준다.

  - create-react-app 구버전에서는 Sass를 사용하려면 추가 작업이 필요했으나 v2 버전부터는 별도의 추가 설정 없이 사용 가능하다.

  - `.scss`와 `.sass`를 지원한다.

    - 둘의 문법은 상당히 다르다.
    - `.sass`는 중괄호와 세미콜론을 사용하지 않는다.
    - 주로 CSS와 크게 다르지 않은 `.scss`가 많이 사용된다.

  ```scss
  // .sass
  $font-stack:Helvetica, sans-serif
  $primary-color:#333
  
  body
      font: 100% $font-stack
      color: $primary-color
  
      
  // .scss
  $font-stack:Helvetica, sans-serif;
  $primary-color:#333;
  
  body{
      font: 100% $font-stack;
      color: $primary-color;
  }
  ```





- Sass 사용하기

  - 설치하기

  ```bash
  $ yarn add node-sass
  ```

  - Sass의 기능
    - 스타일링 값을 변수처럼 사용 가능.
    - 재사용 되는 스타일 블록을 함수처럼 사용할 수 있는 믹스인이 존재.
    - 컴포넌트별로 적용되게 하는 기능

  ```scss
  // 변수 사용하기
  $red: #fa5252;
  $orange: #fd7e14;
  $yellow: #fcc419;
  $green: #40c057;
  $blue: #339af0;
  $indigo: #5c7cfa;
  $violet: #7950f2;
  
  // 믹스인 만들기
  @mixin squre($size) {
    $calculated: 32px * $size;
    width: $calculated;
    height: $calculated;
  }
  
  .SassComponent {
    display: flex;
    background: $oc-gray-2;
    @include media("<768px") {
      background: $oc-gray-9;
    }
    .box {
      background: red; // 일반 CSS 에선 .SassComponent .box 와 마찬가지
      cursor: pointer;
      transition: all 0.3s ease-in;
      &.red {
        // .red 클래스가 .box 와 함께 사용 됐을 때
        background: $red;
        @include square(1);
      }
      &.orange {
        background: $orange;
        @include square(2);
      }
      &.yellow {
        background: $yellow;
        @include square(3);
      }
      &.green {
        background: $green;
        @include square(4);
      }
      &.blue {
        background: $blue;
        @include square(5);
      }
      &.indigo {
        background: $indigo;
        @include square(6);
      }
      &.violet {
        background: $violet;
        @include square(7);
      }
      &:hover {
        // .box 에 마우스 올렸을 때
        background: black;
      }
    }
  }
  ```

  - 적용하기
    - 완료된 후 개발 서버를 재시작해야 적용된다.

  ```react
  import React from "react";
  import "./SassComponent.scss";
  
  const SassComponent = () => {
    return (
      <div className="SassComponent">
        <div className="box red" />
        <div className="box orange" />
        <div className="box yellow" />
        <div className="box green" />
        <div className="box blue" />
        <div className="box indigo" />
        <div className="box violet" />
      </div>
    );
  };
  
  export default SassComponent;
  ```

  

- utils 함수 분리하기

  - 여러 파일에서 사용될 수 있는 Sass 변수 및 믹스인은 다른 파일로 따로 분리하여 작성한 뒤 필요 한 곳에서 불러와 재사용이 가능하다.
  - `src/styles` 내부에 scss 파일 생성 후, 기존에 선언한 변수와 믹스인을 옮긴다.

  ```scss
  // 변수 사용하기
  $red: #fa5252;
  $orange: #fd7e14;
  $yellow: #fcc419;
  $green: #40c057;
  $blue: #339af0;
  $indigo: #5c7cfa;
  $violet: #7950f2;
  
  // 믹스인 만들기
  @mixin square($size) {
    $calculated: 32px * $size;
    width: $calculated;
    height: $calculated;
  }
  ```

  - 이제 기존의 scss 파일에서 변수와 믹스인을 가져와서 사용한다.
    - 기존과 동일한 결과가 나오는 것을 확인 가능하다.

  ```scss
  @import "./styles/utils";
  
  .SassComponent {
    (...)
  }
  ```



- sass-loader 설정 커스터마이징하기

  - 프로젝트 디렉터리 구조가 깊어지면 `@import` 할 때 `../../../../styles/utils`와 같이 한참 거슬러 올라가야 한다는 문제가 있다.
  - sass-lodaer를 사용하면 이러한 문제를 해결 가능하다.
    - 반드시 해야 하는 것은 아니지만 해 두면 유용하다.
  - 설정 정보 꺼내기
    - create-react-app으로 만든 프로젝트는 프로젝트 구조의 복잡도를 낮추기 위해 세부 설정이 모두 숨겨져 있다.
    - sass-loader도 숨겨져 있으므로 아래 명령어로 꺼내 줘야 한다.
    - 단, yarn eject는 아직 git에 커밋하지 않은 변화가 있다면 진행이 안되므로 먼저 커밋을 해줘야 한다.
    - 아래 명령의 결과로 config 폴더가 생성된다.

  ```bash
  $ yarn eject
  ```

  - `webpack.config.js`에서 `sassRegex` 키워드를 찾으면 아래와 같은 코드가 나온다.

  ```javascript
  {
    test: sassRegex,
    exclude: sassModuleRegex,
    use: getStyleLoaders({
      importLoaders: 3,
      sourceMap: isEnvProduction && shouldUseSourceMap
    },
    'sass-loader'
    ),
   sideEffects: true
  },
  ```

  - 'sass-loader' 부분을 지우고 아래와 같이 뒷 부분에 `concat`을 통해 커스터마이징된 sass-loader를 넣어준다.

  ```javascript
  {
    test: sassRegex,
    exclude: sassModuleRegex,
    use: getStyleLoaders({
      importLoaders: 3,
      sourceMap: isEnvProduction && shouldUseSourceMap
    }).concat({
      loader: require.resolve('sass-loader'),
      options: {
        sassOptions: {
          includePaths: [paths.appSrc + '/styles']
        },
        sourceMap: isEnvProduction && shouldUseSourceMap,
        }
     }),
   sideEffects: true
  },
  ```

  - 이후 서버를 재시작하면 절대 경로 사용이 가능해진다.
    - 만일 yarn eject이후 개발 서버가 제대로 동작하지 않는 현상이 발생한다면 프로젝트 디렉터리의 `node_modules`를 삭제하고 `yarn install` 명령어를 실행하면 된다.

  ```scss
  @import 'utils.scss'
  ```

  - 만일 `@import`조차 쓰기 싫다면 아래와 같이 하면 된다.
    - 이제 `@import`를 쓰지 않아도 모든 scss 파일 내에서 자동으로 `utils.scss`를 불러오게 된다.

  ```javascript
  {
    test: sassRegex,
    exclude: sassModuleRegex,
    use: getStyleLoaders({
      importLoaders: 3,
      sourceMap: isEnvProduction && shouldUseSourceMap
    }).concat({
      loader: require.resolve('sass-loader'),
      options: {
        sassOptions: {
          includePaths: [paths.appSrc + '/styles']
        },
        sourceMap: isEnvProduction && shouldUseSourceMap,
        // 아래와 같이 추가해준다.
        prependData: `@import 'utils';`
        }
     }),
   sideEffects: true
  },
  ```

  

- `node_modules`에서 라이브러리 불러오기

  - Sass의 장점 중 하나는 라이브러리를 쉽게 불러와서 사용할 수 있다는 점이다.
    - `yarn`을 통해 설치한 라이브러리를 사용하는 가장 기본적인 방법은 다음과 같이 상대 경로를 사용하여 `node_modules`까지 들어가는 것이다. 
    - `@import '../../../node_modules/libarary/styles';`
    - `~` 문자를 사용하면 `node_modules`에서 라이브러리 디렉터리를 참조하여 스타일을 불러올 수  있다.
    - `@import '~/library/style';`

  - 라이브러리 설치하기
    - open-color: 편리한 색상 팔레트 라이브러리.
    - include-media: 반응형 디자인을 쉽게 만들어주는 라이브러리.

  ```bash
  $ yarn add open-color include-media
  ```

  - 불러오기

  ```scss
  // utills.sscss
  @import "~include-media/dist/include-media";
  @import "~open-color/open-color";
  ```

  - 사용하기

  ```scss
  .SassComponent {
    display: flex;
    background: $oc-gray-2;
    @include media('<768px') {  // 화면 가로 크기가 768px 미만이면 배경색이 어둡게 되도록 설정
      background: $oc-gray-9;
    }
    (...)
  }
  ```

  

## CSS Module

- CSS Module

  - CSS를 불러와서 사용할 때 클래스 이름을 고유한 값, 즉 `[파일이름]_[클래스이름]_[해시값]` 형태로 자동으로 만들어 컴포넌트 스타일 클래스 이름이 중첩되는 현상을 방지해주는 기술
  - 구버전의 create-app-react에서는 웹팩에서 css-loader 설정을 별도로 해주어야 했지만 v2 이상부터는 따로 설정할 필요가 없어졌다.
  - `.module.css` 확장자로 파일을 저장하기만 하면 된다.
    - 만약 글로벌 CSS를 작성하고 싶다면 `:global`을 앞에 입력해주면 된다.

  ```css
  /* 자동으로 고유한 이름을 갖게 되므로 흔히 사용되는 단어를 사용해도 된다. */
  .wrapper {
    background: black;
    padding: 1rem;
    color: white;
    font-size: 2rem;
  }
  
  .inverted {
    color: black;
    background: white;
    border: 1px solid black;
  }
  
  :global .something {
    font-weight: 800;
    color: aqua;
  }
  
  ```

  - 적용하기
    - CSS Module이 적용된 스타일 파일을 불러오면 객체를 하나 전달받게 되는데 CSS Module에서 사용한 클래스 이름과 해당 이름을 고유화 한 값이 `키:값` 형태로 들어있다.
    - 고유한 클래스 이름을 사용하려면 적용하고자 하는 JSX 엘리먼트에 `className={styles.클래스이름}` 형태로 전달해주면 된다.
    - `:global`을 사용하여 전역으로 선언한 클래스는 평범한 클래스와 동일하게 그냥 문자열로 넣으면 된다.

  ```react
  import React from "react";
  import styles from "./CSSModule.module.css";
  
  console.log(styles) // {wrppaer: "CSSModule_wrppaer__1n4OD"}, 파일이름_클래스이름_해시값
  const CSSModule = () => {
    return (
      <div className={styles.wrapper}>
        안녕하세요, 저는 <span className="something">CSS Module 입니다!</span>
      </div>
    );
  };
  
  export default CSSModule;
  ```

  - 복수의 클래스를 적용할 때는 아래와 같이 하면 된다.
    - 템플릿 리터럴을 사용하여 문자열을 합해준다.
    - 혹은 `join()`을 사용할 수도 있다.

  ```react
  import React from "react";
  import styles from "./CSSModule.module.css";
  
  console.log(styles);
  const CSSModule = () => {
    return (
      {/* <div className={[styles.wrapper, styles.inverted].join(' ')}> */}
      <div className={`${styles.wrapper} ${styles.inverted}`}>
        안녕하세요, 저는 <span className="something">CSS Module 입니다!</span>
      </div>
    );
  };
  
  export default CSSModule;
  ```



- classnames

  - CSS 클래스를 조건부로 설정할 때 유용한 라이브러리
    - CSS Module을 사용할 때 이 라이브러리를 사용하면 여러 클래스를 적용할 때 매우 편리하다.

  - 설치

  ```bash
  $ yarn add classnames
  ```

  - 기본적인 사용법

  ```javascript
  import classNames from "classnames";
  
  classNames("one", "two");               // one two
  classNames("one", { two: true });       // one two
  classNames("one", { two: false });      // one
  classNames("one", ["two", "three"]);    // one two three
  
  const myClass = "Hello";
  classNames("one", myClass); 			// one Hello
  ```

  - props 값에 따라 다른 스타일 주기
    - 아래와 같이 `highlited`의 값이 true면 `highlited` 클래스가 적용되고, false면 적용되지 않게 하는 것이 가능하다.

  ```react
  const MyComponent = ({highlited, theme}) => (
      <div className={classNames('MyComponent', {highlited}, theme)}>Hello!</div>
  )
  ```

  - 만일 classnames를 사용하지 않으면 아래와 같이 작성해야 한다.

  ```react
  const MyComponent = ({highlited, theme}) => (
      <div className={`MyComponent ${theme} ${highlited ? 'highlited' : ''}`}>Hello!</div>
  )
  ```

  - CSS Module을 사용하는 것도 훨씬 쉬워진다.
    - classnames의 내장함수 `bind()`를 사용하면 클래스를 넣어줄 때마다 `style.클래스이름` 형태를 사용하지 않아도 된다.
    - 사전에 미리 styles에서 받아 온 후 사용하게끔 설정해두고 `('클래스이름', '클래스이름')` 형태로 사용 가능하다.

  ```react
  import React from "react";
  // classnames/bind 에서 import
  import classNames from "classnames/bind";
  import styles from "./CSSModule.module.css";
  
  // 미리 styles를 받아오고
  const cx = classNames.bind(styles);
  
  const CSSModule = () => {
    return (
      <div className={cx("wrapper", "inverted")}>
        안녕하세요, 저는 <span className="something">CSS Module 입니다!</span>
      </div>
    );
  };
  
  export default CSSModule;
  ```



- Sass와 함께 사용하기

  - Sass를 사용할 때도 파일 이름 뒤에 `module.scss` 확장자를 사용하면 CSS Module로 사용할 수 있다.

  ```react
  .wrapper {
    background: black;
    padding: 1rem;
    color: white;
    font-size: 2rem;
    &.inverted {
      // inverted 가 .wrapper 와 함께 사용 됐을 때만 적용
      color: black;
      background: white;
      border: 1px solid black;
    }
  }
  
  /* 글로벌 CSS 를 작성하고 싶다면 */
  :global {
    // :global {} 로 감싸기
    .something {
      font-weight: 800;
      color: aqua;
    }
  }
  ```



- CSS Module이 아닌 파일에서 CSS Module 사용하기

  - CSS Module에서 `:global`을 통해 글로벌 클래스를 정의한 것처럼 일반 `.css`, `scss` 파일에서도 로컬 클래스를 정의 가능하다.
  - `:local`을 사용하면 된다.

  ```css
  /* CSS */
  :local .wrapper{
      /*지정할 스타일*/
  }
  ```

  ```scss
  /* Sass */
  :local{
      .wrapper{
          /*지정할 스타일*/
      }
  }
  ```



## styled-components

- JS 파일 안에 스타일을 선언하는 방식
  - 이 방식을 `CSS-in-JS`라 부른다.
  - `CSS-in-JS` 라이브러리 중 개발자들이 가장 선호하는 것이 `styled-components`이다.
  - 가장 큰 장점 중 하나는 props 값으로 전달해 주는 값을 쉽게 스타일에 적용할 수 있다는 것이다.



- 사용하기

  - 설치

  ```bash
  $ yarn add styled-components
  ```

  - 사용
    - 아래와 같이 특정 태그에 사용할 때는 `styled.태그명`으로 사용한다.
    - 특정 컴포넌트에 사용할 때는 `styled(컴포넌트명)`으로 사용한다.

  ```react
  import React from "react";
  import styled, { css } from "styled-components";
  
  const Box = styled.div`
    background: ${(props) => props.color || "blue"};
    padding: 1rem;
    display: flex;
  `;
  
  const Button = styled.button`
    background: white;
    color: black;
    border-radius: 4px;
    padding: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    font-size: 1rem;
    font-weight: 600;
  
    /* & 문자를 사용하여 Sass 처럼 자기 자신 선택 가능 */
    &:hover {
      background: rgba(255, 255, 255, 0.9);
    }
  
    /* 다음 코드는 inverted 값이 true 일 때 특정 스타일을 부여해준다. */
    ${(props) =>
      props.inverted &&
      css`
        background: none;
        border: 2px solid white;
        color: white;
        &:hover {
          background: white;
          color: black;
        }
      `};
    & + button {
      margin-left: 1rem;
    }
  `;
  
  const StyledComponent = () => (
    <Box color="black">
      <Button>안녕하세요</Button>
      <Button inverted={true}>테두리만</Button>
    </Box>
  );
  
  export default StyledComponent;
  ```

  

- Tagged 템플릿 리터럴

  - 앞의 예시를 보면 백틱을 사용하여 만든 문자열에 스타일을 넣어주었다.
    - 여기서 사용한 문법을 Tagged 템플릿 리터럴이라 부른다.

  - 일반 템플릿 리털과 다른 점은 템플릿 안에 JS 객체나 함수를 전달할 때 온전히 추출할 수 있다는 것이다.
    - `styled-components`는 이러한 특성을 사용하여 `styled-components`로 만든 컴포넌트의 props를 스타일 쪽에서 쉽게 조화할 수 있도록 해준다.

  ```javascript
  // 일반 템플릿 리터럴
  // 객체는 [object Object]로 변환되고, 함수는 그대로 문자열화 된다.
  `hello ${{foo:'bar'}} ${()=>'world'}!`  // hello [object Object] () => 'world'!
  
  
  // 다음과 같은 함수를 작성하고 나서 해당 함수 뒤에 템플릿 리터럴을 넣어준다면 템플릿 안에 넣은 값을 온전히 추출 가능하다.
  function tagged(...args){
      console.log(args)
  }
  tagged`hello ${{foo:'bar'}} ${()=>'world'}!`
  // 아래와 같이 템플릿 사이사이에 들어가는 JS 객체나 함수의 원본 값을 그대로 추출 가능하다.
  /*
  (3) [Array(3), {…}, ƒ]
      0: (3) ["hello ", " ", "!", raw: Array(3)]
      1: {foo: "bar"}
      2: ()=>'world'
  */
  ```



- 스타일링된 엘리먼트 만들기

  - `styled-components`를 사용하여 스타일링된 엘리먼트를 만들 때는 컴포넌트 파일의 상단에서 `styled`를 불러와야 한다.
  - 이후 `styled.태그명`을 사용하여 구현한다.
    - 아래와 같이 `styled.div` 뒤에 Tagged 템플릿 리터럴 문법을 통해 스타일을 넣어 주면, 해당 스타일이 적용된 div로 이루어진 리액트 컴포넌트가 생성된다.

  ```react
  import styled from 'styled-components'
  
  const MyComponent = styled.div`
    font-size: 2rem;
  `;
  ```

  - 사용해야 할 태그명이 유동적이거나 특정 컴포넌트 자체에 스타일링해 주고 싶다면 다음과 같은 형태로 구현할 수 있습니다.
    - 태그의 타입을 `styled` 함수의 인자로 전달
    - 컴포넌트 형식의 값을 넣어준다.
    - 단, 컴포넌트 형식의 값을 넣어주는 경우 해당 컴포넌트에 className props를 최상위 DOM(아래의 경우 div 태그)의 className으로 설정하는 작업이 필요하다.

  ```react
  // 태그의 타입을 `styled` 함수의 인자로 전달
  const MyInput = styled('input')`
    background: gray;
  `
  
  // 아예 컴포넌트 형식의 값을 넣어준다.
  // 단, 이 경우 해당 컴포넌트에 className props를 최상위 DOM(아래의 경우 div 태그)의 className으로 설정하는 작업이 필요하다.
  const Sample = ({ className }) => {
      return <div className={className}>sample</div>
  }
  const StyledLink = styled(Sample)`
    color: blue;
  `
  ```



- 스타일에서 props 조회하기

  - `styled-components`를 사용하려면 스타일 쪽에서 컴포넌트에게 전달된 props 값을 참조할 수 있다.

  ```react
  const Box = styled.div`
    /* 아래와 같이 props를 조회해서 props.color를 사용할 수 있다. */
    background: ${(props) => props.color || "blue"};
    padding: 1rem;
    display: flex;
  `;
  ```

  - 위와 같이 만들어진 코드는 JSX에서 사용될 때 다음과 같이 color 값을 props로 넣어줄 수 있다.

  ```react
  <Box color="black">(...)</Box>
  ```

  

- props에 따른 조건부 스타일링

  - `styled-components`에서는 조건부 스타일링을 간단하게 props로 처리할 수 있다.
    - 아래와 같이 여러 줄을 props에 따라 넣어 주어야 할 때는 `css`를 `styled-components`에서 불러와야 한다.
    - props를 참조하지 않을 때는 굳이 `css`를 불러와 사용할 필요가 없으나 props를 참조한다면 반드시 `css`로 감싸서 tagged 템플릿 리터럴을 사용햐여 한다.
    - 아래의 경우 `css`이하의 여러 줄의 코드에서는 props를 참조하지 않으므로 굳이 써주지 않아도 된다.

  ```react
  /* 다음 코드는 inverted 값이 true 일 때 특정 스타일을 부여해준다. */
  ${(props) =>
    props.inverted &&
    css`
      background: none;
      border: 2px solid white;
      color: white;
      &:hover {
        background: white;
        color: black;
      }
    `};
    & + button {
    margin-left: 1rem;
  }
  ```

  - 위와 같은 코드는 아래와 같이 JSX에서 props를 활용하여 서로 다른 스타일을 적용할 수 있다.

  ```react
  const StyledComponent = () => (
    <Box color="black">
      <Button>안녕하세요</Button>
      <Button inverted={true}>테두리만</Button>
    </Box>
  );
  ```

  

- 반응형 디자인

  - `styled-components`를 사용하여 반응형 디자인을 할 때는 일반 CSS와 동일하게 media 쿼리를 사용하면 된다.

  ```react
  const Box = styled.div`
    background: ${(props) => props.color || "blue"};
    padding: 1rem;
    display: flex;
    width: 1024px;
    margin: 0 auto;
    @media (max-width: 1024px){
      width: 768px;
    }
    @media (max-width: 768px){
      width: 100%;
    }
  `;
  ```

  - 위 작업을 함수화하여 간편하게 사용하는 것도 가능하다.
    - `styled-components`에서 제공하는 유틸 함수를 사용한다.
    - https://www.styled-components.com/docs/advanced#media-templates 참고
    - 지금은 한 파일에 생성했지만 실제 사용할 때는 아예 다른 파일에서 모듈화 한 뒤 사용하는 것이 편하다.

  ```react
  const sizes = {
    desktop: 1024,
    tablet: 768,
  };
  
  // 위에있는 size 객체에 따라 자동으로 media 쿼리 함수를 만들어준다.
  const media = Object.keys(sizes).reduce((acc, label) => {
    acc[label] = (...args) => css`
      @media (max-width: ${sizes[label] / 16}em) {
        ${css(...args)};
      }
    `;
  
    return acc;
  }, {});
  
  const Box = styled.div`
    background: ${(props) => props.color || "blue"};
    padding: 1rem;
    display: flex;
    width: 1024px;
    margin: 0 auto;
    ${media.desktop`width: 768px;`}
    ${media.tablet`width: 100%;`};
  `;
  
  ```

  



