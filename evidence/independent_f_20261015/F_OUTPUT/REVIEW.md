# P3-B1 Freeze1 独立限定Fレビュー原票

**Verdict: PASS_WITH_MINOR（今回のlocal/synthetic統合範囲）。Critical 0 / Major 0 / Minor 1。G4 STOP。**

- Task: P3-B1-F-INDEPENDENT-01 / 初回Freeze後の独立F 1回。
- Reviewer: Codex別セッションF。同じAI基盤上の役割・セッション分離であり、人間による外部監査ではない。Aを兼任せず、製品・元Candidate・Rのファイルは編集していない。
- 入力: P3_B1_CANDIDATE_v0.3.0_20261015_FREEZE1.zip、SHA256 `7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75`、5,403,706B、399 entries / 398 payload。安全展開、FREEZE1_MANIFESTの全398ファイルのSHA/sizeを開始時・終了時に確認。旧MANIFESTを現版の検算に使っていない。
- 実施UTC: 2026-10-15 07:19頃〜最終SUMMARY.jsonの終了時刻（JST+9）。人時ではなく、対話と機械実行のwall clock。新しい是正・追加再レビュー・外部書込はしていない。
- Linux、Node24.19.0、npm11.9.0、Python3.12.14、Playwright1.62.0、Chromium154.0.8037.57。headful DISPLAY=:99、127.0.0.1実HTTPをFが起動。

## 独立実測

最終suiteのみを数える。合計110 PASS / 1 FAIL / 0 BLOCKED。件数を工程進捗やGate合格率には変換しない。

| Suite | PASS | FAIL | 根拠 |
|---|---:|---:|---|
| 固定入力・source・lock・正常分離・正負mutation | 16 | 0 | static_results.json、01/16 logs |
| headful実HTTP・検索・filter・履歴・XSS・故障UI・network | 72 | 1 | browser_results.json、12_browser_final.log |
| 実故障Pagefind索引・同一scanner・private拒否 | 5 | 0 | fault_index_results.json、13 log |
| vendor再生成parity・依存・回収入力・分割上限・untrusted描画 | 17 | 0 | supplement_results.json、14 log |

コマンドは各*.command.jsonにargv/cwd/start/end/exit、*.logにstdout+stderrを保存。初回npm ciは既定cache先の書込不可でexit254。workspace内cache指定のnpm ciはexit0で199 package取得。ネットワーク障害をmockで置き換えていない。npm lsはAstro7.3.8/Pagefind1.5.2を確認し、npm audit既知脆弱性0。267 lock packageにlicense metadataあり、主要2packageの実LICENSEファイルも確認。法的な全バイナリ権利保証ではない。npm lsのoptional WASM等extraneous表示はログへ保持し、正常build・同一lock/bytesを確認した。

F_OUTPUT/rebuildでAstro実build exit0、Pagefind1.5.2 Extended実index exit0。13ページ・338語・219語辞書。再生成dist全ファイルとFreeze distのbytesが一致し、特にvendor pagefind配下26ファイル全bytes一致。P3-A source16ファイルと元入力内public既存ファイルも一致。lock SHA `dd957c01dc054952d911b48cff783e62c500d83d5d06898d730fba46faac5117`を保持。

独自期待値で谷川→TGW001/002、奥多摩→OKU001/002、丹沢→TNZ001〜004、穂高岳→0を確認。8個別タイトル、存在しない英数字/日本語、引用符・前後空白を含め16照会の詳細IDが一致。search_native_objects.jsonには実Pagefind result data/normalizationを保存した。標準Pagefind単独の奥多摩は詳細0のままで、統合adapter経由だけが指定2件に一致。アプリページのIntl.Segmenterはfunctionのまま。

ホーム8レコード・3テーマ、山域OR／月ORと他条件AND／難度体系とgrade OR／体系変更時のgrade解除／null難度の既定包含と条件時除外／null月・日数の除外／resetを独立操作。Home→谷川テーマ→TGW001→Back→Forward→Back→Home、/search/奥多摩結果click→OKU001→Backを実HTTPで確認。全3テーマ＋全8詳細はHTTP200。合成4形式をGETしてbytes数一致。5組のPNGとnative URLバー付きPNG、URLとUTCをbrowser_results.jsonへ保存した。favicon以外の対象リソース失敗、pageerror、外部requestは0。

