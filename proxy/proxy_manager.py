import requests
import random
import tkinter.messagebox as messagebox
from stem import Signal
from stem.control import Controller
import sys
class ProxyManager:
    def __init__(self, config):
        self.config = config
        self.proxies = None
        self.proxy_list = []
        self.setup_proxy()

    def fetch_proxy_list(self):
        """Fetch a list of proxies from a free proxy service"""
        try:
            url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
            response = requests.get(url)
            if response.status_code == 200:
                self.proxy_list = response.text.splitlines()
                messagebox.showinfo("Proxy Fetch", f"Fetched {len(self.proxy_list)} proxies.")
            else:
                messagebox.showerror("Proxy Fetch", "Failed to fetch proxies.")
        except Exception as e:
            messagebox.showerror("Proxy Fetch", f"Error fetching proxies: {str(e)}")

    def get_random_proxy(self):
        """Get a random proxy from the fetched list"""
        if not self.proxy_list:
            self.fetch_proxy_list()
        if self.proxy_list:
            return random.choice(self.proxy_list)
        return None

    def setup_proxy(self):
        """Configure proxy or Tor based on config"""
        proxy_config = self.config.get("proxy", {})
        if proxy_config.get("use_tor", False):
            self.start_tor()
            self.proxies = {
                'http': f'socks5h://127.0.0.1:{proxy_config["tor_port"]}',
                'https': f'socks5h://127.0.0.1:{proxy_config["tor_port"]}'
            }
        elif proxy_config.get("use_proxy", False):
            if proxy_config.get("dynamic_proxy", False):
                proxy_url = self.get_random_proxy()
                if proxy_url:
                    self.proxies = {
                        'http': f'http://{proxy_url}',
                        'https': f'http://{proxy_url}'
                    }
                    print(f"Using dynamic proxy: {proxy_url}")
                else:
                    messagebox.showerror("Proxy Error", "No proxies available.")
                    sys.exit(1)
            else:
                self.proxies = {
                    'http': proxy_config["proxy_url"],
                    'https': proxy_config["proxy_url"]
                }
                print(f"Using static proxy: {proxy_config['proxy_url']}")
        else:
            self.proxies = None
            print("No proxy configured.")

    def start_tor(self):
        """Start Tor process"""
        try:
            from stem.process import launch_tor_with_config
            tor_config = {
                'SocksPort': str(self.config["proxy"]["tor_port"]),
                'ControlPort': str(self.config["proxy"]["tor_control_port"])
            }
            self.tor_process = launch_tor_with_config(config=tor_config)
        except Exception as e:
            messagebox.showerror("Tor Error", f"Failed to start Tor: {str(e)}")
            sys.exit(1)

    def renew_tor_ip(self):
        """Renew Tor IP address"""
        try:
            with Controller.from_port(port=self.config["proxy"]["tor_control_port"]) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
                messagebox.showinfo("Tor IP Renewed", "Tor IP address has been renewed.")
        except Exception as e:
            messagebox.showerror("Tor Error", f"Failed to renew Tor IP: {str(e)}")