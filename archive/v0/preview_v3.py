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
    This preview:
    - If multiple words are entered, we do separate searches for each word
    - Then union the final results
    - So if query = 'cat dog', we gather icons that match 'cat' union icons that match 'dog'
    - We highlight icons if they EXACT-match or STARTSWITH-match any of the tokens
    """

    # 1) Load data
    with open(input_icons, "r", encoding="utf-8") as f:
        data = json.load(f)

    icons = data.get("icons", [])

    # 2) Group icons by category
    categorized_icons = defaultdict(list)
    for icon in icons:
        category = icon.get("top_category", "Uncategorized")
        raw_tags = icon.get("keywords", dict()).get("en")
        # splitted_tags = [t.strip().lower() for t in raw_tags.split(",") if t.strip()]
        # joined_tags = " ".join(splitted_tags)

        categorized_icons[category].append({
            "name": icon.get("name", ""),
            "score": icon.get("score", 0.0),
            "content": icon.get("content", ""),
            "width": icon.get("width"),
            "height": icon.get("height"),
            "splitted_tags": raw_tags,  # used for EXACT or startswith
            "joined_tags": ','.join(raw_tags),      # for substring checks
        })

    # 3) Build HTML
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

    # Render each category block
    category_names = sorted(categorized_icons.keys())
    for cat_name in category_names:
        icons_in_cat = categorized_icons[cat_name]
        html_content += f'<div class="category-block" data-category-block>\n'
        html_content += f"<h2>{cat_name}</h2>"
        html_content += '<div class="icon-container">'

        for i, icon_data in enumerate(icons_in_cat):
            splitted_str = "|".join(icon_data["splitted_tags"])  # 'tag1|tag2|tag3'
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

    # Close container
    html_content += """
      </div> <!-- container -->

      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
      <script>
      document.addEventListener("DOMContentLoaded", function() {
          // Enable popovers
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

          function doFilter(rawQuery) {
              // Split user input by whitespace, filter out tokens < 3 chars
              let tokens = rawQuery.split(/\\s+/).map(t => t.trim()).filter(t => t.length >= 3);
              let hasTokens = tokens.length > 0;

              // For each category block:
              categoriesData.forEach(({ block, container, icons }) => {
                  if(!hasTokens) {
                      // Show all icons in original order if no valid tokens
                      container.innerHTML = '';
                      icons.sort((a,b) => parseInt(a.dataset.originalIndex) - parseInt(b.dataset.originalIndex));
                      icons.forEach(ic => {
                          ic.classList.remove('exact-match','startswith-match');
                          ic.style.display = 'block';
                          container.appendChild(ic);
                      });
                      block.style.display = 'block';
                      return;
                  }

                  // We'll do a union approach for icons:
                  // Step1: For each token, gather icons that match that token => union set
                  // We'll store references in a big set
                  let matchedIconsSet = new Set();

                  tokens.forEach(token => {
                      // We'll do a pass for this token
                      icons.forEach(icon => {
                          const splitted = icon.dataset.splittedTags.split('|');
                          const joined = icon.dataset.joinedTags;
                          // if joined includes token => match
                          if(joined.includes(token)) {
                              matchedIconsSet.add(icon);
                          }
                      });
                  });

                  // Now we have a set of icons that matched ANY token
                  // We'll highlight them based on EXACT or STARTSWITH for each token
                  // if an icon EXACT matches any token => EXACT
                  // else if an icon STARTSWITH matches any token => STARTSWITH
                  // else partial
                  let exactMatches = [];
                  let startsWithMatches = [];
                  let partialMatches = [];

                  // We'll hide all icons first
                  icons.forEach(ic => ic.style.display = 'none');

                  matchedIconsSet.forEach(icon => {
                      icon.classList.remove('exact-match','startswith-match');
                      // We see if it EXACT matches or STARTSWITH for ANY token
                      let splitted = icon.dataset.splittedTags.split('|');
                      // We'll track booleans
                      let foundExact = false;
                      let foundStart = false;

                      for(let token of tokens) {
                          // if splitted includes token => EXACT
                          for(let st of splitted) {
                              if(st === token) {
                                  foundExact = true;
                                  break;
                              }
                              if(!foundExact && st.startsWith(token)) {
                                  foundStart = true; 
                                  // we won't break here, in case we find exact in another splitted
                              }
                          }
                          if(foundExact) break;
                      }

                      if(foundExact) {
                          icon.classList.add('exact-match');
                          exactMatches.push(icon);
                      } else if(foundStart) {
                          icon.classList.add('startswith-match');
                          startsWithMatches.push(icon);
                      } else {
                          partialMatches.push(icon);
                      }
                  });

                  // reorder
                  container.innerHTML = '';
                  exactMatches.forEach(ic => {
                      ic.style.display = 'block';
                      container.appendChild(ic);
                  });
                  startsWithMatches.forEach(ic => {
                      ic.style.display = 'block';
                      container.appendChild(ic);
                  });
                  partialMatches.forEach(ic => {
                      ic.style.display = 'block';
                      container.appendChild(ic);
                  });

                  // If no icons => hide block
                  const visibleIcons = exactMatches.length + startsWithMatches.length + partialMatches.length;
                  block.style.display = visibleIcons ? 'block' : 'none';
              });
          }

          let debounceTimer = null;
          searchInput.addEventListener('input', function(e) {
              const raw = e.target.value.toLowerCase();
              if(debounceTimer) clearTimeout(debounceTimer);
              debounceTimer = setTimeout(() => {
                  doFilter(raw);
              }, 300);
          });

          // initial
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
