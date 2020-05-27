# Vue 프로젝트

- vue/cli 설치(최초 1회)
  - VScode extention에서 `Vetur` 설치

```bash
$ npm install -g @vue/cli
```

- 프로젝트 생성

```bash
$ vue create 프로젝트명

#입력하면 디폴트 모드와 설정 모드 중 하나를 선택해 엔터
#완료되면  $ cd 프로젝트명, $ npm run serve을 실행해 달라는 문구가 뜬다.

$ vue 프로젝트명
$ npm run serve
```

- 구성

  - src(실제 사용하는 건 이 폴더 뿐)

    - `main.js`가 분리해서 개발한 모든 파일을 관리하는 최상위 파일이다. mount를 담담
    - `App.vue`: component들의 관리자, 최종 component

    ```html
    <!--기본 구조-->
    <template>
      <div id="app">
    
      </div>
    </template>
    
    <script>
    export default {
      name: 'App',
      components: {
        
      }
    }
    </script>
    
    <style>
    
    </style>
    ```

    - `components`: component들을 모아 놓은 폴더 
    - `assets`: 정적인 파일들(img 등) 모아 놓은 곳

  - public: `main.js`가 바라보는 최종 HTML파일이 있는 곳

  - `bable`: Vue 코드를 vanilla JS로 번역해준다.

  - `package.json`, `package-lock.json`: `requirements.txt`와 유사한 역할
    - `package.json`은 django의 `manage.py`와 같이 루트라는 것을 알 수 있는 파일이다.
  - `node_modules`: python의 venv에 해당, 패키지를 설치할 경우 실제로 코드가 들어가게 되는 디렉토리

- `.Vue`파일 component라 불리며 하나의 component는 template, script, style로 이루어져 있다.
  - 파일명은 UpperCamelCase로 작성한다.
  - VScode에서 `Vetur` 확장 프로그램을 설치했다면 폴더를 열고 `<`를 입력하고 탭을 누르면 html에서 `!`를 입력하고 탭을 누르는 것 처럼 기본 구조를 잡아준다.
  - 기본 구조는 html에 해당하는 `<template>`,  js에 해당하는 `<script>`,  css에 해당하는 `<style>`의 세 부분이다.

```html
<!--template 태그 안에는 하나의 root element만 존재해야 한다. 하나의 태그 안에 자식 태그가 있는 것은 괜찮지만 root에는 오직 하나의 태그만 존재해야 한다.-->
<template>
  <div>{{message}}</div>
</template>

<script>
export default {
    name:'First',  //name은 default로 넘어가므로 아무렇게나 지정해도 된다.
    /*
    Vue에서 데이터는 함수로 넘긴다.
    data를 객체가 아닌 함수로 넘기는 이유는 component를 재사용하므로 component는 계속 새로고침 없이 재사용되는데,
    data를 객체로 선언하면 계속 같은 값이 변하게 된다. 
    예를 들어 데이터를 a=1이라는 데이터가 있고 component가 사용될 때 마다 a+=1씩 해주는 함수를 작성했을 때,
    a를 객체로 만들었을 경우 매번 component가 재사용 될 때 마다 계속 +1씩 증가한다.
    반면에 a를 함수로 선언하면 component가 재사용 될 때 마다 a를 선언하는 함수도 다시 실행되면서 a의 복사본이 생기므로 
    몇 번을 재사용해도 a=2가 된다.
    */
    data: function(){ 
        return {
            message: '안녕하세요'
        }
    }
}
</script>

<style>

</style>


<!--export default 내보내고 싶은 대상-->
<!--default는 옵션이다. default로 내보내면 다른 곳에서 import할 때 이름을 마음대로 붙여서 사용할 수 있다. default는 내보낼 것이 하나일 때만 사용할 수 있다.-->

<template>
  <div>
    <h1>Hello World</h1>

    </div>
</template>

<script>
const arr1 = [1,2,3]
const arr2 = [4,5,6]
//export default는 내보낼 것을 지정하는 것이다.
//아래에 작성하지 않은 것은 다른 파일에서 이 파일을 import해도 사용할 수 없다.
//arr1은 내보냈으므로 다른 곳에서 import해서 사용이 가능하지만 arr2는 불가능하다.
export default arr1  //객체를 내보내는 것이 아니므로 {}는 쓰지 않아도 된다.

</script>

<style>

</style>
```

- `App.vue`파일은 `root`파로 아래의 component로 직접 작성한 component는 이곳을 통해 출력한다.

