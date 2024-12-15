from generator.context import get_context


def _render_template(template_path, **kwargs):
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    html_content = template.format(**kwargs)
    return html_content


def generate_site(year: int, result: dict, result_new_repo: dict) -> tuple:
    context = get_context(year, result, result_new_repo)

    html_output = _render_template("templates/template.html", **context)

    return context["AVATAR"], html_output
