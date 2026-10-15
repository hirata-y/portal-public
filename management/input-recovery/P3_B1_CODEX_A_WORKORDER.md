# AI調査成果物共有ポータル｜P3-B1 A Producer Codex実行Work Order

あなたはA：Producer／実装担当です。`AGENTS.md`と`START_HERE.md`および展開済み既存bundle内の `docs/SECURITY_AND_G4_STOPS.md`, `docs/P3_B1_REMEDIATION_REVIEW_PROTOCOL.md`, `docs/SOURCE_PIN.json` を読み、ここに書かれた **実際の検証** を行ってください。計画だけの回答は禁止です。明示されない実サービス接続・実データ利用・本番公開は禁止です。

## 1. 対象と管理
- 作業起点：同梱 `source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip`（SHA256 `a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9`）。初手でSHA・ZIP CRC・構成を検査。
- P2 v1.1.6とP3-A v0.1.0の固定版を編集禁止。合成8レコード・3テーマ・検索のAND/OR/欠損値意味の保持が必要。
- 通常期間の計画基準：2026-10-16〜18 JST。16時間相当は**A実装＋独立F＋統合の合算管理目標**、人間の実測工数ではない。実着手日時をJSTで記録し、超過・重大事項は推計と影響をOwnerへ戻す。非同期実行や依存パッケージ取得が成功するとは事前に仮定しない。
- 通常：公式Candidate Freeze1回 → F限定独立レビュー1回。Critical／Majorが発生したら限定是正猶予を認め、差分のみ独立再レビューし、Ownerに追加期間／工数判断を要請。小さな指摘を口実に全面レビュー無限ループは禁止。初回の48時間猶予と2回でOwner判断は**暫定案**で、正式な絶対上限として扱わない。

## 2. 必須の実行作業
1. Linux/Windowsのnode/npm/Python/ブラウザ/ネットワークを記録。公開npmレジストリへの接続可否を実コマンドで確認。インストールが不可ならEAI_AGAIN等のログ・exitを残して**環境BLOCKED**として止める。PagefindのソースだけでPASS不可。
2. 作業フォルダにAstroとPagefindのバージョンを固定してインストールし（ローカルのみ）、`package-lock.json`を保存、ハッシュ、ライセンス・依存を確認。`npm run build` と `npm run index:pagefind` を実行、正確なexit/stdout/stderrを保管。
3. `astro_candidate/dist`の実生成物で、ホーム、テーマ3件、詳細8件、元P3-AのJS/CSS・実データ、不変性、HTML/PDF/PPTX/XLSX合成4形式、公開側カナリア未混入を検証。`tools/verify_vendor_dist.py --dist astro_candidate/dist --require-index`を実行し、期待と実測をJSONで保存。公開/限定分離では、故障注入でカナリア混入を検出すること。生成後の`pagefind/`まで確認する。
4. 実Pagefindの日本語検索（最低「谷川」2件、「奥多摩」2件、ない文字列0件）を、生成クライアントをHTTPでブラウザ起動して実行し、**詳細URLの`SYN-...` IDs**で比較する。既存の `tools/pagefind_japanese_browser_probe.html` を利用可。Pagefind検索は単なるPython部分一致代替ではない。実index/JS bundleからの結果JSONと実ブラウザ画面を保存。期待差異はFAIL/課題として記録し、勝手に合格条件を変えない。
5. Browser native HTTP: `127.0.0.1`上の出力サイトでHome→谷川テーマ→SYN-TGW-001詳細→戻る／進む、検索→詳細、主要リンクとConsole/Networkを検査。Codexブラウザがloopbackアクセス不可ならNOT_EXECUTEDと記録し、OwnerのWindows実機が必要な証拠を明記（A自己検査と独立Fを区別）。
6. 日本語索引にpublic/member混入なし、ページの遷移・XSS文字列非実行、各合成形式のローカルHTTP取得、ビルド性能・出力サイズ・保守性とVanilla既存ベースラインを比較。PagefindではP2の構造化AND/OR・難度・月・行程日数条件を無条件に置換しない。実機と元データで検証する。
7. Astro／Pagefind採用かVanilla維持か、**実験結果に基づくADR／比較表**を提出。未実施なら「候補／BLOCKED」で止め、採用を断言しない。
8. 証拠が揃った時点に限り、1回の公式Candidate Freezeを実施。Manifestは全ファイルのSHAとバイト数を持ち、入力・lockfile・生成物・検査ログ・差分・異常系・ブラウザEvidenceを含む。新ZIP・SHA、Driveまたはこのチャットに渡せるファイルを作成。`node_modules`、秘密情報、外部個人情報を含めない。

## 3. 禁止とGate停止
外部GitHubリポジトリの書き込み、Cloudflare/Access作成・変更、JWT/Reader本番認証、個人情報/実成果物の取り込み、ドメイン取得/公開、P3-B2の実装を**別Owner承認なしで実行しない**。公開npm依存の取得はPoC実行の範囲に限る。
既存P3-A Fの正式BLOCKEDは履歴として維持、CT04の独立ブラウザE2E証拠はG4停止点。DG012、52件WCAG N/A_PROPOSED、実WCAG2.2AA認証、CT01/02の本番HTTP/JWTは未完了のまま。A Producer自身のPASSをF PASSにしない。重大指摘の放置や工数上限超過を黙って進めることはしない。

## 4. 最終Handoff形式
`【P3_B1_A_EXECUTION_HANDOFF】`：実施JST／Task ID、全入力のSHA、ソフトウェアバージョン、実コマンド・exit・ログ、vendor build・Pagefind実日本語検索のID expected/actual、公開/限定分離の正負試験、synthetic形式の確認、実ブラウザEvidenceまたは制限、判明したCritical/Major/Minorと残余リスク、正式Freezeか中間報告か、作成ファイルのリンク＋SHA、次の独立Reviewerのスコープ、工数の根拠、G4 STOP。`【/P3_B1_A_EXECUTION_HANDOFF】`で閉じる。
