class MyClass(object):
    # 在类的命名空间，不需要"."来访问
    class_var = 1
    # 类命名空间中的变量是可变变量
    data = []

    def __init__(self, i_var, other_data):
        self.i_var = i_var
        self.other_data = other_data


# 不在类的命名空间，需要"."来访问
item = MyClass.class_var

print(item)
