#! usr/bin/env python3

import sys
import subprocess
import json

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

pip_cmd = '-m pip list --format=json --outdated'

if (sys.prefix != sys.base_prefix):
    console.print('Listing [green]environment[/green] packages...')
else:
    console.print('Listing [green]system[/green] packages...')

outdated_pkgs = json.loads(subprocess.check_output([sys.executable, *pip_cmd.split()]))
pkg = json.loads(subprocess.check_output([sys.executable, *pip_cmd.split()[:-1]]))

keys = tuple(key for key in outdated_pkgs[0].keys())
dict_o_outdated = dict((i[keys[0]], i[keys[2]]) for i in outdated_pkgs)

table = Table(show_header=True, header_style="bold blue")
table.add_column("#", style="dim", width=3, justify="centre")
table.add_column("Package", justify="right")
table.add_column("Version", justify="center")
table.add_column("Latest", justify="center")


for i, package in enumerate(pkg, 1):
    if package[keys[0]] in dict_o_outdated.keys():
        old_ver = package[keys[1]]
        new_ver = dict_o_outdated[package[keys[0]]]
        colour_old, colour_new = 'red', 'green'
    else:
        old_ver = new_ver = package[keys[1]]
        colour_old = colour_new = 'gray'

    table.add_row(
        str(i),
        package[keys[0]],
        Text(
            old_ver,
            style=colour_old,
        ),
        Text(
            new_ver,
            style=colour_new,
        )
    )
console.print(table)
