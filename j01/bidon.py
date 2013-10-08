
def var2listsort(*args):
        li = []
        for item in args:
                li.append(item)
        li.sort()
        return li

class Bidon:
    zaz = """je suis un pro du python"""
    def __init__(self, name, number = 42, **kwargs):
        self.txt = name
        self.num = number
        for item in kwargs.keys():
            setattr(self, item, kwargs[item])
