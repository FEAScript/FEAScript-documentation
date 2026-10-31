// Runs every Node.js example of FEAScript-core and records its mesh and solution in scripts/.example-results/,
// for generate-example-figures.py. The examples run unchanged; example-results-hook.mjs records each solve().
// FEAScript-core is expected next to this repository and must be built (npm run build) first.
//
//   node scripts/export-example-results.mjs [path/to/FEAScript-core]

import { execFileSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const scriptsDirectory = path.dirname(fileURLToPath(import.meta.url));
const core = path.resolve(process.argv[2] ?? path.join(scriptsDirectory, "..", "..", "FEAScript-core"));
const outputDirectory = path.join(scriptsDirectory, ".example-results");
const hook = path.join(scriptsDirectory, "example-results-hook.mjs");

function findExamples(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) return findExamples(entryPath);
    return entry.name.endsWith(".js") ? [entryPath] : [];
  });
}

fs.rmSync(outputDirectory, { recursive: true, force: true });
fs.mkdirSync(outputDirectory);

for (const example of findExamples(path.join(core, "examples")).sort()) {
  const name = path.basename(example, ".js");
  const output = execFileSync(process.execPath, ["--import", hook, path.basename(example)], {
    cwd: path.dirname(example),
    env: { ...process.env, FEASCRIPT_CORE: core, EXAMPLE_RESULT: path.join(outputDirectory, name) },
    encoding: "utf8",
  });
  fs.writeFileSync(path.join(outputDirectory, `${name}.out`), output);
  console.log(`Recorded ${name}`);
}
