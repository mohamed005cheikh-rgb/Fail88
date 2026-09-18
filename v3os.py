#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#
#    ███    ███    ████████    ████████    ████████
#   ████  ████   ███    ███  ███    ███  ███    ███
#   ██ ████ ██   ███         ███    ███  ███    ███
#   ██  ██  ██   ███          ████████    ████████
#   ██      ██   ███         ███    ███  ███    ███
#   ██      ██   ███    ███  ███    ███  ███    ███
#   ██      ██    ████████    ████████    ████████
#
#   M C 8 8   ·   D E E P   F R E E Z E   F O R   A N D R O I D
#
#   Mohamed Cheikh  ·  mohamed005cheikh@gmail.com
#
#   The phone stays. The reach ends.
#
# ═══════════════════════════════════════════════════════════════════════════
#
#   MC88 is state-first.
#
#   Before it touches anything on your device, it records what your device
#   already is. That record is written to a JSON file under logs/. It is the
#   ONLY thing that makes restoration possible — MC88 keeps no memory of
#   what it did beyond that file.
#
#   A tool that forgets on purpose is a tool you can trust.
#   There is no cloud, no account, no sync. Only the file on disk.
#
#   Interactive use — one question, one answer:
#
#       $ ./mc88.py
#       Freeze (Y) or Restore (N)?
#
#   Y → freeze apps according to a profile.
#   N → restore the device to the state before the last freeze.
#
#   Advanced users may invoke subcommands directly:
#
#       $ ./mc88.py doctor
#       $ ./mc88.py plan balanced
#       $ ./mc88.py apply balanced --yes
#       $ ./mc88.py restore latest --dry-run
#       $ ./mc88.py verify latest
#
#   License: MIT. See LICENSE at repository root.
#
# ═══════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional


# ─── Constants ──────────────────────────────────────────────────────────────

MC88_VERSION = "0.3.0"
MC88_SCHEMA = "mc88-state-v1"
MC88_ROOT = Path(__file__).resolve().parent
MC88_LOGS = MC88_ROOT / "logs"
MC88_PROFILES = MC88_ROOT / "profiles"
MC88_ACTIVE = MC88_ROOT / ".mc88-active"   # marker: id of the currently active session


# ─── Colors ─────────────────────────────────────────────────────────────────

def _color_enabled() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


if _color_enabled():
    RESET, DIM, BOLD = "\033[0m", "\033[2m", "\033[1m"
    CYAN, GREEN, YELLOW, RED = "\033[36m", "\033[32m", "\033[33m", "\033[31m"
else:
    RESET = DIM = BOLD = CYAN = GREEN = YELLOW = RED = ""


def say(msg: str = "") -> None:
    print(msg)


def info(msg: str) -> None:
    print(f"{CYAN}▸{RESET} {msg}")


def ok(msg: str) -> None:
    print(f"{GREEN}✓{RESET} {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}!{RESET} {msg}", file=sys.stderr)


def die(msg: str, code: int = 1) -> None:
    print(f"{RED}✗{RESET} {msg}", file=sys.stderr)
    sys.exit(code)


def banner() -> None:
    say()
    say(f"{CYAN}{BOLD}  MC88{RESET} {DIM}·{RESET} Deep Freeze for Android "
        f"{DIM}· v{MC88_VERSION}{RESET}")
    say(f"{DIM}  ──────────────────────────────────────────────────────{RESET}")
    say()


# ─── ADB wrapper ────────────────────────────────────────────────────────────

class AdbError(RuntimeError):
    pass


