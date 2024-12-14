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

    # Render template
    html_output = _render_template("template/template.html", **context)

    # Copy avatar image
    if not os.path.exists("dist/assets/img"):
        os.makedirs("dist/assets/img")
    shutil.copy("data/avatar.png", "dist/assets/img/avatar.png")

    # Output to file
    with open("dist/index.html", "w", encoding="utf-8") as file:
        file.write(html_output)
