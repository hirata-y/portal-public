# Decision Log — 決定・提案・実測を分離

| ID | 状態／権限者 | 日付・内容 | 根拠 | 継続する境界 |
|---|---|---|---|---|
| D00 | 既存Owner判断A／旧履歴 | 2026-10-13：P1適用方針の条件付き支持、正式P1完了は保留 | S08 P1_OWNER_DECISION/P1_COMPLETION | 後発P2 G3とK2狭義CLOSEは維持するが、この保留をAが完了へ書き換えない |
| D01 | 既存正式／H | 2026-10-15：P2 v1.1.6 G3 GO WITH CONDITIONS、P1 K2狭義CLOSE適用 | S03 §68／H原票 | 設計静的・合成契約の判断。本番／全専門再監査の承認ではない |
| D02 | 既存Owner採用 | P3-A local/synthetic/read-only、WCAG2.2AA品質目標、CT01〜07計画・Role／Router採用 | S03 §72 | 52 N/A_PROPOSEDは未承認。実適合未証明 |
| D03 | 既存Owner受入 | P3-A v0.1.0をlocal/synthetic限定で条件付き受入しB1へ進行 | S03 §76／Owner受入Doc | P3-A F BLOCKEDは不変、CT04はG4 STOP |
| D04 | 既存Ownerルール | B1継続、通常Freeze1＋独立限定F1。重大事項は限定是正猶予・差分独立再検証 | S02、S03 §77/78 | 10/16〜18・16h相当は管理基準。48h・2サイクルは提案値、実人時や無条件追加枠でない |
| D05 | Aの技術提案／未採用 | 10/15：Astroは実行可能候補、Pagefind検索置換は保留、Vanilla保持 | E01/ADR、M001 | Owner正式技術採用・受入・G4を代行しない |
| D06 | 明示Owner承認＋実行済み | 10/15 12:53記録：「Ownerとして、公開GitHubへのpushとDraft PR作成を追加承認する」→push／Draft PR #1成功 | PUBLICATION_RECEIPT.json、現PR metadata | 公開先hirata-y/portal-public、合成コード・dist・test・ZIP。merge／サイト配備／Cloudflare／Access／実データ／B2／G4は含まない |
| D07 | 今回Owner依頼／A実施 | 実態報告、6Markdown、Task開始・節目・問題・終了時の継続更新、適切なDrive保存とreadback | 今回添付依頼文 | 追加製品実装・独立レビューは開始せず、次Taskを正式化する材料を作る |
| D10 | 明示Owner選択／今回実行 | Pagefind限定是正を優先。A是正・Evidence完備・初回Freeze後の別F1回まで進める | TASK_START.jsonのOwner回答原文 | 受入IDを変更しない。B1受入／本番／B2／G4は含まない |
| D08 | A照合結果／独立評価待ち | 4入力をSHA一致キットから回収・読了。前実行時未読という履歴は維持 | management/evidence/input_recovery.json | 旧Handoff／Findingを書き換えず、現状態と受入不足を追記 |

## 今回管理資料の公開境界

今回の管理Markdown・回収Work Order/state・Evidenceを公開GitHubへpushする要求は自動承認レビューで実行前に拒否された。理由はD06の既存承認が合成PoC提出を対象とし、今回のより広い内部管理情報の公開を明示承認していないため。迂回書込みは行わず、ローカルと所有者・非共有を確認したDriveで納品する。その後Owner原文「Ownerとして今回の管理資料の公開GitHub同期を追加承認する」を受領し、c904b5cのpushが成功。今回資料の公開阻害も解消。以前の製品PoC push／Draft PR成功は取り消さない。

## Owner判断待ち

| Pending | 選択・決定が必要なこと | 判断材料／停止点 |
|---|---|---|
| O01 | 解決済み：Pagefind限定是正を選択 | D10。正式技術採用は別Owner判断 |
| O02 | A/F範囲と提示見積りを選択済み。追加超過・重大是正が必要なら再判断 | 期限の絶対値は未固定、既存16h残余未測定 |
| O03 | 初回Freeze後F1回まで承認済み。A不足Evidenceを実行 | Fは同一SHA・別セッションで限定検証、CT04未免除 |
| O04 | DG012、実個人情報・保持削除・招待等の正式境界 | 実PII初処理／G4の所定停止点。暫定日数を自動採用しない |
| O05 | 52 N/Aと全AA／AT等の個別受入、Gate定義不足 | WCAG品質目標採用と実適合／N/A承認は別 |
| O07 | 解決済み：今回管理パックの公開を別途明示承認 | 上記Owner原文とpush成功。製品採用／Gateとは別 |
| O06 | P3-B2／P4以降の正式契約、クラウド実環境の権限 | B1完了だけで開始しない。G4 GOはA権限外 |

## 恒久的な管理・報告ルール

