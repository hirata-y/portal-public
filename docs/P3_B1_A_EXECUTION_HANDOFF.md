# 【P3_B1_A_EXECUTION_HANDOFF】

Task ID: **P3-B1-REAL-VENDOR-POC-20261016-01**／A Producer。

実製品の導入・ビルド・日本語索引・Chromium HTTP操作・負試験を実施した。**Pagefind「奥多摩」はFAIL。正式Candidate Freeze未実施、独立F未実施、G4 STOP。** GitHub pushは自動承認レビューで拒否され、未実行。ローカル提出成果とGit bundleを用意する。

## 実行時刻・環境

- 実行記録開始：2026-10-15T12:37:34.201228+09:00 JST。
- 最終vendorブラウザ検証終了：2026-10-15T12:46:42.640330+09:00 JST。
- この報告生成：2026-10-15T12:50:40.794745+09:00 JST。上記開始から検証終了まで548.4秒のwall clock。準備前の全セッション開始時刻・人時は計測しておらず推定しない。ログ内の機械時刻はUTC。
- Linux 6.18.44 x86_64、Node 24.19.0、npm 11.9.0、Python 3.12.14、Chromium 154.0.8037.57。
- Astro 7.3.8／Pagefind 1.5.2 Extended。npm ci exit 0、build exit 0、ja index exit 0。13HTML・338 words・26索引ファイル。
- 通常sandboxでnpm接続EPERM。ネットワーク権限付きの実npm pingは成功。Astroの領域外テレメトリ書込みを無効化して再実行した。初回失敗も保存。

## 入力・固定版

固定入力：184,006B／88entries／SHA-256 `a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9` 一致。Drive正式入力を取得し、sourceにそのまま保管した。

P2完全ZIP pin `c1969c801dc47cb15636ce1a74da13433d13ddccf03f308895828ef3d8632f6f`、P3-A完全ZIP pin `bc17d7d10b60433754732598a0d2b781eadb337da7b4a80dd8613c79a81c3a23` は正式Work Order上の値。完全ZIP自体は未取得で、独立再計算を主張しない。入力ZIP内のP3-A source 16ファイルと現在sourceは全てバイト一致。P2/P3-A正本への書込みなし。

**必須4ファイルは欠落**：AGENTS.md、START_HERE.md、P3_B1_CODEX_A_WORKORDER.md、CODEX_EXECUTION_STATE.json。所在を質問したが、この報告時点で補足なし。見つかったと偽らず、正式Drive Work Order 2文書で実行可能な部分を進めた。`EXECUTION_STATE_RESULT.json` は今回新規の結果であり欠落入力の代用記録ではない。

package-lock SHA-256：`dd957c01dc054952d911b48cff783e62c500d83d5d06898d730fba46faac5117`。出力ZIP SHAとManifestはartifactsのsidecar及びMANIFEST.json参照（循環ハッシュを避け、ZIPの自己ハッシュはZIP外に置く）。

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
