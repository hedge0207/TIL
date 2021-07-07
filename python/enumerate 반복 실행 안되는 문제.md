- 아래 코드에서 위에 있는 반복문은 실행이 되지만 아래 있는 반복문은 실행되지 않는다.

```python
a = ['3.', '1.', 'a.', 'd.', 'b.', '2.']
b = enumerate(a)

# 실행 된다.
for i in b:
    print(i)

print("-"*100)

# 실행 안된다.
for i in b:
    print(i)
```

