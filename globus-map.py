#!/usr/bin/python3

import getopt
import json
import re
import sys


def main(args):
    dump=str(args)
    g=open("/tmp/dump","a")
    g.write(dump)
    g.close()
    opts, args = getopt.getopt(args, "as:c:")

    all_flag = False
    connector = None
    storage_gateway = None

    for o in opts:
        if o[0] == "-a":
            all_flag = True
        elif o[0] == "-c":
            connector = o[1]
        elif o[0] == "-s":
            storage_gateway = o[1]

    input_data = json.load(sys.stdin)

    if input_data.get("DATA_TYPE") != "identity_mapping_input#1.0.0":
        sys.exit("Invalid input DATA_TYPE")

    output_doc = {"DATA_TYPE": "identity_mapping_output#1.0.0", "result": []}

    mappings = read_mapfile(connector, storage_gateway)
    for i in input_data.get("identities"):
        res = map_identity(i, mappings, all_flag)
        if res:
            output_doc["result"].extend(res)
            if not all_flag:
                break
    json.dump(output_doc, fp=sys.stdout)
    sys.exit(0)


import pickle

def read_mapfile(connector, storage_gateway):
    # Parses a simple mapping file containing entries
    # "identity_username" local_username[,local_username...]
    mapfile = "/etc/grid-security/gridmap"
    mappings = []

    mapre = re.compile(r'"([^"]*)"\s+(\S*)\s+(\S*)$')
    with open(mapfile, "r") as f:
        for line in f:
            m = mapre.match(line.strip())
            if m:
                identity_username = m.group(1)
                local_usernames = m.group(3).split(",")
                for ln in local_usernames:
                    mapping = (identity_username, ln)
                    mappings.append(mapping)
    pickle.dump(mappings,open("/tmp/see.pkl","wb"));
    return mappings


def map_identity(identity, mappings, all_flag):
    res = []
    for m in mappings:
        if m[0] == identity["username"]:
            res.append({"id": identity["id"], "output": m[1]})
            if not all_flag:
                break
    return res


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
