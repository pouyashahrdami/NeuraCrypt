# """  _   _                       _____                  _
# | \ | |                     / ____|                | |
# |  \| | ___ _   _ _ __ __ _| |     _ __ _   _ _ __ | |_
# | . ` |/ _ \ | | | '__/ _` | |    | '__| | | | '_ \| __|
# | |\  |  __/ |_| | | | (_| | |____| |  | |_| | |_) | |_
# |_| \_|\___|\__,_|_|  \__,_|\_____|_|   \__, | .__/ \__|
#                                          __/ | |
#                                         |___/|_|
# """ By Pouya --------

from configs.config_manager import ConfigManager
from proxy.proxy_manager import ProxyManager
from ai.ai_manager import AIManager
from ui.ui_manager import UIManager
import tkinter as tk

class CompactGeminiChat:
    def __init__(self):
        ConfigManager.run_as_admin()
        self.config = ConfigManager.load_config()
        self.proxy_manager = ProxyManager(self.config)
        self.ai_manager = AIManager(self.config, self.proxy_manager.proxies)
        self.root = tk.Tk()
        self.ui_manager = UIManager(self.root, self.config, self.ai_manager)
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CompactGeminiChat()
    app.run()
