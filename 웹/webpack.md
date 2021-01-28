# Babel

## Babel이란

- ES의 사양과 브라우저

  - 크롬, 사파리, 파이어폭스와 같은 **에버그린 브라우저**(Evergreen browser, 사용자의 업데이트 없이도 최신 버전으로 자동 업데이트를 수행하는 모던 브라우저)의 ES6 지원 비율은 약 98%로 거의 대부분의 ES6 사양을 구현하고 있다.
  - 하지만 인터넷 익스플로어(IE) 11의 ES6 지원 비율은 약 11%이다. 그리고 매년 새롭게 도입되는 ES6 이상의 버전(ES6+)과 제안 단계에 있는 ES 제안 사양(ES NEXT)은 브라우저에 따라 지원 비율이 제각각이다.
  - 따라서 ES6+ 또는 ES NEXT의 ES 최신 사양을 사용하여 프로젝트를 진행하려면 최신 사양으로 작성된 코드를 경우에 따라 IE를 포함한 구형 브라우저에서 문제 없이 동작시키기 위한 개발 환경을 구축하는 것이 필요하다. 특히 모듈의 경우, 모듈 로더가 필요하다.

  - 대부분의 모던 브라우저에서는 ES6 모듈을 사용할 수 있다.
  - 단, 아래와 같은 이유로 아직까지는 브라우저가 지원하는 ES6 모듈 기능보다는 Webpack 등의 모듈 번들러를 사용하는 것이 일반적이다.
    - IE를 포함한 구형 브라우저는 ES6 모듈을 지원하지 않는다.
    - 브라우저의 ES6 모듈 기능을 사용하더라도 트랜스파일링이나 번들링이 필요하다.
    - 아직 지원하지 않는 기능(Bare import 등)이 있다.
    - 점차 해결되고는 있지만 아직 몇가지 이슈가 있다.



- Babel
  - JavaScript compiler
  - 최신 JS 코드를 이전 단계의 JS 코드로 변환 가능하게 해주는 개발 도구, 트랜스파일러(transpiler)
    - 만일 ES6로 개발을 진행한다면 IE 등의 브라우저에서는 해당 사이트가 동작하지 않을 수 있다.
    - babel은 ES6로 작성된 코드를 브라우저에 맞는 JS 코드로 변경해준다.





## Babel 사용하기

- CLI 설치하기

  ```bash
  # package.json 생성
  $ npm init -y
  # babel-core, babel-cli 설치
  $ npm install --save-dev @babel/core @babel/cli
  ```



