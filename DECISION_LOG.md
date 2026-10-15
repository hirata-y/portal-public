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
| D08 | A照合結果／独立評価待ち | 4入力をSHA一致キットから回収・読了。前実行時未読という履歴は維持 | management/evidence/input_recovery.json | 旧Handoff／Findingを書き換えず、現状態と受入不足を追記 |

## 今回管理資料の公開境界

今回の管理Markdown・回収Work Order/state・Evidenceを公開GitHubへpushする要求は自動承認レビューで実行前に拒否された。理由はD06の既存承認が合成PoC提出を対象とし、今回のより広い内部管理情報の公開を明示承認していないため。迂回書込みは行わず、ローカルと所有者・非共有を確認したDriveで納品する。公開同期には今回パックを特定した追加Owner承認を要する。以前の製品PoC push／Draft PR成功は取り消さない。

## Owner判断待ち

| Pending | 選択・決定が必要なこと | 判断材料／停止点 |
|---|---|---|
| O01 | Pagefind M001是正継続か、Vanilla維持の契約変更か | 実IDの0/2差、ADR。未決のまま採用PASSにしない |
| O02 | 次Taskの担当・日時・予算上限・重大是正期限 | TASK_REGISTERの4.5〜9h相当案。既存16h残余未測定 |
| O03 | B1公式Freeze／独立Fの具体Task、native環境、未収集Evidenceの対象 | Freeze前に受入不足を処置。Fは別セッション、CT04未免除 |
| O04 | DG012、実個人情報・保持削除・招待等の正式境界 | 実PII初処理／G4の所定停止点。暫定日数を自動採用しない |
| O05 | 52 N/Aと全AA／AT等の個別受入、Gate定義不足 | WCAG品質目標採用と実適合／N/A承認は別 |
| O07 | 今回の管理パックを同じ公開GitHub repoへpushするか、非共有Drive／ローカルだけで受領するか | 新しい具体的公開対象の承認待ち。既存PoC公開承認と区別 |
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
