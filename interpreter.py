class Expr(object):
    def __init__(self):
        pass

class BinExpr(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class IntExpr(Expr):
    def __init__(self, value):
        self.value = value

class Assign(Expr):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Ident(Expr):
    def __init__(self, name):
        self.name = name

class Sequence(Expr):
    def __init__(self, body):
        self.statements = body

class If(Expr):
    def __init__(self, cond, then, else_):
        self.cond = cond
        self.then = then
        self.else_ = else_

class While(Expr):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class AST(object):
    def __init__(self):
        pass

class Function(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Program(AST):
    def __init__(self, functions, body):
        self.functions = functions
        self.body = body

class Call(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

def tAdd(a,b):
    return BinExpr('+', a, b)

def tSub(a,b):
    return BinExpr('-', a, b)

def tMul(a,b):
    return BinExpr('*', a, b)

def tDiv(a,b):
    return BinExpr('/', a, b)

def tInt(value):
    return IntExpr(value)

def tLt(a,b):
    return BinExpr('<', a, b)

def tGt(a,b):
    return BinExpr('>', a, b)

def tLte(a,b):
    return BinExpr('<=', a, b)

def tGte(a,b):
    return BinExpr('>=', a, b)

def tEq(a,b):
    return BinExpr('==', a, b)

def tNeq(a,b):
    return BinExpr('!=', a, b)

def tBitAnd(a,b):
    return BinExpr('&', a, b)

def tBitOr(a,b):
    return BinExpr('|', a, b)

def tBitXor(a,b):
    return BinExpr('^', a, b)

def tLAnd(a,b):
    return BinExpr('&&', a, b)

def tLOr(a,b):
    return BinExpr('||', a, b)

def tAs(name, expr):
    return Assign(name, expr)

def tId(name):
    return Ident(name)

def eval_math(expr, env):
    op = expr.op
    if op == '+':
        return evaluate(expr.left, env) + evaluate(expr.right, env)
    elif op == '-':
        return evaluate(expr.left, env) - evaluate(expr.right, env)
    elif op == '*':
        return evaluate(expr.left, env) * evaluate(expr.right, env)
    elif op == '/':
        return evaluate(expr.left, env) // evaluate(expr.right, env)
    else:
        raise Exception('Unknown operator: ' + op)

def eval_compare(expr, env):
    op = expr.op
    if op == '<':
        return evaluate(expr.left, env) < evaluate(expr.right, env)
    elif op == '>':
        return evaluate(expr.left, env) > evaluate(expr.right, env)
    elif op == '<=':
        return evaluate(expr.left, env) <= evaluate(expr.right, env)
    elif op == '>=':
        return evaluate(expr.left, env) >= evaluate(expr.right, env)
    elif op == '==':
        return evaluate(expr.left, env) == evaluate(expr.right, env)
    elif op == '!=':
        return evaluate(expr.left, env) != evaluate(expr.right, env)
    else:
        raise Exception('Unknown operator: ' + op)
    
def eval_bit_operation(expr, env):
    op = expr.op
    if op == '&':
        return evaluate(expr.left, env) & evaluate(expr.right, env)
    elif op == '|':
        return evaluate(expr.left, env) | evaluate(expr.right, env)
    elif op == '^':
        return evaluate(expr.left, env) ^ evaluate(expr.right, env)
    
def eval_logic_operation(expr, env):
    op = expr.op
    if op == '&&':
        return evaluate(expr.left, env) and evaluate(expr.right, env)
    elif op == '||':
        return evaluate(expr.left, env) or evaluate(expr.right, env)

def eval_program(program):
    env = {}
    for func in program.functions:
        env[func.name] = func
    for stmt in program.body:
        result = evaluate(stmt, env)
    return result

def evaluate(expr, env={}):
    if type(expr) == BinExpr:
        if expr.op in ['+', '-', '*', '/']:
            return eval_math(expr, env)
        elif expr.op in ['<', '>', '<=', '>=', '==', '!=']:
            return eval_compare(expr, env)
        elif expr.op in ['&', '|', '^']:
            return eval_bit_operation(expr, env)
        elif expr.op in ['&&', '||']:
            return eval_logic_operation(expr, env)
        else:
            raise Exception('Unknown operator: ' + expr.op)
    elif type(expr) == Sequence:
        for stmt in expr.statements:
            result = evaluate(stmt, env)
        return result
    elif type(expr) == Assign:
        env[expr.name] = evaluate(expr.expr, env)
    elif type(expr) == Ident:
        return env[expr.name]
    elif type(expr) == IntExpr:
        if type(expr.value) == int:
            return expr.value
        else:
            raise Exception('Expected int, got ' + type(expr.value))
    elif type(expr) == If:
        cond = evaluate(expr.cond, env)
        if cond:
            return evaluate(expr.then, env)
        else:
            return evaluate(expr.else_, env)
    elif type(expr) == While:
        cond = evaluate(expr.cond, env)
        while cond:
            result = evaluate(expr.body, env)
            cond = evaluate(expr.cond, env)
        return None
    elif type(expr) == Call:
        func = env[expr.name]
        args = [evaluate(arg, env) for arg in expr.args]
        new_env = env
        for i in range(len(func.params)):
            new_env[func.params[i]] = args[i]
        return evaluate(func.body, new_env)
    else:
        raise Exception('Unknown expression type: ' + type(expr))