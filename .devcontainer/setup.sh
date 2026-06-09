#!/usr/bin/env bash
set -Eeuo pipefail

log() {
  echo
  echo "==> $*"
}

# このsetup.sh自身の場所からリポジトリルートを推定する。
# /workspaces/xxx のような固定パスは使わない。
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

export DEBIAN_FRONTEND=noninteractive

# ユーザー領域のnpm/pipxを使う。
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$HOME/bin:/usr/local/bin:$PATH"

mkdir -p "$HOME/.npm-global" "$HOME/.local/bin" "$HOME/bin"

append_path_once() {
  local file="$1"
  local marker="$2"

  touch "$file"

  if ! grep -q "$marker" "$file"; then
    cat <<'EOF' >> "$file"

# Codespaces classroom tools path
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$HOME/bin:/usr/local/bin:$PATH"
EOF
  fi
}

append_path_once "$HOME/.bashrc" "Codespaces classroom tools path"
append_path_once "$HOME/.profile" "Codespaces classroom tools path"

log "Installing apt packages"

sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  git \
  jq \
  ripgrep \
  fd-find \
  tree \
  build-essential \
  pkg-config \
  unzip \
  less

if command -v fdfind >/dev/null 2>&1 && ! command -v fd >/dev/null 2>&1; then
  sudo ln -sf "$(command -v fdfind)" /usr/local/bin/fd
fi

log "Installing Antigravity CLI"

install_antigravity_cli() {
  local before_path
  before_path="$(command -v agy || true)"

  if [ -z "$before_path" ]; then
    local tmpdir
    tmpdir="$(mktemp -d)"

    curl -fsSL https://antigravity.google/cli/install.sh -o "$tmpdir/install-antigravity.sh"
    bash "$tmpdir/install-antigravity.sh"
  fi

  export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$HOME/bin:/usr/local/bin:$PATH"
  hash -r || true

  local agy_bin
  agy_bin="$(command -v agy || true)"

  if [ -z "$agy_bin" ]; then
    agy_bin="$(
      find "$HOME" "$WORKSPACE_DIR" -type f -name agy 2>/dev/null | head -n 1 || true
    )"
  fi

  if [ -z "$agy_bin" ]; then
    echo "ERROR: agy binary was not found after installation."
    echo "Searched:"
    echo "  $HOME"
    echo "  $WORKSPACE_DIR"
    return 1
  fi

  chmod +x "$agy_bin" || true

  # ここが重要。
  # agyをユーザーPATHや作業ディレクトリ依存にせず、必ず /usr/local/bin/agy に固定する。
  sudo ln -sf "$agy_bin" /usr/local/bin/agy
  sudo chmod +x /usr/local/bin/agy

  hash -r || true

  if ! command -v agy >/dev/null 2>&1; then
    echo "ERROR: /usr/local/bin/agy was created, but agy is still not available."
    return 1
  fi

  echo "Antigravity CLI available as: $(command -v agy)"
}

install_antigravity_cli

log "Setting up Python tools"

python3 -m pip install --user --upgrade pip pipx

export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$HOME/bin:/usr/local/bin:$PATH"

python3 -m pipx ensurepath || true

install_pipx_tool() {
  local tool="$1"

  if command -v "$tool" >/dev/null 2>&1; then
    echo "$tool already available: $(command -v "$tool")"
  else
    pipx install "$tool"
  fi
}

install_pipx_tool uv
install_pipx_tool ruff
install_pipx_tool mypy
install_pipx_tool pytest
install_pipx_tool ipython

log "Setting up Node / TypeScript tools"

npm config set prefix "$HOME/.npm-global"

export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$HOME/bin:/usr/local/bin:$PATH"

npm install -g \
  pnpm \
  typescript \
  tsx \
  ts-node \
  eslint \
  prettier \
  vitest

log "Configuring Git defaults"

git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor "code --wait"

log "Installed versions"

echo "--- Git ---"
git --version || true

echo
echo "--- GitHub CLI ---"
gh --version | head -n 1 || true

echo
echo "--- Python ---"
python3 --version || true
pipx --version || true
uv --version || true
ruff --version || true
mypy --version || true
pytest --version || true

echo
echo "--- Node / TypeScript ---"
node --version || true
npm --version || true
pnpm --version || true
tsc --version || true
tsx --version || true
eslint --version || true
prettier --version || true
vitest --version || true

echo
echo "--- Antigravity CLI ---"
echo "agy path: $(command -v agy)"
agy --help | head -n 20 || true

log "Setup complete"

echo "Antigravity CLI is now available from any directory:"
echo "  agy"