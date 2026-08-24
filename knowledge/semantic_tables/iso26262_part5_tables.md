# ISO 26262-5 semantic tables

This output converts ASIL matrices, safety metrics and hardware integration test tables into explicit columns. A symbol is never left without the ASIL or metric column that gives it meaning.

## Symbol and empty-cell semantics

| Symbol／form | Table context | Explicit meaning |
|---|---|---|
| + | Tables 1–3 and 10–12 | recommended method／property for the ASIL column shown |
| ++ | Tables 1–3 and 10–12 | stronger／higher recommendation for the ASIL column shown |
| o | Tables 2, 10 and 12 | no specific recommendation for the ASIL column shown |
| — | notes or table cells | no information／not applicable only where the source table defines it; never a missing number |
| ≥／< | metric and failure-rate tables | inequality operator belonging to the numeric target field |

## Reconstructed tables

### Table 1 — Properties of hardware architectural design

**Clause:** 7.4.1.6  
**Source anchor:** iso26262_part5_layout.txt lines 787–797; PDF physical page 18 / printed page 10  
**Confidence:** `high`

| Property | ASIL A | ASIL B | ASIL C | ASIL D |
|---|---|---|---|---|
| Hierarchical design | + | + | + | + |
| Precisely defined interfaces of safety-related hardware components | ++ | ++ | ++ | ++ |
| Avoidance of unnecessary complexity of interfaces | + | + | + | + |
| Avoidance of unnecessary complexity of hardware components | + | + | + | + |
| Maintainability (service) | + | + | ++ | ++ |
| Testability | + | + | ++ | ++ |

> **Notes:** Testability includes development, production, service and operation.

### Table 2 — Hardware design safety analysis

**Clause:** 7.4.3.1  
**Source anchor:** iso26262_part5_layout.txt lines 846–855  
**Confidence:** `high`

| Method | ASIL A | ASIL B | ASIL C | ASIL D |
|---|---|---|---|---|
| Deductive analysis | o | + | ++ | ++ |
| Inductive analysis | ++ | ++ | ++ | ++ |

### Table 4 — Target single-point fault metric

**Clause:** 8.4.5  
**Source anchor:** iso26262_part5_layout.txt lines 744–754  
**Confidence:** `high`

| Metric | ASIL B | ASIL C | ASIL D |
|---|---|---|---|
| Single-point fault metric | ≥90% | ≥97% | ≥99% |

### Table 5 — Target latent-fault metric

**Clause:** 8.4.6  
**Source anchor:** iso26262_part5_layout.txt lines 765–775  
**Confidence:** `high`

| Metric | ASIL B | ASIL C | ASIL D |
|---|---|---|---|
| Latent-fault metric | ≥60% | ≥80% | ≥90% |

### Table 6 — Random hardware failure target values

**Clause:** 9.4.2.2  
**Source anchor:** iso26262_part5_layout.txt lines 1587–1593  
**Confidence:** `high`

| ASIL | Random hardware failure target value |
|---|---|
| D | <10^-8 h^-1 |
| C | <10^-7 h^-1 |
| B | <10^-7 h^-1 |

> **Notes:** The h^-1 unit and inequality sign belong to the target value and must not be separated.

### Table 7 — Failure-rate-class targets for single-point faults

**Clause:** 9.4.3.5  
**Source anchor:** iso26262_part5_layout.txt lines 1822–1831  
**Confidence:** `high`

| ASIL of safety goal | Acceptable failure-rate-class target |
|---|---|
| D | Failure rate class 1 + dedicated measures |
| C | Failure rate class 2 + dedicated measures, or failure rate class 1 |
| B | Failure rate class 2, or failure rate class 1 |

### Table 8 — Maximum failure-rate classes for residual faults

**Clause:** 9.4.3.6  
**Source anchor:** iso26262_part5_layout.txt lines 1854–1869  
**Confidence:** `high`

| ASIL | DC ≥99.9% | DC ≥99% | DC ≥90% | DC <90% |
|---|---|---|---|---|
| D | Class 4 | Class 3 | Class 2 | Class 1 + dedicated measures |
| C | Class 5 | Class 4 | Class 3 | Class 2 + dedicated measures |
| B | Class 5 | Class 4 | Class 3 | Class 2 |

### Table 9 — Failure-rate-class and coverage targets for plausible dual-point faults

**Clause:** 9.4.3.11  
**Source anchor:** iso26262_part5_layout.txt lines 1931–1939  
**Confidence:** `high`

| ASIL | Latent DC ≥99% | Latent DC ≥90% | Latent DC <90% |
|---|---|---|---|
| D | Class 4 | Class 3 | Class 2 |
| C | Class 5 | Class 4 | Class 3 |

### Table 10 — Methods for deriving test cases for hardware integration testing

**Clause:** 10.4.4  
**Source anchor:** iso26262_part5_layout.txt lines 2054–2073  
**Confidence:** `high`

| Method | ASIL A | ASIL B | ASIL C | ASIL D |
|---|---|---|---|---|
| Analysis of requirements | ++ | ++ | ++ | ++ |
| Analysis of internal and external interfaces | + | ++ | ++ | ++ |
| Generation and analysis of equivalence classes | + | + | ++ | ++ |
| Analysis of boundary values | + | + | ++ | ++ |
| Knowledge or experience based error guessing | ++ | ++ | ++ | ++ |
| Analysis of functional dependencies | + | + | ++ | ++ |
| Analysis of common limit conditions, sequences and dependent failures | + | + | ++ | ++ |
| Analysis of environmental conditions and operational use cases | + | ++ | ++ | ++ |
| Standards if existing | + | + | + | + |
| Analysis of significant variants | ++ | ++ | ++ | ++ |

### Table 11 — Hardware integration tests for completeness and correctness

**Clause:** 10.4.5  
**Source anchor:** iso26262_part5_layout.txt lines 2080–2094  
**Confidence:** `high`

| Method | ASIL A | ASIL B | ASIL C | ASIL D |
|---|---|---|---|---|
| Functional testing | ++ | ++ | ++ | ++ |
| Fault injection testing | + | + | ++ | ++ |
| Electrical testing | ++ | ++ | ++ | ++ |

### Table 12 — Hardware integration tests under environmental and operational stresses

**Clause:** 10.4.6  
**Source anchor:** iso26262_part5_layout.txt lines 2111–2148  
**Confidence:** `high`

| Method | ASIL A | ASIL B | ASIL C | ASIL D |
|---|---|---|---|---|
| Environmental testing with basic functional verification | ++ | ++ | ++ | ++ |
| Expanded functional test | o | + | + | ++ |
| Statistical test | o | o | + | ++ |
| Worst case test | o | o | o | + |
| Over limit test | + | + | + | + |
| Mechanical test | ++ | ++ | ++ | ++ |
| Accelerated life test | + | + | ++ | ++ |
| Mechanical Endurance test | ++ | ++ | ++ | ++ |
| EMC and ESD test | ++ | ++ | ++ | ++ |
| Chemical test | ++ | ++ | ++ | ++ |
