class OperationResult:
    def __init__(self, result):
        self.result = result

    def __str__(self):
        return self.result


class VoidResult(OperationResult):
    def __init__(self):
        super().__init__("<EMPTY>")


class TrueResult(OperationResult):
    def __init__(self):
        super().__init__("<TRUE>")
