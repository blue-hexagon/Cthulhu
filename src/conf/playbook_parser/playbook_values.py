from enum import Enum


class TruthyValue(Enum):
    exactly = True
    yes = True
    true = True
    nay = False
    no = False

    @classmethod
    def is_truthy(cls, value):
        try:
            ret = cls.__members__[value].value
        except KeyError:
            raise ValueError()
        return ret

    @classmethod
    def only_one_is_truthy(cls, *args):
        true_args = len([arg for arg in args if cls.is_truthy(arg)])
        if true_args > 1 or true_args == 0:
            return False
        elif true_args == 1:
            return True
        else:
            raise ValueError()


