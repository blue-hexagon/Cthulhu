class OperationProxyFactory:
    def __new__(cls, subclass_name, args, **kwargs):
        subclass = globals()[subclass_name]
        instance = super().__new__(subclass)
        if args and kwargs:
            instance.__init__(*args, **kwargs)  # noqa
        elif args:
            instance.__init__(*args)  # noqa
        elif kwargs:
            instance.__init__(**kwargs)  # noqa
        return instance