class Adb:
    """Thin wrapper around `adb`. One instance per invocation."""

    def __init__(self) -> None:
        if not shutil.which("adb"):
            raise AdbError("adb not found in PATH. Install Android Platform Tools.")
        self._serial: Optional[str] = None

    def _base(self) -> list[str]:
        cmd = ["adb"]
        if self._serial:
            cmd += ["-s", self._serial]
        return cmd

    def _run(self, *args: str, check: bool = True, timeout: int = 30) -> str:
        cmd = self._base() + list(args)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as e:
            raise AdbError(f"adb timed out: {' '.join(cmd)}") from e
        if check and r.returncode != 0:
            raise AdbError(f"adb failed: {' '.join(cmd)}\n{r.stderr.strip()}")
        return r.stdout

    def shell(self, *args: str, check: bool = True) -> str:
        return self._run("shell", *args, check=check)

    # ── Preconditions ────────────────────────────────────────────────────

    def select_single_device(self) -> None:
        out = self._run("devices")
        devices = [ln for ln in out.splitlines()[1:] if "\tdevice" in ln]
        if not devices:
            raise AdbError("No device connected. Enable USB debugging and reconnect.")
        if len(devices) > 1:
            raise AdbError(f"Multiple devices connected ({len(devices)}). "
                           "Disconnect all but one.")
        self._serial = devices[0].split("\t", 1)[0]

    # ── Reads ────────────────────────────────────────────────────────────

    def serial(self) -> str:
        return self._run("get-serialno").strip()

    def model(self) -> str:
        return self.shell("getprop", "ro.product.model").strip()

    def android(self) -> str:
        return self.shell("getprop", "ro.build.version.release").strip()

    def all_installed(self) -> set[str]:
        out = self.shell("pm", "list", "packages", "--user", "0")
        return {ln[8:] for ln in out.splitlines() if ln.startswith("package:")}

    def all_disabled(self) -> set[str]:
        out = self.shell("pm", "list", "packages", "-d", "--user", "0")
        return {ln[8:] for ln in out.splitlines() if ln.startswith("package:")}

    def wifi(self) -> str:
        return self.shell("settings", "get", "global", "wifi_on").strip()

    def bluetooth(self) -> str:
        return self.shell("settings", "get", "global", "bluetooth_on").strip()

    def airplane(self) -> str:
        return self.shell("settings", "get", "global", "airplane_mode_on").strip()

    # ── Writes ───────────────────────────────────────────────────────────

    def disable(self, pkg: str) -> bool:
        try:
            self.shell("pm", "disable-user", "--user", "0", pkg, check=True)
            return True
        except AdbError:
            return False

    def enable(self, pkg: str) -> bool:
        try:
            self.shell("pm", "enable", "--user", "0", pkg, check=True)
            return True
        except AdbError:
            return False

    def wifi_set(self, on: bool) -> bool:
        try:
            self.shell("svc", "wifi", "enable" if on else "disable", check=True)
            return True
        except AdbError:
            return False

    def bluetooth_set(self, on: bool) -> bool:
        try:
            self.shell("svc", "bluetooth", "enable" if on else "disable", check=True)
            return True
        except AdbError:
            return False


# ─── Package state ──────────────────────────────────────────────────────────

@dataclass
class PackageSnapshot:
    """A snapshot of packages relevant to a profile."""
    states: dict[str, str] = field(default_factory=dict)  # pkg -> enabled|disabled-user|absent

    @classmethod
    def read(cls, adb: Adb, packages: Iterable[str]) -> "PackageSnapshot":
        installed = adb.all_installed()
        disabled = adb.all_disabled()
        snap: dict[str, str] = {}
        for pkg in packages:
            if pkg not in installed:
                snap[pkg] = "absent"
            elif pkg in disabled:
                snap[pkg] = "disabled-user"
            else:
                snap[pkg] = "enabled"
        return cls(states=snap)


@dataclass
class NetworkSnapshot:
    wifi: str = "unknown"
    bluetooth: str = "unknown"
    airplane_mode: str = "unknown"

    @classmethod
    def read(cls, adb: Adb) -> "NetworkSnapshot":
        return cls(
            wifi=adb.wifi(),
            bluetooth=adb.bluetooth(),
            airplane_mode=adb.airplane(),
        )


# ─── Session log ────────────────────────────────────────────────────────────

