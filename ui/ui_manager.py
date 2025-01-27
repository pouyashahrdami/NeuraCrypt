import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import sys

class UIManager:
    def __init__(self, root, config, ai_manager):
        self.root = root
        self.config = config
        self.ai_manager = ai_manager
        self.is_visible = True
        self.setup_window()
        self.create_widgets()
        self.setup_bindings()

    def setup_window(self):
        self.root.title("NeuraCrypt")
        self.root.geometry('300x400+1500+100')
        self.root.configure(bg='#f0f0f0')
        self.root.attributes('-alpha', 0.4)
        self.root.attributes('-topmost', True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.style = ttk.Style()
        self.style.configure('Compact.TButton', padding=2, font=('Helvetica', 8))
        self.style.configure('Explode.TButton', padding=2, font=('Helvetica', 8), foreground='red')

    def create_widgets(self):
        self.main_container = ttk.Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.chat_history = scrolledtext.ScrolledText(
            self.main_container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Helvetica', 8),
            bg='#ffffff',
            height=15
        )
        self.chat_history.grid(row=0, column=0, sticky='nsew', pady=(0, 5))

        self.input_text = tk.Text(
            self.main_container,
            height=2,
            font=('Helvetica', 8),
            bg='#ffffff',
            wrap=tk.WORD
        )
        self.input_text.grid(row=1, column=0, sticky='ew', pady=(0, 5))

        self.button_frame = ttk.Frame(self.main_container)
        self.button_frame.grid(row=2, column=0, sticky='ew')
        self.button_frame.grid_columnconfigure(1, weight=1)

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

    def on_resize(self, event):
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
            threading.Thread(target=self._send_message_async, args=(user_input,)).start()

    def _send_message_async(self, user_input):
        try:
            self.status_bar.config(text="AI is typing...")
            self.root.update()

            response_text = self.ai_manager.generate_response(user_input)

            self.root.after(0, self._update_chat, user_input, response_text)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))

    def _update_chat(self, user_input, response_text):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "You: ", "user")
        self.chat_history.insert(tk.END, f"{user_input}\n", "user_message")
        self.chat_history.insert(tk.END, "AI: ", "bot")
        self.chat_history.insert(tk.END, f"{response_text}\n", "bot_message")
        self.chat_history.config(state=tk.DISABLED)
        self.input_text.delete("1.0", tk.END)
        self.status_bar.config(text="F10:Toggle | Ctrl+Enter:Send")

    def _show_error(self, error_message):
        self.status_bar.config(text=f"Error: {str(error_message)[:20]}...")
        self.chat_history.insert(tk.END, f"Error: {error_message}\n", "error")

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