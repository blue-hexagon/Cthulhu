# class Help:
#     @staticmethod
#     def print():
#         """ Prints the classname followed by the docstring for all ProtocolOperations in this file """
#         class_list = list({element_name: element for element_name, element in globals().items() if isclass(element)})
#         class_list.remove("Help")
#         class_list.remove("Enum")
#         for name in class_list:
#             try:
#                 print(name + eval(name).__doc__)
#             except TypeError:
#                 print(name)
#
#
# if __name__ == '__main__':
#     Help.print()
