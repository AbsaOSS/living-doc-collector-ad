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

"""Unit tests for utils.exceptions."""

import pytest

from utils.exceptions import FetchOrganizationsException


def test_fetch_organizations_exception_is_an_exception() -> None:
    """FetchOrganizationsException is a plain Exception subclass and is raisable."""
    assert issubclass(FetchOrganizationsException, Exception)
    with pytest.raises(FetchOrganizationsException):
        raise FetchOrganizationsException("boom")
