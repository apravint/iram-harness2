#!/usr/bin/env python3
"""
IRAM Harness²: Cyclic Agent Workflow & Experience Reflector
Inspired by Google Research Harness² and Multi-Agent Orchestration.
https://github.com/apravint/iram-harness2
"""

import sys
import os
import json
import time
import urllib.request
import subprocess
from typing import Dict, List, Any, Optional

STATE_DIR = os.path.expanduser("~/.local/state/iram/harness2")
os.makedirs(STATE_DIR, exist_ok=True)

# ANSI Colors
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
RED = "\033[0;31m"
BOLD = "\033[1m"
NC = "\033[0m"


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    conf_path = os.path.expanduser("~/.config/environment.d/20-gemini.conf")
    if os.path.exists(conf_path):
        try:
            with open(conf_path, "r") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        return line.strip().split("=", 1)[1].strip('"').strip("'")
        except Exception:
            pass
    return ""


def call_llm(model: str, prompt: str, system_prompt: str = "") -> str:
    """Unified LLM interface supporting Gemini cloud and Ollama local fallback."""
    api_key = get_api_key()
    if api_key and ("gemini" in model.lower() or "pro" in model.lower() or "flash" in model.lower()):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        payload: Dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        if system_prompt:
            payload["systemInstruction"] = {"parts": [{"text": system_prompt}]}
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "x-goog-api-key": api_key}
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            pass

    # Fallback to local Ollama
    ollama_url = "http://localhost:11434/api/generate"
    ollama_model = os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b")
    payload = {
        "model": ollama_model,
        "prompt": f"{system_prompt}\n\nTask: {prompt}" if system_prompt else prompt,
        "stream": False
    }
    try:
        req = urllib.request.Request(
            ollama_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as e:
        return f"[Fallback Execution Error: {e}]"


class HarnessWorkflow:
    """
    Cyclic State Machine & Experience Reflector.
    Cycle: PLAN -> ACT -> VERIFY -> REFLECT -> COMMIT
    """
    def __init__(self, task: str, max_iterations: int = 3, verbose: bool = False):
        self.task = task
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.run_id = f"harness_{int(time.time())}"
        self.trace: List[Dict[str, Any]] = []

    def plan_phase(self) -> Dict[str, Any]:
        """Tier 1: Architect decomposes goal into testable steps with verification criteria."""
        print(f"\n{BOLD}{MAGENTA}🧠 [Phase 1: Architect Decomposition (Tier 1)]{NC}")
        print(f"   Goal: {self.task}")

        sys_prompt = (
            "You are the Lead Systems Architect in Harness². "
            "Decompose the task into 2 to 4 atomic technical steps. "
            "For each step, specify the task description and strict verification criterion. "
            "Respond ONLY in valid JSON: {\"summary\": \"...\", \"steps\": [{\"id\": 1, \"task\": \"...\", \"verify\": \"...\"}]}"
        )
        model = os.environ.get("TIER1_MODEL", "gemini-2.5-pro")
        resp = call_llm(model, self.task, sys_prompt)

        try:
            cleaned = resp.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            plan = json.loads(cleaned.strip())
        except Exception:
            plan = {
                "summary": "Direct execution sequence",
                "steps": [
                    {"id": 1, "task": f"Analyze scope and codebase for: {self.task}", "verify": "Context established"},
                    {"id": 2, "task": f"Apply implementation for: {self.task}", "verify": "Zero exit error code"},
                    {"id": 3, "task": "Verify system stability and syntax integrity", "verify": "All verification assertions hold"}
                ]
            }

        print(f"   ✓ Plan formulated with {len(plan['steps'])} phases.")
        for s in plan["steps"]:
            print(f"     • Step {s['id']}: {s['task']} \033[2m(Verify: {s['verify']})\033[0m")
        return plan

    def act_phase(self, step: Dict[str, Any]) -> str:
        """Tier 3: Grunt Worker executes atomic action."""
        model = os.environ.get("TIER3_MODEL", "gemini-3.5-flash-lite")
        prompt = step["task"]
        sys_prompt = "You are a Grunt Worker in Harness². Execute the task and provide concise technical results."
        return call_llm(model, prompt, sys_prompt)

    def verify_phase(self, step: Dict[str, Any], result: str) -> bool:
        """Tier 2: Coordinator performs gate review against verification criterion."""
        coord_model = os.environ.get("TIER2_MODEL", "gemini-2.5-flash")
        verify_prompt = (
            f"Step: {step['task']}\n"
            f"Verification Criterion: {step['verify']}\n"
            f"Result: {result[:1200]}\n"
            "Does the result satisfy the verification criterion? Reply YES or NO followed by 1 brief sentence."
        )
        verdict = call_llm(coord_model, verify_prompt)
        passed = "YES" in verdict.upper()
        return passed

    def reflect_phase(self, failures: List[Dict[str, Any]]) -> str:
        """Experience Reflector analyzes bottlenecks or past mistakes."""
        print(f"\n{BOLD}{YELLOW}🔄 [Phase 4: Experience Reflector]{NC}")
        reflector_prompt = (
            f"The following steps had verification warnings: {json.dumps(failures)}\n"
            "Synthesize an ADR / operational reflection note explaining how to prevent this in future runs."
        )
        return call_llm("gemini-2.5-pro", reflector_prompt)

    def run(self) -> Dict[str, Any]:
        t0 = time.time()
        plan = self.plan_phase()
        results = []
        failures = []

        print(f"\n{BOLD}{BLUE}⚙️  [Phase 2 & 3: Act & Verification Loop]{NC}")
        for step in plan["steps"]:
            print(f"   ▶ Dispatching Step {step['id']}: {step['task']}")
            res = self.act_phase(step)
            passed = self.verify_phase(step, res)

            status_str = f"{GREEN}✓ Passed{NC}" if passed else f"{YELLOW}⚠ Review Warning{NC}"
            print(f"     └─ Gate Check: {status_str}")

            step_record = {
                "step": step,
                "result": res[:300],
                "verified": passed
            }
            results.append(step_record)
            if not passed:
                failures.append(step_record)

        reflection = ""
        if failures:
            reflection = self.reflect_phase(failures)
            print(f"   • Reflection Note: {reflection[:160]}...")

        # Record trace
        trace_file = os.path.join(STATE_DIR, f"{self.run_id}.json")
        summary = {
            "run_id": self.run_id,
            "task": self.task,
            "duration": time.time() - t0,
            "steps_count": len(results),
            "all_passed": len(failures) == 0,
            "results": results,
            "reflection": reflection
        }
        with open(trace_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n{BOLD}{GREEN}🏁 [Harness² Execution Finished]{NC}")
        print(f"   • Completed in {summary['duration']:.2f}s")
        print(f"   • Episodic Trace Saved: {trace_file}")
        return summary
