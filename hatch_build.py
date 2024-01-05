import typing as t

import django.core.management

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, t.Any]) -> None:
        django.core.management.call_command("compilemessages")
