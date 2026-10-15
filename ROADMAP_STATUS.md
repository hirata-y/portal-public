# P0〜P7／G0〜G9 ロードマップ進捗

更新：REPORT時刻はPROJECT_STATUS.md。進捗率は算出しない。Phase全体のTask母数と重みが未確定であり、テストPASS率を工程進捗率へ換算しない。下表は資料から確認できた範囲。P0/P1全体の正式完了記録や未実施Gateを創作しない。

| Phase／名称 | 決定・検証予定 | 既決・完成 | 未完了 | 状態 | 完了判定条件 | Evidence | 次工程のOwner／Gate判断 |
|---|---|---|---|---|---|---|---|
| P0 構想確定 | 目的・対象利用者・MVP | PROJECT v1.0.2で本人更新・一般/許可身内の閲覧、検索/比較/参照、MVPを定義。旧PROGRESSは基準計画作成済み | 構想の初期正式完了署名・Gate原票未照合 | 基準計画・目的/MVP確認／正式原票未照合 | 目的・利用者・MVP範囲と承認記録を同定 | S08 PROJECT/PROGRESS。P0の独立Gate原票は未同定 | 元承認を確認。Aが遡及GOしない |
| P1 標準適用・統制設計 | 標準・Role・Router・Gate | Role分離・PROC02/03/04・GOV12運用参照、v1.1.6へのQA02 K2狭義CLOSE | P1全体完了原票・初期Gate全定義未照合 | 統制適用／部分的正式証拠 | Owner判断A（条件付き支持）とP1完了保留の既存履歴を保持。後発K2狭義CLOSE範囲を超えない | S08 P1_COMPLETION/OWNER_DECISION＋S03 §68、S01/S02 | K2の限定判断維持。P1全体やG1/G2と同一視しない |
| P2 要件・コンテンツ・UX設計 | 要件・schema・受入契約・G3 | v1.1.6固定、レビュー工程終了、H G3 GO WITH CONDITIONS | CT01〜07後続実証、DG012・52 N/A等 | 設計レビュー完結／条件付き | 条件の担当・Evidence・停止Gateを後続に移管 | S03 §68/69/72、Full SHA pin | 既存G3とOwner CP3決定を維持。再レビュー自動起動なし |
| P3-A ローカルUI | 8件・3テーマ・検索・HTTP UI | v0.1.0公式Freeze1、F1回、Owner local/synthetic条件付き受入 | F BLOCKEDの独立native HTTP、CT04、全AA/AT | Owner条件付き受入／F履歴BLOCKED | CT04独立ブラウザと後続AX証拠を指定Gateまでに充足 | S03 §72〜76、P3-A SHA pin／F原票リンク | Owner受入をF PASSへ転記しない。CT04はG4 STOP |
| P3-B1 ローカル技術PoC | Astro・日本語検索・分離・4形式・ADR | A実証、Freeze1、別F1 PASS_WITH_MINOR、C0/M0/Minor1 | Owner受入・Minor処置・MVP採用判断、今回public同期E005 | 技術実証・限定F完了／Owner判断待ち | 同一SHA原票受領→Minor処置→B1受入判断 | Freeze1 SHA／F原票・ZIP／ADR002／現行6資料 | B1受入／技術採用／今回公開承認。B2・G4は別判断 |
| P3-B2 認証・実配信PoC | Workers・Access・JWT・実HTTP | 範囲分離とCT01/02停止条件を定義 | 実装・実環境・権限・認可・Range/cache等すべて | 未着手／別契約 | Ownerの明示Task／環境認可と実正負試験、専門レビュー | S01/S02/S03、SECURITY_AND_G4_STOPS | B1完了だけで開始しない。別Owner承認とGate条件 |
| P4 MVP実装・品質 | 本体・CI/CD・統合試験 | 今回参照資料で本体完成Evidenceなし | MVP実装、統合・CI/CD、品質判定 | 未着手として管理／着手Evidenceなし | 採用方式・要件・認証境界・テスト／Gate契約を満たす | 将来Evidence未作成 | 先行技術／Gate判断とP4正式Task |
| P5 既存成果物移行 | HTML/PDF/Slides/Sheets実資料移行 | B1の合成4形式のみ | 実原典53、権利・意味・忠実性・移行試験 | 未着手／合成と区別 | CT05、権利・承認・provenanceと形式別受入 | S03の後続条件、B1合成形式は参考のみ | 実資料取込・権利確認をOwnerが別承認 |
| P6 本番公開・運用開始 | G7/G8・配信・認証・復旧 | 公開本番サイトの作成なし。GitHub成果物公開のみ | リリース、実認証、監視・復旧・運用承認 | 未着手／公開配備禁止継続 | 本番安全・復旧・運用責任と必要Gate正式承認 | 将来実配信／復旧Evidenceなし | G7/G8正式定義照合とOwner配備承認 |
| P7 運用評価・改善 | 利用実績・改善・標準改訂・G9 | 今回は管理更新ルールのみ整備 | 実利用計測、改善評価、G9 | 未着手／運用実績なし | 運用KPI・評価期間・変更統制・G9判断 | 将来運用Evidenceなし | 実運用開始後の正式Task／Owner判断 |

