# ASPICE Agent Implementation SOP

## 1. 建議第一期實際部署

第一期不要一次啟動 54 個角色。先部署 C01、C02、C03／C04、C05、C06、C08，以及 SYS.1–SYS.5、SWE.1–SWE.6、HWE.1–HWE.4、VAL.1、SUP.8、SUP.9、SUP.10。這些角色可以覆蓋 SSD Controller 最重要的需求、架構、設計、實作、驗證、配置、問題與變更證據鏈。M01、M02、M03、M08、M09、M10、M12 先啟用；其餘 Manager 在第二期加入。

## 2. 每一個專案建立 Run Snapshot

在開始任何稽核前，建立一個不可覆蓋的 run 目錄，例如：

```text
runs/2026-08-24/SSDCTRL-A/HW-BL-042/
├── input/
│   ├── scope.yaml
│   ├── evidence_snapshot.jsonl
│   └── traceability_snapshot.jsonl
├── outputs/
│   ├── process_audit/
│   ├── manager_work_packages/
│   ├── findings/
│   └── human_review_queue/
└── manifest.yaml
```

`manifest.yaml` 必須記錄 Git commit、Prompt 版本、Rule Pack 版本、schema 版本、model identifier、資料擷取時間、evidence snapshot hash 與 scope approval 狀態。

## 3. 載入順序

每個 Process Agent 依序載入 Global Policy、Process Auditor Template、Process profile、Process Rule Pack、Scope snapshot、Evidence Object snapshot、Traceability snapshot 與既有 findings。若任一必要輸入缺失，Agent 必須輸出 `unknown` 或 `blocked`，不能自行補值。

## 4. 先做一個 Process 的 dry run

建議用 HWE.2 做第一個 dry run，因為它可同時驗證 digital hardware、analog／mixed-signal、simulation／emulation、tape-out／silicon 的 evidence mapping。使用 `examples/hwe2_audit_input.json`，將 `REPLACE-ME` 欄位替換成實際 hash、owner、baseline、approval 與 URI，然後執行 HWE.2 Process Auditor。確認輸出能逐項列出 hardware architecture、detailed design、schematics、RTL、layout、BOM、production data、simulation、analysis、measurement、communication 與 traceability。

## 5. Finding 轉 Action

只有當 finding 具備來源、狀態、影響、證據缺口與信心後，才交給對應 Manager。Manager 要把 finding 轉成有 owner、reviewer、required artifacts、completion criteria、due date、dependency、reverification plan 與 closure authority 的 work package。`補文件` 不是可接受的 completion criteria；應寫成「建立哪一個 artifact、包含哪些內容、由誰 review、要連回哪一個需求／設計／verification result」。

## 6. 人工 Gate

以下項目必須停在人工佇列：scope／N/A、技術正確性、verification adequacy、正式 rating、重大 finding closure、tape-out／release approval、客戶對外聲明與規範來源矛盾。Agent 可以提供比較表與建議，但不能自動批准。

## 7. 逐步擴張

第一個 dry run 通過後，擴張到 SYS／SWE／HWE 全部 Process，再加入 M08–M10 的驗證管理。當 traceability 與 Evidence Object 穩定後，加入 SUP.1、MAN.3／5／6、PIM.3、SPL.2、ACQ.4、REU.2 與 M11–M14。MLE.1–MLE.4 與 SUP.11 僅在確認產品有 ML requirements／model／training data 時啟用，否則建立受人工批准的 scope rationale。

## 8. 交付檢查

每個 release 前，C08 要確認 32 個 Process ID 都有 scope status、每個 in-scope Process 都有結果、所有 critical／high findings 都有 action、所有 action 都能回到原 finding、所有重新驗證都產生新的 Evidence Object、所有 Prompt／Rule Pack／schema／輸入 snapshot 可重現，並且 human review queue 沒有被未授權關閉。
