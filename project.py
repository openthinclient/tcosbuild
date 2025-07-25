import os
from pathlib import Path

from util import shell

name = shell(r"dpkg-parsechangelog -S source")
branch_type = shell(r"git symbolic-ref --short HEAD || echo HEAD").split('/')[0]
version = shell("dpkg-parsechangelog -S version")
build_id = os.environ.get("BUILD_ID", "")

if branch_type not in ["master", "support"]:
    version = f"{version}~{branch_type}{build_id}"

package_name = f"{name}_{version}"

build_path = Path(f".build/{package_name}")
