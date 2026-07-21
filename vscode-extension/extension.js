const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const { execFile } = require("child_process");

function getProjectRoot(document) {
  const folder = vscode.workspace.getWorkspaceFolder(document.uri);
  return folder ? folder.uri.fsPath : path.dirname(document.fileName);
}

function getWorkspaceRoot() {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) {
    return null;
  }
  return folders[0].uri.fsPath;
}

function runEpp(document) {
  const root = getProjectRoot(document);
  const runner = path.join(root, "epp.py");
  const file = document.fileName;

  const term = vscode.window.createTerminal("E++");
  term.show();
  term.sendText(`python3 "${runner}" "${file}"`);
}

function nextExamplePath(root) {
  const direct = path.join(root, "example.epp");
  if (!fs.existsSync(direct)) {
    return direct;
  }

  for (let i = 2; i < 1000; i += 1) {
    const candidate = path.join(root, `example${i}.epp`);
    if (!fs.existsSync(candidate)) {
      return candidate;
    }
  }

  return path.join(root, `example-${Date.now()}.epp`);
}

async function newEppFile() {
  const root = getWorkspaceRoot();
  if (!root) {
    vscode.window.showErrorMessage("Open the eplusplus folder in VS Code first.");
    return;
  }

  const templatePath = path.join(root, "templates", "example.epp");
  const targetPath = nextExamplePath(root);

  if (!fs.existsSync(templatePath)) {
    vscode.window.showErrorMessage("Could not find templates/example.epp in this project.");
    return;
  }

  fs.copyFileSync(templatePath, targetPath);
  const doc = await vscode.workspace.openTextDocument(targetPath);
  await vscode.window.showTextDocument(doc);

  vscode.window.showInformationMessage(`Created ${path.basename(targetPath)} — press Cmd+Shift+B to run!`);
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("epp.runFile", () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor || editor.document.languageId !== "epp") {
        vscode.window.showWarningMessage("Open an E++ (.epp) file first.");
        return;
      }
      runEpp(editor.document);
    }),
    vscode.commands.registerCommand("epp.newFile", newEppFile)
  );
}

function deactivate() {}

module.exports = { activate, deactivate };