```html
<template>
  <div id="app">
    <!--3.사용하기-->
    <First></First>
	<!--
	  혹은 아래와 같이 써도 된다.
	  <First />
	  태그 안에 /가 있으면 닫힘태그를 쓰지 않아도 된다
	-->
  </div>
</template>

<script>
//1. import하기
// import 변수이름 from 경로
// 만일 import한 파일에서 export할 때 default 설정을 줬다면 설정하고 싶은 대로 설정하면 된다.
// 그러나 일반적으로 import한 파일명과 동일하게 설정하는 것이 관례다.
import First from './components/FirstComponent.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    //2. 등록하기
    //본래 object이므로 'key':value(e.g. 'First':first)형태로 적어야 하지만
    //JS의 object에서 key는 ''를 생략 가능하고, key와 value가 같으면 value는 안 적어도 된다.
    First,
  }
}
</script>

<!--후략-->
```

- axios 설치

```bash
#i는 install의 약자로 Vue에서는 아래와 같이 설치가 가능하다.
$ npm i axios
```

- 프로젝트를 하나의 HTML 파일로 만들기

```bash
$ npm run build

#위 코드를 입력하면 dist 폴더가 새로 생기고 그 안에 HTML,JS,CSS파일이 새로 생긴다.
```



- vue router

  - 모든 기능이 한 url에서 이루어지므로 특정 기능을 이용하기 위해 url을 입력하고 해당 기능으로 바로 이동하는 것이 불가능
  - 새로고침 없이 url을 설정할 수 있도록 해주는 것이 vue router다.
  - `vue add router`: vue cli가 제공하는 vue router 구조를 잡아주는 명령어

  ```bash
  $ vue add router
  
  #commit을 하라고 하는데 완료가 되면 App.vue의 내용이 다 날아가기 때문이다. 따라서 프로젝트 생성하자마자 하는 것이 좋다.
  
  #Use history mode for router? (Requires proper server setup for index fallback in production) (Y/n) 는 Y를 해준다. 이걸 y로 해줘야 뒤로가기를 눌러도 새로고침이 일어나지 않는다.
  
  #완료되면 src폴더에 추가 폴더가 생기고 App.vue과 main.js에도 코드가 추가된다.
  ```

  - `index.js`가 django의 urls.py의 역할을 하는 파일이다.
    - `index.js`에서 쓸 컴포넌트를 `views`에 작성,  `views`에 작성된 컴포넌트를 다른 이름으로 페이지라고도 부른다. 또 `views`에서 import 해서 쓸 컴포넌트를 `components`에 작성한다. 

  ```js
  //생성 후 아무 것도 수정하지 않은 상태
  import Vue from 'vue'
  import VueRouter from 'vue-router'   //from .views와 유사한 코드
  import Home from '../views/Home.vue'
  import About from '../views/About.vue'
  
  Vue.use(VueRouter)
  
    //url_patterns와 유사한 코드
    //django와 달리 :로 variable routing을 표현한다.
    const routes = [
    {
      path: '/',    //이 경로로 접근하면
      name: 'Home',  //경로의 이름
      component: Home  //(위에서 import한)Home이라는 component를 사용하겠다. 
    },
    {
      path: '/about',
      name: 'About',
    //routes 변수에 담긴 오브젝트를 일렬로 표현하면 다음과 같다. django의 url_pattern과 유사하다.
    //{path: '/', name: 'Home', component: Home},
  
      // 아래 코드는 최적화를 위한 코드, 아직 신경쓰지 않아도 된다.
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    }
  ]
  
  //아직 아래 코드는 신경쓰지 않아도 된다.
  const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
  })
  
  export default router
  ```

  - `App.vue`

  ```html
  <template>
    <div id="app">
      <div id="nav">
        <!--
          <router-link>는 a태그와 달리 새로고침 없이 url을 이동시킨다.
          <a>태그를 사용한 것은 맞지만 JS를 통해 새로고침이 일어나지 않게 설계한 것이다.
          아래 링크를 눌러서 url이 바뀌는 것을 index.js가 인지하고 렌더링 해준다.
        -->
        <!--
          django와 딜리 url 경로 뒤가 아니라 앞에 /를 붙인다.
          이건 Vue가 특이한 것이 아니라 django가 특이한 것으로
          대부분의 경우에는 /를 경로 앞에 붙인다.
        -->
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link>
      </div>
  
      <!--
        아래 태그가 컴포넌트를 렌더링 하는 태그다.
        django의 {% block content %}와 유사하다.
      -->
      <router-view/>
        
    </div>
  </template>
  
  <style>
  
  </style>
  
  ```

  