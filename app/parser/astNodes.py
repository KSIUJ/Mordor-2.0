Indentation_size = "   "

class OrNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def indentPrint(self, indent=0):
        ind = Indentation_size * indent
        return (f"{ind}Or(\n"
                f"{self.left.indentPrint(indent+1)},\n"
                f"{self.right.indentPrint(indent+1)}\n"
                f"{ind})")

    def __repr__(self):
        return self.indentPrint()


class AndNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def indentPrint(self, indent=0):
        ind = Indentation_size * indent
        return (f"{ind}And(\n"
                f"{self.left.indentPrint(indent+1)},\n"
                f"{self.right.indentPrint(indent+1)}\n"
                f"{ind})")

    def __repr__(self):
        return self.indentPrint()
    

class NotNode:
    def __init__(self, expr):
        self.expr = expr
    
    def indentPrint(self, indent=0):
        ind = Indentation_size * indent
        return (f"{ind}Not(\n"
                f"{self.expr.indentPrint(indent+1)}\n"
                f"{ind})")

    def __repr__(self):
        return self.indentPrint()


class TagNode:
    def  __init__(self, tag):
        self.tag = tag

    def indentPrint(self, indent=0):
        ind = Indentation_size * indent
        return f"{ind}Tag({self.tag})"

    def __repr__(self):
        return self.indentPrint()