## Gate台帳

| Gate | 状態 | 根拠・残条件 | 判定権限 |
|---|---|---|---|
| G0 | 原定義／判定未照合 | P0原本未取得。過去の成否を推測しない | 正式標準の指定Role／Owner |
| G1 | 原定義／判定未照合 | P1 K2狭義CLOSEをG1へ読み替えない | 同上 |
| G2 | 原定義／判定未照合 | 台帳にStage再baseline案はあるが、G2正式原票を同定していない | 同上 |
| G3 | GO WITH CONDITIONS（既存正式） | S03 §68、H原票。P2静的／合成契約の判断。後続実サービス承認ではない | H正式Verdict＋Owner条件／Task判断 |
| G4 | NOT_APPROVED／STOP | CT04のB1独立Linux HTTP部分はF実証。全AA/AT等と関連CT01/02/03/06・正式判断は残り、B1合格だけでは進めない | 正式Gate担当＋Owner。A代行禁止 |
| G5 | 定義原本未照合／未実施 | 後続実装・移行等の正確なGate対応はOwner／標準で確定 | 正式標準の指定Role／Owner |
| G6 | 定義原本未照合／未実施 | 完了Evidenceなし | 同上 |
| G7 | 未実施／後続STOP保持 | 実配信・実DOM/WCAG/AT・native200%等の移管条件。Gate全定義は未照合 | 正式Gate担当＋Owner |
| G8 | 未実施／原定義詳細未照合 | P6運用開始・配信/復旧の実証は未実施 | 正式Gate担当＋Owner |
| G9 | 未実施／原定義詳細未照合 | P7運用評価の原票・Evidenceなし | 正式Gate担当＋Owner |

## CT01〜07継承

CT01実issuer/JWT/Access：未実施。CT02 GET/HEAD/Range/304/cache：公開loopback GETのみ、実protected delivery未実施。CT03依存：lockとnpm ci、license metadata267件・実license確認、npm audit既知0を実施。法的／全バイナリ権利証明は未実施。CT04：A headful実HTTP＋native URLバー実施、B1独立Fの実HTTP部分は完了、全AA/AT/native200%は未完。CT05実原典・権利：合成のみ。CT06 DG012：未承認の実PII処理禁止。CT07 Task責任／日付／Evidence：本6資料で追跡し、提案と承認済みTaskを分離。

S01〜S03／E01〜の所在はEVIDENCE_INDEX.md。統合台帳原文は読み取りのみとし、今回の追加資料で古い見出しと最新節の混在を解消する。正式原台帳を勝手に再判定・全文書換えしない。


## 2026-10-15T15:59:17.859823+09:00 — 是正Task開始

OwnerはPagefind限定是正と、Evidence完備・初回Freeze後の別セッションF1回までの進行を選択。Task P3-B1-REMEDIATION-20261015-01を開始。受入IDは変更せず、独立Fは未実施、G4 STOP。実開始と根拠：evidence/remediation_20261015/TASK_START.json。既存の未発注記述はこの選択前の履歴であり、次回統合時に現行表を更新する。


更新JST 2026-10-15T16:17:34.895869+09:00：A是正・不足Evidence実証、初回Freeze準備／F未開始。現行状態を本文へ統合。


2026-10-15 16:18:36 JST：初回Freeze1確定、SHA `7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75`。以後コード変更なし。別セッションF初回1回へ固定ZIPを発注。A判定をF PASSにしない。


2026-10-15T16:21:31.886293+09:00：B1-E005として公開GitHubへの新是正payload pushがauto-reviewで実行前拒否。local7a48080／非共有Drive／独立Fは継続し、今回payload特定の追加承認後に同期。過去の公開承認と成功は変更しない。


2026-10-15T16:29:30.416041+09:00 最終：初回Freeze1／独立F1を完了。F PASS_WITH_MINOR、C0/M0/Minor1。Owner受入とE005公開承認待ち。G4 STOP。
