# 現在のFinding台帳

原A台帳・過去ZIP・P3-A独立原票は変更しない。今回の独立F原票はevidence/independent_f_20261015/F_OUTPUT/REVIEW.md（入力Freeze1 SHA 7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75）。FはCritical0/Major0/Minor1、PASS_WITH_MINOR。過去のMajorの版限定是正と未解決の上流標準クライアントの制限を分ける。

| ID | 分類 | 原因・是正／影響 | 現在状態 | 根拠と次の処置 |
|---|---|---|---|---|
| B1-M001 | 原Major | Charabia索引とIntl照会分割不一致。公開fragment辞書＋専用Worker fallbackで実JS/WASM検索 | F VERIFIED_FIXED_IN_INTEGRATION_SCOPE | 指定ID・丹沢・個別title・負語の独立実測。標準vendor単独の奥多摩0は継続し、上流不具合解決／全日本語保証とはしない |
| B1-M002 | 原Major | Astro public script解決不能を3script is:inlineで是正、順序・bytes保持 | F VERIFIED_FIXED | fresh Astro build0、JS/source同一、実filter動作 |
| B1-M003 | 原Major | 公開probe内の限定カナリアを除去。生成物raw/gzip/decoded/routeを検査 | F VERIFIED_FIXED | 正常0・正負mutation・本物の汚染Pagefind indexで検出 |
| B1-M004 | 原Major | quoted canary0のみでは分離を証明できない | F VERIFIED_FIXED_FOR_B1_SEPARATION_METHOD | 汚染indexでもquoted0をF自身が再現。decoded content/URL・入力・故障検査へ。Access/JWT認証保証のcloseではない |
| B1-E001 | 原Major／入力手続 | 回収4入力SHAをFも検算。原実行前未読履歴は残る | CURRENT_INPUT_BLOCKER_RESOLVED／HISTORICAL_DEVIATION_RETAINED | 現Candidateに未検証の重大差異を検出せず。元kit全体の独立再取得は今回未実施と明記 |
| B1-E002 | 原Minor／環境 | npm/cache・telemetry・capture制約をローカル許可範囲で解消 | A/F実行環境RESOLVED | Linux headful URLバーあり。Windows/Edgeは未実施で代替PASSにしない |
| B1-E003 | 過去公開権限 | 元合成PoCの公開push拒否後、別Owner明示承認で成功 | AUTHORIZATION_RESOLVED（旧版） | PUBLICATION_RECEIPT.json。今回E005とは別 |
| B1-E004 | 過去管理公開権限 | 元管理資料の公開は別Owner承認後成功 | AUTHORIZATION_RESOLVED（旧版） | management/PUBLICATION_RECEIPT.json。以前の公開成功を取消さない |
| B1-E005 | 今回公開権限 | 新是正コード・Freeze・status・追加Evidenceの公開pushをauto-reviewが承認不足と判定、実行前拒否 | AUTHORIZATION_RESOLVED／57f5f20 push成功 | local commitと非共有Drive保存／raw照合まで完了。今回Owner追加承認を受領し、23_owner_approved_push exit0。旧拒否は履歴として維持。製品品質FAILではない |
| B1-Q001 | 受入Evidence不足 | 検索click・XSS・Console/Network・依存・native画面をA/Fで収集 | F VERIFIED_WITH_MINOR_CONSOLE_EXCEPTION | 不足は今回埋まり、favicon例外をF001として未解決のまま分離。Windows/Office GUI・全AAを実行済みにしない |
| B1-F001 | F Minor OPEN | favicon.ico未配置→自動取得404→Console error1件。主要操作・分離への影響なし | OPEN_BACKLOG／Owner条件付き受領済み | F browser72PASS/1FAIL。Ownerが条件付き受領・backlog管理を選択。今Candidateは修正しない。将来修正時はicon応答・新context Console・検索／遷移smokeだけ確認 |
| P3-F-BLK-001／CT04 | 歴史的独立BLOCKED | 原P3-A Fのnative localhost制約 | 原票BLOCKED維持／B1実HTTP部分のみF VERIFIED | B1の独立headful HTTP/履歴/click/URL証拠は後発補足。全CT04・全AA/AT/native200%・G4はcloseしない |

B1-M001〜M004の独立是正確認は今回のlocal/synthetic統合限定。一般検索品質や本番認証の保証へ広げない。初回Freeze1・F1で区切り、Minor処置／Owner受入へ回す。Critical/Majorが新たに出た場合は原因と限定影響・追加見積りを示してOwnerに判断を求める。48h・2サイクルは未承認の提案値。期限・人時・追加枠は創作しない。


2026-10-15T16:39:30.339470+09:00：OwnerがB1-F001のbacklog管理と条件付き受領を明示。E005は今回版の具体承認と57f5f20 push成功で解消。独立F原票／未修正Minor／旧拒否履歴は保持。
