# Fork pstack rather than depend on it

`pstack-claude` is MIT and actively maintained, and composing with it as an
installed peer plugin would have cost nothing to set up. We forked it into
`ph-build` anyway, at upstream v0.9.27, because the changes we need are not
patches on top of it — they are a different theory of where certainty comes from.
pstack buys confidence with compute; our planning front-end buys it with human
thinking done up front, and nothing in pstack can detect that the thinking already
happened.

## Considered options

**Depend on it as a peer plugin.** Rejected. Upstream is itself a port of Lauren
Tan's Cursor pstack plus seven `cursor-team-kit` skills, tracked through
`tools/sync.mjs` against two pinned SHAs with a substitution table. Every
core-level change we want — softening the autonomy stance, capping fan-out,
threading a rigor signal through the playbooks — lands in exactly the files a
three-way merge would conflict on, forever.

**Keep the fork tracked.** Rejected for the same reason. A sync tool whose every
run conflicts in the files we care most about is a tax with no yield.

## Consequences

- We own the imported material outright, including bugs we did not write.
- Upstream improvements arrive only if someone reads the changelog and ports them
  by hand. That is the accepted cost.
- Two upstream copyrights travel with the code and must be preserved: Lauren Tan
  (pstack) and Cursor (`cursor-team-kit`). See `plugins/ph-build/NOTICE.md`, which
  pins the fork SHA.
- Model tuning alone could not have solved the cost problem. Agent count is set by
  the playbooks, not by the model map, so the fix had to reach content we do not
  control upstream.
