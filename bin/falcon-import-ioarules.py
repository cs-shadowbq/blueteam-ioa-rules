#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Custom IOA Rule Importer.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|
"""


import time
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
./falcon-import-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -g abcdefg01234567890abcdefg -f ../rules/windows/rules_0001.json
./falcon-import-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -g abcdefg01234567890abcdefg -f ../rules/windows/rules_0001.json -V | jq .
"""


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


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

    req.add_argument(
        "-g", "--custom_ioa_group_id",
        help="Custom IOA Group ID (ex: 51753701bfaf49b7b688977702396d35)",
        required=True
    )

    req.add_argument(
        '-f', '--file', help='File Containing a single JSON Dict IOA Rule or JSON List IOA Rules', required=True
    )

    parser.add_argument(
        '-E', '--fail_on_error', help='exit importing rules if an error occurs', action='store_true'
    )

    parser.add_argument(
        '-V', '--verbose', help='verbose mode', action='store_true'
    )

    return parser.parse_args()


def submit_rule(rule_payload):
    # Service Class style
    # return ioa.create_rule(**rule_payload)
    # Uber Class style
    return falcon.command("create_rule", body=rule_payload)


args = consume_command_line()

CLIENTID = args.falcon_client_id
CLIENTSECRET = args.falcon_client_secret
CLIENTBASE = args.base_url
GROUP_ID = args.custom_ioa_group_id
ioa_file = args.file
failOnError = args.fail_on_error
verboseMode = bool(args.verbose)

# Login to the Falcon API and retrieve our list of sensors
falcon = APIHarness(client_id=CLIENTID,
                    client_secret=CLIENTSECRET, base_url=CLIENTBASE)


# Reads into a dictionary:
with open(ioa_file, "r") as f:
    ioa_rules = json.load(f)

# Check if the rule is a list or a single rule
if (type(ioa_rules) is list):
    eprint('Rule list: True')
elif (type(ioa_rules) is dict):
    eprint('Single Rule: True')
else:
    raise SystemExit("Unknown File Format - Exiting")

RETRY_DELAY = 0.5
MAX_TRIES = 5

if type(ioa_rules) is list:
    eprint(f"{len(ioa_rules)} total rules in this batch.")
    for rule in ioa_rules:
        current = 0
        while current < MAX_TRIES:
            # Add the group ID to the rule
            rule['rulegroup_id'] = GROUP_ID
            response = submit_rule(rule)
            if response['status_code'] in range(200, 208):
                eprint('Rule created: ' + rule['name'])
                if verboseMode:
                    resource = json.dumps(response)
                    print(resource)
                current = MAX_TRIES
            else:
                current += 1
                eprint(f'Retry (sleep {RETRY_DELAY} sec): {rule["name"]}')
                time.sleep(RETRY_DELAY)
                if current == MAX_TRIES - 1:
                    eprint(f"Error: \n{json.dumps(response, indent=4)}")
                    eprint('Error creating rule: ' + rule['name'])
                    if failOnError:
                        raise SystemExit(
                            "Exiting - Fail on Error. Rule failed to import")
else:
    # Add the group ID to the rule
    ioa_rules['rulegroup_id'] = GROUP_ID
    # Create the rule via the API
    for _ in range(MAX_TRIES):
        response = submit_rule(ioa_rules)
        if response["status_code"] in range(200, 208):
            eprint("Rule created: " + ioa_rules["name"])
            if verboseMode:
                resource = json.dumps(response)
                print(resource)

    if response["status_code"] not in range(200, 208):
        if verboseMode:
            resource = json.dumps(response)
            print(resource)
        raise SystemExit("An error occurred submitting this rule.")
