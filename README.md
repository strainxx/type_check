# type_check
Simple python runtime type checking

# Usage
```python
@type_check.type_check(should_raise: bool = False, debug: bool = False)
def example(arg: int):
    ...
```

If should_raise is True type checker will emit error instead of warning 

# Example
See [example.py](example.py)