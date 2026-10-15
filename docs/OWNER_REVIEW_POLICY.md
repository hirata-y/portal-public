https://docs.google.com/document/d/1zc58zYzGKvy5eIVN-SBMv80uEP5y4yQsYVIlB4edAmM/edit

﻿AI調査成果物共有ポータル｜Owner P3-B1レビュー収束方式変更・継続承認記録
Date: 2026-10-15 JST
Project: AI_Research_Artifact_Portal / Phase P3-B1
Owner newly stated: 「レビュー回数は一定設けたほうが良いが、重大な指摘が発生したらその限りではない。レビュー解消するための猶予は設け、進捗させる想定。進捗させて。」


DECISION ALREADY MADE
1. P3-B1 technical PoC continuation is authorized under local/synthetic/controlled scope; P3-A local-only Owner acceptance maintained. P3-A F review historically BLOCKED remains, G4 stop CT04 unwaived.
2. Default review cadence should be bounded, but serious Critical/Major findings are exception to rigid 1-review/1-Freeze stop. Give a bounded remediation window and review the verified causal correction, not automatically return to Owner solely for occurrence of any Major. Deliver quality improvement, verifiable defect closure and progress.
3. Existing baseline proposed start-end 2026-10-16 through 2026-10-18 JST and combined 16h-equivalent is adopted as PROJECT CONTROL TARGET for normal work in this limited phase. This is management proxy, not measured human time, not calendar background scheduling. An unresolved Critical/Major does not become PASS because deadline is reached; escalation/new deadline and resource ceiling require explicit Owner change record.
4. Normal pipeline: A candidate1 / integrated independent scoped review1 / Coordinator disposition. If no Critical/Major and evidence complete, do not initiate more review; Minor may be accepted as documented P4 backlog only if no safety or acceptance norm violation.
5. Critical/Major exception: a) independent Reviewer states exact Finding ID, severity, failing expected/actual, reproducible evidence and whether defect is source, contract or environment; b) Coordinator bundles overlaps, assigns single responsible A correction in narrowly scoped change; c) Producer changes only affected files, runs new positive/negative and mutation tests, freezes a correction candidate with new SHA and manifest; d) separate Reviewer performs targeted independent recheck of that Finding plus bounded impacted functionality; e) Coordinator closes only on VERIFIED_CLOSED or presents genuinely unresolved risk to Owner. Previous PASS does not become invalid unless changed-source impact actually shown.
6. Proposed operational remediation grace: first Critical/Major is allowed 48 hours after Finding as a planning allowance; this is management recommendation, NOT a user-specified immutable number. Within baseline Oct16-18 task, record the actual finding time, due date and whether planned end needs extension. At 2 unsuccessful targeted rechecks, escalate Owner for choice (additional specific time/budget, alternative design, or HOLD); serious defect can warrant further cycles by explicit Owner authorization. No infinite silent loop, no severity downgrades to force GO. New independent reviewer role chosen by Review Router on evidence/change impact rather than blanket C/E/F/G wave.
7. 16h-equivalent is the normal combined A/Review/Coordinator control value. Produce estimates vs actual/test machine timings distinctly. When unexpected Major requires budget beyond, prepare immediate revised scope, estimated extra work and a decision request; do NOT treat budget cap as license to skip required security tests or to auto-bill extra work. No new live service permission.
8. BLOCKED differs from FAIL: npm registry EAI_AGAIN is environment prerequisite, not proof that Astro/Pagefind fail product requirements. Provide reproducibility path on Owner Windows or authorized runner, keep NOT_EXECUTED until verified. No fabricated PASS by reading docs.


CONTROLLING INPUTS / CURRENT STATE
P2 H G3 https://drive.google.com/file/d/114RXxu5yTpM2KoMoaGSAwokcWMM0-EYD/view
P3-A v0.1.0 https://drive.google.com/file/d/1Cchg9Fp2AWAOqQ42_E9kI7xm-aM00U7t/view sha256 bc17d7d10b60433754732598a0d2b781eadb337da7b4a80dd8613c79a81c3a23.
P3-B1 interim https://drive.google.com/file/d/14AB1P1N1WKIYRez3FRqxt7heI1PiJxyp/view sha256 8a903da413cc94a4d0196a2040ab42482eef9e1c35d4b136b6e9b3ef459cd06f.
P3-B1 vendor-readiness work package https://drive.google.com/file/d/1Ry4TvjmFuV7ZBjGrChBHGMke9UcZbqYm/view sha256 03321fc09e08981f4fafe9a5ce355d36d552e79c643e9ade9be39969e67274d8, 153345 bytes, 81 ZIP members, original + SHA readback equal. The package is NOT an official production/review Freeze. Its source tests 41/41 PASS on existing public static baseline, actual vendor Pagefind missing fails required predicate as expected, nonexistent Astro dist yields explicit BLOCKED.
Package manifest https://drive.google.com/file/d/18uQRShxrolVVW9r4DCAWPm5AGRAx6gvb/view sha256 a03eac4966cb439d54b12a10c1e7300a1461c8db915127af9c5a10c01bf7ab7f.
P3-B1 true Astro build, Pagefind extended Japanese run, actual full P2 filter parity, browser Back, actual independent reviewer not executed here (npm registry DNS unavailable); G4 still STOP. Public/member canary on synthetic handcrafted public root is not actual user authorization.
NEXT: use vendor-readiness package in npm-capable Windows for actual binary build, browser query, lockfile, proper protected-index separation proof. One baseline Freeze AFTER runnable vendor results and evidence. If major findings occur follow above controlled exception. External GitHub/Cloudflare, JWT/Reader production, actual PII and real research originals require separate Owner permission; DG012 and 52 N/A stay pending.
END.
ADDENDUM 2026-10-15 — 実行準備パッケージの版整合
Astro実ビルド後に4形式を出力するための合成fixtureが、準備版v0.2.0のastro_candidate/publicに未配置とわかったため、誤った未検証結果を生まないよう準備版v0.2.1を発行し、v0.2.0をsupersedeした。これはまだOfficial B1 Freezeではなくレビュー回数の消費でもない。
利用すべき新最新版 https://drive.google.com/file/d/1TADJ17Qi-5WlHEz2F4M7uqzVcn2rGUdX/view SHA256=a7146a29e8d25a82f1eade189971b29ebb9f653c2f5bd59a730d9bbe01f389d9／Manifest https://drive.google.com/file/d/1UPFoTJBj9TH1Z1uS8TTDluxrCzpCP34p/view SHA256=426172cfb0384ef9e8ce43cec323069d802dcd1387cd6b87066ef6cb9e355cd4。Drive raw readback exact. 静的ベースライン41/41 Producer PASS、索引必須の負例は予期どおりFAIL(終了コード2)、実Astro dist不在はBLOCKED(終了コード3)。公式Astro・Pagefind成功の証明にはならない。
A向け具体的Work Order https://docs.google.com/document/d/1nE28ncCfhsEpLj3jNNz7uZXZgAfxNK4_1oQJFcr9zg0/edit
END ADDENDUM.
