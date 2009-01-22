
class Args:
    def __init__(self, **schema):
        self.schema = schema
        for key, converter in schema.items():
            if converter is bool:
                setattr(self, key, False)

    def split_options(self, argv):
        argsiter = iter(argv)
        current_option = None
        current_values = []
        while True:
            arg = next(argsiter, None)
            if arg is None or arg.startswith("-"):
                if current_option:
                    yield current_option, current_values
                    if arg is None:
                        raise StopIteration()
                    else:
                        current_option = arg[1]
                        current_values = []
            else:
                current_values.append(arg)
                
    def parse(self, argv):
        argsiter = iter(argv)
        while True:
            arg = next(argsiter, None)
            if arg is None:
                break
            option = arg[1]
            converter = self.schema[option]

            if converter is bool:
                value = True
            elif isinstance(converter, list):
                value = []
                for i in range(5):
                    value.append(next(argsiter, None))
            else:
                value = converter(next(argsiter, None))
            setattr(self, option, value)
        return True
                
        