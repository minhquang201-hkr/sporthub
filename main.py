import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


def format_vnd(amount: int) -> str:
    return f"{int(round(amount)):,}".replace(",", ".") + "đ"


class SportHubApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SportHub - Quản Lý Đặt Sân & Ghép Kèo Thể Thao")
        self.root.geometry("1100x700")
        self.root.minsize(1020, 650)
        self.root.configure(bg="#f1f5f9")

        self._setup_styles()
        self._init_mock_data()
        self._build_header()
        self._build_notebook()

        # Initial render
        self.render_courts_list()
        self.render_time_slots()
        self.calculate_split_bill()
        self.render_match_tree()
        self.render_owner_dashboard()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        base_font = ("Segoe UI", 10)
        bold_font = ("Segoe UI", 10, "bold")

        style.configure(".", font=base_font, background="#f1f5f9", foreground="#0f172a")
        style.configure("TNotebook", background="#f1f5f9", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=[16, 9],
            background="#e2e8f0",
            foreground="#475569",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#059669")],
            foreground=[("selected", "#ffffff")],
        )

        style.configure(
            "Primary.TButton",
            font=bold_font,
            background="#059669",
            foreground="#ffffff",
            padding=[12, 7],
            borderwidth=0,
        )
        style.map("Primary.TButton", background=[("active", "#047857"), ("disabled", "#cbd5e1")])

        style.configure(
            "Secondary.TButton",
            font=bold_font,
            background="#0f172a",
            foreground="#ffffff",
            padding=[10, 6],
            borderwidth=0,
        )
        style.map("Secondary.TButton", background=[("active", "#1e293b")])

        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#0f172a",
            rowheight=30,
            fieldbackground="#ffffff",
            font=("Segoe UI", 9),
        )
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e2e8f0", foreground="#0f172a")
        style.map("Treeview", background=[("selected", "#d1fae5")], foreground=[("selected", "#065f46")])

        style.configure("Green.Horizontal.TProgressbar", troughcolor="#e2e8f0", background="#10b981", thickness=18)

    def _init_mock_data(self):
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        day_after = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        self.available_dates = [today, tomorrow, day_after]
        self.hours = list(range(6, 22))
        self.peak_hours = {17, 18, 19, 20}
        self.platform_fee_rate = 0.02  # 2% phí sàn

        self.courts = [
            {
                "id": "FB-1",
                "name": "Sân 1 - Bóng đá 5 người",
                "sport": "Bóng đá",
                "base_price": 300000,
                "peak_price": 450000,
                "address": "Đường Z115, Quyết Thắng, TP. Thái Nguyên",
                "coords": "21.5847° N, 105.8065° E",
                "landmark": "Cách Đại học CNTT & TT (ICTU) 300m",
            },
            {
                "id": "FB-2",
                "name": "Sân 2 - Bóng đá 7 người",
                "sport": "Bóng đá",
                "base_price": 550000,
                "peak_price": 750000,
                "address": "Đường Quang Trung, P. Tân Thịnh, TP. Thái Nguyên",
                "coords": "21.5912° N, 105.8234° E",
                "landmark": "Gần Ngã tư Quang Trung - Phan Đình Phùng",
            },
            {
                "id": "BM-1",
                "name": "Sân 1 - Cầu lông Thảm",
                "sport": "Cầu lông",
                "base_price": 90000,
                "peak_price": 130000,
                "address": "Đường Lương Ngọc Quyến, TP. Thái Nguyên",
                "coords": "21.5941° N, 105.8390° E",
                "landmark": "Đối diện Nhà thi đấu Tỉnh Thái Nguyên",
            },
            {
                "id": "BM-2",
                "name": "Sân 2 - Cầu lông VIP",
                "sport": "Cầu lông",
                "base_price": 110000,
                "peak_price": 150000,
                "address": "KĐT Hồ Xương Rồng, P. Phan Đình Phùng, TP. Thái Nguyên",
                "coords": "21.5880° N, 105.8315° E",
                "landmark": "Cạnh Quảng trường Võ Nguyên Giáp 500m",
            },
            {
                "id": "PK-1",
                "name": "Sân 1 - Pickleball Mái che",
                "sport": "Pickleball",
                "base_price": 140000,
                "peak_price": 200000,
                "address": "Đường Bắc Kạn, P. Hoàng Văn Thụ, TP. Thái Nguyên",
                "coords": "21.6010° N, 105.8421° E",
                "landmark": "Cách Cầu Gia Bảy 400m về phía Bắc",
            },
            {
                "id": "PK-2",
                "name": "Sân 2 - Pickleball Ngoài trời",
                "sport": "Pickleball",
                "base_price": 120000,
                "peak_price": 180000,
                "address": "Đường Thống Nhất, P. Gia Sàng, TP. Thái Nguyên",
                "coords": "21.5725° N, 105.8492° E",
                "landmark": "Khu liên hợp Thể thao Gang Thép",
            },
            {
                "id": "PK-3",
                "name": "Sân 3 - Pickleball Thi đấu",
                "sport": "Pickleball",
                "base_price": 150000,
                "peak_price": 210000,
                "address": "Đường Z115, Quyết Thắng, TP. Thái Nguyên",
                "coords": "21.5850° N, 105.8070° E",
                "landmark": "Trong khuôn viên Tổ hợp SportHub Z115",
            },
        ]

        # Bookings with financial breakdown
        self.bookings = [
            self._make_booking("SH101", "FB-1", today, [18, 19], "FC Anh Em Q7", 900000, "VietQR", 50),
            self._make_booking("SH102", "FB-2", today, [19, 20], "CLB Thép Xanh", 1500000, "VietQR", 100),
            self._make_booking("SH103", "BM-1", today, [17, 18], "Nhóm Cầu Lông Sáng", 260000, "Tiền mặt", 30),
            self._make_booking("SH104", "PK-1", today, [8, 9], "Chị Lan & Team", 280000, "VietQR", 100),
            self._make_booking("SH105", "PK-2", today, [18, 19], "Pickleball Thái Nguyên", 360000, "Tiền mặt", 50),
            self._make_booking("SH106", "FB-1", tomorrow, [19, 20], "FC ICTU", 900000, "VietQR", 30),
        ]

        self.maintenance_slots = {
            ("BM-2", today, 12),
            ("PK-3", today, 13),
        }
        self.waiting_list = []

        # Booking tab state
        self.selected_court_id = self.courts[0]["id"]
        self.selected_date_var = tk.StringVar(value=today)
        self.selected_hours = set()
        self.customer_name_var = tk.StringVar(value="Minh Quang")
        self.customer_phone_var = tk.StringVar(value="0909 123 456")
        self.extra_fee_var = tk.StringVar(value="0")
        self.payment_method_var = tk.StringVar(value="VietQR")
        self.deposit_pct_var = tk.IntVar(value=30)
        self.last_confirmed_booking = self.bookings[0]

        # Split bill tab state
        self.split_court_fee_var = tk.StringVar(value="900000")
        self.split_count_var = tk.StringVar(value="6")
        self.split_code_var = tk.StringVar(value="SH101")
        self.split_players = [
            {"name": "Minh Quang (Host)", "paid": tk.BooleanVar(value=True), "method": tk.StringVar(value="Đã quét QR chuyển khoản")},
            {"name": "Hoàng Long", "paid": tk.BooleanVar(value=True), "method": tk.StringVar(value="Đã quét QR chuyển khoản")},
            {"name": "Đức Anh", "paid": tk.BooleanVar(value=False), "method": tk.StringVar(value="Nộp tiền mặt cho chủ phòng")},
            {"name": "Tuấn Kiệt", "paid": tk.BooleanVar(value=True), "method": tk.StringVar(value="Nộp tiền mặt cho chủ phòng")},
            {"name": "Gia Bảo", "paid": tk.BooleanVar(value=False), "method": tk.StringVar(value="Đã quét QR chuyển khoản")},
            {"name": "Quốc Trung", "paid": tk.BooleanVar(value=False), "method": tk.StringVar(value="Nộp tiền mặt cho chủ phòng")},
        ]

        # Matchmaking tab state
        self.matches = [
            {"id": "M01", "sport": "Bóng đá", "title": "Sân Z115 tối nay - thiếu hậu vệ", "time": "Hôm nay 19:30", "level": "Phong trào", "missing": 3, "fee": 110000},
            {"id": "M02", "sport": "Pickleball", "title": "Đánh đôi xoay tua đường Bắc Kạn", "time": "Ngày mai 18:00", "level": "Cơ bản", "missing": 2, "fee": 100000},
            {"id": "M03", "sport": "Cầu lông", "title": "Đánh đôi Lương Ngọc Quyến", "time": "Hôm nay 20:00", "level": "Bán chuyên", "missing": 1, "fee": 85000},
            {"id": "M04", "sport": "Bóng đá", "title": "Tuyển đối giao hữu sân Quang Trung", "time": "Thứ 6 18:00", "level": "Phong trào", "missing": 5, "fee": 90000},
            {"id": "M05", "sport": "Pickleball", "title": "Kèo sáng sớm nạp năng lượng", "time": "Ngày mai 06:30", "level": "Cơ bản", "missing": 4, "fee": 70000},
        ]

        self.owner_date_var = tk.StringVar(value=today)

    def _make_booking(self, bid, court_id, date_str, hours, customer, court_fee, payment_method, deposit_pct, phone="0909 123 456", extra_fee=0):
        platform_fee = round(court_fee * self.platform_fee_rate)
        total = court_fee + platform_fee + extra_fee
        deposit_paid = round(total * deposit_pct / 100)
        remaining_due = total - deposit_paid
        return {
            "id": bid,
            "court_id": court_id,
            "date": date_str,
            "hours": list(hours),
            "customer": customer,
            "phone": phone,
            "court_fee": court_fee,
            "platform_fee": platform_fee,
            "extra_fee": extra_fee,
            "total": total,
            "payment_method": payment_method,
            "deposit_pct": deposit_pct,
            "deposit_paid": deposit_paid,
            "remaining_due": remaining_due,
        }

    # ---------- HEADER ----------
    def _build_header(self):
        header = tk.Frame(self.root, bg="#0f172a", height=54)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        left = tk.Frame(header, bg="#0f172a")
        left.pack(side="left", padx=18, pady=10)
        tk.Label(left, text="SportHub", font=("Segoe UI", 16, "bold"), fg="#34d399", bg="#0f172a").pack(side="left")
        tk.Label(
            left,
            text="  |  Quản Lý Đặt Sân, Tài Chính & Ghép Kèo Thể Thao",
            font=("Segoe UI", 10),
            fg="#cbd5e1",
            bg="#0f172a",
        ).pack(side="left", pady=(3, 0))

        self.clock_label = tk.Label(header, text="", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#0f172a")
        self.clock_label.pack(side="right", padx=18)
        self._update_clock()

    def _update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))
        self.root.after(1000, self._update_clock)

    # ---------- NOTEBOOK ----------
    def _build_notebook(self):
        container = tk.Frame(self.root, bg="#f1f5f9")
        container.pack(fill="both", expand=True, padx=14, pady=10)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.tab_booking = tk.Frame(self.notebook, bg="#f1f5f9")
        self.tab_split = tk.Frame(self.notebook, bg="#f1f5f9")
        self.tab_match = tk.Frame(self.notebook, bg="#f1f5f9")
        self.tab_owner = tk.Frame(self.notebook, bg="#f1f5f9")

        self.notebook.add(self.tab_booking, text="  1. Đặt Sân  ")
        self.notebook.add(self.tab_split, text="  2. Chia Tiền  ")
        self.notebook.add(self.tab_match, text="  3. Ghép Kèo Giao Lưu  ")
        self.notebook.add(self.tab_owner, text="  4. Quản Trị Chủ Sân  ")

        self._build_tab_booking()
        self._build_tab_split()
        self._build_tab_match()
        self._build_tab_owner()

    # ==================== TAB 1: ĐẶT SÂN ====================
    def _build_tab_booking(self):
        self.tab_booking.columnconfigure(0, weight=4)
        self.tab_booking.columnconfigure(1, weight=7)
        self.tab_booking.rowconfigure(0, weight=1)

        # Left Column: Scrollable Court List with Address + Map button
        left_card = tk.Frame(self.tab_booking, bg="#ffffff", bd=1, relief="solid")
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        tk.Label(
            left_card,
            text="Danh sách Cụm Sân & Địa điểm",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#0f172a",
        ).pack(anchor="w", padx=12, pady=(10, 6))

        list_wrap = tk.Frame(left_card, bg="#ffffff")
        list_wrap.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        court_canvas = tk.Canvas(list_wrap, bg="#ffffff", highlightthickness=0)
        court_scroll = ttk.Scrollbar(list_wrap, orient="vertical", command=court_canvas.yview)
        self.courts_container = tk.Frame(court_canvas, bg="#ffffff")

        self.courts_container.bind("<Configure>", lambda e: court_canvas.configure(scrollregion=court_canvas.bbox("all")))
        court_canvas.create_window((0, 0), window=self.courts_container, anchor="nw")
        court_canvas.configure(yscrollcommand=court_scroll.set)

        court_canvas.pack(side="left", fill="both", expand=True)
        court_scroll.pack(side="right", fill="y")

        # Right Column: Date, Time Slots, Payment & Deposit Config
        right_card = tk.Frame(self.tab_booking, bg="#ffffff", bd=1, relief="solid")
        right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        top_bar = tk.Frame(right_card, bg="#ffffff")
        top_bar.pack(fill="x", padx=14, pady=(10, 6))

        tk.Label(top_bar, text="Chọn ngày:", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(side="left")
        date_combo = ttk.Combobox(
            top_bar,
            textvariable=self.selected_date_var,
            values=self.available_dates,
            state="readonly",
            width=13,
        )
        date_combo.pack(side="left", padx=(8, 12))
        date_combo.bind("<<ComboboxSelected>>", lambda e: self.on_date_change())

        legend = tk.Frame(top_bar, bg="#ffffff")
        legend.pack(side="right")
        for color, label in [("#10b981", "Trống"), ("#f97316", "Đang chọn"), ("#cbd5e1", "Đã đặt")]:
            box = tk.Frame(legend, bg=color, width=11, height=11)
            box.pack(side="left", padx=(8, 3))
            tk.Label(legend, text=label, font=("Segoe UI", 9), bg="#ffffff", fg="#475569").pack(side="left")

        self.booking_court_header = tk.Label(
            right_card,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc",
            fg="#059669",
            pady=6,
        )
        self.booking_court_header.pack(fill="x", padx=14, pady=(0, 6))

        # Time Slots Grid
        self.slots_frame = tk.Frame(right_card, bg="#ffffff")
        self.slots_frame.pack(fill="both", expand=True, padx=14, pady=2)

        # Payment & Deposit Panel (Bottom)
        pay_panel = tk.Frame(right_card, bg="#f8fafc", highlightbackground="#e2e8f0", highlightthickness=1, padx=12, pady=10)
        pay_panel.pack(fill="x", side="bottom", padx=14, pady=(6, 12))

        # Row 1: Payment Method & Deposit %
        opt_row = tk.Frame(pay_panel, bg="#f8fafc")
        opt_row.pack(fill="x", pady=(0, 6))

        tk.Label(opt_row, text="Hình thức:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").pack(side="left")
        tk.Radiobutton(
            opt_row,
            text="Chuyển khoản VietQR",
            variable=self.payment_method_var,
            value="VietQR",
            bg="#f8fafc",
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(6, 8))
        tk.Radiobutton(
            opt_row,
            text="Nộp tiền mặt tại quầy lễ tân",
            variable=self.payment_method_var,
            value="Tiền mặt",
            bg="#f8fafc",
            font=("Segoe UI", 9),
        ).pack(side="left")

        dep_row = tk.Frame(pay_panel, bg="#f8fafc")
        dep_row.pack(fill="x", pady=(0, 6))
        tk.Label(dep_row, text="Tỷ lệ đặt cọc:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").pack(side="left")
        for pct, txt in [(30, "Cọc 30%"), (50, "Cọc 50%"), (100, "Thanh toán 100%")]:
            tk.Radiobutton(
                dep_row,
                text=txt,
                variable=self.deposit_pct_var,
                value=pct,
                bg="#f8fafc",
                font=("Segoe UI", 9),
                command=self.update_booking_totals,
            ).pack(side="left", padx=(6, 6))

        tk.Label(dep_row, text="Khách:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").pack(side="left", padx=(8, 3))
        ttk.Entry(dep_row, textvariable=self.customer_name_var, width=12).pack(side="left")

        extra_row = tk.Frame(pay_panel, bg="#f8fafc")
        extra_row.pack(fill="x", pady=(0, 6))
        tk.Label(extra_row, text="SĐT:", font=("Segoe UI", 9, "bold"), bg="#f8fafc").pack(side="left")
        ttk.Entry(extra_row, textvariable=self.customer_phone_var, width=14).pack(side="left", padx=(6, 12))
        tk.Label(extra_row, text="Phụ phí nước/bóng/bib (đ):", font=("Segoe UI", 9, "bold"), bg="#f8fafc").pack(side="left")
        extra_entry = ttk.Entry(extra_row, textvariable=self.extra_fee_var, width=12)
        extra_entry.pack(side="left", padx=(6, 0))
        extra_entry.bind("<KeyRelease>", lambda e: self.update_booking_totals())

        # Row 3: Financial Breakdown & Confirm Button
        sum_row = tk.Frame(pay_panel, bg="#f8fafc")
        sum_row.pack(fill="x", pady=(4, 0))

        self.booking_breakdown_label = tk.Label(
            sum_row,
            text="Tiền sân: 0đ  +  Phí sàn (2%): 0đ  =  Tổng thanh toán: 0đ",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#f8fafc",
        )
        self.booking_breakdown_label.pack(anchor="w")

        bottom_action = tk.Frame(pay_panel, bg="#f8fafc")
        bottom_action.pack(fill="x", pady=(4, 0))

        self.booking_deposit_label = tk.Label(
            bottom_action,
            text="Tiền cọc cần trả trước (30%): 0đ",
            font=("Segoe UI", 11, "bold"),
            fg="#059669",
            bg="#f8fafc",
        )
        self.booking_deposit_label.pack(side="left")

        ttk.Button(
            bottom_action,
            text="Xác nhận đặt sân",
            style="Primary.TButton",
            command=self.confirm_booking,
        ).pack(side="right")

        ttk.Button(
            bottom_action,
            text="Xem & In Hóa Đơn",
            style="Secondary.TButton",
            command=lambda: self.open_single_invoice_modal(self.last_confirmed_booking),
        ).pack(side="right", padx=(0, 8))

    def get_court_by_id(self, court_id: str) -> dict:
        for c in self.courts:
            if c["id"] == court_id:
                return c
        return self.courts[0]

    def get_slot_price(self, court: dict, hour: int) -> int:
        return court["peak_price"] if hour in self.peak_hours else court["base_price"]

    def is_slot_booked(self, court_id: str, date_str: str, hour: int):
        for b in self.bookings:
            if b["court_id"] == court_id and b["date"] == date_str and hour in b["hours"]:
                return b
        return None

    def render_courts_list(self):
        for w in self.courts_container.winfo_children():
            w.destroy()

        for c in self.courts:
            is_selected = c["id"] == self.selected_court_id
            bg = "#ecfdf5" if is_selected else "#f8fafc"
            border_color = "#10b981" if is_selected else "#e2e8f0"

            row = tk.Frame(self.courts_container, bg=bg, highlightbackground=border_color, highlightthickness=1.5, pady=6, padx=8)
            row.pack(fill="x", pady=4)

            top = tk.Frame(row, bg=bg)
            top.pack(fill="x")
            tk.Label(top, text=c["name"], font=("Segoe UI", 9, "bold"), bg=bg, fg="#0f172a", anchor="w").pack(side="left", fill="x", expand=True)

            btn_text = "Đang chọn" if is_selected else "Chọn sân"
            btn_bg = "#059669" if is_selected else "#0f172a"
            tk.Button(
                top,
                text=btn_text,
                font=("Segoe UI", 8, "bold"),
                bg=btn_bg,
                fg="#ffffff",
                relief="flat",
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda cid=c["id"]: self.select_court(cid),
            ).pack(side="right")

            tk.Label(
                row,
                text=f"📍 {c['address']}",
                font=("Segoe UI", 8),
                bg=bg,
                fg="#334155",
                anchor="w",
            ).pack(fill="x", pady=(2, 1))

            bottom = tk.Frame(row, bg=bg)
            bottom.pack(fill="x")
            tk.Label(
                bottom,
                text=f"{c['sport']} | Thường: {format_vnd(c['base_price'])}/h | Vàng: {format_vnd(c['peak_price'])}/h",
                font=("Segoe UI", 8),
                bg=bg,
                fg="#64748b",
            ).pack(side="left")

            tk.Button(
                bottom,
                text="Xem vị trí / Bản đồ",
                font=("Segoe UI", 8, "bold"),
                bg="#e0f2fe",
                fg="#0369a1",
                relief="flat",
                padx=6,
                pady=1,
                cursor="hand2",
                command=lambda court=c: self.open_map_popup(court),
            ).pack(side="right")

    def open_map_popup(self, court: dict):
        popup = tk.Toplevel(self.root)
        popup.title(f"Vị trí & Chỉ dẫn — {court['name']}")
        popup.geometry("480x420")
        popup.resizable(False, False)
        popup.configure(bg="#ffffff")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(popup, text=court["name"], font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#0f172a").pack(anchor="w", padx=16, pady=(14, 2))
        tk.Label(popup, text=f"Địa chỉ: {court['address']}", font=("Segoe UI", 9), bg="#ffffff", fg="#334155").pack(anchor="w", padx=16)
        tk.Label(popup, text=f"Tọa độ GPS: {court['coords']}  •  {court['landmark']}", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#059669").pack(anchor="w", padx=16, pady=(2, 10))

        # Mini Schematic Map Canvas
        canvas = tk.Canvas(popup, width=448, height=230, bg="#ecfdf5", highlightbackground="#cbd5e1", highlightthickness=1)
        canvas.pack(padx=16, pady=4)

        # Roads
        canvas.create_line(0, 120, 448, 120, fill="#cbd5e1", width=18)
        canvas.create_line(220, 0, 220, 230, fill="#cbd5e1", width=16)
        canvas.create_line(0, 120, 448, 120, fill="#94a3b8", width=1, dash=(6, 4))
        canvas.create_line(220, 0, 220, 230, fill="#94a3b8", width=1, dash=(6, 4))

        # Road Labels
        canvas.create_text(110, 120, text=court["address"].split(",")[0], font=("Segoe UI", 8, "bold"), fill="#334155")
        canvas.create_text(220, 35, text="Trục chính TP. Thái Nguyên", font=("Segoe UI", 8), fill="#475569")

        # Landmark box
        canvas.create_rectangle(30, 30, 145, 70, fill="#dbeafe", outline="#3b82f6", width=1.5)
        canvas.create_text(87, 50, text="Điểm mốc gần nhất", font=("Segoe UI", 8, "bold"), fill="#1d4ed8")

        # Court Pin
        canvas.create_oval(285, 65, 325, 105, fill="#ef4444", outline="#ffffff", width=2)
        canvas.create_text(305, 85, text="★", font=("Segoe UI", 14, "bold"), fill="#ffffff")
        canvas.create_rectangle(245, 138, 385, 175, fill="#059669", outline="#047857")
        canvas.create_text(315, 156, text=court["id"] + " - SportHub", font=("Segoe UI", 9, "bold"), fill="#ffffff")

        # Direction arrow
        canvas.create_line(145, 70, 285, 85, fill="#f97316", width=2, arrow=tk.LAST, dash=(4, 2))

        btn_bar = tk.Frame(popup, bg="#ffffff")
        btn_bar.pack(fill="x", padx=16, pady=12)

        def copy_addr():
            self.root.clipboard_clear()
            self.root.clipboard_append(f"{court['address']} ({court['coords']})")
            messagebox.showinfo("Đã sao chép", "Đã sao chép địa chỉ & tọa độ sân vào clipboard!", parent=popup)

        ttk.Button(btn_bar, text="Sao chép địa chỉ", style="Secondary.TButton", command=copy_addr).pack(side="left")
        ttk.Button(btn_bar, text="Đóng", style="Primary.TButton", command=popup.destroy).pack(side="right")

    def select_court(self, court_id: str):
        self.selected_court_id = court_id
        self.selected_hours.clear()
        self.render_courts_list()
        self.render_time_slots()

    def on_date_change(self):
        self.selected_hours.clear()
        self.render_time_slots()

    def render_time_slots(self):
        for w in self.slots_frame.winfo_children():
            w.destroy()

        court = self.get_court_by_id(self.selected_court_id)
        date_str = self.selected_date_var.get()
        self.booking_court_header.config(text=f"{court['name']}  —  Ngày {date_str}")

        for idx, hour in enumerate(self.hours):
            r, col = divmod(idx, 4)
            self.slots_frame.columnconfigure(col, weight=1)
            self.slots_frame.rowconfigure(r, weight=1)

            booked = self.is_slot_booked(court["id"], date_str, hour)
            maint = (court["id"], date_str, hour) in self.maintenance_slots
            is_sel = hour in self.selected_hours
            price = self.get_slot_price(court, hour)
            label = f"{hour:02d}:00 - {hour + 1:02d}:00\n{format_vnd(price)}"

            if booked:
                btn = tk.Button(
                    self.slots_frame,
                    text=f"{hour:02d}:00 - {hour + 1:02d}:00\nĐã đặt ({booked['id']})",
                    font=("Segoe UI", 8, "bold"),
                    bg="#cbd5e1",
                    fg="#334155",
                    activebackground="#94a3b8",
                    activeforeground="#0f172a",
                    relief="flat",
                    cursor="hand2",
                    command=lambda h=hour, b=booked: self.on_booked_slot_click(court, date_str, h, b),
                )
            elif maint:
                btn = tk.Button(
                    self.slots_frame,
                    text=f"{hour:02d}:00 - {hour + 1:02d}:00\nBảo trì",
                    font=("Segoe UI", 8, "bold"),
                    bg="#fde68a",
                    fg="#92400e",
                    relief="flat",
                    state="disabled",
                )
            elif is_sel:
                btn = tk.Button(
                    self.slots_frame,
                    text=label,
                    font=("Segoe UI", 8, "bold"),
                    bg="#f97316",
                    fg="#ffffff",
                    activebackground="#ea580c",
                    activeforeground="#ffffff",
                    relief="flat",
                    cursor="hand2",
                    command=lambda h=hour: self.toggle_hour(h),
                )
            else:
                btn = tk.Button(
                    self.slots_frame,
                    text=label,
                    font=("Segoe UI", 8, "bold"),
                    bg="#10b981",
                    fg="#ffffff",
                    activebackground="#059669",
                    activeforeground="#ffffff",
                    relief="flat",
                    cursor="hand2",
                    command=lambda h=hour: self.toggle_hour(h),
                )

            btn.grid(row=r, column=col, sticky="nsew", padx=3, pady=3)

        self.update_booking_totals()

    def _get_extra_fee(self) -> int:
        try:
            return max(0, int(float(self.extra_fee_var.get())))
        except ValueError:
            return 0

    def update_booking_totals(self):
        court = self.get_court_by_id(self.selected_court_id)
        court_fee = sum(self.get_slot_price(court, h) for h in self.selected_hours)
        platform_fee = round(court_fee * self.platform_fee_rate)
        extra_fee = self._get_extra_fee() if self.selected_hours else 0
        total = court_fee + platform_fee + extra_fee
        pct = self.deposit_pct_var.get()
        deposit = round(total * pct / 100)

        extra_txt = f" + Phụ phí: {format_vnd(extra_fee)}" if extra_fee > 0 else ""
        self.booking_breakdown_label.config(
            text=f"Tiền sân: {format_vnd(court_fee)} + Phí sàn (2%): {format_vnd(platform_fee)}{extra_txt} = Tổng: {format_vnd(total)}"
        )
        self.booking_deposit_label.config(
            text=f"Tiền cọc cần trả trước ({pct}%): {format_vnd(deposit)}"
        )

    def toggle_hour(self, hour: int):
        if hour in self.selected_hours:
            self.selected_hours.remove(hour)
        else:
            self.selected_hours.add(hour)
        self.render_time_slots()

    def on_booked_slot_click(self, court: dict, date_str: str, hour: int, booking: dict):
        popup = tk.Toplevel(self.root)
        popup.title("Gợi ý thông minh — Ca đã có người đặt")
        popup.geometry("500x430")
        popup.resizable(False, False)
        popup.configure(bg="#ffffff")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(
            popup,
            text="Ca này đã có người đặt!",
            font=("Segoe UI", 13, "bold"),
            fg="#dc2626",
            bg="#ffffff",
        ).pack(anchor="w", padx=18, pady=(14, 2))

        tk.Label(
            popup,
            text=f"{court['name']}  •  {hour:02d}:00 - {hour + 1:02d}:00  •  Ngày {date_str}",
            font=("Segoe UI", 9, "bold"),
            fg="#334155",
            bg="#ffffff",
        ).pack(anchor="w", padx=18, pady=(0, 10))

        # Option 1: Waiting List
        wait_box = tk.Frame(popup, bg="#fffbeb", highlightbackground="#fcd34d", highlightthickness=1, padx=12, pady=10)
        wait_box.pack(fill="x", padx=18, pady=(0, 10))

        tk.Label(
            wait_box,
            text="1. Đăng ký vào Hàng chờ (Waiting List)",
            font=("Segoe UI", 10, "bold"),
            fg="#92400e",
            bg="#fffbeb",
        ).pack(anchor="w")
        tk.Label(
            wait_box,
            text="Nếu khách cũ hủy sân, hệ thống sẽ tự động thông báo ngay cho bạn.",
            font=("Segoe UI", 8),
            fg="#78350f",
            bg="#fffbeb",
        ).pack(anchor="w", pady=(2, 6))

        w_form = tk.Frame(wait_box, bg="#fffbeb")
        w_form.pack(fill="x")
        wait_name_var = tk.StringVar(value=self.customer_name_var.get() or "Minh Quang")
        wait_phone_var = tk.StringVar(value="0909 123 456")

        tk.Label(w_form, text="Tên:", font=("Segoe UI", 8, "bold"), bg="#fffbeb").pack(side="left")
        ttk.Entry(w_form, textvariable=wait_name_var, width=16).pack(side="left", padx=(4, 8))
        tk.Label(w_form, text="SĐT:", font=("Segoe UI", 8, "bold"), bg="#fffbeb").pack(side="left")
        ttk.Entry(w_form, textvariable=wait_phone_var, width=13).pack(side="left", padx=(4, 8))

        def join_waiting_list():
            name = wait_name_var.get().strip() or "Khách hàng"
            phone = wait_phone_var.get().strip() or "Chưa có SĐT"
            self.waiting_list.append({
                "court_id": court["id"],
                "date": date_str,
                "hour": hour,
                "customer": name,
                "phone": phone,
            })
            messagebox.showinfo(
                "Đã vào Hàng chờ",
                f"Đã đăng ký thành công cho {name} ({phone}) vào hàng chờ:\n{court['name']} lúc {hour:02d}:00 - {hour + 1:02d}:00 ({date_str}).",
                parent=popup,
            )
            popup.destroy()

        ttk.Button(w_form, text="Đăng ký chờ", style="Primary.TButton", command=join_waiting_list).pack(side="right")

        # Option 2: Other available courts at the same hour
        alt_box = tk.Frame(popup, bg="#f8fafc", highlightbackground="#cbd5e1", highlightthickness=1, padx=12, pady=10)
        alt_box.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        tk.Label(
            alt_box,
            text=f"2. Các sân khác còn trống lúc {hour:02d}:00 - {hour + 1:02d}:00",
            font=("Segoe UI", 10, "bold"),
            fg="#059669",
            bg="#f8fafc",
        ).pack(anchor="w", pady=(0, 6))

        same_sport_first = sorted(
            [c for c in self.courts if c["id"] != court["id"]],
            key=lambda c: (0 if c["sport"] == court["sport"] else 1, c["id"]),
        )
        available_alts = [
            c for c in same_sport_first
            if not self.is_slot_booked(c["id"], date_str, hour)
            and (c["id"], date_str, hour) not in self.maintenance_slots
        ]

        if not available_alts:
            tk.Label(
                alt_box,
                text="Rất tiếc, tất cả các sân khác đều đã kín hoặc đang bảo trì trong khung giờ này.",
                font=("Segoe UI", 9),
                fg="#64748b",
                bg="#f8fafc",
                wraplength=420,
            ).pack(anchor="w", pady=8)
        else:
            alt_list = tk.Frame(alt_box, bg="#f8fafc")
            alt_list.pack(fill="both", expand=True)
            for alt in available_alts[:4]:
                row = tk.Frame(alt_list, bg="#ffffff", highlightbackground="#e2e8f0", highlightthickness=1, padx=8, pady=5)
                row.pack(fill="x", pady=3)
                price = self.get_slot_price(alt, hour)
                tk.Label(
                    row,
                    text=f"{alt['name']} ({alt['sport']}) — {format_vnd(price)}",
                    font=("Segoe UI", 9, "bold"),
                    bg="#ffffff",
                    fg="#0f172a",
                ).pack(side="left")

                def pick_alt(cid=alt["id"]):
                    self.selected_court_id = cid
                    self.selected_hours = {hour}
                    self.render_courts_list()
                    self.render_time_slots()
                    popup.destroy()

                tk.Button(
                    row,
                    text="Chọn sân này",
                    font=("Segoe UI", 8, "bold"),
                    bg="#059669",
                    fg="#ffffff",
                    relief="flat",
                    padx=8,
                    pady=2,
                    cursor="hand2",
                    command=pick_alt,
                ).pack(side="right")

        ttk.Button(popup, text="Đóng", style="Secondary.TButton", command=popup.destroy).pack(anchor="e", padx=18, pady=(0, 12))

    def confirm_booking(self):
        if not self.selected_hours:
            messagebox.showwarning("Chưa chọn giờ", "Vui lòng chọn ít nhất 1 khung giờ trống.")
            return

        court = self.get_court_by_id(self.selected_court_id)
        date_str = self.selected_date_var.get()
        hours_sorted = sorted(self.selected_hours)
        court_fee = sum(self.get_slot_price(court, h) for h in hours_sorted)
        extra_fee = self._get_extra_fee()
        customer = self.customer_name_var.get().strip() or "Khách vãng lai"
        phone = self.customer_phone_var.get().strip() or "0900 000 000"
        payment_method = self.payment_method_var.get()
        deposit_pct = self.deposit_pct_var.get()
        new_id = f"SH{100 + len(self.bookings) + 1}"

        booking = self._make_booking(
            new_id, court["id"], date_str, hours_sorted, customer, court_fee, payment_method, deposit_pct, phone=phone, extra_fee=extra_fee
        )
        self.bookings.append(booking)
        self.last_confirmed_booking = booking
        self.selected_hours.clear()

        self.render_time_slots()
        self.render_owner_dashboard()
        self.split_court_fee_var.set(str(court_fee + extra_fee))
        self.split_code_var.set(new_id)
        self.calculate_split_bill()

        hours_str = ", ".join(f"{h:02d}:00-{h + 1:02d}:00" for h in hours_sorted)
        if messagebox.askyesno(
            "Đặt sân thành công",
            f"Mã đơn: {new_id}\nSân: {court['name']}\nNgày: {date_str} ({hours_str})\n"
            f"Hình thức: {payment_method} | Đã cọc ({deposit_pct}%): {format_vnd(booking['deposit_paid'])}\n"
            f"Còn lại tại quầy: {format_vnd(booking['remaining_due'])}\n\n"
            "Bạn có muốn Xem & In Hóa Đơn ngay bây giờ không?",
        ):
            self.open_single_invoice_modal(booking)

    # ==================== TAB 2: CHIA TIỀN ====================
    def _build_tab_split(self):
        self.tab_split.columnconfigure(0, weight=6)
        self.tab_split.columnconfigure(1, weight=4)
        self.tab_split.rowconfigure(0, weight=1)

        left_card = tk.Frame(self.tab_split, bg="#ffffff", bd=1, relief="solid")
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        tk.Label(left_card, text="Chia Tiền Sân (Tự động cộng 2% Phí dịch vụ)", font=("Segoe UI", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=16, pady=(12, 8))

        form = tk.Frame(left_card, bg="#ffffff")
        form.pack(fill="x", padx=16)

        tk.Label(form, text="Tiền sân (VNĐ):", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(form, textvariable=self.split_court_fee_var, width=18).grid(row=0, column=1, sticky="w", padx=8, pady=3)

        tk.Label(form, text="Số người chơi:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(form, textvariable=self.split_count_var, width=18).grid(row=1, column=1, sticky="w", padx=8, pady=3)

        ttk.Button(form, text="Tính tiền", style="Primary.TButton", command=self.calculate_split_bill).grid(row=0, column=2, rowspan=2, padx=8)

        self.split_fee_summary = tk.Label(
            left_card,
            text="Tiền sân: 0đ + Phí dịch vụ (2%): 0đ = Tổng hóa đơn: 0đ",
            font=("Segoe UI", 9, "bold"),
            fg="#475569",
            bg="#f8fafc",
            pady=6,
        )
        self.split_fee_summary.pack(fill="x", padx=16, pady=(8, 4))

        self.per_person_label = tk.Label(
            left_card,
            text="Mỗi người cần nộp: 0đ",
            font=("Segoe UI", 12, "bold"),
            fg="#059669",
            bg="#ecfdf5",
            pady=8,
        )
        self.per_person_label.pack(fill="x", padx=16, pady=(0, 8))

        prog_frame = tk.Frame(left_card, bg="#ffffff")
        prog_frame.pack(fill="x", padx=16, pady=(0, 8))
        self.split_progress_label = tk.Label(prog_frame, text="Tiến độ thu tiền: 0%", font=("Segoe UI", 9, "bold"), bg="#ffffff")
        self.split_progress_label.pack(anchor="w", pady=(0, 4))
        self.split_progressbar = ttk.Progressbar(prog_frame, style="Green.Horizontal.TProgressbar", maximum=100, value=0)
        self.split_progressbar.pack(fill="x")

        tk.Label(left_card, text="Danh sách thành viên, phương thức đóng & trạng thái:", font=("Segoe UI", 9, "bold"), fg="#475569", bg="#ffffff").pack(anchor="w", padx=16, pady=(4, 4))

        list_wrapper = tk.Frame(left_card, bg="#ffffff")
        list_wrapper.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        canvas = tk.Canvas(list_wrapper, bg="#f8fafc", highlightthickness=1, highlightbackground="#e2e8f0")
        scrollbar = ttk.Scrollbar(list_wrapper, orient="vertical", command=canvas.yview)
        self.split_players_frame = tk.Frame(canvas, bg="#f8fafc")

        self.split_players_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.split_players_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right: Bank Account Info
        right_card = tk.Frame(self.tab_split, bg="#ffffff", bd=1, relief="solid")
        right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        tk.Label(right_card, text="Thông tin Chuyển khoản Mẫu", font=("Segoe UI", 11, "bold"), bg="#ffffff").pack(anchor="w", padx=16, pady=(14, 8))

        bank_box = tk.Frame(right_card, bg="#f8fafc", highlightbackground="#cbd5e1", highlightthickness=1, padx=14, pady=14)
        bank_box.pack(fill="x", padx=16, pady=6)

        self.bank_info_labels = {}
        rows = [
            ("Ngân hàng:", "MB Bank (Ngân hàng Quân Đội)"),
            ("Số tài khoản:", "0345678901"),
            ("Chủ tài khoản:", "SPORTHUB"),
            ("Số tiền/người:", "0đ"),
            ("Nội dung CK:", "TIENSAN_SH101"),
        ]
        for idx, (k, v) in enumerate(rows):
            tk.Label(bank_box, text=k, font=("Segoe UI", 9), fg="#64748b", bg="#f8fafc").grid(row=idx, column=0, sticky="w", pady=5)
            lbl = tk.Label(bank_box, text=v, font=("Segoe UI", 9, "bold"), fg="#0f172a", bg="#f8fafc")
            lbl.grid(row=idx, column=1, sticky="e", padx=(10, 0), pady=5)
            self.bank_info_labels[k] = lbl
        bank_box.columnconfigure(1, weight=1)

        ttk.Button(
            right_card,
            text="Sao chép thông tin chuyển khoản",
            style="Secondary.TButton",
            command=self.copy_bank_info,
        ).pack(fill="x", padx=16, pady=(12, 6))

        ttk.Button(
            right_card,
            text="In Phiếu Chia Tiền Nhóm",
            style="Primary.TButton",
            command=self.open_group_invoice_modal,
        ).pack(fill="x", padx=16, pady=(0, 12))

    def calculate_split_bill(self):
        try:
            court_fee = max(0, int(float(self.split_court_fee_var.get())))
        except ValueError:
            court_fee = 0
        try:
            count = max(1, min(30, int(self.split_count_var.get())))
        except ValueError:
            count = 1
        self.split_count_var.set(str(count))

        service_fee = round(court_fee * self.platform_fee_rate)
        total_bill = court_fee + service_fee
        per_person = round(total_bill / count)

        self.split_fee_summary.config(
            text=f"Tiền sân: {format_vnd(court_fee)}  +  Phí dịch vụ (2%): {format_vnd(service_fee)}  =  Tổng hóa đơn: {format_vnd(total_bill)}"
        )
        self.per_person_label.config(text=f"Mỗi người cần nộp: {format_vnd(per_person)}")

        code = (self.split_code_var.get().strip() or "SH101").upper()
        self.bank_info_labels["Số tiền/người:"].config(text=format_vnd(per_person), fg="#059669")
        self.bank_info_labels["Nội dung CK:"].config(text=f"TIENSAN_{code}", fg="#2563eb")

        while len(self.split_players) < count:
            idx = len(self.split_players) + 1
            self.split_players.append({
                "name": f"Thành viên {idx}",
                "paid": tk.BooleanVar(value=False),
                "method": tk.StringVar(value="Đã quét QR chuyển khoản"),
            })
        if len(self.split_players) > count:
            self.split_players = self.split_players[:count]

        self._render_split_players(per_person)

    def _render_split_players(self, per_person: int):
        for w in self.split_players_frame.winfo_children():
            w.destroy()

        methods = ["Đã quét QR chuyển khoản", "Nộp tiền mặt cho chủ phòng"]
        for idx, p in enumerate(self.split_players):
            row = tk.Frame(self.split_players_frame, bg="#f8fafc", pady=4, padx=6)
            row.pack(fill="x")

            tk.Label(row, text=f"{idx + 1}. {p['name']}", font=("Segoe UI", 9, "bold"), bg="#f8fafc", width=18, anchor="w").pack(side="left")
            tk.Label(row, text=format_vnd(per_person), font=("Segoe UI", 9), fg="#475569", bg="#f8fafc", width=10).pack(side="left")

            ttk.Combobox(row, textvariable=p["method"], values=methods, state="readonly", width=24).pack(side="left", padx=6)

            status_text = "Đã nộp" if p["paid"].get() else "Chưa nộp"
            tk.Checkbutton(
                row,
                text=status_text,
                variable=p["paid"],
                font=("Segoe UI", 9, "bold"),
                fg="#059669" if p["paid"].get() else "#dc2626",
                bg="#f8fafc",
                activebackground="#f8fafc",
                command=lambda: self._update_split_progress(per_person),
            ).pack(side="right", padx=4)

        self._update_split_progress(per_person, redraw=False)

    def _update_split_progress(self, per_person: int, redraw: bool = True):
        total_players = len(self.split_players)
        paid_count = sum(1 for p in self.split_players if p["paid"].get())
        pct = round((paid_count / total_players) * 100) if total_players else 0
        self.split_progressbar["value"] = pct
        self.split_progress_label.config(text=f"Tiến độ thu tiền: {pct}% ({paid_count}/{total_players} người đã nộp)")
        if redraw:
            self._render_split_players(per_person)

    def copy_bank_info(self):
        amt = self.bank_info_labels["Số tiền/người:"].cget("text")
        content = self.bank_info_labels["Nội dung CK:"].cget("text")
        text = f"MB Bank - STK: 0345678901 - SPORTHUB - Số tiền: {amt} - Nội dung: {content}"
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Đã sao chép", f"Đã sao chép vào clipboard:\n{text}")

    # ==================== TAB 3: GHÉP KÈO GIAO LƯU ====================
    def _build_tab_match(self):
        self.tab_match.rowconfigure(0, weight=1)
        self.tab_match.columnconfigure(0, weight=1)

        wrapper = tk.Frame(self.tab_match, bg="#f1f5f9")
        wrapper.grid(row=0, column=0, sticky="nsew", pady=4)

        tree_card = tk.Frame(wrapper, bg="#ffffff", bd=1, relief="solid")
        tree_card.pack(fill="both", expand=True, pady=(0, 8))

        top_hdr = tk.Frame(tree_card, bg="#ffffff")
        top_hdr.pack(fill="x", padx=14, pady=(10, 6))
        tk.Label(top_hdr, text="Danh sách Kèo Giao Lưu & Tìm Đối Thủ", font=("Segoe UI", 11, "bold"), bg="#ffffff").pack(side="left")
        ttk.Button(top_hdr, text="Tham gia kèo đang chọn", style="Primary.TButton", command=self.join_selected_match).pack(side="right")

        columns = ("sport", "title", "time", "level", "missing", "fee")
        self.match_tree = ttk.Treeview(tree_card, columns=columns, show="headings", selectmode="browse")
        self.match_tree.heading("sport", text="Môn")
        self.match_tree.heading("title", text="Tiêu đề / Sân")
        self.match_tree.heading("time", text="Thời gian")
        self.match_tree.heading("level", text="Trình độ")
        self.match_tree.heading("missing", text="Còn thiếu")
        self.match_tree.heading("fee", text="Phí dự kiến")

        self.match_tree.column("sport", width=100, anchor="center")
        self.match_tree.column("title", width=290, anchor="w")
        self.match_tree.column("time", width=150, anchor="center")
        self.match_tree.column("level", width=120, anchor="center")
        self.match_tree.column("missing", width=110, anchor="center")
        self.match_tree.column("fee", width=110, anchor="e")

        scroll = ttk.Scrollbar(tree_card, orient="vertical", command=self.match_tree.yview)
        self.match_tree.configure(yscrollcommand=scroll.set)
        self.match_tree.pack(side="left", fill="both", expand=True, padx=(14, 0), pady=(0, 12))
        scroll.pack(side="right", fill="y", padx=(0, 14), pady=(0, 12))

        post_card = tk.Frame(wrapper, bg="#ffffff", bd=1, relief="solid", padx=14, pady=12)
        post_card.pack(fill="x")

        tk.Label(post_card, text="Đăng nhanh bài tìm người / ghép kèo mới", font=("Segoe UI", 10, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 8))

        self.new_match_sport = tk.StringVar(value="Bóng đá")
        self.new_match_title = tk.StringVar()
        self.new_match_time = tk.StringVar(value="Hôm nay 19:00")
        self.new_match_level = tk.StringVar(value="Phong trào")
        self.new_match_missing = tk.StringVar(value="2")

        tk.Label(post_card, text="Môn:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w")
        ttk.Combobox(post_card, textvariable=self.new_match_sport, values=["Bóng đá", "Cầu lông", "Pickleball"], state="readonly", width=12).grid(row=1, column=1, padx=(4, 12))

        tk.Label(post_card, text="Tiêu đề / Sân:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w")
        ttk.Entry(post_card, textvariable=self.new_match_title, width=28).grid(row=1, column=3, padx=(4, 12))

        tk.Label(post_card, text="Thời gian:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=1, column=4, sticky="w")
        ttk.Entry(post_card, textvariable=self.new_match_time, width=18).grid(row=1, column=5, padx=(4, 0))

        tk.Label(post_card, text="Trình độ:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Combobox(post_card, textvariable=self.new_match_level, values=["Cơ bản", "Phong trào", "Bán chuyên"], state="readonly", width=12).grid(row=2, column=1, padx=(4, 12), pady=(8, 0))

        tk.Label(post_card, text="Số người thiếu:", bg="#ffffff", font=("Segoe UI", 9, "bold")).grid(row=2, column=2, sticky="w", pady=(8, 0))
        ttk.Entry(post_card, textvariable=self.new_match_missing, width=10).grid(row=2, column=3, sticky="w", padx=(4, 12), pady=(8, 0))

        ttk.Button(post_card, text="Đăng bài mới", style="Primary.TButton", command=self.add_new_match).grid(row=2, column=4, columnspan=2, sticky="e", pady=(8, 0))

    def render_match_tree(self):
        for item in self.match_tree.get_children():
            self.match_tree.delete(item)
        for m in self.matches:
            missing_txt = f"{m['missing']} người" if m["missing"] > 0 else "Đã đủ người"
            self.match_tree.insert(
                "",
                "end",
                iid=m["id"],
                values=(m["sport"], m["title"], m["time"], m["level"], missing_txt, format_vnd(m["fee"])),
            )

    def join_selected_match(self):
        sel = self.match_tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn kèo", "Vui lòng chọn một kèo trong bảng để tham gia.")
            return
        mid = sel[0]
        for m in self.matches:
            if m["id"] == mid:
                if m["missing"] <= 0:
                    messagebox.showinfo("Hết chỗ", "Kèo này đã đủ người chơi.")
                    return
                m["missing"] -= 1
                self.render_match_tree()
                self.match_tree.selection_set(mid)
                messagebox.showinfo("Thành công", f"Bạn đã tham gia kèo '{m['title']}'!\nSố slot còn thiếu: {m['missing']}")
                return

    def add_new_match(self):
        title = self.new_match_title.get().strip()
        if not title:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tiêu đề hoặc tên sân.")
            return
        try:
            missing = max(1, int(self.new_match_missing.get()))
        except ValueError:
            missing = 2

        new_m = {
            "id": f"M{len(self.matches) + 1:02d}",
            "sport": self.new_match_sport.get(),
            "title": title,
            "time": self.new_match_time.get().strip() or "Hôm nay",
            "level": self.new_match_level.get(),
            "missing": missing,
            "fee": 80000,
        }
        self.matches.insert(0, new_m)
        self.new_match_title.set("")
        self.render_match_tree()
        messagebox.showinfo("Đăng bài thành công", "Bài ghép kèo mới đã được thêm vào danh sách.")

    # ==================== TAB 4: QUẢN TRỊ CHỦ SÂN ====================
    def _build_tab_owner(self):
        # Row 1: Main KPI Cards
        kpi_frame = tk.Frame(self.tab_owner, bg="#f1f5f9")
        kpi_frame.pack(fill="x", pady=(4, 6))
        for i in range(3):
            kpi_frame.columnconfigure(i, weight=1)

        self.kpi_rev_lbl = self._create_kpi_card(kpi_frame, 0, "Tổng Doanh thu ngày", "0đ", "#059669")
        self.kpi_cnt_lbl = self._create_kpi_card(kpi_frame, 1, "Tổng ca đã đặt", "0 ca", "#2563eb")
        self.kpi_occ_lbl = self._create_kpi_card(kpi_frame, 2, "Tỷ lệ lấp đầy sân", "0%", "#d97706")

        # Row 2: Financial Source Breakdown Cards
        fin_frame = tk.Frame(self.tab_owner, bg="#f1f5f9")
        fin_frame.pack(fill="x", pady=(0, 8))
        for i in range(3):
            fin_frame.columnconfigure(i, weight=1)

        self.fin_method_lbl = self._create_fin_card(fin_frame, 0, "Nguồn thu: Tiền mặt vs Chuyển khoản", "...")
        self.fin_deposit_lbl = self._create_fin_card(fin_frame, 1, "Tiền cọc đã giữ vs Còn nợ chưa thu", "...")
        self.fin_commission_lbl = self._create_fin_card(fin_frame, 2, "Phí hoa hồng sàn đã trích nộp (2%)", "0đ")

        # Matrix Card
        matrix_card = tk.Frame(self.tab_owner, bg="#ffffff", bd=1, relief="solid")
        matrix_card.pack(fill="both", expand=True, pady=(0, 4))

        top_bar = tk.Frame(matrix_card, bg="#ffffff")
        top_bar.pack(fill="x", padx=14, pady=(10, 6))
        tk.Label(
            top_bar,
            text="Ma trận trạng thái các sân theo khung giờ (Click ô để đổi: Trống → Đã đặt → Bảo trì)",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
        ).pack(side="left")

        date_box = ttk.Combobox(top_bar, textvariable=self.owner_date_var, values=self.available_dates, state="readonly", width=13)
        date_box.pack(side="right")
        date_box.bind("<<ComboboxSelected>>", lambda e: self.render_owner_dashboard())
        tk.Label(top_bar, text="Ngày:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side="right", padx=(0, 6))

        self.owner_matrix_frame = tk.Frame(matrix_card, bg="#ffffff")
        self.owner_matrix_frame.pack(fill="both", expand=True, padx=14, pady=(0, 12))

    def _create_kpi_card(self, parent, col, title, initial_val, color):
        card = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid", padx=14, pady=9)
        card.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 5, 0 if col == 2 else 5))
        tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#64748b", bg="#ffffff").pack(anchor="w")
        val_lbl = tk.Label(card, text=initial_val, font=("Segoe UI", 16, "bold"), fg=color, bg="#ffffff")
        val_lbl.pack(anchor="w", pady=(2, 0))
        return val_lbl

    def _create_fin_card(self, parent, col, title, initial_val):
        card = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid", padx=14, pady=8)
        card.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 5, 0 if col == 2 else 5))
        tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), fg="#475569", bg="#ffffff").pack(anchor="w")
        val_lbl = tk.Label(card, text=initial_val, font=("Segoe UI", 10, "bold"), fg="#0f172a", bg="#ffffff")
        val_lbl.pack(anchor="w", pady=(3, 0))
        return val_lbl

    def render_owner_dashboard(self):
        target_date = self.owner_date_var.get()
        day_bookings = [b for b in self.bookings if b["date"] == target_date]

        total_rev = sum(b["total"] for b in day_bookings)
        booked_slots = sum(len(b["hours"]) for b in day_bookings)
        total_slots = len(self.courts) * len(self.hours)
        occ_pct = round((booked_slots / total_slots) * 100) if total_slots else 0

        cash_rev = sum(b["total"] for b in day_bookings if b["payment_method"] == "Tiền mặt")
        qr_rev = sum(b["total"] for b in day_bookings if b["payment_method"] == "VietQR")
        deposit_held = sum(b["deposit_paid"] for b in day_bookings)
        remaining_debt = sum(b["remaining_due"] for b in day_bookings)
        platform_commission = sum(b["platform_fee"] for b in day_bookings)

        self.kpi_rev_lbl.config(text=format_vnd(total_rev))
        self.kpi_cnt_lbl.config(text=f"{len(day_bookings)} đơn ({booked_slots} giờ)")
        self.kpi_occ_lbl.config(text=f"{occ_pct}%")

        self.fin_method_lbl.config(text=f"Tiền mặt: {format_vnd(cash_rev)}  |  VietQR: {format_vnd(qr_rev)}", fg="#0f172a")
        self.fin_deposit_lbl.config(text=f"Đã cọc: {format_vnd(deposit_held)}  |  Còn nợ: {format_vnd(remaining_debt)}", fg="#b45309")
        self.fin_commission_lbl.config(text=f"{format_vnd(platform_commission)} (trích từ {len(day_bookings)} đơn)", fg="#7c3aed")

        for w in self.owner_matrix_frame.winfo_children():
            w.destroy()

        tk.Label(self.owner_matrix_frame, text="Sân / Giờ", font=("Segoe UI", 8, "bold"), bg="#e2e8f0", width=22, pady=5).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        for c_idx, h in enumerate(self.hours, start=1):
            self.owner_matrix_frame.columnconfigure(c_idx, weight=1)
            tk.Label(self.owner_matrix_frame, text=f"{h:02d}h", font=("Segoe UI", 8, "bold"), bg="#e2e8f0", pady=5).grid(row=0, column=c_idx, sticky="nsew", padx=1, pady=1)

        for r_idx, court in enumerate(self.courts, start=1):
            self.owner_matrix_frame.rowconfigure(r_idx, weight=1)
            tk.Label(
                self.owner_matrix_frame,
                text=court["name"],
                font=("Segoe UI", 8, "bold"),
                bg="#f8fafc",
                anchor="w",
                padx=6,
            ).grid(row=r_idx, column=0, sticky="nsew", padx=1, pady=1)

            for c_idx, h in enumerate(self.hours, start=1):
                booked = self.is_slot_booked(court["id"], target_date, h)
                maint = (court["id"], target_date, h) in self.maintenance_slots

                if booked:
                    bg, fg, txt = "#10b981", "#ffffff", booked["id"]
                elif maint:
                    bg, fg, txt = "#fbbf24", "#78350f", "Bảo trì"
                else:
                    bg, fg, txt = "#f1f5f9", "#64748b", "Trống"

                btn = tk.Button(
                    self.owner_matrix_frame,
                    text=txt,
                    font=("Segoe UI", 7, "bold"),
                    bg=bg,
                    fg=fg,
                    relief="flat",
                    cursor="hand2",
                    command=lambda cid=court["id"], hr=h: self.cycle_owner_slot(cid, target_date, hr),
                )
                btn.grid(row=r_idx, column=c_idx, sticky="nsew", padx=1, pady=1)

    def cycle_owner_slot(self, court_id: str, date_str: str, hour: int):
        court = self.get_court_by_id(court_id)
        price = self.get_slot_price(court, hour)
        booked = self.is_slot_booked(court_id, date_str, hour)
        maint_key = (court_id, date_str, hour)

        if booked:
            self._open_owner_booked_popup(court, date_str, hour, booked)
            return
        elif maint_key in self.maintenance_slots:
            self.maintenance_slots.remove(maint_key)
        else:
            new_id = f"SH{100 + len(self.bookings) + 1}"
            self.bookings.append(
                self._make_booking(new_id, court_id, date_str, [hour], "Khách tại quầy", price, "Tiền mặt", 100)
            )

        self.render_owner_dashboard()
        self.render_time_slots()

    def _open_owner_booked_popup(self, court: dict, date_str: str, hour: int, booked: dict):
        popup = tk.Toplevel(self.root)
        popup.title(f"Chi tiết đơn {booked['id']} — {court['id']}")
        popup.geometry("430x310")
        popup.resizable(False, False)
        popup.configure(bg="#ffffff")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(
            popup,
            text=f"Thông tin đặt sân ({booked['id']})",
            font=("Segoe UI", 12, "bold"),
            fg="#0f172a",
            bg="#ffffff",
        ).pack(anchor="w", padx=18, pady=(14, 8))

        info_box = tk.Frame(popup, bg="#f8fafc", highlightbackground="#cbd5e1", highlightthickness=1, padx=14, pady=12)
        info_box.pack(fill="x", padx=18)

        details = [
            ("Sân:", court["name"]),
            ("Ngày / Giờ:", f"{date_str}  •  {hour:02d}:00 - {hour + 1:02d}:00"),
            ("Khách hàng:", booked["customer"]),
            ("Hình thức:", booked["payment_method"]),
            ("Tổng tiền:", f"{format_vnd(booked['total'])} (Đã cọc {booked['deposit_pct']}%: {format_vnd(booked['deposit_paid'])})"),
            ("Còn nợ:", format_vnd(booked["remaining_due"])),
        ]
        for idx, (k, v) in enumerate(details):
            tk.Label(info_box, text=k, font=("Segoe UI", 9), fg="#64748b", bg="#f8fafc").grid(row=idx, column=0, sticky="w", pady=3)
            tk.Label(info_box, text=v, font=("Segoe UI", 9, "bold"), fg="#0f172a", bg="#f8fafc").grid(row=idx, column=1, sticky="w", padx=(10, 0), pady=3)

        def remove_hour_from_booking():
            price = self.get_slot_price(court, hour)
            booked["hours"].remove(hour)
            booked["court_fee"] = max(0, booked["court_fee"] - price)
            booked["platform_fee"] = round(booked["court_fee"] * self.platform_fee_rate)
            booked["total"] = booked["court_fee"] + booked["platform_fee"]
            booked["deposit_paid"] = round(booked["total"] * booked["deposit_pct"] / 100)
            booked["remaining_due"] = booked["total"] - booked["deposit_paid"]
            if not booked["hours"]:
                self.bookings.remove(booked)

        def cancel_to_available():
            remove_hour_from_booking()
            self.render_owner_dashboard()
            self.render_time_slots()
            popup.destroy()

            # Check Waiting List for notifications
            waiting = [
                w for w in self.waiting_list
                if w["court_id"] == court["id"] and w["date"] == date_str and w["hour"] == hour
            ]
            if waiting:
                names = ", ".join(f"{w['customer']} ({w['phone']})" for w in waiting)
                self.waiting_list = [
                    w for w in self.waiting_list
                    if not (w["court_id"] == court["id"] and w["date"] == date_str and w["hour"] == hour)
                ]
                messagebox.showinfo(
                    "Thông báo Hàng chờ!",
                    f"Ca {hour:02d}:00 - {hour + 1:02d}:00 tại {court['name']} đã trống!\n\nHệ thống đã gửi thông báo tới khách trong Hàng chờ:\n{names}",
                )
            else:
                messagebox.showinfo("Đã trả sân", f"Đã hủy ca {hour:02d}:00 - {hour + 1:02d}:00. Ô lịch đã chuyển về Trống (Xanh).")

        def move_to_maintenance():
            remove_hour_from_booking()
            self.maintenance_slots.add((court["id"], date_str, hour))
            self.render_owner_dashboard()
            self.render_time_slots()
            popup.destroy()

        btn_row = tk.Frame(popup, bg="#ffffff")
        btn_row.pack(fill="x", padx=18, pady=14)

        tk.Button(
            btn_row,
            text="Hủy / Trả sân (Về Trống)",
            font=("Segoe UI", 9, "bold"),
            bg="#dc2626",
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
            command=cancel_to_available,
        ).pack(side="left")

        tk.Button(
            btn_row,
            text="Bảo trì",
            font=("Segoe UI", 9, "bold"),
            bg="#f59e0b",
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
            command=move_to_maintenance,
        ).pack(side="left", padx=8)

        ttk.Button(btn_row, text="Đóng", style="Secondary.TButton", command=popup.destroy).pack(side="right")

    # ==================== INVOICE / RECEIPT MODAL ====================
    def open_single_invoice_modal(self, booking: dict):
        if not booking:
            messagebox.showwarning("Chưa có hóa đơn", "Vui lòng xác nhận đặt sân trước khi xem hóa đơn.")
            return

        court = self.get_court_by_id(booking["court_id"])
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        inv_code = f"SH-{booking['date'].replace('-', '')}-{booking['id']}"
        hours_sorted = sorted(booking["hours"])
        hours_str = ", ".join(f"{h:02d}:00-{h + 1:02d}:00" for h in hours_sorted)
        phone = booking.get("phone", "0909 123 456")
        extra_fee = booking.get("extra_fee", 0)

        lines = [
            "==========================================================",
            "         HÓA ĐƠN ĐẶT SÂN & DỊCH VỤ - SPORTHUB            ",
            "==========================================================",
            f"Mã hóa đơn   : {inv_code}",
            f"Ngày giờ in  : {now_str}",
            "----------------------------------------------------------",
            f"Khách hàng   : {booking['customer']}",
            f"Số điện thoại: {phone}",
            f"Cụm sân      : {court['name']} ({court['sport']})",
            f"Địa chỉ      : {court['address']}",
            f"Ngày chơi    : {booking['date']}",
            f"Khung giờ    : {hours_str} ({len(hours_sorted)} giờ)",
            "----------------------------------------------------------",
            "BẢNG KÊ CHI PHÍ:",
            f"  1. Tiền thuê sân ({len(hours_sorted)}h)          : {format_vnd(booking['court_fee']):>18}",
            f"  2. Phí dịch vụ hệ thống (2%)    : {format_vnd(booking['platform_fee']):>18}",
            f"  3. Phụ phí nước/bóng/áo bib     : {format_vnd(extra_fee):>18}",
            "----------------------------------------------------------",
            f"TỔNG CỘNG THANH TOÁN              : {format_vnd(booking['total']):>18}",
            "----------------------------------------------------------",
            f"Hình thức nộp: {booking['payment_method']}",
            f"Tỷ lệ đặt cọc: {booking['deposit_pct']}%  |  Đã cọc: {format_vnd(booking['deposit_paid'])}",
            f"CÒN LẠI PHẢI THANH TOÁN TẠI QUẦY  : {format_vnd(booking['remaining_due']):>18}",
            "==========================================================",
            "     Cảm ơn quý khách đã sử dụng dịch vụ SportHub!        ",
        ]
        self._show_invoice_modal(booking["id"], "\n".join(lines), title="Xem Trước Hóa Đơn Đặt Sân")

    def open_group_invoice_modal(self):
        try:
            court_fee = max(0, int(float(self.split_court_fee_var.get())))
        except ValueError:
            court_fee = 0
        count = max(1, len(self.split_players))
        service_fee = round(court_fee * self.platform_fee_rate)
        total_bill = court_fee + service_fee
        per_person = round(total_bill / count)

        code = (self.split_code_var.get().strip() or "SH101").upper()
        booking = next((b for b in self.bookings if b["id"] == code), self.bookings[0])
        court = self.get_court_by_id(booking["court_id"])
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        inv_code = f"SH-{datetime.now().strftime('%Y%m%d')}-NHOM-{code}"

        paid_count = sum(1 for p in self.split_players if p["paid"].get())
        host_name = self.customer_name_var.get().strip() or "Minh Quang"
        host_phone = self.customer_phone_var.get().strip() or "0909 123 456"

        lines = [
            "==========================================================",
            "    HÓA ĐƠN ĐẶT SÂN & DỊCH VỤ - SPORTHUB (CHIA NHÓM)      ",
            "==========================================================",
            f"Mã hóa đơn   : {inv_code}",
            f"Ngày giờ in  : {now_str}",
            f"Trưởng nhóm  : {host_name}  |  SĐT: {host_phone}",
            f"Sân thi đấu  : {court['name']} ({court['sport']})",
            f"Địa chỉ      : {court['address']}",
            f"Thành viên   : {paid_count}/{count} người đã hoàn thành đóng tiền",
            "----------------------------------------------------------",
            "BẢNG KÊ CHI PHÍ NHÓM:",
            f"  1. Tiền thuê sân                : {format_vnd(court_fee):>18}",
            f"  2. Phí dịch vụ tiện ích (2%)    : {format_vnd(service_fee):>18}",
            f"  TỔNG HÓA ĐƠN NHÓM               : {format_vnd(total_bill):>18}",
            f"  SỐ TIỀN MỖI NGƯỜI ({count} người)  : {format_vnd(per_person):>18}",
            "----------------------------------------------------------",
            "CHI TIẾT THÀNH VIÊN:",
        ]

        for idx, p in enumerate(self.split_players, start=1):
            if p["paid"].get():
                st = "Đã quét QR" if "QR" in p["method"].get() else "Đã nộp tiền mặt"
            else:
                st = "Chưa nộp"
            lines.append(f"  {idx:02d}. {p['name']:<20} | {format_vnd(per_person):>10} | {st}")

        lines.extend([
            "----------------------------------------------------------",
            "THÔNG TIN CHUYỂN KHOẢN CHỦ PHÒNG (VIETQR):",
            "  Ngân hàng : MB Bank (Quân Đội)",
            "  Số TK     : 0345678901  |  Chủ TK: SPORTHUB",
            f"  Nội dung  : TIENSAN_{code}  |  Số tiền: {format_vnd(per_person)}",
            f"  Link QR   : https://img.vietqr.io/image/MB-0345678901-compact2.png?amount={per_person}&addInfo=TIENSAN_{code}",
            "==========================================================",
        ])

        self._show_invoice_modal(f"NHOM_{code}", "\n".join(lines), title="Phiếu Chia Tiền Nhóm - SportHub")

    def _show_invoice_modal(self, invoice_id: str, receipt_text: str, title: str = "Hóa Đơn SportHub"):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("620x640")
        popup.resizable(False, False)
        popup.configure(bg="#e2e8f0")
        popup.transient(self.root)
        popup.grab_set()

        paper = tk.Frame(popup, bg="#ffffff", highlightbackground="#94a3b8", highlightthickness=2, padx=14, pady=12)
        paper.pack(fill="both", expand=True, padx=18, pady=(16, 10))

        text_box = tk.Text(
            paper,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#0f172a",
            relief="flat",
            wrap="none",
            padx=6,
            pady=6,
        )
        text_box.insert("1.0", receipt_text)
        text_box.config(state="disabled")

        scroll_y = ttk.Scrollbar(paper, orient="vertical", command=text_box.yview)
        text_box.configure(yscrollcommand=scroll_y.set)
        text_box.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        btn_bar = tk.Frame(popup, bg="#e2e8f0")
        btn_bar.pack(fill="x", padx=18, pady=(0, 14))

        def export_txt():
            filename = f"hoa_don_{invoice_id}.txt"
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(receipt_text)
            messagebox.showinfo("Xuất file thành công", f"Đã lưu hóa đơn tại:\n{filepath}", parent=popup)

        def print_bill():
            messagebox.showinfo(
                "In Hóa Đơn",
                f"Đã gửi hóa đơn ({invoice_id}) tới máy in mặc định của hệ thống!\nBạn cũng có thể xuất file .txt để lưu trữ.",
                parent=popup,
            )

        ttk.Button(btn_bar, text="Xuất file Text / Bill (.txt)", style="Secondary.TButton", command=export_txt).pack(side="left")
        ttk.Button(btn_bar, text="In Hóa Đơn", style="Primary.TButton", command=print_bill).pack(side="left", padx=8)
        ttk.Button(btn_bar, text="Đóng", style="Secondary.TButton", command=popup.destroy).pack(side="right")


if __name__ == "__main__":
    app_root = tk.Tk()
    SportHubApp(app_root)
    app_root.mainloop()
