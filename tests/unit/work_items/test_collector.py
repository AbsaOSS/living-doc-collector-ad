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

"""Unit tests for work_items.collector."""

from pytest_mock import MockerFixture

from work_items.collector import ADWorkItemsCollector


def test_collector_stores_output_path() -> None:
    """The constructor keeps the output path for later use."""
    collector = ADWorkItemsCollector("/tmp/out")
    assert collector._output_path == "/tmp/out"  # pylint: disable=protected-access


def test_collect_reports_not_implemented(mocker: MockerFixture) -> None:
    """collect() returns False and logs a warning until the mode is implemented."""
    warn = mocker.patch("work_items.collector.logger.warning")

    result = ADWorkItemsCollector("/tmp/out").collect()

    assert result is False
    warn.assert_called_once()
