#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Custom IOA Rule JSON Exporter.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|
"""

import sys
import json
try:
    from falconpy import APIHarness
except ImportError as no_falconpy:
    raise SystemExit(
        "The CrowdStrike SDK must be installed in order to use this utility.\n"
        "Install this application with the command `python3 -m pip install crowdstrike-falconpy`."
    ) from no_falconpy
from argparse import ArgumentParser, RawTextHelpFormatter

ex = """
Example(s):
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -g 'ac1318045d574d8dbc5de9069a7eebf2' | jq .[].name
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -F "platform:'windows'" > ../rules/windows/rules_0001.json
./falcon-export-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -G 'Burger Files for Linux' -F "enabled:'True'" > ../rules/linux/rules_0001.json
"""


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def falcon_query_rule_group_full(fql_filter=None):
    eprint(f'Filtering on: {fql_filter}')
    return falcon.command("query_rule_groups_full",
                          filter=fql_filter
                          )


def consume_command_line():
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawTextHelpFormatter,
        epilog=ex
    )
    req = parser.add_argument_group("required arguments")
    req.add_argument(
        "-k", "--falcon_client_id",
        help="CrowdStrike Falcon API Client ID",
        required=True
    )

    req.add_argument(
        "-s", "--falcon_client_secret",
        help="CrowdStrike Falcon API Client Secret",
        required=True
    )

    parser.add_argument(
        '-b', '--base_url',
        help="CrowdStrike base URL for Gov Clouds",
        required=False,
        default="auto"
    )

    search = parser.add_argument_group("search arguments")
    search.add_argument(
        '-F', '--filter',
        help='FQL filtering options (Ex: "platform:\'windows\'+rules.name:\'Block python\'")',
        required=False
    )

    group = search.add_mutually_exclusive_group()
    group.add_argument(
        "-g", "--custom_ioa_group_id",
        help="Custom IOA Group ID (ex: 51753701bfaf49b7b688977702396d35)",
        required=False
    )

    group.add_argument(
        "-G", "--custom_ioa_group_name",
        help="Custom IOA Group Name (ex: 'Example IOA Group')",
        required=False
    )
    return parser.parse_args()


args = consume_command_line()

CLIENTID = args.falcon_client_id
CLIENTSECRET = args.falcon_client_secret
CLIENTBASE = args.base_url
GROUP_ID = args.custom_ioa_group_id
GROUPNAME = args.custom_ioa_group_name
fql_filter = args.filter

# Login to the Falcon API and retrieve our list of sensors
# Login to the Falcon API and retrieve our list of sensors
falcon = APIHarness(client_id=CLIENTID,
                    client_secret=CLIENTSECRET, base_url=CLIENTBASE)

if fql_filter:
    if GROUP_ID:
        fql_group_filter = f"id:'{GROUP_ID}'"
        fql_filter = f"{fql_filter}+{fql_group_filter}"
    elif GROUPNAME:
        fql_group_filter = f"name:'{GROUPNAME}'"
        fql_filter = f"{fql_filter}+{fql_group_filter}"

elif GROUP_ID:
    fql_filter = f"id:'{GROUP_ID}'"

elif GROUPNAME:
    fql_filter = f"name:'{GROUPNAME}'"

else:
    fql_filter = None
response = falcon_query_rule_group_full(fql_filter)
resource = response["body"]["resources"]

ruleBucket = []
metaFields = ["modified_on", "modified_by", "rulegroup_id", "magic_cookie", "pattern_id",
              "instance_id", "enabled", "deleted", "version_ids", "instance_version",
              "created_on", "created_by", "committed_on", "customer_id"]

for group in resource:
    newGroup = []
    for rule in group["rules"]:
        newRule = {key: val for key,
                   val in rule.items() if key not in metaFields}
        newGroup.append(newRule)
    ruleBucket.extend(newGroup)

json_object = json.dumps(ruleBucket, indent=4)
print(json_object)

if response['status_code'] not in range(200, 208):
    raise SystemExit("An error occurred exporting the rules.")
