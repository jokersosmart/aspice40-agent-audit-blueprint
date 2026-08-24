# ASPICE 4.0 × SSD Controller Agent Architecture

## 1. 建議結論

建議保留 **90 個邏輯 Agent 角色**，但實際部署約 **18 個共用 Runtime**，另保留 1 個 Human Review／Approval Gateway。90 個角色是 ASPICE、ISO 26262-5 與 ISO/SAE 21434 的稽核責任與輸出邊界數量；Runtime 是實際運算與維護單位。這個區分很重要，因為如果只建立一個混合規範 chatbot，系統無法穩定追蹤 32 個 ASPICE Process、15 個 ISO 26262-5 Safety role 與 15 個 ISO/SAE 21434 Cybersecurity role；如果真的建立 90 個完全獨立服務，則容易出現 Prompt 漂移、規則重複、版本不一致與維運成本過高。

| 層級 | 邏輯角色 | 第一版部署方式 | 目的 |
|---|---:|---|---|
| ASPICE 規範／證據控制 | 8 | 共用控制 Runtime | 固定 ASPICE 規範、Evidence、Information Item、Scope、追溯與報告規則 |
| ASPICE Process 稽核 | 32 | 1 個 Process Audit Runtime + 32 個 Rule Pack | 以 ASPICE Process ID 作為最小可稽核單位 |
| ASPICE／組織 Manager | 14 | Manager Coordination Runtime + 14 個 profile | 將稽核結果轉成責任、接口、action、資源與重新驗證 |
| ISO 26262-5 Safety／Hardware | 15 | R11–R14 + 15 個 profile | 硬體安全需求、設計、安全分析、指標、PMHF／EEC、驗證與引用 |
| ISO 26262 Safety Manager | 3 | Functional Safety Coordination Runtime | Functional Safety、Hardware Safety Assurance、Safety Verification／Confirmation |
| ISO/SAE 21434 Cybersecurity | 15 | R15–R18 + 15 個 profile | Cybersecurity governance、TARA、Concept、漏洞、驗證、營運與 Cybersecurity Case |
| ISO/SAE 21434 Cybersecurity Manager | 3 | Cybersecurity Coordination Runtime | Cybersecurity Governance、Product Cybersecurity Assurance、Operations／Assurance |
| 人工控制 | 不計入 LLM Agent | 1 個 Human Review／Approval Gateway | 由 Process Owner、Verification Owner、QA、Safety／Cybersecurity Reviewer 與 Lead Assessor 做最後確認 |
| **總計** | **90** | **約 18 個 Runtime + 1 個人工 Gateway** | 兼顧稽核粒度、跨規範邊界與可維護性 |

## 2. Cognitive Operating Layer

所有 90 個邏輯 Agent 都載入同一個 `prompts/05_cognitive_operating_layer.md`，再由 `config/agent_cognitive_assignments.json` 指定角色應啟用的模組。這些模組是非規範性的工程協作能力，不是 ASPICE 4.0 requirement，且永遠低於核准的 PAM 原文、客戶／OEM 要求、公司規則、Evidence Object、assessment scope 與人工核准。

它們提供十類標準行為：問題定義與 Scope、證據／來源與量化完整性、假說／模型與受控驗證、決策／優先級與最佳化、反方／偏誤與一致性、利害關係人／介面與溝通、系統與多層因果、學習／重用與知識連續性、責任／倫理與權限、可逆試驗／停損與升級。這些能力會影響 Agent 的提問順序、證據檢查、選項比較、工作包拆解與人工佇列分流，但不會改寫規範原文。

所有 ASPICE、ISO 26262-5 與 ISO/SAE 21434 normative finding 仍必須直接攜帶 `spec_citations`，包含完整原文段落／完整表格列、定位、原文 hash、適用原因、解讀與人工確認狀態。Cognitive Layer 不可代替 direct citation，也不可用通用推理直接產生 PAM 結論。

## 3. 8 個規範／證據控制角色

