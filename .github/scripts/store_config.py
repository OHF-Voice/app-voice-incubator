"""Fail when the store's config changes without a new version.

The app store is a clone of this repository's default branch: every
Supervisor reads voice_incubator/config.yaml from it at once, while the
image only changes when a release is published. A config change under the
released version reaches users with the old image (0.3.3: ingress_port 0
without the run script that reads it broke the web UI). So config.yaml may
differ from the last release only in a commit that also raises the version.

Usage: python3 store_config.py [REF]   (REF: the last release; default:
the newest tag reachable from HEAD)
"""

import subprocess
import sys

import yaml

CONFIG = "voice_incubator/config.yaml"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def main() -> int:
    release = sys.argv[1] if len(sys.argv) > 1 else git("describe", "--tags", "--abbrev=0")
    released = yaml.safe_load(git("show", f"{release}:{CONFIG}"))
    current = yaml.safe_load(git("show", f"HEAD:{CONFIG}"))
    version = current.pop("version")
    released_version = released.pop("version")
    if version != released_version or current == released:
        print(f"{CONFIG}: fine (version {version}, last release {release} is {released_version})")
        return 0
    changed = sorted(key for key in current.keys() | released.keys() if current.get(key) != released.get(key))
    print(
        f"::error file={CONFIG}::{', '.join(changed)} changed since release {release}, "
        f"but the version is still {version}. The store reads this file from the default "
        "branch, so the change would reach users with the old image: change config.yaml "
        "only in the release commit that raises the version."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
