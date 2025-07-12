import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate paper page for website.")
    parser.add_argument("paper_path", help="Path to the paper directory")
    parser.add_argument("--url", default="https://syntavioninstitute.org", help="Base URL for the site")

    args = parser.parse_args()
    paper_path = args.paper_path
    site_url = args.url

    print(f"📄 Generating paper page from {paper_path}")
    print(f"🌐 Base URL: {site_url}")

    # Dummy example: generate simple index.html (replace with your logic)
    os.makedirs("_site", exist_ok=True)
    html_path = os.path.join("_site", "index.html")
    with open(html_path, "w") as f:
        f.write(f"""<html>
  <head><title>Paper</title></head>
  <body>
    <h1>Paper at: {paper_path}</h1>
    <p>Published on: <a href="{site_url}">{site_url}</a></p>
  </body>
</html>
""")
    print(f"✅ Generated {html_path}")

    # ✅ Write CNAME
    cname_path = os.path.join("_site", "CNAME")
    with open(cname_path, "w") as cname_file:
        cname_file.write("syntavioninstitute.org\n")
    print(f"✅ Generated {cname_path}")

if __name__ == "__main__":
    main()
