# Shared Runtime、Token Budget 與 Direct Citation Architecture

## 1. 核心結論

90 個邏輯角色不應等於 90 次同時存在的完整 Prompt，也不應把所有 ASPICE、ISO 26262-5、ISO/SAE 21434 的規範、所有 Rule Pack、所有 Evidence 與所有歷史 finding 一次送入一個模型。正確做法是把角色視為「責任配置」，把 Runtime 視為「可重用執行器」，每一次執行只選擇一個邏輯角色、一次任務、最小的規範範圍、最小的 Evidence 子圖與必要的完整引用。

> **LLM 負責分析與解讀；受控 Citation Service 負責擷取原文；Deterministic Validator 負責確認版本、anchor、段落邊界與 hash；Human Gateway 負責規範權威、風險接受與正式結論。**

這四個責任不能由同一個模型自行兼任。尤其不能把「模型說它引用了某個 Clause」當成引用正確性的證明。

## 2. 90 個角色如何映射到共用 Runtime

| 角色群 | 邏輯角色 | Runtime | 每次執行載入內容 |
|---|---:|---|---|
| ASPICE control | C01–C08 | R01–R08 | 一個 active control profile、對應 schema、任務需要的規範索引 |
| ASPICE Process | 32 個 Process ID | R06 | 一個 Process Rule Pack，不載入其他 31 份全文 |
| ASPICE／組織 Manager | M01–M14 | R09 | 一個 manager profile、相關 findings、責任子圖 |
| ISO 26262 Safety | FS01–FS15 | R11–R14 | 一個 safety profile、Clause／table citation records、Safety Evidence |
| ISO 26262 Manager | M15–M17 | R14 | 一個 manager profile、Safety findings、必要跨規範子圖 |
| ISO/SAE 21434 Cybersecurity | CS01–CS15 | R15–R18 | 一個 cybersecurity profile、RQ／RC／PM／WP citation records、Cybersecurity Evidence |
| ISO/SAE 21434 Manager | M18–M20 | R18 | 一個 manager profile、Cybersecurity findings、TARA／Case 子圖 |
| Human authority | 不屬於 LLM role | R10 | 只讀取待核准的 finding、citation verification、Evidence snapshot 與決策表單 |

同一個 Runtime 可以依 `agent_id` 動態載入不同 profile；Runtime 本身不應把 90 個角色的 Prompt 全部放進 context。Role profile、Cognitive assignment、Rule Pack、Scope 與 Evidence 都透過 ID／版本／hash 引用，只有本次任務需要的內容才會被組裝。

## 3. Context Assembly 的六層結構

每一個 LLM invocation 使用 `schemas/runtime-execution-envelope.schema.json` 表達輸入邊界。Context Assembly 應依序建立六層：Global Policy；單一 active role profile；任務 Scope 與 baseline；目標 Clause／Process 的 Rule Pack 與完整直接引用；Evidence digest 與一跳 traceability subgraph；最後是 output schema、error vocabulary 與 human Gate。

| Layer | 內容 | 是否可摘要 | 是否可省略 |
|---|---|---|---|
| L0 Global policy | 規範優先、direct citation、unknown、人工 Gate | 不可改寫規則 | 不可 |
| L1 Role profile | 一個 active Agent 的職責、輸入、輸出與不可越權 | 可使用固定短 profile | 其他 89 個 profile 必須省略 |
| L2 Scope／baseline | 產品邊界、客戶要求、release、版本、tailoring、dependency | 可使用 immutable snapshot | 不能省略適用性欄位 |
| L3 Rule Pack／Citation | 目標 Process／Clause 的規則與完整原文段落／表格列 | Citation 不可摘要或截斷 | 不可省略適用的 normative citation |
| L4 Evidence digest | Evidence ID、版本、owner、verifier、status、關聯摘要與原始 artifact pointer | 可摘要導航，但原始證據需可回取 | 不能省略 evidence refs |
| L5 Shared state／output | traceability snapshot、prior findings、decision records、schema、Gate | 可用 ID／hash／分頁 | 不可省略版本與狀態 |

完整 Citation 不應由 LLM 自己從一大段 PDF 中挑出並重新複製。LLM 先提出 citation query，例如 `standard_id + edition + clause + provision_id + table_row`；Citation Service 再回傳完整核准文本；Validator 通過後，才允許該引用進入 LLM context。

## 4. Token Budget 原則

Token budget 必須以模型實際 context window 為輸入，而不是假設所有模型都能安全接收同樣大小的 Prompt。預設 routine mode 將輸入 context 控制在模型 context window 的 60% 以下，另保留輸出、validation、error 與人工 Gate metadata 空間；complex mode 也不可超過 70%。真正的硬限制由 `config/token_budget_policy.yaml` 管理。

建議的 routine budget 是 12,000 input tokens target、16,000 input tokens hard limit、3,000 output reserve、1,000 validation reserve。這些數字是 Runtime policy 的預設值，不是所有模型的永久保證；若模型 context window 較小，必須依比例縮放。

### 不可採用的壓縮方式

不可截斷 normative quotation，不可把完整引用換成摘要，不可用 embedding、reference ID、page number 或模型記憶替代 verbatim text，也不可把三套規範合成一個模糊的「安全要求」。如果完整引用加上必要 Evidence 超過 budget，正確做法是切割成多個 child task，而不是刪除引用。

### 可採用的壓縮方式

