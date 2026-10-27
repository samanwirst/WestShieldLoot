"""Build WestShieldLoot using an installed Purpur server's compile dependencies."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile


ROOT = Path(__file__).resolve().parent


def classpath(server: Path, dependency_directories: list[Path]) -> list[Path]:
    explicit = [jar for directory in dependency_directories for jar in sorted(directory.glob("*.jar"))]
    return explicit + [
        *sorted((server / "libraries").rglob("*.jar")),
        *sorted((server / "plugins").glob("*.jar")),
        *sorted((server / "versions").rglob("purpur-*.jar")),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server-root", type=Path, required=True)
    parser.add_argument("--dependency-directory", type=Path, action="append", default=[])
    parser.add_argument("--javac", default="javac", help="JDK 25+ javac executable")
    args = parser.parse_args()
    libraries = classpath(args.server_root.resolve(), args.dependency_directory)
    if not libraries:
        parser.error("No compile dependencies found. Start the Purpur server once and provide the AuthMe JAR.")
    output = ROOT / "build"
    classes = output / "classes"
    if classes.exists():
        shutil.rmtree(classes)
    classes.mkdir(parents=True)
    subprocess.run(
        [args.javac, "--release", "25", "-encoding", "UTF-8", "-cp",
         os.pathsep.join(map(str, libraries)), "-d", str(classes),
         *map(str, sorted((ROOT / "src/main/java").rglob("*.java")))],
        check=True,
    )
    resources = ROOT / "src/main/resources"
    descriptor = (resources / "plugin.yml").read_text(encoding="utf-8")
    match = re.search(r"^version:\s*([\w.-]+)\s*$", descriptor, re.MULTILINE)
    if not match:
        raise ValueError("plugin.yml has no unquoted release version")
    entries = {str(path.relative_to(classes)).replace(os.sep, "/"): path.read_bytes()
               for path in classes.rglob("*.class")}
    entries.update({str(path.relative_to(resources)).replace(os.sep, "/"): path.read_bytes()
                    for path in resources.rglob("*") if path.is_file()})
    artifact = output / f"WestShieldLoot-{match[1]}.jar"
    with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(entries.items()):
            entry = zipfile.ZipInfo(name, (2026, 10, 20, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    artifact.with_suffix(".jar.sha256").write_text(f"{digest}  {artifact.name}\n", encoding="utf-8")
    print(f"{artifact.name} {digest}")


if __name__ == "__main__":
    main()