@dataclass
class SessionLog:
    schema: str
    session: dict
    device: dict
    before: dict
    actions: list
    after: dict

    @classmethod
    def new(
        cls,
        session_id: str,
        profile: str,
        device: dict,
        before_packages: PackageSnapshot,
        before_network: NetworkSnapshot,
    ) -> "SessionLog":
        return cls(
            schema=MC88_SCHEMA,
            session={
                "id": session_id,
                "created_at": datetime.now(timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ"),
                "profile": profile,
                "mc88_version": MC88_VERSION,
            },
            device=device,
            before={
                "packages": dict(before_packages.states),
                "network": asdict(before_network),
            },
            actions=[],
            after={},
        )

    def add_action(self, action_type: str, target: str, **extra) -> None:
        self.actions.append({
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "type": action_type,
            "target": target,
            **extra,
        })

    def finalize(self, after_packages: PackageSnapshot,
                 after_network: NetworkSnapshot) -> None:
        self.after = {
            "packages": dict(after_packages.states),
            "network": asdict(after_network),
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write: temp + rename, so a crash never leaves a half-written log.
        fd, tmp = tempfile.mkstemp(dir=str(path.parent),
                                   prefix=".mc88-", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(asdict(self), f, indent=2, ensure_ascii=False)
                f.write("\n")
            os.replace(tmp, path)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    @classmethod
    def load(cls, path: Path) -> "SessionLog":
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema") != MC88_SCHEMA:
            raise ValueError(f"Unsupported schema: {data.get('schema')!r}")
        return cls(**data)


# ─── Profiles ───────────────────────────────────────────────────────────────

@dataclass
class Profile:
    name: str
    packages: list[str]
    network_off: bool  # true if the profile's header says "network: on"

    @classmethod
    def load(cls, name: str) -> "Profile":
        path = MC88_PROFILES / f"{name}.txt"
        if not path.exists():
            die(f"Unknown profile: {name}. Look in {MC88_PROFILES}/.")
        packages: list[str] = []
        network_off = False
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                if "network:" in line and "on" in line.split("network:", 1)[1]:
                    network_off = True
                continue
            packages.append(line.split()[0])  # tolerate trailing whitespace
        return cls(name=name, packages=packages, network_off=network_off)

    @staticmethod
    def available() -> list[str]:
        if not MC88_PROFILES.exists():
            return []
        return sorted(p.stem for p in MC88_PROFILES.glob("*.txt"))


# ─── Session path helpers ───────────────────────────────────────────────────

def new_session_id() -> str:
    return "mc88-" + datetime.now().strftime("%Y%m%d-%H%M%S")


def session_path(session_id: str) -> Path:
    return MC88_LOGS / f"{session_id}.json"


def resolve_session(arg: str) -> Path:
    """arg may be 'latest', an id, or a path."""
    if arg == "latest":
        candidates = sorted(MC88_LOGS.glob("mc88-*.json"),
                            key=lambda p: p.stat().st_mtime, reverse=True)
        if not candidates:
            die(f"No session logs found in {MC88_LOGS}/.")
        return candidates[0]
    p = Path(arg)
    if p.exists():
        return p
    p = session_path(arg)
    if p.exists():
        return p
    die(f"Session not found: {arg}")


# ─── Active-session marker ──────────────────────────────────────────────────

def active_session_id() -> Optional[str]:
    """Return the id of the currently-active session, or None."""
    if not MC88_ACTIVE.exists():
        return None
    sid = MC88_ACTIVE.read_text(encoding="utf-8").strip()
    if not sid:
        return None
    # Sanity: the marker must point to a real log file. If not, forget it.
    if not session_path(sid).exists():
        MC88_ACTIVE.unlink(missing_ok=True)
        return None
    return sid


def set_active_session(session_id: str) -> None:
    MC88_ACTIVE.write_text(session_id + "\n", encoding="utf-8")


def clear_active_session() -> None:
    MC88_ACTIVE.unlink(missing_ok=True)


# ─── Core operations (reused by both CLI and interactive mode) ──────────────

def _do_apply(adb: Adb, profile_name: str, *, confirm: bool = True) -> int:
    """Core apply logic. Assumes a device is already selected."""
    profile = Profile.load(profile_name)

    info("Reading pre-change state…")
    before_pkgs = PackageSnapshot.read(adb, profile.packages)
    before_net = NetworkSnapshot.read(adb)

    to_freeze = [p for p, s in before_pkgs.states.items() if s == "enabled"]
    if not to_freeze and not profile.network_off:
        warn("Nothing to do — profile has no actionable items on this device.")
        return 0

    if confirm:
        say()
        if to_freeze:
            say("  The following packages will be frozen:")
            for pkg in to_freeze:
                say(f"    {DIM}·{RESET} {pkg}")
        if profile.network_off:
            say()
            say("  Network toggles will be set to OFF (wifi, bluetooth).")
        say()
        reply = input("  Proceed? [y/N] ").strip().lower()
        if reply not in ("y", "yes"):
            warn("Cancelled.")
            return 0

    session_id = new_session_id()
    log = SessionLog.new(
        session_id=session_id,
        profile=profile.name,
        device={
            "serial": adb.serial(),
            "model": adb.model(),
            "android": adb.android(),
        },
        before_packages=before_pkgs,
        before_network=before_net,
    )
    log_path = session_path(session_id)
    log.save(log_path)   # written now; rewritten at the end with actions+after
    info(f"Session: {session_id}")

    info("Applying freeze…")
    for pkg in to_freeze:
        if adb.disable(pkg):
            ok(f"frozen  {pkg}")
            log.add_action("disable", pkg)
        else:
            warn(f"failed  {pkg}")

    if profile.network_off:
        info("Applying network restrictions…")
        if before_net.wifi == "1" and adb.wifi_set(False):
            ok("wifi disabled")
            log.add_action("network", "wifi", to="0")
        if before_net.bluetooth == "1" and adb.bluetooth_set(False):
            ok("bluetooth disabled")
            log.add_action("network", "bluetooth", to="0")

    after_pkgs = PackageSnapshot.read(adb, profile.packages)
    after_net = NetworkSnapshot.read(adb)
    log.finalize(after_pkgs, after_net)
    log.save(log_path)
    set_active_session(session_id)

    say()
    ok(f"Session recorded: {log_path}")
    say(f"  {DIM}Next run of mc88.py will offer to restore this session.{RESET}")
    return 0


def _do_restore(adb: Optional[Adb], log_path: Path, *,
                confirm: bool = True, dry_run: bool = False) -> int:
    """Core restore logic. `adb` may be None only in dry-run mode."""
    log = SessionLog.load(log_path)

    to_enable: list[str] = []
    if not dry_run:
        assert adb is not None
        current_installed = adb.all_installed()
        current_disabled = adb.all_disabled()

    for pkg, state in log.before.get("packages", {}).items():
        if state != "enabled":
            continue
        if dry_run:
            to_enable.append(pkg)
        else:
            assert adb is not None
            if pkg in current_installed and pkg in current_disabled:
                to_enable.append(pkg)

    net_actions = [a["target"] for a in log.actions if a.get("type") == "network"]

    info("Plan:")
    if not to_enable and not net_actions:
        say(f"    {DIM}(nothing to restore){RESET}")
        clear_active_session()
        return 0
    for pkg in to_enable:
        say(f"    {GREEN}enable{RESET}      {pkg}")
    for t in net_actions:
        say(f"    {GREEN}network on{RESET}  {t}")

    if dry_run:
        say()
        ok("Dry-run complete. No changes made.")
        return 0

    if confirm:
        say()
        reply = input("  Proceed? [y/N] ").strip().lower()
        if reply not in ("y", "yes"):
            warn("Cancelled.")
            return 0

    assert adb is not None
    say()
    for pkg in to_enable:
        if adb.enable(pkg):
            ok(f"enabled  {pkg}")
        else:
            warn(f"failed   {pkg}")

    for t in net_actions:
        if t == "wifi" and adb.wifi_set(True):
            ok("wifi enabled")
        elif t == "bluetooth" and adb.bluetooth_set(True):
            ok("bluetooth enabled")
        else:
            warn(f"network restore failed: {t}")

    clear_active_session()
    say()
    ok(f"Restore complete — device is as it was before {log.session['id']}.")
    return 0


# ─── Commands ───────────────────────────────────────────────────────────────

def cmd_doctor(_: argparse.Namespace) -> int:
    banner()
    info("Checking environment…")

    if not shutil.which("adb"):
        die("adb not found in PATH.")
    ok("adb is installed")

    try:
        adb = Adb()
        out = adb._run("devices")
        devices = [ln for ln in out.splitlines()[1:] if "\tdevice" in ln]
        if devices:
            adb._serial = devices[0].split("\t", 1)[0]
            ok("Device connected")
            say(f"    serial  : {adb.serial()}")
            say(f"    model   : {adb.model()}")
            say(f"    android : {adb.android()}")
        else:
            warn("No device connected (fine for a dry check)")
    except AdbError as e:
        warn(str(e))

    MC88_LOGS.mkdir(parents=True, exist_ok=True)
    ok(f"Log directory: {MC88_LOGS}")

    say()
    info("Available profiles:")
    names = Profile.available()
    if not names:
        warn(f"No profiles found in {MC88_PROFILES}/.")
    for name in names:
        p = Profile.load(name)
        say(f"    {name}  {DIM}({len(p.packages)} packages){RESET}")

    say()
    active = active_session_id()
    if active:
        say(f"  {YELLOW}Active session:{RESET} {active}")
    else:
        say(f"  {DIM}No active session.{RESET}")
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    banner()
    info("Reading current device state (read-only)…")
    adb = Adb()
    adb.select_single_device()

    say(f"    serial  : {adb.serial()}")
    say(f"    model   : {adb.model()}")
    say(f"    android : {adb.android()}")
    say()

    net = NetworkSnapshot.read(adb)
    say("  Network:")
    for label, val in (("wifi", net.wifi),
                       ("bluetooth", net.bluetooth),
                       ("airplane", net.airplane_mode)):
        state = "on" if val == "1" else "off" if val == "0" else val
        say(f"    {label:<12}: {state}")
    say()

    say("  Frozen packages (disabled for user 0):")
    disabled = sorted(adb.all_disabled())
    if not disabled:
        say(f"    {DIM}(none){RESET}")
    else:
        for pkg in disabled:
            say(f"    {DIM}·{RESET} {pkg}")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    banner()
    info(f"Planning profile: {BOLD}{args.profile}{RESET}")
    adb = Adb()
    adb.select_single_device()

    profile = Profile.load(args.profile)
    before = PackageSnapshot.read(adb, profile.packages)

    will_freeze = already = missing = 0
    for pkg, state in before.states.items():
        if state == "enabled":
            say(f"    {GREEN}would freeze{RESET}  {pkg}")
            will_freeze += 1
        elif state == "disabled-user":
            say(f"    {DIM}already frozen{RESET}  {pkg}")
            already += 1
        else:
            say(f"    {YELLOW}not installed{RESET}  {pkg}")
            missing += 1

    say()
    say(f"  {BOLD}Summary{RESET}")
    say(f"    listed      : {len(profile.packages)}")
    say(f"    to freeze   : {will_freeze}")
    say(f"    already     : {already}")
    say(f"    absent      : {missing}")
    if profile.network_off:
        say()
        warn("This profile also disables WiFi and Bluetooth (network: on).")
    say()
    say(f"  {DIM}No changes made. Run 'mc88.py apply {args.profile}' to execute.{RESET}")
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    banner()
    info(f"Applying profile: {BOLD}{args.profile}{RESET}")
    adb = Adb()
    adb.select_single_device()
    return _do_apply(adb, args.profile, confirm=not args.yes)


def cmd_unfreeze(args: argparse.Namespace) -> int:
    banner()
    info(f"Unfreezing: {args.package}")
    adb = Adb()
    adb.select_single_device()

    if args.package not in adb.all_installed():
        die(f"Package not installed: {args.package}")
    if args.package not in adb.all_disabled():
        ok("already enabled")
        return 0

    if adb.enable(args.package):
        ok(f"enabled {args.package}")
        return 0
    die(f"could not enable {args.package}")


def cmd_sessions(_: argparse.Namespace) -> int:
    banner()
    info(f"Session logs in {MC88_LOGS}")
    MC88_LOGS.mkdir(parents=True, exist_ok=True)
    files = sorted(MC88_LOGS.glob("mc88-*.json"),
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        say(f"    {DIM}(none){RESET}")
        return 0
    active = active_session_id()
    for f in files:
        size = f.stat().st_size
        marker = f" {GREEN}← active{RESET}" if active and f.stem == active else ""
        say(f"    {DIM}·{RESET} {f.stem}  {DIM}({size} bytes){RESET}{marker}")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    banner()
    log_path = resolve_session(args.session)
    info(f"Session: {log_path}")
    log = SessionLog.load(log_path)
    say(f"    session : {log.session['id']}")
    say(f"    profile : {log.session['profile']}")
    say()

    adb: Optional[Adb] = None
    if not args.dry_run:
        adb = Adb()
        adb.select_single_device()
    return _do_restore(adb, log_path, confirm=True, dry_run=args.dry_run)


def cmd_verify(args: argparse.Namespace) -> int:
    banner()
    log_path = resolve_session(args.session)
    info(f"Verifying against: {log_path}")
    log = SessionLog.load(log_path)

    adb = Adb()
    adb.select_single_device()
    installed = adb.all_installed()
    disabled = adb.all_disabled()

    mismatches = 0
    for pkg, expected in log.before.get("packages", {}).items():
        if pkg not in installed:
            actual = "absent"
        elif pkg in disabled:
            actual = "disabled-user"
        else:
            actual = "enabled"
        if actual == expected:
            ok(f"match    {pkg}  ({actual})")
        else:
            warn(f"differs  {pkg}  expected={expected} actual={actual}")
            mismatches += 1

    say()
    if mismatches == 0:
        ok("All recorded packages match their pre-session state.")
        return 0
    warn(f"{mismatches} package(s) differ. Run restore, or accept the change.")
    return 1


# ─── Interactive mode: one question, one answer ─────────────────────────────

def cmd_interactive(_: argparse.Namespace) -> int:
    """The default UX: one question. Y = freeze, N = restore."""
    banner()

    # ── Device must be present before we ask anything ────────────────────
    adb = Adb()
    adb.select_single_device()

    say(f"    device  : {adb.model()} (Android {adb.android()})")
    say()

    # ── Detect current state ─────────────────────────────────────────────
    active = active_session_id()
    if active:
        log = SessionLog.load(session_path(active))
        frozen_count = sum(
            1 for s in log.after.get("packages", {}).values()
            if s == "disabled-user"
        )
        say(f"  {YELLOW}MC88 session is active.{RESET}")
        say(f"    session : {active}")
        say(f"    profile : {log.session['profile']}")
        say(f"    frozen  : {frozen_count} package(s)")
    else:
        say(f"  {DIM}No MC88 session is currently active.{RESET}")
    say()

    # ── THE question ─────────────────────────────────────────────────────
    say(f"  {BOLD}Freeze (Y) or Restore (N)?{RESET}  [Y/n]")
    try:
        reply = input("  > ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        say()
        warn("Cancelled.")
        return 0

    # ── Y = freeze ───────────────────────────────────────────────────────
    if reply in ("", "y", "yes"):
        profiles = Profile.available()
        if not profiles:
            die(f"No profiles found in {MC88_PROFILES}/.")

        if active:
            say()
            warn(f"A session is already active ({active}).")
            try:
                ans = input("  Freeze again anyway? [y/N] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                say()
                warn("Cancelled.")
                return 0
            if ans not in ("y", "yes"):
                warn("Cancelled.")
                return 0

        say()
        say(f"  {BOLD}Available profiles:{RESET}")
        default_idx = 1
        for i, name in enumerate(profiles, 1):
            p = Profile.load(name)
            marker = ""
            if name == "balanced":
                default_idx = i
                marker = f" {DIM}(recommended){RESET}"
            say(f"    [{i}] {name:<12} {DIM}({len(p.packages)} packages){RESET}{marker}")
        say()

        try:
            choice = input(
                f"  Choose a profile [1-{len(profiles)}, default {default_idx}] > "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            say()
            warn("Cancelled.")
            return 0

        if not choice:
            choice = str(default_idx)
        if not choice.isdigit() or not (1 <= int(choice) <= len(profiles)):
            warn(f"Invalid choice: {choice!r}")
            return 1

        profile_name = profiles[int(choice) - 1]
        say()
        # Top-level question was already answered — skip the second confirm.
        return _do_apply(adb, profile_name, confirm=False)

    # ── N = restore ──────────────────────────────────────────────────────
    if reply in ("n", "no"):
        if not active:
            say()
            warn("No active MC88 session to restore from.")
            say(f"  {DIM}(You have not frozen anything yet.){RESET}")
            return 1
        return _do_restore(adb, session_path(active), confirm=False)

    # ── Anything else ────────────────────────────────────────────────────
    warn(f"Unrecognized answer: {reply!r}  (expected y or n)")
    return 1


# ─── Argparse ───────────────────────────────────────────────────────────────

def build_parser(argv: Optional[list[str]] = None) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mc88.py",
        description="MC88 · Deep Freeze for Android — state-first, reversible. "
                    "Run without arguments for the interactive wizard.",
        epilog="MC88 · Mohamed Cheikh · mohamed005cheikh@gmail.com",
    )
    p.add_argument("--version", action="version",
                   version=f"MC88 {MC88_VERSION} (schema {MC88_SCHEMA})")
    sub = p.add_subparsers(dest="cmd", required=False)

    sub.add_parser("doctor", help="Check environment and list profiles")
    sub.add_parser("status", help="Read device state (no changes)")
    sub.add_parser("sessions", help="List session logs")
    sub.add_parser("help", help="Show this message")

    pl = sub.add_parser("plan", help="Show what would change (no changes)")
    pl.add_argument("profile")

    ap = sub.add_parser("apply", help="Record state, then apply a profile")
    ap.add_argument("profile")
    ap.add_argument("-y", "--yes", action="store_true",
                    help="Skip the confirmation prompt")

    uf = sub.add_parser("unfreeze", help="Re-enable a single package")
    uf.add_argument("package")

    rs = sub.add_parser("restore", help="Restore from a session log")
    rs.add_argument("session", nargs="?", default="latest",
                    help="Session id, path, or 'latest' (default)")
    rs.add_argument("--dry-run", action="store_true",
                    help="Show plan only, do not touch the device")

    vf = sub.add_parser("verify", help="Verify device against a session log")
    vf.add_argument("session", nargs="?", default="latest")

    return p


# ─── Signal handling ────────────────────────────────────────────────────────

def _install_signal_handlers() -> None:
    """Exit cleanly on Ctrl+C. Session logs are written atomically, so a
    mid-operation interrupt never leaves a half-written file on disk."""
    def _handler(_signum, _frame):
        say()
        warn("Interrupted.")
        sys.exit(130)
    signal.signal(signal.SIGINT, _handler)
    signal.signal(signal.SIGTERM, _handler)


# ─── Entry point ────────────────────────────────────────────────────────────

def main(argv: Optional[list[str]] = None) -> int:
    _install_signal_handlers()
    parser = build_parser(argv)
    args = parser.parse_args(argv)

    # No subcommand → interactive wizard.
    if not args.cmd:
        try:
            return cmd_interactive(args)
        except AdbError as e:
            die(str(e))
            return 1
        except ValueError as e:
            die(str(e))
            return 1

    if args.cmd == "help":
        banner()
        parser.print_help()
        say()
        say(f"  {DIM}State first. Action second. The log is the only memory.{RESET}")
        say()
        return 0

    handlers = {
        "doctor": cmd_doctor,
        "status": cmd_status,
        "plan": cmd_plan,
        "apply": cmd_apply,
        "unfreeze": cmd_unfreeze,
        "sessions": cmd_sessions,
        "restore": cmd_restore,
        "verify": cmd_verify,
    }
    fn = handlers.get(args.cmd)
    if fn is None:
        die(f"Unknown command: {args.cmd}")
    try:
        return fn(args)
    except AdbError as e:
        die(str(e))
        return 1
    except ValueError as e:
        die(str(e))
        return 1


if __name__ == "__main__":
    sys.exit(main())