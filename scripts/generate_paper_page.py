# ============ scripts/generate_paper_page.py ============
#!/usr/bin/env python3

import sys
import yaml
import markdown
from pathlib import Path

def generate_paper_page(paper_dir):
    """Generate individual paper page"""
    paper_path = Path(paper_dir)
    
    try:
        # Load metadata
        with open(paper_path / 'metadata.yml') as f:
            metadata = yaml.safe_load(f)
        
        # Load markdown content
        with open(paper_path / 'paper.md') as f:
            content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            content, 
            extensions=['extra', 'codehilite', 'toc']
        )
        
        # Generate paper page HTML
        html = generate_paper_html(metadata, html_content)
        
        # Write paper page
        output_file = paper_path / 'index.html'
        with open(output_file, 'w') as f:
            f.write(html)
        
        print(f"✅ Generated paper page: {output_file}")
        
    except Exception as e:
        print(f"❌ Error generating paper page: {e}")
        raise

def generate_paper_html(metadata, content):
    """Generate HTML for paper page"""
    
    authors_html = ""
    for author in metadata.get('authors', []):
        orcid_link = ""
        if author.get('orcid'):
            orcid_link = f' <a href="https://orcid.org/{author["orcid"]}" target="_blank">🔗</a>'
        
        authors_html += f"""
        <div class="author">
            <strong>{author['name']}</strong>{orcid_link}<br>
            <em>{author['affiliation']}</em><br>
            <a href="mailto:{author['email']}">{author['email']}</a>
        </div>
        """
    
    keywords_html = ", ".join(metadata.get('keywords', []))
    
    doi_html = ""
    if metadata.get('doi'):
        doi_html = f'<p><strong>DOI:</strong> <a href="https://doi.org/{metadata["doi"]}" target="_blank">{metadata["doi"]}</a></p>'
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']} - Syntavion Journal</title>
    <link rel="stylesheet" href="../../../style.css">
    <style>
        .paper-header {{
            background: white;
            padding: 3rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .paper-title {{
            color: #1e3a8a;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }}
        .authors {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        .author {{
            padding: 1rem;
            background: #f8fafc;
            border-radius: 8px;
        }}
        .paper-content {{
            background: white;
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .paper-meta {{
            background: #1e3a8a;
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                        <g stroke="#1e3a8a" stroke-width="8" fill="none">
                            <circle cx="100" cy="100" r="12" fill="#1e3a8a"/>
                            <ellipse cx="100" cy="100" rx="60" ry="25" transform="rotate(0 100 100)"/>
                            <ellipse cx="100" cy="100" rx="60" ry="25" transform="rotate(60 100 100)"/>
                            <ellipse cx="100" cy="100" rx="60" ry="25" transform="rotate(120 100 100)"/>
                        </g>
                    </svg>
                </div>
                <h1>SYNTAVION JOURNAL</h1>
                <p>Open Access Scientific Publishing for All Sciences</p>
            </div>
        </div>
    </header>

    <nav>
        <div class="container">
            <div class="nav-links">
                <a href="../../../index.html">Home</a>
                <a href="../../../about.html">About</a>
                <a href="../../../submit.html">Submit</a>
                <a href="../../../archives.html">Archives</a>
                <a href="../../../editorial-board.html">Editorial Board</a>
                <a href="../../../contact.html">Contact</a>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <div class="paper-header">
                <h1 class="paper-title">{metadata['title']}</h1>
                
                <div class="authors">
                    {authors_html}
                </div>
                
                <div class="paper-meta">
                    {doi_html}
                    <p><strong>Published:</strong> {metadata.get('publication_date', 'Unknown')}</p>
                    <p><strong>Keywords:</strong> {keywords_html}</p>
                    <p><strong>Field:</strong> {metadata.get('field', 'General')}</p>
                    <p><strong>License:</strong> CC BY 4.0</p>
                </div>
            </div>

            <div class="paper-content">
                {content}
            </div>

            <div style="text-align: center; margin: 2rem 0;">
                <a href="paper.pdf" class="cta-button" target="_blank">📄 Download PDF</a>
                <a href="../../../archives.html" class="cta-button">← Back to Archives</a>
            </div>
        </div>
    </main>

    <footer>
        <div class="container">
            <div style="text-align: center; padding: 2rem; color: white;">
                <p>&copy; 2025 Syntavion Journal. All rights reserved. | Open Access | CC BY 4.0 License</p>
            </div>
        </div>
    </footer>
</body>
</html>"""

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_paper_page.py <paper_directory>")
        sys.exit(1)
    
    paper_dir = sys.argv[1]
    generate_paper_page(paper_dir)

if __name__ == "__main__":
    main()
