# ⚡ IRAM Harness²: Cyclic Agent Workflow & Experience Reflector

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/architecture-Google%20Research%20Harness%C2%B2-cyan.svg)](https://github.com/google-research/harness2)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20AI%20Agents-purple.svg)]()

**IRAM Harness²** is a deterministic, cyclic multi-agent execution loop with an integrated **Experience Reflector**. Inspired by [Google Research Harness²](https://github.com/google-research/harness2), it replaces fragile single-shot agent prompting with a structured state machine:

$$\text{PLAN (Tier 1)} \longrightarrow \text{ACT (Tier 3)} \longrightarrow \text{VERIFY (Tier 2)} \longrightarrow \text{REFLECT} \longrightarrow \text{COMMIT}$$

---

## 🏛️ Tiered Swarm Architecture

```
                                  ┌────────────────────────┐
                                  │   TIER 1: ARCHITECT    │
                                  │   (Decomposition)      │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                  ┌────────────────────────┐
                                  │  TIER 2: COORDINATOR   │
                                  │  (Gate Verification)   │
                                  └───────────┬────────────┘
                                              │
                      ┌───────────────────────┼───────────────────────┐
                      ▼                       ▼                       ▼
              [Worker: Research]      [Worker: Testing]       [Worker: Action]
              Grep & Context Read     Red-Green Gate Assert   Atomic Implementation
```

* **Tier 1 (Architect / High Reasoning)**: Formulates high-level strategy and breaks down complex tasks into atomic technical steps with mandatory verification criteria.
* **Tier 2 (Coordinator / Gatekeeper)**: Enforces verification gates before allowing execution to proceed. Rejects code changes with runtime or lint failures.
* **Tier 3 (Grunt Workers / Parallel Execution)**: Executes fast, low-cost local tool actions, grep lookups, and deterministic tests.
* **Experience Reflector**: Detects bottlenecks, synthesizes root causes from verification warnings, and records episodic memory to prevent repeating mistakes.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/apravint/iram-harness2.git
cd iram-harness2

# Make executable available in PATH
mkdir -p ~/.local/bin
ln -sf $(pwd)/bin/iram-harness2 ~/.local/bin/
```

### 2. Usage

```bash
# Run task through the cyclic verification loop
iram-harness2 "Audit PipeWire sink latency and optimize buffer quantum to 128"

# View past episodic execution traces
iram-harness2 --history
```

---

## 📜 License
MIT License. Created by [Pravin](https://github.com/apravint) for IRAM OS.
