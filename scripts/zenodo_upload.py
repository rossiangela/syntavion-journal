import os
import sys
import json
import yaml
import requests
from pathlib import Path

class ZenodoUploader:
    def __init__(self, token, sandbox=False):
        self.token = token
        self.base_url = "https://sandbox.zenodo.org/api" if sandbox else "https://zenodo.org/api"
        self.headers = {'Content-Type': 'application/json'}
        
    def upload_paper(self, paper_dir):
        """Upload paper to Zenodo and get DOI"""
        paper_path = Path(paper_dir)
        print(f"📤 Uploading {paper_path.name} to Zenodo...")
        
        try:
            # Read metadata
            with open(paper_path / 'metadata.yml') as f:
                metadata = yaml.safe_load(f)
                
            # Read Zenodo metadata
            with open(paper_path / '.zenodo.json') as f:
                zenodo_metadata = json.load(f)
            
            # Add journal DOI reference
            if 'related_identifiers' not in zenodo_metadata:
                zenodo_metadata['related_identifiers'] = []
            
            # Add journal DOI
            zenodo_metadata['related_identifiers'].append({
                'identifier': '10.5281/zenodo.15870031',
                'relation': 'isPartOf',
                'resource_type': 'publication-journal'
            })
            
            # Create new deposition
            print("Creating Zenodo deposition...")
            deposition = self.create_deposition()
            deposition_id = deposition['id']
            bucket_url = deposition['links']['bucket']
            
            # Upload PDF
            pdf_file = paper_path / 'paper.pdf'
            if pdf_file.exists():
                print(f"Uploading PDF: {pdf_file.name}")
                self.upload_file(bucket_url, pdf_file)
            else:
                raise FileNotFoundError(f"PDF file not found: {pdf_file}")
            
            # Update metadata
            print("Updating metadata...")
            self.update_metadata(deposition_id, zenodo_metadata)
            
            # Publish
            print("Publishing deposition...")
            published = self.publish_deposition(deposition_id)
            
            # Get DOI
            doi = published['doi']
            print(f"✅ Published! DOI: {doi}")
            
            # Update metadata.yml with DOI
            metadata['doi'] = doi
            metadata['zenodo_id'] = published['id']
            
            with open(paper_path / 'metadata.yml', 'w') as f:
                yaml.dump(metadata, f, default_flow_style=False)
                
            return doi
            
        except Exception as e:
            print(f"❌ Error uploading to Zenodo: {e}")
            raise
    
    def create_deposition(self):
        """Create new Zenodo deposition"""
        r = requests.post(
            f"{self.base_url}/deposit/depositions",
            params={'access_token': self.token},
            json={},
            headers=self.headers
        )
        r.raise_for_status()
        return r.json()
    
    def upload_file(self, bucket_url, file_path):
        """Upload file to deposition bucket"""
        with open(file_path, 'rb') as fp:
            r = requests.put(
                f"{bucket_url}/{file_path.name}",
                data=fp,
                params={'access_token': self.token}
            )
        r.raise_for_status()
        return r.json()
    
    def update_metadata(self, deposition_id, metadata):
        """Update deposition metadata"""
        data = {'metadata': metadata}
        r = requests.put(
            f"{self.base_url}/deposit/depositions/{deposition_id}",
            params={'access_token': self.token},
            data=json.dumps(data),
            headers=self.headers
        )
        r.raise_for_status()
        return r.json()
    
    def publish_deposition(self, deposition_id):
        """Publish the deposition"""
        r = requests.post(
            f"{self.base_url}/deposit/depositions/{deposition_id}/actions/publish",
            params={'access_token': self.token}
        )
        r.raise_for_status()
        return r.json()

def main():
    if len(sys.argv) != 2:
        print("Usage: python zenodo_upload.py <paper_directory>")
        sys.exit(1)
    
    paper_dir = sys.argv[1]
    token = os.environ.get('ZENODO_TOKEN')
    
    if not token:
        print("❌ ZENODO_TOKEN environment variable not set")
        sys.exit(1)
    
    uploader = ZenodoUploader(token)
    uploader.upload_paper(paper_dir)

if __name__ == "__main__":
    main()
