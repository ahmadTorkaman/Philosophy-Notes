#!/usr/bin/env python3
"""
Philosophy Bot Sync Client
Keeps your local Obsidian vault in sync with the bot server

Usage:
    python3 philosophy_sync.py --token YOUR_TOKEN --vault ~/Documents/PhilosophyVault
    
    Optional:
    --interval SECONDS    Sync interval in seconds (default: 3600 = 1 hour)
    --once                Run sync once and exit
    --server URL          Server URL (default: http://localhost:5000)
"""

import requests
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

class PhilosophySync:
    """Sync client for Philosophy Bot vault"""
    
    def __init__(self, token, vault_path, server_url="http://localhost:5000"):
        self.token = token
        self.vault_path = Path(vault_path).expanduser()
        self.server_url = server_url.rstrip('/')
        self.state_file = self.vault_path / '.sync_state.json'
        
        # Create vault directory if it doesn't exist
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        # Load sync state
        self.state = self.load_state()
    
    def load_state(self):
        """Load local sync state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {'files': {}, 'last_sync': None}
    
    def save_state(self):
        """Save sync state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def get_server_status(self):
        """Get vault status from server"""
        url = f"{self.server_url}/api/sync/{self.token}/status"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error connecting to server: {e}")
            return None
    
    def download_file(self, file_path):
        """Download a specific file from server"""
        url = f"{self.server_url}/api/sync/{self.token}/file"
        params = {'path': file_path}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Write to local vault
            local_file = self.vault_path / file_path
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(local_file, 'wb') as f:
                f.write(response.content)
            
            return True
        
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error downloading {file_path}: {e}")
            return False
    
    def sync(self):
        """Perform sync"""
        print(f"🔄 Syncing... [{datetime.now().strftime('%H:%M:%S')}]")
        
        # Get server status
        server_status = self.get_server_status()
        
        if not server_status:
            print("❌ Failed to connect to server")
            return False
        
        server_files = {f['path']: f for f in server_status.get('files', [])}
        
        # Determine what needs to be synced
        files_to_download = []
        
        for path, info in server_files.items():
            local_info = self.state['files'].get(path)
            
            # New file or modified file
            if not local_info or local_info['modified'] < info['modified']:
                files_to_download.append(path)
        
        # Download files
        if files_to_download:
            print(f"📥 Downloading {len(files_to_download)} file(s)...")
            
            for file_path in files_to_download:
                if self.download_file(file_path):
                    print(f"  ✓ {file_path}")
                    # Update state
                    self.state['files'][file_path] = server_files[file_path]
                else:
                    print(f"  ✗ {file_path}")
            
            self.state['last_sync'] = datetime.now().isoformat()
            self.save_state()
            
            print(f"✓ Sync complete - {len(files_to_download)} file(s) updated")
        else:
            print("✓ Already up to date")
        
        return True
    
    def run_continuous(self, interval=3600):
        """Run sync continuously"""
        print("=" * 60)
        print("Philosophy Bot Sync Client")
        print("=" * 60)
        print(f"Vault: {self.vault_path}")
        print(f"Server: {self.server_url}")
        print(f"Sync interval: {interval} seconds ({interval//60} minutes)")
        print("\nPress Ctrl+C to stop\n")
        
        # Initial sync
        self.sync()
        
        # Continuous sync loop
        while True:
            try:
                time.sleep(interval)
                self.sync()
            except KeyboardInterrupt:
                print("\n\n✓ Sync stopped by user")
                break
            except Exception as e:
                print(f"⚠️  Error: {e}")
                time.sleep(60)  # Wait 1 minute before retry
    
    def run_once(self):
        """Run sync once and exit"""
        success = self.sync()
        return 0 if success else 1

def main():
    parser = argparse.ArgumentParser(
        description='Philosophy Bot Sync Client - Sync your Obsidian vault'
    )
    
    parser.add_argument(
        '--token',
        required=True,
        help='Your sync token from the bot (/sync command)'
    )
    
    parser.add_argument(
        '--vault',
        required=True,
        help='Path to your Obsidian vault folder'
    )
    
    parser.add_argument(
        '--server',
        default='http://localhost:5000',
        help='Server URL (default: http://localhost:5000)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=3600,
        help='Sync interval in seconds (default: 3600 = 1 hour)'
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run sync once and exit (no continuous sync)'
    )
    
    args = parser.parse_args()
    
    # Create sync client
    syncer = PhilosophySync(args.token, args.vault, args.server)
    
    # Run sync
    if args.once:
        exit(syncer.run_once())
    else:
        syncer.run_continuous(args.interval)

if __name__ == '__main__':
    main()