| ID | 角色 | 必要輸入 | 主要輸出 | 不可越權 |
|---|---|---|---|---|
| C01 | Spec Text Integrity & Ingestion | 原始 PDF、版本、來源 URL、抽取工具 | Text Integrity Certificate、頁面 manifest、文字／圖表異常 | 不得改寫規範原文；OCR 修復要留原文與人工確認 |
| C02 | ASPICE Knowledge Librarian | PAM／PRM、semantic chunks、版本差異 | 章節索引、術語、purpose／outcome／BP／GP／PA／II 關聯 | 不得把公司慣例寫成 PAM 強制要求 |
| C03 | Evidence Ingestion & Normalization | ALM、Git／Perforce、PLM、CI、test、simulation、lab、tape-out | Evidence Object、revision、baseline、owner、review 狀態 | 不得因檔名相似判定證據滿足要求 |
| C04 | Information Item & Work Product Dictionary | Annex B、文件目錄、工具 metadata | II／IIC 字典、證據特性、synonym、artifact type | 不得把 Information Item 當成固定檔名 |
| C05 | Scope, Tailoring & N/A Gate | assessment context、客戶範圍、產品邊界、組織責任 | in／out／conditional／not-in-scope matrix、rationale | 不得用「找不到文件」作為 N/A 理由 |
| C06 | Traceability & Consistency Graph | 需求、架構、實作、驗證、release、change | 雙向追溯、斷鏈、衝突、影響分析 | 不得只因 link 存在就宣稱內容一致 |
| C07 | Capability & Rating Preparation | Process findings、PA evidence、scope | PA evidence pack、N／P／L／F 前置建議 | 不得做正式 rating、選定 assessment method 或宣布 Level |
| C08 | Audit Orchestrator & Report | 所有結果、衝突、scope、baseline | audit plan、finding register、evidence index、rehearsal report | 不得刪除 conflict／unknown 或用平均數掩蓋重大缺口 |

## 4. 32 個 Process Agent

ASPICE 4.0 Chapter 4 的最小稽核單位是 Process ID。每個 Process Agent 使用相同的 Prompt Contract，只載入不同的 Process Rule Pack。Rule Pack 必須包含：purpose、outcomes、BP、expected Information Items、PA dependencies、upstream／downstream、適用的 SSD evidence domains、Manager routing、known interpretation 與 human gates。

| Process Group | Process IDs | SSD Controller 主要關注 |
|---|---|---|
| ACQ | ACQ.4 | 外部 IP、EDA、NAND、PHY、supplier monitoring、承諾與偏差 |
| SPL | SPL.2 | firmware／hardware／silicon release、release package、approval、delivery |
| SYS | SYS.1–SYS.5 | stakeholder requirements、system requirements、architecture、integration、system verification |
| SWE | SWE.1–SWE.6 | firmware requirements、architecture、detailed design、unit／component／final verification |
| VAL | VAL.1 | intended use、target environment、validation measures、validation results |
| MLE | MLE.1–MLE.4 | 只有產品含 ML 時啟用；否則由 C05 形成 scope rationale |
| HWE | HWE.1–HWE.4 | hardware requirements、digital／analog design、simulation、tape-out、silicon verification |
| SUP | SUP.1、SUP.8、SUP.9、SUP.10、SUP.11 | QA、configuration、problem、change、ML data management |
| MAN | MAN.3、MAN.5、MAN.6 | project、risk、measurement |
| PIM | PIM.3 | process improvement、effectiveness、lessons learned |
| REU | REU.2 | IP／設計／軟體 reuse、qualification、portability、constraints |

## 5. 20 個 Manager Agent

