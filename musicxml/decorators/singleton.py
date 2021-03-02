_register = {}

def singleton(cls):
   def wrapper(*args, **kw):
       if cls not in _register:
           instance = cls(*args, **kw)
           _register[cls] = instance
       return _register[cls] 

   wrapper.__name__ = cls.__name__
   return wrapper