# Python의 memory 관리 방식

> https://realpython.com/python-memory-management/#garbage-collection
>
> https://www.honeybadger.io/blog/memory-management-in-python/#authorDetails

> 아래 내용은 모두 CPython 기준이다.

- Python의 모든 것은 객체이다.
  - Python에 원시타입은 존재하지 않으며 모든 것은 객체로 존재한다.
  - Python의 모든 객체는 C로 구현된 `PyObject`라는 struct를 기반으로 한다.
    - Struct는 객체지향에서의 class 같은 개념으로, 메서드가 존재하지 않고 attribute만 존재하는 class라 생각하면 된다.
  - `PyObject`는 단 두가지 attribute만 가지고 있다.
    - `ob_refcnt`: 객체가 reference된 횟수
    - `ob_Type`: 실제 type에 대한 pointer(pointer 역시 C에 존재하는 개념이다)
  - `ob_refcnt`는 garbage collection에 사용된다.



- Memory management
  - Memory management는 어떤 애플리케이션이 data를 읽고 쓸지를 결정하는 절차이다.
    - Memory manager가 어떤 애플리케이션의 데이터를 언제, 어디에, 어떻게 넣을지를 결정한다.
    - Memory의 할당과 할당 받은 memory에 data를 저장하는 것은 별개의 과정이다.
  - Python code상의 객체가 hardware(memory 혹은 hard drive)에 도달하기 까지 많은 추상 계층이 존재한다.
    - 주요 계층 중 하나는 OS이다.
    - OS는 물리 메모리를 추상화하고, 가상 메모리 계층을 생성한다.
    - OS Virtual Memory Manager(VMM)은 가상 메모리 계층에 애플리케이션을 위한 공간을 할당한다.
    - 애플리케이션은 OS가 할당해준 가상 메모리 계층에 접근한다.



- Private heap
  - Python은 OS로부터 Python process가 독점점으로 점유하는 private heap 영역을 할당받는다.
  - Private heap은 아래 4개의 영역으로 나뉜다.
    - Python Core Non-object memory: Python core에 있는 non-object data들을 위한 영역
    - Internal Buffers: internal buffer를 위한 영역
    - Object-specific memory: object-specific memory allocator를 지닌 object들을 위한 영역
    - Object memory: objects들을 위한 영역
  - 각 영역은 필요에 따라 동적으로 더 커지거나 줄어들 수 있다.



- Memory Allocator
  - Python memory를 관리하기 위해 CPython에 정의된 memory 관리자이다.
  - `malloc`과 `free` 메서드가 너무 자주 호출되는 것을 방지하기 위해 allocator의 계층을 두었다.
    - `malloc`은 메모리를 할당, `free`는 메모리를 반환하는 메서드이다.
  - General Purpose Allcator
    - CPython의 `malloc`  메서드이다.
    - OS의 virtual memory manager와 상호작용하여, memory를 할당받는 역할을 한다.
    - OS의 virtual memory manager와 상호작용하는 유일한 allocator이다.
  - Raw memory Allocator
    - 512bytes 보다 큰 object를 위한 allocator.
    - General purpose allocator의 추상화를 제공한다(즉, malloc 메서드의 추상화를 제공한다).
    - Python process가 memory를 필요로하면, general purpose allocator와 상호작용하여, memory를 할당받는다.
    - Python process 전체에서 필요로하는 만큼의 충분한 memory가 있는지 확인하는 역할을 한다.
  - Object Allocator
    - 512bytes 이하의 object를 위한 allocator.
    - `pymalloc`이라고도 불린다.
  - Object-specific Allocatiors
    - 특정 data type을 위한 allocator.
    - integer, float, string, list 등의 data type은 각기 저마다의 allocator를 가지고 있다.
    - type별로 allocator가 다르게 구현되어 있다.
  - Object allocator와 object-specific allocatiors는 raw memory allocator가 할당 받은 memory 위에서 동작한다.
    - 이 두 개의 allocator는 절대 OS에 memory의 할당을 요청하지 않는다.
    - 만일 두 개의 allocator가 보다 많은 memory를 필요로 할 경우, raw memory allocator가 general-purpose allocator와 상호작용하여 memory를 요청하고, general-purpose allocator는 OS와 상호작용하여 memory를 받아온다.
  - Allocator가 선택되는 과정
    - Memory가 필요해진다.
    - object specific allocator가 존재하면, object specific allocator를 사용한다.
    - 존재하지 않을 경우 요구되는 memory가 512bytes 보다 큰지 확인한다.
    - 512bytes 보다 클 경우 raw memory allocator를 사용한다.
    - 512bytes 이하일 경우 object allocator를 사용한다.



## Object Allocator

