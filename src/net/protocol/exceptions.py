class ProtocolException(Exception):
    def __init__(self, message, additional_info=None):
        super().__init__(message)
        self.additional_info = additional_info
