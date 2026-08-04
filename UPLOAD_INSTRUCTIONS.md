# GitHub Synchronization Instructions

This package contains the code, documentation, derived audit outputs, notebooks, tests, and v2 report files that are missing from the current public repository.

## Browser upload

1. Extract this ZIP locally.
2. Open the public repository on GitHub.
3. Select **Add file > Upload files**.
4. Drag the extracted package contents into the repository root. Preserve the folder hierarchy.
5. Do not delete the existing `data/raw/` workbooks.
6. Replace older top-level files when GitHub prompts, including `README.md`, `CITATION.cff`, `Makefile`, `requirements.txt`, `pyproject.toml`, and `.gitignore`.
7. Confirm that `docs/scope_change_record.md` is the detailed v2 version.
8. Use a commit message such as:

   `Synchronize interim report v2, audit code, documentation, tests, and derived outputs`

## After upload

- Delete obsolete placeholder files and folders such as `code/sample`, `docs/sample`, and files named only `sample`.
- Confirm that all README links open.
- Open the repository in an incognito window.
- Run the automated tests locally if possible.
- Capture the final GitHub screenshot only after the commit is visible.
