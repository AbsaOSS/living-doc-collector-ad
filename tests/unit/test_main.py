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
