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

"""Unit tests for action_inputs.ActionInputs."""

import pytest
import responses

from action_inputs import ActionInputs
from utils.exceptions import FetchOrganizationsException

PROFILE_URL = "https://app.vssps.visualstudio.com/_apis/profile/me"
ORG_URL = "https://dev.azure.com/acme/_apis/projects"
ORGS_JSON = '[{"organization-name": "acme", "projects-name-filter": []}]'


# --- simple getters ---


def test_get_ado_token_reads_the_input(monkeypatch: pytest.MonkeyPatch) -> None:
    """get_ado_token returns the INPUT_ADO_TOKEN value, or an empty string when unset."""
    assert ActionInputs.get_ado_token() == ""
    monkeypatch.setenv("INPUT_ADO_TOKEN", "pat-123")
    assert ActionInputs.get_ado_token() == "pat-123"


@pytest.mark.parametrize(
    "value, expected",
    [("true", True), ("TRUE", True), ("false", False), ("anything", False)],
)
def test_is_work_items_mode_enabled(monkeypatch: pytest.MonkeyPatch, value: str, expected: bool) -> None:
    """The work-items switch is case-insensitive and defaults to disabled."""
    monkeypatch.setenv("INPUT_WORK_ITEMS", value)
    assert ActionInputs.is_work_items_mode_enabled() is expected


def test_is_work_items_mode_enabled_defaults_false() -> None:
    """An unset work-items switch means the mode is off."""
    assert ActionInputs.is_work_items_mode_enabled() is False


def test_get_verbose_logging(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verbose logging is opt-in and case-insensitive."""
    assert ActionInputs.get_verbose_logging() is False
    monkeypatch.setenv("INPUT_VERBOSE_LOGGING", "True")
    assert ActionInputs.get_verbose_logging() is True


# --- get_organizations ---


def test_get_organizations_parses_a_valid_list(monkeypatch: pytest.MonkeyPatch) -> None:
    """A valid JSON array is loaded into ConfigOrganization objects."""
    monkeypatch.setenv(
        "INPUT_WORK_ITEMS_ORGANIZATIONS",
        '[{"organization-name": "acme"}, {"organization-name": "beta", "projects-name-filter": ["P1"]}]',
    )
    orgs = ActionInputs.get_organizations()
    assert [o.organization_name for o in orgs] == ["acme", "beta"]
    assert orgs[1].projects_name_filter == ["P1"]


def test_get_organizations_defaults_to_empty_list() -> None:
    """An unset input yields no organizations and does not raise."""
    assert ActionInputs.get_organizations() == []


def test_get_organizations_skips_entries_that_fail_to_load(monkeypatch: pytest.MonkeyPatch) -> None:
    """An entry missing the required organization name is logged and dropped."""
    monkeypatch.setenv(
        "INPUT_WORK_ITEMS_ORGANIZATIONS",
        '[{"organization-name": "acme"}, {"projects-name-filter": ["P1"]}]',
    )
    orgs = ActionInputs.get_organizations()
    assert [o.organization_name for o in orgs] == ["acme"]


def test_get_organizations_raises_on_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unparseable JSON is turned into a FetchOrganizationsException."""
    monkeypatch.setenv("INPUT_WORK_ITEMS_ORGANIZATIONS", "{not json")
    with pytest.raises(FetchOrganizationsException):
        ActionInputs.get_organizations()


def test_get_organizations_raises_on_non_iterable_json(monkeypatch: pytest.MonkeyPatch) -> None:
    """A JSON scalar (here, a number) is a TypeError and is wrapped."""
    monkeypatch.setenv("INPUT_WORK_ITEMS_ORGANIZATIONS", "123")
    with pytest.raises(FetchOrganizationsException):
        ActionInputs.get_organizations()


# --- _validate / validate_user_configuration ---


def test_validate_fails_without_a_token() -> None:
    """A missing ADO token is a configuration error and short-circuits validation."""
    assert ActionInputs()._validate() == 1  # pylint: disable=protected-access


def test_validate_counts_both_bad_orgs_and_missing_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unparseable organizations JSON and a missing token are counted together."""
    monkeypatch.setenv("INPUT_WORK_ITEMS_ORGANIZATIONS", "{not json")
    assert ActionInputs()._validate() == 2  # pylint: disable=protected-access


@responses.activate
def test_validate_fails_when_the_pat_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """A non-200 from the profile endpoint means the PAT is invalid."""
    monkeypatch.setenv("INPUT_ADO_TOKEN", "bad-pat")
    responses.add(responses.GET, PROFILE_URL, status=401)
    assert ActionInputs()._validate() == 1  # pylint: disable=protected-access


@responses.activate
def test_validate_passes_with_a_valid_pat_and_no_organizations(monkeypatch: pytest.MonkeyPatch) -> None:
    """A valid PAT with no organizations configured is a clean pass."""
    monkeypatch.setenv("INPUT_ADO_TOKEN", "good-pat")
    responses.add(responses.GET, PROFILE_URL, status=200, json={"id": "x"})
    inputs = ActionInputs()
    assert inputs._validate() == 0  # pylint: disable=protected-access


@responses.activate
def test_validate_passes_when_the_organization_is_reachable(monkeypatch: pytest.MonkeyPatch) -> None:
    """A configured organization that returns 200 adds no errors."""
    monkeypatch.setenv("INPUT_ADO_TOKEN", "good-pat")
    monkeypatch.setenv("INPUT_WORK_ITEMS_ORGANIZATIONS", ORGS_JSON)
    responses.add(responses.GET, PROFILE_URL, status=200, json={})
    responses.add(responses.GET, ORG_URL, status=200, json={"value": []})
    assert ActionInputs()._validate() == 0  # pylint: disable=protected-access


@responses.activate
@pytest.mark.parametrize("status", [401, 404, 500])
def test_validate_flags_an_unreachable_organization(monkeypatch: pytest.MonkeyPatch, status: int) -> None:
    """401 / 404 / any other non-200 from the org endpoint is a configuration error."""
    monkeypatch.setenv("INPUT_ADO_TOKEN", "good-pat")
    monkeypatch.setenv("INPUT_WORK_ITEMS_ORGANIZATIONS", ORGS_JSON)
    responses.add(responses.GET, PROFILE_URL, status=200, json={})
    responses.add(responses.GET, ORG_URL, status=status, json={})
    assert ActionInputs()._validate() == 1  # pylint: disable=protected-access


@responses.activate
def test_validate_user_configuration_true_when_validate_clean(monkeypatch: pytest.MonkeyPatch) -> None:
    """The public entry point returns True when _validate reports no errors."""
    monkeypatch.setenv("INPUT_ADO_TOKEN", "good-pat")
    responses.add(responses.GET, PROFILE_URL, status=200, json={})
    assert ActionInputs().validate_user_configuration() is True


def test_validate_user_configuration_false_on_error() -> None:
    """The public entry point returns False when _validate reports any error."""
    assert ActionInputs().validate_user_configuration() is False


def test_print_effective_configuration_runs(monkeypatch: pytest.MonkeyPatch) -> None:
    """The effective-configuration dump works with and without a cached org list."""
    monkeypatch.setenv("INPUT_WORK_ITEMS", "true")
    inputs = ActionInputs()
    inputs.print_effective_configuration()
    inputs._organizations_cache = ActionInputs.get_organizations()  # pylint: disable=protected-access
    inputs.print_effective_configuration()
