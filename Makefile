.PHONY: install run debug clean lint lint-strict
.DEFAULT_GOAL: run
PY = python3

FLAKE8 = uv run $(PY) -m flake8 . --exclude=.venv/
MYPY = uv run $(PY) -m mypy .
MYPYFLAGS = --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs \
	--disallow-subclassing-any
FORCE_MAZEGEN = UV_SKIP_WHEEL_FILENAME_CHECK=1 

run: install
	@$(FORCE_MAZEGEN) uv run --quiet $(PY) -m src

debug: install
	$(FORCE_MAZEGEN) uv run $(PY) -m pdb -m src -v

install:
	@$(FORCE_MAZEGEN) uv sync

lint:
	-@$(FORCE_MAZEGEN) $(FLAKE8)
	-@$(FORCE_MAZEGEN) $(MYPY) $(MYPYFLAGS)

lint-strict:
	-@$(FORCE_MAZEGEN) $(FLAKE8)
	-@$(FORCE_MAZEGEN) $(MYPY) --strict

clean:
	-find . -type d -name "__pycache__" -exec rm -rf {} +
	-find . -type d -name ".mypy_cache" -exec rm -rf {} +
	-find . -type d -name ".pytest_cache" -exec rm -rf {} +
