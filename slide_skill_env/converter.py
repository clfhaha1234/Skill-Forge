"""Convert .pptx → .pdf → .jpg using LibreOffice and poppler."""

import subprocess
from pathlib import Path


def pptx_to_jpg(pptx_path: Path, output_dir: Path) -> Path:
    """Convert a .pptx file to a JPEG image of the first slide.

    Args:
        pptx_path: Path to the .pptx file.
        output_dir: Directory to write intermediate and final files.

    Returns:
        Path to the rendered JPEG image.

    Raises:
        RuntimeError: If conversion fails at any step.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / pptx_path.with_suffix(".pdf").name

    # Step 1: pptx → pdf via LibreOffice
    result = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_dir),
            str(pptx_path),
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(
            f"LibreOffice conversion failed: {result.stderr}"
        )

    # Step 2: pdf → jpg via pdftoppm (first page only)
    jpg_prefix = output_dir / "slide"
    result = subprocess.run(
        [
            "pdftoppm",
            "-jpeg", "-r", "150",
            "-f", "1", "-l", "1",
            str(pdf_path),
            str(jpg_prefix),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm conversion failed: {result.stderr}")

    # pdftoppm outputs slide-1.jpg or slide-01.jpg
    candidates = list(output_dir.glob("slide-*.jpg"))
    if not candidates:
        raise RuntimeError("No JPEG output found from pdftoppm")
    return candidates[0]
