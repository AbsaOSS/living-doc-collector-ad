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

"""Unit tests for utils.constants."""

from utils.constants import Mode, VERBOSE_LOGGING, WORK_ITEMS_ORGANIZATIONS


def test_mode_enum_holds_work_items() -> None:
    """The Mode enum exposes the single supported mining mode."""
    assert Mode.WORK_ITEMS.value == "WORK_ITEMS"
    assert [m.name for m in Mode] == ["WORK_ITEMS"]


def test_input_key_names_map_to_input_env_vars() -> None:
    """Key-name constants match the INPUT_<KEY> environment-variable contract."""
    assert WORK_ITEMS_ORGANIZATIONS == "WORK_ITEMS_ORGANIZATIONS"
    assert VERBOSE_LOGGING == "VERBOSE_LOGGING"
