#!/usr/bin/python3
import logging
import subprocess


from ops.model import ModelError


logger = logging.getLogger()


class SlurmHttpConfigManager:
    def __init__(self, charm):
        """Set self._relation_name and self.charm."""
        try:
            self._resource = charm.model.resources.fetch('slurm-http-config')
        except ModelError as e:
            logger.debug(
                f"No slurm-http-config snap resource was supplied: {e}")

    def install_slurm_http_config_snap(self):
        """Install the slurm-http-config snap resource."""

        cmd = [
            "snap",
            "install",
            self._resource,
            "--dangerous",
            "--classic"
        ]

        try:
            subprocess.call(cmd)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error installing slurm-http-config snap - {e}")
