import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN STREAMLIT ---
st.set_page_config(
    page_title="Ôn Tập Từ Vựng - Bài 1: Tổng Quan Nhà Máy",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CƠ SỞ DỮ LIỆU CHUẨN 20 TỪ CỐT LÕI (BÀI 1) ---
VOCAB_DATA = [
    # Nhóm 1: Cơ sở hạ tầng & Phân khu xưởng
    {
        "id": 1, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Cơ sở hạ tầng & Phân khu",
        "word": "工厂", "pinyin": "gōngchǎng", "meaning": "Nhà máy, công xưởng",
        "collocations": ["参观工厂 (Tham quan xưởng)", "工厂规模 (Quy mô xưởng)", "现代化工厂 (Nhà máy hiện đại)"],
        "example": "欢迎各位领导来我们工厂参观考察。\n(Hoan nghênh các vị lãnh đạo đến tham quan khảo sát nhà máy chúng tôi.)"
    },
    {
        "id": 2, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Cơ sở hạ tầng & Phân khu",
        "word": "车间", "pinyin": "chējiān", "meaning": "Phân xưởng, nhà xưởng sản xuất",
        "collocations": ["生产车间 (Xưởng sản xuất)", "无尘车间 (Phòng sạch)", "总装车间 (Xưởng lắp ráp tổng)"],
        "example": "进入生产车间之前，所有人必须戴好安全帽。\n(Trước khi vào xưởng sản xuất, tất cả mọi người phải đội mũ bảo hộ.)"
    },
    {
        "id": 3, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Cơ sở hạ tầng & Phân khu",
        "word": "办公大楼", "pinyin": "bàngōng dàlóu", "meaning": "Tòa nhà văn phòng hành chính",
        "collocations": ["行政大楼 (Tòa nhà hành chính)", "佩戴厂牌 (Đeo thẻ nhà máy)", "总经办 (Văn phòng Tổng giám đốc)"],
        "example": "所有的行政部门都在这栋三层办公大楼里面。\n(Tất cả các phòng ban hành chính đều làm việc trong tòa văn phòng 3 tầng này.)"
    },
    {
        "id": 4, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Cơ sở hạ tầng & Phân khu",
        "word": "仓库", "pinyin": "cāngkù", "meaning": "Kho bãi",
        "collocations": ["原料仓库 (Kho nguyên liệu)", "成品仓库 (Kho thành phẩm)", "月底盘点 (Kiểm kê cuối tháng)"],
        "example": "原料仓库在工厂东侧，靠近卸货平台。\n(Kho nguyên liệu nằm ở phía đông nhà máy, sát ngay sàn bốc dỡ hàng.)"
    },
    {
        "id": 5, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Cơ sở hạ tầng & Phân khu",
        "word": "设备", "pinyin": "shèbèi", "meaning": "Thiết bị, máy móc",
        "collocations": ["先进设备 (Thiết bị tiên tiến)", "自动化设备 (Thiết bị tự động)", "数控机床 (Máy CNC)"],
        "example": "车间里大部分生产设备都是从德国引进的。\n(Phần lớn thiết bị sản xuất trong xưởng đều được nhập khẩu từ Đức.)"
    },
    {
        "id": 6, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Cơ sở hạ tầng & Phân khu",
        "word": "流水线", "pinyin": "liúshuǐxiàn", "meaning": "Dây chuyền sản xuất lắp ráp",
        "collocations": ["自动化流水线 (Dây chuyền tự động)", "流水线作业 (Thao tác trên chuyền)", "流水线装配 (Lắp ráp dây chuyền)"],
        "example": "目前一号车间拥有八条全自动流水线。\n(Hiện tại xưởng số 1 sở hữu 8 dây chuyền tự động hóa hoàn toàn.)"
    },
    {
        "id": 7, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Cơ sở hạ tầng & Phân khu",
        "word": "安全帽", "pinyin": "ānquánmào", "meaning": "Mũ bảo hộ lao động",
        "collocations": ["佩戴安全帽 (Đội mũ bảo hộ)", "劳保用品 (Đồ bảo hộ lao động)", "安全规范 (Quy chuẩn an toàn)"],
        "example": "不戴安全帽，严禁进入生产车间！\n(Không đội mũ bảo hộ, nghiêm cấm bước vào xưởng sản xuất!)"
    },

    # Nhóm 2: Khối Sản xuất, Kỹ thuật & Chất lượng
    {
        "id": 8, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "生产部", "pinyin": "shēngchǎn bù", "meaning": "Bộ phận sản xuất",
        "collocations": ["安排生产 (Sắp xếp sản xuất)", "生产能力 (Năng lực sản xuất)", "生产进度 (Tiến độ sản xuất)"],
        "example": "生产部主要负责按照订单保质保量完成任务。\n(Bộ phận sản xuất phụ trách hoàn thành đơn hàng bảo đảm chất và lượng.)"
    },
    {
        "id": 9, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "生产主管", "pinyin": "shēngchǎn zhǔguǎn", "meaning": "Chủ quản sản xuất",
        "collocations": ["车间主管 (Chủ quản xưởng)", "布置任务 (Bố trí nhiệm vụ)", "开早会 (Họp giao ban sáng)"],
        "example": "生产主管正在和产线组长开早会。\n(Chủ quản sản xuất đang họp giao ban sáng với các tổ trưởng chuyền.)"
    },
    {
        "id": 10, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "产线组长", "pinyin": "chǎnxiàn zǔzhǎng", "meaning": "Tổ trưởng chuyền sản xuất",
        "collocations": ["车间组长 (Tổ trưởng xưởng)", "巡视产线 (Đi tuần tra chuyền)", "跟催进度 (Đôn đốc tiến độ)"],
        "example": "产线组长负责管理现场作业员并监督产量。\n(Tổ trưởng chuyền chịu trách nhiệm quản lý công nhân và giám sát sản lượng.)"
    },
    {
        "id": 11, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "作业员", "pinyin": "zuòyèyuán", "meaning": "Công nhân thao tác trực tiếp, thợ đứng chuyền",
        "collocations": ["一线作业员 (Công nhân tuyến đầu)", "操作规程 (Quy trình thao tác)", "严格遵守 (Tuân thủ nghiêm ngặt)"],
        "example": "作业员在工位上必须严格遵守操作规程。\n(Công nhân tại vị trí làm việc bắt buộc phải tuân thủ nghiêm quy trình thao tác.)"
    },
    {
        "id": 12, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "品质部", "pinyin": "pǐnzhì bù", "meaning": "Bộ phận quản lý chất lượng (QC)",
        "collocations": ["品质主管 (Chủ quản chất lượng)", "严格把关 (Kiểm soát chặt chẽ)", "不良品 (Hàng lỗi)"],
        "example": "如果品质部判定不合格，货物绝对不能出厂。\n(Nếu phòng QC đánh giá không đạt, hàng tuyệt đối không được xuất xưởng.)"
    },
    {
        "id": 13, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "质检员", "pinyin": "zhìjiǎnyuán", "meaning": "Nhân viên kiểm tra chất lượng (QC)",
        "collocations": ["巡检 (Đi tuần kiểm)", "首件确认 (Xác nhận mẫu đầu)", "检验报告 (Báo cáo kiểm phẩm)"],
        "example": "质检员正在产线上抽检产品的外观和尺寸。\n(Nhân viên QC đang rút mẫu kiểm tra ngoại quan và kích thước trên chuyền.)"
    },
    {
        "id": 14, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "工程部", "pinyin": "gōngchéng bù", "meaning": "Bộ phận kỹ thuật, công trình",
        "collocations": ["设备工程师 (Kỹ sư thiết bị)", "改善工艺 (Cải tiến công nghệ)", "技术支持 (Hỗ trợ kỹ thuật)"],
        "example": "工程部负责制定新产品的作业指导书。\n(Phòng kỹ thuật phụ trách soạn thảo tài liệu SOP cho sản phẩm mới.)"
    },
    {
        "id": 15, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Sản xuất & Kỹ thuật & Chất lượng",
        "word": "技术员", "pinyin": "jìshùyuán", "meaning": "Kỹ thuật viên (chỉnh máy, bảo trì khuôn)",
        "collocations": ["现场调机 (Chỉnh máy hiện trường)", "维修模具 (Sửa khuôn)", "排除故障 (Khắc phục sự cố)"],
        "example": "机台出现故障，技术员马上过来调机。\n(Máy móc gặp sự cố, kỹ thuật viên lập tức qua căn chỉnh máy.)"
    },

    # Nhóm 3: Khối Điều phối, Thu mua & Nghiên cứu
    {
        "id": 16, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Điều phối & Thu mua & R&D",
        "word": "生管部", "pinyin": "shēngguǎn bù", "meaning": "Bộ phận sinh quản (PMC - Lập kế hoạch & Điều độ)",
        "collocations": ["生管排产 (Sinh quản lên lịch)", "核对交期 (Đối chiếu hạn giao)", "产能评估 (Đánh giá năng lực xưởng)"],
        "example": "生管部正在根据客户订单安排下周的排产计划。\n(Phòng sinh quản đang sắp xếp lịch sản xuất tuần tới theo đơn đặt hàng.)"
    },
    {
        "id": 17, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Điều phối & Thu mua & R&D",
        "word": "采购部", "pinyin": "cǎigòu bù", "meaning": "Bộ phận thu mua",
        "collocations": ["寻找供应商 (Tìm nhà cung ứng)", "询价采购 (Hỏi giá thu mua)", "采购订单 (Đơn đặt mua hàng - PO)"],
        "example": "物料短缺时，采购部要第一时间催促供应商交货。\n(Khi thiếu vật tư, phòng thu mua phải giục nhà cung cấp giao hàng ngay.)"
    },
    {
        "id": 18, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Điều phối & Thu mua & R&D",
        "word": "仓管员", "pinyin": "cāngguǎnyuán", "meaning": "Thủ kho, nhân viên quản lý kho",
        "collocations": ["办理入库 (Làm thủ tục nhập kho)", "核对库存 (Đối chiếu tồn kho)", "库存报表 (Báo cáo kho)"],
        "example": "仓管员核对送货单后才办理原材料入库。\n(Thủ kho đối chiếu phiếu giao hàng xong mới làm thủ tục nhập kho vật tư.)"
    },
    {
        "id": 19, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Điều phối & Thu mua & R&D",
        "word": "物料员", "pinyin": "wùliàoyuán", "meaning": "Nhân viên tiếp liệu, cấp phát vật tư",
        "collocations": ["凭单领料 (Lĩnh liệu theo phiếu)", "现场配送 (Phát liệu tại chỗ)", "领料单 (Phiếu lĩnh vật tư)"],
        "example": "产线物料员拿着领料单去仓库领配件。\n(Nhân viên tiếp liệu của chuyền cầm phiếu lĩnh liệu lên kho nhận linh kiện.)"
    },
    {
        "id": 20, "lesson": "Bài 1: Tổng quan nhà máy", "group": "Điều phối & Thu mua & R&D",
        "word": "研发部", "pinyin": "yánfā bù", "meaning": "Bộ phận nghiên cứu và phát triển (R&D)",
        "collocations": ["研发中心 (Trung tâm R&D)", "打样员 (Nhân viên làm mẫu)", "新产品开发 (Phát triển sản phẩm mới)"],
        "example": "研发部负责根据客户样品进行图纸设计和打样。\n(Phòng R&D phụ trách thiết kế bản vẽ và làm mẫu thử theo mẫu của khách.)"
    }
]

HISTORY_FILE = "study_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(entry):
    hist = load_history()
    hist.insert(0, entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

# --- QUẢN LÝ SESSION STATE ---
if "learned_ids" not in st.session_state:
    st.session_state.learned_ids = set()
if "failed_ids" not in st.session_state:
    st.session_state.failed_ids = set()
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "is_flipped" not in st.session_state:
    st.session_state.is_flipped = False
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# --- THANH BÊN (SIDEBAR) ---
st.sidebar.title("🏭 TIẾNG TRUNG CÔNG XƯỞNG")
st.sidebar.markdown("**Hệ thống Flashcard & Test Thực Chiến**")

# Nhập tên học viên
student_name_input = st.sidebar.text_input(
    "👤 Tên học viên:",
    value=st.session_state.student_name,
    placeholder="Nhập họ tên của bạn..."
)
if student_name_input:
    st.session_state.student_name = student_name_input.strip()

# Chọn phạm vi ôn tập
scope_options = [
    "Tất cả từ Bài 1 (20 từ)",
    "Cơ sở hạ tầng & Phân khu (7 từ)",
    "Sản xuất & Kỹ thuật & Chất lượng (8 từ)",
    "Điều phối & Thu mua & R&D (5 từ)"
]
selected_scope = st.sidebar.selectbox("📂 Chọn phạm vi ôn tập:", scope_options)

# Lọc danh sách từ theo lựa chọn
if selected_scope == "Tất cả từ Bài 1 (20 từ)":
    current_vocab = VOCAB_DATA
elif selected_scope == "Cơ sở hạ tầng & Phân khu (7 từ)":
    current_vocab = [w for w in VOCAB_DATA if w["group"] == "Cơ sở hạ tầng & Phân khu"]
elif selected_scope == "Sản xuất & Kỹ thuật & Chất lượng (8 từ)":
    current_vocab = [w for w in VOCAB_DATA if w["group"] == "Sản xuất & Kỹ thuật & Chất lượng"]
else:
    current_vocab = [w for w in VOCAB_DATA if w["group"] == "Điều phối & Thu mua & R&D"]

# Chuyển đổi tính năng
menu = st.sidebar.radio(
    "📌 Chức năng chính:",
    ["📇 Thẻ Flashcard", "🎯 Ôn từ chưa thuộc", "📖 Mục lục từ", "✍️ Kiểm tra thử", "📊 Lịch sử"]
)

# --- THỐNG KÊ TIẾN ĐỘ HỌC TẬP (ĐÚNG FORMAT YÊU CẦU) ---
total_words = len(current_vocab)
scope_ids = {w["id"] for w in current_vocab}
learned_count = len(st.session_state.learned_ids.intersection(scope_ids))
failed_count = len(st.session_state.failed_ids.intersection(scope_ids))
pct = int((learned_count / total_words) * 100) if total_words > 0 else 0

st.markdown("### 📈 Tiến độ học tập")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📚 Tổng", f"{total_words} từ")
col2.metric("✓ Đã nhớ", f"{learned_count}/{total_words}")
col3.metric("⚡ Chưa thuộc", f"{failed_count}/{total_words}")
col4.metric("🎯 Thuộc", f"{pct}%")
st.progress(pct / 100)
st.markdown("---")

# ==================== 1. CHỨC NĂNG FLASHCARD ====================
if menu == "📇 Thẻ Flashcard":
    st.subheader(f"📇 Thẻ Flashcard — {selected_scope}")

    if total_words == 0:
        st.warning("Không có từ vựng nào trong danh mục này.")
    else:
        if st.session_state.card_idx >= total_words:
            st.session_state.card_idx = 0

        cur_word = current_vocab[st.session_state.card_idx]
        st.caption(f"Thẻ số: {st.session_state.card_idx + 1} / {total_words} (Mã từ: #{cur_word['id']} | Nhóm: {cur_word['group']})")

        # Khung hiển thị thẻ Flashcard
        with st.container(border=True):
            if not st.session_state.is_flipped:
                # MẶT TRƯỚC: Hán tự + Pinyin
                st.markdown(f"<h1 style='text-align: center; color: #1E3A8A; font-size: 56px; margin-bottom: 0px;'>{cur_word['word']}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: #4B5563; font-weight: normal; margin-top: 5px;'>{cur_word['pinyin']}</h3>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #9CA3AF; margin-top: 25px;'><i>(Nhấn nút 'Lật mặt thẻ' bên dưới để xem nghĩa tiếng Việt & cụm từ)</i></p>", unsafe_allow_html=True)
            else:
                # MẶT SAU: Nghĩa + Cụm từ + Ví dụ
                st.markdown(f"<h2 style='text-align: center; color: #1E3A8A;'>{cur_word['word']} <span style='font-size:22px; color:#4B5563;'>({cur_word['pinyin']})</span></h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: #047857;'>👉 <i>{cur_word['meaning']}</i></h3>", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("##### 🔗 3 cụm từ kết hợp thực tế:")
                for c in cur_word["collocations"]:
                    st.markdown(f"- **{c}**")
                st.markdown("##### 💬 Câu ví dụ ngữ cảnh:")
                st.info(cur_word["example"])

        # Hàng nút bấm tương tác
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            if st.button("🔄 Lật mặt thẻ", use_container_width=True):
                st.session_state.is_flipped = not st.session_state.is_flipped
                st.rerun()
        with b2:
            if st.button("✓ Đã nhớ", type="primary", use_container_width=True):
                st.session_state.learned_ids.add(cur_word["id"])
                st.session_state.failed_ids.discard(cur_word["id"])
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.session_state.is_flipped = False
                st.rerun()
        with b3:
            if st.button("⚡ Chưa thuộc", use_container_width=True):
                st.session_state.failed_ids.add(cur_word["id"])
                st.session_state.learned_ids.discard(cur_word["id"])
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.session_state.is_flipped = False
                st.rerun()
        with b4:
            if st.button("⏭️ Tiếp theo", use_container_width=True):
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.session_state.is_flipped = False
                st.rerun()

# ==================== 2. CHỨC NĂNG ÔN TỪ CHƯA THUỘC ====================
elif menu == "🎯 Ôn từ chưa thuộc":
    st.subheader("🎯 Ôn từ chưa thuộc")
    failed_words = [w for w in VOCAB_DATA if w["id"] in st.session_state.failed_ids]

    st.markdown(f"Số lượng từ hiện đang đánh dấu **Chưa thuộc**: **`{len(failed_words)}`**")

    if len(failed_words) == 0:
        st.success("🎉 Bạn chưa có từ nào bị đánh dấu 'Chưa thuộc'. Tuyệt vời!")
    else:
        for idx, w in enumerate(failed_words, 1):
            with st.expander(f"#{idx} | {w['word']} ({w['pinyin']}) — Bấm xem chi tiết"):
                st.markdown(f"**Ý nghĩa:** *{w['meaning']}*")
                st.markdown("**Cụm từ kết hợp:**")
                for c in w["collocations"]:
                    st.markdown(f"- {c}")
                st.markdown("**Câu ví dụ:**")
                st.caption(w["example"])
                if st.button(f"Đã thuộc từ '{w['word']}'", key=f"rm_fail_{w['id']}"):
                    st.session_state.failed_ids.remove(w["id"])
                    st.session_state.learned_ids.add(w["id"])
                    st.rerun()

# ==================== 3. CHỨC NĂNG MỤC LỤC TỪ ====================
elif menu == "📖 Mục lục từ":
    st.subheader("📖 Mục lục tổng hợp 20 từ vựng Bài 1")
    search_q = st.text_input("🔍 Tìm kiếm từ (Hán tự, Pinyin hoặc Tiếng Việt):", placeholder="Ví dụ: 车间, cāngkù, kiểm tra...")

    filtered = current_vocab
    if search_q:
        q = search_q.strip().lower()
        filtered = [
            w for w in current_vocab 
            if q in w["word"].lower() or q in w["pinyin"].lower() or q in w["meaning"].lower()
        ]

    table_data = []
    for w in filtered:
        status = "✓ Đã nhớ" if w["id"] in st.session_state.learned_ids else ("⚡ Chưa thuộc" if w["id"] in st.session_state.failed_ids else "Chưa đánh dấu")
        table_data.append({
            "STT": w["id"],
            "Chữ Hán": w["word"],
            "Phiên âm Pinyin": w["pinyin"],
            "Nghĩa Tiếng Việt": w["meaning"],
            "Nhóm phân loại": w["group"],
            "Cụm từ kết hợp": " | ".join(w["collocations"]),
            "Trạng thái": status
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==================== 4. CHỨC NĂNG KIỂM TRA THỬ ====================
elif menu == "✍️ Kiểm tra thử":
    st.subheader(f"✍️ Kiểm tra thử phản xạ — {selected_scope}")

    if not st.session_state.student_name:
        st.warning("⚠️ Vui lòng nhập họ tên của bạn ở ô **'👤 Tên học viên'** tại thanh bên trái trước khi làm bài thi.")

    # Nút tạo bộ đề kiểm tra mới
    if "quiz_questions" not in st.session_state or st.button("🎲 Tạo đề kiểm tra mới (10 câu)"):
        sample_size = min(10, len(current_vocab))
        sampled = random.sample(current_vocab, sample_size)
        questions = []
        for item in sampled:
            wrong_pool = [w["meaning"] for w in VOCAB_DATA if w["id"] != item["id"]]
            distractors = random.sample(wrong_pool, 3)
            options = distractors + [item["meaning"]]
            random.shuffle(options)
            questions.append({
                "id": item["id"],
                "word": item["word"],
                "pinyin": item["pinyin"],
                "correct": item["meaning"],
                "options": options
            })
        st.session_state.quiz_questions = questions
        st.session_state.quiz_submitted = False
        st.rerun()

    # Form làm bài
    with st.form("quiz_form"):
        st.markdown(f"Thí sinh: **{st.session_state.student_name if st.session_state.student_name else '(Chưa nhập tên)'}** | Đề thi gồm: **{len(st.session_state.quiz_questions)} câu** trắc nghiệm")
        st.write("---")
        user_answers = {}
        for i, q in enumerate(st.session_state.quiz_questions, 1):
            st.markdown(f"**Câu {i}:** Từ **{q['word']}** *( {q['pinyin']} )* có nghĩa là gì?")
            user_answers[i] = st.radio(
                f"Lựa chọn cho câu {i}:",
                q["options"],
                key=f"quiz_opt_{i}",
                label_visibility="collapsed"
            )
            st.write("")

        submitted = st.form_submit_button("Nộp bài & Chấm điểm", type="primary", use_container_width=True)
        if submitted:
            if not st.session_state.student_name:
                st.error("Bạn chưa nhập tên học viên! Vui lòng nhập tên ở cột bên trái rồi bấm nộp lại nhé.")
            else:
                score = 0
                total_q = len(st.session_state.quiz_questions)
                for i, q in enumerate(st.session_state.quiz_questions, 1):
                    if user_answers[i] == q["correct"]:
                        score += 1
                        st.session_state.learned_ids.add(q["id"])
                    else:
                        st.session_state.failed_ids.add(q["id"])

                percent_score = round((score / total_q) * 100, 1)
                st.session_state.quiz_submitted = True

                # Báo điểm
                st.success(f"Kết quả kiểm tra: **{score}/{total_q} câu đúng** ({percent_score}%)")
                if percent_score >= 80:
                    st.balloons()

                # Lưu lịch sử kiểm tra
                entry = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": st.session_state.student_name,
                    "scope": selected_scope,
                    "score": f"{score}/{total_q}",
                    "percent": f"{percent_score}%"
                }
                save_history(entry)

# ==================== 5. CHỨC NĂNG LỊCH SỬ ====================
elif menu == "📊 Lịch sử":
    st.subheader("📊 Lịch sử làm bài kiểm tra")
    history_list = load_history()

    if not history_list:
        st.info("Chưa có lịch sử làm bài nào được ghi nhận. Hãy sang tab '✍️ Kiểm tra thử' làm một bài test nhé!")
    else:
        df_hist = pd.DataFrame(history_list)
        df_hist.columns = ["Thời gian", "Họ tên học viên", "Phạm vi đề thi", "Số câu đúng", "Tỷ lệ đạt"]
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

        if st.button("🗑️ Xóa toàn bộ lịch sử", type="secondary"):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.rerun()
