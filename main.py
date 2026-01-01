import customtkinter as ctk
import threading
import socket
import subprocess
import os
import requests
from datetime import datetime
from tkinter import filedialog
from core.scanner import NetworkScanner
from core.styles import COLORS, FONTS


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GhostNetwork v1.0")
        self.geometry("1100x800")

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.logo = ctk.CTkLabel(self.sidebar, text="GHOST NETWORK", font=FONTS["main_bold"])
        self.logo.pack(pady=30)

        self.ip_entry = ctk.CTkEntry(self.sidebar, placeholder_text="IP / URL / Range", width=210)
        self.ip_entry.pack(padx=20, pady=10)

        self.tab_manager = ctk.CTkTabview(self.sidebar, width=220)
        self.tab_manager.pack(padx=10, pady=10)
        self.tab_net = self.tab_manager.add("Security")
        self.tab_sys = self.tab_manager.add("OS/Extra")

        self.create_tool_btn(self.tab_net, "ARP Discovery", "arp")
        self.create_tool_btn(self.tab_net, "Nmap Service", "nmap_v")
        self.create_tool_btn(self.tab_net, "Nikto Web Scan", "nikto")

        self.create_tool_btn(self.tab_sys, "Geolocation", "geo")
        self.create_tool_btn(self.tab_sys, "System Load", "sys_stat")
        self.create_tool_btn(self.tab_sys, "My Public IP", "public_ip")

        self.save_btn = ctk.CTkButton(self.sidebar, text="💾 Save Log", fg_color="#27ae60", command=self.save_to_file)
        self.save_btn.pack(pady=10)

        self.clear_btn = ctk.CTkButton(self.sidebar, text="🗑️ Clear Console", fg_color="transparent", border_width=1,
                                       command=self.clear_logs)
        self.clear_btn.pack(pady=10)

        # --- CONSOLE AREA ---
        self.textbox = ctk.CTkTextbox(self, font=FONTS["terminal"], fg_color="#0a0a0a", text_color="#39ff14")
        self.textbox.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.status_label = ctk.CTkLabel(self, text="Status: Ready", font=FONTS["status"])
        self.status_label.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    def create_tool_btn(self, tab, text, mode):
        btn = ctk.CTkButton(tab, text=text, command=lambda m=mode: self.start_action(m), width=180)
        btn.pack(pady=5)

    def log(self, message):
        self.textbox.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.textbox.see("end")

    def save_to_file(self):
        content = self.textbox.get("0.0", "end").strip()
        if not content: return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 initialfile=f"ghost_report_{datetime.now().strftime('%Y%m%d')}.txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.log("[✔] Report saved successfully.")

    def clear_logs(self):
        self.textbox.delete("0.0", "end")

    def start_action(self, mode):
        target = self.ip_entry.get().strip()
        self.status_label.configure(text=f"Running {mode}...", text_color="yellow")
        threading.Thread(target=self.execute_task, args=(target, mode), daemon=True).start()

    def execute_task(self, target, mode):
        try:
            if mode == "geo":
                self.get_geo(target)
            elif mode == "sys_stat":
                self.get_sys_stats()
            elif mode == "public_ip":
                self.get_public_ip()
            elif mode == "arp":
                devices = NetworkScanner.scan_network(target)
                if isinstance(devices, list):
                    for d in devices: self.log(f"FOUND: {d['ip']} | MAC: {d['mac']}")
                    if not devices: self.log("[-] No devices found.")
                else:
                    self.log(f"[!] ARP Error: {devices}")
            elif mode == "nmap_v":
                self.run_process(["nmap", "-sV", "-T4", target])
            elif mode == "nikto":
                self.run_process(["nikto", "-h", target])
        except Exception as e:
            self.log(f"[!] Error: {str(e)}")

        self.status_label.configure(text="Finished", text_color="green")

    def get_geo(self, target):
        try:
            res = requests.get(f"http://ip-api.com/json/{target}").json()
            if res.get('status') == 'success':
                self.log(f"🌍 {target} -> {res['country']}, {res['city']} (ISP: {res['isp']})")
            else:
                self.log("[-] Geolocation failed for this target.")
        except:
            self.log("[!] Connection error during geo-lookup.")

    def get_sys_stats(self):
        self.log("--- UNIX SYSTEM STATS ---")
        try:
            cpu = subprocess.check_output("uptime", shell=True).decode().strip()
            ram = subprocess.check_output("free -h | grep 'Mem:'", shell=True).decode().strip()
            self.log(f"[CPU]: {cpu}")
            self.log(f"[RAM]: {ram}")
        except:
            self.log("[!] System commands failed. Ensure 'procps' is installed.")

    def get_public_ip(self):
        try:
            ip = requests.get("https://api.ipify.org").text
            self.log(f"[#] Your External IP: {ip}")
        except:
            self.log("[!] Failed to fetch public IP.")

    def run_process(self, cmd):
        self.log(f"[*] Running: {' '.join(cmd)}")
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout: self.log(line.strip())
            proc.wait()
        except FileNotFoundError:
            self.log(f"[!] Tool '{cmd[0]}' not found. Install it first!")


if __name__ == "__main__":
    app = App()
    app.mainloop()