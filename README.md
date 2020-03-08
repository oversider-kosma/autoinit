[![Build Status](https://api.travis-ci.org/oversider-kosma/autoinit.svg?branch=master)](https://travis-ci.org/oversider-kosma/autoinit)

# autoinit
> Python decorator for automatic initialization instance attributes

### What / How
```python3
from autoinit import autoinit

@autoinit
class X:
    def __init__(self, a, b, c, d:int, e=99.99, f='some_default_value'):
	    print("__init__ do some another things")

x = X(42, 100, 500, None)
#  Output: "__init__ do some another things"

print(x.__dict__)
# Output: {'a': 42, 'b': 100, 'c': 500, 'd': None, 'e': 99.99, 'f': 'some_default_value'}
```
### Install
$ ```pip install git+https://github.com/oversider-kosma/autoinit.git```

(pypi package coming soon)

### Why
A lot of elementary assignments inside `__init__` are a fairly frequent and rather dull case.

```python3
class FiveDimensionRecord:
    def __init__(self, x:int, y:int, z:int, u:int, 
                 v:int, dt:typing.Optional[datetime]=None, description:str=''):
        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.v = v
        self.dt = dt or datetime.now()
        self.description = description
```

Dataclasses do not make it much more fun, mainly because you still cannot declare attributes in one line
```python3
@dataclass
class FiveDimensionRecord:
    x: int
    y: int
    z: int
    u: int
    v: int
    dt: 'typing.Any' = None
    description: str = ''

    def __post_init__(self):
        self.dt = self.dt or datetime.now()
```

With `autoinit` it looks much more compact and minimalistic

```python3
@autoinit
class FiveDimensionRecord:
    def __init__(self, x:int , y:int , z:int , 
                 u:int, v:int, dt=None, description:str=''):
        self.dt = self.dt or datetime.now()
```

### TODO
* tests
* pypi package
