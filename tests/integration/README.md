# Disposable loopback integration checks

These scripts operate on a prepared synthetic Purpur 26.2 fixture, not an arbitrary
production installation. Do not pass production data as the template. The scripts
copy the template, create fictional actors, remap loopback ports and modify only
the disposable copy. Test output can contain generated passwords and player data;
keep fixture output private and outside Git.

Prerequisites:

- Java/JDK 25+ and Python dependencies from `requirements-test.txt`.
- A built `build/WestShieldLoot-1.0.0.jar`.
- A disposable server template listening only on `127.0.0.1`, with the WestShield
  authentication/account adapters and the plugins referenced by the harness.
- The test-only `AutoProbe` hostname helper from the existing
  [shared-account test fixture](https://github.com/samanwirst/westshield-simpleclans/tree/westshield-26.2/westshield/accounts/integration).
  It supplies an encrypted native Floodgate handshake. Its private test keys and
  world template are deliberately not distributed here.

The template's ports are 25711–25717 and are remapped to 25721–25727.
The template must include the Geyser, BlueMap, Plan, SimpleVoice-Geyser, voicechat,
LightAntiCheat, LuckPerms and Caddy configurations referenced by `smoke.py`.
This is the server-specific acceptance harness, not a universal turnkey fixture.

```sh
python3 -m pip install -r requirements-test.txt
python3 tests/integration/smoke.py \
  --template /path/to/disposable-loopback-template \
  --server-root /path/to/purpur-server \
  --output /private/path/to/new-acceptance-run \
  --java /path/to/java25/bin/java \
  --confirm-synthetic-template

python3 tests/integration/extra.py \
  --fixture /private/path/to/new-acceptance-run/server \
  --server-root /path/to/purpur-server \
  --output /private/path/to/new-additional-run \
  --java /path/to/java25/bin/java \
  --confirm-synthetic-template
```

`LootProbe.java` is console-only fixture instrumentation. It encodes real inventory
click/use packets using the pinned server codec. Minecart checks use Bukkit
interaction/destruction events. Minimal Java actors receive a fixture-only Grim
movement exemption; production permissions are never changed by these tests.
The handshake verifies canonical identity, not a physical Bedrock client UI.

The public `verification/` directory contains sanitized historical release
receipts. The storage test at `tests/storage.py` needs no prepared game world,
credentials or fixture-only helper and can be run independently.
