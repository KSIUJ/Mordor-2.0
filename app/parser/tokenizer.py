def tokenize(expression: str) -> list:
    """
    Splits the expression into tokens
    """
    result = []
    
    i = 0
    while i < len(expression):
        if expression[i].isspace():
            i += 1
        elif expression[i] in "()!":
            result.append(expression[i])
            i += 1
        elif expression[i] in "|&" and i + 1 < len(expression) and expression[i] == expression[i+1]:
            result.append(expression[i] * 2)
            i += 2
        elif expression[i] == '"' or expression[i] ==  "'":
            s = expression[i]
            i += 1
            begin = i
            while i < len(expression) and expression[i] != s:
                i += 1
            if i >= len(expression):
                raise SyntaxError("Missing ending quotation")
            result.append(expression[begin:i])
            i += 1
        else:
            begin = i
            while i < len(expression) and not expression[i].isspace() and expression[i] not in "()!|&":
                i += 1
            result.append(expression[begin:i])
    return result