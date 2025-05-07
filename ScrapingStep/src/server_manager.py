"""
Server Manager Module

This module handles all server-related operations including starting, stopping, and health checks.
"""

import requests
import subprocess
import time
import os

class ServerManager:
    def __init__(self, server_path, port=5000):
        """
        Initialize the server manager
        
        Args:
            server_path (str): Path to the server directory
            port (int): Server port number
        """
        self.server_path = server_path
        self.port = port
        self.base_url = f"http://localhost:{port}"
        
    def restart_server(self):
        """Restart the server without printing too many messages"""
        try:
            # Safely stop all Node.js processes
            try:
                if os.name == 'nt':  # Windows
                    subprocess.run(["taskkill", "/F", "/IM", "node.exe"], 
                                 shell=True, capture_output=True, timeout=30)
                else:  # Linux/Mac
                    subprocess.run(["pkill", "-f", "node"], 
                                 shell=True, capture_output=True, timeout=30)
            except:
                pass
            
            # Wait to ensure all processes are closed
            time.sleep(3)
            
            # Change to server directory
            original_dir = os.getcwd()
            os.chdir(self.server_path)
            
            # Start server in background
            if os.name == 'nt':  # Windows
                subprocess.Popen(["npm", "start"], 
                               shell=True, 
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            else:  # Linux/Mac
                os.system("npm start > server.log 2>&1 &")
            
            os.chdir(original_dir)
            
            # Wait for server to start
            time.sleep(10)
            
            # Test server health
            response = requests.get(f"{self.base_url}/v1/site/sharh/1", timeout=10)
            if response.status_code != 200:
                raise Exception("Server failed to start properly")
                
        except Exception as e:
            raise Exception(f"Failed to restart server: {str(e)}")
    
    def test_server_health(self):
        """Test server health"""
        try:
            response = requests.get(f"{self.base_url}/v1/site/sharh/1", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def shutdown_server(self):
        """Shutdown the server"""
        print("\n🛑 Shutting down server...")
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(["taskkill", "/F", "/IM", "node.exe"], check=True)
            else:  # Linux/Mac
                subprocess.run(["pkill", "-f", "node"], check=True)
            time.sleep(2)
            print("✅ Server shut down successfully")
        except Exception as e:
            print(f"❌ Error shutting down server: {str(e)}")
            raise 