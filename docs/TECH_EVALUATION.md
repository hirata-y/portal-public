# P3-B1 technical evaluation — measured vs not executed

## B1 decision matrix (evidence-limited)

| Candidate/axis | Current local vanilla static (P3-A) | Astro static candidate | Pagefind Extended Japanese |
|---|---|---|---|
| Runnable PoC here | Yes: original P3-A source copied byte-identical, localhost GET | **NOT EXECUTED**: Astro package unavailable | **NOT EXECUTED**: pagefind extended package unavailable |
| Data source | Original 8 synthetic records, 3 themes | Same source intended; post-build parity unproved | Same generated HTML intended; actual index unproved |
| Search | Shipped JS known from A/F tests; B1's 8-item Python substring baseline verified | JS may be retained; bundling/order must be independently tested | Japanese segmentation/index size/precision/recall must be measured, not assumed |
| Design | A-hybrid P3-A user-preferred layout unchanged | Astro page candidate retains P3-A homepage bytes as working draft | Search integration would require a separate explicit UI decision |
| Dependency risk | No Node/npm external packages needed for runtime | npm package/version/lockfile/security/audit required | npm package/version/extended Japanese index required |
| Performance measurement | 60,102 bytes exact P3-A source; B1 Python substring 10,000 iterations measured locally | NOT_EXECUTED: no build output/bundle stats | NOT_EXECUTED: no index or query stats |
| Security boundary | Static local P3-A only, no real identity | Build-level synthetic public/private segregation can be designed | Must build separate public/member search index; cannot trust visibility filter alone |
| Present technical verdict | BASELINE_LOCAL_READY (not production) | CANDIDATE_UNVERIFIED | CANDIDATE_UNVERIFIED |

No real ranking or vendor adoption can be justified until actual Astro build and Pagefind extended index, Japanese queries, leaked-member negative tests and G4-scoped review are executed. The first P3-A can remain plain static for local demonstration regardless of final stack.

## Measured metrics

All values and test IDs are stored in `evidence/test_expected_actual.json`. `P3A original site bytes` count sums the 16 source files. `B1 public bytes` adds local synthetic formats + experimental JSON, not optimized production output. `Members bytes` represent a fake canary, not access control. Python substring timing at eight records is not a comparative benchmark and must not be generalized to Pagefind or production scale. P3-B1 PoC produced 59 self-checks, not independent evidence.

## Architecture hypothesis

1. Keep immutable originals and strict metadata schema; derive public and members output independently from positive allowlists and different roots.
2. Isolate search indexes per visibility from input selection, not by a UI tab toggle.
3. Do not enable any members package on a public origin. Members Reader/Access JWT/HTTP delivery remain a distinct B2 security/protocol PoC and CT01/CT02 stage hold.
4. If Astro is actually installed, require build output parity and browser history/navigation success on Owner-like Windows browser before adopting it. If failures/maintenance cost outweigh small static benefit, keep vanilla static + generator.
5. Pagefind Extended is only a **candidate** for Japanese text search, not a verified replacement for the original filter semantics. Explicit AND/OR/month/duration/grade filters must remain semantically consistent; Pagefind does not automatically implement the custom compound filter contract.
