# Pointer

- 아래와 같이 변수를 선언했을 때,  변수는 어디에 저장되는가?
  ```c
  int num = 1;
  ```
  
  - 변수는 컴퓨터의 메모리에 저장된다.
    - 메모리에 일정 공간을 확보하고,  그 곳에 원하는 값을 저장하거나, 그곳으로부터 저장된 값을 불러온다.
  - 변수가 저장된 메모리의 주소값 알아보기
    - 변수명 앞에 주소 연산자 `&`를 붙이면 해당 변수의 16진수로 이루어진 주소값을 가리키게 된다.
    - 출력할 때는 point의 약어인 `%p`를 사용하여 출력한다(주소값은 16진수이므로 `%X`로 출력해도 된다).
    - 아래 코드를 실행한 컴퓨터는 64bit이므로 16진수 16자리가 나온다.
  
  ```c
  #include <stdio.h>
  
  int main()
  {
      int num = 1;
  
      printf("%p\n", &num1);    // 000000EBF736FBC4: num의 메모리 주소
      // 실행할 때마다 달라진다.
  
      return 0;
  }
  ```



- Pointer

  - 위에서 살펴본 메모리의 주소값을 저장하는 변수를 pointer(혹은 pointer variable)라 부른다.
    - char형 변수가 문자를 저장하고, int형 변수가 정수를 저장하는 것처럼 포인터는 주소값을 저장한다.
  - pointer는 아래와 같이 `*`를 사용하여 선언한다.
    - pointer `numPt`에는 `num`의 주소값이 저장된다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int* numPt;      // pointer 선언
      int num = 10;
  
      numPt = &num;   // num의 주소값을 numPt에 저장
     
      // numPt와 num의 주소값은 같다.
      printf("%d\n", numPt == &num);		// 1
  
      return 0;
  }
  ```

  - pointer 선언 시에 `*`를 type 쪽에 붙이든, 변수명에 붙이든, 그 사이에 붙이든 차이는 없다.
    - `자료형 *`부분은 pointer to type 이라고 읽는다.
    - 즉 아래의 경우 pointer to int라고 읽으면 된다. 

  ```c
  // 아래는 모두 같다.
  int* numPt;
  int * numPt;
  int *numPt;
  ```

  - pointer 선언시에 앞에 붙여주는 type은 주소가 가리키는 변수의 type에 맞춰야한다.
    - 만일 boolean type 변수의 주소값을 저장하려면 아래와 같이 bool type으로 선언해야한다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      bool* boolPt;
      bool foo = true;
  
      numPt = &foo;
  
      printf("%p\n", numPt);    
      printf("%p\n", &foo);
      printf("%d\n", numPt == &foo);
  
      return 0;
  }
  ```

  - 어차피 모든 pointer는 주소값이라는 고정된 type의 값을 저장하는데 굳이 type을 지정해주는 이유는 무엇인가?
    - type마다 차지하는 메모리의 크기가 다르기 때문이다.



- 역참조하기

  - 만일 pointer에 저장된 주소값에 저장된 값을 가져오려고 한다면 역참조 연산자 `*`를 사용한다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int *numPt;
      int num = 29;
  
      numPt = &num;
  	
      // 역참조 연산을 통해 주소에 해당하는 값을 받아온다.
      printf("%i\n", *numPt);  // 29
  
      return 0;
  }
  ```

  - pointer 변수의 선언과 역참조에 모두 `*`가 사용되어 헷갈릴 수 있으나, 선언과 사용을 구분하여 생각하면 된다.
    - 선언시의 `*`는 pointer를 선언하겠다는 의미이다.
    - 사용시의 `*`는 역참조를 통해 포인터가 가리키는 주소값에 해당하는 값을 가져오겠다는 의미이다. 

  - 역참조 연산자를 사용한 뒤 값을 저장하기

  ```c
  #include <stdio.h>
  
  int main()
  {
      int *numPt;
      int num = 29;
  
      numPt = &num;
      
  	// 역참조 연산자를 사용하여 값을 불러온 뒤 해당 값에 30을 저장한다.
      *numPt = 30;
  	
      // num의 값도 함께 변한다.
      printf("%i\n", num);  //30
  
      return 0;
  }
  ```

  - `*`로 선언한 pointer 변수는 주소를 저장하는 pointer type이고, `*`를 사용한 pointer 변수는 pointer에 저장된 주소가 가리키고 있는 값의 type이다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int *numPt;
      int num = 29;
  
      numPt = &num;
      
  	// *numPt는 num의 type인 int type을 따르므로 주소값인 &num을 저장할 수 없다.
      *numPt = &num;
  
      return 0;
  }
  ```



