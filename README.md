# Living Documentation Collector for Azure DevOps

- [Motivation](#motivation)
- [Data-Mining Modes](#data-mining-modes)
- [Usage](#usage)
    - [Prerequisites](#prerequisites)
    - [Adding the Action to Your Workflow](#adding-the-action-to-your-workflow)
- [Action Configuration](#action-configuration)
    - [Environment Variables](#environment-variables)
    - [Inputs](#inputs)
      - [Base Inputs](#base-inputs)
      - [Mode Inputs](#mode-inputs)
- [Action Outputs](#action-outputs)
- [How-to](#how-to)
  - [How to Create a Personal Access Token](#how-to-create-a-personal-access-token)
  - [How to Store Token as a Secret](#how-to-store-token-as-a-secret)
- [Contribution Guidelines](#contribution-guidelines)
  - [License Information](#license-information)
  - [Contact or Support Information](#contact-or-support-information)

## Motivation

Addresses the need for continuously updated documentation accessible to all team members and stakeholders. Achieves this by extracting information directly from Azure DevOps and providing it in a JSON format, which can be easily transformed into various documentation formats. This approach ensures that the documentation is always up-to-date and relevant, reducing the burden of manual updates and improving overall project transparency.

---
## Data-Mining Modes

This Collector supports multiple mining modes, each with its own unique functionality. Read more about the modes at their respective links:
- [Work Items](work_items/README.md) ![Status](https://img.shields.io/badge/status-in%20development-orange)
- [Boards](boards/README.md) ![Status](https://img.shields.io/badge/status-todo-lightgrey)
- [Pipelines](pipelines/README.md) ![Status](https://img.shields.io/badge/status-todo-lightgrey)
- [Test Plans](test_plans/README.md) ![Status](https://img.shields.io/badge/status-todo-lightgrey)
- [Release Notes](release_notes/README.md) ![Status](https://img.shields.io/badge/status-todo-lightgrey)

---
## Usage

### Prerequisites

Before we begin, ensure you have fulfilled the following prerequisites:
- Azure DevOps Personal Access Token (PAT) with read permission on the target organizations and projects.
- Python version 3.14 or higher.

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

See the default action step definitions for each mode:

- [Work Items mode default step definition](work_items/README.md#adding-work-items-mode-to-the-workflow)

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
| `ADO-TOKEN`        | Azure DevOps Personal Access Token for authentication.  | Yes      |         | Pass via `with:`.        |
| `work-items`       | Enables or disables `Work Items` mode.                  | Yes      | `false` | Set to true to activate. |
| `verbose-logging`  | Enables or disables verbose (debug) logging.             | No       | `false` | Set to true to activate. |


##### Example
```yaml
with:
  ADO-TOKEN: ${{ secrets.ADO_ACCESS_TOKEN }}
  work-items: true          # Activation of Work Items mode
  
  verbose-logging: true     # Activation of verbose (debug) logging
```

#### Mode Inputs

Mode-specific inputs and outputs are detailed in the respective mode's documentation:

- [Work Items mode specific inputs](work_items/README.md#mode-configuration)
    
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

See this [Developer Guide](DEVELOPER.md) for more technical, development-related information.

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

We welcome contributions to the Living Documentation Collector! Whether you're fixing bugs, improving documentation, or proposing new features, your help is appreciated.

#### How to Contribute

Before contributing, please review our [contribution guidelines](https://github.com/AbsaOSS/living-doc-collector-ad/blob/master/CONTRIBUTING.md) for more detailed information.

### License Information

This project is licensed under the Apache License 2.0. It is a liberal license that allows you great freedom in using, modifying, and distributing this software, while also providing an express grant of patent rights from contributors to users.

For more details, see the [LICENSE](https://github.com/AbsaOSS/living-doc-collector-ad/blob/master/LICENSE) file in the repository.

### Contact or Support Information

If you need help with using or contributing to the Living Documentation Collector Action, or if you have any questions or feedback, don't hesitate to reach out:

- **Issue Tracker**: For technical issues or feature requests, use the [GitHub Issues page](https://github.com/AbsaOSS/living-doc-collector-ad/issues).
- **Discussion Forum**: For general questions and discussions, join our [GitHub Discussions forum](https://github.com/AbsaOSS/living-doc-collector-ad/discussions).

