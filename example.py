import type_check
import typing

@type_check.type_check(should_raise=False)
def num_add(a: int, b, c: typing.Any=0):
    # Types parsed {'a': <class 'int'>, 'b': typing.Any, 'c': typing.Any}
    return a + b

print(num_add(5, 5))
print(num_add(1, 2, ":)"))
print(num_add("5", "5", c=1))

"""
Output: 
10
3
example.py:11: TypeWarn: Expected <class 'int'> for arg 'a' but got <class 'str'>
  print(num_add("5", "5", c=1))
55
"""

@type_check.type_check()
def test(a: list[int]): # type[type2] currently not supported
    return "WOOOOO"

@type_check.type_check()
def test2(a: list):
    return "WOOOOOOOOOOOOO"

@type_check.type_check()
def test3(a: int | float):
    return "WOW"

print(test([1]))
print(test2([1]))
print(test2((1,2)))
print(test3(1))
print(test3(1.0))
print(test3("1"))