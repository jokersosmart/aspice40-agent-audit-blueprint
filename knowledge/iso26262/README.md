# ISO 26262 Knowledge Boundary

This directory contains the public, non-confidential integration metadata for ISO 26262-5:2018. The licensed ISO source PDF and full verbatim standard text must be placed in an access-controlled runtime source directory and must not be committed to this public repository.

## Runtime source

Configure the approved local source in `config/standards_registry.yaml` and `config/iso26262_part5_scope.yaml`. At runtime, FS12 loads the approved ISO 26262-5 PDF or organization-approved text extraction, preserves the source hash, extracts the complete paragraph or complete table row, calculates `verbatim_text_sha256`, and injects the result into `spec_citations`.

## Citation requirement

Every ISO 26262 normative finding must include the complete direct quotation, the clause or requirement location, source page or line anchor, quotation hash, applicability explanation, interpretation and human verification status. A public Rule Pack or profile may contain an anchor and an extraction instruction, but it must not contain a substitute quotation or a guessed paraphrase.

If the licensed source is unavailable, the Agent must return `citation_missing`. If a conclusion depends on ISO 26262-2, -4, -8, -9, -11 or another missing Part, the Agent must return `dependency_missing`. Neither condition may be converted into `satisfied`, `partial` or `gap` by model inference.

## Part 5 coverage

The integration metadata covers Clauses 1–10 in the provided Part 5, Annex A–H, and the production／operation／service／decommissioning content found in Clause 7.4.5. The provided document does not contain an independent Clause 11; Agents must not invent one.

## Public repository handling

This repository is public. Do not commit the ISO PDF, complete extracted standard text, or a full verbatim citation catalog. Keep those files in an access-controlled runtime location. The Agent output can contain the authorized direct quotation for the internal assessment record when the organization has the right to use it. Consult the applicable license and organizational policy before distributing any assessment report externally.
