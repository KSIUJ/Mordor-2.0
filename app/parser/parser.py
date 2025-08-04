from .tokenizer import tokenize
from .astNodes import OrNode, AndNode, NotNode, TagNode

class Parser:
    """Recursive tag parser"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def getCurrent(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    

    def consume(self, expected=None):
        if expected and expected != self.getCurrent():
            raise SyntaxError(f"Expected token '{expected!r}', got '{self.getCurrent()!r}' instead, at position {self.pos}")
        self.pos += 1
    

    def parseOrExpr(self):
        """orExpression = andExpression { '||'  andExpression}"""
        left = self.parseAndExpr()
        while self.getCurrent() == "||":
            self.consume("||")
            left = OrNode(left, self.parseAndExpr())
        return left
    

    def parseAndExpr(self):
        """andExpression = notExpression { '&&' notExpression}"""
        left = self.parseNotExpr()
        while self.getCurrent() == "&&":
            self.consume("&&")
            left = AndNode(left, self.parseNotExpr())
        return left


    def parseNotExpr(self):
        """notExpression = '!' notExpression | base"""
        if self.getCurrent() == "!":
            self.consume("!")
            return NotNode(self.parseNotExpr())
        return self.parseBase()


    def parseBase(self):
        """base = tag | '(' expression ')'"""
        if self.getCurrent() == "(":
            self.consume("(")
            node = self.parseOrExpr()
            self.consume(")")
            return node
        
        tag = self.getCurrent()
        if not tag:
            raise SyntaxError("Tag expected")
        if tag in ("||", "&&", ")"):
            raise SyntaxError("Unexpected base token")
        self.consume()

        return TagNode(tag)


def parseExpression(expression: str) -> OrNode | AndNode | NotNode | TagNode:
    """
        Main function that parses a string expression into an abstract syntax tree (AST)
    """
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Empty expression")
    
    parser = Parser(tokens)
    ast = parser.parseOrExpr()
    if parser.pos != len(parser.tokens):
        raise ValueError(f"Unexpected tokens at the end of the expression: {parser.tokens[parser.pos:]!r}")
    
    return ast