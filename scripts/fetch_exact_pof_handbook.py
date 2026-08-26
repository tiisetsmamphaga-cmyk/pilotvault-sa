from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

EXACT_FULL_PDF_SHA256 = "89aca5abff3b3c14aca5d8865e8583994bff611bc0c4de94ec1c8a7ef7aaeed3"

# url, require exact 191-page PDF hash, allow insecure TLS transport
SOURCES = [
    ("https://air.flyingway.com/books/ac_61-23c_phak_canada.pdf", True, False),
    ("http://air.flyingway.com/books/ac_61-23c_phak_canada.pdf", True, False),
    ("https://www.mlettini.com/princilpes%20of%20flight.pdf", False, True),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(url: str, destination: Path, allow_insecure_tls: bool = False) -> str | None:
    command = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--retry", "3", "--retry-delay", "2", "--http1.1",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36",
        "--header", "Accept: application/pdf,application/octet-stream;q=0.9,*/*;q=0.8",
    ]
    if allow_insecure_tls:
        command.append("--insecure")
    command.extend(["--output", str(destination), url])

    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return f"curl exit {result.returncode}: {result.stderr.strip()}"
    if not destination.exists() or destination.stat().st_size < 100_000:
        return "download did not produce a plausible PDF"
    if not destination.read_bytes().startswith(b"%PDF"):
        return "download is not a PDF"
    return None


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: fetch_exact_pof_handbook.py OUTPUT_PDF")

    output = Path(sys.argv[1])
    output.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir) / "source.pdf"
        for url, require_exact_full_hash, allow_insecure_tls in SOURCES:
            if tmp.exists():
                tmp.unlink()
            error = download(url, tmp, allow_insecure_tls)
            if error:
                errors.append(f"{url}: {error}")
                continue

            actual = sha256(tmp)
            if require_exact_full_hash and actual != EXACT_FULL_PDF_SHA256:
                errors.append(f"{url}: SHA mismatch ({actual}, {tmp.stat().st_size} bytes)")
                continue

            tmp.replace(output)
            if actual == EXACT_FULL_PDF_SHA256:
                print(f"VERIFIED exact uploaded-document bytes: {output.stat().st_size} bytes, sha256={actual}")
            else:
                print(
                    "Using Reilly Burke Chapter 1 mirror as transport only: "
                    f"{output.stat().st_size} bytes, sha256={actual}. "
                    "The builder must reproduce every output hash generated from the uploaded PDF or fail."
                )
            return

    raise SystemExit("Could not obtain a permitted POF source:\n" + "\n".join(errors))


if __name__ == "__main__":
    main()
