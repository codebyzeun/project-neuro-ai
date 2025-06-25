import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import os
import threading
import subprocess
import sys
from pathlib import Path
import json
import asyncio
from dotenv import load_dotenv, set_key

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DiscordBotGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("YiXuan Discord Bot Launcher")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Bot process
        self.bot_process = None
        self.is_running = False

        # Load existing config
        self.load_config()

        # Setup UI
        self.setup_ui()

        # Center window
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")

    def load_config(self):
        """Load configuration from .env file"""
        self.config = {
            'discord_token': '',
            'model_path': './models/synexis.gguf',
            'max_tokens': 65,
            'temperature': 0.8,
            'context_window': 2048
        }

        if os.path.exists('.env'):
            load_dotenv()
            self.config['discord_token'] = os.getenv('DISCORD_TOKEN', '')
            self.config['model_path'] = os.getenv('MODEL_PATH', './models/synexis.gguf')

    def setup_ui(self):
        """Setup the main UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🤖 YiXuan Discord Bot",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Sassy AI powered by Mistral 7B",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        subtitle_label.pack(pady=(0, 30))

        # Configuration Section
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", padx=20, pady=(0, 20))

        config_title = ctk.CTkLabel(
            config_frame,
            text="⚙️ Configuration",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        config_title.pack(pady=(15, 10))

        # Discord Token
        token_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        token_frame.pack(fill="x", padx=20, pady=(0, 15))

        token_label = ctk.CTkLabel(token_frame, text="Discord Bot Token:", font=ctk.CTkFont(size=12, weight="bold"))
        token_label.pack(anchor="w")

        self.token_entry = ctk.CTkEntry(
            token_frame,
            placeholder_text="Paste your Discord bot token here...",
            show="*",
            height=35,
            font=ctk.CTkFont(size=11)
        )
        self.token_entry.pack(fill="x", pady=(5, 0))
        self.token_entry.insert(0, self.config['discord_token'])

        # Model Path
        model_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        model_frame.pack(fill="x", padx=20, pady=(0, 15))

        model_label = ctk.CTkLabel(model_frame, text="AI Model Path:", font=ctk.CTkFont(size=12, weight="bold"))
        model_label.pack(anchor="w")

        model_input_frame = ctk.CTkFrame(model_frame, fg_color="transparent")
        model_input_frame.pack(fill="x", pady=(5, 0))

        self.model_entry = ctk.CTkEntry(
            model_input_frame,
            placeholder_text="Path to your .gguf model file...",
            height=35,
            font=ctk.CTkFont(size=11)
        )
        self.model_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.model_entry.insert(0, self.config['model_path'])

        browse_btn = ctk.CTkButton(
            model_input_frame,
            text="Browse",
            command=self.browse_model,
            width=80,
            height=35
        )
        browse_btn.pack(side="right")

        self.advanced_frame = ctk.CTkFrame(config_frame)
        self.advanced_frame.pack(fill="x", padx=20, pady=(0, 20))

        advanced_header = ctk.CTkFrame(self.advanced_frame, fg_color="transparent")
        advanced_header.pack(fill="x", pady=(10, 0))

        self.advanced_btn = ctk.CTkButton(
            advanced_header,
            text="🔧 Advanced Settings ▼",
            command=self.toggle_advanced,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray20"),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.advanced_btn.pack()

        self.advanced_content = ctk.CTkFrame(self.advanced_frame, fg_color="transparent")
        self.advanced_expanded = False

        temp_frame = ctk.CTkFrame(self.advanced_content, fg_color="transparent")
        temp_frame.pack(fill="x", pady=(10, 5))

        temp_label = ctk.CTkLabel(temp_frame, text="Temperature (Creativity):", font=ctk.CTkFont(size=11))
        temp_label.pack(anchor="w")

        self.temp_slider = ctk.CTkSlider(temp_frame, from_=0.1, to=2.0, number_of_steps=19)
        self.temp_slider.pack(fill="x", pady=(5, 0))
        self.temp_slider.set(self.config['temperature'])

        self.temp_value = ctk.CTkLabel(temp_frame, text=f"{self.config['temperature']:.1f}")
        self.temp_value.pack(anchor="e")
        self.temp_slider.configure(command=self.update_temp_label)

        # Max Tokens
        tokens_frame = ctk.CTkFrame(self.advanced_content, fg_color="transparent")
        tokens_frame.pack(fill="x", pady=5)

        tokens_label = ctk.CTkLabel(tokens_frame, text="Max Response Length:", font=ctk.CTkFont(size=11))
        tokens_label.pack(anchor="w")

        self.tokens_entry = ctk.CTkEntry(tokens_frame, width=100, height=30)
        self.tokens_entry.pack(anchor="w", pady=(5, 0))
        self.tokens_entry.insert(0, str(self.config['max_tokens']))

        # Status and Control Section
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", padx=20, pady=(0, 20))

        status_title = ctk.CTkLabel(
            control_frame,
            text="🚀 Bot Control",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        status_title.pack(pady=(15, 10))

        # Status indicator
        self.status_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.status_indicator = ctk.CTkLabel(
            self.status_frame,
            text="⚫ Offline",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="red"
        )
        self.status_indicator.pack()

        # Control buttons
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.start_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Start Bot",
            command=self.start_bot,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.start_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="🛑 Stop Bot",
            command=self.stop_bot,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#dc3545",
            hover_color="#c82333",
            state="disabled"
        )
        self.stop_btn.pack(side="right", expand=True, fill="x", padx=(10, 0))

        # Log output
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, padx=20)

        log_title = ctk.CTkLabel(log_frame, text="📋 Bot Logs", font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(pady=(15, 10))

        self.log_text = ctk.CTkTextbox(log_frame, height=150, font=ctk.CTkFont(family="Consolas", size=10))
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def toggle_advanced(self):
        if self.advanced_expanded:
            self.advanced_content.pack_forget()
            self.advanced_btn.configure(text="🔧 Advanced Settings ▼")
            self.advanced_expanded = False
        else:
            self.advanced_content.pack(fill="x", pady=(10, 0))
            self.advanced_btn.configure(text="🔧 Advanced Settings ▲")
            self.advanced_expanded = True

    def update_temp_label(self, value):
        self.temp_value.configure(text=f"{float(value):.1f}")

    def browse_model(self):
        filename = filedialog.askopenfilename(
            title="Select AI Model File",
            filetypes=[("GGUF files", "*.gguf"), ("All files", "*.*")],
            initialdir="./models" if os.path.exists("./models") else "."
        )
        if filename:
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, filename)

    def save_config(self):
        """Save configuration to .env file"""
        token = self.token_entry.get().strip()
        model_path = self.model_entry.get().strip()

        if not token:
            messagebox.showerror("Error", "Discord token is required!")
            return False

        if not model_path or not os.path.exists(model_path):
            messagebox.showerror("Error", "Please select a valid model file!")
            return False

        try:
            # Create or update .env file
            with open('.env', 'w') as f:
                f.write(f"DISCORD_TOKEN={token}\n")
                f.write(f"MODEL_PATH={model_path}\n")

            # Update config.py with advanced settings
            temp = self.temp_slider.get()
            max_tokens = int(self.tokens_entry.get())

            config_content = f'''AI_CONFIG = {{
    'max_new_tokens': {max_tokens},
    'temperature': {temp:.1f},
    'context_window': 2048,
    'top_p': 0.9,
    'repeat_penalty': 1.2,
    'n_threads': 4,
}}

CHAT_CONFIG = {{
    'history_limit': 10,
    'max_response_length': 1900,
    'typing_speed': 50,
}}'''

            with open('config.py', 'w') as f:
                f.write(config_content)

            self.log("✅ Configuration saved successfully!")
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
            return False

    def start_bot(self):
        """Start the Discord bot"""
        if not self.save_config():
            return

        try:
            self.log("🚀 Starting Discord bot...")

            # Start bot in separate process
            self.bot_process = subprocess.Popen(
                [sys.executable, "bot.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            self.is_running = True
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.status_indicator.configure(text="🟢 Online", text_color="green")

            # Start log monitoring thread
            self.log_thread = threading.Thread(target=self.monitor_logs, daemon=True)
            self.log_thread.start()

        except Exception as e:
            self.log(f"❌ Failed to start bot: {str(e)}")
            messagebox.showerror("Error", f"Failed to start bot: {str(e)}")

    def stop_bot(self):
        """Stop the Discord bot"""
        if self.bot_process:
            self.log("🛑 Stopping Discord bot...")
            self.bot_process.terminate()
            self.bot_process.wait()
            self.bot_process = None

        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_indicator.configure(text="⚫ Offline", text_color="red")
        self.log("✅ Bot stopped successfully!")

    def monitor_logs(self):
        """Monitor bot output and display in GUI"""
        if not self.bot_process:
            return

        try:
            for line in iter(self.bot_process.stdout.readline, ''):
                if not self.is_running:
                    break
                self.log(line.strip())
        except Exception as e:
            self.log(f"Log monitoring error: {str(e)}")

    def log(self, message):
        """Add message to log display"""

        def update_log():
            self.log_text.insert("end", f"{message}\n")
            self.log_text.see("end")

        # Schedule update in main thread
        self.root.after(0, update_log)

    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            self.stop_bot()
        self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    required_files = ['bot.py', 'cogs/ai_chat.py', 'utils/llm_handler.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all bot files are in the correct location.")
        input("Press Enter to exit...")
        sys.exit(1)

    try:
        app = DiscordBotGUI()
        app.run()
    except ImportError as e:
        if "customtkinter" in str(e):
            print("❌ CustomTkinter not installed!")
            print("Install it with: pip install customtkinter")
        else:
            print(f"❌ Import error: {e}")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("Press Enter to exit...")