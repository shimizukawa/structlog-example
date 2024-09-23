# setup
set -ex

curl -LsSf https://astral.sh/uv/install.sh | sh
. $HOME/.cargo/env
uv sync
