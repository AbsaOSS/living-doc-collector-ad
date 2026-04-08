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
This module contains an Action Inputs class methods,
which are essential for running the ADO action.
"""

import base64
import json
import logging
import requests
from living_doc_utilities.github.utils import get_action_input

from living_doc_utilities.inputs.action_inputs import BaseActionInputs

from utils.constants import Mode, WORK_ITEMS_ORGANIZATIONS, VERBOSE_LOGGING
from utils.exceptions import FetchOrganizationsException
from work_items.model.config_organization import ConfigOrganization

logger = logging.getLogger(__name__)


class ActionInputs(BaseActionInputs):
    """
    A class representing all the action inputs. It is responsible for loading, managing
    and validating the inputs required for running the ADO Action.
    """

    def __init__(self) -> None:
        super().__init__()
        self._organizations_cache: list[ConfigOrganization] | None = None

    @staticmethod
    def get_ado_token() -> str:
        """
        Getter of the Azure DevOps Personal Access Token.
        @return: The ADO PAT string.
        """
        return get_action_input("ADO_TOKEN", "")

    @staticmethod
    def is_work_items_mode_enabled() -> bool:
        """
        Getter of the Work Items mode switch.
        @return: True if Work Items mode is enabled, False otherwise.
        """
        mode: str = Mode.WORK_ITEMS.value
        return get_action_input(mode, "false").lower() == "true"

    @staticmethod
    def get_verbose_logging() -> bool:
        """
        Getter of the verbose logging switch. False by default.
        @return: True if verbose logging is enabled, False otherwise.
        """
        return get_action_input(VERBOSE_LOGGING, "false").lower() == "true"

    @staticmethod
    def get_organizations() -> list[ConfigOrganization]:
        """
        Getter and parser of the Config Organizations.

        @return: A list of Config Organizations.
        @raise FetchOrganizationsException: When parsing JSON string to dictionary fails.
        """
        organizations: list[ConfigOrganization] = []
        action_input = get_action_input(WORK_ITEMS_ORGANIZATIONS, "[]")
        try:
            # Parse the organizations json string into json dictionary format
            organizations_json = json.loads(action_input)

            # Load organizations into ConfigOrganization objects from JSON
            for org_json in organizations_json:
                config_org = ConfigOrganization()
                if config_org.load_from_json(org_json):
                    organizations.append(config_org)
                else:
                    logger.error("Failed to load organization from JSON: %s.", org_json)

        except json.JSONDecodeError as e:
            logger.error("Error parsing JSON organizations: %s.", e, exc_info=True)
            raise FetchOrganizationsException from e

        except TypeError as e:
            logger.error("Type error parsing input JSON organizations: %s. Error: %s.", action_input, e, exc_info=True)
            raise FetchOrganizationsException from e

        return organizations

    def _call_profile_api(self, headers: dict[str, str]) -> requests.Response:
        """Call the Azure DevOps profile endpoint to verify token validity."""
        return requests.get(
            "https://app.vssps.visualstudio.com/_apis/profile/me?api-version=7.0",
            headers=headers,
            timeout=10,
        )

    def _call_org_api(self, org_name: str, headers: dict[str, str]) -> requests.Response:
        """Call the Azure DevOps projects endpoint to verify organization access."""
        return requests.get(
            f"https://dev.azure.com/{org_name}/_apis/projects?api-version=7.0",
            headers=headers,
            timeout=10,
        )

    def _validate(self) -> int:
        err_counter = 0
        organizations: list[ConfigOrganization] = []

        # Validate the organizations configuration
        try:
            organizations = self.get_organizations()
            self._organizations_cache = organizations
        except FetchOrganizationsException:
            err_counter += 1

        ado_token = self.get_ado_token()
        if not ado_token:
            logger.error("ADO token is not set.")
            err_counter += 1
            return err_counter

        # Validate ADO PAT by calling the Azure DevOps profile endpoint
        credentials = base64.b64encode(f":{ado_token}".encode()).decode()
        headers = {"Authorization": f"Basic {credentials}"}
        response = self._call_profile_api(headers)
        if response.status_code != 200:
            logger.error(
                "Cannot connect to Azure DevOps. Possible cause: Invalid ADO token. Status code: %s, Response: %s",
                response.status_code,
                response.text[:200],
            )
            err_counter += 1

        if err_counter > 0:
            logger.error("User configuration validation failed.")
            return err_counter

        # Hint: continue organization-level validation only when the PAT is valid
        for org in organizations:
            org_name = org.organization_name
            response = self._call_org_api(org_name, headers)

            if response.status_code == 401:
                logger.error(
                    "Unauthorized access to ADO organization '%s'. Please verify your ADO token.",
                    org_name,
                )
                err_counter += 1
            elif response.status_code == 404:
                logger.error(
                    "ADO organization '%s' could not be found. Please verify it exists and the token has access.",
                    org_name,
                )
                err_counter += 1
            elif response.status_code != 200:
                logger.error(
                    "An error occurred while validating ADO organization '%s'. Status: %s, Response: %s",
                    org_name,
                    response.status_code,
                    response.text[:200],
                )
                err_counter += 1

        if err_counter > 0:
            logger.error("User configuration validation failed.")
        else:
            logger.info("User configuration validation successfully completed.")

        self.print_effective_configuration()

        return err_counter

    def _print_effective_configuration(self) -> None:
        """
        Print the effective configuration of the action inputs.
        """
        organizations = self._organizations_cache if self._organizations_cache is not None else []
        logger.info("Mode: `work-items`: %s.", "Enabled" if ActionInputs.is_work_items_mode_enabled() else "Disabled")
        logger.info("Mode(work-items): `work-items-organizations`: %s.", organizations)
        logger.info("verbose logging: %s", self.get_verbose_logging())
