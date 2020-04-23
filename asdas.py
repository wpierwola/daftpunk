def wraps(to_be_decorated):
    def save_attributes():
        to_be_decorated.__doc__ = getattr(to_be_decorated, '__doc__')
    return save_attributes


def bumelant(*args, **kwargs):
    def wrap(to_be_decorated):
        @wraps(to_be_decorated)
        def wrapper(*args, **kwargs):
            return to_be_decorated(*args, **kwargs)
        return wrapper
    return wrap


@bumelant()
def say_cos():
  "cos"
  return "dasd"