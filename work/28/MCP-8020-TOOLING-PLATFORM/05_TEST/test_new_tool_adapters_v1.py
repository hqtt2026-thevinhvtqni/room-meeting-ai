"""Unit tests for Work 28 v1 runtime, sandbox and GitHub tool adapters."""
import unittest
from runtime_tools_v1 import RuntimeToolsV1, InvalidToolRequest, ToolBlocked
from sandbox_tools_v1 import SandboxToolsV1, InvalidSandboxRequest, SandboxBlocked, normalize_work_path
from github_tools_v1 import GitHubToolsV1, InvalidGitHubRequest, GitHubBlocked

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.tools = RuntimeToolsV1(lambda action, payload: (
            self.calls.append((action, dict(payload))) or {"status": "QUEUED", "run_id": "r1"}))
    def request(self):
        return {"work_id": "28", "operation": "RUN_TESTS", "source_sha256": "a"*64,
                "profile_id": "python-tests-v1", "request_id": "req-1",
                "identity_id": "spoof", "authorized": True, "command": "whoami"}
    def test_submit_forwards_allowlisted_fields_only(self):
        self.assertEqual(self.tools.execution_submit(self.request())["status"], "QUEUED")
        self.assertEqual(set(self.calls[0][1]), {"work_id","operation","source_sha256","profile_id","request_id"})
    def test_arbitrary_operation_rejected(self):
        req = self.request(); req["operation"] = "SHELL"
        with self.assertRaises(InvalidToolRequest): self.tools.execution_submit(req)
    def test_bad_hash_rejected(self):
        req = self.request(); req["source_sha256"] = "bad"
        with self.assertRaises(InvalidToolRequest): self.tools.execution_submit(req)
    def test_missing_core_blocks(self):
        with self.assertRaises(ToolBlocked): RuntimeToolsV1(None).execution_status("r1")
    def test_bool_output_limit_rejected(self):
        with self.assertRaises(InvalidToolRequest): self.tools.execution_output_read("r1", max_bytes=True)

class SandboxTests(unittest.TestCase):
    class Provider:
        def search(self, work_id, query, limit): return {"results": [], "limit": limit}
        def stat(self, work_id, path): return {"path": path, "exists": True}
        def read_range(self, work_id, path, offset, length): return {"path": path, "offset": offset, "content": "ok"}
        def write(self, work_id, path, content, expected_sha256): return {"path": path, "readback_verified": True}
    def setUp(self): self.tools = SandboxToolsV1(self.Provider())
    def test_work_relative_path(self): self.assertEqual(normalize_work_path("docs/readme.md"), "docs/readme.md")
    def test_traversal_and_windows_paths_rejected(self):
        for path in ("../secret", "a/../secret", "C:/secret", "/etc/passwd", "a\\\\b", "file:stream"):
            with self.subTest(path=path), self.assertRaises(InvalidSandboxRequest): normalize_work_path(path)
    def test_range_limit_enforced(self):
        with self.assertRaises(InvalidSandboxRequest): self.tools.sandbox_read_range("28", "a.txt", length=65537)
    def test_write_requires_readback(self):
        class BadProvider(self.Provider):
            def write(self, *args): return {"readback_verified": False}
        with self.assertRaises(SandboxBlocked): SandboxToolsV1(BadProvider()).sandbox_write("28", "a.txt", "hello")
    def test_missing_provider_blocks(self):
        with self.assertRaises(SandboxBlocked): SandboxToolsV1(None).sandbox_stat("28", "a.txt")

class GitHubTests(unittest.TestCase):
    class Provider:
        def repository(self, repository): return {"full_name": repository}
        def read_file(self, repository, path, ref): return {"path": path, "ref": ref}
        def search_files(self, repository, query, ref, limit): return {"items": [], "limit": limit}
        def create_branch(self, repository, branch, base_ref): return {"branch": branch}
        def create_file(self, repository, branch, path, content, message): return {"commit_sha": "a"*40}
        def update_file(self, repository, branch, path, content, message, expected_blob_sha): return {"commit_sha": "b"*40}
    def setUp(self): self.tools = GitHubToolsV1(self.Provider())
    def test_default_branch_write_rejected(self):
        with self.assertRaises(InvalidGitHubRequest): self.tools.github_create_file("owner/repo", "main", "a.txt", "hi", "test")
    def test_create_requires_commit(self):
        class BadProvider(self.Provider):
            def create_file(self, *args): return {}
        with self.assertRaises(GitHubBlocked):
            GitHubToolsV1(BadProvider()).github_create_file("owner/repo", "work/test", "a.txt", "hi", "test")
    def test_update_requires_blob_sha(self):
        with self.assertRaises(InvalidGitHubRequest):
            self.tools.github_update_file("owner/repo", "work/test", "a.txt", "hi", "test", "bad")
    def test_read_file(self): self.assertEqual(self.tools.github_read_file("owner/repo", "README.md", "main")["path"], "README.md")
    def test_missing_provider_blocks(self):
        with self.assertRaises(GitHubBlocked): GitHubToolsV1(None).github_repository("owner/repo")

if __name__ == "__main__": unittest.main()
