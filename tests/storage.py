"""Run permanent-roll and delivery-journal checks against a fresh temporary database."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server-root", type=Path, required=True)
    parser.add_argument("--java", default="java", help="Java 25+ executable")
    parser.add_argument("--javac", default="javac", help="JDK 25+ javac executable")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    libraries = [jar for group in ["org/xerial/sqlite-jdbc", "org/slf4j/slf4j-api"]
                 for jar in sorted((args.server_root / "libraries" / group).rglob("*.jar"))]
    if not libraries:
        parser.error("SQLite JDBC and SLF4J compile dependencies were not found in the server cache")
    with tempfile.TemporaryDirectory(prefix="westshieldloot-checks-") as temporary:
        path = Path(temporary)
        classpath = os.pathsep.join(map(str, libraries))
        subprocess.run(
            [args.javac, "--release", "25", "-cp", classpath, "-d", str(path),
             str(root / "src/main/java/com/westshield/loot/LootStore.java"),
             str(root / "tests/StoreChecks.java")], check=True,
        )
        subprocess.run(
            [args.java, "--enable-native-access=ALL-UNNAMED", "-cp",
             str(path) + os.pathsep + classpath, "StoreChecks", str(path / "checks.sqlite")],
            check=True,
        )


if __name__ == "__main__":
    main()
