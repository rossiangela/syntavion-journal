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
            with open(path / 'metadata.yml') as f:
                metadata = yaml.safe_load(f)
            
            with open(path / '.zenodo.json') as f:
                zenodo_metadata = json.load(f)
            
            # Add journal relationship if provided
            if journal_doi:
                zenodo_metadata = self._add_journal_relation(zenodo_metadata, journal_doi)
            
            # Create deposition
            print("🔹 Creating deposition...")
            deposition = self._create_deposition()
            
            # Upload PDF
            pdf_path = path / 'paper.pdf'
            print(f"⬆️ Uploading PDF: {pdf_path.name}")
            self._upload_file(deposition['links']['bucket'], pdf_path)
            
            # Update metadata
            print("🔹 Updating metadata...")
            self._update_metadata(deposition['id'], zenodo_metadata)
            
            # Publish
            print("🔹 Publishing...")
            published = self._publish_deposition(deposition['id'])
            
            # Update local metadata
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

    def _create_deposition(self) -> Dict[str, Any]:
        """Create new deposition"""
        r = requests.post(
            f"{self.base_url}/deposit/depositions",
            headers=self.headers,
            json={}
        )
        r.raise_for_status()
        return r.json()

    def _upload_file(self, bucket_url: str, file_path: Path) -> None:
        """Upload single file"""
        with open(file_path, 'rb') as f:
            r = requests.put(
                f"{bucket_url}/{file_path.name}",
                data=f,
                params={'access_token': self.token}
            )
        r.raise_for_status()

    def _update_metadata(self, deposition_id: str, metadata: Dict[str, Any]) -> None:
        """Update deposition metadata"""
        r = requests.put(
            f"{self.base_url}/deposit/depositions/{deposition_id}",
            headers=self.headers,
            json={'metadata': metadata}
        )
        r.raise_for_status()

    def _publish_deposition(self, deposition_id: str) -> Dict[str, Any]:
        """Publish deposition"""
        r = requests.post(
            f"{self.base_url}/deposit/depositions/{deposition_id}/actions/publish",
            params={'access_token': self.token}
        )
        r.raise_for_status()
        return r.json()

    def _update_local_metadata(self, paper_path: Path, metadata: Dict[str, Any], 
                             published_data: Dict[str, Any]) -> None:
        """Update local metadata.yml"""
        metadata.update({
            'doi': published_data['doi'],
            'zenodo_id': published_data['id'],
            'url': published_data['links']['doi']
        })
        
        with open(paper_path / 'metadata.yml', 'w') as f:
            yaml.dump(metadata, f, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description='Upload paper to Zenodo')
    parser.add_argument('--path', required=True, help='Path to paper directory')
    parser.add_argument('--journal-doi', help='Journal DOI to link with')
    args = parser.parse_args()

    token = os.environ.get('ZENODO_TOKEN')
    if not token:
        raise ValueError("ZENODO_TOKEN environment variable not set")

    try:
        uploader = ZenodoUploader(token)
        uploader.upload_paper(args.path, args.journal_doi)
    except Exception as e:
        print(f"❌ Publication failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
