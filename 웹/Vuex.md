# Vuex

> https://vuex.vuejs.org/kr/

- Vue.js 애플리케이션에 대한 상태 관리 패턴 + 라이브러리, 모든 컴포넌트에 대한 중앙 집중식 저장소 역할
  - 그 동안은 emit과 props를 통해 부모자식 간에 정보를 주고받았다. 그러나, 지나치게 중첩된 컴포넌트를 통과하는 prop는 장황할 수 있으며 형제 컴포넌트에서는 작동하지 않는다는 문제가 있다.
  - 이를 해결해 주는 것이 `Vuex`로, 이는 데이터 혹은 요청을  자식 혹은 부모가 아닌 중계소로 보내, 중계소에서 해당 데이터 혹은 요청을 받을 곳으로 바로 보내주는 것이다. 
  - 데이터 관리가 보다 쉬워지지만 배우기 어렵다는 단점이 존재한다.



- 관리자 도구의 Vue탭 내부의 2번째 탭은 Vuex가 실행되는 것을 보여준다.



- 사용법

  - Vuex를 불러오기

  ```bash
  $ vue add vuex
  
  #router와 유사하게 여러 파일에 새로운 코드가 추가되고 새로운 폴더, 파일이 생성된다.
  ```

  - 성공적으로 불러오면 `main.js`에 아래 코드가 추가된다.

  ```js
  import Vue from 'vue'
  import App from './App.vue'
  import router from './router'
  import store from './store' //추가된 코드
  //실제 import하는 것은 store 폴더가 아닌 store 폴더 내부의 index.js파일이므로 아래와 같이 써야한다. 
  //import store from './store/index.js'
  
  //그럼에도 이와 같이 쓴 이유는 다음과 같다.
  //첫째, import할 때 뒤의 확장자는 생략 가능하다.
  //import store from './store/index'
  //둘째, import 구문에서 파일명이 생략되면 자동으로 index파일을 탐색한다(index는 특수한 파일명으로 import문이 자동으로 탐색해준다). 
  
  
  Vue.config.productionTip = false
  
  new Vue({
    router,
    store,  //추가된 코드
    render: h => h(App)
  }).$mount('#app')
  
  ```

  

