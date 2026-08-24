# ASPICE 4.0 semantic tables

This output converts table-like ASPICE content into explicit row and column semantics. The process matrices use named Outcome lists instead of standalone X characters.

## Symbol and empty-cell semantics

| Symbol／form | Table context | Explicit meaning |
|---|---|---|
| X | Outcome／BP／Output Information Item mapping | mapped = true for the named row and named Outcome column; the X itself is not left as a standalone cell |
| N/P/L/F | Table 16–17 rating scale | Not, Partially, Largely, Fully achieved |
| P−／P+／L−／L+ | Table 18–19 refined rating | refined sub-level of Partially or Largely achieved |
| — | table separator or empty／not-applicable cell | render as an explicit empty_or_not_applicable value only when the table defines it; never infer a numeric value |

## Reconstructed tables

### Table 14 — Process capability levels

**Clause:** 3.2.1  
**Source anchor:** aspice40_layout.txt lines 815–847  
**Confidence:** `high`

| Level | Name | Semantic description |
|---|---|---|
| 0 | Incomplete process | The process is not implemented or fails to achieve its process purpose. |
| 1 | Performed process | The implemented process achieves its process purpose. |
| 2 | Managed process | The performed process is implemented in a managed fashion and work products are established, controlled and maintained. |
| 3 | Established process | The managed process uses a defined process capable of achieving its process outcomes. |
| 4 | Predictable process | The established process operates predictively within defined limits; quantitative management identifies and addresses variation. |
| 5 | Innovating process | The predictable process is continually improved to respond to organizational change. |

### Table 15 — Process attributes

**Clause:** 3.2.1  
**Source anchor:** aspice40_layout.txt lines 849–867  
**Confidence:** `high`

| Level | Attribute ID | Process attribute |
|---|---|---|
| 1 | PA 1.1 | Process performance |
| 2 | PA 2.1 | Performance management |
| 2 | PA 2.2 | Work product management |
| 3 | PA 3.1 | Process definition |
| 3 | PA 3.2 | Process deployment |
| 4 | PA 4.1 | Quantitative analysis |
| 4 | PA 4.2 | Quantitative control |
| 5 | PA 5.1 | Process innovation |
| 5 | PA 5.2 | Process innovation implementation |

### Table 16 — Rating scale

**Clause:** 3.2.2.1  
**Source anchor:** aspice40_layout.txt lines 887–908  
**Confidence:** `high`

| Rating | Name | Explicit interpretation |
|---|---|---|
| N | Not achieved | Little or no evidence of achievement of the defined process attribute. |
| P | Partially achieved | Some evidence of an approach and some achievement; some aspects may be unpredictable. |
| L | Largely achieved | Evidence of a systematic approach and significant achievement; some weaknesses may exist. |
| F | Fully achieved | Evidence of a complete and systematic approach and full achievement; no significant weaknesses. |

### Table 17 — Rating scale percentage values

**Clause:** 3.2.2.1  
**Source anchor:** aspice40_layout.txt lines 909–916  
**Confidence:** `high`

| Rating | Achievement interval |
|---|---|
| N | 0 to ≤ 15% achievement |
| P | > 15% to ≤ 50% achievement |
| L | > 50% to ≤ 85% achievement |
| F | > 85% to ≤ 100% achievement |

### Table 19 — Refined rating scale percentage values

**Clause:** 3.2.2  
**Source anchor:** aspice40_layout.txt lines 945–950  
**Confidence:** `high`

| Rating | Achievement interval |
|---|---|
| P− | > 15% to ≤ 32.5% achievement |
| P+ | > 32.5% to ≤ 50% achievement |
| L− | > 50% to ≤ 67.5% achievement |
| L+ | > 67.5% to ≤ 85% achievement |

