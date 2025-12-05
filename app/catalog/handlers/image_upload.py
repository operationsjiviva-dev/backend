#!/usr/bin/env python3
"""
Multithreaded Image Pipeline: Download -> Resize -> Upload to S3

Requirements:
  pip install boto3 pillow requests

Usage:
  python bulk_image_pipeline.py         --urls-file urls.txt         --bucket my-s3-bucket         --prefix uploads/resized/         --max-width 1024         --max-height 1024         --workers 32

Notes:
  - AWS credentials are read from your environment/config as per boto3 defaults.
  - urls.txt should contain one image URL per line.
  - Resizing preserves aspect ratio using PIL 'thumbnail' (no upscaling).
  - Content-Type is set based on the output image format.
"""


import concurrent.futures as cf
import hashlib
import logging
import mimetypes
import os
from io import BytesIO
from typing import Optional, Tuple

from botocore.exceptions import ClientError
from PIL import Image, ImageOps
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from common.managers.aws_client import AWSS3

# --------------- Logging -----------------
LOG_FORMAT = "%(asctime)s %(levelname)s [%(threadName)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("image-pipeline")

# --------------- HTTP Session with Retry -----------------


def build_http_session(
    total_retries: int = 2,
    backoff_factor: float = 0.5,
    pool_connections: int = 100,
    pool_maxsize: int = 100,
    timeout: int = 20,
) -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=total_retries,
        connect=total_retries,
        read=total_retries,
        status=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "HEAD"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(
        max_retries=retries, pool_connections=pool_connections, pool_maxsize=pool_maxsize)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.request_timeout = timeout  # custom attribute
    return session

# --------------- S3 Client -----------------


def build_s3_client():
    s3_client = AWSS3.get_client()
    return s3_client


# --------------- Image helpers -----------------
SUPPORTED_SAVE_FORMATS = {"JPEG", "PNG", "WEBP"}


def _choose_output_format(pil_image: Image.Image, original_ext: Optional[str]) -> Tuple[str, str]:
    """Return (pil_format, extension) for saving. Defaults to JPEG for photos."""
    ext = (original_ext or "").lower()
    if ext in {".jpg", ".jpeg"}:
        return "JPEG", ".jpg"
    if ext == ".png":
        return "PNG", ".png"
    if ext == ".webp":
        return "WEBP", ".webp"
    # If image has alpha, prefer PNG or WEBP to preserve transparency
    if pil_image.mode in ("RGBA", "LA") or (pil_image.mode == "P" and "transparency" in pil_image.info):
        return "PNG", ".png"
    return "JPEG", ".jpg"


def _content_type_for_ext(ext: str) -> str:
    if ext == ".jpg" or ext == ".jpeg":
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    # Fallback
    return mimetypes.types_map.get(ext, "application/octet-stream")


def _normalize_orientation(img: Image.Image) -> Image.Image:
    # Apply EXIF orientation if present
    try:
        return ImageOps.exif_transpose(img)
    except Exception:
        return img


def resize_bytes(
    raw: bytes,
    max_w: int,
    max_h: int,
    output_format: Optional[str] = None,
    original_ext: Optional[str] = None,
    jpeg_quality: int = 85,
) -> Tuple[bytes, str, str]:
    """Resize image bytes, preserve aspect ratio, no upscaling.
    Returns (output_bytes, pil_format, ext)
    """
    with Image.open(BytesIO(raw)) as im:
        im = _normalize_orientation(im)
        # Convert CMYK or others to RGB for JPEG/WEBP
        if im.mode not in ("RGB", "RGBA", "LA", "P"):
            im = im.convert("RGB")
        # Resize in place using thumbnail (no upscaling)
        im.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        # Decide output format
        fmt, ext = _choose_output_format(im, original_ext) if output_format is None else (
            output_format, f".{output_format.lower()}")
        out = BytesIO()
        save_kwargs = {}
        if fmt == "JPEG":
            # Drop alpha for JPEG
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGB")
            save_kwargs.update(
                dict(quality=jpeg_quality, optimize=True, progressive=True))
        elif fmt == "PNG":
            save_kwargs.update(dict(optimize=True))
        elif fmt == "WEBP":
            save_kwargs.update(dict(quality=jpeg_quality, method=6))
        im.save(out, format=fmt, **save_kwargs)
        return out.getvalue(), fmt, ext

# --------------- Download helper -----------------


def download_image(session: requests.Session, url: str) -> Tuple[bytes, Optional[str]]:
    timeout = getattr(session, "request_timeout", 20)
    r = session.get(url, timeout=timeout, stream=True)
    r.raise_for_status()
    content = r.content
    # Try to infer extension from URL
    ext = os.path.splitext(url.split("?")[0].split("#")[0])[1] or None
    return content, ext

# --------------- S3 upload -----------------


def upload_to_s3(
    s3,
    bucket: str,
    key: str,
    body: bytes,
    content_type: str,
    cache_control: Optional[str] = "public, max-age=31536000, immutable",
) -> None:
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType=content_type,
        CacheControl=cache_control,
        ACL="public-read"
    )

# --------------- Key builder -----------------


def key_for_url(prefix: str, url: str, ext: str) -> str:
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return f"{prefix.rstrip('/')}/{h}{ext}" if prefix else f"{h}{ext}"

# --------------- Worker -----------------


def process_one(
    url_row: dict,
    session: requests.Session,
    s3,
    bucket: str,
    prefix: str,
    max_w: int,
    max_h: int,
    force_format: Optional[str] = None,  # e.g., "JPEG", "PNG", "WEBP"
) -> Tuple[str, Optional[str]]:

    try:
        keys_for_images = ['image1', 'image2', 'image3', 'image4', 'image5']
        for row_index in keys_for_images:
            if image_url := url_row.get(row_index):
                if '//lovelocal' in url_row.get(row_index):
                    url_row[row_index + '_aws_url'] = image_url
                url = image_url
                raw, ext_hint = download_image(session, url)
                resized, fmt, ext = resize_bytes(
                    raw, max_w, max_h, output_format=force_format, original_ext=ext_hint)
                ctype = _content_type_for_ext(ext)
                key = key_for_url(prefix, url, ext)
                upload_to_s3(s3, bucket, key, resized, ctype)
                aws_url = 'https://{}.s3.amazonaws.com/{}'.format(bucket, key)
                url_row[row_index + '_aws_url'] = aws_url
        return url_row
    except Exception as e:
        url_row['reason'] = str(e)
        return url_row

# --------------- Orchestrator -----------------


def run_pipeline(
    urls,
    bucket: str,
    max_w: int,
    max_h: int,
    workers: int,
    prefix: Optional[str] = None,
    force_format: Optional[str] = None,
):
    session = build_http_session(
        pool_connections=workers, pool_maxsize=workers)
    s3 = build_s3_client()

    total = len(urls)
    success = 0
    failures = 0

    final_result = []
    with cf.ThreadPoolExecutor(max_workers=workers, thread_name_prefix="img") as executor:
        futures = [
            executor.submit(process_one, url_row, session, s3,
                            bucket, prefix, max_w, max_h, force_format)
            for url_row in urls
        ]
        for fut in cf.as_completed(futures):
            result = fut.result()
            final_result.append(result)
            if isinstance(result, str) and result.get("reason"):
                failures += 1
            else:
                success += 1

    logger.info("Done. Success: %d   Failures: %d   Total: %d",
                success, failures, total)
    return final_result
