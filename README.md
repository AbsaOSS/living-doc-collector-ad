# Living Documentation Collector for Azure DevOps

[![Build and Test](https://github.com/AbsaOSS/living-doc-collector-ad/actions/workflows/static_analysis_and_tests.yml/badge.svg)](https://github.com/AbsaOSS/living-doc-collector-ad/actions/workflows/static_analysis_and_tests.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A GitHub Action that extracts living-documentation content from Azure DevOps organizations and projects and emits machine-readable JSON for the downstream `living-doc-*` documentation generators.

## Overview

> **Expected usage: GitHub Actions first.** The supported way to run this action is as a step in a GitHub Actions workflow, chained with the other `living-doc-*` actions. Running it locally — the `run_script.sh` / `python3 main.py` pattern documented in `DEVELOPER.md` — is a development and debugging affordance only, not a second supported deployment target.

> **The Living Documentation pipeline runs AI-free.** Every step — collect → normalize → generate — is deterministic tooling (Python, JSON Schema validation, Jinja2/Markdown templates) with no LLM call anywhere in that path. [`AbsaOSS/agentic-toolkit`](https://github.com/AbsaOSS/agentic-toolkit) can accelerate the upstream *authoring* of GitHub Issues and `.feature` files, but it is never a runtime dependency of this pipeline: a human writing the same input by hand is a fully supported, identical path.

Addresses the need for continuously updated documentation accessible to all team members and stakeholders. Achieves this by extracting information directly from Azure DevOps and providing it in a JSON format, which can be easily transformed into various documentation formats. This approach ensures that the documentation is always up-to-date and relevant, reducing the burden of manual updates and improving overall project transparency.

The Collector supports multiple mining modes, each with its own functionality. Activate only the modes you need.

| Mode | Purpose | Status |
|------|---------|--------|
| **Work Items** | Data-mines Azure DevOps organizations and projects for work items that carry project documentation. | ![Status](https://img.shields.io/badge/status-in%20development-orange) |
| Boards | Prospective mode for Azure DevOps Boards. | ![Status](https://img.shields.io/badge/status-planned-blue) — scope decision deferred to post-v1-pre-release analysis |
| Pipelines | Prospective mode for Azure DevOps Pipelines. | ![Status](https://img.shields.io/badge/status-planned-blue) — scope decision deferred to post-v1-pre-release analysis |
| Test Plans | Prospective mode for Azure DevOps Test Plans. | ![Status](https://img.shields.io/badge/status-planned-blue) — scope decision deferred to post-v1-pre-release analysis |
| Release Notes | Prospective mode for Azure DevOps release notes. | ![Status](https://img.shields.io/badge/status-planned-blue) — scope decision deferred to post-v1-pre-release analysis |

**Key features**
- 🔎 Source-specific: Azure DevOps organizations and projects
- 🧩 Modular: activate only the mining modes you need
- 📄 Structured output: JSON ready for the downstream generators
- ⚡ Deterministic: the same inputs always produce the same JSON
- 🔁 Pipeline-ready: chains with the other `living-doc-*` actions

---
## Usage

### Prerequisites

Before we begin, ensure you have fulfilled the following prerequisites:
- Azure DevOps Personal Access Token (PAT) with read permission on the target organizations and projects.
- Python 3.10 or higher.

### Adding the Action to Your Workflow

See the default action step definition:

```yaml
- name: Living Documentation Collector for Azure DevOps
  id: living_doc_collector_ad
  uses: AbsaOSS/living-doc-collector-ad@v0.1.0
  with:
    ADO-TOKEN: ${{ secrets.ADO_ACCESS_TOKEN }}
    # modes de/activation
    work-items: false
```

#### Full Example of Action Step Definition

See the full example of action step definition (in the example, non-default values are used):

```yaml
- name: Living Documentation Collector for Azure DevOps
  id: living_doc_collector_ad
  uses: AbsaOSS/living-doc-collector-ad@v0.1.0
  with:
    ADO-TOKEN: ${{ secrets.ADO_ACCESS_TOKEN }}
    work-items: true                       # Work Items mode de/activation
    verbose-logging: true                  # Optional: verbose (debug) logging de/activation

    # 'Work Items' mode required configuration
    work-items-organizations: |
        [
          {
            "organization-name": "your-ado-organization",
            "projects-name-filter": []
          },
          {
            "organization-name": "your-another-ado-organization",
            "projects-name-filter": ["Project Alpha", "Project Beta"]
          }
        ]
```

---
## Action Configuration

This section outlines the essential parameters that are common to all modes a user can define. Configure the action by customizing the following parameters based on your needs:

### Environment Variables

This action does not use environment variables directly. Pass the ADO token via the `ADO-TOKEN` input as shown in the examples above.

> **Note**: Unlike some GitHub Actions, this action accepts the `ADO-TOKEN` as a `with:` input rather than an `env:` variable to keep the configuration explicit and self-contained.

### Inputs

#### Base Inputs

These inputs are common to all modes.

| Input Name         | Description                                              | Required | Default | Usage                    |
|--------------------|----------------------------------------------------------|----------|---------|--------------------------|
| `ADO-TOKEN`        | Azure DevOps Personal Access Token for authentication.   | Yes      |         | Pass via `with:`.        |
| `work-items`       | Enables or disables `Work Items` mode.                   | No       | `false` | Set to true to activate. |
| `verbose-logging`  | Enables or disables verbose (debug) logging.             | No       | `false` | Set to true to activate. |

##### Example
```yaml
with:
  ADO-TOKEN: ${{ secrets.ADO_ACCESS_TOKEN }}
  work-items: true          # Activation of Work Items mode

  verbose-logging: true     # Activation of verbose (debug) logging
```

#### Mode Inputs

**Work Items mode**

| Input Name                 | Description                                                                | Required | Default | Usage                            |
|----------------------------|--------------------------------------------------------------------------|----------|---------|----------------------------------|
| `work-items-organizations` | JSON string defining the Azure DevOps organizations and projects to mine. | No       | `[]`    | Required when `work-items: true`. |

Each entry in `work-items-organizations` accepts:
- `organization-name` — the Azure DevOps organization to mine (required).
- `projects-name-filter` — a list of project names to restrict mining to; an empty list mines every accessible project.

The other four modes (Boards, Pipelines, Test Plans, Release Notes) are planned; their inputs will be documented once the scope decision is made.

---
## Action Outputs

The action provides a main output path that allows users to locate and access the generated JSON files easily.
This output can be utilized in various ways within your CI/CD pipeline to ensure the documentation is effectively distributed and accessible.

- `output-path`
  - **Description**: The root output path to the directory where all generated living documentation files are stored.
  - **Usage**:
   ``` yaml
    - name: Living Documentation Collector for Azure DevOps
      id: living_doc_collector_ad
      ... rest of the action definition ...

    - name: Output Documentation Path
      run: echo "ADO Collector root output path: ${{ steps.living_doc_collector_ad.outputs.output-path }}"
    ```

> Each mode generates its output files, which are stored in the `output-path` directory with clear naming conventions.

---
## Developer Guide

For local setup, static analysis, testing, coverage, running the action locally, and releasing, see [DEVELOPER.md](DEVELOPER.md).

---
## How-to

This section aims to help the user walk through different processes, such as:
- [Generating and storing a Personal Access Token](#how-to-create-a-personal-access-token)

### How to Create a Personal Access Token

1. Sign in to your Azure DevOps organization (`https://dev.azure.com/{yourorganization}`).
2. Click on your profile icon in the top-right corner and select **Personal access tokens**.
3. Click **New Token**.
4. Give the token a name and choose expiration date.
5. Select the following scopes (minimum required):
   - **Work Items** → **Read**
   - **Project and Team** → **Read**
   - **Build** → **Read** _(if pipelines mode will be used)_
6. Click **Create** and copy the token value — you will not be able to see it again.

### How to Store Token as a Secret

1. Go to the GitHub repository from which you want to run this GitHub Action.
2. Click on the `Settings` tab in the top bar.
3. In the left sidebar, click on `Secrets and variables` > `Actions`.
4. Click on the `New repository secret` button.
5. Name the secret `ADO_ACCESS_TOKEN` and paste the token value.

---
## Contribution Guidelines

We welcome contributions to the Living Documentation Collector — bug fixes, documentation improvements, and new features. See [CONTRIBUTING.md](CONTRIBUTING.md) for the bug-report, feature-request, branch-naming, and PR conventions.

### License Information

This project is licensed under the Apache License 2.0. It is a liberal license that allows you great freedom in using, modifying, and distributing this software, while also providing an express grant of patent rights from contributors to users.

For more details, see the [LICENSE](LICENSE) file in the repository.

### Contact or Support Information

If you need help with using or contributing to the Living Documentation Collector Action, or if you have any questions or feedback, don't hesitate to reach out:

- **Issue Tracker**: For technical issues, questions, or feature requests, use the [GitHub Issues page](https://github.com/AbsaOSS/living-doc-collector-ad/issues).

Maintained by [ABSA Group Limited](https://github.com/AbsaOSS).
