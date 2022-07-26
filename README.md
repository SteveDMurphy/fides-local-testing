# fides-local-testing
Testing out a local install of fidesctl

### Local Setup

For this workspace, a Docker installation is required. Technically a local postgres installation will also work but the walkthrough will assume Docker.

To start, we will execute a couple of python commands.

Let's create and activate a virtual environment in our new workspace:
`python3 -m venv env && source env/bin/activate`

Then lets install `nox`:
`pip install nox`

Then we can install fidesctl (using latest from GitHub):
`pip install git+https://github.com/ethyca/fides.git`

After that we can start the database:
`nox -s fides_db`

Initialize `fidesctl`:
`fidesctl init`

Then we need to update the default `fidesctl.toml` to use localhost and add our default port:
```toml
[cli]
...
server_port = "8080"
...
[database]
server_host = localhost
```

Then start the webserver:
`fidesctl webserver`

Finally, we can test the installation:
`fidesctl status`

### Dive In

We can then annotate a new system as a starting point:
```yaml
system:
  - fides_key: sample_platform
    name: Platform
    description: Our sample platform
    system_type: Service
    administrating_department: Platform
    data_responsibility_title: Controller
    third_country_transfers:
    - USA
    privacy_declarations:
      - name: Combined Privacy Declaration
        data_categories:
          - user.name
          - user.contact.email
        data_use: provide.service
        data_subjects:
          - customer
        data_qualifier: aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified
```

And apply it to the server:
`fidesctl apply`

This system can be enhanced by extending the default taxonomy:
```yaml
data_use:
  - fides_key: provide.service.delivery
    name: Facilitate Service Delivery
    description: Services to facilitate usage of a product
    recipients:
    - Microsoft
    - Facebook
    - Linkedin
    - Google
    - Apple
    legal_basis: Contract
    special_category: Consent
    parent_key: provide.service
  - fides_key: provide.service.secure_access
    name: Provide Secure Access
    description: Services to provide secure access to a product
    legal_basis: Contract
    special_category: Consent
    parent_key: provide.service

data_subject:
  - fides_key: b2b_creator
    name: Creator (b2b)
    description: A business-to-business creator
    rights:
      strategy: ALL
    automated_decisions_or_profiling: false

data_category:
  - fides_key: user.name.first_name
    name: First Name
    description: The first name of a user
    parent_key: user.name
  - fides_key: user.name.last_name
    name: Last Name
    description: The last name of a user
    parent_key: user.name
  - fides_key: user.username
    name: Username
    description: The username of a user
    parent_key: user
```

Each taxonomy type provides different context to be applied across a privacy declaration. A cheat sheet for each of the attributes is provided below. Depending on your organization structure, different teams can be responsible for different components of the privacy policy.

_Data Categories_: Currently no further attribution from the default, but new categories can be extended via the UI or CLI.

_Data Uses_:
* Recipients - A list of any external recipients of the personal data
* Legal Basis - The legal basis for processing personal data
* Special Category - The special category for processing personal data
* Legitimate Interests - If a legitimate interest exists and any metadata (i.e. impact assessment)

_Data Subjects_:
* Righs Available - Which legal rights are available to the data subject
* Profiling - Denotes whether or not automated profiling or decisions are made

_Data Qualifiers_: Currently no further attribution from the default, and not normally extended, however also possible from the UI or CLI.

As an example of an organizational construct around this, a non-technical user can help maintain the taxonomy in concert with other professionals. Imagine partnering with a privacy officer to create the profile of a Data Subject for a new system. A technical user can be responsible for applying data categories to datasets and systems they work on (both UI and CLI). Fides provides the process and tools to move this work out of email and spreadsheets into an auditable information system.

Moving on! Once completed, we can then annotate these objects in the system and apply the resources to the server.
```yaml
system:
  - fides_key: sample_platform
    name: Platform
    description: Our sample platform
    system_type: Service
    administrating_department: Platform
    data_responsibility_title: Controller
    third_country_transfers:
    - USA
    privacy_declarations:
      - name: Combined Privacy Declaration
        data_categories:
          - user.username
          - user.name.first_name
          - user.name.last_name
          - user.contact.email
        data_use: provide.service.delivery
        data_subjects:
          - b2b_creator
        data_qualifier: aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified

```
`fidesctl apply`

Then we can export our datamap:
`fidesctl export datamap`

Additionally, if we had a detailed dataset maintained by engineering, we are able to reference that to infer the data categories used on the annotated system:
```yaml
        ...
        dataset_references:
          - sample_dataset
```
`fidesctl apply && fidesctl export datamap`

When referencing a dataset, the system will inherit the data categories from the dataset. If a data category is added to the system that violates a privacy policy, it will automatically flag the violation.
