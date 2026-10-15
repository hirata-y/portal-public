# Evidence Index — 実行・正式判断・現在管理

相対pathはこのリポジトリのルート基準。公開GitHub：<https://github.com/hirata-y/portal-public/pull/1>（Draft、未merge）。正式過去判定はS系、今回A実行はE系、管理の照合はM系。Aの検査を独立F Evidenceへ分類しない。

## 正式参照資料

| ID | 資料／取得状態 | URL・版・Hash |
|---|---|---|
| S01 | 単体Codex Work Order raw取得・SHA一致 | <https://drive.google.com/file/d/1tjjp_qGtXYPH2RVm_x-9gueHWF_Rmtbp/view>／`c4e07507987039cf7c64ba76f9da971c7fbb8d649166c506f01ee547d74dbad5`。rootのP3_B1_CODEX_A_WORKORDER.mdと回収原文 |
| S02 | Ownerレビュー収束ルール全文取得 | <https://docs.google.com/document/d/1zc58zYzGKvy5eIVN-SBMv80uEP5y4yQsYVIlB4edAmM/edit>。10/15版＋v0.2.1 addendum |
| S03 | プロジェクト統合台帳全文取得・最新節78まで照合 | <https://docs.google.com/document/d/1tlg-28kdlstQixWRPaxI1D7NVAQfBGvj7_dfRSq1734/edit>／provider modified 2026-10-15 12:23:56.838 JST。冒頭見出しは古く、§68/72/76/78を時点別に参照。Codex実行後の状態はまだ含まない |
| S04 | 環境移管正式Doc全文取得 | <https://docs.google.com/document/d/1xWOth352RCyzFMSd3nrG211CYG5ol06bEHA4ZCR0njQ/edit>。当時Codex未開始は履歴、今回の実行済みを否定しない |
| S05 | Handoff kit raw取得・SHA/8 entries確認 | <https://drive.google.com/file/d/1RGH2dDbCsLpWTs0615YXGH0io0Q821G8/view>／`698431cd189234fb5ea7dd0424b6543ef21c15091b71b31a843afcb41ebea666`。nested vendor ZIPは現入力と全バイト一致 |
| S06 | P2 H正式G3原票への参照 | <https://drive.google.com/file/d/114RXxu5yTpM2KoMoaGSAwokcWMM0-EYD/view>。今回原票raw再取得は未実施、S03 §68/69の正式判定記録で照合 |
| S07 | P3-A F正式原票への参照 | <https://docs.google.com/document/d/12kV4VFZncdyV0maE4SKTezGVt0ryNyMIjUqZpTaJRTg/edit>。今回原票全文再取得は未実施、S03 §73〜76でVerdict確認 |
| S08 | 既存管理ファイル6点を追加読取・統合 | PROJECT、PROGRESS、P1_COMPLETION、P1_OWNER_DECISION_AND_CHIEF_STATUS、PROJECT_STATUS_AND_RESPONSES、REVIEW_CONFIGURATION。source参照JSONにID/版を保持。P1正式完了保留の旧判断Aと後発K2を別扱い |

参照した内部原台帳121,711文字・原Doc本文はローカル別領域で読取り。公開repoや管理ZIPにその全文や実Owner画像を複製しない。今回の根拠URL・版・要約・local export hashのみmanagement/SOURCE_REFERENCES.jsonで追跡する。

## 今回の是正Evidence

