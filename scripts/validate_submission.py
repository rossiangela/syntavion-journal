name: Create Paper Structure

on:
  workflow_dispatch:
    inputs:
      paper_id:
        description: 'Paper ID (e.g., 001-parkinson-voice)'
        required: true
        type: string
      year:
        description: 'Publication year'
        required: true
        default: '2025'
        type: string

permissions:
  contents: write
  actions: read

jobs:
  create-structure:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - name: Create paper directory structure
        run: |
          PAPER_DIR=papers/${{ github.event.inputs.year }}/${{ github.event.inputs.paper_id }}
          if [ -d "$PAPER_DIR" ]; then
            echo "❌ Directory $PAPER_DIR already exists. Exiting..."
            exit 1
          fi
          echo "📁 Creating directory at $PAPER_DIR"
          mkdir -p "$PAPER_DIR"
          echo "# Paper content goes here" > "$PAPER_DIR/paper.md"
          echo "# Upload your PDF here and rename it to paper.pdf" > "$PAPER_DIR/README.md"
          
          cat > "$PAPER_DIR/metadata.yml" << 'EOF'
          title: "Your Paper Title Here"
          authors:
            - name: "Your Name"
              affiliation: "Your Institution"
              email: "your.email@domain.com"
              orcid: "0000-0000-0000-0000"

          abstract: |
            Write your abstract here. Keep it under 300 words.
          keywords: 
            - "keyword1"
            - "keyword2"
            - "keyword3"

          submission_date: null
          acceptance_date: null
          publication_date: null
          doi: null
          zenodo_id: null

          volume: 1
          issue: 1
          article_number: null
          field: "Your Field"
          license: "CC BY 4.0"
          EOF

          cat > "$PAPER_DIR/.zenodo.json" << 'EOF'
          {
            "title": "Your Paper Title Here",
            "description": "Write your abstract here. Keep it under 300 words.",
            "creators": [
              {
                "name": "Name, Your",
                "affiliation": "Your Institution",
                "orcid": "0000-0000-0000-0000"
              }
            ],
            "keywords": [
              "keyword1",
              "keyword2",
              "keyword3"
            ],
            "license": "CC-BY-4.0",
            "upload_type": "publication",
            "publication_type": "article",
            "access_right": "open",
            "communities": [
              {
                "identifier": "syntavionjournal"
              }
            ],
            "journal_title": "Syntavion Journal",
            "journal_volume": "1",
            "journal_issue": "1",
            "related_identifiers": [
              {
                "identifier": "https://syntavionjournal.org",
                "relation": "isPartOf",
                "resource_type": "publication-journal"
              }
            ],
            "notes": "Published in Syntavion Journal - Open Access Scientific Publishing for All Sciences"
          }
          EOF

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Create validation script
        run: |
          cat > validate_submission.py << 'EOF'
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
          EOF

      - name: Install dependencies
        run: pip install pyyaml

      - name: Validate paper structure
        run: python validate_submission.py papers/${{ github.event.inputs.year }}/${{ github.event.inputs.paper_id }}

      - name: Commit new structure
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "Syntavion Journal Bot"
          git add .
          if git diff --staged --quiet; then
            echo "✅ No changes to commit"
          else
            git commit -m "📁 Created paper structure: papers/${{ github.event.inputs.year }}/${{ github.event.inputs.paper_id }}"
            git push
