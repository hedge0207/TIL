# 예외처리

- 예외 상황

  ```java
  package first;
  
  public class ExeptionExam {
  	
  	public static void main(String[] args) {
  		int a = 0;
  		int b = 10;
  		int c = b/a;
  		System.out.println(c);
          //Exception in thread "main" java.lang.ArithmeticException: / by zero
          //파이썬과 마찬가지로 0으로 나누려고 할 경우 Exception이 발생한다.
  	}
  }
  ```

  

- `try` - `catch` - `finally`

  - try: 에러가 발생할 수 있는 부분을 작성
  - catch: 예외 발생시 실행할 코드를 작성
    - 발생할 수 있는 예외 클래스의 이름과 예외 정보를 담을 변수명을 적는다.
    - 모든 예외 클래스는 `Exception` 클래스를 상속 받는다. 
    - 따라서 `catch(Exception 변수명)`과 같이 적으면 특정 예외가 아닌 모든 예외를 처리 할수 있다. 
    - 복수의 catch 블록을 작성할 수 있다.
  - finally: 예외 상황 발생 여부와 무관하게 실행할 코드를 작성, 생략 가능

  ```java
  package first;
  
  public class ExeptionExam {
  	
  	public static void main(String[] args) {
  		int a = 0;
  		int b = 10;
          
          try{
  		int c = b/a;
  		System.out.println(c);
          //catch는 아래와 같이 catch(발생할 수 있는 예외 클래스)형식으로 적는다. 변수에는 예외 내용이 들어가게 된다.
          //catch(Exception e)로 적으면 ArithmeticException 뿐 아니라 모든 예외가 여기서 걸리게 된다.
          }catch(ArithmeticException e){
              System.out.println(e);  
              //java.lang.ArithmeticException: / by zero
              System.out.println("0으로 나눌 수 없습니다."+e.toString());  
              //0으로 나눌 수 없습니다.java.lang.ArithmeticException: / by zero
          }finally {
          	System.out.println("어떤 경우든 실행되는 코드");
              //어떤 경우든 실행되는 코드
          }
  	}
  }
  ```

  

- Throws

  - 예외가 발생했을 경우 예외를 호출한 쪽에서 처리하도록 던져주는 것
  - `throws` 키워드를 사용하며 뒤에 예외 내용을 작성한다.
    - 하나만 작성할 수 있는 것은 아니고 ,로 구분하여 여러 예외를 throw 할 수 있다.
    - catch와 마찬가지로 모든 예외 클래스가 상속받는 `Exception` 클래스를 작성하면 모든 예외처리가 가능하다.

  ```java
  package first;
  
  public class ExceptionExam2 {
  	
  	//실제 예외가 발생하는 곳(0으로 나누게 되는 곳)은 main이 아닌 이 메소드에서 발생하게 된다.
      //그러나 여기서 예외를 바로 처리하지 않고 throws를 사용하여 예외를 호출한 main에서 예외처리를 하도록 할 수 있다.
      //아래의 경우 ArithmeticException하나만 적었지만 ,로 구분하여 다양한 예외를 throw 할 수 있다.
      //throws 예외1, 예외2
  	public static int divide(int a, int b) throws ArithmeticException{
  		int c = a/b;
  		return c;
  	}
  	
  	public static void main(String[] args) {
  		int i = 10;
  		int j = 0;
  		try {
  		int k = divide(i,j);
  		System.out.println(k);
  		}catch(ArithmeticException e) {
  			System.out.println(e);
  		}
  	}
  }
  
  ```

  

