- R01 `evidence/remediation_20261015/TASK_START.json`：Owner2回答・実開始・入力SHA。
- R02 17_final_build / 18_final_index json/log：Astro／Pagefind exit0。公開13ページ・338語・26索引file＋219語辞書。
- R03 `browser/`：headful33 PASS、実日本語3照会、8枚のnative URLバー画面、performance。A自己検査。
- R04 `remediation_checks.json`：20照会・検索click・XSS・主要link・形式GET・Console/Network・不正asset等62 PASS。
- R05 `adapter_negative.json`：32候補制限、private fragment拒否、vendor26file同一bytesの3 PASS。
- R06 `security_formats.json`25 PASS、`index_fault_injection.json`実汚染index検出PASS。
- R07 `dependency_inventory.json`全lock267件／欠落0、08_npm_audit exit0／既知脆弱性0、`comparison_metrics.json`。
- R08 `EXPERIMENT_NOTES.md`、初期失敗JSON・10/12ログ：未成功を保持。最終PASSだけに履歴を塗り替えない。
- R09 ADR002、是正Handoff。正式Freezeの正本ManifestはFREEZE1_MANIFEST.json。旧MANIFEST.jsonは前版時点の歴史資料。
- R10 独立F原票：evidence/independent_f_20261015/F_OUTPUT/REVIEW.md、SUMMARY.json。110PASS/1FAIL、C0/M0/Minor1。原票はそのまま保管。
- R11 独立F ZIP：artifacts/P3_B1_FREEZE1_F_REVIEW_20261015.zip、SHA17f9f82f39b5e0aaced7ee64ac6fc35f78b02ee4c7bc08b361cd14ccae5aa5a3、1,841,404B、115entries。Drive非共有raw照合一致 <https://drive.google.com/file/d/1lIsakOpBeLXedmF0ODV3cVr3Nbhv3HXI/view>。
- R12 Freeze1 ZIP：5,403,706B/399entries、SHA7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75。Drive非共有raw照合一致 <https://drive.google.com/file/d/1-R__3zV-6GBROgvb4Nv4nwaCqooAPtQJ/view>。
- R13 後発管理：management/REMEDIATION_PUBLICATION_RECEIPT.json、management/evidence/remediation_acceptance_current.json、post_freeze_scope.json、今回進捗報告。製品コード・索引はFreeze以後変更なし。

## 前回A実行成果と検査（版固定の履歴）

| ID | 内容 | 実ファイル／結果 |
|---|---|---|
| E01 | 実行スナップショットZIP・SHA | `artifacts/P3_B1_A_EXECUTION_SNAPSHOT_20261015.zip`／`1e0b42cdeb5f08686df09ca2f0d5a95a2cdbd9abc4728d29326b12952e11e8d9`、2,477,711B、269entries。<https://drive.google.com/file/d/1PAOABAdyxf7gmdv8ORjoD1GLNor6tlHE/view>。Drive raw readback一致 |
| E02 | 入力vendor v0.2.1 ZIP | `source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip`／`a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9`、184006B、88entries |
| E03 | package-lock／実依存 | `astro_candidate/package-lock.json`／`dd957c01dc054952d911b48cff783e62c500d83d5d06898d730fba46faac5117`、Astro7.3.8/Pagefind1.5.2。22_npm_ci.json exit0 |
| E04 | 実ビルド／索引 | `evidence/vendor_actual/23_final_build.json` exit0／24_final_index.json exit0。13HTML/338words/26索引ファイル |
| E05 | dist受入 | `evidence/vendor_real_dist_checks.json`／25_final_dist.json、42 PASS |
| E06 | 固定ベースライン | `evidence/test_expected_actual.json`／28_final_baseline.json、59 PASS。実vendor判定をこのsuite単独から推定しない |
| E07 | 分離・形式・source同一性 | `evidence/vendor_actual/security_formats.json`／26_final_security.json、25 PASS。元source16ファイルは入力と同一 |
| E08 | 実故障索引 | `evidence/vendor_actual/index_fault_injection.json`／27_final_index_fault.json PASS。quoted canary0でもprivate route/decoded contentを検出 |
| E09 | Chromium統合 | `evidence/vendor_actual/browser/browser_report.json`／29_final_browser.json、32 PASS/1 FAIL、実URL／UTC／8 PNG |
| E10 | 日本語検索／DLした実JSON | `evidence/vendor_actual/browser/japanese_search.json`／P3_B1_Pagefind_Japanese_Actual_Browser_Result.json。谷川TGW001/002、奥多摩0、穂高岳0。2 PASS/1 FAILはE09に内包 |
| E11 | 原因・限定比較 | `evidence/vendor_actual/search_diagnostics.json`、segmentation_probe.json、previous_minor.json。1.4.0でも不一致 |
| E12 | 4形式／レンダリング | `astro_candidate/dist/fixtures/synthetic_format.*`、`evidence/vendor_actual/formats/`のPDF／PPTX／XLSX PNG、office_render_checks.json。入力にある実specimenをコピー・解析・Office変換した。4形式新規生成コードの実証ではない |
| E13 | 性能／環境 | `evidence/vendor_actual/comparison_metrics.json`、browser/performance.json、runtime.json、environment_prerequisites.json。生timingとCLI時間を保持 |
| E14 | 不変payloadと後発公開 | `MANIFEST.json`：268payloadのSHA、旧ZIP269entries。`PUBLICATION_RECEIPT.json`：Drive readbackと明示Owner公開承認後のpush／Draft PR成功。旧GitHub BLOCKEDを現状態と誤読しない |

