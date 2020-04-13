1. 태그

- 태그는 항상 여는 태그와 닫는 태그가 있어야 하며 태그에는 속성명과 속성 값을 넣을 수 있다.

  - 속성명과 속성값 사이에는 절대 공백을 사용하지 않는다.

- 시멘틱 태그: HTML5에서 등장한 의미론적 요소를 담은 태그, 이들은 div 태그를 쓰지 않고 아래와 같은 별도의 태그로 표현한다. 

  - header: 페이지 또는 섹션의 머릿글 그룹, 섹션 요소 그룹에서 소개하긴 하지만 섹션요소가 아니다. 따라서 새로운 섹션을 의미하지 않는다.
  - nav: 네비게이션 요소, 네비게이션 링크로 구성되는 섹션, 블로그 등의 페이지 삭제, 수정 등은 네비게이션 요소가 아니다.
  - aside: 문서의 주요 콘텐츠와 별개의 영역을 정의
  - section: 범용 섹션 요소, 일반적인 문서 또는 프로그램의 섹션
  - article: 독립적으로 배포 혹은 재사용 가능한 섹션, 독립적인 글(ex. 신문, 잡지, 기사 ,댓글 등)
  - footer: 가장 가까운 조상 요소의 footer, 일반적으로 연관 문서에 대한 정보를 담는다(작성자, 링크, 저작권 등), header와 마찬가지로 섹센 요소 그룹에서 소개하긴 하짐나 섹션요소가 아니다.
  - 헤딩: 섹션의 제목, h1~h6까지 존재 h1이 가장 높고 h6가 가장 낮다. HTML5부터는 꼭 h1부터 사용하지 않아도 무관하다. 섹션의 시작은 표시가 되지만 섹션의 끝은 표기 되지 않음
  - hgroup: 섹션의 제목 그룹(h1~h6 요소들을 그룹 짓기 위해 사용), hgroup은 포함된 헤딩 요소의 가장 높은 등급을 의미한다. 따라서 서브 타이틀 범주의 생성을 감추기 위해 사용한다.
  - address: 가장 가까운 조상 요소인 article 또는 body요소의 연락처 정보 의미
  - table

- a태그와 link태그, 이미지 태그

  - \<a>:  하이퍼링크를 의미, href속성으로 링크 경로를 지정, a요소가 href 속성을 가지면 추가로 target 속성을 지정할 수 있다. target 속성은 링크가 실행될 윈도우를 지정하는 속성으로 아래 4개 중 하나를 가진다.

    - _self: 현재의 웹 브라우저 창에서 링크가 열림
    - _parent: 현재의 웹 브라우저 창의 부모 창이 있다면 거기서 링크가 열림
    - _top: 최상위 웹 브라우저 창에서 링크가 열림
    - _blank: 새로운 웹 브라우저 창을 생성하고 링크가 열림

    ```html
    <a href="https://google.com"></a>
    a {
      text-decoration: none; <!--a태그를 설정했을 때 나타나는 밑줄과 색을 없애준다.-->
    }
    ```

  - link태그

    ```html
    <link rel="stylesheet" href="파일경로"> 
    <!--rel 뒤에는 불러올 링크의 종류가 오며 href뒤에는 파일명이 온다.-->
    ```

  - img태그

    ```html
    <img src="images/abc.png" alt="My Image">
    <!--src뒤에는 이미지 경로가, alt 뒤에는 지정한 경로에 이미지가 없을 경우 출력될 내용이 온다.-->
    ```

    

