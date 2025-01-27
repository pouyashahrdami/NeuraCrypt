# """  _   _                       _____                  _
# | \ | |                     / ____|                | |
# |  \| | ___ _   _ _ __ __ _| |     _ __ _   _ _ __ | |_
# | . ` |/ _ \ | | | '__/ _` | |    | '__| | | | '_ \| __|
# | |\  |  __/ |_| | | | (_| | |____| |  | |_| | |_) | |_
# |_| \_|\___|\__,_|_|  \__,_|\_____|_|   \__, | .__/ \__|
#                                          __/ | |
#                                         |___/|_|
# """ By Pouya --------

import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import google.generativeai as genai
import keyboard
import sys
import ctypes
import os
import win32gui
import win32con
import json


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
            "isadmin": False
        }
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid config.json format")
        sys.exit(1)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    config = load_config()
    if config.get("isadmin", False) and not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


class CompactGeminiChat:
    def __init__(self):
        self.config = load_config()
        self.setup_window()
        self.setup_ai()
        self.create_widgets()
        self.setup_bindings()
        self.is_visible = True

    def setup_window(self):
        self.root = tk.Tk()
        self.root.title("NeuraCrypt")
        # Start with a smaller default size
        self.root.geometry('300x400+1500+100')  # Positioned near screen right
        self.root.configure(bg='#f0f0f0')
        self.root.attributes('-alpha', 0.4)
        self.root.attributes('-topmost', True)

        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Minimal style configuration
        self.style = ttk.Style()
        self.style.configure('Compact.TButton', padding=2,
                             font=('Helvetica', 8))
        self.style.configure('Explode.TButton', padding=2,
                             font=('Helvetica', 8), foreground='red')

    def setup_ai(self):
        try:
            genai.configure(api_key=self.config['api_key'])
            self.model = genai.GenerativeModel(self.config['model'])
        except Exception as e:
            messagebox.showerror("Configuration Error",
                                 "Please check your API key and model name in config.json")
            sys.exit(1)

    def create_widgets(self):
        # Main container using grid layout
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(
            row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Chat history
        self.chat_history = scrolledtext.ScrolledText(
            self.main_container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Helvetica', 8),
            bg='#ffffff',
            height=15
        )
        self.chat_history.grid(row=0, column=0, sticky='nsew', pady=(0, 5))

        # Input area
        self.input_text = tk.Text(
            self.main_container,
            height=2,
            font=('Helvetica', 8),
            bg='#ffffff',
            wrap=tk.WORD
        )
        self.input_text.grid(row=1, column=0, sticky='ew', pady=(0, 5))

        # Button frame using grid
        self.button_frame = ttk.Frame(self.main_container)
        self.button_frame.grid(row=2, column=0, sticky='ew')
        self.button_frame.grid_columnconfigure(
            1, weight=1)  # Make middle space expandable

        # Compact buttons
        self.send_button = ttk.Button(
            self.button_frame,
            text="📤",
            width=3,
            command=self.send_message,
            style='Compact.TButton'
        )
        self.send_button.grid(row=0, column=0, padx=1)

        self.clear_button = ttk.Button(
            self.button_frame,
            text="🗑️",
            width=3,
            command=self.clear_chat,
            style='Compact.TButton'
        )
        self.clear_button.grid(row=0, column=1, padx=1)

        self.explode_button = ttk.Button(
            self.button_frame,
            text="💥",
            width=3,
            command=self.explode_app,
            style='Explode.TButton'
        )
        self.explode_button.grid(row=0, column=2, padx=1)

        # Minimal status bar
        self.status_bar = ttk.Label(
            self.main_container,
            text="F10:Toggle | Ctrl+Enter:Send",
            anchor=tk.W,
            font=('Helvetica', 7)
        )
        self.status_bar.grid(row=3, column=0, sticky='ew', pady=(2, 0))

    def setup_bindings(self):
        self.root.bind('<F10>', lambda e: self.toggle_visibility())
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())
        self.input_text.bind('<Return>', lambda e: self.handle_return(e))
        keyboard.on_press_key('F10', lambda _: self.toggle_visibility())

        # Add resize binding
        self.root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        # Maintain minimum size
        if event.widget == self.root:
            min_width = 200
            min_height = 300
            if event.width < min_width:
                self.root.geometry(f'{min_width}x{event.height}')
            if event.height < min_height:
                self.root.geometry(f'{event.width}x{min_height}')

    def handle_return(self, event):
        if not event.state & 0x4:
            return
        self.send_message()
        return 'break'

    def send_message(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            try:
                self.status_bar.config(text="Sending...")
                self.root.update()

                response = self.model.generate_content(user_input)

                self.chat_history.config(state=tk.NORMAL)
                self.chat_history.insert(tk.END, "You: ", "user")
                self.chat_history.insert(
                    tk.END, f"{user_input}\n", "user_message")
                self.chat_history.insert(tk.END, "AI: ", "bot")
                self.chat_history.insert(
                    tk.END, f"{response.text}\n", "bot_message")
                self.chat_history.see(tk.END)
                self.chat_history.config(state=tk.DISABLED)

                self.input_text.delete("1.0", tk.END)
                self.status_bar.config(text="F10:Toggle | Ctrl+Enter:Send")

            except Exception as e:
                self.status_bar.config(text=f"Error: {str(e)[:20]}...")

    def clear_chat(self):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.config(state=tk.DISABLED)
        self.status_bar.config(text="Cleared")

    def toggle_visibility(self):
        if self.is_visible:
            self.root.attributes('-alpha', 0.0)
            self.is_visible = False
        else:
            self.root.attributes('-alpha', 0.4)
            self.is_visible = True

    def explode_app(self):
        for i in range(10, -1, -1):
            self.root.attributes('-alpha', i/10)
            self.root.update()
            self.root.after(50)
        self.root.destroy()
        sys.exit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    run_as_admin()
    app = CompactGeminiChat()
    app.run()
