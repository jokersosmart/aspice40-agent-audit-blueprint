# Shared Runtime 執行 SOP

## 1. 目的

本 SOP 定義 90 個邏輯 Agent 如何透過共用 Runtime 執行，避免每次呼叫載入整套規範、全部角色與所有證據，同時確保 ASPICE 4.0、ISO 26262-5 與 ISO/SAE 21434 的直接原文引用完整、版本正確、可追溯、可重現。

## 2. 一次任務只選一個 active role

Orchestrator 先建立 `run_id`、`task_id` 與 `parent_task_id`，再依 `agent_id` 查出一個角色 profile。例如 `HWE.2` 由 R06 執行、FS09 由 R12 執行、CS07 由 R16 執行。不能把所有 90 個 profile 放入同一個 Prompt。跨規範任務先拆成各標準的 child task，再由 R05／R13 或 R18 以 mapping 結果合併。

## 3. Context 組裝順序

1. 載入 `prompts/00_global_policy.md` 與 `prompts/05_cognitive_operating_layer.md`。
2. 載入一個 active role 的 profile 與 Cognitive assignment。
3. 載入 project Scope、tailoring、release／baseline、dependency snapshot。
4. 載入一個目標 Process 或 Clause 的 Rule Pack。
5. 由 Citation Service 依 exact anchor／provision／table row 取回完整核准原文。
6. 由 Deterministic Validator 驗證 citation 後才放入 Context。
7. 載入 Evidence digest、Evidence IDs、snapshot hash 與最多一跳的 traceability subgraph。
8. 載入 output schema、status vocabulary 與 human Gate。

## 4. Token preflight

在 LLM 呼叫前，以 provider tokenizer 估算所有 Context layers。若估算超過 `config/token_budget_policy.yaml` 的 hard limit，立即輸出 `context_over_budget`，不進行模型分析。接著依下列順序拆分：先按標準，再按 Clause／Process，再按 Evidence domain，再按 work package。拆分後保留 `parent_task_id`，並讓每個 child task 具有自己的 citation block 與驗證結果。

Routine mode 的預設值為 12,000 input-token target、16,000 input-token hard limit、3,000 output reserve 與 1,000 validation reserve。正式部署必須依實際模型 context window 按比例縮放；這些數字不是引用完整性的例外條款。

## 5. Citation preflight

Citation Service 不接受模型產生的自由文字 citation。輸入必須是結構化 query：`standard_id`、`edition`、Clause／Process、RQ／RC／PM／WP 或 table-row anchor、source baseline。輸出至少包含 `source_hash`、`anchor`、完整 `verbatim_text`、`verbatim_text_sha256` 與七項 verification checks。

Validator 必須確認 source version match、anchor resolved、complete boundary、hash match、no placeholder、no truncation 與 table structure verified。任何一項為 false，結果都不可進入 normative Context。狀態分別為 `source_version_mismatch`、`anchor_unresolved`、`quote_incomplete`、`hash_mismatch`、`placeholder_detected` 或 `table_structure_uncertain`。

## 6. Evidence digest 的用法

原始 RTL、simulation log、FMEDA、FMEA、FTA、TARA spreadsheet、CVE feed、lab log、tape-out package 與 silicon report 不直接全部放入 Prompt。先建立 Evidence Object，保存 URI、版本、owner、verifier、baseline、hash、status、artifact type 與短摘要；Runtime 只載入與任務有關的 digest 與 pointers。若模型需要判斷細節，建立 child retrieval task 取回原始片段，不能用摘要取代必要證據。

## 7. Shared state

Runtime 之間共享 immutable IDs，而不是複製全文。必要狀態包括 `evidence_snapshot_id`、`traceability_snapshot_id`、`citation_verification_id`、`prior_finding_id`、`decision_record_id`、`rulepack_hash`、`scope_baseline_id` 與 `parent_task_id`。所有狀態更新要以新版本寫入，禁止覆蓋已被引用的 snapshot。

## 8. 何時必須停止

缺少完整核准原文時輸出 `citation_missing`；來源版本不一致時輸出 `source_version_mismatch`；條款或表格邊界無法確認時輸出 `source_structure_uncertain` 或 `table_structure_uncertain`；跨 Part 或前置 work product 不存在時輸出 `dependency_missing`；Context 超出預算時輸出 `context_over_budget`；規範衝突、Scope、ASIL／CAL、TARA rating、殘餘風險、正式 ASPICE rating、Safety Case、Cybersecurity Case、tape-out／production release 或重大 finding closure 涉及權責判斷時輸出 `human_decision_required`。

## 9. Human Gate

R10 Human Review／Approval Gateway 只接收經過 schema 與 citation validation 的 review package。Lead Assessor 負責 ASPICE Scope、正式 rating 與 assessment conclusion；Functional Safety authority 負責 ASIL、SPFM／LFM、PMHF、Safety Case 與殘餘風險；Cybersecurity authority 負責 TARA rating、risk treatment、漏洞處置、Cybersecurity Case 與 Security Case；Process／Verification／QA owner 負責技術真實性與獨立性。LLM 可以準備材料，不能寫入 approved、accepted、closed 或 final compliance claim。

## 10. 最小可行 pilot

先選一個 ASPICE HWE.2 work item、一個 ISO 26262-5 Clause 7 hardware safety work item 與一個 ISO/SAE 21434 TARA work item。三個 task 各自執行 R06、R11／R12 與 R16，只傳入各自的 Rule Pack、完整引用與 Evidence digest；R13／R18 只接收三個結果的 IDs、hashes 與 Cross-Standard Mapping，不重新載入所有原文。用人工核准的 golden cases 比較 citation accuracy、token usage、split rate、schema pass rate 與 finding re-open rate。
