# 現在のFinding台帳

原Findingの時点記録はdocs/FINDINGS.jsonと元実行ZIPに保存し、変更しない。このファイルが現在の状態遷移を管理する。Aの重要度／是正判定は独立FのVerdictではない。単純なFinding件数多数決で受入／Gateを決めない。

| ID | 重要度／区分 | 原因・期待／実測 | 是正と担当 | 現在状態 | 再検証／close条件・期限 |
|---|---|---|---|---|---|
| B1-M001 | Major／A製品・統合 | 奥多摩の索引は奥多＋摩、ブラウザは奥多摩。期待OKU-001/002、実測詳細0。1.4.0でも再現 | A。Vanilla保持・Pagefind採用保留。語の表示補正実験は不成功でrevert | OPEN／独立Severity未判定 | Owner方針→必要な局所是正→新Candidate→F。10/17 12:41 JSTは48h提案に過ぎず正式期限ではない |
| B1-M002 | Major／Aソース | Astroがpublicのscript srcを処理しapp.js解決不能 | 3scriptにis:inline、順序と元JS bytesを保持 | A_VERIFIED_FIXED／F_PENDING | 実build0・既存UIのA試験済み。別Fの差分確認まで独立closeにしない |
| B1-M003 | Major／Aテスト配布境界 | 公開用probe自身に合成限定カナリアがありbyte scan FAIL | probeから除去、照会は外部テストコード側へ。raw/gzip/content/URL共通scanner、4mutation、実故障索引 | A_VERIFIED_FIXED／F_PENDING | 正常distと故障索引に同一scanner。別Fで限定再検証 |
| B1-M004 | Major／A検証方法 | 汚染索引でもquoted canary0、正常索引で無引用8hit。照会0件のみは分離証明にならない | queryは参考とし、生成入力・decoded fragment・route・faultを判定根拠へ変更 | A_VERIFIED_FIXED／F_PENDING | 実故障索引でprivate URL/decoded content検出済み。別F未実施 |
| B1-E001 | Major／入力手続 | 前Task開始時4入力不在、別の正式Docで実行。今回指定キット内に発見 | Aがkit SHA・単体WO SHA・nested ZIP同一性を確認、4原文回収・読了 | RECOVERED_RECONCILED_A_ONLY／手続差異評価待ち | 不在という現行物流阻害は解消。実行前未読の履歴は残る。回収WOに照らした不足をB1-Q001へ。F／Coordinatorが影響判定 |
| B1-E002 | Minor／環境 | npm接続EPERM、Astro設定書込み、動画ffmpeg不足 | 許可networkで接続、telemetry無効、実Chromium PNG＋URL/時刻JSON | A_RESOLVED／GUI制約継続 | NativeURLバー・Windows/Edge Evidenceは未実施のまま |
| B1-E003 | Major／公開権限 | 初回pushは自動承認レビュー拒否 | Ownerが明示追加承認しpush・Draft PR #1成功 | AUTHORIZATION_RESOLVED | PUBLICATION_RECEIPTと現PR readback。旧ZIP中のBLOCKEDは過去状態で再openしない |
| B1-E004 | 管理公開承認／Severity未査定 | 今回管理資料のpublic GitHub pushがauto-reviewで拒否 | Aはローカル／非共有Driveへ保存後、別Owner追加承認を受け公開同期 | AUTHORIZATION_RESOLVED | 具体的な管理パックの追加承認とpush成功。B1-M001や元PoC公開成功とは別 |
| B1-Q001 | 受入Evidence不足／Severity未査定 | 回収WO要求の一部に実行ログがない | Aの次Taskで未収集分のみ。検索結果click→detail、明示XSS、包括Console/Network、license依存確認、nativeGUI等 | NOT_EXECUTED／受入未完 | 管理22項目表AC14〜18。既に成功したbuild等の重複発注ではない。新規実行は未開始 |
| P3-F-BLK-001／CT04 | 歴史的独立F BLOCKED／受入阻害 | P3-A Fのnative localhost navigationがERR_BLOCKED_BY_ADMINISTRATOR | Owner UATは緩和Evidence。B1 A headlessHTTPは追加の自己証拠 | F正式BLOCKED維持／独立native未確認 | 元FをPASSにせず、Router選定別Fで実HTTPと履歴を検証。G4 STOP |

## 件数の読み方

原A台帳7件＝Major6・Minor1という当時の自己分類。現在は製品Major OPEN1、A是正済みF待ち3、入力回収済み手続評価待ち1、公開権限解消1、環境是正1。今回のEvidence不足はB1-Q001として明示するが、独立Reviewerの新Major確定と偽らない。P3-AのF指摘は別版・別Roleの継承で、B1独立レビュー件数に足さない。

## 継続ルール

新FindingはID・版SHA・Role・severity・根因・expected/actual・Evidence・影響範囲・担当・期限・回数・予算影響を記録。是正には新差分と正負試験を添付。重大未解消をPASSにせず、独立closeには別Fの根拠とCoordinator処置が必要。Minorも安全／受入条件を破る場合は単なるBacklogへ押し出さない。48hと2回はOwner未確定の提案値。期限接近・工数超過見込みは追加見積りを出し、無限再レビューをしない。
