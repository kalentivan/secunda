"""
Роуты для получения логов
"""
import shutil
import tempfile
from pathlib3x import Path
from typing import Literal

from fastapi import APIRouter, BackgroundTasks
from starlette.responses import FileResponse, Response

from ..core.config import settings

router = APIRouter(prefix='/debug/log', tags=['Отладка'])


@router.get("/archive/")
def route_get_logs_archive(response: Response,
                           background: BackgroundTasks) -> FileResponse:
    tmp_dir = tempfile.gettempdir()
    archive_path = Path(tmp_dir) / "logs_archive.zip"
    shutil.make_archive(base_name=str(archive_path.with_suffix("")),
                        format="zip",
                        root_dir=f"{settings.LOG_PATH}")

    def cleanup():
        try:
            archive_path.unlink()
        except Exception:
            pass

    background.add_task(cleanup)

    response.status_code = 200
    return FileResponse(
        path=str(archive_path),
        filename="logs_archive.zip",
        media_type='application/zip',
        background=background
    )


@router.get("/{name}/")
def route_get_log_api(response: Response,
                      name: Literal["error", "fastapi", "warnings", "info", "debug"]) -> FileResponse:
    """Получить файл лога с warning"""
    response.status_code = 200
    return FileResponse(
        path=f"{settings.LOG_PATH}/{name}.log",
        filename=f"{name}.log",
        media_type='multipart/form-data'
    )
