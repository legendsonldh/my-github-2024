import shutil
import os

from template.context import get_context


def _render_template(template_path, **kwargs):
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    html_content = template.format(**kwargs)
    return html_content


def generate_site(year: int):
    context = get_context(year)

    html_output = _render_template("template/template.html", **context)

    return context["AVATAR"], html_output
