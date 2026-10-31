// Preloaded by export-example-results.mjs: records the mesh and the solution of every solve() call of a
// FEAScript-core example, without changing the example. FEASCRIPT_CORE is the FEAScript-core directory and
// EXAMPLE_RESULT the output file (without the extension; a counter is appended for each solve)
import fs from "fs";

const core = process.env.FEASCRIPT_CORE;
const { FEAScriptModel } = await import(`${core}/dist/feascript.esm.js`);
const { prepareMesh } = await import(`${core}/src/mesh/meshUtils.js`);

let solveCount = 0;
const originalSolve = FEAScriptModel.prototype.solve;

FEAScriptModel.prototype.solve = function (...args) {
  const result = originalSolve.apply(this, args);
  const meshData = prepareMesh(this.meshConfig);
  const { parsedMesh, ...meshConfig } = this.meshConfig;
  const fields = result.fields
    ? Object.fromEntries(Object.entries(result.fields).map(([name, values]) => [name, Array.from(values)]))
    : null;

  fs.writeFileSync(
    `${process.env.EXAMPLE_RESULT}-${solveCount++}.json`,
    JSON.stringify({
      solverConfig: this.solverConfig,
      meshConfig,
      gmsh: Boolean(parsedMesh),
      boundaryConditions: this.boundaryConditions,
      elementOrder: meshData.elementOrder,
      elementShape: meshData.elementShape,
      nop: meshData.nop,
      x: Array.from(meshData.nodesXCoordinates),
      y: meshData.nodesYCoordinates ? Array.from(meshData.nodesYCoordinates) : null,
      solution: Array.from(result.solutionVector),
      fields,
    }),
  );
  return result;
};
