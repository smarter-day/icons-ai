#!.venv/bin/python
import json
import webbrowser
from collections import defaultdict
from pathlib import Path

import dotenv
import typer

dotenv.load_dotenv()
app = typer.Typer()


@app.command()
def preview(
        input_icons: str = typer.Option(..., help="Path to the filtered icons JSON file"),
        output_html: str = typer.Option("preview.html", help="Path to save the generated HTML file"),
):
    """
    Preview SVG icons grouped by their categories and display their keywords for each language.
    Generates an HTML file and opens it using the default web browser.
    """
    with open(input_icons, "r", encoding="utf-8") as f:
        data = json.load(f)

    icons = data.get("icons", [])

    # Group icons by categories
    categorized_icons = defaultdict(list)
    for icon in icons:
        for category, keywords in icon.get("categories", {}).items():
            categorized_icons[category].append({
                "name": icon["name"],
                "score": icon["score"],
                "content": icon["content"],
                "width": icon["width"],
                "height": icon["height"],
                "keywords": icon.get("keywords", {})
            })

    # Generate HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SVG Icons Preview</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css">
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f9; }
            h1 { text-align: center; }
            h2 { margin-top: 40px; border-bottom: 2px solid #ccc; padding-bottom: 10px; }
            .icon-container { display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 40px; }
            .icon { text-align: center; width: 200px; }
            .icon svg { display: block; margin: 0 auto; width: 20px; height: 20px; }
            .icon-name { margin-top: 10px; font-size: 14px; font-weight: bold; color: #007bff; cursor: pointer; }
            .icon-name:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>SVG Icons Preview (""" + str(len(icons)) + """)</h1>
        <div class="container">
    """

    for category, icons in categorized_icons.items():
        html_content += f"<h2>{category}</h2>"
        html_content += '<div class="icon-container">'
        for icon in icons:
            # Prepare popover content
            popover_content = ""
            for lang, keywords in icon["keywords"].items():
                popover_content += f"<strong>{lang.upper()}:</strong> " \
                                   f"{', '.join(keywords)}<br>"

            html_content += f"""
            <div class="icon">
                {icon["content"]}
                <div class="icon-name" tabindex="0" data-bs-toggle="popover" data-bs-html="true"
                     data-bs-content="{popover_content}">
                     {icon["name"]} <small><pre>{icon["score"]}</pre></small>
                </div>
            </div>
            """
        html_content += "</div>"

    html_content += """
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function () {
            const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
            const popoverList = [...popoverTriggerList].map(el => new bootstrap.Popover(el, { container: 'body' }));

            // Close popovers when clicking outside
            document.addEventListener('click', function (event) {
                popoverList.forEach(popover => {
                    const popoverElement = popover._element;
                    if (!popoverElement.contains(event.target) && popoverElement !== event.target) {
                        popover.hide();
                    }
                });
            });
        });
        </script>
    </body>
    </html>
    """

    # Write HTML to file
    output_path = Path(output_html)
    output_path.write_text(html_content, encoding="utf-8")

    # Open the HTML file in the default web browser
    typer.echo(f"Opening preview: {output_path.absolute()}")
    webbrowser.open(output_path.absolute().as_uri())




if __name__ == "__main__":
    app()
