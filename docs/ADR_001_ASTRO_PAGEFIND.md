# ADR-001 — Astro実行可、Pagefind日本語検索の採用保留

決定状態：Aによる技術採用提案。Owner／独立F未承認。G4 STOP。2026-10-15T12:50:40.794745+09:00

既存Vanillaの検索・フィルタを維持する。Astro 7.3.8は静的生成の技術候補として継続可能。Pagefind 1.5.2 Extendedは現在の日本語検索受入条件を満たさず、置換採用を保留する。既存UIにはPagefindを接続していない。

## 実測

Linux / Node 24.19.0 / npm 11.9.0 / Chromium 154。127.0.0.1の同一マシン、各10 fresh contexts、通信・CPU制限なし。初期化時間はnavigation開始から8結果表示を観測するまでのPlaywright wall clock。順序はVanilla→Astroで交互無作為化しておらず、差は性能優位の根拠にしない。

| 項目 | Vanilla HTML/JS | Astro + Pagefind |
|---|---:|---:|
| 配信用総バイト | 99,245 | 694,892 |
| Pagefind追加出力 | 0 | 592,665（26ファイル） |
| 既存共通JS | 19,685 | 同一バイト |
| 8件表示までの中央値 | 308.6 ms | 281.6 ms |
| ビルドwall time | 必須ビルドなし | 1.100 s |
| 日本語索引wall time | なし | 1.190 s |
| 「谷川」の詳細ID | TGW-001 / TGW-002 | TGW-001 / TGW-002 |
| 「奥多摩」の詳細ID | OKU-001 / OKU-002 | 0件：FAIL |
| 「穂高岳」の詳細ID | 0件 | 0件 |
| 構造化フィルタ | 既存11条件にPASS | 同じJSを利用し11条件にPASS |

Pagefindは全文検索＋全結果fragment取得でcold 84.7 ms、warm 20回中央値 0.8 ms。比較対象のタイトル部分一致は10,000回で7.6 ms、DOM描画を含まない。異なる処理なので直接の速度比や大規模性能を推定しない。サイズは非圧縮ディスクバイトで、初期通信量とは異なる。生のnavigation/resource timingは `evidence/vendor_actual/browser/performance.json`。

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
