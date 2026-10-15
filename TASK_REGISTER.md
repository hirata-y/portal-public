# Task台帳 — 実行済みと未発注提案を分離

現在位置はPROJECT_STATUS.md。Task IDは既存正式IDを保持。今回の報告IDと末尾の提案IDはAの管理付番で、Owner発注・内部サービスUUIDではない。表の「実行完了」は受入／レビュー／Gate合格を意味しない。

## 現行契約

Ownerの後発回答により、当初提案の検索方針決定・限定是正・不足Evidence・Freeze後F1回の順に進行を承認。作業推計はA2〜4h＋A1〜2h＋F1〜2h相当。実人時／料金／16h残余を意味せず、追加範囲・超過見込みが生じれば再見積りする。期限は新たに固定されていない。

Aの対象・expected IDsは当初案を維持。独立Fは未Freezeでは開始せず、別セッションへ実ZIP SHAを固定して1回発注する。Coordinator／OwnerのB1受入とB2開始は未承認。

## 履歴と現在

| Task ID | Phase／担当 | 実開始／終了（JST） | 状態・結果 | 依存／次の条件 |
|---|---|---|---|---|
| H-P2-G3-V116-ONE-GATE-20261015-01 | P2／H | 正式台帳は2026-10-15。詳細時刻は本報告で未照合 | 正式G3 GO WITH CONDITIONS、レビュー工程終了。K2狭義CLOSE適用 | §68を維持し、Owner CP3判断と後続CTを継承 |
| P3-A v0.1.0 A制作Task（正式ID本報告で未照合） | P3-A／A | 2026-10-15、詳細人時未測定 | 公式Freeze1、Owner local/synthetic条件付き受入 | 元F BLOCKED／CT04を維持 |
| P3-F-LOCAL-HYBRID-ONE-REVIEW-20261015-01 | P3-A／独立F | 台帳上の完了2026-10-15 10:29:10.971927 | BLOCKED、87 PASS/0 FAIL/1 BLOCKED/3 NOT_EXECUTED | 独立native HTTPの不足をCT04へ移管。今回再実行なし |
| P3-OWNER-UAT-FIXED-V010-20261015-01 | P3-A／Owner | Owner申告2026-10-15 11:07:48 | Owner UAT reported PASS、local/synthetic受入の根拠。F PASSではない | 独立性・native200%等の残条件を維持 |
| P3-B1-REAL-VENDOR-POC-20261016-01 | P3-B1／Codex A | 記録開始10/15 12:37:34.201228、最終vendor検査終了12:46:42.640330、公開receipt12:54:08.863799 | EXECUTION_COMPLETED_WITH_FAIL。Astro build／ja index成功。M001 OPEN。公式Freeze0/F0 | 本実測を受けたOwner方針決定、残Evidence、正式Candidate後のF |
| P3-B1-REMEDIATION-20261015-01 | P3-B1／A | 10/15 15:59:17.859823〜継続 | Ownerが限定是正・不足Evidence・初回Freeze後別F1回を選択。A全suite PASS、Freeze準備 | 同一Candidate SHA→別F→Owner受入。G4 STOP |
| P3-B1-STATUS-INTEGRATION-20261015-01 | P3-B1／Codex A | 10/15報告作業。本Task全体開始時刻は未計測、管理資料の時刻は個別記録 | 6資料整備・既存ログ照合・4入力回収。保存結果は管理receipt。製品実装／レビューなし。新管理資料も別Owner追加承認後に公開GitHub同期済み | Coordinatorへ受領・統合依頼。次の実装は未発注 |

前Taskの管理計画は10/16〜18 JST・合算16h相当（A/F/統合の目標）。実際には10/15に実行した。記録開始から最終vendor検査終了548.439102秒＝機械・操作のwall clockであり、人の実工数ではない。準備開始時刻、人時、16h枠の使用量／残余は未測定。待機・会話間の経過を作業時間としない。

## 当初の次Task契約案 — Owner選択前の履歴

既に成功したインストール・build/index・既存テスト全体を新規Taskとして重複発注しない。差分がないPASSは固定Evidenceを再利用し、変更で影響する部分を再検証する。

### 優先1：P3-B1-DISPOSITION-01／検索方針・是正枠のOwner決定

