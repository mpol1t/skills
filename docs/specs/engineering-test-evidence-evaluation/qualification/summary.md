# Trial isolation qualification

Before the baseline dispatch, a fresh Codex CLI process used the exact
trial permission profile on an unrelated canary. A child spawned by that
process ran the same shell check. The process and child both exited the
check with code 0. The verifier recorded these outcomes.

| Probe | Observation |
| --- | --- |
| Pinned installed skill copy | Readable both in the parent and child. |
| Local parent spec, existing Codex and Claude skill links, model client credential path | Reads failed in both model sessions. |
| A fixture symlink to a controller-only canary | Read failed in the direct permission-profile check. |
| TCP socket and public GitHub HTTPS request | Unavailable in the parent and child. |
| Managed browser and app tools | Hosted search disabled, apps disabled, and tool inventories for both sessions showed local shell, time, user interaction and in-session collaboration. No web search, GitHub tracker connector, or cross-session history tool appeared. |
| Actual parent and child contexts | Both recorded gpt-6.2-sol at medium with the restricted filesystem profile, restricted network, and approvals set to never. |

The qualification was separate from the 26 planned baseline trials. Each
baseline attempt independently ran the permission-profile check before the
CLI received the neutral prompt. Raw account and runtime metadata stays in
the controller's private logs. The accompanying probe event log preserves
the parent run and reported child result.
