# StageSkip (掃蕩) flow

Sections run in order **Main → Hard → Tour → Leftover**; each can be switched off and falls through
to the next on success or failure. Pipeline is generated: edit `tools/dev/gen_stage_skip.py`, then
`python tools/dev/gen_stage_skip.py`.

Ticket skips count for the 主線 / 困難 / 挑戰 daily missions (not event stages) — one skip each plus the
60-energy mission brings the daily bar from 75 to 100+ (verified 2026-10-17: 165, all chests opened).

| Step | Identified by | Action |
|---|---|---|
| Home → 出擊 | `HomeAnchor` | tap `[290,1110,140,80]` |
| 出擊 → STORY | OCR `STORY` | tap (node retries itself if the tap landed mid-transition) |
| STORY chapter list | header `主線` | agent `goto_stage {stage, hard}` |
| Stage detail | `^速通$` `[215,1185,110,55]` | tap |
| 速通 dialog | `速通次數` | agent `sweep_set_count {count}` (+ ×(n−1), or max when 0) |
| | `^確定$` `[380,765,160,55]` | tap |
| 速通結果 | `速通結果` + `^完成$` | tap 完成 |
| Any 「…不足」 prompt | `不足` + `^取消$` | tap 取消 — spend guard |
| 出擊 → CHALLENGE → 觀光工坊 | `ALLENGE\|^挑戰$`, `觀光工坊` | tap |
| 推薦 switch | `^OFF$` → tap; `^ON$` → continue | only the highest level per folder shows |
| Folder | `^.{2}工坊$` (locked folders are cut by a lock icon) | tap to expand |
| Level | `工坊.?LV.?[0-9]+` | tap, then sweep with max (all attempts) |

`goto_stage` (agent/stage_nav.py): toggles 普通/困難 via the bottom switch, finds the chapter by
OCR'ing the big number beside each chapter title (`StageNav_ChapterNumber`, only_rec), then scrolls
the stage path until `(?<![\d-])C-S$` matches (`困難11-4` for hard). Lists slide in when opened, so it
waits 2 s and re-checks once before scrolling.

Stage labels: main `11-36` (10 energy, ≤16/day by energy), hard `困難11-4` (20 energy, 3/day),
觀光工坊 玩具工坊 LV15 (20 energy, 3 attempts shared; 果凍工坊 on 二四六日). 健身中心 skipped (user),
秘境探險 not skippable.

Live (2026-10-17): main 11-36 ×1 ✓ 66 s · hard 11-4 ×1 ✓ · 觀光工坊 max ✓ 65 s.
Bugs found live: agent needs `register_sink` to reach the controller; controller handle must be
fetched fresh per call inside actions; menu taps during slide-in animations get lost.
