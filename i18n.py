import json


class I18n:
    def __init__(self):
        with open("i18n.json", 'r+') as f:
            self.f = json.load(f)

    def read(self, Code):
        return self.f[Code]

    def log_(self, Code):
        return f"\033[92m{self.read(Code)}\033[00m"

    def warn_(self, Code):
        return f"\033[93m{self.read(Code)}\033[0m"

    @staticmethod
    def inf_(txt):
        return "\x1B[3m" + f"\033[96m {txt} \033[00m" + "\x1B[0m"

    @staticmethod
    def bl_(_):
        return f"\033[5m{_}\033[0m"

    def var_(self, Code=None):
        V = self.read("V")
        if Code:
            return V[Code]
        else:
            return V.keys()

    def raise_(self, ErrorClass, ErrorCode: str, *args):
        raise ErrorClass(f"{ErrorCode}: {self.read(ErrorCode)}" % args)
