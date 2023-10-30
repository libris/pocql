package pocql;

import java.util.*;

public class PocqlPatternBuilder extends PocqlBaseListener {
    Map root;

    @Override public void exitStart(PocqlParser.StartContext ctx) {
        System.out.println(ctx);
    }
}