| ID | Manager | 責任範圍 | 主要 Process |
|---|---|---|---|
| M01 | System Engineering | 系統需求、架構、介面、行為、變更影響 | SYS.1–SYS.3；交叉 SYS.4–SYS.5、VAL.1 |
| M02 | Firmware／Software Engineering | firmware requirements、architecture、detailed design、implementation、release readiness | SWE.1–SWE.6 |
| M03 | Hardware Engineering | 硬體需求、架構、設計、production data、design decision | HWE.1–HWE.4 |
| M04 | Digital Hardware | RTL、micro-architecture、CDC、reset、power-domain、netlist | HWE.1–HWE.4、SYS.3／SYS.4 |
| M05 | Analog／Mixed-Signal | electrical requirements、schematic、layout、PVT／corner、characterization | HWE.1–HWE.4、VAL.1 |
| M06 | Simulation／Emulation | RTL simulation、formal、FPGA／emulation、logs、coverage、regression | HWE.3／HWE.4、SYS.4／SYS.5、SWE.4–SWE.6 |
| M07 | Tape-out／Silicon | design freeze、sign-off、mask／production data、bring-up、silicon characterization | HWE.2–HWE.4、SUP.8–SUP.10、SPL.2 |
| M08 | System Verification & Validation | system integration、system verification、target environment validation | SYS.4、SYS.5、VAL.1 |
| M09 | Firmware Verification | unit、component／integration、final software verification、static analysis、regression | SWE.4–SWE.6 |
| M10 | Hardware Verification | design／requirements verification、simulation、measurement、analysis、silicon evidence | HWE.3、HWE.4、SYS.4／SYS.5、VAL.1 |
| M11 | QA & Process Improvement | independent QA、process compliance、nonconformance、improvement、internal assessment | SUP.1、PIM.3 |
| M12 | Configuration／Change／Problem | configuration item、baseline、change impact、problem root cause、closure | SUP.8–SUP.10 |
| M13 | Project／Risk／Measurement | scope、schedule、resource、risk、metrics、status、quantitative control | MAN.3、MAN.5、MAN.6 |
| M14 | Supplier／Release／Reuse | supplier monitoring、external IP／EDA／NAND／PHY、release、reuse qualification | ACQ.4、SPL.2、REU.2 |
| M15 | Functional Safety | functional safety lifecycle、safety plan、ASIL context、safety case、residual-risk governance | ISO 26262-5；交叉 SYS／HWE／SUP／MAN |
| M16 | Hardware Safety Assurance | HSR／HSI、safety mechanisms、safety analysis、SPFM／LFM、PMHF／EEC、qualification | ISO 26262-5；HWE.1–HWE.4、SUP.8–SUP.10 |
| M17 | Safety Verification／Confirmation | independent safety verification、confirmation measures、anomaly disposition、re-verification、safety release evidence | ISO 26262-5；HWE.3–HWE.4、SYS.4–SYS.5、VAL.1 |
| M18 | Cybersecurity Governance | policy、cybersecurity plan、roles、resources、customer／supplier responsibility、security culture | ISO/SAE 21434 Clauses 5–7；ACQ.4、SPL.2、SUP.1、SUP.8、SUP.10 | 
| M19 | Product Cybersecurity Assurance | item definition、TARA、goals、concept、requirements、architecture、implementation、validation | ISO/SAE 21434 Clauses 9–11；SYS、SWE、HWE、VAL | 
| M20 | Cybersecurity Operations／Assurance | monitoring、vulnerability、incident、production、updates、support lifecycle、Cybersecurity Case、assessment readiness | ISO/SAE 21434 Clauses 8、12–14；SUP.9、SUP.10、MAN.6 |

> Digital、Analog／Mixed-Signal、Simulation／Emulation、Tape-out／Silicon 是 SSD Controller 的責任分流，不是 ASPICE 新 Process。所有結果仍必須回接 HWE、SYS、VAL、SUP、MAN 或 SPL 的正式 Process。

## 6. 驗證獨立性

每一筆重要證據至少需要三個責任位置：產出 owner、independent verification owner、QA／authorized reviewer。Agent 可以檢查三者是否被指定、是否有利益衝突、是否有 review／approval 與重新驗證，但不能自己替技術專家簽核技術正確性。

| 證據 | 產出 owner | 獨立驗證 | QA／最終 reviewer |
|---|---|---|---|
| System architecture | System Engineering | System V&V 或指定 architecture reviewer | QA／Lead Assessor |
| Firmware detailed design | Firmware | Firmware Verification | QA／Process Owner |
| Digital RTL／design | Digital Hardware | Hardware Verification／Simulation | QA／Hardware Manager |
| Analog／mixed-signal design | Analog／Mixed-Signal | Hardware Verification／Silicon characterization | QA／Hardware Manager |
| Tape-out／silicon data | Tape-out／Silicon | Hardware Verification | QA、Project／Release authority |
| Product release package | Release Manager | QA／independent release approval | Project／customer interface |

## 7. 建置順序

第一階段先建立 C01、C02、C03、C04、C05、C06、C08，以及 SYS／SWE／HWE／VAL、SUP.8、SUP.9、SUP.10 的 Process Rule Pack。第二階段導入 M01–M10，將系統、韌體、硬體、驗證、simulation、tape-out／silicon 的責任接到同一張 Evidence Graph。第三階段導入 M11–M17、C07、MAN、PIM、ACQ、SPL、REU，形成完整的 ASPICE 與功能安全閉環。第四階段導入 CS01–CS15、M18–M20、R15–R18，建立 TARA、Cybersecurity Concept、vulnerability、incident、security update 與 Cybersecurity Case 閉環。MLE.1–MLE.4 與 SUP.11 則依產品 Scope 條件式啟用。

## 8. ISO 26262-5 Safety Extension

