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
    required_files = ['paper.md', 'README.md', 'metadata.yml', '.zenodo.json']
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
            
            if 'authors' in metadata:
                for i, author in enumerate(metadata['authors']):
                    required_author_fields = ['name', 'affiliation', 'email']
                    for field in required_author_fields:
                        if field not in author or not author[field]:
                            errors.append(f"Author {i+1} missing required field: {field}")
        
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in metadata.yml: {e}")
    
    # Validate .zenodo.json
    zenodo_file = paper_path / '.zenodo.json'
    if zenodo_file.exists():
        try:
            with open(zenodo_file) as f:
                json.load(f)  # Solo verifica sintattica
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in .zenodo.json: {e}")
    
    # Output risultati
    if warnings:
        print("⚠️ Warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Paper validation passed")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_submission.py <paper_directory>")
        sys.exit(1)
    
    if not validate_paper(sys.argv[1]):
        sys.exit(1)
