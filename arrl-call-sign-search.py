#!/usr/bin/env python3

import argparse
import lxml.html
import re
import requests
import sys


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
        "--callsign", type=str, required=True, help="ham radio call sign string"
    )
    args = parser.parse_args()

    # set up constants
    arrl_call_sign_search_url = "https://www.arrl.org/advanced-call-sign-search"

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
    except Exception:
        print(f"ERROR: Could not get proper response from ARRL URL", file=sys.stderr)
        sys.exit(4)

    # generate output
    print(title.strip())
    for item in call_sign_details_response:
        if not re.match(r"^\s+$", item):
            line = re.sub(r"\t+", "", item).strip()
            print(line)
