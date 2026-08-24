# ASPICE 4.0 Direct Spec Citation Catalog

Each entry below contains the complete verbatim paragraph or complete definition excerpt used by an Agent. Whitespace is normalized only; the source line range and hash are retained.

## SPEC-HWE2-PURPOSE-001

- **Kind:** purpose
- **Location:** 4.7.2 / HWE.2 /  / page 72
- **Source lines:** 4684–4687
- **Verbatim SHA-256:** `05c958d4fc0d179ef9bbdb5e37ce2a7cf8f5a9ef85fba63d0ad187e28d45823d`

> Process purpose The purpose is to provide an analyzed design, including dynamic aspects, that is consistent with the hardware requirements and suitable for manufacturing, and to derive production-relevant data.

**Why it applies:** Use when checking whether the hardware design work is expected to produce an analyzed, manufacturable design and production-relevant data.

**Interpretation:** The purpose covers analyzed design, dynamic aspects, consistency with hardware requirements, manufacturing suitability and derivation of production-relevant data.

**Not implied:** This does not prescribe a specific EDA tool, document filename or silicon milestone.

## SPEC-HWE2-BP5-001

- **Kind:** base_practice
- **Location:** 4.7.2 / HWE.2 / BP5 / page 73
- **Source lines:** 4735–4738
- **Verbatim SHA-256:** `e9cbbf56a2ab2bff378a22db8f386ec2a3bcf1af5d0aff5879b12746434dd847`

> HWE.2.BP5: Ensure consistency and establish bidirectional traceability. Ensure consistency and establish traceability between hardware elements and hardware requirements. Ensure consistency and establish traceability between the hardware detailed design and components of the hardware architecture.

**Why it applies:** Use when checking requirements-to-hardware and architecture-to-detailed-design consistency and bidirectional traceability.

**Interpretation:** The Agent must inspect both consistency and bidirectional traceability between hardware elements and hardware requirements, and between detailed design and architecture components.

**Not implied:** A link existing in a tool is not by itself proof that the linked information is consistent.

## SPEC-HWE2-NOTE9-001

- **Kind:** assessment_guidance
- **Location:** 4.7.2 / HWE.2 / BP5 / page 73
- **Source lines:** 4742–4744
- **Verbatim SHA-256:** `52c1e82f7e23baf9774f055944ee283a046292e164f43ea9d8bb96ba692d5afa`

> Note 9: Bidirectional traceability further supports consistency, and facilitates impact analysis of change requests, and demonstration of verification coverage. Traceability alone, e.g, the existence of links, does not necessarily mean that the information is consistent with each other.

**Why it applies:** Use when evaluating whether a traceability report demonstrates consistency rather than only link existence.

**Interpretation:** The traceability check must test consistency and support change-impact and verification-coverage reasoning; mere link presence is insufficient.

**Not implied:** The passage does not require a particular traceability database or visualization tool.

## SPEC-HWE2-BP6-001

- **Kind:** base_practice
- **Location:** 4.7.2 / HWE.2 / BP6 / page 73
- **Source lines:** 4746–4748
- **Verbatim SHA-256:** `e342ac9f1c02afeb1d3259f9cebea0b15b0d9aa63cc0b838337092f134698d4a`

> HWE.2.BP6: Communicate agreed hardware architecture and hardware detailed design. Communicate the agreed hardware architecture and the hardware detailed design, including the special characteristics and relevant production data, to all affected parties.

**Why it applies:** Use when checking communication and agreement of architecture, detailed design, special characteristics and relevant production data.

**Interpretation:** Affected parties must receive the agreed hardware architecture and detailed design together with special characteristics and relevant production data.

**Not implied:** The source matrix on the next page displays a BP7 label for this communication row; that conflict must remain open for human review.

## SPEC-VAL1-PURPOSE-001

- **Kind:** purpose
- **Location:** 4.5.1 / VAL.1 /  / page 58
- **Source lines:** 3851–3853
- **Verbatim SHA-256:** `af1b8c4b8f75a9bea04d0ba088ebb04a2d373ebc2abb9d3adc8a7e2d5ba246fa`

> Process purpose The purpose is to provide evidence that the end product, allowing direct end user interaction, satisfies the intended use expectations in its operational target environment.

**Why it applies:** Use when checking whether product validation demonstrates intended use in the operational target environment.

**Interpretation:** Validation is concerned with the end product, direct end-user interaction, intended-use expectations and the operational target environment.

**Not implied:** System verification or laboratory testing alone is not automatically equivalent to validation in the target environment.

## SPEC-VAL1-BP4-001

- **Kind:** base_practice
- **Location:** 4.5.1 / VAL.1 / BP4 / page 60
- **Source lines:** 3914–3917
- **Verbatim SHA-256:** `1769f5cf87ec39aa7bcf1f233a91802f473e5e79c10b5d08fa3b97f863e5b359`

> VAL.1.BP4: Ensure consistency and establish bidirectional traceability. Ensure consistency and establish bidirectional traceability from validation measures to the stakeholder requirements from which they are derived. Establish bidirectional traceability between validation results and validation measures.

**Why it applies:** Use when checking bidirectional traceability between validation measures, stakeholder requirements and validation results.

**Interpretation:** The Agent must look for consistency and bidirectional traceability in both measure-to-requirement and result-to-measure relationships.

**Not implied:** A validation result without its measure and stakeholder-requirement relationship is incomplete evidence.

## SPEC-SUP1-BP1-001

- **Kind:** base_practice
- **Location:** 4.8.1 / SUP.1 / BP1 / page 79
- **Source lines:** 5163–5167
- **Verbatim SHA-256:** `70c80966c75b676f621952d83f0a1b7c7a0fe30249868aeed7362cddc881da90`

> SUP.1.BP1: Ensure independence of quality assurance. Ensure that quality assurance is performed independently and objectively without conflicts of interest. Note 1: Possible inputs for evaluating the independence may be assignment to financial and/or organizational structure as well as responsibility for processes that are subject to quality assurance (no self-monitoring).

**Why it applies:** Use when checking QA independence and the absence of self-monitoring conflicts.

**Interpretation:** Quality assurance is expected to be independent and objective; financial or organizational assignment and responsibility for the subject process can affect independence.

**Not implied:** The passage does not mean every QA activity must be performed by a separate company or external supplier.

## SPEC-ANNEXB-VERIFICATION-MEASURE-001

- **Kind:** information_item
- **Location:** Annex B /  / 08-60 / page 129
- **Source lines:** 8562–8568
- **Verbatim SHA-256:** `705566177028505511e38907633a8d01c3904c2aaa9ef646233dd29488d06846`

> A validation measure can be a test case, a measurement, a simulation, an emulation, or an end user survey The specification of a validation measure includes - pass/fail criteria for validation measures (completion and end criteria) - a definition of entry and exit criteria for the validation measures, and abort and re-start criteria

**Why it applies:** Use when determining acceptable forms and characteristics of verification measures for hardware, firmware or system evidence.

**Interpretation:** A verification/validation measure can include test, measurement, simulation or emulation; the specification should include criteria and entry/exit conditions.

**Not implied:** This does not imply that every project must use every listed technique.
