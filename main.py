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
This module contains the main script for the Living Documentation Collector for Azure DevOps.
It sets up logging, loads action inputs, runs the data collection, and sets the action output.
"""

import logging
import sys

from living_doc_utilities.constants import OUTPUT_PATH
from living_doc_utilities.github.utils import set_action_output
from living_doc_utilities.logging_config import setup_logging

from action_inputs import ActionInputs
from utils.utils import make_absolute_path
from work_items.collector import ADWorkItemsCollector

logger = logging.getLogger(__name__)


def run() -> None:
    """
    The main function to run the Living Documentation (Liv-Doc) Collector for Azure DevOps.

    @return: None
    """
    setup_logging()

    logger.info("Liv-Doc collector for Azure DevOps - starting.")

    if not ActionInputs().validate_user_configuration():
        logger.info("Liv-Doc collector for Azure DevOps - user configuration validation failed.")
        sys.exit(1)

    output_path: str = make_absolute_path(OUTPUT_PATH)
    all_modes_success: bool = True

    if ActionInputs.is_work_items_mode_enabled():
        logger.info("Liv-Doc collector for Azure DevOps - Starting the `work-items` mode.")

        if ADWorkItemsCollector(output_path).collect():
            logger.info("Liv-Doc collector for Azure DevOps - `work-items` mode completed successfully.")
        else:
            logger.info("Liv-Doc collector for Azure DevOps - `work-items` mode failed.")
            all_modes_success = False
    else:
        logger.info("Liv-Doc collector for Azure DevOps - `work-items` mode disabled.")

    # Set the output for the GitHub Action
    set_action_output("output-path", output_path)
    logger.info("Liv-Doc collector for Azure DevOps - root output path set to `%s`.", output_path)

    logger.info("Liv-Doc collector for Azure DevOps - ending.")

    if not all_modes_success:
        sys.exit(1)


if __name__ == "__main__":
    run()
