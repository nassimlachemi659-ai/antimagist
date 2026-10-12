"""
keygen_admin.py — Antimagist V5 Master Admin License Key Generator
===================================================================
Antimagist Enterprise Security V5 Admin Suite
- Private key generator for the software creator
- Issues valid cryptographic license keys for paying customers
- Supports:
    • 10€ Lifetime License (No Expiration)
    • 2€ Monthly License (30-day auto-expiry)
    • Custom duration (7, 30, 90, 365 days)
- Features:
    • Beautiful modern GUI for 1-click key creation & clipboard copy
    • CLI generator for command-line automation
    • Automatically records issued keys to 'issued_licenses.json'
"""

import os
import sys
import time
import json
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from license_manager import compute_key_signature

DATABASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "issued_licenses.json")


def generate_license_key(tier: str = "LIFETIME", duration_days: int = 30, customer_name: str = "Anonymous") -> str:
    """Generates a cryptographically signed Antimagist V5 license key."""
    tier_code = "LIFE" if tier.upper() == "LIFETIME" else "SUB"

    if tier_code == "LIFE":
        expiry_val = "9999999999"
    else:
        expiry_val = str(int(time.time()) + (duration_days * 86400))

    # Generate random 4-character hex seed
    seed = "".join(random.choices("0123456789ABCDEF", k=4))

    payload = f"AM5-{tier_code}-{expiry_val}-{seed}"
    sig = compute_key_signature(payload)

    key = f"{payload}-{sig}"

    # Log to local records
    record = {
        "license_key": key,
        "tier": tier.upper(),
        "customer": customer_name,
        "issued_at": int(time.time()),
        "expires_at": int(expiry_val),
        "duration_days": duration_days if tier_code == "SUB" else "LIFETIME"
    }
    _save_record(record)
    return key


def _save_record(record: dict):
    records = []
    if os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []
    records.append(record)
    try:
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    except Exception:
        pass


class AntimagistKeygenApp(ctk.CTk):
    """Cyber Sci-Fi Admin Keygen Window."""

    def __init__(self):
        super().__init__()
        self.title("Antimagist V5 — Admin Keygen & Sales Center")
        self.geometry("560x520")
        self.resizable(False, False)
        self.configure(fg_color="#08090E")

        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#0F1320", corner_radius=0, height=70)
        header.pack(fill="x", padx=0, pady=0)

        lbl_title = ctk.CTkLabel(
            header,
            text="🔑 ANTIMAGIST V5 KEYGEN ADMIN",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color="#00F0FF"
        )
        lbl_title.pack(anchor="w", padx=20, pady=(12, 2))

        lbl_sub = ctk.CTkLabel(
            header,
            text="Official Commercial Licensing & Key Issuance Engine",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#94A3B8"
        )
        lbl_sub.pack(anchor="w", padx=20, pady=(0, 10))

        # Main Body
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=16)

        # Customer Field
        ctk.CTkLabel(body, text="Customer Discord / Email:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#E2E8F0").pack(anchor="w", pady=(4, 2))
        self.ent_customer = ctk.CTkEntry(body, placeholder_text="e.g. GamerPro#1337 or user@gmail.com", fg_color="#161F33", border_color="#334155")
        self.ent_customer.pack(fill="x", pady=(0, 12))

        # License Tier Selection
        ctk.CTkLabel(body, text="Select License Package:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#E2E8F0").pack(anchor="w", pady=(4, 2))
        self.tier_var = tk.StringVar(value="LIFETIME")

        tier_frame = ctk.CTkFrame(body, fg_color="#121826")
        tier_frame.pack(fill="x", pady=(0, 14), padx=0)

        r1 = ctk.CTkRadioButton(
            tier_frame, text="💎 Lifetime License (€10)",
            variable=self.tier_var, value="LIFETIME",
            text_color="#00FF9D", fg_color="#00FF9D"
        )
        r1.pack(side="left", padx=16, pady=12)

        r2 = ctk.CTkRadioButton(
            tier_frame, text="⚡ Monthly Subscription (€2 / 30 Days)",
            variable=self.tier_var, value="MONTHLY",
            text_color="#00F0FF", fg_color="#00F0FF"
        )
        r2.pack(side="left", padx=16, pady=12)

        # Generate Button
        self.btn_gen = ctk.CTkButton(
            body,
            text="🚀 GENERATE SIGNED LICENSE KEY",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#00F0FF",
            text_color="#000000",
            hover_color="#38BDF8",
            height=40,
            command=self._on_generate
        )
        self.btn_gen.pack(fill="x", pady=10)

        # Result Key Display
        ctk.CTkLabel(body, text="Generated Customer License Key:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#00FF9D").pack(anchor="w", pady=(8, 2))
        self.ent_key = ctk.CTkEntry(
            body,
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            fg_color="#0D111A",
            border_color="#00FF9D",
            text_color="#00FF9D",
            height=42
        )
        self.ent_key.pack(fill="x", pady=(0, 10))

        # Action Buttons: Copy to Clipboard & View Issued
        btn_bar = ctk.CTkFrame(body, fg_color="transparent")
        btn_bar.pack(fill="x", pady=4)

        btn_copy = ctk.CTkButton(
            btn_bar,
            text="📋 Copy Key to Clipboard",
            fg_color="#1E293B",
            hover_color="#334155",
            command=self._copy_key
        )
        btn_copy.pack(side="left", expand=True, fill="x", padx=(0, 6))

        btn_db = ctk.CTkButton(
            btn_bar,
            text="📁 View Issued Keys DB",
            fg_color="#1E293B",
            hover_color="#334155",
            command=self._view_db
        )
        btn_db.pack(side="right", expand=True, fill="x", padx=(6, 0))

    def _on_generate(self):
        tier = self.tier_var.get()
        customer = self.ent_customer.get().strip() or "Customer"
        key = generate_license_key(tier=tier, duration_days=30, customer_name=customer)

        self.ent_key.delete(0, "end")
        self.ent_key.insert(0, key)

    def _copy_key(self):
        k = self.ent_key.get()
        if k:
            self.clipboard_clear()
            self.clipboard_append(k)
            messagebox.showinfo("Copied", "License Key copied to clipboard! Send this to your buyer.")

    def _view_db(self):
        if os.path.exists(DATABASE_FILE):
            os.startfile(DATABASE_FILE)
        else:
            messagebox.showinfo("Database", "No keys have been issued yet.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        tier = sys.argv[2] if len(sys.argv) > 2 else "LIFETIME"
        cust = sys.argv[3] if len(sys.argv) > 3 else "CLI-User"
        key = generate_license_key(tier=tier, customer_name=cust)
        print(f"GENERATED_KEY: {key}")
    else:
        app = AntimagistKeygenApp()
        app.mainloop()
