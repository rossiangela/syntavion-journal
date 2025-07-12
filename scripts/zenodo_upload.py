#!/usr/bin/env python3
import os
import sys
import json
import yaml
import requests
from pathlib import Path
from typing import Dict, Any

class ZenodoUploader:
    def __init__(self, token: str, journal_doi: str = "10.5281/zenodo.15870031", sandbox: bool = False):
        self.token = token
        self.journal_doi = journal_doi  # DOI fisso del journal
        self.base_url = "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
    def upload_paper(self, paper_dir: str) -> str:
        """Upload paper to Zenodo and return DOI"""
        paper_path = Path(paper_dir)
        if not paper_path.exists():
            raise FileNotFoundError(f"Paper directory not found: {paper_dir}")
        
        print(f"📤 Processing paper from: {paper_path}")
        print(f"🔖 Journal DOI: {self.journal_doi}")

        try:
            # Validate and load metadata
            self._validate_files(paper_path)
            metadata = self._load_metadata(paper_path)
            zenodo_metadata = self._prepare_zenodo_metadata(paper_path)
            
            # Create and populate deposition
            deposition = self._create_deposition()
            self._upload_files(deposition['links']['bucket'], paper_path)
            self._update_metadata(deposition['id'], zenodo_metadata)
            
            # Publish and update local records
            published = self._publish_deposition(deposition['id'])
            self._update_local_metadata(paper_path, metadata, published)
            
            print(f"✅ Successfully published! Paper DOI: {published['doi']}")
            return published['doi']
            
        except requests.exceptions.RequestException as e:
            error_msg = e.response.text if e.response else str(e)
            print(f"❌ HTTP Error: {error_msg}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            raise
    
    def _prepare_zenodo_metadata(self, paper_path: Path) -> Dict[str, Any]:
        """Prepare metadata with journal DOI"""
        with open(paper_path / '.zenodo.json') as f:
            metadata = json.load(f)
        
        # Aggiungi il DOI del journal come related identifier
        if 'related_identifiers' not in metadata:
            metadata['related_identifiers'] = []
            
        metadata['related_identifiers'].append({
            'relation': 'isPartOf',
            'identifier': self.journal_doi,
            'scheme': 'doi'
        })
        
        return metadata

    # ... (keep all other methods unchanged from previous version)

def main():
    if len(sys.argv) != 2:
        print("Usage: python zenodo_upload.py <paper_directory>")
        print("Example: python zenodo_upload.py papers/2024/001-example")
        sys.exit(1)
    
    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        print("❌ Error: ZENODO_TOKEN environment variable not set")
        sys.exit(1)
    
    try:
        uploader = ZenodoUploader(
            token=token,
            journal_doi="10.5281/zenodo.15870031"  # DOI fisso del journal
        )
        uploader.upload_paper(sys.argv[1])
    except Exception as e:
        print(f"❌ Publication failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
