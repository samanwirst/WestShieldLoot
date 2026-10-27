# WestShieldLoot

Personal, permanent vanilla loot for natural containers on **Purpur 26.2 / Java 25**.
Developed for WestShield by Minecraft Club and WestDevs. Original open-source
implementation, licensed under **GPL-3.0-only**.

Each account receives its own random vanilla roll the first time it opens a natural
container. Returning to that container shows the same remaining items forever.
There are no refills, timers, paid unlocks or player reset commands.

## Features

- Natural chests, double chests, barrels and chest minecarts.
- Independent vanilla random rolls per account and container; matching results are possible.
- Shared Java/Bedrock history when WestShieldAccounts supplies the same canonical UUID.
- Take-only inventories; full inventories never consume rewards or spill them on the ground.
- Durable SQLite seeds, remaining contents, delivery receipts and destruction history.
- Containers remain breakable. Destruction permanently removes every account's unclaimed loot.
- Replacing a destroyed container does not recreate its rewards.
- Existing authentication/claim denials are respected; hopper extraction and insertion are blocked.
- Trial Vaults, keys and rewards remain vanilla.
- The Overworld and Nether are enabled by default. Creative worlds and the End are excluded.

Already emptied ordinary containers without an original loot table are not reconstructed.
The plugin does not provide client mods, generate extra loot on edition changes or replace AuthMe.

## Requirements

| Dependency | Requirement |
| --- | --- |
| Minecraft server | Purpur **26.2**; other Minecraft versions are refused at runtime |
| Runtime | Java **25**; build with JDK 25 or newer |
| Authentication | AuthMe, tested with 6.0.1-b2770 |
| Account identity | WestShieldAccounts 1.0.0, required by the plugin descriptor |
| Bedrock connections | Geyser + Floodgate and the shared-account adapter |
| Database driver | SQLite JDBC 3.49.1.0, downloaded by Paper's plugin library loader |

[WestShieldAccounts source and build tooling](https://github.com/samanwirst/westshield-simpleclans/tree/westshield-26.2/westshield/english/adapters/accounts)
are public in the WestShield server-adapters repository. It is a separate required
plugin, not bundled into WestShieldLoot. AuthMe remains responsible for account
authentication on both editions. Equal names alone do not grant this plugin any
authentication authority.

## Installation

1. Back up the worlds and plugin data, then stop the server cleanly.
2. Install the required authentication and account plugins first.
3. Download the JAR from [Releases](https://github.com/samanwirst/WestShieldLoot/releases)
   and place it in `plugins/`.
4. Start the server and run `westshieldloot status` in the console.
5. Confirm `ready=true`, `failures=0` and `unresolved-transfers=0`.

Players simply open an eligible natural container. Left-click or shift-click takes
a stack; right-click takes one item. Deposits, drag transfers and hotbar swaps are
disabled. No player command or resource pack is required.

The generated configuration is `plugins/WestShieldLoot/config.yml`.
The persistent database is `plugins/WestShieldLoot/loot.sqlite`.

## Administration

| Command | Purpose |
| --- | --- |
| `/westshieldloot status` | Readiness, failure counters and durable record counts |
| `/westshieldloot inspect` | Inspect the registered container targeted by the player |

Both commands require `westshieldloot.admin`, granted to operators by default.
Players must also be authenticated. There is no refill, restore or reset command.

## Build from source

The build script uses Python 3.10+ standard-library modules and an installed
Purpur server's dependency cache. Run the server once to populate `libraries/`,
then provide its root directory and a directory containing the AuthMe JAR:

```sh
git clone https://github.com/samanwirst/WestShieldLoot.git
cd WestShieldLoot
python3 build.py --server-root /path/to/purpur-server \
  --dependency-directory /path/to/authme-and-account-jars
```

Output: `build/WestShieldLoot-1.0.0.jar` and its SHA-256 checksum.
The target is Java 25 regardless of the compiler's host version. Server binaries,
private plugin configurations and credentials are not distributed in this repo.

The v1.0.0 release is the exact artifact installed on WestShield:

```text
a4f19a65451ae0d57ab431aad52b5ebad6c84c2f7436bf542d97223d8b45ff56  WestShieldLoot-1.0.0.jar
```

## Verification

Run the self-contained storage checks against a fresh temporary database:

```sh
python3 tests/storage.py --server-root /path/to/purpur-server
```

They check permanent seed reservation, transactional debit, restart recovery,
unknown-state holds, independent accounts and permanent destruction.

The release passed **29 storage checks, 23 native loopback checks and 12 additional
integration checks**. The published [receipts](verification/) distinguish local
gameplay acceptance from the narrower production startup/status checks.
Java/Bedrock identity was exercised with an encrypted native Floodgate handshake.
Physical Bedrock touch/controller rendering has not been tested.

The advanced [integration harness](tests/integration/README.md) requires an
explicitly prepared disposable loopback fixture. Its test-only plugins, fictional
accounts and movement exemptions must remain outside production.

## Data and recovery

Back up the entire plugin directory together with the worlds and player data.
Use a clean stop for a consistent full snapshot. Do not restore an older loot
database over newer player inventories or delete it to resolve an incident:
consumption history is essential to preventing duplicate rewards.

SQLite and Minecraft player files are separate storage systems. The plugin keeps
exact delivery receipts and holds unknown states for review; it does not claim
atomic recovery across arbitrary crashes or unrelated plugin writes. CoreProtect
block rollback does not roll back this database. Removing the plugin does not
return unclaimed virtual items to physical containers.

See [DESIGN.md](DESIGN.md) for eligibility rules, persistence boundaries and test
qualifications, and [CHANGELOG.md](CHANGELOG.md) for release notes.

## License and contributions

Source is available under the [GNU General Public License v3.0](LICENSE),
SPDX identifier `GPL-3.0-only`. You may use, study, modify and redistribute it under
that license. Third-party runtime dependencies retain their own licenses and are
not included in the release JAR. This implementation contains no Lootr or other
third-party loot-plugin source code.

Issues and pull requests are welcome. Keep credentials, database files and real
player records out of bug reports; use a disposable reproduction world.
