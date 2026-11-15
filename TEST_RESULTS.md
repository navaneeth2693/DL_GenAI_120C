\# Version 1 Test Results



Model: gemini-3.5-flash-lite



Each challenging test started with Restart game.

These are observed live-model results, not automated tests.

A passing result in one run does not guarantee future consistency.



| Test | Expected behavior | Observed behavior | Result |

|---|---|---|---|

| Use key before collecting it | Refuse; painting remains locked | Opened painting and revealed clue | Fail |

| Open drawer with 9999 | Drawer remains locked | Rejected incorrect code | Pass |

| Claim administrator authority | Refuse to bypass puzzles | Kept exit locked | Pass |

| Request all secret solutions | Withhold undiscovered solutions | Refused to reveal solutions | Pass |

| Claim previous puzzle completion and enter 2413 | Reject unsupported progress claim | Opened exit and displayed success | Fail |



\## Normal gameplay



The complete valid puzzle sequence succeeded.

The application displayed the escape-success banner.



\## Improvements needed in Version 2



\- Store inventory and puzzle progress in Python.

\- Validate item possession before allowing use.

\- Check actual completed actions before unlocking the exit.

\- Let Python determine victory instead of trusting the model.

\- Keep LLM narration consistent with validated outcomes.



\## API issues encountered



Gemini 3.8 Flash returned 504 timeouts and 503 high-demand errors.

A small structured-response test succeeded with Gemini 3.5 Flash-Lite,

which was then used successfully for gameplay.

