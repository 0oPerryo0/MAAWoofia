# FriendPoke (好友 → 頂一下) flow — optional, off by default

Once per friend per day (user); tapping again is harmless and gives no visual feedback, so the task
taps every 頂一下 and scrolls until a page shows no new friend names.

| Screen | Identified by | Action |
|---|---|---|
| Home | `HomeAnchor` | tap 好友 in left bar `[10,345,65,75]` |
| FRIENDS (追蹤清單) | OCR `FRIENDS` header | agent `poke_all_friends` |

`poke_all_friends` (agent/friend_poke.py): OCR the list (`FriendPoke_OCR`), tap the icon 18 px above
each `頂一下` label, collect names (text starting at x 215–235), swipe up; stop when no new names.

Live (2026-10-17): 15 friends, all pages poked → home ✓ 51 s.
