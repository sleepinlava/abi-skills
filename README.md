# ABI agent skills

This repository is the standalone distribution point for two ABI agent skills:

- `abi` — the operator skill for discovering, planning, checking, dry-running,
  inspecting, and reporting installed ABI workflows.
- `abi-plugin-development` — the contributor checklist for adding or revising
  ABI workflow modules.

The skills are maintained alongside the ABI core at
[sleepinlava/BAI](https://github.com/sleepinlava/BAI). This repository exists so
skill registries can install them without cloning the full Python project.

## Install

With the open `skills` CLI:

```bash
npx skills add sleepinlava/abi-skills --skill abi
npx skills add sleepinlava/abi-skills --skill abi-plugin-development
```

With Claude Code's self-hosted marketplace:

```bash
claude plugin marketplace add sleepinlava/abi-skills
claude plugin install abi@abi-skills
```

The plugin includes the safe-profile ABI MCP configuration in `.mcp.json`.
The `safe` profile does not expose real workflow execution.

## Scope and limits

The skills are documentation-only. They do not install ABI, analysis plugins,
biological tools, reference databases, Conda environments, or runtime resources.
Installing a skill is not scientific validation, and a successful plan or
dry-run does not prove that a workflow is biologically valid.

Real execution requires an ABI installation with the `full` MCP profile and
explicit confirmation. External tools and databases must be prepared separately
and checked by the operator.

The `abi-plugin-development` skill assumes that the developer has already
selected the workflow, tool versions, and scientific thresholds. It does not
certify a plugin, its resources, or its results.

## Layout

```text
skills/
  abi/SKILL.md
  abi-plugin-development/SKILL.md
.claude-plugin/
  plugin.json
  marketplace.json
.mcp.json
```

Each skill lives in exactly one directory so registries that hash content do not
see duplicate variants. Registry indexing and ranking are controlled by the
individual registry; this repository does not control them.

## Licensing

The repository text is licensed under the MIT license in `LICENSE`. ClawHub
publishes submitted skills under its own MIT-0 terms; that applies only to the
copy published there. The repository copy keeps the MIT license.

## Validation

```bash
npx skills add . --list
claude plugin validate --strict .
python3 scripts/validate_skills.py
```
