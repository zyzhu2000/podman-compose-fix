#!/usr/bin/env python3

import argparse
import sys
import subprocess
import yaml
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument('-f', dest="file", nargs=1)

args, unknown = parser.parse_known_intermixed_args()

flag = 0
l_cmd = ['podman-compose'] + sys.argv[1:]

ret = subprocess.run(l_cmd, check=False, capture_output=True, text=True)
if ret.returncode!=0:
    flag = 1

if 'config' != args.command:
    flag = 1


if args.file is None or not isinstance(args.file, list) or len(args.file)!=1:
    flag = 1

if flag==0:
    file = pathlib.Path(args.file[0])
    if file.exists():
        base_path = file.parent.resolve()
    else:
        flag = 1

if flag==0:
    try:
        config = yaml.safe_load(ret.stdout)
    except yaml.YAMLError:
        flag = 1

if flag==1:
    print(ret.stderr, file=sys.stderr, end="")
    print(ret.stdout, file=sys.stdout, end="")
    sys.exit(ret.returncode)

def recursive_fix(d: dict):
    for k, v in d.items():
        if isinstance(v, dict):
            recursive_fix(v)
        elif k=='context' and isinstance(v, str):
            rel_path = pathlib.Path(v)
            rel_path2 = base_path / rel_path
            abs_path = rel_path2.resolve()
            d[k] = abs_path.as_posix()


recursive_fix(config)

#   https://stackoverflow.com/questions/37200150/can-i-dump-blank-instead-of-null-in-yaml-pyyaml
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

yaml.representer.SafeRepresenter.add_representer(type(None), represent_none)


yaml.safe_dump(config, sys.stdout)

