# ARRL Ham Radio Call Sign Search Utility

## Intro

`arrl-call-sign-search` is a small utility I wrote to look up ham radio call sign from [ARRL](https://www.arrl.org/advanced-call-sign-search). The utility parses ARRL responses and print call sign details.

## Dependencies

`arrl-call-sign-search` is written in Python3.

Following Python packages are needed:

```
lxml.html
requests
tabulate
```

## Usage

```
$ ./arrl-call-sign-search.py -h
usage: arrl-call-sign-search.py [-h] [--pretty] callsign

Ham Radio Call Sign Search Utility - ARRL

positional arguments:
  callsign    ham radio call sign string

options:
  -h, --help  show this help message and exit
  --pretty    print pretty format
```

## Example

### Default Output

```
$ ./arrl-call-sign-search.py W1AW
ARRL HQ OPERATORS CLUB, W1AW (Club)
225 MAIN ST
NEWINGTON, CT 06111
ATTN: JOSEPH P CARCIA III
Trustee: CARCIA III, JOSEPH P, NJ1Q
Licensee ID: L00306106
FRN: 0004511143
Radio Service: HA
Issue Date: 12/08/2020
Expire Date: 02/26/2031
Date of Last Change: 12/08/2020 (License Renewed)
```

### Tabular Output

```
$ ./arrl-call-sign-search.py --pretty W1AW
ARRL HQ OPERATORS CLUB, W1AW (Club)
225 MAIN ST
NEWINGTON, CT 06111
┌─────────────────────┬──────────────────────────────┐
│ ATTN                │ JOSEPH P CARCIA III          │
├─────────────────────┼──────────────────────────────┤
│ Trustee             │ CARCIA III, JOSEPH P, NJ1Q   │
├─────────────────────┼──────────────────────────────┤
│ Licensee ID         │ L00306106                    │
├─────────────────────┼──────────────────────────────┤
│ FRN                 │ 0004511143                   │
├─────────────────────┼──────────────────────────────┤
│ Radio Service       │ HA                           │
├─────────────────────┼──────────────────────────────┤
│ Issue Date          │ 12/08/2020                   │
├─────────────────────┼──────────────────────────────┤
│ Expire Date         │ 02/26/2031                   │
├─────────────────────┼──────────────────────────────┤
│ Date of Last Change │ 12/08/2020 (License Renewed) │
└─────────────────────┴──────────────────────────────┘
```
