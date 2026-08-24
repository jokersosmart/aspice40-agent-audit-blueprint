# Three-standard semantic tables

This directory contains the table-semantic repair outputs for ASPICE 4.0, ISO 26262-5:2018, and ISO/SAE 21434:2021. It is intended to supplement, not silently overwrite, the original standard extracts.

The rendered Markdown and HTML outputs replace meaningless standalone symbols with explicit row and column semantics. For example, an ASPICE `X` becomes `Mapped = true` with a named Outcome list; an ISO 26262 `+`, `++`, or `o` remains in an explicit ASIL column; and an ISO/SAE 21434 `---`, `—`, `I1/I2/I3`, or `T1/T2` remains in a named CAL, independence, or testing column.

The JSON files are the machine-oriented long-table representation. Each table object carries its clause, source anchor, confidence, notes, and manual-review status. The manual-review queue is authoritative for unresolved merged-cell or horizontal-position questions. Nothing in that queue may be auto-filled by model inference.

The source PDF and full licensed standard text are not redistributed in this directory. Runtime citation services should use the locally controlled source and inject only validated, complete quotations into an LLM context.