完全元P2 ZIP pin：`c1969c801dc47cb15636ce1a74da13433d13ddccf03f308895828ef3d8632f6f`。完全元P3-A ZIP pin：`bc17d7d10b60433754732598a0d2b781eadb337da7b4a80dd8613c79a81c3a23`。今回完全ZIPのraw再計算はしていない。S03では以前の正式検算記録があり、今回Aの直接確認はE02内source16ファイルのバイト一致。証拠階層を混同しない。

## 今回の管理Evidence

| ID | 内容 | 所在・注意 |
|---|---|---|
| M01 | 4入力回収・読了・nested入力一致 | `management/evidence/input_recovery.json`、`management/input-recovery/`の4原文。実行前に読んだとはしない |
| M02 | 実行ログ集計と未実施の照合 | `management/evidence/reconciliation.json`。160assertion=159/1、22受入管理項目=12PASS/1FAIL/2BLOCKED/7NOT_EXECUTED。二つの母数を加算しない |
| M03 | 現PR readback／source参照 | `management/evidence/github_pr_readback.json`、management/SOURCE_REFERENCES.json |
| M04 | 9節詳細報告／Coordinator引継ぎ | `management/P3_B1_PROGRESS_REPORT_20261015.md` |
| M05 | 今回管理パック・Manifest・SHA・読戻し | `management/STATUS_MANIFEST.json`、`artifacts/P3_B1_STATUS_MANAGEMENT_20261015_v1.0.2.zip`、SHA sidecar。Drive保存先・readback結果はmanagement/PUBLICATION_RECEIPT.json。旧E01や公式Freezeを置換しない |

## 前報告時点の非実施根拠（今回R系の後発実証を優先）

該当するログ／コードのassertionがない項目はNOT_EXECUTED。ブラウザpageerror=[]は包括Console/Network検査やXSS負試験を意味しない。Fの旧版87PASSはB1の独立PASSではない。未実施GateとOwner受入は実行済みassertion件数へ混ぜない。

今回管理資料の公開GitHub同期はB1-E004として一旦停止したが、別Owner明示追加承認後のpush成功で解消。PR #1に現在の管理資料も同期。v1.0.1は承認前履歴、v1.0.2が承認反映後。Driveの7Markdownと旧PROGRESSは所有者一致・非共有を確認して保存／raw読戻し済み。


## 2026-10-15T15:59:17.859823+09:00 — 是正Task開始

OwnerはPagefind限定是正と、Evidence完備・初回Freeze後の別セッションF1回までの進行を選択。Task P3-B1-REMEDIATION-20261015-01を開始。受入IDは変更せず、独立Fは未実施、G4 STOP。実開始と根拠：evidence/remediation_20261015/TASK_START.json。既存の未発注記述はこの選択前の履歴であり、次回統合時に現行表を更新する。


更新JST 2026-10-15T16:17:34.895869+09:00：A是正・不足Evidence実証、初回Freeze準備／F未開始。現行状態を本文へ統合。


2026-10-15 16:18:36 JST：初回Freeze1確定、SHA `7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75`。以後コード変更なし。別セッションF初回1回へ固定ZIPを発注。A判定をF PASSにしない。


2026-10-15T16:21:31.886293+09:00：B1-E005として公開GitHubへの新是正payload pushがauto-reviewで実行前拒否。local7a48080／非共有Drive／独立Fは継続し、今回payload特定の追加承認後に同期。過去の公開承認と成功は変更しない。


2026-10-15T16:29:30.416041+09:00 最終：F原票・CandidateとF ZIPのDrive raw検算成立。今回GitHub同期のみE005で追加承認待ち。旧PRリンクの製品状態を現行と取り違えない。


## Owner受領・今回公開成功（後発）

- R14 management/OWNER_ACCEPTANCE_PUBLICATION_20261015.json：Owner2回答原文、B1条件付き受領／Minor backlog、公開対象commit57f5f20。
- R15 evidence/remediation_20261015/23_owner_approved_push.json/.log：git push exit0、9465776→57f5f20。今回E005の公開阻害を解消。
- 既存Freeze1・F原票・ZIP／過去管理ZIPは不変。以後の管理スナップショットはOwner処置を反映する追補で、新Candidate Freezeではない。
