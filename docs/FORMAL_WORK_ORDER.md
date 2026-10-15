https://docs.google.com/document/d/1nE28ncCfhsEpLj3jNNz7uZXZgAfxNK4_1oQJFcr9zg0/edit

﻿AI調査成果物共有ポータル｜P3-B1 A Producer実ビルド・日本語検索／レビュー収束正式Work Order
Task ID P3-B1-REAL-VENDOR-POC-20261016-01 / 発行2026-10-15 JST
計画日程2026-10-16〜18 JST、通常管理枠16時間相当（実際の人時ではない）。実際の開始終了は実施時に記録し、非同期作業をしたと仮定しない。
Owner重要方針 https://docs.google.com/document/d/1zc58zYzGKvy5eIVN-SBMv80uEP5y4yQsYVIlB4edAmM/edit
P3-B1初期草案 https://docs.google.com/document/d/1tX1elYTK783Ry7sTPlPbAXwsLqXc21wDNg7rQcz8400/edit
P3-A Owner条件付き受入 https://docs.google.com/document/d/1y4RnhM-73h3QvR4u0-c6ivRm5wtBUxMBF03tGKNTom0/edit
P3-B1中間 ZIP https://drive.google.com/file/d/14AB1P1N1WKIYRez3FRqxt7heI1PiJxyp/view SHA256 8a903da413cc94a4d0196a2040ab42482eef9e1c35d4b136b6e9b3ef459cd06f。
本Taskの唯一の起点はWindows実行準備v0.2.1 ZIP https://drive.google.com/file/d/1TADJ17Qi-5WlHEz2F4M7uqzVcn2rGUdX/view SHA256 a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9、184006B、88 entries。Manifest https://drive.google.com/file/d/1UPFoTJBj9TH1Z1uS8TTDluxrCzpCP34p/view SHA256 426172cfb0384ef9e8ce43cec323069d802dcd1387cd6b87066ef6cb9e355cd4。
旧準備v0.2.0はv0.2.1にsupersede。v0.2.0とv0.2.1どちらも公式Freezeではなく、vendor実ビルドの成功を示さない。
P2 Full SHA256 c1969c801dc47cb15636ce1a74da13433d13ddccf03f308895828ef3d8632f6f とP3-A v0.1.0 SHA256 bc17d7d10b60433754732598a0d2b781eadb337da7b4a80dd8613c79a81c3a23 は不変正本。
【実行役割・安全境界】
別A Producer Task／セッションで実行。Review Routerが変更箇所とリスクで独立F及び必要な専門スポットを選ぶ。FとAはセッション・判定を分離する。同じAI基盤での分離は外部監査ではない。
外部GitHub・Cloudflare・ドメイン・会員・実JWT/Reader・本番HTTP配信・実個人情報・実資料アップロードは禁止。利用する実外部取得はユーザーが許容する環境の公開npm依存取得だけであり、これによって本番配備をしない。P3-B2は別契約。
【実行手順】
1. WindowsローカルでZIPのSHA256をPowerShell Get-FileHashで検算して展開。手順とスクリプトの内容を確認し、PowerShellから tools/run_real_vendor_probe_windows.ps1 を実行。任意のExecutionPolicy変更は1プロセス限りとし、利用できなければスクリプト内のコマンドを個別に実行する。
2. Node/npm/Pythonの版と実行日時、全command/exit/stdout/stderrを記録。スクリプトはローカルだけにAstro、Pagefindを--save-exactで導入し、package-lock.jsonを生成、npm run build、npm run index:pagefindを実行。失敗はそのままERROR/BLOCKEDとし、架空のAstro/Pagefind PASSを作らない。
3. 実build astro_candidate/distに11 theme/detail HTML、ホーム、日本語lang、固定8 SYNレコード、共通JS・CSS、合成HTML/PDF/PPTX/XLSX四形式があることを tools/verify_vendor_dist.py --dist astro_candidate/dist --require-index で評価。Pagefindの索引がない場合は検証FAIL。公開側にmembersカナリアの文字列・専用index・実ファイルが混入しないことをバイトと生成ルートで確認し、TEMPへの意図的混入を検出する。
4. distだけを127.0.0.1:8766でローカルHTTP配信し、Chrome/EdgeでHome→谷川テーマ→SYN-TGW-001詳細→ブラウザBack/Forwardを実行。URLバー、日時、スクリーンショットまたは短い画面録画を保存。独立Reviewerが後で同じ試験をする場合、本人の実行と区別。
5. dist/tech-evidence/pagefind_japanese_browser_probe.htmlを127.0.0.1:8766経由で開き、実際の検索ボタンを押してJSONを保存。谷川と奥多摩のレコード詳細は各2件、穂高岳は0件を比較。カナリア照会単独の0件では権限分離の証明としない。Pagefind索引は全HTMLにもヒットするため、レコード詳細URLのIDを抽出して期待値と照合する。
6. 元8件・3テーマ、P2 AND/OR/月/行程/難度の意味が壊れていないことを実画面とFixture比較で確認。Pagefindはこれらの構造化フィルタを自動的には実装しない。保守コスト、HTML/JSサイズ、ビルド時間、検索結果差分、負試験を記録。採用ADRはVanilla・Astro・Pagefindを実測に基づき比較し、未実施は別扱い。
7. 実build、Pagefind index、package-lockと固定版、テストコード、JSON、実ログ、スクリーンショット、差分、Manifest／SHAを新しい別成果物ZIPで保存。node_modules/npmキャッシュや秘密情報は保存しない。Drive raw readback SHA確認。実製品の検証完了後にのみ「公式Candidate Freeze 1回」を消化する。
【レビュー収束運用】
初回Freeze1回と独立限定レビュー1回が通常ルール。Critical/Majorが出たら、Findingの原原因・実行値と根拠・差分・担当・期限を固定し、Aが必要な局所是正、新SHA Candidate、専門担当の差分限定独立再検証を行う。再検証は硬直的な1回打切りにしない。是正猶予48時間・不成功2サイクルでOwner判断という数値は調整可能な提案であり、重大指摘の解消に必要な追加期限/工数はOwnerに理由を示して調整する。Critical/Majorが残ったままG4へGOしない。Minorは影響を評価して後続Backlogとし、無制限な全面再レビューをしない。
npm接続EAI_AGAINやChrome制限などの環境BLOCKEDと製品FAILを混同しない。Owner実機UATは独立Fレビューの代替ではない。元P3-A F BLOCKEDは記録を維持し、CT04独立HTTPブラウザ実測をG4停止条件とする。G4本判定とP3-B2実認証は新Owner判断。
【納品】
P3_B1_A_EXECUTION_HANDOFF：A Task ID/JST start/end/OS/Node/npm/Browser、入力/出力 SHA、実CLI logs/exit、Japanese Search Actual IDs JSON、実ブラウザ URL/Backの実測、公開側カナリアと4形式、テストPASS FAIL BLOCKED NOT_EXECUTED、公式Freeze status、A自己検証 vs F独立性、Critical/Major/Minor Finding、工数実測または推計、Drive原本／readbackリンク、次Review Router処置。
END WORK ORDER
