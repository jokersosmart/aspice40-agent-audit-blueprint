# Prompt Composition and Runtime Contract

## 1. 不要為每個 Agent 手寫完全不同的長 Prompt

建議把一次執行的內容分成六層，並依固定順序載入：

| 順序 | 輸入 | 用途 | 是否版本化 |
|---:|---|---|---|
| 1 | `prompts/00_global_policy.md` | 證據優先、未知項、衝突與人工 Gate | 是 |
| 2 | `prompts/10_process_auditor_template.md` 或 `20_manager_template.md` | 共用工作方法與輸出契約 | 是 |
| 3 | `profiles/process_agents.yaml` 或 `manager_agents.yaml` | 角色責任、上下游與 evidence domain | 是 |
| 4 | `knowledge/aspice40/process_rules/{{process_id}}.yaml` | PAM 4.0 的 purpose、outcomes、BP、II 與解釋 | 是 |
| 5 | `knowledge/aspice40/spec_citation_catalog.jsonl` | 每個 normative check 可直接複製的完整 ASPICE 原文段落／表格列、定位與 hash | 是 |
| 6 | `config/process_scope.yaml` | 本次專案的 scope、tailoring、conditional／N/A rationale | 是 |
| 7 | `Evidence Object`、traceability graph、既有 findings | 公司實際證據與目前狀態 | 每次 Run 固定 snapshot |

## 2. Process Agent 的執行訊息

以下是 `HWE.2` 的概念性實例。實作時可把 YAML／JSON 以 structured input 傳入，不要把大型檔案直接截斷貼進 Prompt。

```text
[GLOBAL_POLICY]
載入 prompts/00_global_policy.md

[ROLE_TEMPLATE]
載入 prompts/10_process_auditor_template.md

[PROCESS_PROFILE]
從 profiles/process_agents.yaml 取 HWE.2

[RULE_PACK]
載入 knowledge/aspice40/HWE.2.yaml

[DIRECT_SPEC_CITATIONS]
載入 knowledge/aspice40/spec_citation_catalog.jsonl，並從 HWE.2 Rule Pack 的 `spec_citations` 取出與本次 check 對應的完整 `verbatim_text`。輸出時直接貼出該段原文、source_anchor、verbatim_text_sha256、why_this_text_applies 與 interpretation；不得只輸出 reference。

[SCOPE]
本次 assessment scope:
- project_id: SSDCTRL-A
- baseline: HW-BL-042
- HWE.2: in_scope
- scope_approved_by: REPLACE-ME

[EVIDENCE]
載入 examples/hwe2_audit_input.json 的 evidence_objects 與 traceability_edges

[TASK]
請依 HWE.2 Rule Pack，逐一檢查 outcomes、BP、expected Information Items、traceability、版本／baseline、一致性、review／approval 與跨部門責任。輸出 process-audit-result.schema.json。若 evidence 不足，輸出 unknown；若發現來源或文件衝突，輸出 conflict。不要自行做正式 N/P/L/F rating。
```

## 3. Manager Agent 的執行訊息

Manager Agent 不重新逐句稽核 PAM。它讀取 Process Audit Result、Evidence Object、traceability graph、RASIC／RACI 與專案限制，回答以下問題：誰負責補哪個證據？誰獨立驗證？誰是 QA reviewer？是否存在 self-review？何時完成？完成條件是什麼？重新驗證如何執行？何時需要 escalation？凡是說明某個 action 為何與 ASPICE 要求相關，都必須從原始 finding 原封不動攜帶 `spec_citations`，包含完整 ASPICE 原文段落、章節／Process／BP／GP／II 定位、原文 hash 與解讀；若 citation 缺失，Manager 必須保留 `citation_missing`，不能自行補寫規範原文。

## 4. 工具權限建議

C01 只能寫入規範來源、頁面 manifest 與抽取 QA；C03／C04 只能寫入 evidence index；C05 可以提出 scope draft 但不能自己批准；C06 可以更新 graph candidate 與 conflict；Process Agent 只能產生 audit result；Manager Agent 只能產生 work package；C08 只能建立 report draft 與 human review queue；Human Gateway 才能寫入 approval、正式 rating 或 finding closure。這種最小權限設計比在 Prompt 中單純寫「請小心」更可靠。

## 5. 執行後的可重現性

每一筆輸出都要記錄 `run_id`、runtime version、prompt commit、profile commit、rule pack commit、schema version、scope snapshot、evidence snapshot、model identifier 與執行時間。若日後資料更新，應建立新的 run，而不是覆蓋舊結果。
