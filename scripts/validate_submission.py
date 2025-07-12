import sys
import yaml
import json
from pathlib import Path

def validate_paper(paper_dir):
    """Validate paper submission"""
    paper_path = Path(paper_dir)
    errors = []
    warnings = []
    
    print(f"🔍 Validating {paper_path.name}...")
    
    # Check required files
    required_files = ['paper.md', 'paper.pdf', 'metadata.yml', '.zenodo.json']
    for file in required_files:
        if not (paper_path / file).exists():
            errors.append(f"Missing required file: {file}")
    
    # Validate metadata.yml
    metadata_file = paper_path / 'metadata.yml'
    if metadata_file.exists():
        try:
            with open(metadata_file) as f:
                metadata = yaml.safe_load(f)
            
            required_fields = ['title', 'authors', 'abstract', 'keywords']
            for field in required_fields:
                if field not in metadata or not metadata[field]:
                    errors.append(f"Missing or empty required metadata field: {field}")
            
            # Validate authors
            if 'authors' in metadata and isinstance(metadata['authors'], list):
                for i, author in enumerate(metadata['authors']):
                    if not isinstance(author, dict):
                        errors.append(f"Author {i+1} must be a dictionary")
                        continue
                    
                    required_author_fields = ['name', 'affiliation', 'email']
                    for field in required_author_fields:
                        if field not in author or not author[field]:
                            errors.append(f"Author {i+1} missing required field: {field}")
            
            # Validate keywords
            if 'keywords' in metadata:
                if not isinstance(metadata['keywords'], list):
                    errors.append("Keywords must be a list")
                elif len(metadata['keywords']) < 3:
                    warnings.append("Recommend at least 3 keywords")
                elif len(metadata['keywords']) > 10:
                    warnings.append("Too many keywords (max 10 recommended)")
            
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in metadata.yml: {e}")
    
    # Validate .zenodo.json
    zenodo_file = paper_path / '.zenodo.json'
    if zenodo_file.exists():
        try:
            with open(zenodo_file) as f:
                zenodo_data = json.load(f)
            
            required_zenodo_fields = ['title', 'description', 'creators', 'keywords']
            for field in required_zenodo_fields:
                if field not in zenodo_data:
                    errors.append(f"Missing required Zenodo field: {field}")
                    
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in .zenodo.json: {e}")
    
    # Check PDF file size (max 50MB)
    pdf_file = paper_path / 'paper.pdf'
    if pdf_file.exists():
        size_mb = pdf_file.stat().st_size / (1024 * 1024)
        if size_mb > 50:
            errors.append(f"PDF file too large: {size_mb:.1f}MB (max 50MB)")
        elif size_mb < 0.1:
            warnings.append(f"PDF file very small: {size_mb:.1f}MB")
    
    # Print results
    if warnings:
        print("⚠️ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Paper validation passed")
        return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_submission.py <paper_directory>")
        sys.exit(1)
    
    paper_dir = sys.argv[1]
    if not validate_paper(paper_dir):
        sys.exit(1)

if __name__ == "__main__":
    main()
