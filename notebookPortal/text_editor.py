# text_editor.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import socket

# Configuration
HOST = '192.168.0.7'  # The server's IP address
PORT = 65432          # The port used by the server

def open_file():
    filepath = filedialog.askopenfilename(defaultextension=".txt",
                                          filetypes=[("Text files", "*.txt"), ("All files", "*")])
    if filepath:
        with open(filepath, 'r') as file:
            text_editor.delete(1.0, tk.END)  # Clear existing content
            text_editor.insert(tk.END, file.read())  # Insert new content

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*")])
    if filepath:
        with open(filepath, 'w') as file:
            file.write(text_editor.get(1.0, tk.END))  # Save current content

def update_servers():
    servers = get_running_servers()
    server_dropdown['values'] = servers
    if servers:
        server_dropdown.set(servers[0])
    else:
        server_dropdown.set("No running servers")

def get_running_servers():
    # Returns a list of running servers
    servers = []
    try:
        # Try connecting to the server to check if it's running
        with socket.create_connection((HOST, PORT), timeout=1):
            servers.append(f"{HOST}:{PORT}")
    except (socket.timeout, ConnectionRefusedError):
        pass
    return servers

# Create the main application window
root = tk.Tk()
root.title("Text Editor with Server Dropdown")

# Create the text editor widget
text_editor = tk.Text(root, wrap='word', height=20, width=60)
text_editor.pack(padx=10, pady=10)

# Create the drop-down menu
server_dropdown = ttk.Combobox(root, state="readonly")
server_dropdown.pack(padx=10, pady=(0, 10))
update_servers()

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add File menu with Open and Save options
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Exit", command=root.quit)

# Add Refresh option to update the server list
refresh_button = tk.Button(root, text="Refresh Servers", command=update_servers)
refresh_button.pack(pady=(0, 10))

# Run the application
root.mainloop()
