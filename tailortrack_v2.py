# ============================================================
#   TailorTrack GUI v2 — Modern Glassy Interface
#   Course  : MGT-173 Introduction to Programming
#   Install : pip install customtkinter
#   Run     : python tailortrack_v2.py
# ============================================================

import customtkinter as ctk
import os

# ── File names ──
CUSTOMERS_FILE = "customers.txt"
ORDERS_FILE    = "orders.txt"
PAYMENTS_FILE  = "payments.txt"

# ── Theme ──
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Color Palette ──
BG       = "#06080f"   # deep black
SB       = "#080c17"   # sidebar
CARD     = "#0c1220"   # card surface
CARD2    = "#101828"   # slightly lighter card
GLOW     = "#0a84ff"   # bright cyan-blue
GLOW2    = "#0055cc"   # deeper blue
CYAN     = "#00c8ff"   # cyan highlight
BORDER   = "#1a2540"   # subtle border
TEXT     = "#e8f0ff"   # primary text
MUTED    = "#4a6080"   # muted text
DIM      = "#1e2d45"   # dim elements
SUCCESS  = "#00d68f"   # green
DANGER   = "#ff4d6a"   # red
WARN     = "#ffb830"   # amber

# ─────────────────────────────────────────────
#  FILE HELPERS
# ─────────────────────────────────────────────

def save_data(filename, data):
    file = open(filename, "w")
    for line in data:
        file.write(line + "\n")
    file.close()

def load_data(filename):
    if not os.path.exists(filename):
        return []
    file  = open(filename, "r")
    lines = file.read().splitlines()
    file.close()
    return [line for line in lines if line.strip() != ""]

def next_id(filename, prefix):
    data = load_data(filename)
    return f"{prefix}{len(data) + 1:03d}"

# ─────────────────────────────────────────────
#  WIDGET HELPERS
# ─────────────────────────────────────────────

def heading(parent, text, size=26):
    return ctk.CTkLabel(parent, text=text,
                        font=("Segoe UI", size, "bold"),
                        text_color=TEXT)

def subheading(parent, text):
    return ctk.CTkLabel(parent, text=text,
                        font=("Segoe UI", 12),
                        text_color=MUTED)

def label(parent, text, size=13, color=None):
    return ctk.CTkLabel(parent, text=text,
                        font=("Segoe UI", size),
                        text_color=color or TEXT)

def entry(parent, ph="", w=0):
    kwargs = dict(
        placeholder_text=ph, height=40,
        corner_radius=10, border_width=1,
        border_color=BORDER, fg_color=CARD2,
        text_color=TEXT, placeholder_text_color=MUTED,
        font=("Segoe UI", 13)
    )
    if w: kwargs["width"] = w
    return ctk.CTkEntry(parent, **kwargs)

def button(parent, text, cmd, color=None, w=140, icon=""):
    return ctk.CTkButton(
        parent, text=icon+text, command=cmd,
        fg_color=color or GLOW, hover_color=GLOW2,
        height=40, corner_radius=10,
        font=("Segoe UI", 13, "bold"), width=w,
        border_spacing=10
    )

def ghost_button(parent, text, cmd, w=120):
    return ctk.CTkButton(
        parent, text=text, command=cmd,
        fg_color="transparent", hover_color=DIM,
        border_width=1, border_color=BORDER,
        height=40, corner_radius=10,
        font=("Segoe UI", 13), width=w,
        text_color=TEXT
    )

def card(parent, **kw):
    return ctk.CTkFrame(parent, fg_color=CARD,
                        corner_radius=16,
                        border_width=1,
                        border_color=BORDER, **kw)

def divider(parent):
    ctk.CTkFrame(parent, height=1,
                 fg_color=BORDER).pack(fill="x", padx=24, pady=10)

def table_box(parent, h=240):
    return ctk.CTkTextbox(
        parent, height=h, corner_radius=10,
        font=("Consolas", 12),
        fg_color="#05080f",
        text_color=CYAN,
        border_color=BORDER, border_width=1,
        scrollbar_button_color=GLOW2,
        wrap="none"
    )

