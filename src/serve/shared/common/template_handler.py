from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape, environment

TEMPLATE_DIRECTORY = Path(__file__).resolve().parents[3] / "templates"
environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIRECTORY),
    autoescape=select_autoescape(["html", "xml"]),
)

def render_template(
        template_name: str,
        **context: object,
) -> str:
    template = environment.get_template(template_name)
    return template.render(**context)