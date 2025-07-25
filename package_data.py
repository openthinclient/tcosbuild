import shutil
from pathlib import Path
from subprocess import run

from project import package_name, build_path, name

def build_package_data():
    package_data_dir = build_path / 'package-data'

    sfs_package_dir = package_data_dir / 'sfs' / 'package'
    sfs_package_dir.mkdir(parents=True)
    shutil.copy2(f'.build/{package_name}/{name}.sfs', sfs_package_dir)
    shutil.copy2(build_path / 'changelog',
                 sfs_package_dir / f'{name}.changelog')

    # Copies schema/ (if schema/ exists)
    schema_dir = Path('schema')
    if schema_dir.exists() and schema_dir.is_dir():
        shutil.copytree(schema_dir, package_data_dir / schema_dir)

    # Copies package-metadata/ (if package-metadata/ exists)
    package_metadata_dir = Path('package-metadata')
    if package_metadata_dir.exists() and package_metadata_dir.is_dir():
        shutil.copytree(package_metadata_dir,
                        package_data_dir / package_metadata_dir)

    # Copies custom/ (if custom/ exists)
    custom_dir = Path('custom')
    if custom_dir.exists() and custom_dir.is_dir():
        shutil.copytree(custom_dir, package_data_dir / custom_dir)

    run(['zsyncmake', f'{sfs_package_dir}/{name}.sfs',
        '-o', f'{sfs_package_dir}/{name}.sfs.zsync',
        '-u', f'{name}.sfs'])
