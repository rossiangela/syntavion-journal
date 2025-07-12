#!/usr/bin/env python3
import os
import argparse
import json
import yaml
import requests
from pathlib import Path
from typing import Dict, Any

class ZenodoUploader:
    def __init__(self, token: str, sandbox: bool = False):
        self.token = token
        self.base_url = "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    
    def upload_paper(self, paper_path: str, journal_doi: str = None) -> str:
        """Upload paper to Zenodo with journal relationship"""
        path = Path(paper_path)
        print(f"📤 Processing: {path.name}")
        
        try:
            # Load metadata
            metadata = self._load_yml(path / 'metadata.yml')
            zenodo_metadata = self._load_json(path / '.zenodo.json')
            
            # Add journal relationship if provided
            if journal_doi:
                zenodo_metadata = self._add_journal_relation(zenodo_metadata, journal_doi)
            
            # Create deposition
            deposition = self._create_deposition()
            self._upload_file(deposition['links']['bucket'], path / 'paper.pdf')
            self._update_metadata(deposition['id'], zenodo_metadata)
            
            # Publish
            published = self._publish_deposition(deposition['id'])
            self._update_local_metadata(path, metadata, published)
            
            print(f"✅ Published! DOI: {published['doi']}")
            return published['doi']
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            raise

    def _add_journal_relation(self, metadata: Dict[str, Any], journal_doi: str) -> Dict[str, Any]:
        """Add journal DOI as related identifier"""
        if 'related_identifiers' not in metadata:
            metadata['related_identifiers'] = []
        
        metadata['related_identifiers'].append({
            'relation': 'isPartOf',
            'identifier': journal_doi,
            'scheme': 'doi'
        })
        return metadata

    # ... (keep all other helper methods from previous version)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='Path to paper directory')
    parser.add_argument('--journal-doi', help='Journal DOI to link with')
    args = parser.parse_args()

    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        raise ValueError("ZENODO_TOKEN environment variable not set")

    uploader = ZenodoUploader(token)
    uploader.upload_paper(args.path, args.journal_doi)

if __name__ == "__main__":
    main()
