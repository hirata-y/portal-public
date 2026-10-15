# P3-B1 有限レビュー＋重大指摘の猶予と例外

Owner 2026-10-15 決定：通常時はレビュー回数を制限する。Critical/Majorは是正猶予を認め、対象Findingの独立再検証を許す（機械的な1回打切りにしない）。

- 通常: 初回Candidate Freeze 1回、分離したF等の独立限定レビュー1回。Minorは原則P4 Backlogまたは条件付き受入とし、同一内容の全文書改訂・再レビューを自動化しない。
- 重大なCritical/Major: Finding ID・原原因・根拠・影響範囲・直近Freezeとの差分・修正Responsible・Expected/Actual・停止条件を独立Reviewerが明示。**この期間中はGO/次Gateへ進めない**。修正対象と否定的影響テストを修正担当が固定し、差分限定の新Candidateを1回ずつ再Freeze、元Reviewerと可能な限り分離したReview Router選定ReviewerがFinding限定で再検証する。
- 是正猶予: 最初の重大Finding起票から原則48時間相当を提案（Ownerの承認で日時固定、元の2026-10-16〜18予定に食い込む場合は期限再調整）。初回重大Findingへの再検証は最大2サイクルを管理目安とする。なおユーザー要望の「重大な指摘が発生したらその限りではない」を尊重し、2サイクルで未クローズなら自動終了せず**Ownerの継続／方針変更／停止の再判断**へ移す。新Critical/Majorや別ルートの本質的重大指摘が出た場合も同様にOwner判断して例外枠を設定する。
- 16時間相当は通常時の目安・合算管理枠。Critical/Majorの品質要件は免除しないが、超過しそうな追加作業はOwnerへ見積・追加上限を求め、無制限に自動着手しない。
- BLOCKED (環境/実行条件未達) は製品FAILと区別し、代替可能な環境検証・User UATも証拠階層を明示する。Fの過去BLOCKEDを上書きしない。
- Release/G4: 全てのCritical/Majorを VERIFIED_CLOSED または条件付きの正式Ownerリスク決定とし、未検証CT04 independent actual browser、CT01/02 protected origin、CT06 DG012、52 N/A等の後続STOPを保持。G4で満たす必要のある要件を根拠なくG7へ移すことは禁止。
- コミュニケーション: Findingsが起きる都度一覧（Finding ID、担当、期限、試験、状況、回数、残工数）を同一統合台帳に追記。レビューごとに全文をやり直さない。

**正式にOwnerが今回指示した事実**は「重大指摘にはレビュー回数の例外、是正猶予を設ける」まで。48hと2サイクルという運用値は**提案**であり、Ownerの別途決定なく必須上限や正式承認として扱わない。