- 목록 관련 태그

  - 순서 있는 목록: 순서가 바뀌면 의미가 바뀌는 목록, 순서가 있기에 맨 앞에 숫자 또는 알파벳이 붙으며 이는 CSS로 정의한다.

    - \<ol>: 순서가 있는 목록 정의
    - \<li>: \<ol>의 자식 요소로 목록의 아이템 역할
    - type 어트리뷰트를 사용하여 순서를 나타내는 문자를 지정할 수 있다.
      - "1": 숫자, 기본값
      - "A": 알파벳 대분자
      - "a": 알파벳 소문자
      - "I": 로마숫자 대문자
      - "i": 로마숫자 소문자
    - start 어트리뷰트로 리스트의 시작값을 지정할 수 있다.
    - reveresed 어트리뷰트를 지정하면 리스트의 순서값을 역으로 표현한다.

    ```html
    <!--순서 있는 목록-->
    <!DOCTYPE html>
    <html>
      <body>
        <h2>순서있는 목록 (Ordered List)</h2>
        <ol>
          <li>Coffee</li>
          <li>Tea</li>
          <li>Milk</li>
        </ol>
      </body>
    </html>
    
    out
    순서있는 목록 (Ordered List)
    1.Coffee
    2.Tea
    3.Milk
    
    <!--type 사용-->
    <ol type="I">
      <li value="2">Coffee</li>
      <li value="4">Tea</li>
      <li>Milk</li>
    </ol>
    
    out
    Ⅱ.Coffee
    Ⅳ.Tea
    Ⅴ.Milk
    
    <!--start 사용-->
    <ol start="3">
      <li>Coffee</li>
      <li>Tea</li>
      <li>Milk</li>
    </ol>
    
    out
    3.Coffee
    4.Tea
    5.Milk
    
    <!--reversed 사용-->
    <ol reversed>
      <li>Coffee</li>
      <li>Tea</li>
      <li>Milk</li>
    </ol>
    
    out
    3.Coffee
    2.Tea
    1.Milk
    ```

    

  - 순서가 없는 목록: 목록 앞에 숫자 대신 말머리 기호가 나타남.

    - \<ul>: 순서 없는 목록 정의
    - \<li>: \<ul>의 자식 요소로 목록의 아이템 역할

    ```html
    <!--순서 없는 목록-->
    <!DOCTYPE html>
    <html>
      <body>
        <h2>순서없는 목록 (Unordered List)</h2>
        <ul>
          <li>Coffee</li>
          <li>Tea</li>
          <li>Milk</li>
        </ul>
      </body>
    </html>
    
    out
    순서없는 목록 (Unordered List)
    ●Coffee
    ●Tea
    ●Milk
    ```


- input태그, form 태그, label태그, textarea태그

  - form태그 : 아래의 모든 태그가 위치하는 태그로 입력 받은 내용을 어디로 보낼 것인지에 대한 내용을 담는다.

    ```html
    <!--action=""에 입력받은 것들을 보낼 곳을 지정한다.-->
    <form action=""></form>
    ```

  - input태그:입력을 받는 태그

    ```html
    <input type="text" id="username" placeholder="아이디 입력" required autofocus autocomplete="username">
    
    <!--
    id는 이후에 label태그를 위한 것, 
    required는 이 input이 입력되지 않으면 제출할 때 오류가 출력되는 것,
    autofocus는 창이 실행되자마자 커서가 자동으로 입력란에 위치하게 해주는 것,
    autocomplete는 '='뒤에 오는 id와 같은 id로 입력되었던 값들이 브라우저에 저장되어 있는데 이를 불러와 자동완성을 하게 해주는 기능이다.
    -->
    ```

  - label태그: label에 해당하는 영역을 클릭하면 input을 입력할수 있게 해준다.

    ```html
    <label class="required" for="username">사용자 이름</label>
    <input type="text" id="username">
    <!--위 코드의 경우 사용자 이름 아래에 입력창이 뜨게 되는데 이때 사용자 이름을 누르면 입력창에 입력이 가능해진다. 이점이 바로 다른 태그로 넣었을 때와의 차이점이다.-->
    <!--둘이 부모 관계가 아님에도 이게 가능한 이유는 바로 id때문이다. label에 있는 for와 input에 있는 id가 동일하다면 위 기능을 수행할 수 있다.-->
    ```

  - textarea태그: input과 비슷하지만 일반적으로 input보다 긴 값을 받을 때 사용한다.

