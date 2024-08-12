class UserException(Exception):
    """这是一个可以给用户看到异常信息的异常，或者是程序发现的用户操作失误产生的异常"""

    def __init__(self, message="这是一个自定义的异常"):
        # 调用基类的构造函数
        super().__init__(message)
        # 你可以在这里添加更多的初始化代码
        self.message = message

    def __str__(self):
        # 返回自定义的异常信息
        return f'【操作错误】{self.message}'