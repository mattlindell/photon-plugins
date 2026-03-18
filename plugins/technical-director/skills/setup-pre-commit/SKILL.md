---
name: setup-pre-commit
description: Use when user wants to add pre-commit hooks in a JavaScript or TypeScript project, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing with Prettier.
---

# Setup Pre-Commit Hooks

## What This Sets Up

- **Husky** pre-commit hook
- **lint-staged** running Prettier (and ESLint if present) on staged files
- **eslint-config-prettier** to prevent ESLint/Prettier conflicts
- **Prettier** config (if missing)
- **typecheck** and **test** scripts in the pre-commit hook

## Steps

### 1. Detect package manager

Check for `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun). Use whichever is present. Default to npm if unclear.

### 2. Install dependencies

Install as devDependencies:

```bash
husky lint-staged prettier eslint-config-prettier
```

### 3. Initialize Husky

```bash
npx husky init
```

This creates `.husky/` dir and adds `prepare: "husky"` to package.json.

### 4. Create `.husky/pre-commit`

Write this file (no shebang needed for Husky v9+):

```bash
npx lint-staged
npm run typecheck
npm run test
```

**Adapt**: Replace `npm` with detected package manager. If repo has no `typecheck` or `test` script in package.json, omit those lines and tell the user.

### 5. Create `.lintstagedrc`

If the project uses ESLint, run both ESLint and Prettier on JS/TS files:

```json
{
  "*.{js,ts,jsx,tsx}": ["eslint --fix", "prettier --write"],
  "*": "prettier --ignore-unknown --write"
}
```

If the project does not use ESLint, use Prettier only:

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. Create `.prettierrc` (if missing)

Only create if no Prettier config exists (check for `.prettierrc`, `.prettierrc.json`, `.prettierrc.js`, `prettier.config.js`, or a `prettier` key in `package.json`).

Copy the default config from `defaults/prettierrc.json` in this skill directory into `.prettierrc` at the project root.

### 7. Configure ESLint for Prettier (if ESLint is present)

If the project has an ESLint config, add `"prettier"` as the **last** item in the `extends` array. This disables ESLint's formatting rules so Prettier owns formatting exclusively.

- For `.eslintrc.json` / `.eslintrc`: add `"prettier"` to the end of `extends`
- For `eslint.config.js` (flat config): add `require('eslint-config-prettier')` as the last config object
- If no ESLint config exists, skip this step

### 8. Verify

- [ ] `.husky/pre-commit` exists and is executable
- [ ] `.lintstagedrc` exists
- [ ] `prepare` script in package.json is `"husky"`
- [ ] `prettier` config exists
- [ ] Run `npx lint-staged` to verify it works

### 9. Commit

Stage all changed/created files and commit with message: `Add pre-commit hooks (husky + lint-staged + prettier)`

This will run through the new pre-commit hooks — a good smoke test that everything works.

## Notes

- Husky v9+ doesn't need shebangs in hook files
- `prettier --ignore-unknown` skips files Prettier can't parse (images, etc.)
- The pre-commit runs lint-staged first (fast, staged-only), then full typecheck and tests
