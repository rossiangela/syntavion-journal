#!/usr/bin/env python3

import os
import sys
import yaml
import json
from pathlib import Path
from datetime import datetime

def generate_paper_page(paper_dir):
    """Generate HTML page for a paper"""
    paper_path = Path(paper_dir)
    
    print(f"📄 Generating paper page for {paper_path.name}...")
    
    # Read metadata
    metadata_file = paper_path / 'metadata.yml'
    if not metadata_file.exists():
        print(f"❌ metadata.yml not found in {paper_path}")
        return False
    
    try:
        with open(metadata_file) as f:
            metadata = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error reading metadata.yml: {e}")
        return False
    
    # Check if paper is published (has DOI)
    if not metadata.get('doi'):
        print(f"⚠️ Paper not yet published (no DOI found)")
        return False
    
    # Generate HTML content
    html_content = generate_html_template(metadata, paper_path)
    
    # Write index.html to paper directory
    index_file = paper_path / 'index.html'
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Generated {index_file}")
        return True
    except Exception as e:
        print(f"❌ Error writing index.html: {e}")
        return False

def generate_html_template(metadata, paper_path):
    """Generate HTML template for paper page"""
    
    # Extract metadata
    title = metadata.get('title', 'Untitled Paper')
    authors = metadata.get('authors', [])
    abstract = metadata.get('abstract', '')
    keywords = metadata.get('keywords', [])
    doi = metadata.get('doi', '')
    publication_date = metadata.get('publication_date', '')
    field = metadata.get('field', '')
    volume = metadata.get('volume', '')
    issue = metadata.get('issue', '')
    article_number = metadata.get('article_number', '')
    
    # Generate authors HTML
    authors_html = ""
    for author in authors:
        name = author.get('name', '')
        affiliation = author.get('affiliation', '')
        email = author.get('email', '')
        orcid = author.get('orcid', '')
        
        orcid_link = f' <a href="https://orcid.org/{orcid}" target="_blank">🔗</a>' if orcid else ''
        
        authors_html += f"""
                    <div class="author">
                        <strong>{name}</strong>{orcid_link}<br>
                        <em>{affiliation}</em><br>
                        <a href="mailto:{email}">{email}</a>
                    </div>"""
    
    # Generate keywords string
    keywords_str = ", ".join(keywords) if keywords else ""
    
    # Calculate relative path to root
    # papers/2025/001-paper-name/ -> ../../../
    relative_root = "../../../"
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Syntavion Journal</title>
    <link rel="stylesheet" href="{relative_root}style.css">
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
        .paper-meta a {{
            color: #93c5fd;
        }}
        .download-section {{
            text-align: center;
            margin: 2rem 0;
            padding: 2rem;
            background: #f8fafc;
            border-radius: 15px;
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
                <a href="{relative_root}index.html">Home</a>
                <a href="{relative_root}about.html">About</a>
                <a href="{relative_root}submit.html">Submit</a>
                <a href="{relative_root}archives.html">Archives</a>
                <a href="{relative_root}editorial-board.html">Editorial Board</a>
                <a href="{relative_root}contact.html">Contact</a>
            </div>
        </div>
    </nav>

    <main>
        <div class="container">
            <div class="paper-header">
                <h1 class="paper-title">{title}</h1>
                
                <div class="authors">{authors_html}
                </div>
                
                <div class="paper-meta">
                    <p><strong>DOI:</strong> <a href="https://doi.org/{doi}" target="_blank">{doi}</a></p>
                    <p><strong>Published:</strong> {publication_date}</p>
                    <p><strong>Keywords:</strong> {keywords_str}</p>
                    <p><strong>Field:</strong> {field}</p>
                    <p><strong>License:</strong> CC BY 4.0</p>
                    <p><strong>Volume:</strong> {volume}, Issue: {issue}, Article: {article_number}</p>
                </div>
            </div>

            <div class="download-section">
                <h3>📄 Download & Access</h3>
                <a href="paper.pdf" class="cta-button" target="_blank">📄 Download PDF</a>
                <a href="https://doi.org/{doi}" class="cta-button" target="_blank">🔗 View on Zenodo</a>
            </div>

            <div class="paper-content">
                <h2>Abstract</h2>
                <p>{abstract}</p>
                
                <h2>Full Paper</h2>
                <p>For the complete research paper including methodology, results, discussion, and references, please download the PDF or access the paper on Zenodo using the links above.</p>
                
                <h2>Citation</h2>
                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; font-family: monospace;">
                    {authors[0].get('name', '') if authors else 'Author'}. ({publication_date[:4] if publication_date else 'Year'}). {title}. <em>Syntavion Journal</em>, {volume}({issue}), {article_number}. <a href="https://doi.org/{doi}">https://doi.org/{doi}</a>
                </div>
            </div>

            <div style="text-align: center; margin: 2rem 0;">
                <a href="{relative_root}archives.html" class="cta-button">← Back to Archives</a>
                <a href="https://doi.org/{doi}" class="cta-button" target="_blank">Cite This Paper</a>
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
    
    return html_template

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_paper_page.py <paper_directory>")
        sys.exit(1)
    
    paper_dir = sys.argv[1]
    if not generate_paper_page(paper_dir):
        sys.exit(1)

if __name__ == "__main__":
    main()
