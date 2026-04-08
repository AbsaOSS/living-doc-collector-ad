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
This module defines constants used across the ADO collector.
"""

from enum import Enum


class Mode(Enum):
    """Enumeration of supported data-mining modes."""

    WORK_ITEMS = "WORK_ITEMS"


# Input key names (map to INPUT_<KEY> environment variables)
WORK_ITEMS_ORGANIZATIONS = "WORK_ITEMS_ORGANIZATIONS"
VERBOSE_LOGGING = "VERBOSE_LOGGING"
