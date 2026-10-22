# Merge and restack safety

Use this reference with [Shipping](../playbooks/shipping.md) and before any topology change to a stack. Keep the existing watcher responsible for CI and blocker classification. These operations add revision and destination checks; they do not grant merge authority.

## Read both pending mechanisms

A PR can carry two pending-merge mechanisms: GitHub auto-merge and merge-queue membership. The watcher and these reads share one landing revision: the repository, PR number, head OID, base branch, and base OID. Record it with the verification evidence.

```sh
gh pr view "$pr" --repo "$owner/$repo"   --json state,headRefOid,baseRefName,autoMergeRequest,mergeCommit > "$record_file"
```

Read queue membership through GraphQL `pullRequest.mergeQueueEntry`, which `gh pr view --json` may not expose. Treat a missing field or an unsupported API as unknown, never as an absent request. Read the base branch OID separately (`gh api repos/$owner/$repo/git/ref/heads/$base --jq .object.sha`) and add it to the record.

Cancel in this order, rereading after each step:

```sh
gh pr merge "$pr" --repo "$owner/$repo" --disable-auto
```

Then, if `mergeQueueEntry` is non-null, remove the PR with the GraphQL `dequeuePullRequest` mutation. Reread the PR and confirm both mechanisms are absent on the same open head and base. Only that readback permits the planned topology operation. If the PR is no longer open, the head or base moved, or either mechanism is still present, stop and reconcile before rewriting. Do not replace the saved record to bypass a mismatch. Cancellation neither merges nor grants landing authority.

Establish the affected dependency chain and coordinate its topology writer first. Inspect and cancel each affected PR, including descendants whose context will change, and leave unrelated PRs alone. Cancellation is an observed condition, not a lock against another actor rearming afterward. If state changes, stop and reconcile. Origin needs its own equivalent validated operation through its installed service. These commands are GitHub-specific and must not be presented as Origin support.

## Preserve concurrent writes and child changes

Capture the remote branch SHA before rewriting with `git ls-remote --exit-code origin "refs/heads/$branch"`, and validate that exactly the intended ref was returned. Keep that SHA in the operation record. An implicit lease or a prior read alone is insufficient; a background fetch can move a tracking ref.

After confirming the parent squash landed in the intended destination, fetch trunk and identify the recorded old parent tip on which this child was built. Verify it is an ancestor of the child and inspect `old-parent..child` to confirm the range contains only child work. If it does not, reconstruct the boundary before proceeding. Never infer it from the parent's new squash commit.

```sh
git merge-base --is-ancestor "$old_parent_tip" "$child"
git rebase --onto "$trunk_tip" "$old_parent_tip" "$child"
git push --force-with-lease="refs/heads/$child:$captured_remote_head" \
  origin "HEAD:refs/heads/$child"
```

Run the rebase in the child's clean worktree, where `HEAD` is the prepared child. This excludes the parent's old commits. Inspect the resulting diff and content, reassess review applicability, and run checks at the new head. If the lease refuses the push, fetch and reconcile the concurrent work; do not refresh the lease and retry the overwrite blindly. Retarget only after cancellation has been verified. Keep the recorded boundary for each remaining child when preparing later levels.

## What the service guards

GitHub's immediate merge head condition is `--match-head-commit` in `gh`, `expectedHeadOid` in GraphQL `mergePullRequest`, or `sha` in the REST merge endpoint. Use one, carrying the exact verified SHA. None of these supplies an expected base-branch condition. Observe the base immediately before and after and coordinate retargeting; do not call those observations atomic.

A queue or automatic request may outlive its admission revision. Use it only when existing repository rules enforce the required verification for the eventual revision and merge context. A prose verdict or a green check on an older head is not such a gate. If those guarantees cannot be established, keep watching for an immediate guarded merge. If the repository requires a queue, stop at that unmet gate rather than bypassing protection.

After a merge, confirm state `MERGED`, the approved final head, the intended base, and a non-null merge commit. Fetch the destination and run `git merge-base --is-ancestor "$merge_commit" "$destination_tip"`; then check resulting content before advancing. If the service cannot report the relevant facts, the outcome remains unconfirmed.

Service references: [GitHub CLI merge flags](https://cli.github.com/manual/gh_pr_merge), [GraphQL pull requests and queue mutations](https://docs.github.com/en/graphql/reference/pulls), and [REST merge endpoint](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request). Recheck installed service capabilities when these differ. Test service behavior in a disposable repository, never with production PRs.
