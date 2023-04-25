# BlueTeam IOA Rules

CrowdStrike Falcon Custom IOA rules, for the Blue Team when faced with Red Team Operations. 

## Overview

This repository contains custom IOA rules often used during Red Team exercises.

This repository has multiple executables to help with the lifecycle management of the IOA rules.

- falcon-export-ioarules.py
- falcon-import-ioarules.py
- falcon-list-ioarules.py
- falcon-validate-credentials.py

This also includes a HTML client (react.js) for viewing the IOA rules in a browser.

See the `./viewer/README.md` in the viewer directory for more information.

## Setup Validation

The following environment variables can be used with the switches to validate the API credentials.

```shell
export FALCON_CLIENT_ID=7xxxxxxxxxxxxxxx
export FALCON_CLIENT_SECRET=5Abbbbbbbbbbbbbbbbbbbbbbbb31
export FALCON_BASE_URL=https://api.laggar.gcw.crowdstrike.com
```

Use this tool `falcon-validate-credentials.py` to validate the credentials. The return code will be 0 if the credentials are valid.

```shell
usage: falcon-validate-credentials.py [-h] -k FALCON_CLIENT_ID -s FALCON_CLIENT_SECRET [-b BASE_URL] [-V]

Validate Credentials.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|

optional arguments:
  -h, --help            show this help message and exit
  -b BASE_URL, --base_url BASE_URL
                        CrowdStrike base URL for Gov Clouds
  -V, --verbose         verbose mode

required arguments:
  -k FALCON_CLIENT_ID, --falcon_client_id FALCON_CLIENT_ID
                        CrowdStrike Falcon API Client ID
  -s FALCON_CLIENT_SECRET, --falcon_client_secret FALCON_CLIENT_SECRET
                        CrowdStrike Falcon API Client Secret

Example(s):
./falcon-validate-credentials.py  -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET
./falcon-validate-credentials.py  -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL
```

Run the following command to validate the credentials.

```shell
./falcon-validate-credentials.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -V
Authentication successful
```

***Note: The authentication success does not mean the credentials are authorized for the API calls, just that the credentials are valid.***

## List IOA Rules from the Cloud

Using this tool `falcon-list-ioarules.py` to list rules from a CID and strip OWNER Meta Data, and Rules grouping with a provided filter.

```shell
usage: falcon-list-ioarules.py [-h] [-n] [-t TABLE_FORMAT] [-f FILTER] -k FALCON_CLIENT_ID -s FALCON_CLIENT_SECRET [-b BASE_URL] [-p]

Custom IOA Group and Rule Viewer.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|

optional arguments:
  -h, --help            show this help message and exit
  -n, --nocolor         Disable color output
  -t TABLE_FORMAT, --table_format TABLE_FORMAT
                        Tabular display format
  -b BASE_URL, --base_url BASE_URL
                        CrowdStrike base URL for Gov Clouds
  -p, --show_patterns   Show IOA patterns in output

search arguments:
  -f FILTER, --filter FILTER
                        String to filter results (IOA rule group name)

required arguments:
  -k FALCON_CLIENT_ID, --falcon_client_id FALCON_CLIENT_ID
                        CrowdStrike Falcon API Client ID
  -s FALCON_CLIENT_SECRET, --falcon_client_secret FALCON_CLIENT_SECRET
                        CrowdStrike Falcon API Client Secret

Example(s):
./falcon-list-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET 
./falcon-list-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -f "My IOA Rule Group" -p
```

Run the following command will list the IOA rules filtered on `Custom IOA Group Name`.

```shell
./falcon-list-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -f "Logon Anomolies"

_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|

╒══════════════════════════════════╤═════════════════════════════════════════════════╤════════════╤════════════════════════════════════╕
│ Custom IOA Group Name            │ Description                                     │ Platform   │ IOA Rules                          │
╞══════════════════════════════════╪═════════════════════════════════════════════════╪════════════╪════════════════════════════════════╡
│ Logon Anomolies                  │ Collection of rules to identify logon anomolies │ Windows    │ login-chain-informational (ver: 3) │
│ ac1318045d574d8dbc5de9069a7eebf2 │                                                 │ Disabled   │                                    │
│                                  │                                                 │ Version: 3 │                                    │
╘══════════════════════════════════╧═════════════════════════════════════════════════╧════════════╧════════════════════════════════════╛
```

## Export IOA Rules from the Cloud

Using this tool `falcon-export-ioarules.py` to dump rules as JSON from a CID and strip OWNER Meta Data, and Rules grouping with a provided filter.

