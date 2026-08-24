# Direct Spec Citation Policy

## 1. 核心要求

任何 Agent 只要對 ASPICE 4.0 的 purpose、outcome、Base Practice、Generic Practice、Process Attribute、Information Item、definition、assessment guidance 或 Annex guidance 做出判斷，就必須在該筆判斷內直接貼出對應的完整原文段落。只寫 `HWE.2.BP5`、`PA 2.2`、頁碼、文件名稱或超連結，均不算有效引用。

每個 `spec_citations[]` 至少包含：

| 欄位 | 要求 |
|---|---|
| `verbatim_text` | 從核准的 ASPICE 4.0 文字庫複製完整段落；表格情境則複製完整列／欄內容 |
| `source_anchor` | section、Process ID、indicator ID、page、source line range、source file |
| `verbatim_text_sha256` | 對引用文字計算的 SHA-256，防止事後改寫 |
| `why_this_text_applies` | 為什麼這段原文適用於本次檢查 |
| `interpretation` | 用自己的話解釋原文在本次 evidence mapping 的意思 |
| `requirement_type` | PAM 明文、公司規則、客戶要求、產品情境或推論 |
| `verified_status` | PDF／核准文字／OCR／人工核對狀態 |
| `human_confirmation_required` | 技術正確性、Scope、rating、重大 finding 等情境一律為 true |

## 2. 完整段落的判定

「完整」是指從一個規範段落的開頭到該段落結束；不得只截取第一句來改變語意。若 Base Practice 後有直接適用的 Note，Agent 應另建立一筆 citation 或將 Note 與該段落一起引用。若規範要求以表格欄位／X matrix 表達關係，必須引用完整的表格列與欄位標頭，不得只貼一個 X。

只能做以下不改變文字意義的正規化：移除 PDF physical line break、合併單字斷行、統一空白。任何 OCR 修復都必須同時保存 `original_text_if_corrected`、`text_normalization: verified_ocr_correction`、修復方法與核對者。

## 3. 一筆 finding 的最低結構

```json
{
  "process_id": "HWE.2",
  "check_id": "HWE.2.BP5",
  "requirement_type": "pam_explicit",
  "spec_citations": [
    {
      "citation_id": "SPEC-HWE2-BP5-001",
      "source_anchor": {
        "section": "4.7.2",
        "process_id": "HWE.2",
        "indicator_id": "BP5",
        "page": 73,
        "source_line_start": 4735,
        "source_line_end": 4738
      },
      "verbatim_text": "Ensure consistency and establish traceability between hardware elements and hardware requirements. Ensure consistency and establish traceability between the hardware detailed design and components of the hardware architecture.",
      "verbatim_text_sha256": "SHA-256-OF-VERBATIM-TEXT",
      "why_this_text_applies": "本次檢查的是 hardware requirement、hardware element、detailed design 與 architecture 的雙向追溯。",
      "interpretation": "除檢查 link 存在外，也要檢查方向、版本、baseline 與內容一致性。",
      "verified_status": "verified_against_approved_text",
      "human_confirmation_required": true
    }
  ],
  "evidence_refs": [],
  "status": "unknown"
}
```

上面 `verbatim_text` 只是欄位格式示意；正式執行時，必須載入 approved citation catalog 的實際完整段落，不可使用 placeholder。

## 4. 缺引用時的處理

若 Agent 找不到對應的 approved paragraph 或表格列，輸出 `citation_missing: true`、`status: unknown`、`confidence: low` 與 `human_confirmation_required: true`。禁止用模型記憶補寫看似合理的 ASPICE 原文。若來源正文與表格衝突，建立兩筆完整引用，`status: conflict`，並把 conflict 送人工確認。

## 5. Manager 的繼承規則

Manager Agent 產生責任地圖、工作包、升級或重新驗證 action 時，必須攜帶原 finding 的 `spec_citations`，或建立對應的完整 direct citation。Manager 不得將完整原文壓縮成只有 BP ID 的摘要後再往下傳遞。

## 6. 版本與法律邊界

Citation catalog 必須與 PAM 4.0 source hash、Rule Pack commit、Prompt commit 與 audit run 綁定。這份系統是內部自評與證據準備工具；正式 assessment scope、rating、重大 finding closure 與對外聲明仍需由授權人員／Lead Assessor 決定。引用與轉換方式也要遵守原始文件的版權與散布條件，不能因為 Agent 需要原文就任意對外重發布完整文件。
