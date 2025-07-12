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
                            
                            # Only include papers with DOI (published)
                            if metadata.get('doi'):
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
    try:
        with open('archives.html', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ archives.html not found")
        return
    
    # Generate papers HTML
    papers_html = ""
    if papers:
        papers_html = """
        <div class="papers-list">
"""
        for paper in papers:
            authors_str = ", ".join([author['name'] for author in paper.get('authors', [])])
            abstract_preview = paper.get('abstract', '')[:200] + "..." if len(paper.get('abstract', '')) > 200 else paper.get('abstract', '')
            
            papers_html += f"""
            <article class="paper-item">
                <h4><a href="{paper['url']}">{paper['title']}</a></h4>
                <p class="authors">{authors_str}</p>
                <p class="abstract">{abstract_preview}</p>
                <div class="paper-meta">
                    <span class="date">📅 {paper.get('publication_date', 'Unknown')}</span>
                    <span class="doi">🔗 <a href="https://doi.org/{paper['doi']}" target="_blank">{paper['doi']}</a></span>
                    <span class="field">🔬 {paper.get('field', 'General')}</span>
                </div>
            </article>
"""
        papers_html += """
        </div>
"""
    
    # Replace the coming-soon section or update existing papers
    if papers:
        # Try to find and replace the coming-soon section
        start_marker = '<div class="coming-soon">'
        end_marker = '</div>\n                </div>'
        
        start_idx = content.find(start_marker)
        if start_idx != -1:
            # Find the end of the coming-soon div
            temp_content = content[start_idx:]
            div_count = 0
            end_idx = start_idx
            
            for i, char in enumerate(temp_content):
                if char == '<' and temp_content[i:i+5] == '<div ':
                    div_count += 1
                elif char == '<' and temp_content[i:i+6] == '</div>':
                    div_count -= 1
                    if div_count == 0:
                        end_idx = start_idx + i + 6
                        break
            
            if end_idx > start_idx:
                before = content[:start_idx]
                after = content[end_idx:]
                content = before + papers_html.strip() + after
        else:
            # If no coming-soon section, try to replace existing papers list
            papers_start = content.find('<div class="papers-list">')
            if papers_start != -1:
                papers_end = content.find('</div>', papers_start) + 6
                before = content[:papers_start]
                after = content[papers_end:]
                content = before + papers_html.strip() + after
    
    # Update stats
    content = content.replace(
        '<h3>0</h3>',
        f'<h3>{len(papers)}</h3>',
        1  # Only replace first occurrence
    )
    
    # Write updated content
    with open('archives.html', 'w') as f:
        f.write(content)

# Add CSS for paper items if not exists
def add_paper_styles():
    """Add CSS styles for paper items"""
    css_styles = """
/* Paper Items Styles */
.papers-list {
    display: grid;
    gap: 2rem;
    margin-top: 2rem;
}

.paper-item {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    border-left: 4px solid #3b82f6;
    transition: transform 0.3s;
}

.paper-item:hover {
    transform: translateY(-2px);
}

.paper-item h4 {
    color: #1e3a8a;
    margin-bottom: 1rem;
    font-size: 1.3rem;
}

.paper-item h4 a {
    text-decoration: none;
    color: inherit;
}

.paper-item h4 a:hover {
    text-decoration: underline;
}

.paper-item .authors {
    color: #666;
    font-weight: 500;
    margin-bottom: 1rem;
}

.paper-item .abstract {
    color: #333;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.paper-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    font-size: 0.9rem;
}

.paper-meta span {
    background: #f8fafc;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
}

.paper-meta a {
    color: #3b82f6;
    text-decoration: none;
}

.paper-meta a:hover {
    text-decoration: underline;
}

@media (max-width: 768px) {
    .paper-meta {
        flex-direction: column;
        gap: 0.5rem;
    }
}
"""
    
    # Check if style.css exists and add styles if needed
    try:
        with open('style.css', 'r') as f:
            css_content = f.read()
        
        if 'papers-list' not in css_content:
            with open('style.css', 'a') as f:
                f.write(f"\n\n{css_styles}")
            print("✅ Added paper styles to CSS")
    except FileNotFoundError:
        print("⚠️ style.css not found, skipping CSS update")

if __name__ == "__main__":
    generate_archives()
    add_paper_styles()
