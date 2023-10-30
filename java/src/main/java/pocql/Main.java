package pocql;

import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class Main {
    public static void main(String[] args) throws Exception {
        var input = CharStreams.fromStream(System.in);
        var lexer = new PocqlLexer(input);
        var tokens = new CommonTokenStream(lexer);
        var parser = new PocqlParser(tokens);

        var builder = new PocqlPatternBuilder();
        parser.addParseListener(builder);

        var tree = parser.start();

        System.out.println(tree.toStringTree(parser));
        System.out.println(builder.root);
    }
}
