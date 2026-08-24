# ISO/SAE 21434:2021 Knowledge Layer

This directory contains public-safe metadata, templates and operating rules for ISO/SAE 21434:2021 Automotive Cybersecurity Engineering. The complete licensed standard text is not stored in the public repository.

## Runtime source policy

At runtime, the Cybersecurity Agent must load the approved local source supplied by the organization. It must verify the edition, source hash, page or line anchor and quotation hash before using a requirement, recommendation, permission or work product record. Each normative conclusion must include the complete approved paragraph or complete table row, the Clause or RQ／RC／PM／WP identifier, the reason it applies, the interpretation and human verification state.

If the local source is absent, stale, inaccessible or structurally ambiguous, the Agent must emit `citation_missing` or `source_structure_uncertain`. If a conclusion depends on another ISO 26262 or ISO/SAE 21434 source that is not loaded, it must emit `dependency_missing`; it must not claim compliance from memory or from a secondary summary.

## Coverage

The source provided for this Blueprint is ISO/SAE 21434:2021(E), 88 pages. The Agent model covers Clauses 1–15 and Annex A–H. Clauses 5–15 define objectives, provisions and work products. Clause 9 and Clause 15 support item definition, TARA, cybersecurity goals, cybersecurity concept, impact rating, attack feasibility, risk value and risk treatment. Clause 10 covers product development; Clauses 11–14 cover validation, production, operations／maintenance and end of cybersecurity support／decommissioning.

## SSD Controller evidence domains

The knowledge layer is designed to route evidence for NAND and host interfaces, PCIe／NVMe or equivalent interfaces, firmware／FTL, secure boot, key management, debug and service access, DMA and memory paths, digital RTL, analog／mixed-signal boundaries, simulation／emulation, tape-out／silicon changes, manufacturing provisioning, security updates, vulnerability monitoring, incident response and end-of-support.

## Cross-standard boundary

ASPICE 4.0, ISO 26262-5 and ISO/SAE 21434 may share factual Evidence Objects when the scope, baseline and ownership match. A shared Evidence Object does not automatically prove a requirement in another standard. Each standard claim requires its own direct citation and interpretation, and cross-standard relationships must be classified as shared, complementary, insufficient, conflict or dependency_missing.
