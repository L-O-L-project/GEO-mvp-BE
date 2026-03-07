from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from app.services.geo_audit import run_geo_audit

router = APIRouter()
GEO_TEST_PAGE_PATH = Path(__file__).resolve().parent.parent.joinpath("static", "geo-test.html")


def _error_detail(category: str, code: str, user_message: str, debug_detail: Any = None) -> Dict[str, Any]:
    return {
        "ok": False,
        "errorCategory": category,
        "errorCode": code,
        "userMessage": user_message,
        "debugDetail": debug_detail,
    }


async def _json_payload(req: Request) -> Dict[str, Any]:
    try:
        data = await req.json()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=_error_detail("config", "INVALID_JSON", "요청 본문(JSON) 형식이 올바르지 않습니다.", str(e)),
        ) from e
    if not isinstance(data, dict):
        raise HTTPException(
            status_code=400,
            detail=_error_detail("config", "JSON_OBJECT_REQUIRED", "JSON 객체 형태의 본문이 필요합니다."),
        )
    return data


@router.get("/geo-test")
async def geo_test_page() -> FileResponse:
    if not GEO_TEST_PAGE_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail=_error_detail("server", "GEO_TEST_PAGE_MISSING", "geo-test page is missing", str(GEO_TEST_PAGE_PATH)),
        )
    return FileResponse(GEO_TEST_PAGE_PATH)


@router.post("/api/geo-audit")
async def geo_audit(req: Request) -> Dict[str, Any]:
    payload = await _json_payload(req)
    url = str(payload.get("url") or "").strip()
    if not url:
        raise HTTPException(
            status_code=400,
            detail=_error_detail("config", "URL_REQUIRED", "url is required"),
        )

    try:
        return await run_geo_audit(url)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=_error_detail("config", "INVALID_URL", "invalid url", str(e)),
        ) from e
    except RuntimeError as e:
        raise HTTPException(
            status_code=502,
            detail=_error_detail("dependency", "GEO_CRAWL_FAILED", "failed to crawl target url", str(e)),
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=_error_detail("server", "GEO_AUDIT_FAILED", "geo audit failed", str(e)),
        ) from e
