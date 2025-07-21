# tests/conftest.py
import sys
import os

# Add the project root (the parent of tests/) to sys.path,
# so `import src…` works even if the CWD is tests/.
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)