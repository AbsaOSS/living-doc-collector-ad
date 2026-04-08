#
# Copyright 2026 ABSA Group Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This module defines the ConfigOrganization model for ADO organization configuration.
"""

import logging

logger = logging.getLogger(__name__)


class ConfigOrganization:
    """
    Represents the configuration for a single Azure DevOps organization to mine.
    """

    def __init__(self) -> None:
        self.organization_name: str = ""
        self.projects_name_filter: list[str] = []

    def load_from_json(self, data: dict[str, object]) -> bool:
        """
        Load the organization configuration from a JSON dictionary.

        @param data: Dictionary containing 'organization-name' and optional 'projects-name-filter'.
        @return: True on success, False if required fields are missing.
        """
        org_name = data.get("organization-name", "")
        if not org_name:
            logger.error("Missing required field 'organization-name' in organization config: %s.", data)
            return False
        self.organization_name = str(org_name)
        projects_filter = data.get("projects-name-filter", [])
        self.projects_name_filter = list(projects_filter) if isinstance(projects_filter, list) else []
        return True

    def __repr__(self) -> str:
        return (
            f"ConfigOrganization(organization_name={self.organization_name!r}, "
            f"projects_name_filter={self.projects_name_filter!r})"
        )