- babellrc 설정 파일 작성

  - Babel을 사용하려면 `@babel/preset-env`을 설치해야 한다. 
    - `@babel/preset-env`은 함께 사용되어야 하는 Babel 플러그인을 모아 둔 것으로 **Babel 프리셋**이라고 부른다. 
  - Babel이 제공하는 공식 Babel 프리셋(Official Preset)은 아래와 같다.
    - `@babel/preset-env`
    - `@babel/preset-flow`
    - `@babel/preset-react`
    - `@babel/preset-typescript`
  - `@babel/preset-env`도 공식 프리셋중 하나이며 필요한 플러그인 들을 프로젝트 지원 환경에 맞춰서 동적으로 결정해 준다.
    - 프로젝트 지원 환경은 [Browserslist](https://github.com/browserslist/browserslist) 형식으로 .browserslistrc 파일에 상세히 설정할 수 있다. 프로젝트 지원 환경 설정 작업을 생략하면 기본값으로 설정된다.

  ```bash
  # env preset 설치
  $ npm install --save-dev @babel/preset-env
  ```

  - 설치가 완료되었으면 프로젝트 루트에 `.babelrc` 파일을 생성하고 아래와 같이 작성한다. 
    - 지금 설치한 `@babel/preset-env`를 사용하겠다는 의미이다.

  ```json
  {
    "presets": ["@babel/preset-env"]
  }
  ```

  

- 트랜스파일링

  - Babel을 사용하여 ES6+ 코드를 ES5 이하의 코드로 트랜스파일링하기 위해 Babel CLI 명령어를 사용할 수도 있다.
  - 그러나 아래 설명은 npm script를 사용하여 트랜스파일링하는 방법이다.

  - `package.json` 파일에 `scripts`를 추가한다.
  - 아래 npm script는 src/js 폴더(타깃 폴더)에 있는 모든 ES6+ 파일들을 트랜스파일링한 후, 그 결과물을 dist/js 폴더에 저장한다. 사용한 옵션의 의미는 아래와 같다.
    - `-w`: 타깃 폴더에 있는 모든 파일들의 변경을 감지하여 자동으로 트랜스파일한다. (`--watch` 옵션의 축약형)
    - `-d`: 트랜스파일링된 결과물이 저장될 폴더를 지정한다. (`--out-dir` 옵션의 축약형)

  ```json
  {
    "name": "es6-project",
    "version": "1.0.0",
    "scripts": {
      "build": "babel src/js -w -d dist/js"
    },
    "devDependencies": {
      "@babel/cli": "^7.7.0",
      "@babel/core": "^7.7.2",
      "@babel/preset-env": "^7.7.1"
    }
  }
  ```

  - 트랜스파일링을 테스트하기 위해 ES6+ 파일을 작성. 
    - 프로젝트 루트에 src/js 폴더를 생성한 후 `lib.js`와 `main.js`를 추가.

  ```javascript
  // src/js/lib.js
  // ES6 모듈
  export const pi = Math.PI
  
  export function power(x, y) {
    // ES7: 지수 연산자
    return x ** y
  }
  
  // ES6 클래스
  export class Foo {
    // stage 3: 클래스 필드 정의 제안
    #private = 10
  
    foo() {
      // stage 4: 객체 Rest/Spread 프로퍼티
      const { a, b, ...x } = { ...{ a: 1, b: 2 }, c: 3, d: 4 }
      return { a, b, x }
    }
  
    bar() {
      return this.#private
    }
  }
  ```

  ```javascript
  // src/js/main.js
  // ES6 모듈
  import { pi, power, Foo } from './lib'
  
  console.log(pi)
  console.log(power(pi, pi))
  
  const f = new Foo()
  console.log(f.foo())
  console.log(f.bar())
  ```

  - 터미널에서 아래 명령으로 트랜스파일링을 실행한다.
    - 실행하면 에러가 발생한다.
    - `@babel/preset-env`는 현재 제안 단계에 있는 사양에 대한 플러그인을 지원하지 않기 때문에 발생한 에러이다. 
    - 현재 제안 단계에 있는 사양을 지원하려면 별도의 플러그인을 설치하여야 한다.

  ```bash
  $ npm run build
  
  > es6-project@1.0.0 build /Users/leeungmo/Desktop/es6-project
  > babel src/js -w -d dist/js
  
  SyntaxError: /Users/leeungmo/Desktop/es6-project/src/js/lib.js: Unexpected character '#' (12:2)
  
    10 | export class Foo {
    11 |   // stage 3: 클래스 필드 정의 제안
  > 12 |   #private = 10;
       |   ^
    13 |
    14 |   foo() {
    15 |     // stage 4: 객체 Rest/Spread 프로퍼티
  ...
  ```

  

- Babel 플러그인

  - 설치가 필요한 플러그인은 Babel 홈페이지에서 검색할 수 있다. 
  - 상단 메뉴의 Search에 제안(프로포절)의 이름을 입력하면 해당 플러그인을 검색할 수 있다. 
  - 클래스 필드 정의 제안 플러그인을 검색하기 위해 “Class field”를 입력.
  - 검색한 플러그인 `@babel/plugin-proposal-class-properties`를 설치.

  ```bash
  $ npm install --save-dev @babel/plugin-proposal-class-properties
  ```

  - 설치 이후 `package.json` 파일

  ```json
  {
    "name": "es6-project",
    "version": "1.0.0",
    "scripts": {
      "build": "babel src/js -w -d dist/js"
    },
    "devDependencies": {
      "@babel/cli": "^7.7.0",
      "@babel/core": "^7.7.2",
      "@babel/plugin-proposal-class-properties": "^7.7.0",
      "@babel/preset-env": "^7.7.1"
    }
  }
  ```

  - 설치한 플러그인은 `.babelrc` 파일에 추가해야 한다.

  ```json
  {
    "presets": ["@babel/preset-env"],
    "plugins": ["@babel/plugin-proposal-class-properties"]
  }
  ```

  - 다시 터미널에서 트랜스파일링을 실행
    - 트랜스파일링에 성공하면 프로젝트 루트에 dist/js 폴더가 자동 생성되고 트랜스파일링된 `main.js`와 `lib.js`가 저장된다.

  ```bash
  $ npm run build
  ```

  - 트랜스파일링된 main.js를 실행해 본다.

  ```bash
  $ node dist/js/main
  3.141592653589793
  36.4621596072079
  { a: 1, b: 2, x: { c: 3, d: 4 } }
  10
  ```

  

- 브라우저에서 모듈 로딩 테스트

  - 앞에서 `main.js`와 `lib.js` 모듈을 트랜스파일링하여 ES5로 변환된 `main.js`을 실행한 결과, 문제없이 실행되는 것을 확인하였다. 
  - 하지만 모듈 기능은 node.js 환경에서 동작한 것이고 Babel이 모듈을 트랜스파일링한 것도 node.js가 기본 지원하는 CommonJS 방식의 module loading system에 따른 것이다. 
  - 아래는 `src/js/main.js`가 Babel에 의해 트랜스파일링된 결과이다.

  ```javascript
  // dist/js/main.js
  "use strict";
  
  var _lib = require("./lib");
  
  console.log(_lib.pi);
  console.log((0, _lib.power)(_lib.pi, _lib.pi));
  var f = new _lib.Foo();
  console.log(f.foo());
  console.log(f.bar());
  ```

  - 브라우저는 CommonJS 방식의 module loading system(require 함수)을 지원하지 않으므로 위에서 트랜스파일링된 결과를 그대로 브라우저에서 실행하면 에러가 발생한다.
  - 이는 Webpack을 통해 해결 가능하다.



# Webpack

## Webpack이란

- Webpack
  - 의존 관계에 있는 모듈들을 하나의 JS 파일로 번들링하는 모듈 번들러.
  - 의존 모듈이 하나의 파일로 번들링되므로 별도의 모듈 로더가 필요없다. 
  - 그리고 다수의 자바스크립트 파일을 하나의 파일로 번들링하므로, html 파일에서 script 태그로 다수의 자바스크립트 파일을 로드해야 하는 번거로움도 사라진다.



## Webpack 사용하기

- Webpack 설치하기

  ```bash
  # Webpack V4는 webpack-cli를 요구한다
  $ npm install --save-dev webpack webpack-cli
  ```

  

- babel-loader

  - Webpack이 모듈을 번들링할 때, Babel을 사용하여 ES6+ 코드를 ES5 코드로 트랜스파일링하도록 babel-loader를 설치한다.

  ```bash
  # babel-loader 설치
  $ npm install --save-dev babel-loader
  ```

  - npm script를 변경하여 Babel 대신 Webpack을 실행하도록 아래와 같이 package.json 파일의 scripts를 변경한다.

  ```json
  {
    "name": "es6-project",
    "version": "1.0.0",
    "scripts": {
      "build": "webpack -w"
    },
    "devDependencies": {
      "@babel/cli": "^7.7.0",
      "@babel/core": "^7.7.2",
      "@babel/plugin-proposal-class-properties": "^7.7.0",
      "@babel/preset-env": "^7.7.1",
      "babel-loader": "^8.0.6",
      "webpack": "^4.41.2",
      "webpack-cli": "^3.3.10"
    }
  }
  ```

  

- webpack.config.js

  - 프로젝트 루트에 webpack.config.js 파일을 생성하고 아래와 같이 작성한다.

  ```javascript
  const path = require('path');
  
  module.exports = {
      // enntry file
      entry: './src/js/main.js',
      // 컴파일 + 번들링된 js 파일이 저장될 경로와 이름 지정
      output: {
          path: path.resolve(__dirname, 'dist/js'),
          filename: 'bundle.js'
      },
      module: {
          rules: [
              {
                  test: /\.js$/,
                  include: [
                      path.resolve(__dirname, 'src/js')
                  ],
                  exclude: /node_modules/,
                  use: {
                      loader: 'babel-loader',
                      options: {
                          presets: ['@babel/preset-env'],
                          plugins: ['@babel/plugin-proposal-class-properties']
                      }
                  }
              }
          ]
      },
      devtool: 'source-map',
      // https://webpack.js.org/concepts/mode/#mode-development
      mode: 'development'
  };
  ```

  - Webpack을 실행하여 트랜스파일링 및 번들링을 실행.
    - 트랜스파일링은 Babel이 실행하고 번들링은 Webpack이 실행한다.
    - 만약 이전에 실행시킨 빌드 명령이 실행 중인 상태라면 중지시키고 다시 아래 명령을 실행한다.

  ```bash
  $ npm run build
  ```

  - 실행 결과 dist/js 폴더에 `bundle.js` 파일이 생성된다. 
    - 이 파일은 main.js, lib.js 모듈이 하나로 번들링된 결과물이다.
  - `index.html`을 아래와 같이 작성하고 브라우저에서 실행한다.
    - `main.js`, `lib.js` 모듈이 하나로 번들링된 bundle.js가 브라우저에서 문제없이 실행되는 것을 확인 가능하다.

  ```html
  <!DOCTYPE html>
  <html>
  <body>
    <script src="./dist/js/bundle.js"></script>
  </body>
  </html>
  ```

  

- babel-polyfill

  - Babel을 사용하여 ES6+ 코드를 ES5 이하로 트랜스파일링하여도 브라우저가 지원하지 않는 코드가 남아 있을 수 있다. 
  - 예를 들어, ES6에서 추가된 Promise, Object.assign, Array.from 등은 ES5 이하로 트랜스파일링하여도 대체할 ES5 기능이 없기 때문에 그대로 남아 있다.
  - 즉, Promise, Object.assign, Array.from 등과 같이 ES5 이하로 대체할 수 없는 기능은 트랜스파일링이 되지 않는다.
  - 따라서 오래된 브라우저에서도 ES6+에서 새롭게 추가된 객체나 메소드를 사용하기 위해서는 `@babel/polyfill`을 설치해야 한다.
    - babel-polyfill은 개발 환경에서만 사용하는 것이 아니라 실제 환경에서도 사용하여야 하므로 `--save-dev` 옵션으로 개발 설치를 하지 않도록 한다.

  ```bash
  $ npm install @babel/polyfill
  ```

  - ES6의 import를 사용하는 경우에는 진입점의 선두에서 먼저 폴리필을 로드하도록 한다.

  ```javascript
  // src/js/main.js
  import "@babel/polyfill";
  ```

  - webpack을 사용하는 경우에는 위 방법을 대신 폴리필을 webpack.config.js 파일의 entry 배열에 추가한다.

  ```javascript
  const path = require('path');
  
  module.exports = {
    // entry files
    entry: ['@babel/polyfill', './src/js/main.js'],
  ```

  - 수정 사항을 반영

  ```bash
  $ npm run build
  ```

  - dist/js/bundle.js을 확인해보면 polyfill이 추가된 것을 확인할 수 있다.



### Sass 컴파일

- Sass를 컴파일한 결과물인 css를 bundle.js 파일에 포함시키는 방법

  - 필요한 패키지를 설치
    - node-sass는 node.js 환경에서 사용할 수 있는 Sass 라이브러리이다. 
    - 실제로 Sass를 css로 컴파일하는 것은 node-sass이다. 
    - style-loader, css-loader, sass-loader는 Webpack 플러그인이다.

  ```bash
  $ npm install node-sass style-loader css-loader sass-loader --save-dev
  ```

  - webpack.config.js 파일을 아래와 같이 수정한다.

  ```javascript
  const path = require('path');
  
  module.exports = {
    // entry files
    entry: ['@babel/polyfill', './src/js/main.js', './src/sass/main.scss'],
    // 컴파일 + 번들링된 js 파일이 저장될 경로와 이름 지정
    output: {
      path: path.resolve(__dirname, 'dist/js'),
      filename: 'bundle.js'
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          include: [
            path.resolve(__dirname, 'src/js')
          ],
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env'],
              plugins: ['@babel/plugin-proposal-class-properties']
            }
          }
        },
        {
          test: /\.scss$/,
          use: [
            "style-loader", // creates style nodes from JS strings
            "css-loader",   // translates CSS into CommonJS
            "sass-loader"   // compiles Sass to CSS, using Node Sass by default
          ],
          exclude: /node_modules/
        }
      ]
    },
    devtool: 'source-map',
    // https://webpack.js.org/concepts/mode/#mode-development
    mode: 'development'
  };
  ```

  - 테스트를 위해 3개의 Sass 파일을 src/sass 폴더와 src/sass/partials 폴더에 추가한다.
    - src/sass/main.scss, src/sass/partials/\_vars.scss, src/sass/partials/_body.scss

  ```css
  @import "partials/vars";
  @import "partials/body";
  ```

  ```css
  
  $font_color: #333;
  $font_family: Arial, sans-serif;
  $font_size: 16px;
  $line_height: percentage(20px / $font_size);
  ```

  ```css
  body {
    color: $font_color;
  
    // Property Nesting
    font: {
      size: $font_size;
      family: $font_family;
    }
  
    line-height: $line_height;
  }
  ```

  - 반영하기

  ```bash
  $ npm run build
  ```

  - CSS가 적용되는 것을 확인하기 위해 index.html을 아래와 같이 수정 후 실행.
    - 컴파일된 CSS는 bundle.js에 포함되어 있다.

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <script src="./dist/js/bundle.js"></script>
    </head>
  <body>
    Hello world!
  </body>
  </html>
  ```

  

  

- 별도의 css 파일로 분리하는 방법.

  - Sass 파일이 방대해지면 자바스크립트 파일에서 분리하는 것이 효율적일 수 있다. 
    - bundle.js 파일에 컴파일된 css를 포함시키지 말고 별도의 css 파일로 분리해서 하나의 파일로 번들링하는 방법도 있다. 
    - 이때 사용하는 플러그인은 mini-css-extract-plugin이다.
  - mini-css-extract-plugin을 설치

  ```bash
  $ npm install --save-dev mini-css-extract-plugin
  ```

  - webpack.config.js 파일을 아래와 같이 수정한다.

  ```javascript
  const path = require('path');
  const MiniCssExtractPlugin = require('mini-css-extract-plugin');
  
  module.exports = {
      // entry files
      entry: ['@babel/polyfill', './src/js/main.js', './src/sass/main.scss'],
      // 컴파일 + 번들링된 js 파일이 저장될 경로와 이름 지정
      output: {
          path: path.resolve(__dirname, 'dist'),
          filename: 'js/bundle.js'
      },
      plugins: [
          // 컴파일 + 번들링 CSS 파일이 저장될 경로와 이름 지정
          new MiniCssExtractPlugin({ filename: 'css/style.css' })
      ],
      module: {
          rules: [
              {
                  test: /\.js$/,
                  include: [
                      path.resolve(__dirname, 'src/js')
                  ],
                  use: {
                      loader: 'babel-loader',
                      options: {
                          presets: ['@babel/preset-env'],
                          plugins: ['@babel/plugin-proposal-class-properties']
                      }
                  },
                  exclude: /node_modules/
              },
              {
                  test: /\.scss$/,
                  use: [
                      MiniCssExtractPlugin.loader,
                      'css-loader',
                      'sass-loader'
                  ],
                  exclude: /node_modules/
              }
          ]
      },
      devtool: 'source-map',
      // https://webpack.js.org/concepts/mode/#mode-development
      mode: 'development'
  };
  ```

  - 빌드 명령어 실행

  ```bash
  $ npm run build
  ```

  - 성공한다면 css 폴더가 생성되고 style.css 파일이 저장된다. 
    - 컴파일되고 하나의 파일로 번들링된 css가 bundle.js 파일에 포함되지 않고 별도 파일로 분리된 것이다.
  - 이제 index.html에서 style.css 파일을 로드한다.

  ```html
  <!DOCTYPE html>
  <html>
    <head>
      <link href="./dist/css/style.css" rel="stylesheet"></link>
      <script src="./dist/js/bundle.js"></script>
    </head>
  <body>
    Hello world!
  </body>
  </html>
  ```

  







