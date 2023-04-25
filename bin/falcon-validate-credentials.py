#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Validate Credentials.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|
"""

import sys
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
./falcon-validate-credentials.py  -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET
./falcon-validate-credentials.py  -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL
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

    parser.add_argument(
        '-V', '--verbose', help='verbose mode', action='store_true'
    )
    return parser.parse_args()


args = consume_command_line()
CLIENTID = args.falcon_client_id
CLIENTSECRET = args.falcon_client_secret
CLIENTBASE = args.base_url
verboseMode = bool(args.verbose)


# Login to the Falcon API and retrieve our list of sensors
falcon = APIHarness(client_id=CLIENTID,
                    client_secret=CLIENTSECRET, base_url=CLIENTBASE)

if falcon.authenticate():
    if verboseMode:
        eprint("Authentication successful")
    sys.exit(0)
else:
    if verboseMode:
        eprint("Authentication failure")
    sys.exit(1)
