from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_SHA256 = "89aca5abff3b3c14aca5d8865e8583994bff611bc0c4de94ec1c8a7ef7aaeed3"

URLS = [
    "https://air.flyingway.com/books/ac_61-23c_phak_canada.pdf",
    "http://air.flyingway.com/books/ac_61-23c_phak_canada.pdf",
    "https://air.flyingway.com/books/ac_61-23c_phak_canada.pdf?download=1",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def try_curl(url: str, destination: Path) -> str | None:
    command = [
        "curl",
        "--fail",
        "--location",
        "--silent",
        "--show-error",
        "--retry",
        "3",
        "--retry-delay",
        "2",
        "--http1.1",
        "--user-agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36",
        "--referer",
        "https://air.flyingway.com/",
        "--header",
        "Accept: application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
        "--output",
        str(destination),
        url,
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return f"curl exit {result.returncode}: {result.stderr.strip()}"
    if not destination.exists():
        return "curl reported success but produced no file"
    actual = sha256(destination)
    if actual != EXPECTED_SHA256:
        size = destination.stat().st_size
        return f"SHA mismatch ({actual}, {size} bytes)"
    return None


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: fetch_exact_pof_handbook.py OUTPUT_PDF")

    output = Path(sys.argv[1])
    output.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir) / "source.pdf"
        for url in URLS:
            if tmp.exists():
                tmp.unlink()
            error = try_curl(url, tmp)
            if error is None:
                tmp.replace(output)
                print(
                    f"VERIFIED exact POF handbook: {output.stat().st_size} bytes, "
                    f"sha256={EXPECTED_SHA256}"
                )
                return
            errors.append(f"{url}: {error}")

    raise SystemExit("Could not obtain the exact locked POF handbook:\n" + "\n".join(errors))


if __name__ == "__main__":
    main()