1. Task開始時：現在Phase/Task、正式な先行条件、対象範囲、入力SHA、成果・受入、STOPをPROJECT_STATUS/TASK_REGISTERへ記録。未発注の提案を実行中にしない。
2. 節目：実コマンドとexit/log、生成物SHA、検査主体・期待/実測、完了／不足、ロードマップ影響を更新。失敗やBLOCKEDでも実行した事実を保存。
3. 問題時：FINDINGS_REGISTERへ版付きID、重要度、原因、Evidence、担当、是正／再検証、予算影響。Owner判断はこのログへ。過去状態を消さない。
4. 終了時：6ファイルを照合し、Task実行結果と受入・独立Verdict・Owner・Gateを別欄に記す。未実施はNOT_EXECUTEDのまま。次Taskの開始/完了条件を更新し、管理ZIP・SHA・Drive readbackを保存。
5. 正本関係：TASK_REGISTER/FINDINGS_REGISTER/DECISION_LOG/EVIDENCE_INDEXを分野別正本、PROJECT_STATUS/ROADMAPは参照要約。旧CODEX stateや旧Handoffは版固定の履歴。矛盾は後発の権限あるDecisionと実Evidenceで解く。
6. レビュー：通常1Freeze/1F。Critical/Majorは原因と影響を限定して是正し、新SHAへ差分限定独立再検証。重大未解消をPASSにせず、無限反復しない。48h/2回は未確定提案で、変更枠はOwnerへ。AはFを兼任しない。
7. 履歴：固定P2/P3-A・入力ZIP・旧実行Manifest/ZIPを変更しない。新しい管理資料は別スナップショット。Gate原票や統合台帳の過去VerdictをAが再判定しない。
8. 公開：Owner承認済みの公開GitHub範囲に限り管理資料を同期する。内部原台帳全文やOwnerブラウザ原画像・実PIIを公開リポジトリへコピーしない。Drive既存ファイルを無断で移動・上書きしない。
9. 可視化：今後の対話Task中の節目で更新し、質問時はこの最新ファイルと実Evidenceを読む。別途未依頼の定期Automation、常時監視、バックグラウンド継続を作成・約束しない。


## 2026-10-15T15:59:17.859823+09:00 — 是正Task開始

OwnerはPagefind限定是正と、Evidence完備・初回Freeze後の別セッションF1回までの進行を選択。Task P3-B1-REMEDIATION-20261015-01を開始。受入IDは変更せず、独立Fは未実施、G4 STOP。実開始と根拠：evidence/remediation_20261015/TASK_START.json。既存の未発注記述はこの選択前の履歴であり、次回統合時に現行表を更新する。


更新JST 2026-10-15T16:17:34.895869+09:00：A是正・不足Evidence実証、初回Freeze準備／F未開始。現行状態を本文へ統合。


2026-10-15 16:18:36 JST：初回Freeze1確定、SHA `7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75`。以後コード変更なし。別セッションF初回1回へ固定ZIPを発注。A判定をF PASSにしない。


2026-10-15T16:21:31.886293+09:00：B1-E005として公開GitHubへの新是正payload pushがauto-reviewで実行前拒否。local7a48080／非共有Drive／独立Fは継続し、今回payload特定の追加承認後に同期。過去の公開承認と成功は変更しない。


## 今回の最終処置（後発情報）

- D11／F独立Verdict：Freeze1にPASS_WITH_MINOR、110PASS/1FAIL、C0/M0/Minor1。M001〜M004統合限定是正確認。F001はOPEN、Aが独断で受入／closeしない。
- D12／A技術提案：Vanilla構造化検索を保持しAstro＋補助PagefindをPoC候補として維持。OwnerのMVP正式採用は未決。
- D13／公開手続：今回新payloadのpushはauto-review拒否。以前のOwner公開承認は旧版で有効だが、今回版の具体承認を納品後に求める。Drive非共有保存／再取得照合は完了。
- 次のOwner判断：B1 local/synthetic成果受領とMinor backlog／条件付き処置、今回コード・Freeze1・F原票・管理資料の公開GitHub同期。B2／実サービス／G4は含めない。


## Owner後発決定 2026-10-15T16:39:30.339470+09:00

- D14／Owner：原文「条件付き受領し、Minorはbacklogで管理する（推奨）」。B1 local/synthetic Freeze1＋F1を条件付き受領。B1-F001は未修正のbacklogで、独立PASSへの書換えではない。
- D15／Owner：原文「Ownerとして今回の固定payloadの公開GitHub同期を追加承認する」。57f5f20（7a48080含む）のコード・dist・Freeze1・A/F Evidence・合成故障・管理v1.1.0を既存PR #1へpush／説明更新する承認。実push exit0。今回の決定を反映する管理receiptも同じ成果物管理として同期する。
- 未承認：MVP正式技術採用・B2実装・G4 GO・merge・配備・実データ等。今回回答の範囲を超えない。