- 텍스트 관련 태그
  - b태그와 strong태그: b태그는 단순 볼드체, strong은 의미론적 강조+볼드체
  - i태그와 em태그: i태그는 단순 이텔릭체, em태그는 의미론적 강조+이텔릭체
- 테이블 테그
  - tr(테이블 로우): 표 내부의 행
  - th(데이블 헤드): 행 내부의 제목 셀 
  - td(테이블 데이터): 행 내부의 일반 셀
  - thead,tbody,tfoot 등도 존재: 안써도 내용은 동일하게 출력되지만 이 역시 의미론적 중요성을 가지고 있는 태그로 thead의 자식요소로 th가, tbody의 자식요소로 td가, tfoot의 자식 요소로 (주로)마지막 줄의 td(합계, 평균 등)가 들어간다. 그리고 당연히 셋 모두 공통적으로 tr을 자식요소로 가진다.



2. 상속

- 부모의 높이는 자식의 content의 높이가 된다.
- 상속 되는 것: Text 관련 요소(폰트, 컬러, text-align 등), opacity, visibility 등
- 상속 되지 않는 것: box model(widht, heigth, margin, padding, border, box-sizing, display 등), position(top, bottom,right, left, z-index 등)



3. CSS 적용 우선순위(cascading order)

- 중요도-우선순위(인라인-id선택자-class선택자-요소 선택자)-소스 순서
  - 소스 순서는 정의된 순서로, 나중에 정의된 요소가 적용된다.
  - 태그에 할당된 순서와는 무관하다.



4. Box-model

- 마진 상쇄
  - 형제 요소 간의 마진은 겹쳐서 보이게 된다. 예를 들어 두 박스를 위 아래로 배치하고 각각의 top, bottom마진을 30px로 줬을 때윗 박스의 top마진과 아랫 박스의 bottom마진은 30px가 제대로 들어가게 되는데 둘 사이에 있는 공간의 margin은 60px가 되지 않고 이보다 작은 값이 나오게 된다.



5. 블록과 인라인 레벨요소

- 대표적 요소들
  - 블록 레벨에 속하는 요소들: div / ul,ol,li / p / hr / form

  - 인라인 레벨에 속하는  요소들: span / a / img / input,label / b, i, strong, em
- 특징

  - 블록
    - 줄 바꿈이 일어나는 요소
    - 화면 크기 전체의 가로폭을 차지: content를 벗어나는 가로폭을 전부 마진처리 한다.
    - 블록 레벨 요소 안에 인라인 레벨 요소가 들어갈 수 있음
  - 인라인
    - 줄 바꿈이 일어나지 않는 행의 일부 요소
    - content 넓이 만큼 가로 폭을 차지
    - width, height, margin-top, margin-bottom을 지정할 수 없다.
    - 상하여백은 line-heigth로 지정한다.
- 수평정렬

  - 블록
    - 좌측: margin-right: auto; 를 넣으면 콘텐츠를 맨 좌측에 배치하고 콘텐츠 우측을 전부 마진처리
    - 우측: margin-left: auto; 를 넣으면 콘텐츠를 맨 우측에 배치하고 콘텐츠 좌측을 전부 마진처리
    - 중앙: margin-right: auto; 와 margin-left: auto; 륻 동시에 쓰면 콘텐츠를 중앙에 배치하고 콘텐츠 좌우측을 전부 마진처리
  - 인라인
    - 좌측: text-align: left;
    - 우측: text-align: right;
    - 중앙: text-align: center;
- 수직 정렬
  - 블록
    - 구글링 하면 다양한 방법이 나오지만 그냥 flex를 쓰는 것이 가장 편하다.
  - 인라인
    - vertical-align은 inline 요소에 대하여 활용 가능. line-height가 부여되어 있어, 그 길이를 기준으로 가운데로 맞출 수 있음.
- 인라인 블록: 블록과 인라인의 특성을 모두 가짐

  - 처럼 한 줄에 표시 가능
  - 블록처럼 width, height, margin 속성 지정 가능
