# ASPICE 4.0 × SSD Controller Agent Blueprint

這份 Blueprint 不是把 54 個角色做成 54 個彼此獨立、各自維護上下文的聊天機器人，而是採用「**54 個可追蹤的邏輯角色、10 個共用 Runtime、版本化 Rule Pack 與固定資料契約**」的架構。這樣可以同時滿足 ASPICE 4.0 的 Process-level 稽核粒度，以及 SSD Controller 產品在系統、韌體、數位硬體、類比／混合訊號、simulation／emulation、tape-out／silicon 和驗證之間的實際責任邊界。

## 建議數量

| 類別 | 邏輯角色 | 實作方式 |
|---|---:|---|
| 規範／證據控制 | 8 | 其中 C03／C04 可共用 Evidence Runtime；其餘各自維持責任邊界 |
| ASPICE Process 稽核 | 32 | 一個 Process Audit Runtime 載入 32 份 Process rule pack，執行時可平行派工 |
| 部門／治理 Manager | 14 | 一個 Manager Coordination Runtime 載入 14 份 manager profile |
| **合計** | **54** | 54 個邏輯角色，不等於 54 個獨立部署服務 |

## 10 個建議 Runtime

1. C01 Spec Text Integrity & Ingestion Runtime。
2. C02 ASPICE Knowledge Librarian Runtime。
3. C03／C04 Evidence Ingestion & Information Item Dictionary Runtime。
4. C05 Scope, Tailoring & N/A Gate Runtime。
5. C06 Traceability & Consistency Graph Runtime。
6. Process Audit Runtime，載入 32 個 Process rule pack。
7. C07 Capability & Rating Preparation Runtime。
8. C08 Audit Orchestrator & Report Runtime。
9. Manager Coordination Runtime，載入 14 個部門／治理 profile。
10. Human Review／Approval Gateway；這是控制與簽核介面，不應讓 LLM 自行關閉重大 finding。

## 使用順序

第一期先完成規範入庫、證據標準化、Scope、追溯與 28 個非 MLE Process 的 rule pack。第二期導入系統、韌體、硬體與驗證的跨領域稽核。第三期再將 14 個 Manager profile 與能力等級準備納入。若產品沒有 Machine Learning，MLE.1–MLE.4 與 SUP.11 應由 C05 產生有依據的 out-of-scope／not-in-scope rationale，不應被靜默忽略。

## 重要使用原則

> Agent 可以做自評、證據整理、缺口辨識、追溯檢查、變更影響分析與稽核 rehearsal；Agent 不可以取代 Lead Assessor 進行 assessment scope、N/A 最終合理性、正式 N/P/L/F rating、重大 finding closure 或對外宣稱通過 ASPICE 的決策。

所有 Agent 輸出都必須帶有 `source_anchor`、`spec_citations`、`evidence_refs`、`status`、`confidence`、`human_confirmation_required` 與規則版本。`spec_citations` 必須直接包含 ASPICE 4.0 的完整原文段落／完整表格列、段落定位、原文 SHA-256、適用原因與解讀；只提供 reference link、Process ID、BP ID 或頁碼都不算合格。若找不到證據或找不到核准原文，分別輸出 `unknown` 或 `citation_missing`，不能因為文件名稱相似就輸出 `satisfied`。

## 目錄

- `docs/agent_architecture.md`：完整架構、職責、流程與建置順序。
- `prompts/00_global_policy.md`：所有 Agent 共用的安全與證據政策。
- `prompts/10_process_auditor_template.md`：32 個 Process Agent 共用 Prompt。
- `prompts/20_manager_template.md`：14 個 Manager Agent 共用 Prompt。
- `prompts/30_control_agents_template.md`：C01–C08 控制 Agent Prompt 邊界。
- `prompts/05_cognitive_operating_layer.md`：所有 Agent 共用的中性化 Cognitive Operating Layer，不屬於 ASPICE requirement。
- `knowledge/cognitive/cognitive_modules.yaml`：10 個可部署的分析與協作模組，以及 76 個中性能力索引。
- `config/agent_cognitive_assignments.json`：54 個邏輯 Agent 的模組配置、強調事項與人工 Gate。
- `profiles/process_agents.yaml`：32 個 Process profile 與 manager routing。
- `profiles/manager_agents.yaml`：14 個 Manager profile、輸入與輸出責任。
- `knowledge/aspice40/spec_citation_catalog.jsonl`：直接引用 catalog，每筆包含完整原文與 SHA-256。
- `knowledge/aspice40/spec_citation_catalog.md`：供人工閱讀的原文引用庫。
- `knowledge/aspice40/process_rules/`：32 份逐 Process rule pack，每份含 purpose、outcomes、BP 與 direct spec citations。
- `schemas/`：Evidence Object、Direct Spec Citation、Audit Finding、Process Audit Result 等固定資料契約。
- `config/process_scope.yaml`：Assessment scope、MLE conditional scope 與公司 tailoring 的設定入口。
- `workflows/audit_workflow.md`：從規範入庫到稽核 rehearsal 的工作流程，含 Cognitive Layer 介入點。
- `docs/cognitive_operating_layer_guide.md`：Cognitive Layer 的採用、優先順序、模組分配與維護方式。
- `examples/`：HWE.2 等 SSD Controller 情境的範例，包含 `hwe2_audit_result_with_citations.json` 的完整原文引用輸出。
- `docs/direct_spec_citation_policy.md`：逐項原文引用政策、缺引用處理與版權／人工 Gate 邊界。

## 版本控制要求

所有 Prompt、Rule Pack、Process profile、Manager profile、schema、scope 設定與報告模板都應納入 Configuration Management。每一份 audit run 都要記錄它們的 Git commit／baseline，否則日後無法重現同一份稽核結論。
