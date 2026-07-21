#!/usr/bin/env bash
# Install E++ and the VS Code extension on your Mac

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
echo "Installing E++ from $ROOT"

chmod +x "$ROOT/epp.py"

# Optional: add a shortcut command
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
ln -sf "$ROOT/epp.py" "$BIN_DIR/epp"
echo "Linked epp -> $BIN_DIR/epp"
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
  echo ""
  echo "Add this to your ~/.zshrc so you can type 'epp' anywhere:"
  echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# Install VS Code / Cursor extension
EXT_TARGET="$HOME/.vscode/extensions/eplusplus.eplusplus-0.3.0"
if command -v code >/dev/null 2>&1; then
  echo ""
  echo "Installing E++ VS Code extension..."
  if ! code --install-extension "$ROOT/vscode-extension" --force 2>/dev/null; then
    echo "CLI install failed — linking extension manually..."
    rm -rf "$EXT_TARGET"
    ln -sf "$ROOT/vscode-extension" "$EXT_TARGET"
  fi
  echo "Extension installed!"
elif command -v cursor >/dev/null 2>&1; then
  echo ""
  echo "Installing E++ Cursor extension..."
  cursor --install-extension "$ROOT/vscode-extension" --force
  echo "Extension installed!"
else
  VSCODE_BIN="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
  if [ -x "$VSCODE_BIN" ]; then
    echo ""
    echo "Installing E++ VS Code extension..."
    if ! "$VSCODE_BIN" --install-extension "$ROOT/vscode-extension" --force 2>/dev/null; then
      echo "CLI install failed — linking extension manually..."
      rm -rf "$EXT_TARGET"
      ln -sf "$ROOT/vscode-extension" "$EXT_TARGET"
    fi
    echo "Extension installed!"
  else
    echo ""
    echo "Could not find 'code' or 'cursor' CLI."
    echo "Install the extension manually:"
    echo "  ln -sf \"$ROOT/vscode-extension\" \"$EXT_TARGET\""
  fi
fi

echo ""
echo "Done! Next steps:"
echo "  1. Open this folder in VS Code or Cursor: $ROOT"
echo "  2. Open examples/kids/adventure.epp"
echo "  3. Press Cmd+Shift+B to run (or click the Play button)"
echo "  4. Or run: python3 epp.py examples/kids/adventure.epp"