- pointer와 상수

  - pointer에도 const keyword를 붙일 수 있다.
    - 붙이는 위치에 따라서 의미가 달라진다.
  - 상수를 가리키는 pointer(pointer to constant)
    - `*` 앞에 const keyword를 입력한다.

  ```c
  const int num = 10;    // int형 상수
  const int *numPtr;     // int형 상수를 가리키는 포인터. int const *numPtr도 같다.
  ```

  - 상수인 pointer(constant pointer)
    - `*` 뒤에 const keyword를 둔다.

  ```c
  int num1 = 10;    // int형 변수
  int num2 = 20;    // int형 변수
  int * const numPtr = &num1;    // int형 포인터 상수
  
  // 상수 pointer의 주소값을 바꿀 수 없으므로 error가 발생
  numPtr = &num2;	
  ```

  - 상수를 가리키는 상수인 pointer(constant pointer to constant)
    - `*`의 앞뒤로 const keyword를 입력한다.

  ```c
  const int num1 = 10;    // int형 상수
  const int num2 = 20;    // int형 상수
  // int형 상수를 가리키는 포인터 상수
  const int * const numPtr = &num1;    // int const * const numPtr도 같다.
  
  *numPtr = 30;      // num1이 상수이므로 역참조로 값을 변경할 수 없다.
  numPtr = &num2;    // 상수 pointer의 주소값을 바꿀 수 없으므로 error가 발생
  ```



- void pointer

  - 자료형이 정해져있지 않은 pointer
    - 범용 pointer라고도 한다.
    - `void *pointerName` 형태로 선언한다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int num = 29;
      char c = 'a';
      int* intPt = &num;
      char* cPt = &c;
  
      void* ptr;        // void 포인터 선언
  
      // 포인터 자료형이 달라도 컴파일 경고가 발생하지 않음
      ptr = intPt;    // void 포인터에 int 포인터 저장
      ptr = cPt;      // void 포인터에 char 포인터 저장
      
      // 반대의 경우도 마찬가지다.
      // intPt = ptr;
      // cPt = ptr
  
      return 0;
  }
  ```

  - 값을 가져오거나 저장할 때 크기가 정해져있지 않으므로 역참조는 불가능하다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int num = 29;
  
      void* ptr = &num;
  
      printf("%i\n", *ptr);	// error C2100: 간접 참조가 잘못되었습니다.
      
  
      return 0;
  }
  ```



