#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""Custom IOA Group and Rule Viewer.
_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______
|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______
|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|
"""

try:
    from falconpy import CustomIOA
except ImportError as no_falconpy:
    raise SystemExit(
        "The CrowdStrike SDK must be installed in order to use this utility.\n"
        "Install this application with the command `python3 -m pip install crowdstrike-falconpy`."
    ) from no_falconpy
from argparse import ArgumentParser, RawTextHelpFormatter
from tabulate import tabulate


ex = """
Example(s):
./falcon-list-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL
./falcon-list-ioarules.py -k $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -b $FALCON_BASE_URL -f "My IOA Rule Group" -p
"""


class Color:  # pylint: disable=R0903
    """Class to represent the text color codes used for terminal output."""

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    LIGHTBLUE = "\033[94m"
    GREEN = "\033[32m"
    LIGHTGREEN = "\033[92m"
    LIGHTYELLOW = "\033[93m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    LIGHTRED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def monochrome():
    """Disable color output."""
    return [setattr(Color, item, "") for item in dir(Color) if "__" not in item]


def chunk_long_description(desc, col_width) -> str:
    """Chunks a long string by delimiting with CR based upon column length."""
    desc_chunks = []
    chunk = ""
    for word in desc.split():
        new_chunk = f"{chunk} {word.strip()}"
        if len(new_chunk) >= col_width:
            if new_chunk[0] == " ":
                new_chunk = new_chunk[1:]
            desc_chunks.append(new_chunk)
            chunk = ""
        else:
            chunk = new_chunk

    delim = "\n"
    desc_chunks.append(chunk[1:])

    return delim.join(desc_chunks)


def consume_arguments():
    """Consume any user provided arguments."""
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawTextHelpFormatter,
        epilog=ex
    )
    parser.add_argument(
        "-n", "--nocolor",
        help="Disable color output",
        required=False,
        action="store_true",
        default=False
    )

    parser.add_argument(
        "-t", "--table_format",
        help="Tabular display format",
        required=False,
        default="fancy_grid"
    )

    srch = parser.add_argument_group("search arguments")
    srch.add_argument(
        "-f", "--filter",
        help="String to filter results (IOA rule group name)",
        required=False,
        default=None
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
        "-b", "--base_url",
        help="CrowdStrike base URL for Gov Clouds",
        required=False,
        default="auto"
    )

    parser.add_argument(
        "-p", "--show_patterns",
        help="Show IOA patterns in output",
        action="store_true",
        required=False
    )

    return parser.parse_args()


def open_sdk(client_id: str, client_secret: str, base_url: str):
    """Create instances of the Custom IOA Service Class and return it."""
    init_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "base_url": base_url
    }

    return CustomIOA(**init_params)


def get_ioa_list(sdk: CustomIOA, filter_string: str = None):
    """Return the list of IOAs based upon the provided filter."""
    parameters = {}
    if filter_string:
        parameters["filter"] = f"name:*'*{filter_string}*'"
    return sdk.query_rule_groups_full(parameters=parameters)


def show_ioas(matches: dict, table_format: str, show_patterns: bool):
    """Display the IOA listing in tabular format."""

    headers = {
        "name": f"{Color.BOLD}Custom IOA Group Name{Color.END}",
        "description": f"{Color.BOLD}Description{Color.END}",
        "platform": f"{Color.BOLD}Platform{Color.END}",
        "rules": f"{Color.BOLD}IOA Rules{Color.END}"
    }
    ioas = []
    for match in matches["body"]["resources"]:
        ioa = {
            "name": f"{match['name']}\n{Color.CYAN}{match['id']}{Color.END}\n{match['comment']}",
            "description": chunk_long_description(match["description"], 40),
        }
        if match["enabled"]:
            enabled = f"{Color.GREEN}Enabled{Color.END}"
        else:
            enabled = f"{Color.LIGHTRED}Disabled{Color.END}"
        platform = [f"{str(match['platform']).title()}",
                    f"{enabled}",
                    f"Version: {Color.BOLD}{match['version']}{Color.END}"
                    ]
        ioa["platform"] = "\n".join(platform)

        rules = []
        for rule in match["rules"]:
            if show_patterns:
                ioa_patterns = [
                    f"{x['final_value']}" for x in rule['field_values']]
                rules.extend([
                    f"{rule['name']} (ver: {rule['instance_version']})\n{Color.LIGHTBLUE}(patterns: {ioa_patterns}){Color.END}"])
            else:
                rules.extend([
                    f"{rule['name']} (ver: {rule['instance_version']})"])

        ioa["rules"] = "\n".join(rules)
        ioas.append(ioa)

    if not ioas:
        print_no_results()
    else:
        print_banner()
        print(tabulate(ioas, headers=headers, tablefmt=table_format))


def print_banner():
    banner = [
        f"{Color.MAGENTA}",
        "_______ _     _ _______ _______  _____  _______      _____  _____  _______ _______",
        "|       |     | |______    |    |     | |  |  |        |   |     | |_____| |______",
        "|_____  |_____| ______|    |    |_____| |  |  |      __|__ |_____| |     | ______|",
        f"{Color.END}"
    ]
    print("\n".join(banner))


def print_no_results():
    fail = [
        f"{Color.BOLD}{Color.YELLOW}",
        "_  _ ____    ____ ____ ____ _  _ _    ___ ____",
        "|\ | |  |    |__/ |___ [__  |  | |     |  [__",
        "| \| |__|    |  \ |___ ___] |__| |___  |  ___]",
        f"{Color.END}"
    ]
    print("\n".join(fail))


if __name__ == "__main__":
    # Retrieve our command line
    args = consume_arguments()
    if args.nocolor:
        # They don't want shiny, turn off the colors
        monochrome()
    # Create an instance of our Custom IOA Service Class
    falcon = open_sdk(args.falcon_client_id,
                      args.falcon_client_secret,
                      args.base_url)
    # Retrieve all IOA rule groups matching the provided filter
    ioa_rules = get_ioa_list(falcon, args.filter)

    # Display all IOA rule group matches in tabular format
    show_ioas(ioa_rules, args.table_format, args.show_patterns)
