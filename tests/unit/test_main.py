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

"""Unit tests for main.py entry point."""

import pytest
from pytest_mock import MockerFixture

import main

# --- run() validation path ---


def test_run_exits_when_validation_fails(mocker: MockerFixture) -> None:
    """run() calls sys.exit(1) when user configuration validation returns False."""
    mocker.patch("main.setup_logging")
    mocker.patch("main.ActionInputs.validate_user_configuration", return_value=False)

    with pytest.raises(SystemExit) as exc_info:
        main.run()

    assert exc_info.value.code == 1


# --- run() mode-dispatch path ---


def test_run_completes_when_work_items_mode_disabled(mocker: MockerFixture) -> None:
    """With validation passing and no mode enabled, run() sets the output and does not exit."""
    mocker.patch("main.setup_logging")
    mocker.patch("main.ActionInputs.validate_user_configuration", return_value=True)
    mocker.patch("main.ActionInputs.is_work_items_mode_enabled", return_value=False)
    mocker.patch("main.make_absolute_path", return_value="/abs/output")
    set_output = mocker.patch("main.set_action_output")
    collector = mocker.patch("main.ADWorkItemsCollector")

    main.run()

    set_output.assert_called_once_with("output-path", "/abs/output")
    collector.assert_not_called()


def test_run_completes_when_work_items_mode_succeeds(mocker: MockerFixture) -> None:
    """An enabled mode whose collect() returns True is a clean run."""
    mocker.patch("main.setup_logging")
    mocker.patch("main.ActionInputs.validate_user_configuration", return_value=True)
    mocker.patch("main.ActionInputs.is_work_items_mode_enabled", return_value=True)
    mocker.patch("main.make_absolute_path", return_value="/abs/output")
    mocker.patch("main.set_action_output")
    collector = mocker.patch("main.ADWorkItemsCollector")
    collector.return_value.collect.return_value = True

    main.run()

    collector.return_value.collect.assert_called_once()


def test_run_exits_when_work_items_mode_fails(mocker: MockerFixture) -> None:
    """An enabled mode whose collect() returns False maps to exit code 1."""
    mocker.patch("main.setup_logging")
    mocker.patch("main.ActionInputs.validate_user_configuration", return_value=True)
    mocker.patch("main.ActionInputs.is_work_items_mode_enabled", return_value=True)
    mocker.patch("main.make_absolute_path", return_value="/abs/output")
    set_output = mocker.patch("main.set_action_output")
    collector = mocker.patch("main.ADWorkItemsCollector")
    collector.return_value.collect.return_value = False

    with pytest.raises(SystemExit) as exc_info:
        main.run()

    assert exc_info.value.code == 1
    set_output.assert_called_once_with("output-path", "/abs/output")
