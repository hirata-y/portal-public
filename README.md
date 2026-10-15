# AI調査成果物共有ポータル — P3-B1 実行成果

Astro 7.3.8の実ビルドとPagefind 1.5.2 Extendedの日本語索引を生成しました。**日本語分割補助を加え、谷川2件・奥多摩2件・不一致0件を実証しました。標準Pagefind単独は未解決です。初回Freezeと独立Fの最新状態はPROJECT_STATUS.mdを参照。G4 STOP。**

- [今回の是正Handoff](docs/P3_B1_REMEDIATION_HANDOFF.md)
- [今回ADR・実測比較](docs/ADR_002_JAPANESE_BOUNDARY_ADAPTER.md)
- [最新管理状態](PROJECT_STATUS.md)
- [旧実行Handoff](docs/P3_B1_A_EXECUTION_HANDOFF.md)
- [ADR・実測比較](docs/ADR_001_ASTRO_PAGEFIND.md)
- [Finding台帳](docs/FINDINGS.json)
- [最新ブラウザ結果](evidence/vendor_actual/browser/browser_report.json)
- [日本語検索の期待ID／実測ID](evidence/vendor_actual/browser/japanese_search.json)
- [実行可能ZIP・SHA](artifacts/)

## 起動

同梱の `astro_candidate/dist` が実生成済みの静的サイトです。リポジトリのルートをHTTP配信しないでください。

```sh
cd astro_candidate/dist
python -m http.server 8766 --bind 127.0.0.1
```

`http://127.0.0.1:8766/` が既存8レコードの検索UI、`http://127.0.0.1:8766/tech-evidence/pagefind_japanese_browser_probe.html` が補助付き実Pagefind照会、`http://127.0.0.1:8766/search/` が検索結果をクリックできるPoCです。画面のボタンで照会・JSON保存できます。既存UIは引き続きVanillaの構造化検索を使用します。

## 再生成

Node 24.19.0 / npm 11.9.0で実行。依存導入はネットワークを必要とします。

```sh
cd astro_candidate
npm ci --no-audit --no-fund
npm run build
npm run index:pagefind
cd ..
```

`npm run build` はAstroのテレメトリをプロセス内で無効にします。索引再生成は前回の索引・検査ページを除去し、13公開HTMLのみを索引化してから検査ページを再配置します。依存はpackage-lockで固定。Windows PowerShellの既存ランナーも `npm ci` に変更済みですが、Windows実機での実行は未検証です。

## A検査の再実行

```sh
python -m pip install -r tools/python-requirements.txt
P3_B1_EVIDENCE="$PWD/evidence/remediation_rerun" python tools/browser_probe.py
python tools/remediation_checks.py
python tools/adapter_negative_probe.py
```

Chromium実行ファイルが `/usr/bin/chromium` 以外なら環境変数 `P3_B1_BROWSER` に絶対パスを指定してください。ブラウザは既存の実バイナリを使用します。PDF/PPTX/XLSXの解析は上記Python依存で実行し、Officeレンダリングは別途LibreOfficeが必要です。

現行受入実測は `evidence/remediation_20261015/`。元vendor_actualのFAILは当時の履歴として維持。上記追加2スクリプトは今回ディレクトリへ書き込むため、Freeze ZIPは別フォルダへ展開して再検証してください。期待IDは変更していません。

## 証拠の読み方

`evidence/vendor_actual/` は前回の実行記録。`23_final_build`〜`29_final_browser` が提出distに対応する最終実行です。以前の失敗・局所是正は時刻付きログとして残しています。入力由来の `evidence/*.json` と旧README・旧技術評価・旧Manifestは準備段階の履歴であり、今回のPASS根拠に使いません。今回の一覧は `EXECUTION_STATE_RESULT.json` と `MANIFEST.json` を参照してください。

固定入力ZIPと `source/p3_a_site` は保存・照合済み。P2/P3-Aの完全な元ZIPは今回の作業領域にはなく、正式Work Order上のSHA pinと、入力ZIPに含まれるP3-A 16ファイルの同一性を区別しています。

この公開GitHubリポジトリには合成カナリア・テストコード・検証用ZIPを含みます。実限定データ・秘密・個人情報・実資料を扱う境界の証明ではありません。HTTP配信対象はdistのみ。Cloudflare／Access・本番JWT・公開サイト配備・P3-B2は実施していません。
