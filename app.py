import tkinter as tk
from tkinter import ttk, messagebox
import threading
from bot.orders import place_order
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price

BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
GREEN = "#3fb950"
RED = "#f85149"
YELLOW = "#d29922"
TEXT = "#e6edf3"
MUTED = "#8b949e"
FONT = ("Consolas", 11)
FONT_BOLD = ("Consolas", 11, "bold")
FONT_TITLE = ("Consolas", 16, "bold")
FONT_SMALL = ("Consolas", 9)

class TradingBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binance Futures Trading Bot")
        self.root.configure(bg=BG)
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        self.build_ui()

    def build_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg=BG)
        title_frame.pack(fill="x", padx=20, pady=(20, 5))
        tk.Label(title_frame, text="⬡ BINANCE FUTURES BOT",
                font=FONT_TITLE, bg=BG, fg=GREEN).pack(side="left")
        tk.Label(title_frame, text="TESTNET",
                font=FONT_SMALL, bg=YELLOW, fg=BG,
                padx=6, pady=2).pack(side="left", padx=10)

        # Divider
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=20)

        # Order Form Panel
        form_frame = tk.Frame(self.root, bg=PANEL, bd=0)
        form_frame.pack(fill="x", padx=20, pady=15)

        tk.Label(form_frame, text="ORDER DETAILS",
                font=FONT_BOLD, bg=PANEL, fg=MUTED).grid(
                row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12,8))

        fields = [
            ("Symbol", "BTCUSDT"),
            ("Quantity", "0.002"),
            ("Price (LIMIT only)", ""),
        ]

        self.entries = {}
        for i, (label, default) in enumerate(fields):
            tk.Label(form_frame, text=label, font=FONT,
                    bg=PANEL, fg=TEXT).grid(
                    row=i+1, column=0, sticky="w", padx=15, pady=6)
            entry = tk.Entry(form_frame, font=FONT, bg=BG, fg=TEXT,
                           insertbackground=TEXT, relief="flat",
                           bd=0, highlightthickness=1,
                           highlightbackground=BORDER,
                           highlightcolor=GREEN, width=28)
            entry.insert(0, default)
            entry.grid(row=i+1, column=1, padx=15, pady=6, ipady=6)
            self.entries[label] = entry

        # Side selector
        tk.Label(form_frame, text="Side", font=FONT,
                bg=PANEL, fg=TEXT).grid(
                row=4, column=0, sticky="w", padx=15, pady=6)
        self.side_var = tk.StringVar(value="BUY")
        side_frame = tk.Frame(form_frame, bg=PANEL)
        side_frame.grid(row=4, column=1, sticky="w", padx=15, pady=6)
        self.buy_btn = tk.Button(side_frame, text="BUY",
                                font=FONT_BOLD, bg=GREEN, fg=BG,
                                relief="flat", padx=20, pady=4,
                                command=lambda: self.set_side("BUY"))
        self.buy_btn.pack(side="left", padx=(0,5))
        self.sell_btn = tk.Button(side_frame, text="SELL",
                                 font=FONT_BOLD, bg=BORDER, fg=MUTED,
                                 relief="flat", padx=20, pady=4,
                                 command=lambda: self.set_side("SELL"))
        self.sell_btn.pack(side="left")

        # Order type selector
        tk.Label(form_frame, text="Order Type", font=FONT,
                bg=PANEL, fg=TEXT).grid(
                row=5, column=0, sticky="w", padx=15, pady=6)
        self.type_var = tk.StringVar(value="MARKET")
        type_frame = tk.Frame(form_frame, bg=PANEL)
        type_frame.grid(row=5, column=1, sticky="w", padx=15, pady=6)
        self.market_btn = tk.Button(type_frame, text="MARKET",
                                   font=FONT_BOLD, bg=YELLOW, fg=BG,
                                   relief="flat", padx=16, pady=4,
                                   command=lambda: self.set_type("MARKET"))
        self.market_btn.pack(side="left", padx=(0,5))
        self.limit_btn = tk.Button(type_frame, text="LIMIT",
                                  font=FONT_BOLD, bg=BORDER, fg=MUTED,
                                  relief="flat", padx=16, pady=4,
                                  command=lambda: self.set_type("LIMIT"))
        self.limit_btn.pack(side="left")

        # Place order button
        self.order_btn = tk.Button(form_frame, text="PLACE ORDER",
                                  font=FONT_BOLD, bg=GREEN, fg=BG,
                                  relief="flat", padx=20, pady=10,
                                  width=30, command=self.place_order)
        self.order_btn.grid(row=6, column=0, columnspan=2, pady=15)

        # Divider
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=20)

        # Response panel
        resp_frame = tk.Frame(self.root, bg=PANEL)
        resp_frame.pack(fill="x", padx=20, pady=15)
        tk.Label(resp_frame, text="ORDER RESPONSE",
                font=FONT_BOLD, bg=PANEL, fg=MUTED).pack(
                anchor="w", padx=15, pady=(12,8))

        self.resp_labels = {}
        resp_fields = ["Order ID", "Status", "Executed Qty", "Avg Price"]
        for field in resp_fields:
            row = tk.Frame(resp_frame, bg=PANEL)
            row.pack(fill="x", padx=15, pady=3)
            tk.Label(row, text=f"{field}:", font=FONT,
                    bg=PANEL, fg=MUTED, width=14,
                    anchor="w").pack(side="left")
            lbl = tk.Label(row, text="—", font=FONT_BOLD,
                          bg=PANEL, fg=TEXT, anchor="w")
            lbl.pack(side="left")
            self.resp_labels[field] = lbl

        # Divider
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=20)

        # Log panel
        log_frame = tk.Frame(self.root, bg=PANEL)
        log_frame.pack(fill="both", expand=True, padx=20, pady=15)
        tk.Label(log_frame, text="ACTIVITY LOG",
                font=FONT_BOLD, bg=PANEL, fg=MUTED).pack(
                anchor="w", padx=15, pady=(12,8))
        self.log_box = tk.Text(log_frame, font=FONT_SMALL,
                              bg=BG, fg=MUTED, relief="flat",
                              bd=0, height=8, state="disabled",
                              wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=15, pady=(0,12))

    def set_side(self, side):
        self.side_var.set(side)
        if side == "BUY":
            self.buy_btn.config(bg=GREEN, fg=BG)
            self.sell_btn.config(bg=BORDER, fg=MUTED)
        else:
            self.sell_btn.config(bg=RED, fg=TEXT)
            self.buy_btn.config(bg=BORDER, fg=MUTED)

    def set_type(self, order_type):
        self.type_var.set(order_type)
        if order_type == "MARKET":
            self.market_btn.config(bg=YELLOW, fg=BG)
            self.limit_btn.config(bg=BORDER, fg=MUTED)
        else:
            self.limit_btn.config(bg=YELLOW, fg=BG)
            self.market_btn.config(bg=BORDER, fg=MUTED)

    def log(self, message, color=None):
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"› {message}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def update_response(self, response):
        if "orderId" in response:
            self.resp_labels["Order ID"].config(
                text=str(response.get("orderId", "—")), fg=GREEN)
            self.resp_labels["Status"].config(
                text=response.get("status", "—"), fg=GREEN)
            self.resp_labels["Executed Qty"].config(
                text=str(response.get("executedQty", "—")), fg=TEXT)
            self.resp_labels["Avg Price"].config(
                text=str(response.get("avgPrice", "—")), fg=TEXT)
            self.log(f"Order placed! ID: {response['orderId']}", GREEN)
        else:
            msg = response.get("msg", "Unknown error")
            self.resp_labels["Status"].config(text=f"FAILED: {msg}", fg=RED)
            self.log(f"Order failed: {msg}")

    def place_order(self):
        threading.Thread(target=self._place_order_thread).start()

    def _place_order_thread(self):
        try:
            symbol = validate_symbol(self.entries["Symbol"].get())
            quantity = validate_quantity(self.entries["Quantity"].get())
            side = validate_side(self.side_var.get())
            order_type = validate_order_type(self.type_var.get())

            price = None
            if order_type == "LIMIT":
                price_val = self.entries["Price (LIMIT only)"].get()
                if not price_val:
                    self.log("Price is required for LIMIT orders!")
                    return
                price = validate_price(price_val)

            self.log(f"Placing {order_type} {side} {quantity} {symbol}...")
            self.order_btn.config(state="disabled", text="PLACING...")

            response = place_order(symbol, side, order_type, quantity, price)
            self.root.after(0, self.update_response, response)

        except ValueError as e:
            self.root.after(0, self.log, f"Validation error: {e}")
        except Exception as e:
            self.root.after(0, self.log, f"Error: {e}")
        finally:
            self.root.after(0, self.order_btn.config,
                          {"state": "normal", "text": "PLACE ORDER"})

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotApp(root)
    root.mainloop()