- Object Allocator

  - 상기했듯 512bytes 미만의 object에 memory를 할당하는 allocator이다.
  - 만일 작은 크기의 object가 memory를 요청하면 해당 객체를 위한 memory를 할당하는 대신, 큰 크기의 memory chunk를 할당하고, 해당 block에 작은 객체를 저장한다.
    - 이를 통해 매번 객체가 생성될 때마다 memory 할당을 위해 `malloc`이 호출되는 것을 피할 수 있다.
  - Arena
    - Object Allocator가 할당 받은 큰 크기의 memory chunk를 **Arena**라 부른다.
    - 하나의 Arena는 256kb이다.
  - Pool
    - Arena를 효율적으로 사용하기 위해서 CPython은 Arena를 여러 개의 **Pool**로 분할한다.
    - 하나의 Pool의 크기는 [virtual memory page](https://en.wikipedia.org/wiki/Page_(computer_memory))의 크기와 같다.
    - 대부분의 경우 virtual memory page의 크기는 4kb이므로, 대부분의 Pool 역시 4kb이다.

  - Block
    - Pool은 다시 여러 개의 **Block**으로 나뉜다.
    - Object allocator가 object에 할당할 수 있는 가장 작은 크기의 memory 단위이다.



- Block

  - 하나의 object는 여러 block에 걸쳐서는 할당될 수 없고, 하나의 block에만 할당된다.
    - 하나의 Block의 크기는 가변적(최소 크기는 8kb, 최대 크기는 512kb)이며, 동일한 Pool 내에 있는 Block의 크기는 모두 동일하다.
  - 각 block의 크기는 **Size Class**라고도 불린다.
    - 예를 들어 아래 보이는 것과 같이 size class가 0인 block은 8bytes의 크기를 가지고, size class가 4인 block은 40의 크기를 가진다.
    - 하나의 block에는 object 전체가 할당되거나, 할당되지 않거나 둘 중 하나이다. 따라서 예를들어, 41 bytes의 memory가 필요하다면, 7bytes가 남더라도 48bytes짜리 block에 저장해야 한다.

  ```c
   // CPython의 source code에서 발췌
   /*
   * For small requests we have the following table:
   *
   * Request in bytes     Size of allocated block      Size class idx
   * ----------------------------------------------------------------
   *        1-8                     8                       0
   *        9-16                   16                       1
   *       17-24                   24                       2
   *       25-32                   32                       3
   *       33-40                   40                       4
   *       41-48                   48                       5
   *       49-56                   56                       6
   *       57-64                   64                       7
   *       65-72                   72                       8
   *        ...                   ...                     ...
   *      497-504                 504                      62
   *      505-512                 512                      63
   *
   *      0, SMALL_REQUEST_THRESHOLD + 1 and up: routed to the underlying
   *      allocator.
   */
  
  /*==========================================================================*/
  ```

  - Block은 3가지 상태를 가진다.
    - untouched는 아직 data가 할당된 적 없으며, memory를 할당 받은 적도 없는 상태이다.
    - free는 data가 할당된 적이 있으나, 현재는 할당이 해제되어 아무런 data도 저장하고 있지 않은 상태이다.
    - allocated는 data가 저장되어 있는 상태이다.
  - free 상태의 경우, data는 담고있지 않지만, OS로 부터 할당 받은 memory는 계속 가지고 있다.
    - 즉, block에서 data가 지워졌다고 해서 해당 block이 할당 받은 memory까지 반환하는 것은 아니다.
    - memory는 반환하지 않고 할당 받은 채로 유지하고 있다가, 새로운 데이터가 들어오면 새로 할당을 요청하지 않고, 바로 data를 저장한다.
  - `freeblock` pointer는 free 상태인 memory block들의 linked list를 가리킨다.
    - 즉, data를 저장할 수 있는 block들이 저장된 list를 가리키고 있다.
  - 가용한 free block 보다 많은 양의 memory가 필요해질 경우에만, allocator는 untouched 상태인 block에 memory를 할당한다.
    - 즉, allocator는 memory가 실제로 필요해지기 전에는 memory를 할당하지 않도록 디자인 되어 있다.



- Pool

  - Pool은 현재 Arena에 가용한 Block을 가진 Pool이 없을 때, 새로 생성된다.
  - Pool의 생성과 함께 Block도 생성된다.
    - 단, 모든 Block이 한 번에 생성되는 것은 아니다.
    - 처음에는 단 2개의 Block만이 생성되며, 이후 필요(memory)에 따라 하나씩 더 생성된다.

  - Pool은 Used, Full, Empty 세 가지 상태중 하나의 상태를 가진다.
    - Used는 할당에 사용할 수 있는 block을 가지고 있는 상태이다.
    - Full은 pool 내의 모든 block이 모두 할당되어 더 이상 여유 공간이 없는 상태이다.
    - Empty는 pool 내의 모든 block이 사용 가능한 상태이다. 아직 size class도 정해져 있지 않아, 어떤 size class의 block도 할당할 수 있다.
  - Pool의 source code

  ```c
  struct pool_header {
      union { block *_padding;
              uint count; } ref;          /* number of allocated blocks    */
      block *freeblock;                   /* pool's free list head         */
      struct pool_header *nextpool;       /* next pool of this size class  */
      struct pool_header *prevpool;       /* previous pool       ""        */
      uint arenaindex;                    /* index into arenas of base adr */
      uint szidx;                         /* block size class index        */
      uint nextoffset;                    /* bytes to virgin block         */
      uint maxnextoffset;                 /* largest valid nextoffset      */
  };
  ```

  - 같은 size class를 가진 다른 pool들과 doubly linked list로 연결되어 있다.
    - 이를 통해 서로 다른 pool 사이에서도 block size에 맞는 pool을 쉽게 찾을 수 있게 된다.
    - 위 코드에서 `nextpool` pointer가 같은 size class를 가진 다음 pool을 가리키고, `prevpool` pointer가 이전 pool을 가리킨다.
  - `freeblock` pointer
    - `freeblock` pointer는 pool 내의 가용한 block들의 정보가 저장된 linked list를 가키리고 있다.
  - `usedpools` list에는 사용 가능한 공간을 가지고 있는 pool들의 정보가 저장되어 있다.
    - `usedpools` list의 각 index는 class size와 동일하다.
    - 예를 들어 `usedpool[0]`에는 size class가 0인 pool들이 저장되어 있다.
    - 만일 특정 block size의 data를 저장해야 할 경우  `usedpools`를 확인하여 해당 block size와 일치하는 pool을 찾아낸다.

  - `freepools` list는 empty 상태인 pool들에 대한 정보를 저장하고 있다.
    - empty pool이 최초로 memory를 할당 받는 과정은 다음과 같다.
    - 8byte 짜리 block이 필요한 데이터가 들어온다.
    - `usedpools`에서 8bytes짜리 block을 가진 pool을 찾는다. 
    - 만일 8bytes짜리 block을 가진 pool이 존재하면 해당 pool에 저장한다.
    - 만일 존재하지 않는다면, `freepools`에 있는 pool들 중 하나를 선택하여 block size를 8 bytes로 설정하여 memory를 할당 받는다. 
    - 해당 block에 data를 저장 후, `freepools`에서 `usedpools`로 옮겨진다.

  - full 상태였던 pool에서 일부 block이 가용한 상태가 되면 다시 `usedpools` list에 추가된다.



- Arena

  - 작은 크기의 object가 memory를 요청했을 때, 해당 memory만큼의 가용 공간을 가진 arena가 없다면, raw memory allocator는 OS에 256kb의 memory를 요구한다.
  - source code

  ```c
  struct arena_object {
      /* The address of the arena, as returned by malloc */ 
      uintptr_t address;
  
      /* Pool-aligned pointer to the next pool to be carved off. */
      block* pool_address;
  
      /* The number of available pools in the arena:  free pools + never-
       * allocated pools.
       */
      uint nfreepools;
  
      /* The total number of pools in the arena, whether or not available. */
      uint ntotalpools;
  
      /* Singly-linked list of available pools. */
      struct pool_header* freepools;
  
      struct arena_object* nextarena;
      struct arena_object* prevarena;
  };
  ```

  - `freepools` pointer는 가용한 상태(empty or used 상태인 pool들)인 pool들에 대한 정보가 담긴 list를 가리킨다.
    - `nfreepools`은 arena에 있는 가용한 상태인 pool들의 숫자이다.

  - Arena는 `usable_arenas`라는 doubly linked list에 의해 관리된다.
    - `usable_arenas`에는 arena들에 대한 정보가 가용한 pool들의 정보와 함께 저장되어 있다.
  - `usable_arenas`는 arena별로 `nfreepools`에 따라 오름차순으로 정렬된다.
    - 즉, 가용한 상태인 pool의 개수가 적을 수록 list의 앞에 오게 된다.
    - 이는 가용한 상태인 pool의 개수가 적은 arena에 새로운 data가 먼저 저장된다는 것을 의미한다.
  - free 상태인 pool의 개수가 적은 arena에 새로운 data가 먼저 저장되는 이유
    - Arena는 pool, block과 달리 memory에 저장된 data가 삭제될 경우(즉 arena의 경우 모든 pool이 empty 상태가 될 경우), 실제로 OS로부터 할당받은 memory를 다시 OS에 반환한다(pool과 block의 경우 data가 삭제된다고 memory를 반환하지는 않는다).
    - 이를 통해 뒤에 있는 pool 들에는 memory를 할당하지 않게 되어, 전체 메모리를 감소시킬 수 있게 된다.



- Python Process는 Memory를 반환하는가?
  - Object를 저장하고 있던 Block이 free 상태가 되어도, CPython은 OS에 memory를 반환하지 않는다.
    - 심지어 Pool 내의 모든 Block이 free 상태가 되어도, CPython은 OS에 memory를 반환하지 않는다.

  - CPython은 Arena 단위로 메모리를 반환한다.
    - 따라서 CPython은 되도록 기존에 할당받았으나 반환하지 않은 메모리에 Object를 할당하며, 정말 필요할 때만 새로운 메모리를 요구한다.
    - 이것이 `usable_arenas`가 `nfreepools`에 따라 오름차순으로 정렬되는 이유이다.
    - 최대한 앞에서부터(가용한 메모리가 적은 Arena부터) Object가 할당되므로, 뒤에 있는 Arena일수록 할당은 적어지게 된다.
    - 결국, 뒤에 있는 Arena일 수록 Arena가 가지고 있는 모든 Pool이 비워질 가능성이 높아지게 된다.
    - Arena 내에 있는 모든 Object가 삭제되면 OS에 해당 Arena가 점유하고 있던 memory를 반환한다.



# Python의 Garbage Collection

> https://www.honeybadger.io/blog/memory-management-in-python/#garbage-collection-in-python

- Garbage Collection(GC)
  - Garbage Collection은 더 이상 사용되지 않는 메모리를 반환하거나 회수하는 process이다.
    - 할당 되었으나 더 이상 사용되지 않는 메모리를 garbage라 부른다.
  - Python은 자동으로 GC를 수행한다.
    - C와 같은 언어에서는 더 이상 사용되지 않는 메모리(Object)를 수동으로 할당 해제해야한다.
  - Python은 아래 2가지 방식으로 자동으로 GC를 수행한다.
    - reference counting 기반의 GC
    - Generational GC



- Reference Count

  - CPython의 객체에는 `type`과 `ref_count`가 있다.
    - `type`은 객체의 type을 의미한다.
    - `ref_count`는 object가 참조된 횟수를 의미한다.

  ```python
  var = "memory"
  
  """
  위와 같이 변수를 선언하면 Cpython은 아래 구조와 같은 object를 생성한다.
  type: string
  value: memory
  ref_count: 1
  """
  ```

  - `sys` 모듈의 `getrefcount` 메서드로 object의 참조 횟수를 확인할 수 있다.
    - 1이 아닌 4가 나오는 이유는 아래 번외 참고

  ```python
  import sys
  
  
  var = 'memory'
  ref_count = sys.getrefcount(var)
  print(ref_count)	# 4
  ```

  - ref_count가 증가하는 경우들
  
    - 변수에 객체를 할당할 경우
    - 객체를 arguments로 넘길 경우
    - 객체를 list에 포함시킬 경우
  
  
  
  
  - ref_count 감소시키기
    - bar가 foo를 참조하게 하여 foo의 ref_count를 1 증가시킨 후, bar에 None을 할당하면, bar가 더 이상 foo를 참조하지 않게 되면서 foo의 ref_count가 다시 감소하게 된다.
    - 혹은 `del bar`를 통해 bar 객체를 삭제하여도 foo의 ref_count가 1 감소하게 된다.
  
  ```python
  import sys
  
  
  foo = 'memory'
  bar = foo
  
  ref_count = sys.getrefcount(foo)
  print(ref_count)	# 5
  
  bar = None
  ref_count = sys.getrefcount(foo)
  print(ref_count)    # 4
  ```
  
  - Reference count를 활용한 GC
    - Reference count를 활용한 GC의 원리는 단순하다.
    - 어떤 객체의 ref_count가 0이 되면, GC는 해당 객체를 memory에서 삭제한다.
    - Reference count를 활용한 GC는 real-time으로 진행되며, 비활성화 하는 것이 불가능하다.
  
  ```python
  # 아래와 같이 foo를 삭제하더라도, foo가 가리키는 객체를 참조하는 bar가 존재하므로, foo가 가리키던 객체는 memory에서 삭제되지 않는다.
  foo = "memory"
  bar = [foo]
  del foo
  print(bar[0])	# memory
  ```



- Generational Garbage Collection

  - Reference count 기반의 GC는 cyclic references에는 작동하지 않는다.
    - Cyclic references를 가지는 객체의 GC를 위해 Generational Garbage Collection가 필요하다.

  - Cyclic references(Circular reference)
    - Object가 스스로를 참조하거나 두 개의 서로 다른 object가 서로를 참조하는 상황을 의미한다.
    - List나 dictionary, 사용자 정의 object등의 container object에서만 가능한 상황이다.
    - integer, float, string 등의 immutable한 type에서는 불가능하다.

  ```python
  """
  예시1.
  아래와 같이 lst가 lst를 참조하는 상황에서 lst를 제거한다고 해도 lst가 가리키는 객체는 여전히 lst를 참조하고 있으므로, memory에서 삭제되지 않는다.
  """
  import sys
  
  lst = list()
  print(sys.getrefcount(lst))		# 2
  lst.append(lst)
  print(sys.getrefcount(lst))		# 3
  del lst
  
  
  """
  예시2
  foo 객체는 bar 객체를 참조하고, bar 객체 역시 foo 객체를 참조하는 상황에서 foo와 bar 객체를 삭제한다고 해도, 서로를 참조하고 있기에 memory에서 완전히 삭제되지 않는다.
  """
  class Foo:
      pass
  class Bar:
      pass
  foo = Foo()
  bar = Bar()
  foo.ref_bar = bar
  bar.ref_foo = foo
  del foo
  del bar
  ```

  - Generational Garbage Collection의 동작 방식
    - Cyclic references는 오직 container 객체에서만 가능한 상황이므로, 모든 container 객체를 scan하여 circular references 상태인 객체를 찾고, 삭제가 가능하다면 삭제한다.
    - Scan해야 할 객체의 개수를 줄이기 위해서 generational GC는 immutable type만을 담고 있는 tuple은 무시한다.
    - 또한 모든 container 객체를 scan하는 것은 시간이 오래 걸리는 작업이기 때문에 reference count GC와는 달리 real-time으로 동작하지는 않고, 일정 기간마다 실행된다.
    - reference count GC와는 달리 비활성화가 가능하다.
    - generational GC가 실행되면, 다른 모든 작업은 정지된다.
    - 또한 generational GC가 수행되는 횟수를 줄이기 위해서, CPython은 객체를 여러 generation으로 구분하여 각 generation별로 threshold를 설정한다.
    - 만일 특정 generation에 있는 객체들의 수가 threshold를 초과하면, generational GC가 실행된다.
  - Generation
    - CPython은 object를 세 개의 generation(0, 1, 2)으로 분류한다.
    - 새로운 객체가 생성되면, 첫 generation에 속하기 된다.
    - 만일 generational garbage collection가 실행된 후에도 남아있다면, 해당 객체는 두 번째 generation으로 넘어가게 된다.
    - 만일 generational garbage collection이 한 번 더 실행된 후에도 남아있다면, 해당 객체는 마지막 generation으로 넘어가게 된다.
    - 일반적으로 대부분의 객체는 첫 generational garbage collection 때 사라지게 된다.
    - Generational garbage collection은 항상 주어진 generation이하의 generation들을 대상으로 GC를 수행한다.
    - 예를 들어 두 번째 generation에 general GC가 수행되면, 첫 번째 generation에도 general GC가 수행된다.
  - `gc` module
    - Python에는 Generational garbage collection을 조작하기 위한 `gc` 모듈이 있다.
    - 각 generation 별 threshold 확인 및 변경, 각 generation에 저장된 객체의 개수 확인, generational garbage collection 비활성화 등이 가능하다.

  ```python
  import gc
  
  
  print(gc.get_threshold())
  print(gc.get_count())
  ```



- 번외. 위 예시에서 ref_count가 1이 아닌 4가 나오는 이유

  > https://stackoverflow.com/questions/45021901/why-does-a-newly-created-variable-in-python-have-a-ref-count-of-four

  - 위와 같이 script가 아닌 REPL console로 작성하면 다음과 같은 결과가 나온다.
    - var가 선언되면서 1번, `getrefcount`의 인자로 넘어가면서 1번

  ```bash
  >>> import sys
  >>> var = "memory"
  >>> print(sys.getrefcount(var))	# 2
  ```

  - 이와 같은 차이가 나는 이유
    - `gc` 모듈의 `get_referrers` 메서드를 사용하면 객체를 어디서 참조하고 있는지를 확인 가능하다(결과는 Python version에 따라 달라질 수 있다).
    - string type의 경우 byte code로 complie 과정에서 객체를 2번 더 참조하게 되어, ref_count가 2 증가하게 된다.
    - 그러나 REPL console의 경우 context를 분리하여 수행하므로, ref_count가 2 증가하지 않는다.

  ```python
  import sys
  import gc
  from pprint import pprint
  
  
  var = 'memory'
  ref_count = sys.getrefcount(var)
  print(ref_count)
  pprint(gc.get_referrers(var))
  
  """
  4
  [{'__annotations__': {},
    '__builtins__': <module 'builtins' (built-in)>,
    '__cached__': None,
    '__doc__': None,
    '__file__': 'test.py',
    '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f462bc90160>,
    '__name__': '__main__',
    '__package__': None,
    '__spec__': None,
    'gc': <module 'gc' (built-in)>,
    'pprint': <function pprint at 0x7f462bb990d0>,
    'ref_count': 4,
    'sys': <module 'sys' (built-in)>,
    'var': 'memory'},
   ['sys',
    'gc',
    'pprint',
    'pprint',
    'var',
    'memory',
    'ref_count',
    'sys',
    'getrefcount',
    'var',
    'print',
    'ref_count',
    'pprint',
    'gc',
    'get_referrers',
    'var']]
  """
  ```

  - 따라서 직접 compile후에 ref_count를 확인하면 결과가 달라지게 된다.

  ```python
  import sys
  
  exec(compile("var = 'memory'", "<string>", "exec"))
  print(sys.getrefcount(var))	# 2
  ```







# Python은 왜 느린가?

> http://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/

- Python은 동적 타이핑 언어다.

  - 동일한 결과를 얻기 위해서 더 많은 과정을 거쳐야 하기에 Python은 느릴 수 밖에 없다.
  - C와 같은 정적 타이핑 언어는 변수를 선언할 때 변수의 type을 함께 정의해주기에, 해당 변수의 type을 바로 알 수 있다.

  ```c
  int a = 1;
  int b = 2;
  int c = a + b;
  
  /*
  int 타입인 1을 a에 할당한다.
  int 타입인 2를 b에 할당한다.
  + 연산자를 통해 그 둘을 더한다.
  더한 값을 c에 할당한다.
  */
  ```

  - 반면에 Python의 경우 Python 프로그램이 실행될 때, interpreter는 코드에 정의된 변수의 type을 모르는 상태다.
    - Interpreter가 아는 것은 각 변수가 모두 Python Object라는 것이다.

  ```python
  a = 1
  b = 2
  c = a + b
  
  """
  1. 1을 a에 할당
    - a 변수의 PyObject_HEAD의 typecode를 int로 설정
    - a에 int type인 1을 할당
  2. 2를 b에 할당
    - b 변수의 PyObject_HEAD의 typecode를 int로 설정
    - b에 int type인 2를 할당
  3. 더하기
    - a의 PyObject_HEAD의 typecode 찾기
    - a는 interger이며, a의 val은 1이라는 것을 인지
    - b의 PyObject_HEAD의 typecode 찾기
    - b는 interger이며, b의 val은 2라는 것을 인지
    - a와 b를 더한다.
  4. 결과 값을 c에 할당
    - c 변수의 PyObject_HEAD의 typecode를 int로 설정
    - a에 int type인 1을 할당
  """
  ```



- Python은 컴파일 언어 보다는 인터프리터 언어에 가깝다.
  - 좋은 컴파일러는 반복되거나 불필요한 연산을 미리 찾아내어 속도를 높일 수 있다.
  - 그러나 인터프리터 언어에 가까운 Python은 위 방식이 불가능하다.



- Python의 object model은 비효율적인 메모리 접근을 유발할 수 있다.

  - 많은 언어들은 원시 자료형을 지원한다.
    - 원시 자료형은 어떤 데이터의 참조를 담고 있는 자료형이 아닌 값 그 자체를 담을 수 있는 자료형이다.
    - 그러나 python에는 원시 자료형 자체가 존재하지 않는다.
  - Python의 모든 것은 객체이다.
    - Python의 모든 변수들은 data 자체를 저장하고 있는 것이 아니라 data를 가리키는 pointer를 저장하고 있다.

  - 예시

    - 다른 언어들에서 일반적으로 원시 자료형이라 불리는 integer 등도 하나의 객체이다.

    - C에서 `int a = 1`의 a는 숫자 1 자체를 저장하고 있지만, Python에서  `a = 1`의 a는 숫자 1을 가리키는 pointer를 저장하고 있는 것이다.





# GIL

- GIL(Global Interpreter Lock)

  > https://xo.dev/python-gil/
  >
  > https://dgkim5360.tistory.com/entry/understanding-the-global-interpreter-lock-of-cpython

  - CPython에서 여러 thread를 사용할 경우, 단 하나의 thread만이 Python object에 접근할 수 있도록 제한하는 mutex이다.
    - mutex: mutal exclusion(상호 배제)의 줄임말로, 공유 불가능한 자원의 동시 사용을 피하는 기법이다.
    - Python은 thread-safe하지 않기에 GIL이라는 mutex로 lock을 걸어놓은 것이다.
    - 즉, Python에서는 둘 이상의 thread가 동시에 실행될 수 없다.
    - 둘 이상의 thread가 동시에 실행되는 것 처럼 보인다면 각 thread가 빠른 속도로 번갈아가며 실행되고 있는 것이다.
    - 즉, multi threading이 자체가 불가능한 것이 아니다. 여러 개의 thread가 생성되고 실행될 수는 있지만, 병렬적으로 실행될 수는 없어 결과적으로 싱글 스레드처럼 동작하는 것이다.
  - Python은 thread-safe하지 않다.
    - thtead-safeness란 thread들이 race condition을 발생시키지 않으면서 각자의 일을 수행한다는 뜻이다.
    - race condition이란 하나의 값에 여러 스레드가 동시에 접근하여 값이 올바르지 않게 읽히거나 쓰이는 문제를 의미한다.
    - 예를 들어 아래 코드의 결과 x는 0이 될 것 같지만 그렇지 않다(0이 나올 수도 있지만, 여러 번 수행해보면 0이 아닌 값들도 나온다).
    - 이는 x라는 값에 2개의 스레스가 동시에 접근하여 race condition가 발생했기 때문이다.
    - GIL이 걸려 있어도 아래와 같이 race condition이 발생하게 된다.
  
  ```python
  """
  3.10부터 재현이 불가능하다.
  """
  import threading 
  
  x = 0
  
  def foo(): 
      global x 
      for i in range(100000): 
          x += 1
  
  def bar(): 
      global x 
      for i in range(100000): 
          x -= 1
  
  t1 = threading.Thread(target=foo) 
  t2 = threading.Thread(target=bar) 
  t1.start() 
  t2.start() 
  t1.join() 
  t2.join()
  
  print(x)
  ```
  
  - Python의 GC 방식
    - Python에서 모든 것은 객체다.
    - 모든 객체는 해당 객체를 가리키는 참조가 몇 개 존재하는지를 나타내는 참조 횟수(reference count) 필드를 지니고 있다.
    - 참조 될 때마다 1씩 증가하며, 0이 될 경우 GC에 의해 메모리에서 삭제된다.
    - `sys` 모듈의 `getrefcount` 메서드로 확인 가능하다.
  
  ```python
  import sys
  
  
  foo = []
  bar = foo
  print(sys.getrefcount(foo))		# 3(foo가 선언될 때 1번, bar에 할당될 때 1번, getrefcount 함수에 매개변수로 넘어가면서 1번)
  ```
  
  - 왜 Python은 thread-safe하지 않은가?
    - 참조 횟수를 기반으로 GC가 이루어지는 Python의 특성상 여러 스레드가 하나의 객체를 참조할 경우 참조 횟수가 제대로 count되지 않을 수 있다.
    - 따라서 삭제되어선 안 되는 객체가 삭제될 수도 있고, 삭제되어야 할 객체가 삭제되지 않을 수도 있다.
    - 만일 GC가 정상적으로 이루어지게 하려면 모든 개별 객체에 mutex가 필요하게 된다.
    - 그러나 모든 객체에 mutex를 사용할 경우 성능상의 손해뿐 아니라, deadlock이 발생할 수도 있다.
    - 따라서 CPython은 개별 객체를 보호하는 것이 아니라 Python interpreter 자체를 잠궈 오직 한 thread만이 Python code를 실행시킬 수 있게 했다.
  - 예시
    - 만약 화장실에 변기가 1칸 밖에 없다고 생각해보자.
    - 변기는 공유가 불가능한 자원으로, 여러 명이 동시에 사용할 수는 없다.
    - 따라서 사람들은 화장실에 들어가 화장실 문(mutex)를 닫고, 자기가 사용할 동안 다른 사람이 사용하지 못하도록 잠궈놓는다(lock).
    - 다른 사람들(theads)는 문이 잠겨 있는 동안은 화장실을 이용하지 못한다.
  - GIL이 영향을 미치는 범위
    - CPU bound는 GIL의 영향을 받고, I/O bound는 GIL의 영향을 받지 않는다는 설명들이 있는데 이는 잘못된 것이다.
    - GIL의 영향을 받는지 여부는 Python runtime과 상호작용을 하는가에 달려있다. 즉 Python runtime과 상호작용을 하면 GIL의 영향을 받고, 반대일 경우 아니다.
    - Python runtime과 상호작용 한다는 것의 의미는 Python interpreter가 프로그램 실행 중 관리하는 시스템적 동작(memory 관리, refcnt 조정, 객체 생성/삭제 등)을 포함하는 작업을 의미한다.
    - CPU bound란 CPU 성능에 영향을 받는 작업으로, 일반적으로 연산을 수행하거나 image processing과 같이 수학적 계산을 많이 하는 작업들이 이에 속한다.
    - I/O bound란 대부분의 시간을 input/output을 기다리는데 사용하는 작업을 뜻하며, filesystem에 접근하거나 network 통신을 하는 작업들이 이에 속한다.
    - 보통 하나의 프로그램은 CPU bound와 I/O bound 작업들이 함께 섞여 있다.
    - 일반적으로 I/O bound의 작업들은 Python runtime과 상호작용을 하지 않으므로 GIL의 영향을 덜 받는다.
  - CPU bound 예시
    - multi thread를 사용했을 때 오히려 속도가 더 느려진다.
    - GIL로 인해 single thread로 동작할 뿐 아니라, lock을 걸고 해제하는 과정을 반복하면서 overhead가 발생하기 때문이다.
  
  ```python
  import time
  from threading import Thread
  
  
  N = 10000000
  
  def countdown(n):
      while n>0:
          n -= 1
  
  # single thread
  start = time.time()
  countdown(N)
  print(time.time()-start)	# 0.459784...
          
  
  # multi thread
  t1 = Thread(target=countdown, args=(N//2,))
  t2 = Thread(target=countdown, args=(N//2,))
  
  start = time.time()
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  print(time.time()-start)	# 0.852366...
  ```
  
    - I/O bound 예시
      - multi thread가 single thread에 비해 훨씬 빠르다.
  
  ```python
  import time
  from threading import Thread
  from elasticsearch import Elasticsearch
  
  
  es_client = Elasticsearch("127.0.0.1:9200")
  
  N = 1000
  
  def send_reqeusts(n):
      for _ in range(n):
          es_client.cat.indices()
  
  # single thread
  start = time.time()
  send_reqeusts(N)
  print(time.time()-start)	# 10.40409...
         
  
  # multi thread
  t1 = Thread(target=send_reqeusts, args=(N//2,))
  t2 = Thread(target=send_reqeusts, args=(N//2,))
  
  start = time.time()
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  print(time.time()-start)	# 5.85471...
  ```



  - Python에서 multi thread 자체가 불가능한 것은 아니다.
    - 여러 개의 thread를 실행시키는 것 자체는 가능하다.
    - 단지, 여러 개의 스레드가 병렬적으로 실행되는 것이 막혀있는 것이다.
    - 즉 동시성에는 열려있지만 병렬성에는 닫혀있다고 볼 수 있다.
    - 그러나 Python에서 multi thread는 성능상의 이점이 거의 존재하지 않기에(lock을 걸고(aquire) lock을 풀 때(release) overhead가 발생) multi process를 사용하거나 비동기 코드를 작성하는 것이 낫다.
    - 단, 위에서 봤듯 Python runtime과 상호작용하지 않는 작업들은 multi thread로 구현했을 때 성능상의 이득이 있을 수 있다.



- 의문들

    - 왜 다른 언어에는 GIL이 존재하지 않는가?
      - 다른 언어는 Python처럼 refcnt로 GC를 실행하지 않기 때문이다.

    - 왜 이렇게 설계 했으며, 왜 바꾸지 않는가?
      - Python이 공개됐던 1991년만 하더라도 하드웨어적인 한계로 인해 multi thread는 크게 고려할 사항이 아니었다.
      - 이전에 몇 번 GIL을 없애려는 시도가 있었으나 모두 실패로 돌아갔다.
      - 귀도 반 로섬은 GIL을 없앨 경우 기존에 개발된 라이브러리들과 제품들의 코드를 모두 수정해야 하므로 없애기 쉽지 않다고 밝혔고, 실제로 이전에 있었던 몇 번의 시도들도 위와 같은 이유 때문에 실패했다.
      - 그러나 없애고 싶지 않은 것은 아니며, 부작용을 최소화하면서 없앨 방법을 찾는 중이다.



  - race condition을 막는 방법

    - 방법1
      - 하나의 스레드가 작업을 종료하고 다른 스레드가 작업을 시작하도록 한다.

    ```python
    from threading import Thread
    
    x = 0
    N = 1000000
    mutex = Lock()
    
    def add():
    	global x
    	for i in range(N):
    		x += 1
    	
    def subtract():
    	global x
    	for i in range(N):
    		x -= 1
    	
    
    add_thread = Thread(target=add)
    subtract_thread = Thread(target=subtract)
    
    # 스레드가 시작하고
    add_thread.start()
    # 끝날때 까지 대기한다.
    add_thread.join()
    
    subtract_thread.start()
    subtract_thread.join()
    
    print(x)
    ```

      - 방법2. mutex를 설정한다.
        - 스레드에서 공유 객체에 접근하는 부분(임계영역)을 지정하고 lock을 설정한다.

    ```python
    from threading import Thread, Lock
    
    x = 0
    N = 1000000
    mutex = Lock()
    
    def add():
    	global x
        # lock을 걸고
    	mutex.acquire()
    	for i in range(N):
    		x += 1
        # 작업이 완료되면 lock을 푼다.
    	mutex.release()
    
    def subtract():
    	global x
    	mutex.acquire()
    	for i in range(N):
    		x -= 1
    	mutex.release()
    
    
    add_thread = Thread(target=add)
    subtract_thread = Thread(target=subtract)
    
    add_thread.start()
    subtract_thread.start()
    
    add_thread.join()
    subtract_thread.join()
    
    print(x)
    ```



- Python에서 thread들 간의 switching은 오직 bytecode를 실행하고 다음 bytecode를 실행되기 전의 기간에만 일어난다.

  - 따라서 원자성 문제가 생길 수 있다.
  - Switching이 얼마나 빈번하게 일어날지는 `sys.setswitchinterval()`의 설정에 따라 달라진다.



# Multi processing

- Python에서의 multi processing
  - Python은 GIL로 인해 thread 기반의 병렬 처리가 까다롭다.
  - 따라서 multi-thread 방식 보다는 multi-processing 방식으로 병렬 처리를 해야한다.
  - Python 내장 패키지 중 multiprocessing을 사용하면 간단하게 구현이 가능하다.



- Process 생성하기

  - Process를 생성하는 것을 spawning이라 한다.
  - `Process` class의 인스턴스를 생성하는 방식으로 process를 생성할 수 있다.
    - `Process`의 인스턴스를 생성할 때는 첫 번째 인자로 실행 시킬 함수를, 두 번째 인자로 해당 함수에 넘길 인자를 입력한다.
  - `start()`메서드를 사용하여 spawn된 process를 실행시킬 수 있다.

  ```python
  from multiprocessing import Process
  
  def f(name):
      print('hello', name)
  
  if __name__ == '__main__':
      p = Process(target=f, args=('bob',))
  ```



- multiprocessing은 platform(OS)에 따라 세 가지 다른 방식의 Process 실행 방식을 지원한다.

  - spawn
    - 자식 process는 부모 process로부터 `run()` 메서드를 실행시키는 데 필요한 자원만을 상속 받는다.
    - 불필요한 file descriptor와 handle은 상속받지 않는다.
    - fork나 forkserver에 비해 느리다.
    - Unix와 Windows에서 사용 가능하며, Windows와 macOS의 기본값이다.
  - fork
    - 부모 process는 `os.fork()`메서드를 사용하여 Python interpreter를 fork한다.
    - 자식 process는 부모 process로부터 모든 자원을 상속받는다.
    - 자식 process는 부모 process와 사실상 동일한 상태로 시작된다.
    - Unix에서만 사용 가능하며, Unix의 기본 값이다.
  - forkserver
    - 프로그램이 실행되고, forkserver start method를 선택하면, server process가 시작된다.
    - 이후 새로운 프로세스가 필요할 때마다 부모 프로세스는 server에 새로운 process를 fork하도록 요청한다.
    - 불필요한 자원은 상속되지 않는다.
    - Unix pipe를 통한 file descriptor를 지원하는 Unix에서만 사용 가능하다.
  - multiprocessing의 `set_start_method`를 통해 어떤 method로 실행시킬지 지정이 가능하다.

  ```python
  from multiprocessing import Process
  
  def f(name):
      print('hello', name)
  
  if __name__ == '__main__':
      multiprocessing.set_start_method('spawn')
      p = Process(target=f, args=('bob',))
  ```

  - 혹은 아래와 같이 `get_context()`메서드를 사용하는 방법도 있다.

  ```python
  from multiprocessing
  
  def f(name):
      print('hello', name)
  
  if __name__ == '__main__':
      ctx = multiprocessing.get_context('spawn')
      p = ctx.Process(target=f, args=('bob',))
  ```



- Process 사이의 communication channel 사용하기

  - `multiprocessing`은 두 가지 communication channel을 지원한다.
  - `Queue`
    - `queue.Queue`의 clone이다.
    - thread, process safe하다.

  ```python
  from multiprocessing import Process, Queue
  
  def f(q):
      q.put([42, None, 'hello'])
  
  if __name__ == '__main__':
      q = Queue()
      p = Process(target=f, args=(q,))
      p.start()
      print(q.get())    # prints "[42, None, 'hello']"
      p.join()
  ```

  - `Pipe`
    - `Pipe()` 함수는 `Pipe`로 연결된 한 쌍의 connection object를 반환한다.
    - 반환된 connection object들은 `send()`와 `recv()` 메서드를 가진다.

  ```python
  from multiprocessing import Process, Pipe
  
  def f(conn):
      conn.send([42, None, 'hello'])
      conn.close()
  
  if __name__ == '__main__':
      parent_conn, child_conn = Pipe()
      p = Process(target=f, args=(child_conn,))
      p.start()
      print(parent_conn.recv())   # prints "[42, None, 'hello']"
      p.join()
  ```



- Process 사이의 동기화

  - `multiprocessing`은 `threading`의 동기화 관련 요소들을 모두 포함하고 있다.
  - 예시
    - Lock을 사용하여 한 번에 하나의 proecess에서만 print를 출력하도록 하는 예시이다.

  ```python
  from multiprocessing import Process, Lock
  
  def f(l, i):
      l.acquire()
      try:
          print('hello world', i)
      finally:
          l.release()
  
  if __name__ == '__main__':
      lock = Lock()
  
      for num in range(10):
          Process(target=f, args=(lock, num)).start()
  ```



- Process간의 상태 공유

  - 동시성 프로그래밍을 할 때에는 왠만하면 상태의 공유를 피하는 것이 좋다.
    - 특히 multi process를 사용할 때는 더욱 그렇다.
  - 그럼에도 `multiprocessing`에서는 상태 공유를 위한 몇 가지 방법을 제공한다.
  - Shared memory
    - `Value`와 `Array`를 사용하여 data를 shared memory map에 저장할 수 있다.
    - `'d'`와 `'i'`는 typecode를 나타낸다. `d`는 double precision float type을 나타내고, `i`는 signed integer를 나타낸다. 

  ```python
  from multiprocessing import Process, Value, Array
  
  def f(n, a):
      n.value = 3.1415927
      for i in range(len(a)):
          a[i] = -a[i]
  
  if __name__ == '__main__':
      num = Value('d', 0.0)
      arr = Array('i', range(10))
  
      p = Process(target=f, args=(num, arr))
      p.start()
      p.join()
  
      print(num.value)
      print(arr[:])
  ```

  - Server process
    - `Manager()`가 반환한 manager 객체는 Python 객체를 가지고 있는 server process를 통제하고, 다른 process들이 proxy를 사용하여 이를 조정할 수 있도록 해주는 역할을 한다.
    - `Manager()`가 반환한 manager는 list, dict, Namespace, Lock, RLock, Semaphore, Boundedsemaphore, Condition, Event, Barrier, Queue, Value, Array type을 지원한다.

  ```python
  from multiprocessing import Process, Manager
  
  def f(d, l):
      d[1] = '1'
      d['2'] = 2
      d[0.25] = None
      l.reverse()
  
  if __name__ == '__main__':
      with Manager() as manager:
          d = manager.dict()
          l = manager.list(range(10))
  
          p = Process(target=f, args=(d, l))
          p.start()
          p.join()
  
          print(d)
          print(l)
  ```



- Pool 사용하기

  - `Pool` class는 worker process들의 pool을 생성한다.
  - `Pool` class는 task들을 process로 넘길 수 있는 몇 가지 method를 제공한다.
    - `apply()`: 하나의 process에게 특정 작업을 실행시키고 해당 작업의 종료까지 기다린다.
    - `apply_async()`: process에게 특정 작업을 시키고 종료는 기다리지 않고 `AsyncResult`를 반환 받는다.  작업이 완료되었을 때 `AsyncResult`의  `get()` 메서드를 통해 작업의 반환값을 얻을 수 있다.
  
  ```python
  from multiprocessing import Pool, TimeoutError
  import time
  import os
  
  def f(x):
      return x*x
  
  if __name__ == '__main__':
      # 4개의 worker process를 시작한다.
      with Pool(processes=4) as pool:
          # evaluate "f(20)" asynchronously
          res = pool.apply_async(f, (20,))      # 오직 하나의 process에서만 실행된다.
          print(res.get(timeout=1))             # prints "400"
  
          # evaluate "os.getpid()" asynchronously
          res = pool.apply_async(os.getpid, ()) # 오직 하나의 process에서만 실행된다.
          print(res.get(timeout=1))
  
          # 여러 개의 process에서 실행될 수도 있다.
          multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
          print([res.get(timeout=1) for res in multiple_results])
  
          # 하나의 worker를 10초 동안 휴식시킨다.
          res = pool.apply_async(time.sleep, (10,))
          try:
              print(res.get(timeout=1))
          except TimeoutError:
              print("We lacked patience and got a multiprocessing.TimeoutError")
  
          print("For the moment, the pool remains available for more work")
  
      # with block을 벗어나면 pool이 정지된다.
      print("Now the pool is closed and no longer available")
  ```
  
  - `Pool`과 `Process`의 차이
    - `Pool`은 처리할 일을 쌓아두고 process들이 알아서 분산 처리를 하게 만드는 방식이다.
    - `Process`는 각 process마다 할당량을 지정해주고 분산 처리를 하게 만드는 방식이다.



- `map`, `map_async`, `imap`, `imap_unordered`의 차이

  - `map(func, iterable[, chunksize, callback, error_callback])`
    - Iterable한 값을 chunk로 자른 뒤 각 chunk들을 pool 내의 worker process로 보내는 방식으로 동작한다.
    - `chunksize` option을 통해 몇 개의 item을 하나의 chunk로 묶을지를 설정할 수 있다(단 반드시 해당 크기로 묶이지는 않을 수도 있다).
    - Iterable을 모두 처리한 뒤 그 결과를 list로 반환한다.
    - 따라서 iterable의 크기가 커질 수록 memory에 부담이 가게 되므로, 이런 경우 `imap`을 사용하는 것이 권장된다.

  ```python
  from multiprocessing import Pool
  
  def f(x):
      return x*x
  
  with Pool(processes=4) as pool:
      print(pool.map(f, range(10)))	# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
  ```

  - `map_async(func, iterable[, chunksize])`
    - `map`과 유사하지만 작업의 종료를 기다리지 않고, `AsyncResult`를 반환한다는 점이 다르다.
    - 만약 `callback` 함수는 오직 하나의 argument만을 받는 callable한 객체여야하며, `error_callback`도 마찬가지다.

  ```python
  from multiprocessing import Pool
  
  def f(x):
      return x // x
  
  def callback(x):
      print(x)
  
  def error_callback(x):
      print(x)
  
  with Pool(processes=4) as pool:
      # 아래는 ZeroDivisionError가 발생하여 error_callback이 실행된다.
      res = pool.map_async(f, range(10), callback=callback, error_callback=error_callback)
      # 완료까지 기다린다.
      res.wait()
      # 아래는 문제 없이 실행되어 callback이 실행된다.
      res = pool.map_async(f, range(1, 10), callback=callback, error_callback=error_callback)
      res.wait()
  ```

  - `imap(func, iterable[, chunksize])`
    - `map`과 동작 방식은 유사하지만 `map`이 결과를 list로 한 번에 반환하는 것과 달리 `imap`은 iterator를 반환한다.
    - 기본 chunksize는 1이며, 1보다 적절히 큰 값을 줄 경우 처리 속도를 크게 높일 수 있다.

  ```python
  from multiprocessing import Pool
  
  def f(x):
      return x*x
  
  with Pool(processes=4) as pool:
      result = pool.imap(f, range(10))
      print(type(result))				# <class 'multiprocessing.pool.IMapIterator'>
      for result in result:
          print(result, end=" ")		# 0 1 4 9 16 25 36 49 64 81
  ```

  - `imap_unordered(func, iterable[, chunksize])`
    - 결과의 순서가 보장되지 않는다는 점만 빼면 `imap`과 동일하다.
    - Process가 하나만 있을 경우에는 순서가 보장된다.

  ```python
  from multiprocessing import Pool
  
  def f(x):
      return x*x
  
  with Pool(processes=4) as pool:
      result = pool.imap_unordered(f, range(10))
      print(type(result))				# <class 'multiprocessing.pool.IMapIterator'>
      for result in result:
          print(result, end=" ")		# 0 16 1 25 9 4 64 49 36 81
  ```



- Daemon process 생성하기

  - 특정 작업을 백그라운드에서 실행하기 위하여 daemon process를 실행할 수 있다.
    - `Process`의 인스턴스의 `daemon` 속성을 True로 주면 된다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo(num):
      time.sleep(10)
      print(os.getpid())
      print(num)
      print("-"*100)
  
  
  if __name__ == "__main__":
  
      p = Process(target=foo, args=[0])
      p.daemon = True
      p.start()
  ```

  - Daemon proecess는 main process가 종료되면 함께 종료된다.



- `join()` 메서드

  - `join()`메서드는 자식 process의 작업이 완료될 때 까지 부모 process가 기다리게 한다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      p.join()
      print("Parent process")
  ```

  - `join()`이 없을 경우

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      print("Parent process")
  ```

  - 자식 process는 join 없이 종료되고, 부모 process는 아직 실행중이라면 자식 process는 zombie process가 된다.
    - 아래 코드에서 자식 process가 join 없이 부모 프로세스보다 먼저 종료가 되는데, 이 상태에서 자식 프로세스의 pid로 process 상태를 확인해보면 `[python] <defunct>`와 같이 뜨게 된다.
    - 만일 부모 process가 종료되지 않고 계속 실행되는 코드였을 경우 자식 process는 zombie process인 상태로 계속 남아있게 되므로 반드시 join을 해줘야한다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      time.sleep(300)
      print("Parent process")
  ```

  - 명시적으로 `join()` 메서드를 호출하지 않아도, 부모 프로세스가 종료될 때가 되면 암묵적으로 `join()` 메서드가 호출된다.
    - 아래 코드를 보면 `join()`을 호출하지 않았음에도, 부모 process가 다 실행된 이후에도 종료되지 않고 자식 process의 실행이 완료되기를 기다린다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      time.sleep(20)
      print("Child process")
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.start()
      print("Parent process")
  ```

  - 단 `join()` 메서드의 암묵적인 호출은 non-daemonic process일 때 만이고 daemon process의 경우 부모 프로세스의 종료와 함께 종료된다.

  ```python
  import os
  import time
  from multiprocessing import Process
  
  
  def foo():
      print(os.getpid())
      print("Child process")
      time.sleep(20)
  
  
  if __name__ == "__main__":
      p = Process(target=foo)
      p.daemon = True
      p.start()
      print("Parent process")
  ```




- Event

  - 여러 Process들 사이에 event를 공유하기 위해 사용한다.
  - 예를 들어 한 프로세스가 특정 작업을 처리한 뒤에 다른 프로세스들이 실행되어야 하는 경우 등에 사용할 수 있다.
  - Methods
    - `wait()`: flag가 True가 될 때 까지 block한다.
    - `set()`: flag를 True로 설정한다.
    - `clear()`: flag를 False로 설정한다.
  - 예시

  ```python
  from multiprocessing import Process, Event
  import time
  
  
  def first(event):
      event.clear()
      print("first")
      time.sleep(5)
      event.set()
  
  def second(event):
      event.wait()
      print("second")
  
  
  if __name__ == "__main__":
      event = Event()
      processes = []
      for i in range(3):
          if i == 0:
              process = Process(target=first, args=(event,))
          else:
              process = Process(target=second, args=(event,))
          processes.append(process)
          process.start()
      
      for p in processes:
          p.join()
  ```
  
  - Python multiprocessing의 Event 사용시 주의점
  
    - Event의 flag는 기본적으로 False 상태로 시작한다.
    - 따라서 이를 원치 않을 경우 생성 이후 바로 True로 변경해줘야한다.
  
  
  ```python
  from multiprocessing import Event
  
  
  event = Event()
  print(event.is_set())
  event.set()
  ```
  
  
  
  
  
  



- Lock

  - Event와 함께 Python에서 multiprocessing 실행시 race condition을 방지하기 위한 모듈이다.
  - 여러 프로세스 중 오직 하나의 process만이 `acquire`를 통해 lock을 얻으며, `acquire`를 실행한 다른 process들은 lock을 획득한 process가 `release`를 실행할 때 까지 멈추게 block된다.
  - Methods
    - `acquire()`: lock을 획득한다. 이미 다른 process가 lock을 획득한 상태라면 lock을 획득한 process가 `release()`를 실행할 때 까지 block된다.
    - `release()`: 획득한 lock을 반환한다.
  - 예시

  ```python
  from multiprocessing import Process, Lock
  import time
  
  
  def first(lock):
      lock.acquire()
      print("first")
      time.sleep(5)
      lock.release()
  
  def second(lock):
      lock.acquire()
      print("second")
      time.sleep(5)
      lock.release()
      
  
  if __name__ == "__main__":
      lock = Lock()
      processes = []
      for i in range(3):
          if i == 0:
              process = Process(target=first, args=(lock,))
          else:
              process = Process(target=second, args=(lock,))
          processes.append(process)
          process.start()
      
      for p in processes:
          p.join()
  ```

  





