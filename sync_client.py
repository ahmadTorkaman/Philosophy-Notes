#!/usr/bin/env python3
import argparse
import requests
import json
from pathlib import Path
from datetime import datetime
import time

class PhilosophySync:
    def __init__(self, token, vault_path, server="http://localhost:5000"):
        self.token = token
        self.vault_path = Path(vault_path).expanduser()
        self.server = server
        self.vault_path.mkdir(parents=True, exist_ok=True)
        self.state_file = self.vault_path / '.sync_state.json'
        self.state = self.load_state()
    
    def load_state(self):
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {'files': {}}
    
    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def sync(self):
        print(f"🔄 Syncing... [{datetime.now().strftime('%H:%M:%S')}]")
        
        try:
            r = requests.get(f"{self.server}/api/sync/{self.token}/status")
            r.raise_for_status()
            server_files = {f['path']: f for f in r.json()['files']}
            
            changes = 0
            for path, info in server_files.items():
                local_info = self.state['files'].get(path)
                if not local_info or local_info['modified'] < info['modified']:
                    r2 = requests.get(f"{self.server}/api/sync/{self.token}/file", params={'path': path})
                    local_file = self.vault_path / path
                    local_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(local_file, 'wb') as f:
                        f.write(r2.content)
                    print(f"📥 {path}")
                    self.state['files'][path] = info
                    changes += 1
            
            self.save_state()
            print(f"✓ Synced {changes} files" if changes else "✓ Up to date")
            return True
        except Exception as e:
            print(f"⚠️  Error: {e}")
            return False
    
    def run_once(self):
        print("Philosophy Bot Sync Client")
        print(f"Vault: {self.vault_path}\n")
        self.sync()
        return 0
    
    def run_continuous(self, interval=3600):
        print("Philosophy Bot Sync Client")
        print(f"Vault: {self.vault_path}")
        print(f"Interval: {interval}s\n")
        
        while True:
            try:
                self.sync()
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n✓ Stopped")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True)
    parser.add_argument('--vault', required=True)
    parser.add_argument('--server', default='http://localhost:5000')
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--interval', type=int, default=3600)
    
    args = parser.parse_args()
    syncer = PhilosophySync(args.token, args.vault, args.server)
    
    if args.once:
        syncer.run_once()
    else:
        syncer.run_continuous(args.interval)
