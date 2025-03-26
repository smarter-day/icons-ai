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
    with open(input_icons, "r", encoding="utf-8") as f:
        data = json.load(f)

    icons = data.get("icons", [])

    categorized_icons = defaultdict(list)
    for icon in icons:
        category = icon.get("top_category", "Uncategorized")
        raw_tags = icon.get("tags", "")
        splitted_tags = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]
        joined_tags = " ".join(splitted_tags)

        categorized_icons[category].append({
            "name": icon.get("name", ""),
            "score": icon.get("score", 0.0),
            "content": icon.get("content", ""),
            "width": icon.get("width"),
            "height": icon.get("height"),
            "splitted_tags": splitted_tags,
            "joined_tags": joined_tags,
        })

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>SVG Icons Preview</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" />
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f4f4f9;
            }}
            h1 {{
                text-align: center;
            }}
            h2 {{
                margin-top: 40px;
                border-bottom: 2px solid #ccc;
                padding-bottom: 10px;
            }}
            .icon-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 40px;
            }}
            .icon {{
                text-align: center;
                width: 200px;
                transition: all 0.2s ease-in-out;
            }}
            .icon svg {{
                display: block;
                margin: 0 auto;
                width: 20px;
                height: 20px;
            }}
            .icon-name {{
                margin-top: 10px;
                font-size: 14px;
                font-weight: bold;
                color: #007bff;
                cursor: pointer;
            }}
            .icon-name:hover {{
                text-decoration: underline;
            }}
            .icon.exact-match {{
                background-color: #d4edda; 
                border: 2px dashed #28a745; 
                padding: 5px;
                border-radius: 5px;
            }}
            .icon.startswith-match {{
                background-color: #fff3cd; 
                border: 2px dashed #ffc107; 
                padding: 5px;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>SVG Icons Preview ({sum(len(lst) for lst in categorized_icons.values())})</h1>

        <div style="text-align:center; margin-bottom:20px;">
            <input
              type="search"
              id="searchInput"
              placeholder="Type 3+ chars to search (by tags)..."
              style="width:50%; padding:5px; font-size:16px;"
            />
        </div>

        <div class="container">
    """

    category_names = sorted(categorized_icons.keys())
    for cat_idx, cat_name in enumerate(category_names):
        icons_in_cat = categorized_icons[cat_name]

        html_content += f'<div class="category-block" data-category-block>\n'
        html_content += f"<h2>{cat_name}</h2>"
        html_content += '<div class="icon-container">'

        for i, icon_data in enumerate(icons_in_cat):
            splitted_str = "|".join(icon_data["splitted_tags"])
            joined_str = icon_data["joined_tags"]
            popover_content = f"Tags: {', '.join(icon_data['splitted_tags'])}"

            html_content += f"""
            <div class="icon"
                 data-original-index="{i}"
                 data-splitted-tags="{splitted_str}"
                 data-joined-tags="{joined_str}">
                {icon_data["content"]}
                <div class="icon-name" tabindex="0"
                     data-bs-toggle="popover"
                     data-bs-html="true"
                     data-bs-content="{popover_content}">
                    {icon_data["name"]} <small><pre>{icon_data["score"]}</pre></small>
                </div>
            </div>
            """

        html_content += "</div> <!-- icon-container -->"
        html_content += "</div> <!-- category-block -->"

    html_content += """
        </div> <!-- container -->

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
            const popoverList = [...popoverTriggerList].map(
                el => new bootstrap.Popover(el, { container: 'body' })
            );

            document.addEventListener('click', function (event) {
                popoverList.forEach(popover => {
                    const popoverElement = popover._element;
                    if (!popoverElement.contains(event.target) && popoverElement !== event.target) {
                        popover.hide();
                    }
                });
            });

            const searchInput = document.getElementById('searchInput');
            const categoryBlocks = document.querySelectorAll('[data-category-block]');
            const categoriesData = [];

            categoryBlocks.forEach(block => {
                const container = block.querySelector('.icon-container');
                const icons = Array.from(container.querySelectorAll('.icon'));
                categoriesData.push({ block, container, icons });
            });

            function doFilter(query) {
                if (query.length < 3) {
                    categoriesData.forEach(({ block, container, icons }) => {
                        container.innerHTML = '';
                        icons.sort((a,b) => parseInt(a.dataset.originalIndex) - parseInt(b.dataset.originalIndex));
                        icons.forEach(icon => {
                            icon.style.display = 'block';
                            icon.classList.remove('exact-match', 'startswith-match');
                            container.appendChild(icon);
                        });
                        block.style.display = 'block';
                    });
                    return;
                }

                categoriesData.forEach(({ block, container, icons }) => {
                    let exactMatches = [];
                    let startsWithMatches = [];
                    let partialMatches = [];

                    icons.forEach(icon => {
                        icon.classList.remove('exact-match', 'startswith-match');
                        const splitted = icon.dataset.splittedTags.split('|');
                        const joined = icon.dataset.joinedTags;

                        if (!joined.includes(query)) return;

                        let isExact = false;
                        let isStartsWith = false;
                        for (let t of splitted) {
                            if (t === query) {
                                isExact = true;
                                break;
                            }
                            if (t.startsWith(query)) {
                                isStartsWith = true;
                            }
                        }

                        if (isExact) {
                            icon.classList.add('exact-match');
                            exactMatches.push(icon);
                        } else if (isStartsWith) {
                            icon.classList.add('startswith-match');
                            startsWithMatches.push(icon);
                        } else {
                            partialMatches.push(icon);
                        }
                    });

                    container.innerHTML = '';
                    [...exactMatches, ...startsWithMatches, ...partialMatches].forEach(ic => {
                        ic.style.display = 'block';
                        container.appendChild(ic);
                    });

                    block.style.display = (exactMatches.length + startsWithMatches.length + partialMatches.length) 
                                          ? 'block' 
                                          : 'none';
                });
            }

            let debounceTimer;
            searchInput.addEventListener('input', function(e) {
                const query = e.target.value.toLowerCase().trim();
                if (debounceTimer) clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    doFilter(query);
                }, 300);
            });

            doFilter('');
        });
        </script>
    </body>
    </html>
    """

    output_path = Path(output_html)
    output_path.write_text(html_content, encoding="utf-8")

    typer.echo(f"Opening preview: {output_path.absolute()}")
    webbrowser.open(output_path.absolute().as_uri())


if __name__ == "__main__":
    app()