可以把重複文件替換為 immutable Evidence ID 與 snapshot hash；可以只帶一跳 traceability subgraph；可以先用 evidence digest 導航，再按需要回取原始 artifact；可以依 citation hash 去除相同原文；可以把同一個 Runtime 的多個獨立 work item 分批執行，最後交給 Orchestrator 合併。

## 5. Runtime 執行流程

一次安全的執行應依照以下狀態機進行：

| 階段 | 執行者 | 主要動作 | 失敗狀態 |
|---|---|---|---|
| 1. Intake | Orchestrator | 建立 run／task、選 runtime、確認 agent role | invalid_scope、unknown_task |
| 2. Scope Gate | Scope Runtime | 確認產品、客戶、release、標準與 dependency | not_in_scope、dependency_missing |
| 3. Citation Query | Citation Service | 依 anchor／provision／table row 取得完整原文 | citation_missing、anchor_unresolved |
| 4. Citation Verify | Deterministic Validator | 比對 source version、source hash、quote hash、邊界、placeholder、表格結構 | source_version_mismatch、hash_mismatch、quote_incomplete |
| 5. Context Assemble | Runtime | 只組裝單一任務最小 Context | context_over_budget |
| 6. LLM Analysis | Active role | 進行 evidence mapping、gap analysis、alternative explanation 與 action planning | model_error、insufficient_evidence |
| 7. Output Validate | Schema／Policy Validator | 驗證 citation、Evidence、狀態與 Gate 欄位 | output_contract_error |
| 8. Human Route | R08／R10／Safety／Cybersecurity Manager | 建立人工作業佇列與決策記錄 | human_decision_required |
| 9. Persist | Evidence／Decision Store | 儲存 immutable output、版本、hash、parent／child task | persistence_error |

## 6. Citation 正確性的四個必要 hash

`source_hash` 是整份核准來源的 hash；`verbatim_text_sha256` 是實際引用內容的 hash；`rulepack_hash` 是載入的角色規則版本；`evidence_snapshot_hash` 是當時證據快照的 hash。四者用途不同，不應只保存一個 hash。

| Hash | 驗證對象 | 目的 |
|---|---|---|
| source_hash | 受控 PDF／文本來源 | 確認使用哪一版來源 |
| verbatim_text_sha256 | 完整引用段落／表格列 | 確認引用未被改寫、截斷或串接 |
| rulepack_hash | Agent 規則包 | 重現當時採用的檢查範圍 |
| evidence_snapshot_hash | Evidence／traceability snapshot | 重現當時的事實基線 |

Validator 應至少執行：標準與版次比對、anchor 是否唯一解析、段落／表格完整邊界、引用 hash 比對、禁止 placeholder、禁止未核准 OCR、禁止跨版次混用、禁止把相鄰段落錯誤黏接，以及表格列／欄關係是否已驗證。

## 7. 分批與並行策略

同一個 Runtime 可以對多個獨立 work item 並行，但每個 work item 必須有獨立 task ID、獨立 Context Envelope 與獨立 output。對 R06、R11、R12、R15、R16 等高密度 Runtime，建議最多同時處理 2–4 個 work item，並將大 Evidence 拆成 Evidence digest、citation task、technical review task 三個階段。

例如 HWE.2 與 ISO 26262-5 Clause 7 的一個安全硬體設計檢查，不應把 ASPICE 全本、ISO 26262 全本、21434 全本、RTL repository、FMEDA、TARA 與測試 log 一次送入 R06。應由 R08 建立 DAG：先由 R04 確認 Scope，再由 R03 建立 Evidence refs，再由 R05 取出 HWE.2 子圖；接著 R06 只載入 HWE.2 Rule Pack，R11 只載入相關 ISO 26262-5 citation，若牽涉 security control 再由 R16 另外載入 ISO/SAE 21434 citation。最後 R14／R18 做跨規範 mapping，R10 進行人工核准。

## 8. Output 不應是「通過／不通過」

每一次 LLM 執行應輸出結構化 finding，至少區分 `satisfied`、`partial`、`gap`、`unknown`、`conflict`、`not_in_scope`、`citation_missing`、`dependency_missing`、`context_over_budget` 與 `human_decision_required`。Manager 可以將 finding 轉成 work package，但「建議行動」不等於「證據已完成」，也不等於「規範已符合」。

## 9. 觀測性與成本控制

每次執行需記錄 input token estimate、實際 input／output token、模型版本、Runtime、agent_id、Rule Pack hash、citation hash、source hash、cache hit、split count、retry count、validation result、human Gate status 與最終 outcome。不要只記錄 LLM 回答文字，否則無法分析哪一個 Runtime 造成 token 爆量或哪一個 citation parser 經常失敗。

最有價值的指標包括：每次任務平均輸入 token；Citation cache hit rate；citation verification failure rate；context_over_budget rate；一次通過 schema 的比例；跨規範 conflict rate；人工退回率；finding re-open rate；以及由人員抽樣檢查發現的引用錯誤率。任何引用錯誤率上升都應優先停用該 Runtime 的自動結論，而不是提高模型溫度或增加 Prompt 長度。

## 10. 建置順序

第一階段先完成 Citation Service、Deterministic Validator、Runtime Execution Envelope、Token Budget Policy 與 R10 Human Gateway。第二階段選 R06 ASPICE Process Audit 與 R16 ISO/SAE 21434 TARA／Product Runtime 做小範圍 pilot。第三階段接 R11／R12／R15／R17 等高風險 Runtime，最後才擴展到所有 Manager 與 Orchestrator。每一階段都要用同一批人工已核准的 golden cases 做 regression，確認 token 下降沒有造成 citation 完整性或 finding 品質下降。