### PIM.3 matrix — PIM.3 Process Improvement — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 4249  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 02-01 | Commitment/agreement | O1 | true |
| Output Information Item | 06-04 | Training material | O4, O6 | true |
| Output Information Item | 07-04 | Process metric | O5, O6 | true |
| Output Information Item | 10-00 | Process description | O4 | true |
| Output Information Item | 13-52 | Communication evidence | O6 | true |
| Output Information Item | 13-16 | Change request | O2 | true |
| Output Information Item | 15-51 | Analysis result | O2, O3, O4, O5 | true |
| Output Information Item | 15-13 | Assessment/audit report | O3, O5 | true |
| Output Information Item | 15-16 | Improvement opportunity | O2, O3, O4 | true |
| Output Information Item | 16-06 | Process repository | O4 | true |
| Base Practice | BP1 | Establish commitment | O1 | true |
| Base Practice | BP2 | Identify improvement measures | O2, O3 | true |
| Base Practice | BP3 | Establish process improvement goals | O4 | true |
| Base Practice | BP4 | Prioritize improvements | O3 | true |
| Base Practice | BP5 | Define process improvement measures | O3 | true |
| Base Practice | BP6 | Implement process improvement measures | O3 | true |
| Base Practice | BP7 | Confirm process improvement | O3 | true |
| Base Practice | BP8 | Communicate results of improvement | O4 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### REU.2 matrix — REU.2 Management of Products for Reuse — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 4343  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 04-02 | Domain architecture | O2, O3 | true |
| Output Information Item | 12-03 | Reuse candidate | O1, O5 | true |
| Output Information Item | 13-52 | Communication evidence | O6 | true |
| Output Information Item | 15-07 | Reuse analysis evidence | O2, O3 | true |
| Output Information Item | 13-53 | Qualification evidence | O4 | true |
| Base Practice | BP1 | Select products for reuse | O1 | true |
| Base Practice | BP2 | Analyze the reuse capability of the product | O2 | true |
| Base Practice | BP3 | Define limitations for reuse | O3 | true |
| Base Practice | BP4 | Ensure qualification of products for reuse | O4 | true |
| Base Practice | BP5 | Provide products for reuse | O5 | true |
| Base Practice | BP6 | Communicate information about effectiveness of reuse activities | O6 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### ACQ.4 matrix — ACQ.4 Supplier Monitoring — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1247  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 02-01 | Commitment/Agreement | O1, O2, O3, O4 | true |
| Output Information Item | 13-52 | Communication evidence | O1, O2, O3 | true |
| Output Information Item | 13-09 | Meeting support evidence | O1, O2 | true |
| Output Information Item | 13-14 | Progress status | O2, O3 | true |
| Output Information Item | 13-16 | Change request | O4 | true |
| Output Information Item | 13-19 | Review evidence | O2 | true |
| Output Information Item | 14-02 | Corrective action | O4 | true |
| Output Information Item | 15-51 | Analysis results | O3 | true |
| Base Practice | BP1 | Agree on and maintain joint processes, joint interfaces, and information to be exchanged | O1, O2, O4 | true |
| Base Practice | BP2 | Exchange all agreed information | O1, O2, O3 | true |
| Base Practice | BP3 | Review development work products with the supplier | O1, O3, O4 | true |
| Base Practice | BP4 | Review progress of the supplier | O1, O3, O4 | true |
| Base Practice | BP5 | Act to correct deviations | O3, O4 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SPL.2 matrix — SPL.2 Product Release — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1334  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 11-03 | Release note | O1, O3, O4, O5 | true |
| Output Information Item | 11-04 | Product release package | O2, O3 | true |
| Output Information Item | 13-06 | Delivery evidence | O3, O5 | true |
| Output Information Item | 13-13 | Product release approval | O4, O5 | true |
| Output Information Item | 18-06 | Product release criteria | O1, O2, O4 | true |
| Base Practice | BP1 | Define the functional content of releases | O1 | true |
| Base Practice | BP2 | Define release package | O1 | true |
| Base Practice | BP3 | Establish a product release classification and numbering scheme | O1 | true |
| Base Practice | BP4 | Build the release from configured items | O1 | true |
| Base Practice | BP5 | Ensure product release approval before delivery | O1 | true |
| Base Practice | BP6 | Provide a release note | O1 | true |
| Base Practice | BP7 | Communicate the type, service level and duration of support for a release | O1 | true |
| Base Practice | BP8 | Deliver the release package to the intended customer | O1 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SYS.1 matrix — SYS.1 Requirements Elicitation — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1417  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 15-51 | Analysis Results | O3 | true |
| Output Information Item | 13-52 | Communication Evidence | O1, O2 | true |
| Output Information Item | 17-00 | Requirement | O2 | true |
| Output Information Item | 17-54 | Requirement Attribute | O2, O3, O4 | true |
| Base Practice | BP1 | Obtain stakeholder expectations and requests | O1 | true |
| Base Practice | BP2 | Agree on requirements | O2 | true |
| Base Practice | BP3 | Analyze stakeholder requirements changes | O3 | true |
| Base Practice | BP4 | Communicate requirements status | O1, O4 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SYS.2 matrix — SYS.2 System Requirements Analysis — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1510  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 17-00 | Requirement | O1, O2 | true |
| Output Information Item | 17-54 | Requirement Attribute | O2, O3 | true |
| Output Information Item | 15-51 | Analysis Results | O3, O4 | true |
| Output Information Item | 13-51 | Consistency Evidence | O5 | true |
| Output Information Item | 13-52 | Communication Evidence | O6 | true |
| Base Practice | BP1 | Specify system requirements | O1 | true |
| Base Practice | BP2 | Structure system requirements | O2 | true |
| Base Practice | BP3 | Analyze system requirements | O3 | true |
| Base Practice | BP4 | Analyze the impact on the system context | O4 | true |
| Base Practice | BP5 | Ensure consistency and establish bidirectional traceability | O5 | true |
| Base Practice | BP6 | Communicate agreed system requirements and impact on the system context | O6 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SYS.3 matrix — SYS.3 System Architectural Design — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1598  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 04-06 | System Architecture | O1 | true |
| Output Information Item | 13-51 | Consistency Evidence | O3 | true |
| Output Information Item | 13-52 | Communication Evidence | O4 | true |
| Output Information Item | 15-51 | Analysis Results | O2 | true |
| Output Information Item | 17-57 | Special Characteristics | O2 | true |
| Base Practice | BP1 | Specify static aspects of system architecture | O1 | true |
| Base Practice | BP2 | Specify dynamic aspects of system architecture | O1 | true |
| Base Practice | BP3 | Analyze the system architecture | O2 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability | O3 | true |
| Base Practice | BP5 | Communicate agreed system architecture | O1 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SYS.4 matrix — SYS.4 System Integration and Integration Verification — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1708  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-60 | Verification Measure | O1 | true |
| Output Information Item | 06-50 | Integration Sequence Instruction | O2 | true |
| Output Information Item | 03-50 | Verification Measure Data | O4 | true |
| Output Information Item | 08-58 | Verification Measure Selection Set | O3 | true |
| Output Information Item | 15-52 | Verification Results | O4 | true |
| Output Information Item | 13-51 | Consistency Evidence | O5, O6 | true |
| Output Information Item | 13-52 | Communication Evidence | O7 | true |
| Output Information Item | 11-06 | Integrated System | O2 | true |
| Base Practice | BP1 | Specify verification measures for system integration | O1 | true |
| Base Practice | BP2 | Select verification measures | O3 | true |
| Base Practice | BP3 | Integrate system elements and perform integration verification. | O2, O4 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability | O5, O6 | true |
| Base Practice | BP5 | Summarize and communicate results | O7 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SYS.5 matrix — SYS.5 System Verification — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1805  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-60 | Verification Measure | O1 | true |
| Output Information Item | 03-50 | Verification Measure Data | O3 | true |
| Output Information Item | 08-58 | Verification Measure Selection Set | O2 | true |
| Output Information Item | 15-52 | Verification Results | O3 | true |
| Output Information Item | 13-51 | Consistency Evidence | O4, O5 | true |
| Output Information Item | 13-52 | Communication Evidence | O6 | true |
| Base Practice | BP1 | Specify verification measures for system verification | O1 | true |
| Base Practice | BP2 | Select verification measures | O2 | true |
| Base Practice | BP3 | Perform verification of the integrated system | O3 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability. | O4, O5 | true |
| Base Practice | BP5 | Summarize and communicate results | O6 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SWE.1 matrix — SWE.1 Software Requirements Analysis — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 1916  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 17-00 | Requirement | O1, O2 | true |
| Output Information Item | 17-54 | Requirement Attribute | O2 | true |
| Output Information Item | 15-51 | Analysis Results | O3, O4 | true |
| Output Information Item | 13-51 | Consistency Evidence | O5, O6 | true |
| Output Information Item | 13-52 | Communication Evidence | O7 | true |
| Base Practice | BP1 | Specify software requirements | O1 | true |
| Base Practice | BP2 | Structure software requirements | O1 | true |
| Base Practice | BP3 | Analyze software requirements | O2 | true |
| Base Practice | BP4 | Analyze the impact on the operating environment | O2 | true |
| Base Practice | BP5 | Ensure consistency and establish bidirectional traceability | O3 | true |
| Base Practice | BP6 | Communicate agreed software requirements and impact on the operating environment | O4 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SWE.2 matrix — SWE.2 Software Architectural Design — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2008  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 04-04 | Software Architecture | O1 | true |
| Output Information Item | 13-51 | Consistency Evidence | O3 | true |
| Output Information Item | 13-52 | Communication Evidence | O4 | true |
| Output Information Item | 15-51 | Analysis Results | O2 | true |
| Base Practice | BP1 | Specify static aspects of software architecture | O1 | true |
| Base Practice | BP2 | Specify dynamic aspects of software architecture | O1 | true |
| Base Practice | BP3 | Analyze software architecture | O2 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability | O3 | true |
| Base Practice | BP5 | Communicate agreed software architecture | O4 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SWE.3 matrix — SWE.3 Software Detailed Design and Unit Construction — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2105  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 04-05 | Software Detailed Design | O1 | true |
| Output Information Item | 11-05 | Software Unit | O1, O2 | true |
| Output Information Item | 13-51 | Consistency Evidence | O3 | true |
| Output Information Item | 13-52 | Communication Evidence | O4 | true |
| Base Practice | BP1 | Specify the static aspects of the detailed design | O1 | true |
| Base Practice | BP2 | Specify the dynamic aspects of the detailed design | O1 | true |
| Base Practice | BP3 | Develop software units | O2 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability | O3 | true |
| Base Practice | BP5 | Communicate agreed software detailed design and developed software units | O2 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SWE.4 matrix — SWE.4 Software Unit Verification — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2190  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-60 | Verification Measure | O1 | true |
| Output Information Item | 03-50 | Verification Measure Data | O3 | true |
| Output Information Item | 08-58 | Verification Measure Selection Set | O2 | true |
| Output Information Item | 15-52 | Verification Results | O3 | true |
| Output Information Item | 13-51 | Consistency Evidence | O4 | true |
| Output Information Item | 13-52 | Communication Evidence | O5 | true |
| Base Practice | BP1 | Specify software unit verification measures | O1 | true |
| Base Practice | BP2 | Select software unit verification measures | O2 | true |
| Base Practice | BP3 | Verify software units | O3 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability for software unit verification | O4 | true |
| Base Practice | BP5 | Summarize and communicate results | O5 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SWE.5 matrix — SWE.5 Software Component Verification and — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2328  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-60 | Verification Measure | O1, O2 | true |
| Output Information Item | 06-50 | Integration Sequence Instruction | O3 | true |
| Output Information Item | 03-50 | Verification Measure Data | O5 | true |
| Output Information Item | 08-58 | Verification Measure Selection Set | O4 | true |
| Output Information Item | 15-52 | Verification Results | O5, O6 | true |
| Output Information Item | 13-51 | Consistency Evidence | O7 | true |
| Output Information Item | 13-52 | Communication Evidence | O8 | true |
| Output Information Item | 01-03 | Software Component | O3 | true |
| Output Information Item | 01-50 | Integrated Software | O3 | true |
| Base Practice | BP1 | Specify software integration verification measures | O1 | true |
| Base Practice | BP2 | Specify verification measures for verifying software component behavior | O2 | true |
| Base Practice | BP3 | Select verification measures | O4 | true |
| Base Practice | BP4 | Integrate software elements and perform integration verification | O3, O6 | true |
| Base Practice | BP5 | Perform software component verification | O5 | true |
| Base Practice | BP6 | Ensure consistency and establish bidirectional traceability | O7 | true |
| Base Practice | BP7 | Summarize and communicate results | O8 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SWE.6 matrix — SWE.6 Software Verification — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2435  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-60 | Verification Measure | O1 | true |
| Output Information Item | 03-50 | Verification Measure Data | O3 | true |
| Output Information Item | 08-58 | Verification Measure Selection Set | O2 | true |
| Output Information Item | 15-52 | Verification Results | O3 | true |
| Output Information Item | 13-51 | Consistency Evidence | O4 | true |
| Output Information Item | 13-52 | Communication Evidence | O5 | true |
| Base Practice | BP1 | Specify verification measures for software verification | O1 | true |
| Base Practice | BP2 | Select verification measures | O2 | true |
| Base Practice | BP3 | Verify the integrated software | O3 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability. | O4 | true |
| Base Practice | BP5 | Summarize and communicate results | O2 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### VAL.1 matrix — VAL.1 Validation — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2542  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-59 | Validation Measure | O1 | true |
| Output Information Item | 08-57 | Validation Measure Selection Set | O1 | true |
| Output Information Item | 13-24 | Validation Results | O2 | true |
| Output Information Item | 13-51 | Consistency Evidence | O3 | true |
| Output Information Item | 13-52 | Communication Evidence | O4 | true |
| Base Practice | BP1 | Specify validation measures | O1 | true |
| Base Practice | BP2 | Select validation measures | O1 | true |
| Base Practice | BP3 | Perform validation and evaluate results | O2 | true |
| Base Practice | BP4 | Ensure consistency and establish traceability. | O3 | true |
| Base Practice | BP5 | Summarize and communicate results | O4 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### MLE.1 matrix — MLE.1 Machine Learning Requirements Analysis — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2638  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 17-00 | Requirement | O1, O2 | true |
| Output Information Item | 17-54 | Requirement attribute | O2, O3 | true |
| Output Information Item | 13-52 | Communication evidence | O6 | true |
| Output Information Item | 13-51 | Consistency evidence | O5 | true |
| Output Information Item | 15-51 | Analysis results | O3, O4 | true |
| Base Practice | BP1 | Specify ML requirements | O1 | true |
| Base Practice | BP2 | Structure ML requirements | O2 | true |
| Base Practice | BP3 | Analyze ML requirements | O3 | true |
| Base Practice | BP4 | Analyze the impact on the ML operating environment | O4 | true |
| Base Practice | BP5 | Ensure consistency and establish bidirectional traceability | O5 | true |
| Base Practice | BP6 | Communicate agreed ML requirements | O6 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### MLE.2 matrix — MLE.2 Machine Learning Architecture — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2733  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 04-51 | ML architecture | O1, O2, O3, O4, O5 | true |
| Output Information Item | 13-52 | Communication evidence | O7 | true |
| Output Information Item | 13-51 | Consistency evidence | O6 | true |
| Output Information Item | 01-54 | Hyperparameter | O1, O2 | true |
| Output Information Item | 15-51 | Analysis results | O1, O3 | true |
| Base Practice | BP1 | Develop ML architecture | O1 | true |
| Base Practice | BP2 | Determine hyperparameter ranges and initial values. | O2 | true |
| Base Practice | BP3 | Evaluate ML architectural elements | O3 | true |
| Base Practice | BP4 | Define interfaces of the ML architectural elements | O4 | true |
| Base Practice | BP5 | Define resource consumption objectives for the ML architectural elements | O5 | true |
| Base Practice | BP6 | Ensure consistency and establish bidirectional traceability | O6 | true |
| Base Practice | BP7 | Communicate agreed ML architecture | O7 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### MLE.3 matrix — MLE.3 Machine Learning Training — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2826  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-65 | ML training and validation approach | O1 | true |
| Output Information Item | 03-51 | ML data set | O2 | true |
| Output Information Item | 01-53 | Trained ML model | O3 | true |
| Output Information Item | 01-54 | Hyperparameter | O3 | true |
| Output Information Item | 13-51 | Consistency evidence | O4 | true |
| Output Information Item | 13-52 | Communication evidence | O5 | true |
| Base Practice | BP1 | Specify ML training and validation approach | O1 | true |
| Base Practice | BP2 | Create ML training and validation data set | O2 | true |
| Base Practice | BP3 | Create and optimize ML model | O3 | true |
| Base Practice | BP4 | Ensure consistency and establish bidirectional traceability | O4 | true |
| Base Practice | BP5 | Summarize and communicate agreed trained ML model | O5 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### MLE.4 matrix — MLE.4 Machine Learning Model Testing — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 2932  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-64 | ML test approach | O1 | true |
| Output Information Item | 03-51 | ML data set | O2 | true |
| Output Information Item | 13-50 | ML test results | O3, O4 | true |
| Output Information Item | 11-50 | Deployed ML model | O4 | true |
| Output Information Item | 13-51 | Consistency evidence | O5 | true |
| Output Information Item | 13-52 | Communication evidence | O6 | true |
| Base Practice | BP1 | Specify an ML test approach | O1 | true |
| Base Practice | BP2 | Create ML test data set | O1 | true |
| Base Practice | BP3 | Test trained ML model | O1 | true |
| Base Practice | BP4 | Derive deployed ML model | O1 | true |
| Base Practice | BP5 | Test deployed ML model | O1 | true |
| Base Practice | BP6 | Ensure consistency and establish bidirectional traceability | O1 | true |
| Base Practice | BP7 | Summarize and communicate results | O1 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### HWE.1 matrix — HWE.1 Hardware Requirements Analysis — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3050  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 13-52 | Communication Evidence | O7 | true |
| Output Information Item | 13-51 | Consistency Evidence | O5, O6 | true |
| Output Information Item | 17-00 | Requirement | O1, O2, O3 | true |
| Output Information Item | 17-54 | Requirement Attribute | O1 | true |
| Output Information Item | 15-51 | Analysis Results | O1 | true |
| Base Practice | BP1 | Specify hardware requirements | O1 | true |
| Base Practice | BP2 | Structure hardware requirements | O1 | true |
| Base Practice | BP3 | Analyze hardware requirements | O1 | true |
| Base Practice | BP4 | Analyze the impact on the operating environment | O1 | true |
| Base Practice | BP5 | Ensure consistency and establish bidirectional traceability | O2 | true |
| Base Practice | BP6 | Communicate agreed hardware requirements | O3 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### HWE.2 matrix — HWE.2 Hardware Design — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3157  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 04-52 | Hardware Architecture | O1 | true |
| Output Information Item | 04-53 | Hardware Detailed Design | O1 | true |
| Output Information Item | 15-51 | Analysis Results | O2 | true |
| Output Information Item | 13-51 | Consistency Evidence | O3 | true |
| Output Information Item | 17-57 | Special Characteristics | O2 | true |
| Output Information Item | 13-52 | Communication Evidence | O6 | true |
| Output Information Item | 04-54 | Hardware Schematics | O1, O4, O5 | true |
| Output Information Item | 14-54 | Hardware Bill of Materials | O1, O4, O5 | true |
| Output Information Item | 04-55 | Hardware Layout | O1, O4, O5 | true |
| Output Information Item | 03-54 | Hardware Production Data | O1, O4, O5 | true |
| Output Information Item | 04-56 | Hardware Element Interface | O1 | true |
| Base Practice | BP1 | Specify the hardware architecture | O1, O4, O5 | true |
| Base Practice | BP2 | Specify the hardware detailed design | O1, O4, O5 | true |
| Base Practice | BP3 | Specify dynamic aspects | O1 | true |
| Base Practice | BP4 | Analyze the hardware architecture and the hardware detailed design | O2 | true |
| Base Practice | BP5 | Ensure consistency and establish bidirectional traceability | O3 | true |
| Base Practice | BP7 | Communicate agreed hardware architecture and hardware detailed design | O4, O5, O6 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### HWE.3 matrix — HWE.3 Verification against Hardware Design — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3271  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-60 | Verification Measure | O1 | true |
| Output Information Item | 03-50 | Verification Measure Data | O3 | true |
| Output Information Item | 08-58 | Verification Measure Selection Set | O2 | true |
| Output Information Item | 15-52 | Verification Results | O3 | true |
| Output Information Item | 13-51 | Consistency Evidence | O4, O5 | true |
| Output Information Item | 13-52 | Communication Evidence | O6 | true |
| Base Practice | BP1 | Specify verification measures for the verification against hardware design | O1 | true |
| Base Practice | BP2 | Ensure use of compliant samples | O3 | true |
| Base Practice | BP3 | Select verification measures | O2 | true |
| Base Practice | BP4 | Verify hardware design | O3 | true |
| Base Practice | BP5 | Ensure consistency and establish bidirectional traceability | O4, O5 | true |
| Base Practice | BP6 | Summarize and communicate results | O6 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### HWE.4 matrix — HWE.4 Verification against Hardware Requirements — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3372  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-60 | Verification Measure | O1 | true |
| Output Information Item | 03-50 | Verification Measure Data | O3 | true |
| Output Information Item | 08-58 | Verification Measure Selection Set | O2 | true |
| Output Information Item | 15-52 | Verification Results | O3 | true |
| Output Information Item | 13-51 | Consistency Evidence | O4, O5 | true |
| Output Information Item | 13-52 | Communication Evidence | O6 | true |
| Base Practice | BP1 | Specify verification measures for the verification against hardware requirements | O1 | true |
| Base Practice | BP2 | Ensure use of compliant samples | O3 | true |
| Base Practice | BP3 | Select verification measures | O2 | true |
| Base Practice | BP4 | Verify hardware | O3 | true |
| Base Practice | BP5 | Ensure consistency and establish bidirectional traceability | O4, O5 | true |
| Base Practice | BP6 | Summarize and communicate results | O6 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SUP.1 matrix — SUP.1 Quality Assurance — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3471  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 16-50 | Organizational structure | O1, O5 | true |
| Output Information Item | 18-52 | Escalation path | O5, O6 | true |
| Output Information Item | 18-07 | Quality criteria | O2, O3, O4 | true |
| Output Information Item | 13-52 | Communication evidence | O3, O4, O5 | true |
| Output Information Item | 13-18 | Quality conformance evidence | O3, O4 | true |
| Output Information Item | 13-19 | Review evidence | O3, O4 | true |
| Output Information Item | 14-02 | Corrective action | O4, O6 | true |
| Base Practice | BP1 | Ensure independence of quality assurance. | O1 | true |
| Base Practice | BP2 | Define criteria for quality assurance. | O2 | true |
| Base Practice | BP3 | Assure quality of work products. | O3, O4 | true |
| Base Practice | BP4 | Assure quality of process activities. | O3, O4 | true |
| Base Practice | BP5 | Summarize and communicate quality assurance activities and results. | O2, O3 | true |
| Base Practice | BP6 | Ensure resolution of non-conformances. | O2, O3 | true |
| Base Practice | BP7 | Escalate non-conformances. | O3 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SUP.8 matrix — SUP.8 Configuration Management — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3588  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 18-53 | Configuration item selection criteria | O1 | true |
| Output Information Item | 01-52 | Configuration item list | O1, O2, O7 | true |
| Output Information Item | 16-03 | Configuration management system | O3, O4, O5 | true |
| Output Information Item | 13-08 | Baseline | O5, O7 | true |
| Output Information Item | 14-01 | Change history | O2, O3 | true |
| Output Information Item | 15-56 | Configuration status | O3 | true |
| Output Information Item | 13-51 | Consistency Evidence | O3 | true |
| Output Information Item | 06-52 | Backup and recovery mechanism information | O3 | true |
| Base Practice | BP1 | Identify configuration items | O1 | true |
| Base Practice | BP2 | Define configuration item properties | O1 | true |
| Base Practice | BP3 | Establish configuration management | O2 | true |
| Base Practice | BP4 | Control modifications | O2 | true |
| Base Practice | BP5 | Establish baselines | O2 | true |
| Base Practice | BP6 | Summarize and communicate configuration status | O3 | true |
| Base Practice | BP7 | Ensure completeness and consistency | O3 | true |
| Base Practice | BP8 | Verify backup and recovery mechanisms availability | O3 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SUP.9 matrix — SUP.9 Problem Resolution Management — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3683  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 13-07 | Problem | O1, O2, O3, O4 | true |
| Output Information Item | 15-55 | Problem analysis evidence | O2 | true |
| Output Information Item | 15-12 | Problem status | O3 | true |
| Base Practice | BP1 | Identify and record the problem | O1, O2 | true |
| Base Practice | BP2 | Determine the cause and the impact of the problem | O1 | true |
| Base Practice | BP3 | Authorize urgent resolution action | O2 | true |
| Base Practice | BP4 | Raise alert notifications | O2 | true |
| Base Practice | BP5 | Initiate problem resolution | O2 | true |
| Base Practice | BP6 | Track problems to closure | O2, O3 | true |
| Base Practice | BP7 | Report the status of problem resolution activities | O3 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SUP.10 matrix — SUP.10 Change Request Management — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3774  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 18-57 | Change analysis criteria | O2 | true |
| Output Information Item | 13-16 | Change request | O1, O2, O3, O5, O6 | true |
| Output Information Item | 13-51 | Consistency evidence | O4 | true |
| Base Practice | BP1 | Identify and record the change requests | O1 | true |
| Base Practice | BP2 | Analyze and assess change requests | O2 | true |
| Base Practice | BP3 | Approve change requests before implementation | O3 | true |
| Base Practice | BP4 | Establish bidirectional traceability | O4 | true |
| Base Practice | BP5 | Confirm the implementation of change requests | O5 | true |
| Base Practice | BP6 | Track change requests to closure | O4 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### SUP.11 matrix — SUP.11 Machine Learning Data Management — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3858  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 16-52 | ML data management system | O1 | true |
| Output Information Item | 19-50 | ML data quality approach | O2 | true |
| Output Information Item | 03-53 | ML data | O3, O4 | true |
| Output Information Item | 13-52 | Communication evidence | O5 | true |
| Base Practice | BP1 | Establish an ML data management system | O1 | true |
| Base Practice | BP2 | Develop an ML data quality approach | O2 | true |
| Base Practice | BP3 | Collect ML data | O3 | true |
| Base Practice | BP4 | Process ML data | O3 | true |
| Base Practice | BP5 | Assure quality of ML data | O4 | true |
| Base Practice | BP6 | Communicate agreed processed ML data | O5 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### MAN.3 matrix — MAN.3 Project Management — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 3970  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 08-53 | Scope of work | O1 | true |
| Output Information Item | 08-54 | Feasibility analysis | O2, O4 | true |
| Output Information Item | 14-10 | Work package | O3, O4, O5 | true |
| Output Information Item | 13-52 | Communication evidence | O1 | true |
| Output Information Item | 13-16 | Change request | O3 | true |
| Output Information Item | 13-51 | Consistency evidence | O1, O3 | true |
| Output Information Item | 14-02 | Corrective action | O3 | true |
| Output Information Item | 18-52 | Escalation path | O2, O3 | true |
| Output Information Item | 08-56 | Schedule | O1, O2, O3 | true |
| Output Information Item | 14-50 | Stakeholder groups list | O2 | true |
| Output Information Item | 15-06 | Project status | O2, O3 | true |
| Base Practice | BP1 | Define the scope of work | O1 | true |
| Base Practice | BP2 | Define project life cycle | O1 | true |
| Base Practice | BP3 | Evaluate feasibility of the project | O1 | true |
| Base Practice | BP4 | Define and monitor work packages | O1, O2, O3 | true |
| Base Practice | BP5 | Define and monitor project estimates and resources | O1, O3 | true |
| Base Practice | BP6 | Define and monitor required skills, knowledge, and experience | O1, O3 | true |
| Base Practice | BP7 | Define and monitor project interfaces and agreed commitments | O1, O2, O3 | true |
| Base Practice | BP8 | Define and monitor project schedule | O3 | true |
| Base Practice | BP9 | Ensure consistency | O1, O2, O3 | true |
| Base Practice | BP10 | Review and report progress of the project | O3 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### MAN.5 matrix — MAN.5 Risk Management — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 4070  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 15-51 | Analysis results | O1, O2, O3, O5 | true |
| Output Information Item | 15-09 | Risk status | O1, O3, O4, O5 | true |
| Output Information Item | 08-55 | Risk measure | O4, O5 | true |
| Output Information Item | 14-02 | Corrective action | O2 | true |
| Base Practice | BP1 | Identify sources of risks | O1 | true |
| Base Practice | BP2 | Identify potential undesirable events | O1 | true |
| Base Practice | BP3 | Determine risks | O1 | true |
| Base Practice | BP4 | Define risk treatment options | O2 | true |
| Base Practice | BP5 | Define and perform risk treatment activities. | O2 | true |
| Base Practice | BP6 | Monitor risks | O2 | true |
| Base Practice | BP7 | Take corrective action | O2 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.

