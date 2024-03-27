#         self.catalog_ref = ProtocolOperationsCatalog()
#         self.catalog_ref.register_protocol_operation(self)
#
#
# class ProtocolOperationsCatalog:
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(ProtocolOperationsCatalog, cls).__new__(cls)
#         return cls._instance
#
#     def __init__(self):
#         self.catalog: List[ProtocolOperation] = list()
#
#     def register_protocol_operation(self, operation: ProtocolOperation):
#         self.catalog.append(operation)
#
#     def build_catalog(self):
#         for operation in self.catalog:
#             operation()
