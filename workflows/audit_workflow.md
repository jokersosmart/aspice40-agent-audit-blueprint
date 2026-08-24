# ASPICE 4.0 Agent Audit Workflow

## 0. 一次稽核 Run 的輸入

每次執行都要先建立 `run_id`、`project_id`、`release_or_baseline`、assessment context、scope 設定、Prompt／Rule Pack commit、Cognitive Module assignment commit、schema version 與資料擷取時間。沒有這些欄位時，C08 只能產生 draft，不能宣稱結果可重現。

每個 Agent 的載入順序固定為：Global Policy → Cognitive Operating Layer → Agent profile → ASPICE Rule Pack／Spec Citation Catalog → Scope snapshot → Evidence Object snapshot → Traceability snapshot → existing findings。Cognitive Operating Layer 只能提供問題拆解、證據挑戰、跨域分析、溝通與風險分流；PAM 原文與已核准證據優先。

## 1. 規範入庫

C01 接收 ASPICE 4.0 原始 PDF，計算 hash，保留原檔、page-aware text、重排版 semantic text、表格／圖表清單與抽取 QA。C02 再將 Chapter 1–5 與 Annex A–D 切成可引用的 semantic chunks。任何 OCR 或人工修正都要留下原始值、修正值、來源頁面、方法、人工核對者與時間。

## 2. Assessment Scope

C05 讀取產品、專案、客戶／OEM 約定、組織責任與 lifecycle，建立每個 Process 的 scope matrix。MLE.1–MLE.4、SUP.11、ACQ.4、REU.2 通常需要明確的 conditional／N/A 討論；不能因為尚未匯入證據便自動變成 not-in-scope。Scope owner、QA 與 Lead Assessor 或指定責任者必須完成 human gate。

## 3. 證據匯入

C03 從 requirements／ALM、Git／Perforce、PLM、issue tracker、test management、CI、simulation、lab、tape-out／silicon data 匯入 Evidence Object。C04 將 Evidence Object 對應 Annex B Information Item characteristics 與公司 artifact type。此階段只做 normalization，不做合規判斷。

## 4. Process Audit

C08 依 Scope matrix 派送 32 個 Process rule pack。每個 Process Agent 先用 Cognitive Module assignment 將問題拆成可檢查的 claims、證據、依賴、替代解釋與 stop conditions，再依序檢查 purpose、outcomes、BP、需要的 GP／PA、Information Items、上下游流程、證據品質、雙向追溯與跨版本一致性。每一個 normative check 都必須直接附 `spec_citations` 的完整原文段落／表格列；每一筆結果用 `process-audit-result.schema.json` 輸出。

## 5. SSD Controller Cross-domain Review

C06 建立 requirements → architecture → detailed design／RTL／code → verification measure → result → release 的 graph。M01–M10 讀取相關 Process Audit Result，將 findings 轉為責任地圖與工作包。對硬體要分 Digital、Analog／Mixed-Signal、Simulation／Emulation、Tape-out／Silicon 證據來源，但不得另創 ASPICE Process。

## 6. Capability Preparation

C07 將每個 Process 的已驗證 evidence 與 findings 對應 PA 1.1–5.2。它可以使用反方檢查、假設驗證、證據品質與時間／變更影響分析整理 N／P／L／F 的前置判斷、缺證與未知項；每一個 PA／GP 結論都必須攜帶完整 direct spec citation。但它不可以自行選定正式 rating method 或作正式 assessment rating。

## 7. QA 與人工 Gate

Cognitive Operating Layer 的 stop／escalation 規則不能取代人工 Gate；它只能提高人工佇列的辨識率。

M11 檢查 QA independence、process compliance、nonconformance 與 corrective action。C08 產生 `human_review_queue`，至少將以下項目送人工：scope／N/A、技術內容正確性、verification adequacy、重大 finding closure、release approval、正式 N／P／L／F、任何來源衝突與客戶對外聲明。

## 8. Corrective Action 與回歸

M12 管理 problem／change／baseline；M13 管理 risk、schedule、resource、metrics；相關 domain Manager 產出 action。Action 必須指定 owner、reviewer、完成條件、期限、依賴、重新驗證方式與關閉權限。重新驗證後，C08 必須把新的 Evidence Object、revision、baseline 與原 finding 連回同一條 traceability graph。

## 9. Release／Assessment Rehearsal

M14、C08 與 Lead Assessor 準備 evidence index、open issue list、unknown list、cross-domain conflict、assessor question list、assessment input draft 與報告草稿。Agent 產物只能標記為 self-assessment／rehearsal，直到人員完成正式確認。

## 10. Definition of Done

一次完整的內部 rehearsal 至少應滿足下列條件：32 個 Process ID 都有 scope status；每個 in-scope Process 都有 audit result；所有 findings 都有 evidence refs 或明確的 unknown／gap 理由；所有 critical／high findings 都有 owner 與 action；雙向追溯與版本／baseline 檢查已執行；QA 與 verification independence 已檢查；重大 conflict 沒有被刪除；Prompt、Rule Pack、schema 與輸入資料版本可重現；人工 Gate 狀態完整。
