"""Adversarial component tests for the Linux handle-anchored filesystem backend."""
import os
import tempfile
import unittest
from pathlib import Path

from sandbox_handle_fs_v1 import HandleFilesystemError, LinuxHandleFilesystem


@unittest.skipUnless(os.name == "posix" and hasattr(os, "O_NOFOLLOW"),
                     "Linux/POSIX no-follow primitives required")
class LinuxHandleFilesystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.sandbox = self.base / "sandbox"
        self.sandbox.mkdir()
        self.outside = self.base / "outside"
        self.outside.mkdir()
        self.fs = LinuxHandleFilesystem(self.sandbox)

    def tearDown(self):
        self.fs.close()
        self.tmp.cleanup()

    def test_work_handle_remains_anchored_after_work_path_swap(self):
        (self.sandbox / "119").mkdir()
        with self.fs.work("119") as work:
            parked = self.sandbox / "119-original"
            os.replace(self.sandbox / "119", parked)
            (self.sandbox / "119").symlink_to(self.outside, target_is_directory=True)
            with self.fs.directory(work.fd, ".upload-staging", create=True) as staging:
                with self.fs.create_exclusive(staging.fd, "UP-test.part") as f:
                    self.fs.write_at(f.fd, 0, b"pinned")
            self.assertFalse((self.outside / ".upload-staging").exists())
            self.assertTrue((parked / ".upload-staging" / "UP-test.part").exists())

    def test_nested_symlink_is_rejected_without_touching_outside(self):
        (self.sandbox / "119").mkdir()
        (self.sandbox / "119" / "images").symlink_to(self.outside, target_is_directory=True)
        with self.fs.work("119") as work:
            with self.assertRaises(OSError):
                with self.fs.directory(work.fd, "images", create=False):
                    pass
        self.assertEqual(list(self.outside.iterdir()), [])

    def test_exclusive_create_rejects_existing_leaf(self):
        (self.sandbox / "119").mkdir()
        with self.fs.work("119") as work:
            with self.fs.directory(work.fd, ".upload-staging", create=True) as staging:
                with self.fs.create_exclusive(staging.fd, "same.part") as f:
                    self.fs.write_at(f.fd, 0, b"original")
                with self.assertRaises(FileExistsError):
                    self.fs.create_exclusive(staging.fd, "same.part")

    def test_atomic_no_replace_promotion_preserves_existing_destination(self):
        (self.sandbox / "119").mkdir()
        with self.fs.work("119") as work:
            with self.fs.directory(work.fd, ".upload-staging", create=True) as staging, \
                 self.fs.directory(work.fd, "images", create=True) as images:
                with self.fs.create_exclusive(staging.fd, "new.part") as f:
                    self.fs.write_at(f.fd, 0, b"new")
                with self.fs.create_exclusive(images.fd, "photo.png") as f:
                    self.fs.write_at(f.fd, 0, b"old")
                with self.assertRaises(FileExistsError):
                    self.fs.promote_no_replace(staging.fd, "new.part", images.fd, "photo.png")
                with self.fs.open_file(images.fd, "photo.png") as f:
                    self.assertEqual(self.fs.digest(f.fd), (3, __import__("hashlib").sha256(b"old").hexdigest()))

    def test_digest_and_write_are_descriptor_based(self):
        (self.sandbox / "119").mkdir()
        with self.fs.work("119") as work:
            with self.fs.directory(work.fd, ".upload-staging", create=True) as staging:
                with self.fs.create_exclusive(staging.fd, "bytes.part") as f:
                    self.fs.write_at(f.fd, 0, b"binary\\x00payload")
                    self.assertEqual(self.fs.digest(f.fd)[0], len(b"binary\\x00payload"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
