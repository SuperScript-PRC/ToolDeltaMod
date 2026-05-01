# TYPE_CHECKING
if 0:
    import typing

    T = typing.TypeVar("T")
    PT = typing.ParamSpec("PT")
# TYPE_CHECKING END


def MethodCacher(cacher_getter):
    # type: (typing.Callable[[], typing.Callable[PT, T]]) -> typing.Callable[PT, T]
    """
    运行时生成方法。传入的方法产生函数只有在被调用时才产生。
    通常用在客户端和服务端混用区, 但是实际上不万不得已最好不要混用服务端和客户端逻辑。
    """
    g = [None]  # type: list[typing.Callable[PT, T] | None]

    def runner(*args, **kwargs):
        if g[0] is None:
            g[0] = cacher_getter()
        return g[0](*args, **kwargs)

    return runner


def AttrCacher(cacher_getter):
    # type: (typing.Callable[[], T]) -> typing.Callable[[], T]
    """
    运行时生成属性。传入的属性只有在被调用时才获取。
    通常用在客户端和服务端混用区, 但是实际上不万不得已最好不要混用服务端和客户端逻辑。
    """
    g = [None]  # type: list[T | None]

    def runner():
        if g[0] is None:
            g[0] = cacher_getter()
        return g[0]

    return runner
