"""Verify the dependency chart inherits IDC client settings without overrides."""

import os
import subprocess
import unittest
from pathlib import Path

import yaml

CHART = Path(os.environ.get(
    "GALAXY_DEPS_CHART",
    Path(__file__).resolve().parents[1] / "galaxy-deps",
))


class CvmfsDefaultsTest(unittest.TestCase):
    def test_repositories_are_inherited_from_csi_chart(self):
        output = subprocess.check_output(
            ["helm", "template", "galaxy-deps", str(CHART), "-n", "galaxy-deps"],
            text=True,
        )
        documents = [d for d in yaml.safe_load_all(output) if d]
        config = next(d for d in documents if d["kind"] == "ConfigMap"
                      and d["metadata"]["name"] == "cvmfs-csi-config-d")
        for repository in ("data.galaxyproject.org", "idc.galaxyproject.org"):
            with self.subTest(repository=repository):
                conf = config["data"][f"{repository}.conf"]
                self.assertIn(f"/etc/cvmfs/config.d/{repository}.pub", conf)
                self.assertIn(f"{repository}.pub", config["data"])
        storage = next(d for d in documents if d["kind"] == "StorageClass"
                       and d["metadata"]["name"] == "galaxy-cvmfs")
        self.assertEqual(storage["provisioner"], "cvmfs.csi.cern.ch")
        defaults = yaml.safe_load((CHART / "values.yaml").read_text())
        self.assertNotIn("extraConfigMaps", defaults["cvmfs"]["cvmfscsi"])


if __name__ == "__main__":
    unittest.main()