def fill_table(box, rows, headers=None):
    box.configure(state="normal")
    box.delete("1.0", "end")
    if not rows:
        box.insert("end", "  No records found.")
        box.configure(state="disabled")
        return
    w = 20
    if headers:
        box.insert("end", "  " + "".join(h.ljust(w) for h in headers) + "\n")
        box.insert("end", "  " + "─" * (w * len(headers)) + "\n")
    for r in rows:
        box.insert("end", "  " + "".join(str(x).ljust(w) for x in r) + "\n")
    box.configure(state="disabled")

def msg(lbl, text, ok=True):
    lbl.configure(
        text=("✓  " if ok else "✗  ") + text,
        text_color=SUCCESS if ok else DANGER
    )

def tabs(parent):
    return ctk.CTkTabview(
        parent,
        fg_color=CARD,
        segmented_button_fg_color=SB,
        segmented_button_selected_color=GLOW,
        segmented_button_selected_hover_color=GLOW2,
        segmented_button_unselected_color=SB,
        segmented_button_unselected_hover_color=DIM,
        text_color=TEXT,
        corner_radius=16,
        border_width=1,
        border_color=BORDER
    )

# ─────────────────────────────────────────────
#  STAT CARD
# ─────────────────────────────────────────────

class StatCard(ctk.CTkFrame):
    def __init__(self, parent, icon, title, color=GLOW, **kw):
        super().__init__(parent, fg_color=CARD, corner_radius=16,
                         border_width=1, border_color=BORDER, **kw)
        # glow bar
        ctk.CTkFrame(self, height=3, fg_color=color,
                     corner_radius=3).pack(fill="x")
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=18, pady=(12, 16))

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        # icon bubble
        bubble = ctk.CTkFrame(top, width=38, height=38,
                               fg_color=DIM, corner_radius=10)
        bubble.pack(side="left")
        bubble.pack_propagate(False)
        ctk.CTkLabel(bubble, text=icon,
                     font=("Segoe UI", 17)).place(relx=.5, rely=.5, anchor="center")

        ctk.CTkLabel(top, text=title,
                     font=("Segoe UI", 11),
                     text_color=MUTED).pack(side="left", padx=10)

        self.val = ctk.CTkLabel(inner, text="0",
                                font=("Segoe UI", 36, "bold"),
                                text_color=TEXT)
        self.val.pack(anchor="w", pady=(8, 0))

    def set(self, v):
        self.val.configure(text=str(v))

# ─────────────────────────────────────────────
#  BADGE LABEL
# ─────────────────────────────────────────────

STATUS_COLORS = {
    "Pending":     ("#1a2540", WARN),
    "In Progress": ("#0a1a35", GLOW),
    "Ready":       ("#0a2018", SUCCESS),
    "Delivered":   ("#1a1a2a", MUTED),
    "Paid":        ("#0a2018", SUCCESS),
    "Unpaid":      ("#2a0a10", DANGER),
}

# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("TailorTrack  ✂")
        self.geometry("1200x720")
        self.minsize(1000, 640)
        self.configure(fg_color=BG)
        self._sidebar()
        self._content()
        self.show("dashboard")

    # ── SIDEBAR ──
    def _sidebar(self):
        sb = ctk.CTkFrame(self, width=230, fg_color=SB, corner_radius=0)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # Logo
        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.pack(fill="x", padx=18, pady=(28, 10))

        icon_box = ctk.CTkFrame(logo, width=46, height=46,
                                 fg_color=GLOW, corner_radius=13)
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        ctk.CTkLabel(icon_box, text="✂",
                     font=("Segoe UI", 22),
                     text_color="white").place(relx=.5, rely=.5, anchor="center")

        txt = ctk.CTkFrame(logo, fg_color="transparent")
        txt.pack(side="left", padx=12)
        ctk.CTkLabel(txt, text="TailorTrack",
                     font=("Segoe UI", 17, "bold"),
                     text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(txt, text="v2.0  ·  MGT-173",
                     font=("Segoe UI", 10),
                     text_color=MUTED).pack(anchor="w")

        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(fill="x", padx=16, pady=(14, 10))
        ctk.CTkLabel(sb, text="MENU",
                     font=("Segoe UI", 10, "bold"),
                     text_color=MUTED).pack(anchor="w", padx=22, pady=(4, 6))

        self.nav = {}
        for key, icon, lbl in [
            ("dashboard", "◈", "Dashboard"),
            ("customers", "👤", "Customers"),
            ("orders",    "📋", "Orders"),
            ("payments",  "💰", "Payments"),
        ]:
            b = ctk.CTkButton(
                sb, text=f"  {icon}   {lbl}", anchor="w",
                fg_color="transparent", hover_color=DIM,
                text_color=MUTED, font=("Segoe UI", 13),
                height=44, corner_radius=10,
                command=lambda k=key: self.show(k)
            )
            b.pack(fill="x", padx=10, pady=3)
            self.nav[key] = b

        # Footer
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=16, pady=8, side="bottom")
        ctk.CTkLabel(sb, text="COMSATS University",
                     font=("Segoe UI", 10),
                     text_color="#1a2535").pack(side="bottom", pady=(0, 10))

    # ── CONTENT ──
    def _content(self):
        self.area = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.area.pack(side="right", fill="both", expand=True)
        self.pages = {}
        for n in ["dashboard", "customers", "orders", "payments"]:
            f = ctk.CTkFrame(self.area, fg_color=BG, corner_radius=0)
            f.place(relwidth=1, relheight=1)
            self.pages[n] = f
        self._dashboard()
        self._customers()
        self._orders()
        self._payments()

    def show(self, name):
        for k, b in self.nav.items():
            if k == name:
                b.configure(fg_color=DIM, text_color=CYAN)
            else:
                b.configure(fg_color="transparent", text_color=MUTED)
        self.pages[name].lift()
        if name == "dashboard":
            self._refresh_dash()

    # ── DASHBOARD ──
    def _dashboard(self):
        p = self.pages["dashboard"]

        hdr = ctk.CTkFrame(p, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(26, 0))
        heading(hdr, "Dashboard").pack(anchor="w")
        subheading(hdr, "Welcome back — here's your business at a glance").pack(anchor="w", pady=(3, 0))
        divider(p)

        # Stat cards
        row = ctk.CTkFrame(p, fg_color="transparent")
        row.pack(fill="x", padx=30, pady=(0, 20))
        self.sc = {}
        for title, icon, color in [
            ("Customers", "👥", CYAN),
            ("Orders",    "📋", GLOW),
            ("Revenue",   "💵", SUCCESS),
            ("Pending",   "⏳", WARN),
        ]:
            c = StatCard(row, icon, title, color=color)
            c.pack(side="left", expand=True, fill="both", padx=(0, 14))
            self.sc[title] = c

        # Recent orders card
        rc = card(p)
        rc.pack(fill="both", expand=True, padx=30, pady=(0, 26))

        rc_hdr = ctk.CTkFrame(rc, fg_color="transparent")
        rc_hdr.pack(fill="x", padx=20, pady=(16, 6))
        label(rc_hdr, "Recent Orders", size=14).pack(side="left")
        label(rc_hdr, "Last 5", color=MUTED).pack(side="right")
        ctk.CTkFrame(rc, height=1, fg_color=BORDER).pack(fill="x", padx=20, pady=(0, 10))

        self.dash_tbl = table_box(rc, 210)
        self.dash_tbl.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _refresh_dash(self):
        custs  = load_data(CUSTOMERS_FILE)
        orders = load_data(ORDERS_FILE)
        pays   = load_data(PAYMENTS_FILE)

        self.sc["Customers"].set(len(custs))
        self.sc["Orders"].set(len(orders))
        rev = sum(float(l.split("|")[3]) for l in pays
                  if len(l.split("|")) > 5 and l.split("|")[5] == "Paid")
        self.sc["Revenue"].set(f"Rs {rev:.0f}")
        pend = sum(1 for l in orders
                   if len(l.split("|")) > 4 and l.split("|")[4] in ["Pending", "In Progress"])
        self.sc["Pending"].set(pend)

        rows = []
        for line in list(reversed(orders))[:5]:
            p = line.split("|")
            if len(p) >= 5:
                rows.append([p[0], p[1], p[2], p[3], p[4]])
        fill_table(self.dash_tbl, rows,
                   ["Order ID", "Customer", "Dress Type", "Delivery", "Status"])

    # ── CUSTOMERS ──
    def _customers(self):
        p = self.pages["customers"]

        hdr = ctk.CTkFrame(p, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(26, 0))
        heading(hdr, "Customers").pack(anchor="w")
        subheading(hdr, "Manage client records and body measurements").pack(anchor="w", pady=(3, 0))
        divider(p)

        tb = tabs(p)
        tb.pack(fill="both", expand=True, padx=30, pady=(0, 26))
        tb.add("  ＋  Add  ")
        tb.add("  🔍  Search  ")
        tb.add("  ✏  Update  ")
        tb.add("  🗑  Delete  ")

        # ── Add ──
        af = tb.tab("  ＋  Add  ")
        g  = ctk.CTkFrame(af, fg_color="transparent")
        g.pack(fill="x", padx=10, pady=10)
        g.columnconfigure((0, 1), weight=1)

        self._ce = {}
        flds = [("Name","Full name","Contact","Phone number"),
                ("Chest","inches","Waist","inches"),
                ("Length","inches", None, None)]
        row = 0
        for f1, p1, f2, p2 in flds:
            label(g, f1).grid(row=row, column=0, sticky="w", padx=(10,4), pady=(10,2))
            e1 = entry(g, p1)
            e1.grid(row=row+1, column=0, sticky="ew", padx=(10,4), pady=(0,4))
            self._ce[f1] = e1
            if f2:
                label(g, f2).grid(row=row, column=1, sticky="w", padx=(4,10), pady=(10,2))
                e2 = entry(g, p2)
                e2.grid(row=row+1, column=1, sticky="ew", padx=(4,10), pady=(0,4))
                self._ce[f2] = e2
            row += 2

        self._cmsg = label(af, "", color=SUCCESS)
        self._cmsg.pack(anchor="w", padx=14, pady=(4, 2))

        def add_c():
            name    = self._ce["Name"].get().strip()
            contact = self._ce["Contact"].get().strip()
            chest   = self._ce["Chest"].get().strip()
            waist   = self._ce["Waist"].get().strip()
            length  = self._ce["Length"].get().strip()
            if not name or not contact:
                msg(self._cmsg, "Name and contact are required.", False)
                return
            cid  = next_id(CUSTOMERS_FILE, "C")
            line = "|".join([cid, name, contact, chest, waist, length])
            data = load_data(CUSTOMERS_FILE)
            data.append(line)
            save_data(CUSTOMERS_FILE, data)
            msg(self._cmsg, f"Customer added!  ID: {cid}")
            for e in self._ce.values(): e.delete(0, "end")

        btn_row = ctk.CTkFrame(af, fg_color="transparent")
        btn_row.pack(anchor="w", padx=14, pady=(4, 12))
        button(btn_row, "Save Customer", add_c).pack(side="left", padx=(0, 10))
        ghost_button(btn_row, "Clear", lambda: [e.delete(0,"end") for e in self._ce.values()], w=90).pack(side="left")


        # ── Search ──
        sf = tb.tab("  🔍  Search  ")
        sr = ctk.CTkFrame(sf, fg_color="transparent")
        sr.pack(fill="x", padx=10, pady=(12, 8))
        label(sr, "Search:").pack(side="left", padx=(10, 8))
        se = entry(sr, "Name or ID...")
        se.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self._ctbl = table_box(sf, 280)
        self._ctbl.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        def do_search():
            kw   = se.get().strip().lower()
            data = load_data(CUSTOMERS_FILE)
            rows = []
            for line in data:
                pts = line.split("|")
                if kw == "" or kw in pts[1].lower() or kw == pts[0].lower():
                    rows.append([pts[0], pts[1], pts[2],
                                 (pts[3] if len(pts) > 3 else "-") + '"',
                                 (pts[4] if len(pts) > 4 else "-") + '"',
                                 (pts[5] if len(pts) > 5 else "-") + '"'])
            fill_table(self._ctbl, rows, ["ID","Name","Contact","Chest","Waist","Length"])

        button(sr, "Search", do_search, w=90).pack(side="left")

        # ── Update ──
        uf = tb.tab("  ✏  Update  ")
        ui = ctk.CTkFrame(uf, fg_color="transparent")
        ui.pack(fill="x", padx=10, pady=12)
        label(ui, "Customer ID:").pack(anchor="w", padx=10, pady=(0, 4))
        uid_e = entry(ui, "e.g. C001", w=220)
        uid_e.pack(anchor="w", padx=10, pady=(0, 12))
        self._ue = {}
        for lbl, ph in [("Chest","new (inches)"),("Waist","new (inches)"),("Length","new (inches)")]:
            label(ui, lbl + ":").pack(anchor="w", padx=10, pady=(6, 2))
            e = entry(ui, ph, w=220)
            e.pack(anchor="w", padx=10, pady=(0, 4))
            self._ue[lbl] = e

        self._umsg = label(ui, "", color=SUCCESS)
        self._umsg.pack(anchor="w", padx=10, pady=4)

        def do_upd():
            cid  = uid_e.get().strip().upper()
            data = load_data(CUSTOMERS_FILE)
            for i in range(len(data)):
                pts = data[i].split("|")
                if pts[0] == cid:
                    c = self._ue["Chest"].get().strip()
                    w = self._ue["Waist"].get().strip()
                    l = self._ue["Length"].get().strip()
                    if c: pts[3] = c
                    if w: pts[4] = w
                    if l: pts[5] = l
                    data[i] = "|".join(pts)
                    save_data(CUSTOMERS_FILE, data)
                    msg(self._umsg, "Measurements updated!")
                    return
            msg(self._umsg, "Customer not found.", False)

        button(ui, "Update", do_upd, w=110).pack(anchor="w", padx=10, pady=(4,12))


        # ── Delete Customer ──
        dt = tb.tab("  🗑  Delete  ")
        di = ctk.CTkFrame(dt, fg_color="transparent")
        di.pack(fill="x", padx=10, pady=20)
        label(di, "Enter Customer ID to delete:").pack(anchor="w", padx=10, pady=(0,6))
        del_cid = entry(di, "e.g. C001", w=220)
        del_cid.pack(anchor="w", padx=10, pady=(0,14))
        self._cdelmsg = label(di, "", color=DANGER)
        self._cdelmsg.pack(anchor="w", padx=10, pady=(0,8))

        def del_c():
            cid  = del_cid.get().strip().upper()
            data = load_data(CUSTOMERS_FILE)
            new_data = [l for l in data if l.split("|")[0] != cid]
            if len(new_data) == len(data):
                msg(self._cdelmsg, "Customer not found.", False)
                return
            save_data(CUSTOMERS_FILE, new_data)
            msg(self._cdelmsg, f"Customer {cid} deleted successfully!", True)
            del_cid.delete(0, "end")

        button(di, "Delete Customer", del_c, color=DANGER, w=160).pack(anchor="w", padx=10)

    # ── ORDERS ──
    def _orders(self):
        p = self.pages["orders"]

        hdr = ctk.CTkFrame(p, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(26, 0))
        heading(hdr, "Orders").pack(anchor="w")
        subheading(hdr, "Create and track all stitching orders").pack(anchor="w", pady=(3, 0))
        divider(p)

        tb = tabs(p)
        tb.pack(fill="both", expand=True, padx=30, pady=(0, 26))
        tb.add("  ＋  Create  ")
        tb.add("  📋  View All  ")
        tb.add("  🔄  Status  ")
        tb.add("  ⏳  Pending  ")
        tb.add("  🗑  Delete  ")

        # ── Create ──
        cf = tb.tab("  ＋  Create  ")
        g  = ctk.CTkFrame(cf, fg_color="transparent")
        g.pack(fill="x", padx=10, pady=10)
        g.columnconfigure((0, 1), weight=1)

        self._oe = {}
        oflds = [("Customer ID","e.g. C001","Dress Type","e.g. Shalwar Kameez"),
                 ("Delivery Date","DD/MM/YYYY","Advance (Rs)","0 if none")]
        row = 0
        for f1, p1, f2, p2 in oflds:
            label(g, f1).grid(row=row, column=0, sticky="w", padx=(10,4), pady=(10,2))
            e1 = entry(g, p1)
            e1.grid(row=row+1, column=0, sticky="ew", padx=(10,4), pady=(0,4))
            self._oe[f1] = e1
            label(g, f2).grid(row=row, column=1, sticky="w", padx=(4,10), pady=(10,2))
            e2 = entry(g, p2)
            e2.grid(row=row+1, column=1, sticky="ew", padx=(4,10), pady=(0,4))
            self._oe[f2] = e2
            row += 2

        self._omsg = label(cf, "", color=SUCCESS)
        self._omsg.pack(anchor="w", padx=14, pady=(4,2))

        def do_create():
            cid      = self._oe["Customer ID"].get().strip().upper()
            dress    = self._oe["Dress Type"].get().strip()
            delivery = self._oe["Delivery Date"].get().strip()
            advance  = self._oe["Advance (Rs)"].get().strip() or "0"
            if not cid or not dress or not delivery:
                msg(self._omsg, "All fields are required.", False)
                return
            oid  = next_id(ORDERS_FILE, "O")
            line = "|".join([oid, cid, dress, delivery, "Pending", advance])
            data = load_data(ORDERS_FILE)
            data.append(line)
            save_data(ORDERS_FILE, data)
            msg(self._omsg, f"Order created!  ID: {oid}")
            for e in self._oe.values(): e.delete(0, "end")

        btn_row = ctk.CTkFrame(cf, fg_color="transparent")
        btn_row.pack(anchor="w", padx=14, pady=(4,12))
        button(btn_row, "Create Order", do_create).pack(side="left", padx=(0,10))
        ghost_button(btn_row, "Clear", lambda: [e.delete(0,"end") for e in self._oe.values()], w=90).pack(side="left")


        # ── View All ──
        vf = tb.tab("  📋  View All  ")
        self._otbl = table_box(vf, 300)
        self._otbl.pack(fill="both", expand=True, padx=12, pady=(12,8))

        def do_view():
            data = load_data(ORDERS_FILE)
            rows = []
            for line in reversed(data):
                pts = line.split("|")
                if len(pts) >= 5:
                    rows.append([pts[0], pts[1], pts[2], pts[3], pts[4]])
            fill_table(self._otbl, rows,
                       ["Order ID","Customer","Dress Type","Delivery","Status"])

        button(vf, "Refresh", do_view, w=100).pack(anchor="w", padx=12, pady=(0,8))

        # ── Status ──
        sf = tb.tab("  🔄  Status  ")
        si = ctk.CTkFrame(sf, fg_color="transparent")
        si.pack(fill="x", padx=10, pady=12)
        label(si, "Order ID:").pack(anchor="w", padx=10, pady=(0,4))
        s_oid = entry(si, "e.g. O001", w=220)
        s_oid.pack(anchor="w", padx=10, pady=(0,14))
        label(si, "New Status:").pack(anchor="w", padx=10, pady=(0,4))
        svar = ctk.StringVar(value="Pending")
        ctk.CTkOptionMenu(
            si, values=["Pending","In Progress","Ready","Delivered"],
            variable=svar, width=220, height=40,
            fg_color=CARD2, button_color=GLOW,
            button_hover_color=GLOW2,
            dropdown_fg_color=CARD2,
            dropdown_hover_color=DIM,
            font=("Segoe UI", 13), text_color=TEXT
        ).pack(anchor="w", padx=10, pady=(0,14))

        self._smsg = label(si, "", color=SUCCESS)
        self._smsg.pack(anchor="w", padx=10, pady=4)

        def do_status():
            oid  = s_oid.get().strip().upper()
            data = load_data(ORDERS_FILE)
            for i in range(len(data)):
                pts = data[i].split("|")
                if pts[0] == oid:
                    pts[4]   = svar.get()
                    data[i]  = "|".join(pts)
                    save_data(ORDERS_FILE, data)
                    msg(self._smsg, f"Status → {pts[4]}")
                    return
            msg(self._smsg, "Order not found.", False)

        button(si, "Update", do_status, w=110).pack(anchor="w", padx=10, pady=(4,12))

        # ── Pending ──
        pf = tb.tab("  ⏳  Pending  ")
        self._ptbl = table_box(pf, 300)
        self._ptbl.pack(fill="both", expand=True, padx=12, pady=(12,8))

        def do_pend():
            data = load_data(ORDERS_FILE)
            rows = []
            for line in data:
                pts = line.split("|")
                if len(pts) >= 5 and pts[4] in ["Pending","In Progress"]:
                    rows.append([pts[0], pts[1], pts[2], pts[3], pts[4]])
            fill_table(self._ptbl, rows,
                       ["Order ID","Customer","Dress Type","Due","Status"])

        button(pf, "Load Pending", do_pend, w=130).pack(anchor="w", padx=12, pady=(0,8))


        # ── Delete Order ──
        odt = tb.tab("  🗑  Delete  ")
        odi = ctk.CTkFrame(odt, fg_color="transparent")
        odi.pack(fill="x", padx=10, pady=20)
        label(odi, "Enter Order ID to delete:").pack(anchor="w", padx=10, pady=(0,6))
        del_oid = entry(odi, "e.g. O001", w=220)
        del_oid.pack(anchor="w", padx=10, pady=(0,14))
        self._odelmsg = label(odi, "", color=DANGER)
        self._odelmsg.pack(anchor="w", padx=10, pady=(0,8))

        def del_o():
            oid  = del_oid.get().strip().upper()
            data = load_data(ORDERS_FILE)
            new_data = [l for l in data if l.split("|")[0] != oid]
            if len(new_data) == len(data):
                msg(self._odelmsg, "Order not found.", False)
                return
            save_data(ORDERS_FILE, new_data)
            msg(self._odelmsg, f"Order {oid} deleted successfully!", True)
            del_oid.delete(0, "end")

        button(odi, "Delete Order", del_o, color=DANGER, w=140).pack(anchor="w", padx=10)

    # ── PAYMENTS ──
    def _payments(self):
        p = self.pages["payments"]

        hdr = ctk.CTkFrame(p, fg_color="transparent")
        hdr.pack(fill="x", padx=30, pady=(26, 0))
        heading(hdr, "Payments").pack(anchor="w")
        subheading(hdr, "Track revenue and outstanding balances").pack(anchor="w", pady=(3, 0))
        divider(p)

        # Summary cards
        sr = ctk.CTkFrame(p, fg_color="transparent")
        sr.pack(fill="x", padx=30, pady=(0, 16))
        self._psc = {}
        for title, icon, color in [
            ("Collected", "💵", SUCCESS),
            ("Outstanding", "⚠️", DANGER),
            ("Partial", "🔄", WARN),
        ]:
            c = StatCard(sr, icon, title, color=color)
            c.pack(side="left", expand=True, fill="both", padx=(0, 14))
            self._psc[title] = c

        tb = tabs(p)
        tb.pack(fill="both", expand=True, padx=30, pady=(0, 26))
        tb.add("  ＋  Add  ")
        tb.add("  🔍  View  ")
        tb.add("  📊  Revenue  ")
        tb.add("  🗑  Delete  ")

        # ── Add ──
        af = tb.tab("  ＋  Add  ")
        ai = ctk.CTkFrame(af, fg_color="transparent")
        ai.pack(fill="x", padx=10, pady=12)
        self._pe = {}
        for lbl, ph in [("Order ID","e.g. O001"),
                         ("Total Bill (Rs)","e.g. 3000"),
                         ("Amount Paid (Rs)","e.g. 2500")]:
            label(ai, lbl).pack(anchor="w", padx=10, pady=(6,2))
            e = entry(ai, ph, w=300)
            e.pack(anchor="w", padx=10, pady=(0,4))
            self._pe[lbl] = e

        self._paymsg = label(ai, "", color=SUCCESS)
        self._paymsg.pack(anchor="w", padx=10, pady=4)

        def do_pay():
            oid   = self._pe["Order ID"].get().strip().upper()
            tot   = self._pe["Total Bill (Rs)"].get().strip()
            paid  = self._pe["Amount Paid (Rs)"].get().strip()
            if not oid or not tot or not paid:
                msg(self._paymsg, "All fields are required.", False)
                return
            tot       = float(tot)
            paid      = float(paid)
            remaining = max(0, tot - paid)
            status    = "Paid" if remaining <= 0 else "Unpaid"
            pid  = next_id(PAYMENTS_FILE, "P")
            line = "|".join([pid, oid, str(tot), str(paid), str(remaining), status])
            data = load_data(PAYMENTS_FILE)
            data.append(line)
            save_data(PAYMENTS_FILE, data)
            msg(self._paymsg,
                f"Saved!   Remaining: Rs {remaining:.0f}   Status: {status}")
            for e in self._pe.values(): e.delete(0,"end")
            self._refresh_pay_summary()

        btn_row = ctk.CTkFrame(af, fg_color="transparent")
        btn_row.pack(anchor="w", padx=10, pady=(4,12))
        button(btn_row, "Record Payment", do_pay).pack(side="left", padx=(0,10))
        ghost_button(btn_row, "Clear", lambda: [e.delete(0,"end") for e in self._pe.values()], w=90).pack(side="left")


        # ── View ──
        vf  = tb.tab("  🔍  View  ")
        vr  = ctk.CTkFrame(vf, fg_color="transparent")
        vr.pack(fill="x", padx=10, pady=(12,8))
        label(vr, "Order ID:").pack(side="left", padx=(10,8))
        vp_oid = entry(vr, "e.g. O001", w=200)
        vp_oid.pack(side="left", padx=(0,8))

        self._vtbl = table_box(vf, 260)
        self._vtbl.pack(fill="both", expand=True, padx=12, pady=(0,8))

        def do_view_pay():
            oid  = vp_oid.get().strip().upper()
            data = load_data(PAYMENTS_FILE)
            rows = []
            for line in data:
                pts = line.split("|")
                if pts[1] == oid:
                    rows.append([pts[0], pts[1],
                                 f"Rs {float(pts[2]):.0f}",
                                 f"Rs {float(pts[3]):.0f}",
                                 f"Rs {float(pts[4]):.0f}",
                                 pts[5]])
            fill_table(self._vtbl, rows,
                       ["Pay ID","Order","Total","Paid","Remaining","Status"])

        button(vr, "Search", do_view_pay, w=90).pack(side="left")

        # ── Revenue ──
        rf = tb.tab("  📊  Revenue  ")
        self._rtbl = table_box(rf, 200)
        self._rtbl.pack(fill="x", padx=12, pady=(12,8))

        def do_rev():
            data = load_data(PAYMENTS_FILE)
            if not data:
                fill_table(self._rtbl, [])
                return
            billed = received = pending = 0
            for line in data:
                pts      = line.split("|")
                billed   += float(pts[2])
                received += float(pts[3])
                pending  += float(pts[4])
            fill_table(self._rtbl,
                       [["Total Billed",   f"Rs {billed:.2f}"],
                        ["Total Received", f"Rs {received:.2f}"],
                        ["Total Pending",  f"Rs {pending:.2f}"]],
                       ["Category", "Amount"])
            self._refresh_pay_summary()

        button(rf, "Calculate", do_rev, w=110).pack(anchor="w", padx=12, pady=(0,8))
        self._refresh_pay_summary()


        # ── Delete Payment ──
        pdt = tb.tab("  🗑  Delete  ")
        pdi = ctk.CTkFrame(pdt, fg_color="transparent")
        pdi.pack(fill="x", padx=10, pady=20)
        label(pdi, "Enter Payment ID to delete:").pack(anchor="w", padx=10, pady=(0,6))
        del_pid = entry(pdi, "e.g. P001", w=220)
        del_pid.pack(anchor="w", padx=10, pady=(0,14))
        self._pdelmsg = label(pdi, "", color=DANGER)
        self._pdelmsg.pack(anchor="w", padx=10, pady=(0,8))

        def del_p():
            pid  = del_pid.get().strip().upper()
            data = load_data(PAYMENTS_FILE)
            new_data = [l for l in data if l.split("|")[0] != pid]
            if len(new_data) == len(data):
                msg(self._pdelmsg, "Payment not found.", False)
                return
            save_data(PAYMENTS_FILE, new_data)
            msg(self._pdelmsg, f"Payment {pid} deleted successfully!", True)
            del_pid.delete(0, "end")
            self._refresh_pay_summary()

        button(pdi, "Delete Payment", del_p, color=DANGER, w=150).pack(anchor="w", padx=10)

    def _refresh_pay_summary(self):
        data = load_data(PAYMENTS_FILE)
        collected = partial = outstanding = 0
        for line in data:
            pts = line.split("|")
            if len(pts) < 6: continue
            if pts[5] == "Paid":   collected   += float(pts[3])
            elif pts[5] == "Unpaid": outstanding += float(pts[4])
            else:                  partial     += float(pts[4])
        self._psc["Collected"].set(f"Rs {collected:.0f}")
        self._psc["Outstanding"].set(f"Rs {outstanding:.0f}")
        self._psc["Partial"].set(f"Rs {partial:.0f}")


# ── RUN ──
if __name__ == "__main__":
    app = App()
    app.mainloop()
