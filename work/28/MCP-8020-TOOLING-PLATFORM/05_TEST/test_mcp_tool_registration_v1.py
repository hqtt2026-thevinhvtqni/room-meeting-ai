import unittest
from mcp_tool_registration_v1 import register_work28_tools
from runtime_tools_v1 import RuntimeToolsV1
from sandbox_tools_v1 import SandboxToolsV1
from github_tools_v1 import GitHubToolsV1


class FakeMCP:
    def __init__(self):
        self.registered = {}
    def tool(self, name):
        def decorate(handler):
            self.registered[name] = handler
            return handler
        return decorate


class RegistrationTests(unittest.TestCase):
    def test_registers_all_13_named_tools(self):
        mcp = FakeMCP()
        names = register_work28_tools(
            mcp, RuntimeToolsV1(None), SandboxToolsV1(None), GitHubToolsV1(None))
        self.assertEqual(len(names), 13)
        self.assertEqual(set(names), set(mcp.registered))
        self.assertIn("execution_submit", names)
        self.assertIn("sandbox_search", names)
        self.assertIn("github_update_file", names)

    def test_rejects_missing_mcp_decorator(self):
        with self.assertRaises(TypeError):
            register_work28_tools(
                object(), RuntimeToolsV1(None), SandboxToolsV1(None), GitHubToolsV1(None))


if __name__ == "__main__":
    unittest.main()
