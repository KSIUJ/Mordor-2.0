# Tag query parser documentation

## 1. Summary

- The main goal of this parser is to support **advanced tag filtering** feature.

- It transforms input expressions (e.g. !(dog || cat) && cute) into an **abstract syntax tree (AST)**, which can later be translated into SQL WHERE clauses.


## 2. Grammar (EBNF)
```EBNF
    expression ::= orExpression
    orExpression ::= andExpression { '||'  andExpression}
    andExpression ::= notExpression { '&&' notExpression}
    notExpression ::= '!' notExpression | base
    base ::= tag | '(' expression ')'
    tag ::= [a-zA-Z0-9_-.] { [a-zA-Z0-9_-.] }
```

## 3. AST Node types

- `OrNode(left, right)` - logical OR
- `AndNode(left, right)` - logical AND
- `NotNode(expr)` - logical NOT
- `TagNode(tag)` - single tag

## 4. Usage example

```python
expression = "!(dog || cat) && cute"
ast = parseExpression(expression)
print(ast)
```
**Result:**
```text
And(
   Not(
      Or(
         Tag(dog),
         Tag(cat)
      )
   ),
   Tag(cute)
)
```

## 5. Tag restrictions

Tags must follow these rules:

# TBD


## 6. Notes

- **Functional completeness:** The combination of logical operators (`!`, `&&`, `||`) and parentheses makes it functionally complete.
- **Tests:** Contains basic tests for tokenization and parsing.