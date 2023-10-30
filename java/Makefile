.PHONY: test javasrc

test: javasrc
	(python3 ../getexamples.py | sed 's/^$$/;/'; echo 'Last') | gradle run

javasrc: src/main/java/pocql/PocqlParser.java

src/main/java/pocql/PocqlParser.java: Pocql.g4
	antlr4 Pocql.g4 -o src/main/java/pocql/ -package pocql

Pocql.g4: ../pocql.lark
	cat ../pocql.lark | python3 lark2g4.py Pocql > Pocql.g4
