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

"""Unit tests for work_items.model.config_organization."""

from work_items.model.config_organization import ConfigOrganization


def test_defaults_are_empty() -> None:
    """A fresh ConfigOrganization has empty name and project filter."""
    config = ConfigOrganization()
    assert config.organization_name == ""
    assert config.projects_name_filter == []


def test_load_from_json_populates_fields() -> None:
    """A well-formed entry loads the name and the project filter."""
    config = ConfigOrganization()
    ok = config.load_from_json({"organization-name": "acme", "projects-name-filter": ["Alpha", "Beta"]})
    assert ok is True
    assert config.organization_name == "acme"
    assert config.projects_name_filter == ["Alpha", "Beta"]


def test_load_from_json_defaults_missing_project_filter_to_empty_list() -> None:
    """A missing projects-name-filter yields an empty list, not an error."""
    config = ConfigOrganization()
    assert config.load_from_json({"organization-name": "acme"}) is True
    assert config.projects_name_filter == []


def test_load_from_json_coerces_non_list_project_filter_to_empty_list() -> None:
    """A non-list projects-name-filter is discarded rather than trusted."""
    config = ConfigOrganization()
    assert config.load_from_json({"organization-name": "acme", "projects-name-filter": "Alpha"}) is True
    assert config.projects_name_filter == []


def test_load_from_json_rejects_missing_organization_name() -> None:
    """The organization name is required; an entry without it fails to load."""
    config = ConfigOrganization()
    assert config.load_from_json({"projects-name-filter": ["Alpha"]}) is False


def test_repr_contains_both_fields() -> None:
    """__repr__ exposes both attributes for log/debug output."""
    config = ConfigOrganization()
    config.load_from_json({"organization-name": "acme", "projects-name-filter": ["Alpha"]})
    text = repr(config)
    assert "acme" in text
    assert "Alpha" in text