For an SSD Controller used in a road-vehicle E/E system, the Blueprint adds 15 logical ISO 26262-5 Safety／Hardware roles: FS01–FS11 for clause-focused activities, FS12 for licensed-source citation and evidence, FS13 for cross-standard traceability, FS14 for safety assessment orchestration, and FS15 for independent verification and confirmation evidence. It also adds M15 Functional Safety Manager, M16 Hardware Safety Assurance Manager and M17 Safety Verification and Confirmation Manager.

The ISO extension is deployed through four additional Safety runtimes: R11 Clause Audit, R12 Quantitative Safety Analysis, R13 Functional Safety Evidence and Cross-Standard, and R14 Functional Safety Coordination. R10 remains the Human Review and Approval Gateway. These runtimes are not substitutes for ASPICE Process Agents; they operate on a separate normative layer and create explicit interfaces to SYS, HWE, SWE, VAL, SUP and MAN evidence.

The ISO 26262-5 clause boundary in the provided source is Clauses 1–10 plus Annex A–H. The provided Part 5 does not contain an independent Clause 11. Production, operation, service and decommissioning content is handled through Clause 7.4.5 and related work products. Agents must not invent a Clause 11 or silently treat a missing dependency Part as satisfied.

The public repository contains metadata, profiles, schemas and a runtime citation generator, but not the licensed ISO source PDF or a full quotation catalog. FS12 must load the authorized local source at runtime and inject the complete approved paragraph or table row into `spec_citations`. Missing ISO 26262-2, -4, -8, -9 or -11 content becomes `dependency_missing` when a conclusion depends on it.

## 9. ISO/SAE 21434 Cybersecurity Extension

For an SSD Controller used in a road-vehicle E/E system, the Blueprint adds 15 logical ISO/SAE 21434 Cybersecurity roles: CS01–CS04 for scope, governance, project and distributed responsibility; CS05–CS06 for continual monitoring and vulnerability management; CS07–CS08 for item definition, TARA, cybersecurity goals and concept; CS09–CS10 for cybersecurity requirements, architecture, implementation and integration; CS11 for cybersecurity validation; CS12–CS14 for production, operations, incident response, updates, end of support and decommissioning; and CS15 for Cybersecurity Case, audit, assessment readiness and evidence integrity. It also adds M18 Cybersecurity Governance, M19 Product Cybersecurity Assurance and M20 Cybersecurity Operations／Assurance.

The ISO/SAE 21434 extension is deployed through R15 Clause and Governance Audit, R16 TARA and Product Development, R17 Continual Security Operations and R18 Cybersecurity Coordination and Assurance. These runtimes operate on a separate cybersecurity normative layer and create explicit interfaces to SYS, SWE, HWE, VAL, SUP, MAN, FS and the existing Human Review／Approval Gateway.

The provided ISO/SAE 21434:2021(E) source covers Clauses 1–15 and Annex A–H. Clause 2 identifies ISO 26262-3:2018 as a normative reference. If a finding depends on missing vehicle context, missing customer／supplier responsibility, missing dependency Parts, missing TARA input or missing approved source text, the Agent must emit `dependency_missing`, `citation_missing` or `unknown`; it must not claim compliance from memory or from a secondary summary.

The public repository stores only cybersecurity metadata, Scope, profiles, Prompt templates, schemas, examples and the runtime citation generator. It does not store the licensed ISO/SAE 21434 source or a full runtime quotation catalog. At execution time, the Agent loads the approved local source and injects the complete authorized paragraph or table row into `spec_citations` with its source and quotation hash.

## 10. 最重要的設計原則

Agent 的輸出不是「通過／不通過」聊天答案，而是可重現的 Evidence-based finding。每筆 finding 必須有規範來源、**直接複製的完整 ASPICE、ISO 26262-5 或 ISO/SAE 21434 原文段落／完整表格列**、原文 SHA-256、段落意義、適用原因、證據來源、版本／baseline、狀態、理由、缺口、owner、verification owner、推薦 action、信心與人工確認旗標。只留下 reference link、Process ID、BP ID 或頁碼是不合格的輸出。找不到資料要輸出 `unknown`；找不到核准原文要輸出 `citation_missing`，而不是猜測 `gap` 或 `satisfied`。

Manager Agent 若將 finding 轉成工作包，也必須攜帶原始 `spec_citations`，不能把規範原文壓縮成只剩一個 BP 編號。每次執行要記錄 Prompt、Rule Pack、citation catalog、scope 與 evidence snapshot 的版本，讓人員可以重新取得同一段原文並比對 hash。
