#!/usr/bin/env python3

import argparse
import lxml.html
import re
import requests
import sys
import tabulate


def build_query_payload(callsign: str) -> dict:
    query_payload = {}
    query_payload["_method"] = "POST"
    query_payload["data[Search][terms]"] = callsign

    return query_payload


if __name__ == "__main__":
    # set up command arguments
    parser = argparse.ArgumentParser(
        description="Ham Radio Call Sign Search Utility - ARRL"
    )
    parser.add_argument(
        "--pretty", required=False, action="store_true", help="print pretty format"
    )
    parser.add_argument("callsign", type=str, help="ham radio call sign string")
    args = parser.parse_args()

    # set up constants
    arrl_call_sign_search_url = "https://www.arrl.org/advanced-call-sign-search"
    output = {}

    # build query payload
    payload = build_query_payload(args.callsign)

    # send HTTP request and process the response
    try:
        response = requests.post(arrl_call_sign_search_url, data=payload)
    except Exception as e:
        print(f"ERROR: Could not send HTTP request to ARRL URL: {e}", file=sys.stderr)
        sys.exit(2)

    if response.status_code != 200:
        print(
            "ERROR: Non-200 HTTP response code retrieved from ARRL URL", file=sys.stderr
        )
        sys.exit(3)

    response_xml = lxml.html.fromstring(response.text)
    try:
        title = response_xml.xpath("//div[@class='list2']/ul/li/h3/text()")[0]
        call_sign_details_response = response_xml.xpath(
            "//div[@class='list2']/ul/li/p/text()"
        )

        # some results do not have <p> tag
        if not call_sign_details_response:
            call_sign_details_response = response_xml.xpath(
                "//div[@class='list2']/ul/li/text()"
            )
    except Exception:
        print(f"ERROR: Could not get proper response from ARRL URL", file=sys.stderr)
        sys.exit(4)

    # generate output
    output["title"] = re.sub(r"\t+", "", title.strip())
    output["basic_info"] = []
    output["tables"] = []
    license_holders = []
    current_license_holder = []
    primary_holder_processed = False
    for line in call_sign_details_response:
        line = line.strip()  # Remove leading and trailing whitespace
        if line.startswith("Previous call sign:"):
            # If we encounter a "Previous call sign" line, we know that a new license holder is starting
            if current_license_holder:
                license_holders.append(current_license_holder)
                current_license_holder = []
        current_license_holder.append(line)
    # Add the last license holder if there is one
    if current_license_holder:
        license_holders.append(current_license_holder)

    for license_holder in license_holders: 
        if primary_holder_processed: print()
        output["tables"] = []
        for item in license_holder:
            if not re.match(r"^\s+$", item):
                line = re.sub(r"\t+", "", item).strip()
                if re.match(r".*:\s+.*", line):
                    key, value = line.split(":")
                    output["tables"].append([key, value.strip()])
                else:
                    if not primary_holder_processed: 
                        output["basic_info"].append(line)
        if not primary_holder_processed:
            print(output["title"])
            for item in output["basic_info"]:
                print(item.replace("Previous call sign","\033[1mPrevious call sign\033[0m"))
            primary_holder_processed = True

        if args.pretty:
            table_format = "simple_grid"
            print(tabulate.tabulate(output["tables"], tablefmt=table_format))
        else:
            for item in output["tables"]:
                print(f"{item[0]}: {item[1]}")
