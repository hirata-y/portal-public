# 初回限定Fレビュー発注記録

Task: P3-B1-F-INDEPENDENT-20261015-01。Ownerはこの対話で「A是正・Evidence完備・初回Freeze後、別セッションの独立Fレビュー1回まで」を選択。Codexがこの選択に従い別セッション `f_review_freeze1` を割当。役割は独立限定Reviewer F、Aの兼任ではない。同一AI実行基盤上の別コンテキストであり、外部人間の監査とは称さない。

入力：P3_B1_CANDIDATE_v0.3.0_20261015_FREEZE1.zip、SHA256 7a1af9f2cc3734db4837d138c779e06e0f3553e677d0ea1df501f2e807426f75、5,403,706B、399entries/398payload。Freeze1実時刻2026-10-15 16:18:36.077893 JST。Fはその後に発注。前版Manifestは履歴、対象版はFREEZE1_MANIFEST.json。

限定スコープ：M001〜M004、E001入力回収手続差異、Q001不足Evidence、影響する日本語検索ID／8件3テーマ／filter AND・OR・null／source・lock／公開分離と実故障索引／実HTTP browser履歴と検索click／XSS・Console/Network。本人の独自コード、expected/actual、exact commandとexit/log、画面を必要とする。AのPASSを独立PASSへ転載しない。Critical/Majorは原因・影響・限定修正と正負試験を明示し、一回の一次Verdictとして提出。元Candidateを編集しない。

期待検索ID：谷川SYN-TGW-001/002、奥多摩SYN-OKU-001/002、穂高岳0。標準Pagefind単独では奥多摩0が残り、補助統合を受入対象とすることを隠さない。上流修正や一般的な日本語完全品質の保証とはしない。

実行場所：/workspace/p3-b1-f-review-20261015、成果はF_OUTPUT。Linux実Chromium／loopback HTTP、既存Xorg :99によりheadfulとnative URL証拠取得可能。Windows/Edge、全AA/AT/native200%、本番認証／配備／実資料／B2／G4 GOは対象外。原P3-A F BLOCKEDを上書きしない。

通常レビュー1回の枠。初回重大Findingが出ても無限に自動再レビューせず、是正差分・追加見積り・Owner判断を分離する。48時間／2サイクルは未承認の運用提案で絶対値にしない。
