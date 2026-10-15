# P3-B1 Codex 実行引継ぎ — 2026-10-15 (日本語)

## 進行判定
**移行を推奨**：このChatGPT実行環境では `npm view astro version --fetch-retries=0 --fetch-timeout=4000` が `EAI_AGAIN registry.npmjs.org` で失敗。AstroとPagefindのCLIを稼働できず、これ以上のChatのみでの検証は実製品評価にならない。一方、Codexのコード／ターミナル／リポジトリ作業環境なら、依存取得が利用できれば実行可能。Codex環境のネットワーク可用性は未確認なので初手で確認する。

優先実行先：**ユーザーのWindows 11上のCodex（デスクトップ版のローカルフォルダー、もしくはCodex CLI）**。理由はユーザーのWindows Chromeによる127.0.0.1での実画面表示が確認済みで、GitHub新設・本番外部配備が不要なため。Codex Cloud利用も可能だが、必要なら別途リポジトリを環境に接続し、npmネットワークとローカルブラウザが利用可能な設定にする。ChatGPTのこのチャットからCodexタスクを直接起動する機能は提供されていない。

## 起動 5手順
1. このZIPをローカルフォルダに展開。`AGENTS.md`, `START_HERE.md`, `P3_B1_CODEX_A_WORKORDER.md` を残し、`source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip`を改変しない。
2. Windows PowerShellで `py -3 scripts\preflight.py`（ない場合は `python scripts\preflight.py`）を実行。予期されるSHAは `a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9`。
3. `source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip` を `work` のような作業フォルダに展開し、最内層 `P3_B1_VENDOR_READINESS_v0.2.1_20261015/` の内容を作業ルートとしてCodexに渡す。ローカルCodexにこのプロジェクトフォルダを開かせる。`AGENTS.md`とWork Orderも作業ルートに提示する。
4. Codexにこのファイルの `P3_B1_CODEX_A_WORKORDER.md` と下部の依頼文を渡す。Windowsは既存 `tools/run_real_vendor_probe_windows.ps1` を最初に内容確認し実行。LinuxのCodexには本キットの `scripts/run_vendor_probe_linux.sh` を作業ルートにコピーして実行可能（必要な依存取得はネットワーク許可がある場合に限る）。
5. Codexが生成したログ、`dist`、`package-lock.json`、索引実検索結果JSON、ブラウザ実画面の証拠を**新しい**成果物に保全。正式Freezeは実ビルド・実索引の証拠を得てから。独立Fは別セッションで、元Aが同時に「自己PASS」として判定しない。生成ファイルをこのチャットへ返して品質とGateを統合する。

## 正本
- P3-B1ソースZIP: `source/P3_B1_VENDOR_READINESS_v0.2.1_20261015.zip` SHA256 `a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9`。
- 元P2 Full v1.1.6 SHA256 `c1969c801dc47cb15636ce1a74da13433d13ddccf03f308895828ef3d8632f6f`。
- 元P3-A v0.1.0 SHA256 `bc17d7d10b60433754732598a0d2b781eadb337da7b4a80dd8613c79a81c3a23`。
- 現P3-B1自己検証：中間59/59 PASS、追加readiness静的41/41 PASS。どちらもProducer自己検証でありAstro/Pagefind実体未稼働、正式Freeze0、独立F0。
- H/P2 G3 GO WITH CONDITIONS、P3-A F BLOCKED historical、P3-Aローカル限定Owner受入、G4未承認。

## 依頼文
`P3_B1_CODEX_A_WORKORDER.md`を以下のタスクとしてCodexに貼り付ける。**計画だけで終了せず**実際のvendor build/index/queryとEvidenceを作る。環境BLOCKEDならログ、原因、実行済み範囲、次のオプションを記録して終了。
