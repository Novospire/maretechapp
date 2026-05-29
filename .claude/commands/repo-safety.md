# repo-safety

Check repository safety only.

Do not edit files.

Report:

* current branch
* git status
* latest commits
* changed files
* untracked files
* whether it is safe to proceed
* risks or stop conditions

Maretech-specific checks:

* no generated/local files should be committed
* no `__pycache__` files should be present
* docs-only tickets must not touch app/, tests/, backend/API, auth, database, deployment or package files
* Maretech non-negotiables must remain intact

Stop if working tree is dirty and the dirty files are not part of the current ticket.