```shell
usage: falcon-export-ioarules.py [-h] -k FALCON_CLIENT_ID -s FALCON_CLIENT_SECRET [-b BASE_URL] [-F FILTER] [-g CUSTOM_IOA_GROUP_ID | -G CUSTOM_IOA_GROUP_NAME]

Custom IOA Rule JSON Exporter.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|

optional arguments:
  -h, --help            show this help message and exit
  -b BASE_URL, --base_url BASE_URL
                        CrowdStrike base URL for Gov Clouds

required arguments:
  -k FALCON_CLIENT_ID, --falcon_client_id FALCON_CLIENT_ID
                        CrowdStrike Falcon API Client ID
  -s FALCON_CLIENT_SECRET, --falcon_client_secret FALCON_CLIENT_SECRET
                        CrowdStrike Falcon API Client Secret

search arguments:
  -F FILTER, --filter FILTER
                        FQL filtering options (Ex: "platform:'windows'+rules.name:'Block python'")
  -g CUSTOM_IOA_GROUP_ID, --custom_ioa_group_id CUSTOM_IOA_GROUP_ID
                        Custom IOA Group ID (ex: 51753701bfaf49b7b688977702396d35)
  -G CUSTOM_IOA_GROUP_NAME, --custom_ioa_group_name CUSTOM_IOA_GROUP_NAME
                        Custom IOA Group Name (ex: 'Example IOA Group')

Example(s):
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -g 'ac1318045d574d8dbc5de9069a7eebf2' | jq .[].name
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -F "platform:'windows'" > ../rules/windows/rules_0001.json
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -G 'Burger Files for Linux' -F "enabled:'True'" > ../rules/linux/rules_0001.json
```

### Filters

Filter term criteria available for IOA Rules:

- enabled
- platform
- id (IOA Group ID)
- name  (IOA Group Name)
- description
- rules.action_label
- rules.name (IOA Rule Name)
- rules.description
- rules.pattern_severity
- rules.ruletype_name
- rules.enabled

### Exporting Rules

When exporting rules, the following fields are stripped from the rules:

```python
metaFields = ["modified_on", "modified_by", "rulegroup_id", "magic_cookie", "pattern_id",
              "instance_id", "enabled", "deleted", "version_ids", "instance_version",
              "created_on", "created_by", "committed_on", "customer_id"]
```

ex: In the below example we strip the windows Platform IOA rules from multiple IOA Groups and dump to JSON

```shell
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -F "platform:'windows'" > ../rules/windows/rules_0001.json
```

### Using JQ to filter the JSON

Using `jq` to filter the JSON to only show the IOA Rules names.

```shell
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET  | jq .[].name
Filtering on: None
"login-chain-informational"
"Dellepiane burger"
"Login Detected"
"Test001 ClikToRun"
"Block malicious process logr0tate"
"Kill French Fry Files"
```

Filter a single Group and use `jq` to trim the JSON to remove the `field_values`, and `disposition_id` and print the json as table using `jtbl`.

```shell

```shell
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -G 'Burger Files for Linux' | jq 'map(del(.field_values,.disposition_id))' | jtbl
Filtering on: name:'Burger Files for Linux'
  ruletype_id  ruletype_name    comment    name                   description                               pattern_severity    action_label
-------------  ---------------  ---------  ---------------------  ----------------------------------------  ------------------  --------------
           13  File Creation               Kill French Fry Files  kill process that create frenchfry files  critical            Kill Process
```

Reference:

* https://stedolan.github.io/jq/manual/
* https://jtbl.readthedocs.io/en/latest/

## Importing IOA Rules to the Cloud

Using this tool `falcon-import-ioarules.py` to push rules to a CID from a JSON file. Note importing rules will create duplicates and not overwrite existing rules.

There is a rate limit for requests per minute for this API. The tool will pause for 5 second increment backoff (5,10,15,etc..) if the rate limit is hit.

```shell
usage: falcon-import-ioarules.py [-h] -k FALCON_CLIENT_ID -s FALCON_CLIENT_SECRET [-b BASE_URL] -g CUSTOM_IOA_GROUP_ID -f FILE [-E] [-V]

Custom IOA Rule Importer.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|

optional arguments:
  -h, --help            show this help message and exit
  -b BASE_URL, --base_url BASE_URL
                        CrowdStrike base URL for Gov Clouds
  -E, --fail_on_error   exit importing rules if an error occurs
  -V, --verbose         verbose mode

required arguments:
  -k FALCON_CLIENT_ID, --falcon_client_id FALCON_CLIENT_ID
                        CrowdStrike Falcon API Client ID
  -s FALCON_CLIENT_SECRET, --falcon_client_secret FALCON_CLIENT_SECRET
                        CrowdStrike Falcon API Client Secret
  -g CUSTOM_IOA_GROUP_ID, --custom_ioa_group_id CUSTOM_IOA_GROUP_ID
                        Custom IOA Group ID (ex: 51753701bfaf49b7b688977702396d35)
  -f FILE, --file FILE  File Containing a single JSON Dict IOA Rule or JSON List IOA Rules

Example(s):
./falcon-import-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -g abcdefg01234567890abcdefg -f ../rules/windows/rules_0001.json
./falcon-import-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -g abcdefg01234567890abcdefg -f ../rules/windows/rules_0001.json -V | jq .
```


