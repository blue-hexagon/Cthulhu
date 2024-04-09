class NonUniqueProfileIdError(Exception):
    def __init__(self, message, additional_info=None):
        super().__init__(message)
        self.additional_info = additional_info


class MultipleHostSelectorError(Exception):
    def __init__(self, message, additional_info=None):
        super().__init__(message)
        self.additional_info = additional_info
class MoreOrLessThanASingleOptionSelectedError(Exception):
    def __init__(self, message, additional_info=None):
        super().__init__(message)
        self.additional_info = additional_info
