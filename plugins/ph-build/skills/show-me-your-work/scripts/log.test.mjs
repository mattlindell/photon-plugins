import { afterEach, expect, test } from "bun:test";
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const script = join(import.meta.dir, "log.sh");
const dirs = [];

afterEach(() => {
  for (const dir of dirs.splice(0)) rmSync(dir, { recursive: true, force: true });
});

function repo() {
  const dir = mkdtempSync(join(tmpdir(), "log-sh-"));
  dirs.push(dir);
  const init = spawnSync("git", ["init", "-q"], { cwd: dir, encoding: "utf8" });
  expect(init.status, init.stderr).toBe(0);
  return dir;
}

function log(cwd, logfile) {
  const result = spawnSync("bash", [script, logfile, "frame", "decided", "because", "commit abc", "open"], {
    cwd,
    encoding: "utf8",
  });
  expect(result.status, result.stderr).toBe(0);
}

function untracked(cwd) {
  const result = spawnSync("git", ["status", "--porcelain", "--untracked-files=all"], { cwd, encoding: "utf8" });
  expect(result.status, result.stderr).toBe(0);
  return result.stdout.split("\n").filter(Boolean);
}

test("the first write into .audit/ makes the folder ignore itself", () => {
  const dir = repo();
  log(dir, ".audit/task.tsv");

  expect(readFileSync(join(dir, ".audit", ".gitignore"), "utf8")).toBe("*\n");
  expect(untracked(dir)).toEqual([]);
  expect(existsSync(join(dir, ".gitignore"))).toBe(false);
});

test("an existing .audit/.gitignore is left as it is", () => {
  const dir = repo();
  mkdirSync(join(dir, ".audit"));
  writeFileSync(join(dir, ".audit", ".gitignore"), "task.tsv\n");
  log(dir, ".audit/task.tsv");
  log(dir, ".audit/task.tsv");

  expect(readFileSync(join(dir, ".audit", ".gitignore"), "utf8")).toBe("task.tsv\n");
});

test("an absolute path into .audit/ gets the same rule", () => {
  const dir = repo();
  log(tmpdir(), join(dir, ".audit", "task.tsv"));

  expect(readFileSync(join(dir, ".audit", ".gitignore"), "utf8")).toBe("*\n");
});

test("a log outside .audit/ creates no ignore file", () => {
  const dir = repo();
  log(dir, "logs/task.tsv");
  log(dir, "task.tsv");

  expect(existsSync(join(dir, "logs", ".gitignore"))).toBe(false);
  expect(existsSync(join(dir, ".gitignore"))).toBe(false);
  expect(untracked(dir).sort()).toEqual(["?? logs/task.tsv", "?? task.tsv"]);
});
