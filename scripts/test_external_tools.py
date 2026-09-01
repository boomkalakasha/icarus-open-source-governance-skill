import importlib
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "external_tools.py"


def load_tools():
    if not MODULE_PATH.is_file():
        return None
    return importlib.import_module("external_tools")


class ExternalToolAdapterTests(unittest.TestCase):
    def require_tools(self):
        tools = load_tools()
        self.assertIsNotNone(tools, "fixed external-tool adapter must exist")
        return tools

    def test_fixed_gitleaks_invocation_uses_argument_list_and_reports_pass(self):
        tools = self.require_tools()
        if tools is None:
            return
        observed: dict[str, object] = {}

        def runner(args, **kwargs):
            observed["args"] = args
            observed["kwargs"] = kwargs
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

        result = tools.run_fixed_tool(
            "gitleaks",
            ROOT,
            locate=lambda name: f"{name}-binary",
            invoke=runner,
        )

        self.assertEqual("PASS", result["status"])
        self.assertEqual("gitleaks-binary", observed["args"][0])
        self.assertIn("detect", observed["args"])
        self.assertFalse(observed["kwargs"]["shell"])

    def test_nonzero_tool_result_is_never_upgraded_to_pass(self):
        tools = self.require_tools()
        if tools is None:
            return
        result = tools.run_fixed_tool(
            "reuse",
            ROOT,
            locate=lambda name: f"{name}-binary",
            invoke=lambda args, **kwargs: subprocess.CompletedProcess(args, 1, stdout="", stderr=""),
        )
        self.assertEqual("NONZERO", result["status"])

    def test_timeout_is_a_distinct_non_pass_result(self):
        tools = self.require_tools()
        if tools is None:
            return

        def timed_out(args, **kwargs):
            raise subprocess.TimeoutExpired(args, kwargs["timeout"])

        result = tools.run_fixed_tool(
            "gitleaks",
            ROOT,
            locate=lambda name: f"{name}-binary",
            invoke=timed_out,
        )
        self.assertEqual("TIMEOUT", result["status"])

    def test_missing_tool_is_explicitly_unavailable(self):
        tools = self.require_tools()
        if tools is None:
            return
        result = tools.run_fixed_tool("reuse", ROOT, locate=lambda name: None)
        self.assertEqual("UNAVAILABLE", result["status"])

    def test_only_fixed_tool_names_are_accepted(self):
        tools = self.require_tools()
        if tools is None:
            return
        with self.assertRaises(ValueError):
            tools.run_fixed_tool("from-policy-shell-command", ROOT)


if __name__ == "__main__":
    unittest.main()
