class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        cls_instances = cls._instances.get(cls) or []
        matching_instances = list(
            filter(
                lambda x: x["args"] == args and x["kwargs"] == kwargs,
                cls_instances,
            )
        )
        if len(matching_instances) == 1:
            return matching_instances[0]["instance"]
        else:
            instance = super().__call__(*args, **kwargs)
            cls_instances.append({"instance": instance, "args": args, "kwargs": kwargs})
            cls._instances[cls] = cls_instances
            return instance
