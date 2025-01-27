import json
import ctypes
import sys
import tkinter.messagebox as messagebox

class ConfigManager:
    @staticmethod
    def load_config():
        """Load configuration from config.json file"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            # Create default config file if it doesn't exist
            default_config = {
                "api_key": "YOUR_API_KEY_HERE",
                "model": "gemini-1.5-flash",
                "window": {
                    "width": 300,
                    "height": 400,
                    "x": 1500,
                    "y": 100,
                    "opacity": 0.4
                },
                "proxy": {
                    "use_proxy": False,
                    "proxy_url": "http://your_proxy:port",
                    "use_tor": False,
                    "tor_port": 9050,
                    "tor_control_port": 9051,
                    "dynamic_proxy": False
                },
                "isadmin": False
            }
            with open('config.json', 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid config.json format")
            sys.exit(1)

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def run_as_admin():
        config = ConfigManager.load_config()
        if config.get("isadmin", False) and not ConfigManager.is_admin():
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()