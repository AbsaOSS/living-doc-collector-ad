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

"""Unit tests for utils.utils."""

import os

from utils.utils import make_absolute_path


def test_make_absolute_path_returns_absolute_input_unchanged() -> None:
    """An already-absolute path is returned as-is."""
    absolute = os.path.abspath(os.sep + "tmp")
    assert make_absolute_path(absolute) == absolute


def test_make_absolute_path_expands_relative_input() -> None:
    """A relative path is resolved against the current working directory."""
    result = make_absolute_path("./output")
    assert os.path.isabs(result)
    assert result == os.path.abspath("./output")
