# ASPICE 4.0 × ISO 26262-5 × ISO/SAE 21434 Agent Audit Blueprint

這份 Blueprint 是給 SSD Controller 汽車產品開發與稽核使用的規範驅動 Agent 資產包。它將 ASPICE 4.0、ISO 26262-5:2018 硬體功能安全與 ISO/SAE 21434:2021 Automotive Cybersecurity 分成三個規範層，再透過 Evidence Object、Traceability、Change、Verification、Supplier、Release 與 Human Review Gateway 連接。三套規範可以共享事實證據，但任何一套規範的 evidence 都不能自動宣稱滿足另一套規範。

## 建議數量

| 類別 | 邏輯角色 | 實作方式 |
|---|---:|---|
| ASPICE 規範／證據控制 | 8 | C01–C08，使用共用控制 Runtime，固定 Scope、Evidence、追溯、能力評等與報告規則 |
| ASPICE Process 稽核 | 32 | 一個 Process Audit Runtime 載入 32 份 Process Rule Pack，執行時可平行派工 |
| ASPICE／組織／功能安全 Manager | 20 | Manager Coordination、Functional Safety Coordination 與 Cybersecurity Coordination Runtime 載入 M01–M20 |
| ISO 26262-5 Safety／Hardware | 15 | FS01–FS15，使用 R11–R14，聚焦硬體安全需求、設計、分析、指標、PMHF／EEC、驗證與 Safety Case |
| ISO/SAE 21434 Cybersecurity | 15 | CS01–CS15，使用 R15–R18，聚焦治理、TARA、Cybersecurity Concept、漏洞、驗證、營運與 Cybersecurity Case |
| ISO/SAE 21434 Cybersecurity Manager | 3 | M18–M20，分別負責 Governance、Product Cybersecurity Assurance、Operations／Assurance |
| **邏輯角色合計** | **90** | 90 個可追蹤責任角色，不等於 90 個獨立服務 |

## Runtime 設計

實際部署採共用 Runtime，而不是為每個邏輯角色建立獨立服務。既有 ASPICE 與 ISO 26262-5 共有 R01–R14；ISO/SAE 21434 新增 R15 Clause／Governance Audit、R16 TARA／Product Development、R17 Continual Security Operations、R18 Cybersecurity Coordination and Assurance。R10 保留為 Human Review／Approval Gateway，不屬於 LLM Agent。

## 使用順序

第一期先完成三套規範的受控來源登錄、Evidence Object、Scope、Traceability、direct citation contract 與 Human Review Gateway。第二期啟用 ASPICE 的系統、韌體、硬體、驗證 Process Agent，以及 ISO 26262-5 的硬體安全 Agent。第三期啟用 ISO/SAE 21434 的 CS01–CS15 與 M18–M20，導入 TARA、Cybersecurity Concept、vulnerability management、incident response、security update 與 Cybersecurity Case。若某個產品不屬於汽車量產 E/E 系統或客戶沒有要求該規範，仍須由受權責人員建立有依據的 out-of-scope／not-in-scope rationale，不可靜默忽略。

## 重要使用原則

> Agent 可以做自評、證據整理、缺口辨識、追溯檢查、變更影響分析、TARA／安全分析整理與 assessment rehearsal；Agent 不可以取代 Lead Assessor、Functional Safety Manager、Cybersecurity Manager 或 QA 進行 Scope、正式 rating、風險接受、重大 finding closure、Cybersecurity Case 核准或對外合規宣稱。

所有 Agent 輸出都必須帶有 `source_anchor`、`spec_citations`、`evidence_refs`、`status`、`human_confirmation_required` 與規則版本。`spec_citations` 必須直接包含適用規範的完整原文段落／完整表格列、段落定位、原文 SHA-256、適用原因與解讀；只提供 reference link、Process ID、Clause ID、RQ／RC／PM／WP ID 或頁碼都不算合格。若找不到證據、核准原文或相依規範，分別輸出 `unknown`、`citation_missing` 或 `dependency_missing`，不能因為文件名稱相似就輸出 `satisfied`。

## 目錄