- Phase／Role：P3-B1／Owner＋Coordinator。Aは実測資料を説明。
- 目的・範囲：M001の是正継続か、Vanilla維持に伴うB1受入契約の明示変更かを選ぶ。期限・追加上限・役割・残条件を確定。
- 入力・固定SHA：E01実行ZIP `1e0b42cdeb5f08686df09ca2f0d5a95a2cdbd9abc4728d29326b12952e11e8d9`、ADR、FINDINGS_REGISTER、回収Work Order `c4e07507987039cf7c64ba76f9da971c7fbb8d649166c506f01ee547d74dbad5`。最新管理ZIPはmanagement/PUBLICATION_RECEIPT.jsonで固定。
- 作業：実測の受領、2選択肢と受入影響の確認、Task責任・日程・予算枠・Freeze前条件を決定。
- 成果物：Owner Decisionと承認済みTask Contract、DECISION_LOG／TASK_REGISTER更新。
- 受入基準：選択と適用範囲・担当・期限・上限が文面で確定。Pagefind期待値をAが勝手に変更しない。未決ならHOLD。
- テスト／独立レビュー：本決定自体は製品テストではない。契約変更はPROC04の影響地点をRouterが指定。
- 先行依存：今回の進捗報告受領。
- リスク・STOP：Vanilla維持を現Pagefind条件の自動PASSと扱うこと、重大事項の黙殺。
- 見積・優先度：0.25〜0.5h相当、P0優先（管理見積り）。
- Owner承認：Owner自身の正式判断が必要。今回は未決。

### 優先2：P3-B1-JA-REMEDIATION-01／M001限定是正（選択された場合のみ）

- Phase／Role：P3-B1／A Producer。
- 目的・範囲：索引／照会の日本語分割不一致を、許可された方式で解消。固定8レコード・原ソース・既存構造化検索を保持。
- 入力・固定SHA：上記E01 ZIP、入力vendor ZIP `a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9`、lock `dd957c01dc054952d911b48cff783e62c500d83d5d06898d730fba46faac5117`、diagnostics／previous_minor／segmentation JSON。
- 作業：Ownerが選択した設計で分割整合を実装し、実vendor index／browser照会、変更に影響する正負試験を実行。特定の「奥多摩」だけを例外補正して合格させない。
- 成果物：限定差分、固定lock、新実測JSON、原因と検証範囲、変更影響表。元ZIPは不変。
- 受入基準：谷川TGW-001/002、奥多摩OKU-001/002、穂高岳0を実生成クライアントで再現し、合意した代表日本語コーパスでも照会・索引の整合を確認。8件・3テーマとAND/OR/null意味を保持。FAILはFAILとして提出。
- テスト／独立レビュー：A差分回帰／正負・mutation。正式Candidate後、優先4の別Fへ回す。自己PASSは独立closeではない。
- 先行依存：優先1の是正選択と予算／期限承認。
- リスク・STOP：vendor内部の無根拠パッチ、期待ID変更、範囲外データ、重大事項未解消、見積超過見込み時はOwnerへ提示。
- 見積・優先度：A 2〜4h相当、P1優先。実人時ではない。
- Owner承認：次Task正式化と追加枠の明示判断待ち。新実装未開始。

### 優先3：P3-B1-CANDIDATE-COMPLETION-01／未収集Evidenceと初回Freeze

- Phase／Role：P3-B1／A。新製品機能の追加ではなく受入証拠の完備。
- 目的・範囲：回収Work Orderとの不足照合で確認した未実施分を埋め、公式Freeze可能なCandidateへまとめる。
- 入力・固定SHA：E01、回収Work Order上記SHA、優先2の新差分SHAまたはOwner契約変更記録、22受入管理項目表。
- 作業：検索結果クリック→詳細、明示XSS非実行負例、Console/Networkの必要範囲、ライセンス・依存の確認を実行。必要なnativeブラウザURL Evidenceを取得し、入力回収後の契約差異を記録。既存4形式・フィルタのPASSは変更影響がない限り再利用。
- 成果物：不足Evidence、残項目の明確なPASS/FAIL/BLOCKED/NOT_EXECUTED、新Manifest／ZIP／SHA、成立時のみ初回公式Freeze。
- 受入基準：合意したB1契約に未評価項目が残らず、重大受入阻害を解消または正式契約判断で処置し、入力・lock・出力・ログ・差分・ブラウザEvidenceを同一Candidateへ固定。NOT_EXECUTEDをPASSに置換しない。
- テスト／独立レビュー：不足チェックと是正影響範囲のみA実行。Freezeの後に優先4。
- 先行依存：優先1、必要なら優先2。native環境利用と追加枠。
- リスク・STOP：未実行のlicense/XSS/GUIを完了扱い、元入力未読を遡及修正、Evidence不足のままFreeze。
- 見積・優先度：A 1〜2h相当、P1優先。環境準備時間は含まず、必要なら再見積り。
- Owner承認：次Task契約・追加範囲と上限の判断待ち。

