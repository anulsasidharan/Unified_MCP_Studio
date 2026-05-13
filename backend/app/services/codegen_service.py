"""Render MCP server bundles from project rows (Phase 4 — TASKS.md)."""

from __future__ import annotations

import io
import re
import shutil
import uuid
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.project import Project
from app.services import project_service


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_]+", "_", text.strip()).strip("_")
    if not s:
        s = "project"
    if s[0].isdigit():
        s = f"p_{s}"
    return s.lower()


def _template_root() -> Path:
    if settings.codegen_template_root:
        return Path(settings.codegen_template_root).resolve()
    return Path(__file__).resolve().parents[3] / "templates"


def _jinja_env(subdir: str) -> Environment:
    root = _template_root() / subdir
    return Environment(
        loader=FileSystemLoader(str(root)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _write_python_bundle(project: Project, dest_dir: Path) -> None:
    env = _jinja_env("python")
    slug_name = _slug(project.name)
    ctx_project = {
        "name": project.name,
        "slug": slug_name,
    }
    (dest_dir / "src" / "generated_mcp").mkdir(parents=True, exist_ok=True)
    (dest_dir / "src" / "generated_mcp" / "tools").mkdir(parents=True, exist_ok=True)

    def render(name: str, out: Path, **extra: Any) -> None:
        tpl = env.get_template(name)
        out.write_text(tpl.render(project=ctx_project, **extra), encoding="utf-8")

    render("pyproject.toml.j2", dest_dir / "pyproject.toml", project_slug=slug_name)
    render("README.md.j2", dest_dir / "README.md")
    render("studio_execute.py.j2", dest_dir / "studio_execute.py")

    tool_tpl = env.get_template("src/generated_mcp/tools/tool.py.j2")
    for tool in project.tools:
        mod = _slug(tool.name)
        body = tool_tpl.render(
            tool={
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.input_schema,
                "handler_code": tool.handler_code,
            },
        )
        (dest_dir / "src" / "generated_mcp" / "tools" / f"{mod}.py").write_text(
            body,
            encoding="utf-8",
        )

    # static package initializers (also in repo templates for packaging)
    init_pkg = _template_root() / "python" / "src" / "generated_mcp" / "__init__.py"
    init_tools = _template_root() / "python" / "src" / "generated_mcp" / "tools" / "__init__.py"
    if init_pkg.is_file():
        (dest_dir / "src" / "generated_mcp" / "__init__.py").write_bytes(init_pkg.read_bytes())
    if init_tools.is_file():
        (dest_dir / "src" / "generated_mcp" / "tools" / "__init__.py").write_bytes(
            init_tools.read_bytes(),
        )


def _write_typescript_stub(project: Project, dest_dir: Path) -> None:
    env = _jinja_env("typescript")
    slug_name = _slug(project.name)
    (dest_dir / "src").mkdir(parents=True, exist_ok=True)
    tpl = env.get_template("package.json.j2")
    (dest_dir / "package.json").write_text(
        tpl.render(project_name=project.name, package_slug=slug_name),
        encoding="utf-8",
    )
    tscfg = env.get_template("tsconfig.json.j2")
    (dest_dir / "tsconfig.json").write_text(tscfg.render(), encoding="utf-8")
    readme = env.get_template("README.md.j2")
    (dest_dir / "README.md").write_text(readme.render(project=project), encoding="utf-8")
    index = env.get_template("src/index.ts.j2")
    (dest_dir / "src" / "index.ts").write_text(
        index.render(project=project, tools=project.tools),
        encoding="utf-8",
    )


def zip_directory(src_dir: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in src_dir.rglob("*"):
            if path.is_file():
                arc = path.relative_to(src_dir).as_posix()
                zf.write(path, arcname=arc)
    return buf.getvalue()


async def materialize_project_tree(db: AsyncSession, project_id: uuid.UUID) -> tuple[Project, Path]:
    project = await project_service.get_project_with_children(db, project_id)
    if project is None:
        raise ValueError("project not found")
    root = Path(settings.sandbox_workspace_root).resolve() / "trees" / str(project.id)
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    dest = root / "bundle"
    dest.mkdir(parents=True, exist_ok=True)
    if project.runtime == "python":
        _write_python_bundle(project, dest)
    elif project.runtime == "typescript":
        _write_typescript_stub(project, dest)
    else:
        raise ValueError("unsupported runtime")
    return project, dest


async def write_zip_artifact(db: AsyncSession, project_id: uuid.UUID) -> dict[str, Any]:
    project, tree_dir = await materialize_project_tree(db, project_id)
    data = zip_directory(tree_dir)
    out_dir = Path(settings.artifact_local_dir).resolve() / str(project.id)
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_name = f"{uuid.uuid4().hex}.zip"
    out_path = out_dir / zip_name
    out_path.write_bytes(data)
    meta = {
        "path": str(out_path),
        "filename": zip_name,
        "generated_at": datetime.now(UTC).isoformat(),
        "runtime": project.runtime,
        "bytes": len(data),
    }
    cfg = dict(project.config or {})
    cfg["artifact"] = meta
    project.config = cfg
    await db.commit()
    await db.refresh(project)
    return meta