### MAN.6 matrix — MAN.6 Measurement — explicit Outcome mapping

**Clause:** Chapter 4  
**Source anchor:** aspice40_visual_matrices.json source_layout_line 4152  
**Confidence:** `high`

| Row type | Row ID | Name | Mapped Outcomes | Mapped |
|---|---|---|---|---|
| Output Information Item | 03-03 | Benchmarking data | O4, O5 | true |
| Output Information Item | 03-04 | Customer satisfaction data | O4, O5 | true |
| Output Information Item | 03-06 | Process performance information | O4, O5 | true |
| Output Information Item | 07-51 | Measurement result | O2, O3, O4, O5 | true |
| Output Information Item | 15-51 | Analysis results | O1, O4, O5 | true |
| Base Practice | BP1 | Identify information needs | O1 | true |
| Base Practice | BP2 | Specify metrics | O2, O3 | true |
| Base Practice | BP3 | Collect and store metrics | O3, O4 | true |
| Base Practice | BP4 | Analyze collected metrics | O4, O5 | true |
| Base Practice | BP5 | Communicate measurement information | O5 | true |
| Base Practice | BP6 | Use metrics for decision-making | O5 | true |

> **Notes:** The original standalone X marks are represented as explicit mapped=true plus a named outcome list.

> **Manual review:** Verify horizontal X positions against the original PDF before using this mapping as normative assessment evidence.
