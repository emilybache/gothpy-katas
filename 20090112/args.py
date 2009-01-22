

class Args:
    def __init__(self, schema):
        self.schema = schema
        self.valid = False
        self.options = {}
        for k in self.schema.keys():
            self.options[k] = False

    def parse(self, args):
        given_options = self._get_options(args)
        for opt in given_options:
            if not opt.flag in self.options.keys():
                raise BadArgsException(opt.flag, self.schema, args)
            try:
                self.options[opt.flag] = self.schema[opt.flag](opt.value)
            except ValueError, details:
                raise BadArgsException(opt.flag, self.schema, args, str(details))
        self.valid = True
        
    def _get_options(self, args):
        raw_options = []
        all_args = " ".join(args)
        for raw_option in all_args.split("-"):
            if not raw_option:
                continue
            raw_options.append(option_from_raw(raw_option))
        return raw_options
                
    def is_valid(self):
        return self.valid
    
    def __getitem__(self, key):
        return self.options[key]
    
def option_from_raw(raw_option):
    fields = raw_option.split()
    option = Option(fields[0])
    if len(fields) == 2:
        option.value = fields[1]
    elif len(fields) > 2:
        option.value = fields[1:]
    return option
        
def int_list(str_list):
    return map(int, str_list)
        
class Option:
    def __init__(self, flag, value=True):
        self.flag = flag
        self.value = value
    
class BadArgsException(Exception):
    def __init__(self, option, schema, args, underlying_problem=""):
        message = "problem with option %s. Schema is %s args is %s." % (option, schema, args)
        if underlying_problem:
            message += " Underlying problem %s " % underlying_problem
        Exception.__init__(self, message)
        