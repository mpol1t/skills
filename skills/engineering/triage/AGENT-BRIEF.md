# Writing Agent Briefs

A designated agent brief comment is the authoritative contract for the Issue or PR; the original body and superseded discussion provide context. Keep the AI disclaimer required by the triage entry point, the `## Agent Brief` wrapper, and the category role.

## Implementation Issues

Call the Skill tool with "issue-brief" to compose the body, unless already loaded for this step. It owns the format, conditional detail, authority interpretation, navigation hints, and material-gap check. Keep those rules there rather than maintaining a second template here. Use the shared brief beneath the wrapper and category. A ready-for-human Issue uses the same information contract, with the reason it needs human work made explicit.

## PR remediation

A PR brief describes what remains to do to the existing diff: finish it, close gaps, or address review points. Preserve that scope rather than treating it as a fresh implementation Issue. State current and desired behavior, relevant interfaces, independently verifiable acceptance criteria, and exclusions. A ready-for-human brief explains why the next step needs a human.

Name behavioral contracts and relevant interfaces rather than prescribing edits against an assumed implementation layout. Avoid line-number instructions. Keep the existing category and state meanings; the Issue-format skill does not redefine this PR workflow.

### Good agent brief (PR)

For a PR, "Current behavior" describes the state of the diff, and the brief asks the agent to finish or fix it rather than build from scratch.

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** Finish the contributor's `--json` output flag for `triage list`

**Current behavior:**
The PR adds a `--json` flag that serializes the issue list to JSON. The happy
path works and the diff matches the project's command structure. Two gaps
remain: errors are still printed as human text (not JSON), and the new flag has
no test coverage.

**Desired behavior:**
With `--json`, all output (including errors) is well-formed JSON on stdout,
and the command's exit codes are unchanged. The existing human-readable output
is untouched when the flag is absent.

**Key interfaces:**
- The command's error path should emit `{ "error": string }` under `--json`
  instead of the plain-text error
- Reuse the existing serializer the PR already added; don't introduce a second

**Acceptance criteria:**
- [ ] `triage list --json` emits valid JSON for both success and error cases
- [ ] Exit codes match the non-JSON command
- [ ] A test covers the `--json` success output and one error case
- [ ] Default (non-JSON) output is byte-for-byte unchanged

**Out of scope:**
- Adding `--json` to any other command
- Changing the JSON shape of the success payload the PR already defined
```
