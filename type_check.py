import ast, inspect, typing, warnings
from pydoc import locate

class TypeWarn(Warning):
    pass

def _is_valid(type_: object, obj: object):
    if type_ == typing.Any: return True
    if type(type_) == list: # list of types
        for t in type_:
            if isinstance(obj, t): return True
        return False
    return isinstance(obj, type_)

# Hard to read
def type_check(should_raise: bool = False, debug: bool = False):
    """Type checking decorator"""
    def decorator(func):
        # Here we parse expected types
        try:
            function_source = inspect.getsource(func)
        except OSError:
            # Can't retrieve source
            return func
        tree = ast.parse(function_source)
        if debug: print("[type_check] Ast dump:",ast.dump(tree, indent=4))
        func_def: ast.FunctionDef = tree.body[0]
        arg_type = {}
        pos_arg = {}
        i = 0
        for arg in func_def.args.args:
            pos_arg[i] = arg.arg
            if arg.annotation != None:
                if _is_valid(ast.Subscript,arg.annotation):
                    print("[type_check] Subscript annotation is not supported. Found:", ast.unparse(arg.annotation))
                    arg_type[arg.arg] = typing.Any
                elif _is_valid(ast.BinOp, arg.annotation):
                    arg_type[arg.arg] = [locate(node.id) for node in ast.walk(arg.annotation) if isinstance(node, ast.Name)]
                else: arg_type[arg.arg] = locate(ast.unparse(arg.annotation))
            else:
                arg_type[arg.arg] = typing.Any
            i+=1
        if debug: print("[type_check] Types parsed", arg_type)
        def wrapper(*args, **kwargs):
            # Here we do type checking
            arg_dict = {}
            for i in range(len(args)):
                arg_dict[pos_arg[i]] = args[i]
            arg_dict.update(kwargs)
            for key, value in arg_dict.items():
                if not _is_valid(arg_type[key], value):
                    if should_raise: raise TypeError(f"Expected {arg_type[key]} for arg '{key}' but got {type(value)}")
                    else: warnings.warn(f"Expected {arg_type[key]} for arg '{key}' but got {type(value)}", TypeWarn, 2)
            return func(*args, **kwargs)
        return wrapper
    return decorator