- 박스 내부의 텍스트 수직, 수평 정렬: 수직 정렬은 line-height를 박스의 높이 만큼 주면 되고, 수평 정렬은 text-align을 통해 가능하다.



6. 기타 레이아웃

- 포지션

  - static: 
    - 좌표 프로퍼티를 사용하여 이동이 불가능
    - 디폴트 값
    - 기준이 되는 위치
    - 기본적인 요소의 배치 순서에 따른다(좌측상단)
    - 부모 요소 내에 배치될 때는 부모 요소의 위치를 기준으로 배치됨
  - relative
    - static 위치를 기준으로 이동
    - 자신의 위치를 유지한 채로 움직인다. 즉, 이동하기 전의 위치에 다른 요소가 올 수 없다.
  - absolute
    - 조상 요소 중 static이 아닌 것을 기준으로 이동(따라서 큰 박스 안에서 작은박스로 absolute 박스를 이동하고자 할 때에는 부모 요소인 큰 박스에 relative를 지정해줘야 한다.)
    - 조상 요소 중 static이 아닌 것이 없을 경우 HTML을 기준으로 이동
    - 자신의 위치를 지우고 움직인다. 즉, 이동하기 전의 위치에 다른 요소가 올 수 있다.
    - 일반적으로 박스 위에 다른 박스를 올릴 때에만 사용한다(relative로 움직인 박스 위에 absolute박스가 올 수 있다.).
  - fixed
    - 스크롤이 움직이더라도 화면에 고정됨, 부모 요소가 아닌 브라우저를 기준으로 위치가 결정된다.

- float

  - 일반적인 흐름에서 벗어나도록 하는 속성 중 하나

  - 모든 것은 박스 모델이고, 좌측 상단부터 배치되는 것이 기본인데 float은 이 일반적인 틀을 깬다.

  - 반드시 clear 속성을 통해 초기화가 필요하며 예상치 못한 상황이 발생할 수 있음

    - clear: both;를 해주지 않으면 float을 지정한 요소와 한 줄에 위치하게 된다. 따라서 다음 줄에 배치하고자 하는 요소에 clear: both속성을 넣어줘야 한다.

    - 또한 clear를 해주어서 float을 지정한 요소 아래로 위치하게 된다 하더라도 마진이 제대로 표현되지 않는 문제가 존재한다.

    - 일반적으로 부모 요소의 높이는 자식 컨텐츠의 높이와 같은데 float의 경우 높이가 없는 것으로 취급되어 float의 부모 요소는 높이를 갖지 않게 된다.

    - 이를 해결하는 방법

      -의사(가상) 요소 선택자

       ```css
      비어있는 내용으로 블록을 만들고 그걸 clear하겠다는 의미
      .clearfix::after {
        content: "";
        display: block;
        clear: both;
      }
       ```

  - float을 사용하는 경우 block 사용을 뜻하며, display 값이 inline인 경우 block으로 계산한다.

  - 왼쪽 정렬과 오른쪽 정렬 기능만 있고 중앙 정렬은 따로 구현을 해야한다.



