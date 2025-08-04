import pytest
from app.parser.tokenizer import tokenize
from app.parser.parser import parseExpression
from app.parser.astNodes import OrNode, AndNode, NotNode, TagNode

"""
    run from main directory with "PYTHONPATH=. pytest Test/test_parser.py"
    or all tests with "PYTHONPATH=. pytest"
"""

def ast_to_list(ast):
    """helper function converting ast to list for easier testing"""
    if isinstance(ast, OrNode):
        return ["or", ast_to_list(ast.left), ast_to_list(ast.right)]
    elif isinstance(ast, AndNode):
        return ["and", ast_to_list(ast.left), ast_to_list(ast.right)]
    elif isinstance(ast, NotNode):
        return ["not", ast_to_list(ast.expr)]
    elif isinstance(ast, TagNode):
        return ["tag", ast.tag]
    else:
        raise ValueError(f"Unexpected node type: {type(ast)}")


#       tokenizer test

@pytest.mark.parametrize("tokenizer_inp,tokenizer_exp",[
    # Basic
    ("a", ["a"]),
    ("!a", ["!", "a"]),
    ("!(dog || cat) && cute", ["!", "(", "dog", "||", "cat", ")", "&&", "cute"]),
    
    # Special char
    ("tag-with-hyphens || a", ["tag-with-hyphens", "||", "a"]),
    ("tag_with_underscores  || a", ["tag_with_underscores", "||", "a"]),
    ("tag.with.dots || a", ["tag.with.dots", "||", "a"]),
    ("tag123 || a", ["tag123", "||", "a"]),
    ("tag_-.,@#$+=%~^:*/?   || ' tag  _-.,@#$+=%~^:*/? || && () ! ' && $+=%", ["tag_-.,@#$+=%~^:*/?", "||", " tag  _-.,@#$+=%~^:*/? || && () ! ", "&&", "$+=%"]),
    
    # Operators
    ("a && b || c", ["a", "&&", "b", "||", "c"]),
    
    # Nested
    ("((a))", ["(", "(", "a", ")", ")"]),
    ("(a && (b || c))", ["(", "a", "&&", "(", "b", "||", "c", ")", ")"]),
    
    # Complex
    ("(a || b) && !(c || d)", ["(", "a", "||", "b", ")", "&&", "!", "(", "c", "||", "d", ")"]),
    ("((a && !b) || (c && d)) && !(e || f)", ["(", "(", "a", "&&", "!", "b", ")", "||", "(", "c", "&&", "d", ")", ")", "&&", "!", "(", "e", "||", "f", ")"]),
    
    # Whitespace
    ("    a    &&b||    c      ", ["a", "&&", "b", "||", "c"]),
    
    # Edge cases
    ("", []),
    ("   ", []),
    ("!()", ["!", "(", ")"]),
])
def test_tokenize(tokenizer_inp, tokenizer_exp):
    assert tokenize(tokenizer_inp) == tokenizer_exp


#       main parseExpression test

@pytest.mark.parametrize("parse_inp,parse_exp",[
    # Basic
    ("a", ["tag", "a"]),
    ("!a", ["not", ["tag", "a"]]),
    ("!(dog || cat) && cute", ["and", ["not", ["or", ["tag", "dog"], ["tag", "cat"]]], ["tag", "cute"]]),
    
    # Special char
    ("tag-with-hyphens", ["tag", "tag-with-hyphens"]),
    ("tag_with_underscores", ["tag", "tag_with_underscores"]),
    ("tag.with.dots", ["tag", "tag.with.dots"]),
    ("tag123", ["tag", "tag123"]),
    
    # Operators
    ("a && b || c", ["or", ["and", ["tag", "a"], ["tag", "b"]], ["tag", "c"]]),
    
    # Nested
    ("((a))", ["tag", "a"]),
    ("(a && (b || c))", ["and", ["tag", "a"], ["or", ["tag", "b"], ["tag", "c"]]]),
    
    # Complex
    ("(a || b) && !(c || d)", ["and", ["or", ["tag", "a"], ["tag", "b"]], ["not", ["or", ["tag", "c"], ["tag", "d"]]]]),
    ("((a && !b) || (c && d)) && !(e || f)", ["and", ["or", ["and", ["tag", "a"], ["not", ["tag", "b"]]], ["and", ["tag", "c"], ["tag", "d"]]], ["not", ["or", ["tag", "e"], ["tag", "f"]]]]),
    
    # Whitespace
    ("    a    &&b||    c      ", ["or", ["and", ["tag", "a"], ["tag", "b"]], ["tag", "c"]])
])
def test_parseExpression_valid(parse_inp, parse_exp):
    assert ast_to_list(parseExpression(parse_inp)) == parse_exp


@pytest.mark.parametrize("parseExpr_synErr", ["", "a && b c d e"])
def test_parseExpression_SyntaxErr(parseExpr_synErr):
    with pytest.raises(SyntaxError):
        parseExpression(parseExpr_synErr)


@pytest.mark.parametrize("parseExpr_synErr2", ["(a ^ b)", "a && (b   c)"])
def test_parseExpression_SyntaxErr2(parseExpr_synErr2):
    with pytest.raises(SyntaxError):
        parseExpression(parseExpr_synErr2)