### 優先4：P3-B1-F-INDEPENDENT-01／初回の独立限定レビュー

- Phase／Role：P3-B1／Review Router選定の別セッションF。Aが兼任しない。
- 目的・範囲：M001〜M004と回収入力差異、影響する検索・フィルタ・分離・HTTP navigation/Back/Forwardを独立評価。CT04の独立実HTTP証拠を取得。
- 入力・固定SHA：優先3で作る公式Candidate SHA／Manifestを発注時に固定（現時点未発行。仮SHAを創作しない）、旧E01の比較根拠。
- 作業：同一SHA確認、本人のテスト・故障注入・ブラウザ実測、Expected/Actual・独立Verdict提出。必要外の全C/E/F/G再レビューはしない。
- 成果物：F原コード・ログ・画面・結果JSON・Finding・VerdictとDrive readback。
- 受入基準：PASS／FAIL／BLOCKEDを根拠付きで確定。TaskはFAILでも実行完了になり得るがCandidate受入合格とはしない。重大closeはVERIFY根拠と役割分離を要する。
- テスト／独立レビュー：このTask自身が初回F 1回。重大事項の是正後は当該差分だけ限定再検証。
- 先行依存：初回公式Freeze、Router発注、FのHTTPブラウザ環境。未Freezeの現在は開始しない。
- リスク・STOP：F環境BLOCKED、別版入力、A自己テストの転記、元P3-A BLOCKEDの改ざん。
- 見積・優先度：F 1〜2h相当、P2優先。前回0.5〜1h案から、回収Work Orderの未収集分と独立native確認範囲を踏まえた提案更新。Owner未承認。
- Owner承認：通常1回枠の原則は既決、具体Task／範囲／予算・Router選定は正式化待ち。

### 優先5：P3-B1-COORD-HANDOFF-01／B1受入・次工程境界の統合

- Phase／Role：P3-B1／Coordinator・必要Gate担当・Owner。
- 目的・範囲：AとFの結果を分けて受領し、B1受入、残リスク、P3-B2の別契約判断材料へ統合。
- 入力・固定SHA：公式Candidate、F Evidence SHA、Decision、CT01〜07台帳。未発行分は開始前に固定。
- 作業：Finding照合、重大事項の処置、Owner受入可否、B2の範囲／権限／停止条件案を整理。
- 成果物：Coordinator disposition、Owner受入／HOLD決定、次工程Task案。
- 受入基準：重大未処置のままGOにしない。B1受入を実認証・本番配備・G4 GOに読み替えない。CT04等の責任・期限・Evidenceが追跡可能。
- テスト／独立レビュー：重複の製品テストを自動再実行せず、F結果と正式条件を統合。必要な正式Gateはその権限者へ。
- 先行依存：優先4のVerdictと重大Finding処置。
- リスク・STOP：B2自動着手、Owner代行、予算残余の捏造。
- 見積・優先度：0.25〜0.5h相当、P3優先。
- Owner承認：B1受入とB2開始は別判断。未承認。

## 新見積りの扱い

上記5Taskをすべて採る場合は合計4.5〜9h相当の管理推計。これは新たな作業範囲の提案であり、既存16h枠の「残り」や追加発注済み工数ではない。Vanilla維持の契約変更を選ぶ場合、優先2は未発注のまま不要となり、影響を再見積りする。予定日・正式期限はOwner確定までTBD。48h・2失敗サイクルは提案値のまま。


## 2026-10-15T15:59:17.859823+09:00 — 是正Task開始

OwnerはPagefind限定是正と、Evidence完備・初回Freeze後の別セッションF1回までの進行を選択。Task P3-B1-REMEDIATION-20261015-01を開始。受入IDは変更せず、独立Fは未実施、G4 STOP。実開始と根拠：evidence/remediation_20261015/TASK_START.json。既存の未発注記述はこの選択前の履歴であり、次回統合時に現行表を更新する。


更新JST 2026-10-15T16:17:34.895869+09:00：A是正・不足Evidence実証、初回Freeze準備／F未開始。現行状態を本文へ統合。


2026-10-15 16:18:36 JST：初回Freeze1確定、SHA `7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75`。以後コード変更なし。別セッションF初回1回へ固定ZIPを発注。A判定をF PASSにしない。
