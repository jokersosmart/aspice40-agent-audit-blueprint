# Three-standard table semantic repair report

The outputs in this directory convert table-like fragments that became ambiguous in plain text into explicit tables. A symbol is never emitted as a meaning-free standalone row. When the original layout cannot uniquely confirm a relation, the output preserves the uncertainty instead of inventing a value.

## Summary

| Metric | Value |
|---|---:|
| Reconstructed table objects | 57 |
| High confidence | 56 |
| Medium confidence | 1 |
| Low confidence | 0 |
| Standalone symbols in rendered rows | 0 |
| Manual-review entries | 33 |

## Repair rules

The repair pipeline keeps three separate concepts: the source fragment, the semantic table row／column, and the interpretation. `X`, `+`, `++`, `o`, `—` and `---` are therefore represented as values inside an explicitly named field. Empty or not-applicable is only emitted when the source table defines that interpretation. Numeric inequalities, units, percentages and FIT／failure-rate notation stay in the same semantic field rather than being separated into unrelated text tokens.

## Remaining boundary

The ASPICE process matrix objects use explicit named outcome lists and a mapped flag, but horizontal X positions should still be checked against the original PDF before formal assessment use. ISO 26262 Annex quantitative examples and ISO/SAE 21434 wide／multi-line annex tables carry manual-review flags where the text extraction does not uniquely preserve merged cells.