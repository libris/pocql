from pathlib import Path
from lark import Lark, Transformer, Token

with (Path(__file__).parent / 'pocql.lark').open() as f:
    pocql_grammar = f.read()


class PocqlAST(Transformer):
    def compound_expr(self, v):
        return v[0]
    def group(self, v):
        return {"poc:group": v[0]}
    def and_expr(self, v):
        parts = _reduce("poc:and", v)
        return parts[0] if len(parts) == 1 else {"poc:and": parts}
    def or_expr(self, v):
        parts = _reduce("poc:or", v)
        return parts[0] if len(parts) == 1 else {"poc:or": parts}
    def expr(self, v):
        return v[0]
    def fact(self, v):
        assert len(v) < 3
        return {"poc:path": self._path(v[0]), "poc:object": v[1]}
        return o
    def some_fact(self, v):
        return {"poc:object": v[0]}
    def not_fact(self, v):
        return {"poc:not": self.some_fact(v) if len(v) == 1 else self.fact(v)}
    def predicate(self, v):
        return v[0]
    def compound_object(self, v):
        return v[0]
    def unary_object(self, v):
        return v[0]
    def operator_object(self, v):
        op, o = v
        return {'poc:op': op, 'poc:object': o}
    def operator(self, v):
        return v[0]
    def object_group(self, v):
        return v[0]
    def object_and_group(self, v):
        #return {"poc:and": v}
        return _reduce("poc:and", v)
    def object_or_group(self, v):
        return {"poc:or": v}
    def negated_object(self, v):
        return {"poc:not": v}
    def STRING(self, v):
        return {"@value": str(v[1:-1].replace("\\\"", "\""))}

    def _value(self, v):
        return v

    GTE = _value
    LTE = _value
    NEQ = _value
    GT = _value
    LT = _value
    EQ = _value
    # TODO: turn STRING into string and optimize plus handle UNICODE
    #def ESC(self, v):
    #    print(v)
    #    return v
    #def UNICODE(self, v):
    #    print(v)
    #    return v
    #def HEX(self, v):
    #    print(v)
    #    return v
    #def SAFECODEPOINT(self, v):
    #    print(v)
    #    return v
    def TERM(self, v):
        return str(v)

    def _path(self, p):
        # TODO:
        # - figure out actual predicate path from "soft key" (e.g. partial label)
        # - parse SPARQL path microsyntax?
        return p


def _reduce(key, l):
    r = []
    for v in l:
        if isinstance(v, dict) and key in v:
            r += _reduce(key, v[key])
        else:
            r.append(v)
    return r


def parse(q):
    parser = Lark(pocql_grammar, parser='lalr', transformer=PocqlAST())
    return parser.parse(q)


if __name__ == '__main__':
    import json
    import sys

    args = sys.argv[1:]
    qs = [sys.stdin.read()] if not args else args
    for q in qs:
        ast = parse(q)
        print(json.dumps(ast, indent=2))