- `docs/agent_architecture.md`：三規範總體架構、責任、流程與建置順序。
- `docs/iso26262_part5_agent_architecture.md`：ISO 26262-5 的 Safety role、M15–M17、Runtime、ASPICE interface 與 Safety Gate。
- `docs/iso21434_agent_architecture.md`：ISO/SAE 21434 的 CS01–CS15、M18–M20、TARA、Cybersecurity Case 與 Security Gate。
- `docs/iso21434_integration_report.md`：ISO/SAE 21434 與 ASPICE／ISO 26262-5 的整合、Evidence、Runtime 與人工 Gate。
- `docs/prompt_composition.md`：Global Policy、Cognitive Layer、standard profile、Rule Pack、Scope、Evidence 與 citation 的組裝順序。
- `prompts/00_global_policy.md`：所有 Agent 共用的安全、證據與規範優先政策。
- `prompts/05_cognitive_operating_layer.md`：所有 Agent 共用的中性化工程分析行為，不屬於任何規範 requirement。
- `prompts/10_process_auditor_template.md`：32 個 ASPICE Process Agent 共用 Prompt。
- `prompts/20_manager_template.md`：M01–M20 Manager Agent 共用 Prompt。
- `prompts/30_control_agents_template.md`：C01–C08 控制 Agent Prompt 邊界。
- `prompts/40_iso26262_safety_auditor_template.md`、`prompts/41_iso26262_safety_manager_template.md`：ISO 26262-5 Prompt。
- `prompts/42_iso21434_cybersecurity_auditor_template.md`、`prompts/43_iso21434_cybersecurity_manager_template.md`：ISO/SAE 21434 Prompt。
- `knowledge/cognitive/cognitive_modules.yaml`：10 個可部署的分析與協作模組，以及 76 個中性能力索引。
- `config/agent_cognitive_assignments.json`：90 個邏輯角色的 Cognitive module 配置、強調事項與人工 Gate。
- `profiles/process_agents.yaml`：32 個 ASPICE Process profile 與 manager routing。
- `profiles/manager_agents.yaml`：M01–M20 Manager profile、輸入與輸出責任。
- `profiles/iso26262_safety_agents.yaml`：FS01–FS15 的 ISO 26262-5 Safety／Hardware profile。
- `profiles/iso21434_cybersecurity_agents.yaml`：CS01–CS15 的 ISO/SAE 21434 Cybersecurity profile。
- `knowledge/aspice40/process_rules/`：32 份 ASPICE Process Rule Pack，每份含 direct spec citations。
- `knowledge/aspice40/spec_citation_catalog.*`：ASPICE 4.0 direct citation catalog；規範原文限受控來源使用。
- `knowledge/iso26262/`：ISO 26262-5 的 runtime-only source policy 與 Rule Pack template。
- `knowledge/iso21434/`：ISO/SAE 21434 的 runtime-only source policy 與 Rule Pack template。
- `schemas/`：Evidence、Direct Citation、Audit Finding、Safety Finding、Cybersecurity Finding、Cybersecurity Case、Cross-Standard Mapping 與三規範 Mapping 契約。
- `config/standards_registry.yaml`：三套規範的版本、優先級、dependency 與來源限制。
- `config/process_scope.yaml`、`config/iso26262_part5_scope.yaml`、`config/iso21434_scope.yaml`：各規範 Scope、tailoring 與 dependency 設定。
- `config/runtime_registry.yaml`：R01–R18 Runtime 與 Human Review Gateway 的部署映射。
- `workflows/audit_workflow.md`：三規範從來源入庫、證據整理到人工 Gate 的稽核流程。
- `docs/cognitive_operating_layer_guide.md`、`docs/cognitive_integration_report.md`：Cognitive Layer 的採用、分配、優先級與驗證。
- `docs/direct_spec_citation_policy.md`：逐項完整原文引用政策與 public repository 邊界。
- `docs/external_references.md`：VDA QMC、intacs 與 DNV 的外部背景來源；normative 結論仍以核准標準原文為準。
- `examples/`：HWE.2、ISO 26262-5 與 ISO/SAE 21434 SSD Controller 稽核輸入及三規範 Crosswalk 範例。

## ISO 26262-5 Safety Extension

ISO 26262-5:2018 的擴充包含 FS01–FS15、M15–M17、R11–R14、Safety Finding schema、Cross-Standard Mapping schema、Safety Auditor／Manager Prompt，以及 runtime citation generator。完整 ISO 26262 標準全文不放入 public repository；FS12 在 runtime 從核准本地來源注入完整原文段落或表格列，缺少 ISO 26262-2／-4／-8／-9／-11 等依賴時必須保留 `dependency_missing`。

## ISO/SAE 21434 Cybersecurity Extension

ISO/SAE 21434:2021 的擴充包含 CS01–CS15、M18–M20、R15–R18、Cybersecurity Finding schema、Cybersecurity Case schema、三規範 Cross-Standard Mapping schema、Cybersecurity Auditor／Manager Prompt，以及 runtime citation generator。提供的 88 頁文件涵蓋 Clauses 1–15 與 Annex A–H；public repository 只存 metadata、Scope、profile、Prompt、schema、範例與 generator，不存完整授權標準全文。CS07／CS08 負責 TARA、Cybersecurity Goals 與 Concept；CS09／CS10 負責 requirements、architecture、implementation 與 integration；CS05／CS06／CS13／CS14 負責持續監控、漏洞、事件、更新、支援結束與除役；CS15 負責 Cybersecurity Case、audit／assessment 與證據完整性。

## 版本控制要求

所有 Prompt、Rule Pack、Process profile、Manager profile、Safety／Cybersecurity profile、schema、Scope 設定、runtime registry 與報告模板都應納入 Configuration Management。每一份 audit run 都要記錄其 Git commit／baseline、規範版本、runtime source hash、citation hash、Evidence baseline 與人工決策，否則日後無法重現同一份稽核結論。
