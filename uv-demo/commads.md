# Install uv if not already
pip install uv

# Init a project
uv init

# Add packages (equivalent of pip install)
uv add requests fastapi

# This creates uv.lock + pyproject.toml
uv sync        # installs everything from lock file (like pip install -r)
uv run main.py # runs in the managed env