# pr-review

Review the PR before merge.

Do not edit files.

Check:

* changed files
* scope vs non-scope
* forbidden files
* docs-only vs code changes
* build/test/lint evidence when applicable
* documentation impact
* known warnings
* merge readiness

Maretech-specific checks:

* no diagnosis language introduced
* no survey-replacement language introduced
* Osmosis and Corrosion remain separate
* app and marketing site workstreams remain separate
* async-only inference assumption is not weakened
* no generated/local files included
* no **pycache** files included

Return:

* mergeable: yes/no
* blockers
* non-blocking notes
* recommended next action
