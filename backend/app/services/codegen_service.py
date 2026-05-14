"""Code generation service — renders Jinja2 templates into a dict of {filepath: content}."""

import io
import json
import zipfile
from pathlib import Path
from uuid import UUID

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.prompt import Prompt
from app.models.resource import Resource
from app.models.tool import Tool

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "templates"


def _tojson_filter(value: object, indent: int = 2) -> str:
    return json.dumps(value, ensure_ascii=False, indent=indent)


def _topython_filter(value: object) -> str:
    """Render a Python object as a valid Python literal (dict/list/str/bool/None)."""
    import pprint
    return pprint.pformat(value, indent=2, sort_dicts=False)


def _make_env(runtime: str) -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR / runtime)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=select_autoescape([]),
    )
    env.filters["tojson"] = _tojson_filter
    env.filters["topython"] = _topython_filter
    return env


async def _load_project_data(
    db: AsyncSession,
    project_id: UUID,
    user_id: UUID,
) -> tuple[Project | None, list[Tool], list[Resource], list[Prompt]]:
    proj_result = await db.execute(
        select(Project).where(Project.id == project_id, Project.user_id == user_id)
    )
    project = proj_result.scalar_one_or_none()
    if project is None:
        return None, [], [], []

    tools = list(
        (await db.execute(select(Tool).where(Tool.project_id == project_id).order_by(Tool.created_at)))
        .scalars()
        .all()
    )
    resources = list(
        (await db.execute(select(Resource).where(Resource.project_id == project_id).order_by(Resource.created_at)))
        .scalars()
        .all()
    )
    prompts = list(
        (await db.execute(select(Prompt).where(Prompt.project_id == project_id).order_by(Prompt.created_at)))
        .scalars()
        .all()
    )
    return project, tools, resources, prompts


def _render_python(
    project: Project,
    tools: list[Tool],
    resources: list[Resource],
    prompts: list[Prompt],
) -> dict[str, str]:
    env = _make_env("python")
    ctx = {"project": project, "tools": tools, "resources": resources, "prompts": prompts}

    files: dict[str, str] = {
        "main.py": env.get_template("main.py.j2").render(**ctx),
        "pyproject.toml": env.get_template("pyproject.toml.j2").render(**ctx),
        "README.md": env.get_template("README.md.j2").render(**ctx),
        "tools/__init__.py": "",
    }
    tool_tmpl = env.get_template("tool.py.j2")
    for tool in tools:
        files[f"tools/{tool.name}.py"] = tool_tmpl.render(tool=tool)

    return files


def _render_typescript(
    project: Project,
    tools: list[Tool],
    resources: list[Resource],
    prompts: list[Prompt],
) -> dict[str, str]:
    env = _make_env("typescript")
    ctx = {"project": project, "tools": tools, "resources": resources, "prompts": prompts}

    files: dict[str, str] = {
        "src/index.ts": env.get_template("index.ts.j2").render(**ctx),
        "package.json": env.get_template("package.json.j2").render(**ctx),
        "tsconfig.json": env.get_template("tsconfig.json.j2").render(**ctx),
        "README.md": env.get_template("README.md.j2").render(**ctx),
    }
    tool_tmpl = env.get_template("tool.ts.j2")
    for tool in tools:
        files[f"src/tools/{tool.name}.ts"] = tool_tmpl.render(tool=tool)

    return files


async def generate_project_files(
    db: AsyncSession,
    project_id: UUID,
    user_id: UUID,
) -> tuple[dict[str, str] | None, Project | None]:
    project, tools, resources, prompts = await _load_project_data(db, project_id, user_id)
    if project is None:
        return None, None

    if project.runtime == "typescript":
        files = _render_typescript(project, tools, resources, prompts)
    else:
        files = _render_python(project, tools, resources, prompts)

    return files, project


def make_zip(files: dict[str, str]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path, content in sorted(files.items()):
            zf.writestr(path, content)
    return buf.getvalue()
