# POCQL - A Query Language Using Predicates and Objects in Context

## Introduction

POCQL, the "Predicates and Objects in Context Query Language", is designed to be a lax syntax for making simple queries upon RDF data. It is based on a pragmatic mix of [CQL](https://www.loc.gov/standards/sru/cql/spec.html) and [SPARQL](https://www.w3.org/TR/sparql11-query/).

Queries are defined as:

- an *implicit* subject,
- for which a *set of selectors* are matched,
- against resource descriptions in a dataset.

It supports a form of pseudo-Turtle (the terse RDF syntax), but following the CQL design, being natural language-like, allowing for terse, sometimes vague but disambiguatable expressions. This disambiguation is performed by backing queries with underlying vocabulary data and JSON-LD contexts.

Results are graphs describing each matched subject resource. Exactly what the preconfigured set of data is used is application-dependent (e.g. using [CBDs](https://www.w3.org/submissions/CBD/) or embellished cards). It is recommended that result construction dynamically extend the set of descriptive paths with the set of matched selectors.

Queries are representable as RDF (e.g. in Turtle or JSON-LD).

## Examples

Combinations:

    Electronic AND genreForm lcsh:Physics AND genreForm lcsh:Cosmology AND author "Some Body"

Same combinations in terse (Turtle-like) form:

    a Electronic; genreForm (lcsh:Physics, lcsh:Cosmology); author "Some Body"

Grouping:

    a Electronic AND (genreForm lcsh:Physics OR genreForm lcsh:Cosmology) AND author "Some Body"

Terse grouping:

    a Electronic; genreForm (lcsh:Physics | lcsh:Cosmology); author "Some Body"

Compact form 1:

    author:(a b c)

Compact form 2:

    FÖRF:("Ekelöf, Gunnar" trl); ÄMNE:(översättare); ÄMNE:(biografi)

More complex:

    type (Electronic AND NOT Print)
        AND genreForm (lcsh:Physics OR lcsh:Cosmology)
        AND (author "Some Body" OR creator "Some \"Any\" Body")
        AND ((produced AND NOT published 2023) OR published NOT 2023)
        AND isbn NOT 0-000-111-000-0
        AND hasItem/heldBy lib:S

Complex containing predicate paths:

    type (Instance AND Electronic AND NOT Print)
        AND instanceOf?/genreForm (lcsh:Physics OR lcsh:Cosmology)
        AND (author|creator "Some Body" OR responsibilityStatement "Some \"Any\" Body")
        AND ((produced AND NOT published 2023) OR published NOT 2023)
        AND isbn NOT 0-000-111-000-0
        AND ^itemOf/heldBy lib:S

Complex example in terse (Turtle/SPARQL-like) form:

    a (Instance, Electronic, !Print);
        instanceOf?/genreForm (lcsh:Physics | lcsh:Cosmology);
        (author|creator "Some Body" UNION responsibilityStatement "Some \"Any\" Body");
        ((produced; !published 2023) UNION published !2023);
        isbn !0-000-111-000-0;
        ^itemOf/heldBy lib:S

## Structure

An outline of the structure is:

1. A nested structure of groups joined with AND, OR, or NOT.
2. Group items consist of pairs of either nested query groups, query patterns or predicate-object-items.
3. Query patterns consist of paths and object items.
4. Object items are either simple RDF terms or POCQL optionals, negations unions or sets.

## Design

There are many reasons for the POCQL design.

1. It is designed to query RDF terms, *not* any particular syntax.
2. It leaves room for *completing* the terms by leveraging detailed semantics "under the hood".
3. This language needs to support simple query engines, such as those based on Lucene (commonly ElasticSearch).
4. For this reason, the language is *not* designed as a general triple pattern language, but as a series of predicate object pairs, grouped using boolean operators.
5. It needs to support *some* power, mainly for convenience, but also to access the features of the underlying indexer (while avoiding too much feature lock-in). This includes property paths (including alternates and *manifested inverses*), object alternates, existence and negation, and "simple" string "likneness" (engine dependent).
6. The queries must also be possible to translate to SPARQL.
7. For this reason, it needs to be possible to *lift* to an *unambiguous* representation of RDF triples.

The final point means that the resulting parse tree must be possible to represent as an RDF structure. This is for representing query results as unambiguous RDF, where the choices, predicates and objects are expressed as RDF terms. That enables clients to employ a uniform means for presenting queries, search results and included data.

## Contextual Term Disambiguation (Punning)

This specifically means that a term used in the query might be a *label* for a term, or it might be an alias term for a property chain axiom employed by the vocabularies used in the queried data. In particular, if a term used is backed by an ObjectProperty but is paired with a string, an engine supporting POCQL Queries must expand this to a property path ending with a generic, descriptive label property (e.g. rdfs:label). It is up to the indexing mechanism to infer or manifest such properties in the backing search index.

## Comparison to other languages

### CQL

POCQL is a partial superset of CQL.

### SPARQL

The last query in the example section above *should* be equivalent to this SPARQL:

    ?s a :Instance, :Electronic ;
        :instanceOf?/:genreForm ?genreForm ;
        :isbn ?isbn;
        ^:itemOf/:heldBy lib:S .
    FILTER NOT EXISTS { ?s a :Print }
    FILTER(?genreForm IN (lcsh:Physics, lcsh:Cosmology))
    FILTER(?isbn != '0-000-111-000-0')
    FILTER EXISTS {
        { ?s :author|:creator "Some Body" } UNION { ?s :responsibilityStatement "Some \"Any\" Body" }
        {
            ?s :produced []
            FILTER NOT EXISTS { ?s :published "2023" }
        } UNION {
            ?s :published ?published . FILTER(?published != "2023")
        }
    }

### SHACL

The materialised POCQL pattern is reminiscent of SHACL Shapes. This wasn't initially by design but paves the path for a convergent mental model. Validation and querying are closely related.

## Development

POCQL is defined in a grammar file, which is used to generate parser code. Steps below include installing required parser generator tooling.

### Python

Requires Python 3.

Install:

    $ pip3 install lark

Test:

    $ python3 test.py

Run:

    $ python3 pocqlparser.py 'Book; aut tolkien; published >= 1980; sortBy published'

### Java

Requires Java 11+ and Gradle +7.

Install ANTLR4:

    $ pip3 install antlr4-tools

Generate Java source and run test:

    $ cd java
    $ make
