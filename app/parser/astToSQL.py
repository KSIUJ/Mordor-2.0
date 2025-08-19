from .astNodes import AndNode, OrNode, NotNode, TagNode
from .parser import parseExpression

class AST_to_SQL():
    """Recursive AST parser"""

    def __init__(self):
        self.params = {}
        self.counter = 0
        
    
    def _AST_to_SQL(self, node):
        if isinstance(node, OrNode):
            l = self._AST_to_SQL(node.left)
            r = self._AST_to_SQL(node.right)
            return f"({l} OR {r})"

        elif isinstance(node, AndNode):
            l = self._AST_to_SQL(node.left)
            r = self._AST_to_SQL(node.right)
            return f"({l} AND {r})"
        
        elif isinstance(node, NotNode):
            expr = self._AST_to_SQL(node.expr)
            return f"NOT ({expr})"
        
        elif isinstance(node, TagNode):
            self.counter += 1
            self.params[f"p{self.counter}"] = node.tag
            return(
                "(EXISTS ("
                "SELECT 1 FROM tag_file tf "
                "JOIN tags t ON tf.tag_id = t.id "
                f"WHERE tf.file_id = files.id AND t.name = :p{self.counter}"
                "))"
            )
        
        raise ValueError("Unknown AST node type")


    def run(self, ast: str) -> str:
        self.params = {}
        self.counter = 0
        sql_where = self._AST_to_SQL(ast)
        sql = f"SELECT * FROM files WHERE {sql_where}"
        
        return sql


def parseAST(ast: str) -> tuple[str, dict]:
    """
        Utility function that parses an AST into sql query
    """
    parser = AST_to_SQL()
    sql = parser.run(ast)
    
    return sql, parser.params