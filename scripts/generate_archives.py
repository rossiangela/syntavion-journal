# ============ scripts/generate_archives.py ============
#!/usr/bin/env python3

import os
import yaml
from pathlib import Path
from datetime import datetime

def generate_archives():
    """Generate updated archives.html with all published papers"""
    papers = []
    
    # Scan papers directory
    papers_dir = Path('papers')
    if not papers_dir.exists():
        print("Papers directory not found")
        return
    
    for year_dir in papers_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit():
            for paper_dir in year_dir.iterdir():
                if paper_dir.is_dir() and paper_dir.name != 'template':
                    try:
                        # Load paper metadata
                        metadata_file = paper_dir / 'metadata.yml'
                        if metadata_file.exists():
                            with open(metadata_file) as f:
                                metadata = yaml.safe_load(f)
                            
                            # Skip if no DOI (not published yet)
                            if not metadata.get('doi'):
                                continue
                            
                            # Add computed fields
                            metadata['year'] = year_dir.name
                            metadata['paper_id'] = paper_dir.name
                            metadata['url'] = f"papers/{year_dir.name}/{paper_dir.name}/"
                            
                            papers.append(metadata)
                    except Exception as e:
                        print(f"Error processing {paper_dir}: {e}")
    
    # Sort papers by publication date (newest first)
    papers.sort(key=lambda x: x.get('publication_date', ''), reverse=True)
    
    # Update the existing archives.html
    update_archives_html(papers)
    
    print(f"✅ Generated archives.html with {len(papers)} papers")

def update_archives_html(papers):
    """Update archives.html with papers list"""
    
    # Read existing archives.html
    with open('archives.html', 'r') as f:
        content = f.read()
    
    # Generate papers HTML
    papers_html = ""
    if papers:
        papers_html = """
        <div class="papers-list">
"""
        for paper in papers:
            authors_str = ", ".join([author['name'] for author in paper.get('authors', [])])
            papers_html += f"""
            <article class="paper-item">
                <h4><a href="{paper['url']}">{paper['title']}</a></h4>
                <p class="authors">{authors_str}</p>
                <p class="abstract">{paper.get('abstract', '')[:200]}...</p>
                <div class="paper-meta">
                    <span class="date">Published: {paper.get('publication_date', 'Unknown')}</span>
                    <span class="doi">DOI: <a href="https://doi.org/{paper['doi']}" target="_blank">{paper['doi']}</a></span>
                    <span class="field">{paper.get('field', 'General')}</span>
                </div>
            </article>
"""
        papers_html += """
        </div>
"""
