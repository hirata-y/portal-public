#!/usr/bin/env python3
import json,hashlib,statistics,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R/'evidence/vendor_actual';D=R/'docs'
J=lambda p:json.loads((R/p).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
size=lambda p:sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
perf=J('evidence/vendor_actual/browser/performance.json');runtime=J('evidence/vendor_actual/runtime.json');browser=J('evidence/vendor_actual/browser/browser_report.json');search=J('evidence/vendor_actual/browser/japanese_search.json')
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat();start=datetime.datetime.fromisoformat(runtime['started_at']);testend=datetime.datetime.fromisoformat(browser['end_utc']);elapsed=(testend-start).total_seconds()
metrics={'vanilla_public_bytes':size(R/'outputs/public'),'astro_dist_bytes':size(R/'astro_candidate/dist'),'pagefind_bytes':size(R/'astro_candidate/dist/pagefind'),'common_js_bytes':sum((R/'source/p3_a_site'/n).stat().st_size for n in ['app.js','demo-data.js','data-validation.js']),'vanilla_init_median_ms':perf['vanilla']['median_wall_to_8_results_ms'],'astro_init_median_ms':perf['astro']['median_wall_to_8_results_ms'],'pagefind_query_cold_ms':perf['pagefind_query'][0]['ms'],'pagefind_query_warm_median_ms':statistics.median(x['ms'] for x in perf['pagefind_query'][1:]),'substring_10000_total_ms':perf['vanilla_query']['total_ms'],'build_wall_seconds':J('evidence/vendor_actual/23_final_build.json')['duration_seconds'],'index_wall_seconds':J('evidence/vendor_actual/24_final_index.json')['duration_seconds']}
(E/'comparison_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
findings=[
 {'id':'B1-M001','severity':'Major','kind':'product/integration','status':'OPEN','trigger':'Pagefind 1.5.2 Extended: Japanese query 奥多摩','expected':['SYN-OKU-001','SYN-OKU-002'],'actual':[],'cause':'Generated Japanese fragment uses 奥多 + 摩; Chromium Intl.Segmenter uses 奥多摩. Raw client/index segmentation differs.','impact':'Pagefind cannot replace the existing keyword search under current acceptance criteria. Vanilla UI is intact.','evidence':['evidence/vendor_actual/browser/japanese_search.json','evidence/vendor_actual/search_diagnostics.json','evidence/vendor_actual/segmentation_probe.json','evidence/vendor_actual/previous_minor.json'],'owner':'A; Review Router selects independent F','remediation':'No test expectation relaxed. Reproduced on 1.4.0; visible area labels did not correct the mismatch and were reverted. Defer Pagefind adoption pending a bounded segmentation design or explicit acceptance-contract decision.','proposed_due_jst':'2026-10-17T12:41:00+09:00','due_note':'48h proposed planning allowance after first observed failing probe at approximately 2026-10-15 12:40:57 JST, not an Owner-approved deadline or background schedule.','estimate':'Additional A 2–4h + independent F 0.5–1h, estimate only; no background work or billing assumed.'},
 {'id':'B1-M002','severity':'Major','kind':'source','status':'A_VERIFIED_FIXED_F_PENDING','trigger':'Astro build of unmodified HTML scripts','expected':'build exit 0','actual_before':'Rolldown cannot resolve app.js; exit 1','cause':'Astro processes script src by default; assets live in public/.','correction':'Add is:inline to the three existing external script tags, preserving script order and copied bytes.','evidence':['evidence/vendor_actual/03b_astro_build.json','evidence/vendor_actual/23_final_build.json','evidence/vendor_actual/browser/browser_report.json']},
 {'id':'B1-M003','severity':'Major','kind':'test-artifact boundary','status':'A_VERIFIED_FIXED_F_PENDING','trigger':'Copy the readiness browser probe into dist','expected':'public dist contains no member canary bytes','actual_before':'The probe itself embeds the private synthetic canary; dist scanner exit 2.','correction':'Remove the literal from the public browser probe; inject diagnostic queries from external A test code. Use one scanner for raw/gzip/decoded Pagefind content and private URLs plus four temp mutations and a real fault-built index.','evidence':['evidence/vendor_actual/05_dist_acceptance.json','evidence/vendor_actual/26_final_security.json','evidence/vendor_actual/index_fault_injection.json']},
 {'id':'B1-M004','severity':'Major','kind':'verification method','status':'A_VERIFIED_FIXED_F_PENDING','trigger':'Use only Pagefind canary zero-result query as isolation evidence','expected':'fault injection must be detected','actual_before':'An exact quoted canary query returns 0 even in a fault-built index containing members/canary.html; unquoted normal corpus query can return 8 public pages.','correction':'Treat query count as informational. Verify decompressed fragment content/URLs, public routes and build inputs; actual fault index is detected by the same scanner.','evidence':['evidence/vendor_actual/21_index_fault_exact.json','evidence/vendor_actual/index_fault_injection.json','evidence/vendor_actual/browser/canary_search.json']},
 {'id':'B1-E001','severity':'Major','kind':'input prerequisite','status':'BLOCKED','expected':'AGENTS.md, START_HERE.md, P3_B1_CODEX_A_WORKORDER.md, CODEX_EXECUTION_STATE.json present before work','actual':'All four absent from empty checkout, /workspace file inventory and the 88-entry input ZIP.','action':'Asked for location asynchronously; used user-linked formal Work Order and SHA-verified input for independent executable work. Do not claim the missing instructions were read. Formal freeze remains withheld.','estimate':'Recover and reconcile inputs: 0.25h estimate.'},
 {'id':'B1-E002','severity':'Minor','kind':'environment','status':'A_RESOLVED','actual_before':'Default sandbox npm connect EPERM; Astro telemetry cannot write /home/agent/.config/astro; Playwright video ffmpeg unavailable.','correction':'Use granted network permission; disable Astro telemetry per process; capture actual Chromium screenshots and URL/time JSON instead of video.','remaining':'Headless captures do not include native address-bar chrome. Windows/Edge GUI and address-bar evidence NOT_EXECUTED.'},
 {'id':'B1-E003','severity':'Major','kind':'external write authorization','status':'BLOCKED','trigger':'git push -u origin main','actual':'Automatic approval review rejected GitHub public write because Owner additional approval against the formal Work Order prohibition was not established. Command was rejected before execution.','action':'No alternate write path attempted. Prepare local commits, runnable ZIP and Git bundle. Obtain explicit Owner approval for push and draft PR.','evidence':['docs/GITHUB_PUBLICATION_BLOCKED.md']}
]
(D/'FINDINGS.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n')
state={'task_id':'P3-B1-REAL-VENDOR-POC-20261016-01','role':'A Producer','generated_jst':now,'recorded_execution_start_jst':runtime['started_at'],'vendor_test_end_jst':testend.astimezone(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),'recorded_execution_elapsed_seconds_to_test_end':elapsed,'actual_human_effort_hours':None,'input_zip_sha256':runtime['input_sha256'],'input_zip_bytes':184006,'input_zip_entries':88,'package_lock_sha256':sha(R/'astro_candidate/package-lock.json'),'versions':{'node':'24.19.0','npm':'11.9.0','python':'3.12.14','astro':'7.3.8','pagefind':'1.5.2 Extended','chromium':browser['browser']},'results':{'npm_ci':'PASS','astro_build':'PASS','pagefind_ja_index':'PASS','dist_checks':J('evidence/vendor_real_dist_checks.json')['summary'],'baseline_checks':J('evidence/test_expected_actual.json')['summary'],'security_formats':J('evidence/vendor_actual/security_formats.json')['summary'],'browser':browser['summary'],'japanese_search':search['summary'],'real_index_fault_detection':J('evidence/vendor_actual/index_fault_injection.json')['status']},'official_candidate_freeze':'NOT_PERFORMED','official_freezes_consumed':0,'independent_F':'NOT_EXECUTED','historical_P3A_F':'BLOCKED retained','G4':'STOP','B2':'NOT_STARTED','github':'PUSH_BLOCKED_BY_AUTO_REVIEW; local artifacts prepared','unverified':['Missing four priority local input files','Windows/Edge native GUI/address-bar evidence','Independent F CT04 and targeted recheck','Full original P2/P3-A ZIP hashes: pins only; extracted source subtree verified','Production authorization/JWT/Access and delivery','Microsoft Office desktop interoperability','Production dependency audit/full WCAG/AT'],'scope':'Local loopback and synthetic artifacts; current user authorizes GitHub management but automatic approval review requires explicit Owner approval.'}
(R/'EXECUTION_STATE_RESULT.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
adr=f'''# ADR-001 — Astro実行可、Pagefind日本語検索の採用保留

決定状態：Aによる技術採用提案。Owner／独立F未承認。G4 STOP。{now}

既存Vanillaの検索・フィルタを維持する。Astro 7.3.8は静的生成の技術候補として継続可能。Pagefind 1.5.2 Extendedは現在の日本語検索受入条件を満たさず、置換採用を保留する。既存UIにはPagefindを接続していない。

## 実測

Linux / Node 24.19.0 / npm 11.9.0 / Chromium 154。127.0.0.1の同一マシン、各10 fresh contexts、通信・CPU制限なし。初期化時間はnavigation開始から8結果表示を観測するまでのPlaywright wall clock。順序はVanilla→Astroで交互無作為化しておらず、差は性能優位の根拠にしない。

| 項目 | Vanilla HTML/JS | Astro + Pagefind |
|---|---:|---:|
| 配信用総バイト | {metrics['vanilla_public_bytes']:,} | {metrics['astro_dist_bytes']:,} |
| Pagefind追加出力 | 0 | {metrics['pagefind_bytes']:,}（26ファイル） |
| 既存共通JS | {metrics['common_js_bytes']:,} | 同一バイト |
| 8件表示までの中央値 | {metrics['vanilla_init_median_ms']:.1f} ms | {metrics['astro_init_median_ms']:.1f} ms |
| ビルドwall time | 必須ビルドなし | {metrics['build_wall_seconds']:.3f} s |
| 日本語索引wall time | なし | {metrics['index_wall_seconds']:.3f} s |
| 「谷川」の詳細ID | TGW-001 / TGW-002 | TGW-001 / TGW-002 |
| 「奥多摩」の詳細ID | OKU-001 / OKU-002 | 0件：FAIL |
| 「穂高岳」の詳細ID | 0件 | 0件 |
| 構造化フィルタ | 既存11条件にPASS | 同じJSを利用し11条件にPASS |

Pagefindは全文検索＋全結果fragment取得でcold {metrics['pagefind_query_cold_ms']:.1f} ms、warm 20回中央値 {metrics['pagefind_query_warm_median_ms']:.1f} ms。比較対象のタイトル部分一致は10,000回で{metrics['substring_10000_total_ms']:.1f} ms、DOM描画を含まない。異なる処理なので直接の速度比や大規模性能を推定しない。サイズは非圧縮ディスクバイトで、初期通信量とは異なる。生のnavigation/resource timingは `evidence/vendor_actual/browser/performance.json`。

## 保守性・実装負担

現在はAstroがホーム1ページを生成し、11のテーマ／詳細HTMLをpublicからコピーする最小移植。テンプレート共通化・コンテンツ管理の効率向上は未実証。Vanillaは8件では単純でビルド依存がなく、AstroはNode／lockfile更新とビルド工程を増やす。今回の必須差分は3つのscriptへのis:inline指定、テレメトリ無効化ランナー、索引再生成ランナー、検査ページ修正と実行テスト。`npm ci` を実行して固定lockから199パッケージを導入した。

Pagefindは全body 13HTMLを索引化し、検索はホームやテーマにもヒットする。レコードID抽出は詳細URLから行い、構造化フィルタは既存JSで別途維持する。PagefindのCLI出力は0 filtersであり、P2のAND／OR／null規則を自動実装したとは扱わない。

## 検索不一致と採用条件

「奥多摩」の索引fragmentは「奥多／摩」、ブラウザ照会はIntl.Segmenterによる「奥多摩」。Pagefind 1.4.0でも再現。日本語山域の表示を明示する局所実験でも改善せず、最終ページは固定ソースと同一バイトへ戻した。期待2件を変更してPASSにしない。

次の候補は索引・照会の分割規則をそろえる設計を隔離PoCで検証すること。vendor生成JSやWASMへの場当たり的パッチ、特定語だけのハードコード、固定データ変更での通過は行わない。A 2–4h、Fの差分限定再検証0.5–1hを見積もる。これは見積りであり追加予算承認や自動継続予定ではない。OwnerがPagefindを保留してVanillaを維持する選択も可能だが、現受入条件のMajorは独断でcloseしない。

## セキュリティ境界

索引生成入力はdistのみ。限定側はoutputs/membersに分離。公開distのraw bytes・gzip展開内容・fragment URLを同一scannerで検査し、HTML・gzip索引・限定index・限定routeの4故障を検出した。別TEMPで実Pagefindに限定ページを混入させた索引も生成し、scannerとmembers URLヒットで検知した。

カナリア検索0件だけでは証明にならない。実際に汚染索引でも引用符付きカナリアは0件となり、無引用の正常公開索引は8件に広くヒットした。クエリ結果は補助Evidenceとして保存し、分離判定はデコード済み成果物・生成ルートと故障注入に依拠する。

実会員認証・本番JWT・Accessは未実装。GitHubは公開リポジトリで、合成カナリアとテストコードを含む成果物管理先。実データの秘匿を意味しない。配信対象をdistへ限定すること。実限定データを公開成果物や公開検索索引へ入れない設計は本番でも必須だが、本PoCを実認可の証明には用いない。

## 未検証・停止条件

優先4ファイルが作業領域にない。Windows実機／ネイティブURLバーの画面証跡、独立F、CT04独立HTTPブラウザ実測、Microsoft Office実機、全WCAG/AT、本番依存監査は未完了。元P3-A F BLOCKEDを維持。公式Freezeは0回、G4 STOP、P3-B2未開始。
'''
(D/'ADR_001_ASTRO_PAGEFIND.md').write_text(adr)
handoff=f'''# 【P3_B1_A_EXECUTION_HANDOFF】

Task ID: **P3-B1-REAL-VENDOR-POC-20261016-01**／A Producer。

実製品の導入・ビルド・日本語索引・Chromium HTTP操作・負試験を実施した。**Pagefind「奥多摩」はFAIL。正式Candidate Freeze未実施、独立F未実施、G4 STOP。** GitHub pushは自動承認レビューで拒否され、未実行。ローカル提出成果とGit bundleを用意する。

## 実行時刻・環境

- 実行記録開始：{runtime['started_at']} JST。
- 最終vendorブラウザ検証終了：{state['vendor_test_end_jst']} JST。
- この報告生成：{now} JST。上記開始から検証終了まで{elapsed:.1f}秒のwall clock。準備前の全セッション開始時刻・人時は計測しておらず推定しない。ログ内の機械時刻はUTC。
- Linux 6.18.44 x86_64、Node 24.19.0、npm 11.9.0、Python 3.12.14、Chromium 154.0.8037.57。
- Astro 7.3.8／Pagefind 1.5.2 Extended。npm ci exit 0、build exit 0、ja index exit 0。13HTML・338 words・26索引ファイル。
- 通常sandboxでnpm接続EPERM。ネットワーク権限付きの実npm pingは成功。Astroの領域外テレメトリ書込みを無効化して再実行した。初回失敗も保存。

## 入力・固定版

固定入力：184,006B／88entries／SHA-256 `a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9` 一致。Drive正式入力を取得し、sourceにそのまま保管した。

P2完全ZIP pin `c1969c801dc47cb15636ce1a74da13433d13ddccf03f308895828ef3d8632f6f`、P3-A完全ZIP pin `bc17d7d10b60433754732598a0d2b781eadb337da7b4a80dd8613c79a81c3a23` は正式Work Order上の値。完全ZIP自体は未取得で、独立再計算を主張しない。入力ZIP内のP3-A source 16ファイルと現在sourceは全てバイト一致。P2/P3-A正本への書込みなし。

**必須4ファイルは欠落**：AGENTS.md、START_HERE.md、P3_B1_CODEX_A_WORKORDER.md、CODEX_EXECUTION_STATE.json。所在を質問したが、この報告時点で補足なし。見つかったと偽らず、正式Drive Work Order 2文書で実行可能な部分を進めた。`EXECUTION_STATE_RESULT.json` は今回新規の結果であり欠落入力の代用記録ではない。

package-lock SHA-256：`{state['package_lock_sha256']}`。出力ZIP SHAとManifestはartifactsのsidecar及びMANIFEST.json参照（循環ハッシュを避け、ZIPの自己ハッシュはZIP外に置く）。

## 最終検査

| 検査 | 結果 | Evidence |
|---|---|---|
| 実Astro静的生成 | PASS / exit 0 | 23_final_build.json |
| 実Pagefind ja索引 | PASS / exit 0 | 24_final_index.json |
| dist・ルート・8ID・原ソース互換 | 42 PASS / 0 FAIL | 25_final_dist.json |
| 正常系raw/gzip/fragment分離・4故障・4形式解析 | 25 PASS / 0 FAIL | 26_final_security.json |
| 実限定混入Pagefind索引の故障検知 | PASS | index_fault_injection.json |
| 固定ベースライン | 59 PASS / 0 FAIL | 28_final_baseline.json |
| Chromium統合 | 32 PASS / 1 FAIL | browser/browser_report.json |
| Pagefind日本語3照会 | 2 PASS / 1 FAIL | browser/japanese_search.json |
| 独立F／元CT04 | NOT_EXECUTED／歴史的BLOCKED維持 | A結果と分離 |
| Windows/Edge・ネイティブURLバー証跡 | NOT_EXECUTED | headless PNGと実URL/UTC JSONは保存 |
| GitHub push／Draft PR | BLOCKED／NOT_EXECUTED | GITHUB_PUBLICATION_BLOCKED.md |

最終Pagefind詳細ID：谷川 `[SYN-TGW-001, SYN-TGW-002]`、奥多摩 `[]`（期待 `[SYN-OKU-001, SYN-OKU-002]`）、穂高岳 `[]`。奥多摩は環境BLOCKEDでなく**製品／統合FAIL**。

ブラウザは `http://127.0.0.1:8766/` → `/themes/tanigawa-sawa-db/index.html` → `/themes/tanigawa-sawa-db/records/SYN-TGW-001.html` → browser Back → Forward を実行。各実URL・UTC・PNGを保存した。Vanilla／Astro双方で11検索条件（同項目OR、項目間AND、体系内グレード、月、行程、null除外、空結果）を期待IDと照合。両者一致。頭出しだけの見かけの試験ではなく、実コントロール入力を行った。

4形式は同梱実ファイルを開いた。HTMLはChromiumで表示、PDFはPyMuPDFで解析・画像化、PPTXはpython-pptx、XLSXはopenpyxlでID／7点・5点などのセルを確認。PPTX/XLSXはLibreOfficeで別PDFへ実変換し、画像化・目視確認。Microsoft Office実機互換は未検証。

## Findingと処置

- **B1-M001 OPEN**：Pagefind日本語分割不一致。1.4.0でも再現。採用保留、Vanilla維持。期待値を変更せずFAILを残す。
- B1-M002：Astro script取り込み失敗をis:inlineで是正。A再検証済み、F未判定。
- B1-M003：配布用検査ページにカナリアが混入する準備版欠陥を除去。raw/gzip/decoded・故障注入でA再検証、F未判定。
- B1-M004：カナリア照会0件単独による誤判定を防止。同一scannerと故障索引に基づく検査へ補強。F未判定。
- B1-E001：優先入力4ファイル欠落はBLOCKED。B1-E003：GitHub外部書込みは自動承認レビューでBLOCKED。

詳細はFINDINGS.json、採用比較はADR-001。通常16h相当は管理枠であり実人時ではない。Pagefind是正の追加候補はA2–4h＋F0.5–1h、入力回復0.25hの見積り。重大指摘を未解消のままGOにせず、必要な期限・範囲はOwner判断へ提示する。

## 次の独立限定レビュー

Review RouterがAとは別セッションのFを選び、提出SHAを固定して1回の限定レビューを行う。A自己検査をF PASSに転記しない。

1. B1-M001の同じ3照会・詳細IDと索引/照会分割の不一致を独立再現し、採用保留の妥当性を判定。
2. M002〜M004の差分（script保持、公開probeの文字列除去、raw/gzip/URL検査、実故障索引検知）と直接影響範囲を独立再実行。
3. 8件・3テーマ・AND/OR/月/行程/難度の意味、4形式、Home→theme→detail→Back/Forwardを対象とする。CT04独立HTTP実測とネイティブURL証跡の欠落を解消するまでG4停止。
4. Critical/Majorが残れば原因と担当を固定し、局所是正＋新SHA＋該当箇所の独立再検証。機械的な全面再レビューを繰り返さない。

公式Freezeは0回消化。提出物は**実行成果スナップショット**。Drive新規保存とraw readbackは別receiptに実測値を記す。GitHub書込みは具体的公開対象のOwner承認待ち。公開サイト配備・Cloudflare／Access・本番JWT・実データ取込み・P3-B2・G4 GOは実施していない。
'''
# correct the P2 pin from the authoritative source instead of transcribing it.
handoff=handoff.replace('c1969c801dc47cb15636ce1a74da13433d13ddccf03f308895828ef3d8632f6f',J('docs/SOURCE_PIN.json')['source_p2_full_sha256'])
(D/'P3_B1_A_EXECUTION_HANDOFF.md').write_text(handoff)
print(json.dumps({'generated_jst':now,'metrics':metrics,'state':state['results']},ensure_ascii=False,indent=2))
