# ISO/SAE 21434 semantic tables

This output converts CAL, independence, testing and risk matrices into explicit rows and columns. Symbols such as X, — and --- are interpreted only within the table context that defines them.

## Symbol and empty-cell semantics

| Symbol／form | Table context | Explicit meaning |
|---|---|---|
| --- | Table E.1, Negligible impact row | not applicable／no CAL assigned for that impact and attack-vector combination, as defined by the table footnote |
| — | Tables E.3–E.4 | no suggestion regarding independence or testing parameters |
| X | Table H.2 | the corresponding cybersecurity property is affected／relevant for that asset or damage scenario |
| ― | Table H.2 | the corresponding cybersecurity property is not affected／not relevant |
| I1／I2／I3 | Table E.3 | increasing independence level defined by the table notes |
| T1／T2 | Table E.4 | testing parameter set 1 or 2, not an unqualified test result |

## Reconstructed tables

### Table 1 — Attack feasibility ratings and descriptions

**Clause:** 15.7.2  
**Source anchor:** iso21434_layout.txt lines 2826–2833  
**Confidence:** `high`

| Attack feasibility rating | Description |
|---|---|
| High | The attack path can be accomplished utilizing low effort. |
| Medium | The attack path can be accomplished utilizing medium effort. |
| Low | The attack path can be accomplished utilizing high effort. |
| Very low | The attack path can be accomplished utilizing very high effort. |

### Table E.1 — Example CAL determination based on impact and attack vector

**Clause:** Annex E  
**Source anchor:** iso21434_layout.txt lines 3392–3401; PDF physical page 65 / printed page 59  
**Confidence:** `high`

| Impact rating | Physical | Local | Adjacent | Network |
|---|---|---|---|---|
| Severe | CAL2 | CAL3 | CAL4 | CAL4 |
| Major | CAL1 | CAL2 | CAL3 | CAL4 |
| Moderate | CAL1 | CAL1 | CAL2 | CAL3 |
| Negligible | --- | --- | --- | --- |

> **Notes:** The `---` values are explicitly defined by footnote a and are not missing numeric cells.

### Table E.2 — Example CALs and expected rigour in cybersecurity assurance measures

**Clause:** Annex E  
**Source anchor:** iso21434_layout.txt lines 3435–3457  
**Confidence:** `medium`

| CAL | Assurance description | Confidence that activities are rigorous | Confidence that vulnerabilities do not remain | Independence scheme |
|---|---|---|---|---|
| CAL1 | Low to moderate cybersecurity assurance is required | Requirement-based testing | Analysis and/or testing based on known information | Not needed |
| CAL2 | Moderate cybersecurity assurance is required | Requirement-based testing | Analysis and/or testing based on known information | Assessment by a different person than the originator |
| CAL3 | Moderate to high cybersecurity assurance is required | All interactions between components are tested | Exploratory analysis and/or testing | Assessment by a person in a different team |
| CAL4 | High cybersecurity assurance is required | All combinations of interactions between components are tested | Exploratory analysis and/or testing | Independent regarding management, resources and release authority |

> **Manual review:** The source table uses merged／multi-line cells; verify the full CAL2–CAL4 text against the original page before normative use.

### Table E.3 — Example level of independence of cybersecurity activities

**Clause:** Annex E  
**Source anchor:** iso21434_layout.txt lines 3493–3511  
**Confidence:** `high`

| Activity | Requirement reference | CAL1 | CAL2 | CAL3 | CAL4 |
|---|---|---|---|---|---|
| Verification of cybersecurity concept and design activities | [RQ-09-11]; [RQ-10-08] | I1 | I1 | I2 | I2 |
| Verification of implementation and integration of components | [RQ-10-09] | I1 | I1 | I2 | I2 |
| Cybersecurity validation | [RQ-11-01] | I1 | I1 | I2 | I2 |
| Cybersecurity assessment | [RQ-06-27] | — | I1 | I2 | I3 |

> **Notes:** I1, I2 and I3 are defined by the table footnotes; the dash means no suggestion regarding independence.

### Table E.4 — Example parameters of testing methods

**Clause:** Annex E  
**Source anchor:** iso21434_layout.txt lines 3527–3550  
**Confidence:** `high`

| Activity | Requirement reference | CAL1 | CAL2 | CAL3 | CAL4 |
|---|---|---|---|---|---|
| Functional testing | [RC-10-12]; [RQ-11-01] | T1 | T1 | T2 | T2 |
| Vulnerability scanning | [RC-10-12]; [RQ-11-01] | T1 | T1 | T1 | T1 |
| Fuzz testing | [RC-10-12]; [RQ-11-01] | — | T1 | T2 | T2 |
| Penetration testing | [RC-10-12]; [RQ-11-01] | — | — | T1 | T2 |

> **Notes:** T1／T2 are parameter sets, not pass／fail results.

### Table H.8 — Risk matrix example

**Clause:** Annex H, H.2.7  
**Source anchor:** iso21434_layout.txt lines 4369–4376; printed page 77; physical page to be resolved by anchor  
**Confidence:** `high`

| Impact rating | Very Low | Low | Medium | High |
|---|---|---|---|---|
| Severe | 2 | 3 | 4 | 5 |
| Major | 1 | 2 | 3 | 4 |
| Moderate | 1 | 2 | 2 | 3 |
| Negligible | 1 | 1 | 1 | 1 |

### Table H.9 — Examples of determined risk values

**Clause:** Annex H, H.2.7  
**Source anchor:** iso21434_layout.txt lines 4378–4387  
**Confidence:** `high`

| Threat scenario | Aggregated attack feasibility rating | Impact rating | Risk value |
|---|---|---|---|
| Spoofing of a signal leads to loss of integrity of the data communication of “Lamp Request” signal for power switch actuator ECU | High | Severe | S: 5 |
| Denial of service of oncoming car information | Low | Moderate | O: 2 |

### Table H.10 — Example translation of impact and attack feasibility to numerical values

**Clause:** Annex H, H.2.7  
**Source anchor:** iso21434_layout.txt lines 4394–4403  
**Confidence:** `high`

| Rating type | Rating | Numerical value |
|---|---|---|
| Impact | Negligible | 0 |
| Impact | Moderate | 1 |
| Impact | Major | 1.5 |
| Impact | Severe | 2 |
| Attack feasibility | Very low | 0 |
| Attack feasibility | Low | 1 |
| Attack feasibility | Medium | 1.5 |
| Attack feasibility | High | 2 |

> **Notes:** The source formula is R = 1 + I × F.

### Table H.11 — Example results of risk treatment decision

**Clause:** Annex H, H.2.8  
**Source anchor:** iso21434_layout.txt lines 4409–4414  
**Confidence:** `high`

| Threat scenario | Risk value | Risk treatment option |
|---|---|---|
| Spoofing of a signal leads to loss of integrity of the data communication of “Lamp Request” signal for power switch actuator ECU | S: 5 | Reducing the risk |
| Denial of service of oncoming car information | O: 2 | Reducing the risk |