- 이중 pointer

  - pointer도 변수이기에 메모리상에 주소를 갖는다.
    - pointer의 pointer를 이중 pointer라 부르며 `**`를 사용하여 선언한다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int num = 29;
  
      int *ptr1 = &num;
      // pointer의 pointer를 선언
      int **ptr2 = &ptr1;
  	
      // 역참조 할 때도 마찬가지로 역참조 연산자를 두 번 쓴다.
      printf("%i\n", **ptr2);
  
      return 0;
  }
  ```

  - 삼중, 사중, 그 이상으로 중첩하여 사용하는 것도 가능은 하다.



- 배열과 pointer

  - 배열은 사실 첫 번째 요소의 주소값만을 갖고 있다.
    - 즉 배열이 가지고 있는 값은 주소값이다.
    - 따라서 포인터에 할당이 가능하다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int numArr[5] = { 0, 1, 2, 3, 4};    // 크기가 5인 int형 배열
  
      int* numPtr = numArr;       // 포인터에 int형 배열의 주소값을 할당
      return 0;
  }
  ```

  - 배열의 주소를 저장하고 있는 pointer를 역참조하면 배열의 첫 번째 요소에 접근한다.
    - 사실 배열 자체가 첫 번째 요소의 주소값이니 당연한 결과다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int numArr[5] = { 0, 1, 2, 3, 4};    // 크기가 5인 int형 배열
  
      int* numPtr = numArr;       // 포인터에 int형 배열의 주소값을 할당
  
      // 배열의 주소가 들어있는 포인터를 역참조
      printf("%d\n", *numPtr);    // 0, 배열의 첫 번째 요소에 접근한다. 
      // 배열 자체를 역참조
      printf("%d\n", *numArr);    // 0, 배열 자체를 역참조해도 배열의 첫 번째 요소에 접근한다. 
      
      return 0;
  }
  ```

  - 아래와 같이 pointer에서 인덱스로 배열의 요소에 접근하는 것도 가능하다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int numArr[5] = { 0, 1, 2, 3, 4};    // 크기가 5인 int형 배열
  
      int* numPtr = numArr;       // 포인터에 int형 배열의 주소값을 할당
       
      printf("%d\n", numPtr[4]);  // 4: 배열의 주소가 들어있는 포인터는 인덱스로 접근할 수 있다. 
  
      return 0;
  }
  ```

  - 둘의 차이는 `sizeof`로 크기를 계산했을 때 드러난다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      int numArr[5] = { 0, 1, 2, 3, 4};    // 크기가 5인 int형 배열
  
      int* numPtr = numArr;       // 포인터에 int형 배열을 할당
  
      // sizeof로 배열의 크기를 구하면 배열이 메모리에서 차지하는 공간이 출력된다.
      printf("%d\n", sizeof(numArr));
      // sizeof로 배열의 주소가 들어있는 포인터의 크기를 구하면 포인터의 크기가 출력된다.(64비트라면 8)
      printf("%d\n", sizeof(numPtr));    
  
      return 0;
  }
  ```



- 2차원 배열에서의 pointer

  - 2차원 배열에서의 pointer는 `type (*pointerName)[size]`형태로 선언한다.
    - size에는 내부 배열의 크기를 입력한다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      // 세로 크기 3, 가로 크기 4인 int형 2차원 배열 선언
      int numArr[3][4] = {    
          { 11, 12, 13, 14 },
          { 21, 22, 23, 24 },
          { 31, 32, 33, 34 }
      };
  
      int (*pt)[4] = numArr;
      
      // 둘의 역참조 결과는 첫 번째 내부 리스트의 주소 값이다.
      printf("%i\n", *pt == *numArr);
  
      return 0;
  }
  ```

  - 괄호를 붙였을 때와 붙이지 않았을 때 뜻이 완전히 달라지므로 반드시 붙여야한다.
    - 괄호를 붙이지 않으면 size 만큼의 pointer를 담을 배열을 선언하는 것이다.

  ```c
  // int type의 pointer 4개를 가질 수 있는 배열을 선언
  int *pt[4];
  
  // int type으로 구성된 크기가 4인 배열의 주소를 저장할 pointer를 선언
  int (*pt)[4]
  ```

  - 1차원 배열과 마찬가지로 pointer에서 index로 요소에 접근할 수 있다.

  ```c
  #include <stdio.h>
  
  int main()
  {
      // 세로 크기 3, 가로 크기 4인 int형 2차원 배열 선언
      int numArr[3][4] = {    
          { 11, 12, 13, 14 },
          { 21, 22, 23, 24 },
          { 31, 32, 33, 34 }
      };
  
      int (*pt)[4] = numArr;
      
      printf("%i\n", pt[0][3]);	// 14
  
      return 0;
  }
  ```

  







