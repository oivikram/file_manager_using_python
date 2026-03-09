from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI(title="File Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FileCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    content: str


class FileAppendRequest(BaseModel):
    content: str


def resolve_data_path(relative_name: str) -> Path:
    candidate = (DATA_DIR / relative_name).resolve()
    data_root = DATA_DIR.resolve()

    try:
        candidate.relative_to(data_root)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid path") from exc

    if candidate == data_root:
        raise HTTPException(status_code=400, detail="File name is required")

    return candidate


def ensure_regular_file(path: Path) -> None:
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    if not path.is_file():
        raise HTTPException(status_code=400, detail="Path must point to a file")


@app.get("/api/items")
def list_items() -> dict[str, list[dict[str, str]]]:
    items: list[dict[str, str]] = []

    for item in sorted(DATA_DIR.rglob("*")):
        item_type = "dir" if item.is_dir() else "file"
        items.append(
            {
                "path": item.relative_to(DATA_DIR).as_posix(),
                "type": item_type,
            }
        )

    return {"items": items}


@app.post("/api/files", status_code=201)
def create_file(payload: FileCreateRequest) -> dict[str, str]:
    file_path = resolve_data_path(payload.name)

    if file_path.exists():
        raise HTTPException(status_code=409, detail="File already exists")

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(payload.content, encoding="utf-8")
    return {"message": "File created successfully", "name": payload.name}


@app.get("/api/files/{name:path}")
def read_file(name: str) -> dict[str, str]:
    file_path = resolve_data_path(name)
    ensure_regular_file(file_path)

    return {
        "name": name,
        "content": file_path.read_text(encoding="utf-8"),
    }


@app.post("/api/files/{name:path}/append")
def append_file(name: str, payload: FileAppendRequest) -> dict[str, str]:
    file_path = resolve_data_path(name)
    ensure_regular_file(file_path)

    with file_path.open("a", encoding="utf-8") as handle:
        handle.write("\n" + payload.content)

    return {"message": "File updated successfully", "name": name}


@app.delete("/api/files/{name:path}")
def delete_file(name: str) -> dict[str, str]:
    file_path = resolve_data_path(name)
    ensure_regular_file(file_path)
    file_path.unlink()

    return {"message": "File deleted successfully", "name": name}