- flex: 배치를 훨씬 쉽게 해준다.

  - 기본적으로 부모 요소(일반적으로  container라 부른다.) 하부에 다양한 자식 요소(items)를 정렬하는데 쓰인다.

  - 부모 요소에 반드시 적용해줘야 하는 속성

    ```css
    /*부모요소에 반드시 지정해줘야 한다.*/
    display:flex;
    
    /*부모요소가 inline 요소인 경우 위처럼 쓰지 않고 아래와 같이 쓴다.*/
    display:inline-flex;
    ```

  - 부모요소에 선택적으로 적용해주는 속성

    - flex-direction

      ```css
      /*좌에서 우로(ltr) 수평 배치, 기본값*/
      flex-direction:row;
      
      /*우에서 좌로(rtl) 수평 배치*/
      flex-direction:row-revers;
      
      /*위에서 아래로 수직 배치*/
      flex-direction: column;
      
      /*아래에서 위로 수직 배치*/
      flex-direction: column-reverse;
      ```

    - flex-wrap

      ```css
      /*flex item을 개행하지 않고 1행에 배치, 기본값*/
      flex-wrap: nowrap;
      
      /*각 flex item의 폭은 flex container에 들어갈 수 있는 크기로 축소된다. 하지만 flex item들의 width의 합계가 flex 컨테이너의 width보다 큰 경우 flex 컨테이너를 넘치게 된다. 이때 overflow: auto;를 지정하면 가로 스크롤이 생기며 컨테이너를 넘치지 않는다.*/
      /*flex item들의 width의 합계가 flex 컨테이너의 width보다 큰 경우, 복수행에 배치*/
      flex-wrap: wrap;
      
      /*flex-wrap: wrap;과 동일하나 아래에서 위로 배치된다.*/
      flex-wrap: wrap-reverse;
      ```

    - flex-flow

      ```css
      /*flex-direction 속성과 flex-wrap 속성을 동시에 설정*/
      flex-flow: <flex-direction> || <flex-wrap>;
      ```

    - justify-content: flex container의 main axis를 기준으로 flex item을 수평 정렬한다.

      ```css
      /*main start(좌측)를 기준으로 정렬, 기본값*/
      justify-content: flex-start;
      
      /*main end(우측)를 기준으로 정렬*/
      justify-content: flex-end;
      
      /*flex container의 중앙에 정렬*/
      justify-content: center;
      
      /*첫번째와 마지막 flex item은 좌우 측면에 정렬되고 나머지와 균등한 간격으로 정렬된다.*/
      justify-content: space-between;
      
      /*모든 flex item은 균등한 간격으로 정렬된다.*/
      justify-content: space-around;
      ```
    
    - align-content: flex container의 cross axis를 기준으로 flex item을 수직 정렬한다.
    
  ```css
      /*모든 flex item은 flex item의 행 이후에 균등하게 분배된 공간에 정렬되어 배치, 기본값*/
      align-content: stretch;
      
  /*모든 flex item은 flex container의 cross start 기준으로 stack 정렬된다.*/
      align-content: flex-start;
      
  /*모든 flex item은 flex container의 cross end 기준으로 stack 정렬된다.*/
      align-content: flex-end;
      
  /*모든 flex item은 flex container의 cross axis의 중앙에 stack 정렬된다.*/
      align-content: center;
      
  /*첫번째 flex item의 행은 flex container의 상단에 마지막 flex item의 행은 flex container의 하단에 배치되며 나머지 행은 균등 분할된 공간에 배치 정렬*/
      align-content: space-between;
      
      /*모든 flex item은 균등 분할된 공간 내에 배치 정렬된다.*/
      align-content: space-around;
  ```
  
    - align-items: flex item을 flex container의 수직 방향(cross axis)으로 정렬
    
      ```css
      /*모든 flex item은 flex container의 높이(cross start에서 cross end까지의 높이)에 꽉찬 높이를 갖는다. 기본값*/
      align-items: stretch;
      
      /*모든 flex item은 flex container의 cross start 기준으로 정렬된다.*/
      align-items: flex-start;
      
      /*모든 flex item은 flex container의 cross end 기준으로 정렬된다.*/
      align-items: flex-end;
      
      /*모든 flex item은 flex container의 cross axis의 중앙에 정렬된다.*/
      align-items: center;
      
      /*모든 flex item은 flex container의 baseline을 기준으로 정렬된다.*/
      align-items: baseline;
      /**/
      ```
  
    
  
  - 자식요소에 주는 속성
  
    - order : flex item의 배치 순서를 지정한다. 기본값은 0
  
      ```css
      order: 정수값;
      ```
  
    - align-self :  align-items 속성보다 우선하여 개별 flex item을 정렬한다. 기본값은 auto
  
      ```css
      align-self: auto | flex-start | flex-end | center | baseline | stretch;
      ```
  
      