query文字列3種のXSS非実行に加え、独立fault Workerから悪意あるtitle・外部URL・javascript URL・private URLを渡す描画境界試験を実施。titleは文字として表示、img DOMは生成されず、外部/JS/private routeは結果へ出ない。このfault responseはXSS試験専用で、検索正否の証拠には使っていない。壊れた辞書、Worker起動故障は結果0＋明示エラー。201文字と32分割候補超過も拒否された。

分離は正常dist raw/gzip復号とprivate routeを走査し0、raw/gzip mutationで検出。さらにF_OUTPUT/fault_siteのコピーだけにmembersページを作り、本物のPagefind CLIで再索引した。正常・故障へ同じ独自scannerを使い、故障pf_fragmentの限定URLとzero-width除去後のcanaryを検出。実native検索もprivate routeを返す。**引用カナリア検索は汚染索引でも0件**であり、それだけでは分離を証明できないことをF自身が再現した。lexicon生成器はこのprivate fragmentを拒否した。

## Findingと独立disposition

| ID | F評価 | 原因・影響・範囲／根拠 |
|---|---|---|
| B1-M001 | VERIFIED_FIXED_IN_INTEGRATION_SCOPE | 公開fragment由来辞書＋専用Workerのnative fallbackで固定期待IDと回帰が一致。vendor単独の奥多摩0は継続し、完全全文品質の解決とはしない。対象pagefind-ja.js/worker、create_ja_lexicon、index pipeline、/search/のみ。 |
| B1-M002 | VERIFIED_FIXED | 3 scriptのis:inlineと順序を確認。実Astro build exit0、元JS/source bytes一致、実ホームfilter動作。 |
| B1-M003 | VERIFIED_FIXED | 正常公開dist/probeから限定canaryなし。独自正負mutationと実故障indexで検出器が反応。 |
| B1-M004 | VERIFIED_FIXED_FOR_B1_SEPARATION_METHOD | query0だけに依存せずdecoded fragment/route/生成入力と実故障indexで確認。引用0でも混入する現象を独立再現。Access/JWT保証のcloseではない。 |
| B1-E001 | CURRENT_INPUT_BLOCKER_RESOLVED; HISTORICAL_DEVIATION_RETAINED | 回収4原文hash・Work Order単体SHAを独自検算し、回収原文と現Task要求を照合。実行前未読の手続事実を遡及修正しない。今回Fは指定文書を読了。元handoff kit ZIP全体の独自raw再取得は今回行っておらず、nested一致の過去記録をF実測と偽らない。現versionの製品・受入証拠に未検証の重大差異は検出しなかった。 |
| B1-Q001 | VERIFIED_WITH_MINOR_CONSOLE_EXCEPTION | 検索click、XSS、Console/Network、依存/license、native画面の独立証拠を収集。favicon errorは以下Minor。 |
| CT04独立実HTTP部分 | VERIFIED_FOR_B1_LINUX_CHROMIUM | F自身のheadful実HTTP・履歴・検索click・XSSとnative URL画面を取得。歴史P3-A F BLOCKED原票を変更せず、全CT04やG4をcloseしない。 |
| B1-F001 | **Minor OPEN** | ブラウザが/favicon.icoを自動取得すると404となりConsoleに1 error。期待error0／実測1。原因は公開distにfavicon未同梱。ページJS・検索・filter・navigationは正常で、データ分離・主要操作へ影響しないためMinor。browser_results.json normal_console_errors、12 log。 |

B1-F001の処置候補はP4 backlog/条件付き受入。Aの修正を本レビュー内で依頼せず、Candidateを固定したまま報告する。将来是正する場合の限定確認は、favicon同梱またはHTML指定差分、/favicon.ico HTTP正常応答と新context初回Home/SearchでConsole正常、主要navigation/search smoke。全面Gate再レビューは不要。

## 限界と判断境界

任意全文の完全再現、高度ランキング、多端末・大量データ性能は今回の受入範囲外。native vendor単独FAILを隠さず、補助辞書再生成とWorker運用の保守負担を残す。完全P2/P3-A元ZIP全体のraw再計算、Windows/Edge、Office GUI、全WCAG2.2AA・AT・native200%、DG012/52N/A正式判断、実issuer/JWT/保護配信・Cloudflare・PII・B2/G4/GitHub書込は未実施。G4 GO、OwnerのB1受入・技術採用・B2開始承認ではない。

同一F作業中に独自harnessの括弧誤り、絶対URL連結、画面capture寸法・再実行時のmutation残存を直し、失敗ログを保持した。製品修正や追加Fサイクルではない。最終browser suiteのfavicon FAILも保持し、ゼロFAILと記載しない。実施済みsuiteをさらに反復せず、初回1回の原票を固定する。
