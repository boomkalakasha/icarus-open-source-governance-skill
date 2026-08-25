# Evaluation evidence

`baseline/` preserves the three pre-Skill RED scenarios. `with-skill/` contains a static, documented-only reference rubric after `SKILL.md` exists; it is **not** evidence that a particular model host installed or executed the Skill.

Run `python scripts/run_evals.py` to verify every scenario has its required objective markers. A future host-run evaluation must keep its transcript, host/version, date, prompt, result, and limitations separate from these documented checks.
