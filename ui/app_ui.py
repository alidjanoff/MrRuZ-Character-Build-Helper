"""
ui.py — MuRuZ Character Build Helper
Premium dark-themed Tkinter GUI with background image, icon, glass panels, 
multi-language support, and optional VIT toggle.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import threading
import os
import sys

from logic.game_data import CLASS_LIST, HAS_CMD, BASE_STAT_VALUE, stat_names_for, total_stat_points
from logic.build_engine import validate_input, generate_builds
from core.locales import get_text
from core.app_config import VERSION

# ──────────────────────────────────────────────
# Premium color palette 
# ──────────────────────────────────────────────
BG_DARK       = "#0b0e17"
BG_PANEL      = "#101626"
BG_CARD       = "#141c30"
BG_INPUT      = "#0d1220"
BG_HOVER_ROW  = "#1a2540"
FG_TEXT        = "#d8dce8"
FG_DIM        = "#6b7a99"
FG_TITLE      = "#00d4ff"
FG_ACCENT     = "#00b4d8"
FG_GOLD       = "#f0c040"
FG_GREEN      = "#2ee89a"
FG_RED        = "#ff4d6a"
FG_SECTION    = "#7b8cde"
BTN_BG        = "#0077b6"
BTN_FG        = "#ffffff"
BTN_HOVER     = "#00a8e8"
BORDER_COLOR  = "#1e2d4a"
BORDER_ACCENT = "#00507a"
CARD_BORDER   = "#1a3050"
SEPARATOR     = "#1e2d4a"


def _resource_path(filename):
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


class MuRuZApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=BG_DARK)
        self.root.minsize(1050, 720)
        self.root.geometry("1120x820")

        self.lang_var = tk.StringVar(value="en")
        
        # State vars
        self.class_var = tk.StringVar(value=CLASS_LIST[0])
        self.info_var = tk.StringVar(value="")
        self.allow_vit_var = tk.BooleanVar(value=True)

        # Dynamic UI references
        self.ui_labels = {}
        self.ui_sections = {}
        
        try:
            icon_path = _resource_path("assets/icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        self.font_title    = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.font_subtitle = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.font_label    = tkfont.Font(family="Segoe UI", size=10)
        self.font_small    = tkfont.Font(family="Segoe UI", size=9)
        self.font_input    = tkfont.Font(family="Consolas", size=11)
        self.font_result   = tkfont.Font(family="Consolas", size=10)
        self.font_btn      = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.font_stat_val = tkfont.Font(family="Consolas", size=14, weight="bold")
        self.font_stat_lbl = tkfont.Font(family="Segoe UI", size=9, weight="bold")

        self.bg_image = None
        try:
            bg_path = _resource_path("assets/background.png")
            self.bg_image = tk.PhotoImage(file=bg_path)
        except Exception:
            pass

        self._build_ui()
        self._update_texts()

    def _get_lang(self):
        return self.lang_var.get()

    # ──────────────────────────────────────────
    # UI Construction
    # ──────────────────────────────────────────
    def _build_ui(self):
        if self.bg_image:
            bg_label = tk.Label(self.root, image=self.bg_image, bg=BG_DARK)
            bg_label.place(x=0, y=0, relwidth=1, relheight=0.45)

        # ── Header ──
        header = tk.Frame(self.root, bg=BG_DARK, pady=14)
        header.pack(fill="x")

        # Language selector at top right
        lang_frame = tk.Frame(header, bg=BG_DARK)
        lang_frame.pack(side="right", padx=20, anchor="n")
        lang_combo = ttk.Combobox(
            lang_frame, textvariable=self.lang_var, values=["en", "ru", "az"],
            state="readonly", width=4, font=self.font_label
        )
        lang_combo.pack()
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self._update_texts())

        self.ui_labels["app_title_sh"] = tk.Label(header, font=self.font_title, fg="#004060", bg=BG_DARK)
        self.ui_labels["app_title_sh"].pack()
        self.ui_labels["app_title_sh"].place(in_=header, relx=0.5, y=3, anchor="n")

        self.ui_labels["app_title"] = tk.Label(header, font=self.font_title, fg=FG_TITLE, bg=BG_DARK)
        self.ui_labels["app_title"].pack()

        self.ui_labels["app_sub"] = tk.Label(header, font=self.font_small, fg=FG_DIM, bg=BG_DARK)
        self.ui_labels["app_sub"].pack(pady=(0, 2))

        # ── Main ──
        main = tk.Frame(self.root, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=18, pady=(4, 18))
        main.columnconfigure(0, weight=2, minsize=350)
        main.columnconfigure(1, weight=5)
        main.rowconfigure(0, weight=1)

        self._build_input_panel(main)
        self._build_results_panel(main)

    def _build_input_panel(self, parent):
        panel = tk.Frame(parent, bg=BG_PANEL, bd=0, highlightbackground=BORDER_COLOR, highlightthickness=1)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        inner = tk.Frame(panel, bg=BG_PANEL, padx=18, pady=14)
        inner.pack(fill="both", expand=True)

        self._section_label(inner, "char_class")
        class_frame = tk.Frame(inner, bg=BG_PANEL)
        class_frame.pack(fill="x", pady=(0, 10))
        class_combo = ttk.Combobox(
            class_frame, textvariable=self.class_var, values=CLASS_LIST,
            state="readonly", font=self.font_input, width=24
        )
        class_combo.pack(anchor="w")
        class_combo.bind("<<ComboboxSelected>>", self._on_class_change)

        self._section_label(inner, "prog")
        prog_frame = tk.Frame(inner, bg=BG_PANEL)
        prog_frame.pack(fill="x", pady=(0, 6))

        self.reset_var, _ = self._labeled_entry(prog_frame, "rst", 0)
        self.level_var, _ = self._labeled_entry(prog_frame, "lvl", 1, default_val=1)

        self.ui_labels["info_pts"] = tk.Label(inner, textvariable=self.info_var, font=self.font_small,
                                              fg=FG_ACCENT, bg=BG_PANEL, wraplength=280, justify="left")
        self.ui_labels["info_pts"].pack(anchor="w", pady=(2, 8))
        self.reset_var.trace_add("write", self._update_info)
        self.level_var.trace_add("write", self._update_info)

        self._section_label(inner, "curr_stats")
        stats_frame = tk.Frame(inner, bg=BG_PANEL)
        stats_frame.pack(fill="x", pady=(0, 6))

        self.str_var, _ = self._labeled_entry(stats_frame, "STR", 0, is_stat=True)
        self.agi_var, _ = self._labeled_entry(stats_frame, "AGI", 1, is_stat=True)
        self.vit_var, _ = self._labeled_entry(stats_frame, "VIT", 2, is_stat=True)
        self.ene_var, _ = self._labeled_entry(stats_frame, "ENE", 3, is_stat=True)

        self.cmd_frame = tk.Frame(stats_frame, bg=BG_PANEL)
        tk.Label(self.cmd_frame, text="CMD", font=self.font_label, fg=FG_DIM, bg=BG_PANEL, width=16, anchor="w").pack(side="left")
        self.cmd_var = tk.StringVar(value=str(BASE_STAT_VALUE))
        tk.Entry(self.cmd_frame, textvariable=self.cmd_var, font=self.font_input, bg=BG_INPUT, fg=FG_TEXT,
                 width=10, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=BORDER_ACCENT).pack(side="left", padx=(0, 8))
        self.cmd_frame.grid(row=4, column=0, sticky="w", pady=3)
        self.cmd_frame.grid_remove()

        # ── Remaining Points ──
        rem_frame = tk.Frame(inner, bg=BG_PANEL)
        rem_frame.pack(fill="x", pady=(4, 6))
        self.remaining_var, self.lbl_rem = self._labeled_entry(rem_frame, "rem_pts", 0)

        # ── Optional VIT Toggle ──
        self.ui_labels["vit_opt"] = tk.Checkbutton(
            inner, text="Invest in Vitality (VIT)?\n(Uncheck if gear gives enough HP)", 
            variable=self.allow_vit_var, onvalue=True, offvalue=False,
            font=self.font_small, bg=BG_PANEL, fg=FG_ACCENT, selectcolor=BG_INPUT,
            activebackground=BG_PANEL, activeforeground=FG_ACCENT, justify="left"
        )
        self.ui_labels["vit_opt"].pack(anchor="w", pady=(0, 14))

        # ── Calculate Button ──
        btn_frame = tk.Frame(inner, bg=BG_PANEL)
        btn_frame.pack(fill="x")
        self.calc_btn = tk.Button(
            btn_frame, font=self.font_btn, bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_HOVER, activeforeground=BTN_FG,
            bd=0, padx=24, pady=11, cursor="hand2", relief="flat", command=self._on_calculate
        )
        self.calc_btn.pack(fill="x")
        self.calc_btn.bind("<Enter>", lambda e: self.calc_btn.config(bg=BTN_HOVER))
        self.calc_btn.bind("<Leave>", lambda e: self.calc_btn.config(bg=BTN_BG))

    def _build_results_panel(self, parent):
        panel = tk.Frame(parent, bg=BG_PANEL, bd=0, highlightbackground=BORDER_COLOR, highlightthickness=1)
        panel.grid(row=0, column=1, sticky="nsew")

        header = tk.Frame(panel, bg=BG_PANEL, padx=18, pady=10)
        header.pack(fill="x")
        self.ui_labels["recs"] = tk.Label(header, font=self.font_subtitle, fg=FG_GOLD, bg=BG_PANEL)
        self.ui_labels["recs"].pack(anchor="w")
        tk.Frame(header, bg=SEPARATOR, height=1).pack(fill="x", pady=(6, 0))

        canvas_frame = tk.Frame(panel, bg=BG_PANEL)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=BG_PANEL, highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.results_inner = tk.Frame(self.canvas, bg=BG_PANEL)

        self.results_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.results_inner, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.placeholder = tk.Label(self.results_inner, font=self.font_label, fg=FG_DIM, bg=BG_PANEL, justify="left")
        self.placeholder.pack(padx=24, pady=60)

    # ──────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────
    def _update_texts(self):
        l = self._get_lang()
        app_title = get_text(l, "app_title")
        full_title = f"{app_title} - v{VERSION}"
        
        self.root.title(full_title)
        self.ui_labels["app_title_sh"].config(text=app_title)
        self.ui_labels["app_title"].config(text=app_title)
        self.ui_labels["app_sub"].config(text=get_text(l, "app_sub"))
        self.ui_labels["recs"].config(text=get_text(l, "recs"))
        self.ui_labels["vit_opt"].config(text=get_text(l, "vit_opt"))
        self.calc_btn.config(text=get_text(l, "calc_btn"))
        
        # Clear results panel so old language builds don't show
        for w in self.results_inner.winfo_children():
            w.destroy()
            
        # Re-create the placeholder in the new language
        self.placeholder = tk.Label(self.results_inner, font=self.font_label, fg=FG_DIM, bg=BG_PANEL, justify="left")
        self.placeholder.pack(padx=24, pady=60)
        self.placeholder.config(text=get_text(l, "placeholder"))

        for key, lbl in self.ui_sections.items():
            if key in ("STR", "AGI", "VIT", "ENE", "CMD"):
                lbl.config(text=key)
            else:
                lbl.config(text=get_text(l, key))
                
        self._update_info()

    def _section_label(self, parent, key):
        frame = tk.Frame(parent, bg=BG_PANEL)
        frame.pack(fill="x", pady=(10, 4))
        lbl = tk.Label(frame, font=self.font_stat_lbl, fg=FG_SECTION, bg=BG_PANEL)
        lbl.pack(side="left")
        self.ui_sections[key] = lbl
        tk.Frame(frame, bg=BORDER_COLOR, height=1).pack(side="left", fill="x", expand=True, padx=(10, 0), pady=1)

    def _labeled_entry(self, parent, key, row, is_stat=False, default_val=None):
        lbl = tk.Label(parent, font=self.font_label, fg=FG_DIM, bg=BG_PANEL, width=16, anchor="w")
        lbl.grid(row=row, column=0, sticky="w", pady=3)
        self.ui_sections[key] = lbl
        
        if default_val is not None:
            default = str(default_val)
        else:
            default = str(BASE_STAT_VALUE) if is_stat else "0"
            
        var = tk.StringVar(value=default)
        tk.Entry(parent, textvariable=var, font=self.font_input, bg=BG_INPUT, fg=FG_TEXT, insertbackground=FG_ACCENT,
                 width=10, bd=0, highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=BORDER_ACCENT).grid(row=row, column=1, sticky="w", padx=(0, 8), pady=3)
        return var, lbl

    def _on_class_change(self, event=None):
        cls = self.class_var.get()
        if HAS_CMD[cls]:
            self.cmd_frame.grid()
        else:
            self.cmd_frame.grid_remove()
        self._update_info()

    def _update_info(self, *_args):
        try:
            cls = self.class_var.get()
            lvl = int(self.level_var.get() or 0)
            rst = int(self.reset_var.get() or 0)
            if 1 <= lvl <= 400 and rst >= 0:
                pts = total_stat_points(cls, lvl, rst)
                self.info_var.set(get_text(self._get_lang(), "info_pts", pts=pts))
            else:
                self.info_var.set("")
        except ValueError:
            self.info_var.set("")

    def _safe_int(self, var, default=0):
        try:
            return int(var.get())
        except ValueError:
            return default

    # ──────────────────────────────────────────
    # Calculation
    # ──────────────────────────────────────────
    def _on_calculate(self):
        cls  = self.class_var.get()
        lang = self._get_lang()

        resets    = self._safe_int(self.reset_var, -1)
        level     = self._safe_int(self.level_var, -1)
        str_v     = self._safe_int(self.str_var, -1)
        agi_v     = self._safe_int(self.agi_var, -1)
        vit_v     = self._safe_int(self.vit_var, -1)
        ene_v     = self._safe_int(self.ene_var, -1)
        cmd_v     = self._safe_int(self.cmd_var, BASE_STAT_VALUE) if HAS_CMD[cls] else BASE_STAT_VALUE
        remaining = self._safe_int(self.remaining_var, -1)

        for name, val in [("rst", resets), ("lvl", level), ("STR", str_v),
                          ("AGI", agi_v), ("VIT", vit_v), ("ENE", ene_v),
                          ("rem_pts", remaining)]:
            if val < 0:
                name_loc = get_text(lang, name) if name in ("rst", "lvl", "rem_pts") else name
                messagebox.showerror(get_text(lang, "warn_title"), get_text(lang, "err_num", name=name_loc))
                return

        stats_dict = {"str": str_v, "agi": agi_v, "vit": vit_v, "ene": ene_v}
        if HAS_CMD[cls]:
            stats_dict["cmd"] = cmd_v

        valid, err, bonus = validate_input(cls, resets, level, stats_dict, remaining, lang=lang)
        if not valid:
            messagebox.showwarning(get_text(lang, "warn_title"), get_text(lang, "warn_msg", err=err))

        self.calc_btn.config(state="disabled", text=get_text(lang, "calc_loading"))
        self.root.update_idletasks()

        def run():
            builds = generate_builds(
                cls, level, resets, bonus_points=bonus, 
                allow_vit=self.allow_vit_var.get(), lang=lang
            )
            self.root.after(0, lambda: self._display_results(builds))

        threading.Thread(target=run, daemon=True).start()

    # ──────────────────────────────────────────
    # Results display
    # ──────────────────────────────────────────
    def _display_results(self, builds):
        self.calc_btn.config(state="normal", text=get_text(self._get_lang(), "calc_btn"))

        for w in self.results_inner.winfo_children():
            w.destroy()

        cls = self.class_var.get()
        snames = stat_names_for(cls)

        for build in builds:
            self._render_build_card(build, snames)

        self.canvas.yview_moveto(0)

    def _render_build_card(self, build, snames):
        type_colors = {
            "farm": {"accent": "#2ee89a", "border": "#1a4a3a"},
            "pve":  {"accent": "#5b9fff", "border": "#1a2e5a"},
            "pvp":  {"accent": "#ff5c7c", "border": "#4a1a2a"},
        }
        tc = type_colors.get(build["type"], type_colors["farm"])
        lang = self._get_lang()

        card = tk.Frame(self.results_inner, bg=BG_CARD, bd=0, highlightbackground=tc["border"], highlightthickness=1)
        card.pack(fill="x", padx=14, pady=8)

        inner = tk.Frame(card, bg=BG_CARD, padx=18, pady=14)
        inner.pack(fill="x")

        header_frame = tk.Frame(inner, bg=BG_CARD)
        header_frame.pack(fill="x")

        tk.Label(header_frame, text=build["label"], font=self.font_subtitle, fg=tc["accent"], bg=BG_CARD).pack(side="left")
        tk.Label(header_frame, text=f"  ·  {build['focus']}", font=self.font_small, fg=FG_DIM, bg=BG_CARD).pack(side="left", padx=(4, 0))

        stat_row = tk.Frame(inner, bg=BG_CARD)
        stat_row.pack(fill="x", pady=(10, 8))

        for sn in snames:
            val = build["stats"][sn]
            box = tk.Frame(stat_row, bg=BG_DARK, padx=12, pady=8, highlightbackground=BORDER_COLOR, highlightthickness=1)
            box.pack(side="left", padx=(0, 6), fill="x", expand=True)

            tk.Label(box, text=sn.upper(), font=self.font_stat_lbl, fg=FG_DIM, bg=BG_DARK).pack()
            tk.Label(box, text=f"{val:,}", font=self.font_stat_val, fg=FG_GREEN, bg=BG_DARK).pack()

        tk.Frame(inner, bg=SEPARATOR, height=1).pack(fill="x", pady=(6, 8))

        tk.Label(inner, text=get_text(lang, "analysis"), font=self.font_stat_lbl, fg=FG_SECTION, bg=BG_CARD).pack(anchor="w")

        exp_text = tk.Text(inner, font=self.font_result, bg=BG_DARK, fg=FG_TEXT, wrap="word", bd=0, highlightthickness=0,
                           height=self._text_height(build["explanation"]), padx=10, pady=8, selectbackground=BORDER_ACCENT)
        exp_text.pack(fill="x", pady=(4, 0))
        exp_text.insert("1.0", build["explanation"])
        exp_text.config(state="disabled")

    def _text_height(self, text):
        return min(max(text.count("\n") + 1, 8), 22)


def run_app():
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground=BG_INPUT, background=BG_INPUT, foreground=FG_TEXT, selectbackground=BG_CARD, selectforeground=FG_TEXT, arrowcolor=FG_ACCENT, bordercolor=BORDER_COLOR, lightcolor=BORDER_COLOR, darkcolor=BORDER_COLOR)
    style.map("TCombobox", fieldbackground=[("readonly", BG_INPUT)], selectbackground=[("readonly", BG_CARD)], bordercolor=[("focus", BORDER_ACCENT)], lightcolor=[("focus", BORDER_ACCENT)])
    style.configure("Vertical.TScrollbar", background=BG_PANEL, troughcolor=BG_DARK, arrowcolor=FG_DIM, bordercolor=BG_DARK, lightcolor=BG_PANEL, darkcolor=BG_DARK)
    style.map("Vertical.TScrollbar", background=[("active", BORDER_ACCENT)])

    app = MuRuZApp(root)
    root.mainloop()