- 구성

  - `src/store/index.js`

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  import axios from 'axios'
  
  Vue.use(Vuex)
  
  //기본 구성은 state,mutations,modules뿐으로 getters는 추가한 것이다.
  export default new Vuex.Store({
    
    // data 의 집합, 중앙 관리할 모든 데이터(혹은 상태)
    state: {
    },
      
    
    // state(data) 를 (가공해서 혹은 그대로)가져올 함수들, computed와 동일
    getters: {
    },
      
    
    // state 를 변경하는 함수들(state를 변경하는 코드는 mutations에 작성해야만 동작한다.)
    // 모든 mutation 함수들은 동기적으로 동작하는 코드여야 한다.
    // commit 을 통해 실행한다.
    mutations: {
    },
      
    
    // 범용적인 함수들을 작성(범용적인 함수를 작성하기에 state, mutations 등 위에 있는 모든 것들에 접근이 가능하다), mutations 에 정의한 함수를 	actions 에서 실행 가능하다.
    // 비동기 로직은 actions 에서 정의한다.
    // dispatch 를 통해 실행한다.
    actions: {
    },
      
    
    //당장은 몰라도 된다.
    modules: {}
  })
  ```



- 사용 예시

  - 파일 구조
  
```
  App-A-Aa-Ca
  	 -Ab
     -B-Ba-Cb
  	 -Bb
  ```
  
  - Ca에서 Cb까지 데이터를 보내려면 Ca-Aa-A-App-B-Ba-Cb의 여러 단계를 거쳐야 한다.
    - Vuex를 사용하면 이를 훨씬 편하게 보낼 수 있다.
  
  ```html
  <!--Cb.vue-->
  <template>
    <div>
        <h1>Ca</h1>
        <div>{{Aac}},Ca</div>
        <button @click="sendToAa">Send To A</button>
        <button @click="sendToCb">Send To Cb</button>
    </div>
  </template>
  
  <script>
  export default {
      name: 'Ca',
      data: function(){
          return {
              CaToA:'message from Ca to A',
              CaToCb:'message from Ca to Cb',
          }
      },
      props:{
          Aac:String,
      },
      methods:{
          sendToAa(){
              this.$emit('sendToAa',this.CaToA)
          },
          sendToCb(){
              this.$emit('sendToCb',this.CaToCb)
          },
      }
  }
  </script>
  
  <style>
  
  </style>
  ```
  
  



- 실제 활용 코드

  - 아래 예시 코드는 실제로 동작하지는 않는다. 중간 중간 수정하지 않은 것도 있고 모든 component파일을 가져온 것도 아니며 모든 코드를 옮긴 것이 아니라 이해에 필요한 부분만 작성한 것이므로 동작하는 완전한 코드를 보고자 한다면 gitlab을 참고(교수님 코드)할 것
  - `App.vue`

  ```html
  <template>
    <div class="container">
      <!--
        <SearchBar @input-change="onInputChange" />
  	-->
      <SearchBar/>
      <div class="row">
        <!--
  	    만일 VideoDetail.vue의 코드를 아래와 같이 수정했다면 내려줄 필요가 없다.
          <VideoDetail :video="selectedVideo"/>
  	  -->
        <VideoDetail/>
        <!--
          <VideoList @video-select="onVideoSelect" :videos="videos" />
  	  -->
        <VideoList/>
      </div>
    </div>
  </template>
  
  <script>
  /*
  import axios from 'axios'
  */
  import SearchBar from './components/SearchBar.vue'
  import VideoList from './components/VideoList.vue'
  import VideoDetail from './components/VideoDetail.vue'
  
  /*
  const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY
  const API_URL = 'https://www.googleapis.com/youtube/v3/search'
  */
  
  export default {
    name: 'App',
    components: { SearchBar, VideoList, VideoDetail },
    /*최종 수정이 완료되면 아래 코드 전부가 필요 없는 코드가 된다.
    data() {
      return {
        //아래 3개의 데이터를 index.js의 state로 옮긴다.
        inputValue: '',
        videos: [],
        selectedVideo: null,
      }
    },
    methods: {
      onInputChange(inputText) {
        //data를 변경하는 로직이므로 mutations에 적어야 한다.
        this.inputValue = inputText
        axios.get(API_URL, {
          params: {
            key: API_KEY,
            part: 'snippet',
            type: 'video',
            q: this.inputValue,
          }
        })
          .then(res => { 
            res.data.items.forEach(item => {
              const parser = new DOMParser()
              const doc = parser.parseFromString(item.snippet.title, 'text/html')
              item.snippet.title = doc.body.innerText
            })
            //data를 변경하는 로직이므로 mutations에 적어야 한다.
            this.videos = res.data.items
          })
          .catch(err => console.error(err))
      },
      onVideoSelect(video) {
        //data를 변경하는 로직이므로 mutations에 적어야 한다.
        this.selectedVideo = video
      }
    }
    */
  }
  </script>
  ```

  - `VideoDetail.vue`

  ```html
  <template>
    <!--
      <div v-if="video" class="col-lg-8">
      index.js 수정이 완료되면 위와 같이 적지 않고 아래와 같이 적는다
    -->
    <div v-if="$store.state.selectedVideo" class="col-lg-8">
      <div class="embed-responsive embed-responsive-16by9">
  
        <!--
            <iframe 
              class="embed-responsive-item"
              :src="videoUrl" 
              allowfullscreen
            ></iframe>
  	  -->
        <!--
  		  원래 위와 같이 쓰지만 getters에서 받아온 것을 쓰고자 한다면 아래와 같이 쓰면 된다. ':src=' 부분을 바꿔준다
            <iframe 
              class="embed-responsive-item"
              :src="$store.getters.videoUrl"
              allowfullscreen
            ></iframe>
  	  -->
        <!--computed와 getters를 매핑하면 위보다 간결하게 아래와 같이 쓸 수 있다.-->
        <iframe 
          class="embed-responsive-item"
          :src="videoUrl" 
          allowfullscreen
        ></iframe>
      </div>
        
        
      <div class="details">
         
        <!--version1, 원래 코드
  		<h4 v-html="video.snippet.title"></h4>
          <p>{{ video.snippet.description }}</p>
  		위 코드는 부모에게 받아온 video 정보를 활용하는 코드이고, 아래 코드는 index.js의 state에 저장된 video 정보를 활용하는 코드이다.
  	  -->
          
        <!--version2, state를 활용한 코드
        	<h4 v-html="$store.state.selectedVideo.snippet.title"></h4>
        	<p>{{ $store.state.selectedVideo.snippet.description }}</p>
       	위 코드는 props나 emit을 거치지 않는다는 점에서는 간편하지만 너무 장황하다는 단점이 있으므로 이 코드 역시 getters에 저장한 후 아래처럼
  		불러와서 사용한다.
  	  -->
        
        <!--version3, getters를 활용한 코드
          <h4 v-html="$store.getters.videoTitle"></h4>
          <p>{{ $store.getters.videoDescription }}</p>
  		확실히 짧아지긴 했지만 더 줄이는 방법이 있다. 아래에서 cumputed를 getters에 옮겨 적었다고 지우는 것이 아니라 computed와 getters를 매핑		   하는 것이다.
  	  -->
        <!--computed와 getters를 매핑 3)코드로 작성-->
        <h4 v-html="videoTitle"></h4>
        <p>{{ videoDescription }}</p>
          
      </div>
    </div>
  </template>
  
  <script>
  //computed와 getters를 매핑 1)import
  import { mapGetters } from 'vuex' //computed와 getters 매핑을 위해 import(공식문서에 코드가 있다.) 
      
  export default {
      name: 'VideoDetail',
      props: {
        video: Object,
      },
      
      //computed는 Vuex에서 getters와 유사하므로 getters에 쓸 수 있다. 따라서 computed의 내용을 getters에 옮겨 적는다.
      /*
      computed: {
        videoUrl() {
          return `https://youtube.com/embed/${this.video.id.videoId}`
        }
      }
      */
      
      //computed와 getters를 매핑 2)매핑하기, 아래 코드를 적기 위해서는 위에서 import를 해줘야 한다.
      computed:{
          ...mapGetters([   //...mapGetters([매핑하고자 하는 변수들])
          'videoUrl',
          'videoTitle',
          'videoDescription'
        ])
      }
  }
  </script>
  ```

  - `VideoListItem.vue `

  ```html
  <template>
    <!--
  	클릭하면 onVideoSelect가 실행되고 emit되어 App.vue의 onVideoSelect함수가 실행된다.
  	이렇게 단계를 거치지 않고 한 번에 고쳐지게 하기 위해서는 표시한 코드를 추가
    -->
    <li @click="onVideoSelect" class="video-list-item list-group-item">
        <img :src="thumbnailUrl" class="mr-3" alt="youtube-thumbnail-image">
        <div class="media-body">
          {{ video.snippet.title }}
        </div>
    </li>
  </template>
  
  <script>
  export default {
      name: 'VideoListItem',
      
      props: {
          video: Object,
      },
      
      methods: {
          onVideoSelect() {
              /*
              this.$emit('video-select', this.video)
              */
  
              //mutations는 commit을 통해 실행되므로 아래에 commit을 써준다.
              //첫 번째 인자에는 mutations에서 실행시킬 함수를, 두번째 인자에는 넘길 데이터를 적으면 된다.
              //이제 onVideoSelect함수가 실행되면 index.js의 setSelectedVideo함수가 실행된다.
              this.$store.commit('setSelectedVideo', this.video)
          }
      },
      computed: {
          thumbnailUrl() {
              return this.video.snippet.thumbnails.default.url
          }
      }
      
  }
  </script>
  ```

  - searchBar.vue

  ```html
  <template>
    <div class="search-bar">
        <!--
         <input @keypress.enter="onInput">
         마찬가지로 enter를 눌렀을 때 emit이 수행되는 것이 아니라 바로 inputValue를 변경
        -->
        <input @keypress.enter="$store.commit('fetchVideos')">
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex' //actions와 매핑을 위한 코드, 공식문서 참고
  //만일 mutations와 매핑하고 싶다면 아래와 같이 적으면 된다.
  import { mutations } from 'vuex'
      
  export default {
      name: 'SearchBar',
      methods: {
          /*emit하는 것이 아니라
          onInput(event) {
              this.$emit('input-change', event.target.value)
          */
          //actions에 정의한 함수를 사용
           ...mapActions([
              'fetchVideos'
          }
      },
  }
  </script>
  ```

  - `src/store/index.js`

  ```js
  import Vue from 'vue'
  import Vuex from 'vuex'
  
  //기존에 App.vue에서 실행하던 axios관련 코드를 아래 actions에 정의했으므로 import해야 한다.
  import axios from 'axios'
  
  Vue.use(Vuex)
  
  //기존에 App.vue에서 실행하던 코드를 실행하기 위해 이것도 옮겨온다.
  const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY
  const API_URL = 'https://www.googleapis.com/youtube/v3/search
  
  
  //관리자 도구에서 Vue탭을 보면 넘겨받은 데이터,이벤트 등이 payload에 담겨서 넘어오게 된다. 아래에 payload라고 적은 것은 인자 이름이므로, payload라고 적는 것 보다는 실제 payload에 담겨 넘어온 것을 명시적으로 알 수 있도록 하는 것이 더 낫다.
  export default new Vuex.Store({
  
    state: {
      inputValue: '',
      videos: [],
      selectedVideo: null,
    },
  
    getters: {
      //getters는 mutations와 마찬가지로 반드시 state를 첫 인자로 받는다.
      //state를 첫 인자로 받는 이유는 getters의 존재 이유가 state(data)의 가공이기 때문이다.
      videoUrl(state){
        //return `https://youtube.com/embed/${this.video.id.videoId}`
        //원 코드는 위와 같지만 여기서는 this를 쓸 수 없으므로 아래와 같이 수정해서 적는다.
        return `https://youtube.com/embed/${state.selectedVideo.id.videoId}`
      },
      videoTitle(state){
        return state.selectedVideo.snippet.title
      },
      //화살표 함수로는 아래와 같이 표현 가능하다. 화살표함수는 사용을 지양하는 것이 좋으나 이 경우 공식문서에서도 화살표 함수를 사용하므로 써도 된다.
      //videoTitle: state => state.selectedVideo.snippet.title,
      videoDescription(state){
        return state.selectedVideo.snippet.description
      },
    },
  
    mutations: {
     	//django의 views.py에 작성한 함수들이 무조건 request를 첫 인자로 받는 것과 마찬가지로 mutations는 반드시 첫 인자로 state를 받는다.
      //단 js는 인자를 적지 않아도 작동하므로 굳이 적지 않아도 되지만 적어주는 것이 좋다.
      //state를 첫 인자로 받는 이유는 mutations의 존재 이유가 state(data)의 변경이기 때문이다.
  
      //inputValue를 변경하는 함수
      //inputValue에는 아래 actions의 fetchVideos함수에서 넘어온 event.target.value가 들어가게 된다.
      setInputValue(state, inputValue) {
        state.inputValue = inputValue
      },
  
      //videos를 변경하는 함수
      //videos에는 아래 actions의 fetchVideos함수에서 넘어온 res.data.items가 들어가게 된다.
       setVideos(state, videos) {
        state.videos = videos
      },
  
      //selectedVideo를 변경하는 함수
      //payload보다는 payload에 담겨온 것이 video이므로 video라고 적는 것이 더 명시적이지만 처음 배우는 것이므로 payload라고 적는다.
      setSelectedVideo(state, payload){
          state.selectedVideo = payload
      },
      
    },
  
    actions: {
      //원래 actions 내부에 정의하는 모든 함수는 첫 번째 인자로 context를 받는데 commit과 state는 모두 context내부의 요소다.
      //context를 console창에 찍어보면 감이 올 것이다.
      //fetchVideos(context , event)와 같이 적어도 상관 없다. 단, 일부 코드를 수정해야 한다. -1),2),3)
      //event listener에 의해 실행되는 함수들은 두 번째 인자로 event를 넘기는데 넘어온 event는 payload에 담겨서 온다.
      fetchVideos({ commit, state } , event) {
        // 1. inputValue 를 바꾼다.
        //inputValue는 state에 정의된 변수이고 state를 변경하는 것은 mutations에서만 해야 하므로 actions에서 직접 변경하는 것이 아니라 			mutations에서 해당 코드를 실행시키는 코드를 작성한다.
        commit('setInputValue', event.target.value)  //1)context.commit('setInputValue', event.target.value)
          
        // 2. state.inputValue를 포함시켜 요청을 보낸다. 본래 App.vue에서 하던 일을 이제 이 함수에서 한다.
        axios.get(API_URL, {
          params: {
            key: API_KEY,
            part: 'snippet',
            type: 'video',
            q: state.inputValue, //2)context.state.inputValue
          }
        })
          .then(res => { 
            res.data.items.forEach(item => {
              const parser = new DOMParser()
              const doc = parser.parseFromString(item.snippet.title, 'text/html')
              item.snippet.title = doc.body.innerText
            })
            
            // 3. state.videos 를 응답으로 바꾼다.
            // 1과 마찬가지 이유로 mutations에서 해당 코드를 실행시키는 코드를 작성한다.
            commit('setVideos', res.data.items)  //3)context.commit('setVideos', res.data.items)
          })
          .catch(err => console.error(err))
      }
    },
    modules: {}
  })
  ```

  

- state, getters,mutations,actions 모두 매핑이 가능하다. 각기 매핑되는 위치가 다르므로 공식문서 참고(6.8 1부 1:20분 경 참고)