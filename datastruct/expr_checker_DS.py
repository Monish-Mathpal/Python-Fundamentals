'''Using to solve the problem of checking whether the open or close brackets are balanced or not '''
import Stack_DS as sd

def par(expr):
    balanced = True
    s = sd.Stack()
    index = 0

    while index < len(expr) and balanced:
        sym = expr[index]

        if sym == "(":
            s.push(sym)
        else:
            if s.is_empty():
                balanced == False
            else:
                s.pop()
        index += 1

    if balanced and s.is_empty():
        return True
    else:
        return False

print(par("(())"))   