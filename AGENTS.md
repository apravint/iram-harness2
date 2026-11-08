# AGENTS.md - Developer & AI Agent Guide for iram-harness2 🤖

## 🎯 Repository Overview
**iram-harness2**: IRAM Harness² is a deterministic, cyclic multi-agent execution loop with an integrated Experience Reflector. Inspired by Google Research Harness², it replaces fragile single-shot agent prompting with a structured state machine: $$\text{PLAN (Tier 1)} \longrightarrow \text{ACT (Tier 3)} \longrightarrow \text{VERIFY (Tier 2)} \longrightarrow \text{REFLECT} \longrightarrow \text{COMMIT}$$

---

## 🏗️ Repository Architecture
Key directories and entrypoints: `LICENSE, README.md, bin/, harness2/`.

### Tech Stack & Runtime
- **Target Platform:** Linux / Wayland / Hyprland (Ubuntu 26.10, systemd)
- **Scripting:** POSIX Bash / Shell (`set -euo pipefail`)

## ⚙️ Executable Verification Commands

### 1. Shell Syntax Validation
```bash
bash -n $(find . -maxdepth 3 -name '*.sh' -not -path '*/.*')
```

### 2. ShellCheck Linting
```bash
shellcheck $(find . -maxdepth 3 -name '*.sh' -not -path '*/.*')
```

### 3. Dry-Run or Help Verification
```bash
./install.sh --dry-run || ./install.sh --help
```

---

## 🛡️ Coding & Safety Guidelines for Autonomous Agents

1. **Documentation Integrity:** Preserve all existing docstrings, header comments, and licensing banners. Never delete context unless specifically instructed.
2. **Zero Hardcoded Secrets:** Never embed API keys, OAuth tokens, personal access tokens, or sensitive credentials in committed files. Read credentials exclusively from environment variables or secure credential paths.
3. **Git Hygiene:**
   - Do not force-push (`git push --force`) or execute destructive resets.
   - Never modify root git configurations or harness infrastructure outside task scope.
   - Keep git diffs atomic, focused, and verified before committing.
4. **Agent Workflow Protocol:**
   - **Plan:** Inspect codebase architecture and dependencies before editing.
   - **Act:** Make minimal, clean, high-precision changes.
   - **Verify:** Run the appropriate verification commands listed above.
   - **Reflect:** Confirm zero regressions and review `git diff`.

---
*Maintained by Ayyappa Pravin • Built for Antigravity, Claude, Cursor & Autonomous AI Agents.*
