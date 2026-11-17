import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime

# --- CẤU HÌNH TRANG STREAMLIT ---
st.set_page_config(
    page_title="Ôn Tập Tiếng Trung Công Xưởng",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS TỐI ƯU GIAO DIỆN & ẨN LOGO / MENU GÓC PHẢI ---
st.markdown("""
<style>
    /* ======================================================== */
    /* 1. ẨN HOÀN TOÀN LOGO STREAMLIT, MENU & HEADER GÓC PHẢI */
    /* ======================================================== */
    #MainMenu {visibility: hidden; display: none !important;}
    header[data-testid="stHeader"] {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden; display: none !important;}
    [data-testid="stDecoration"] {visibility: hidden; display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}

    /* ======================================================== */
    /* 2. GIAO DIỆN MOBILE & 3D FLIP CARD                       */
    /* ======================================================== */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        max-width: 700px;
        margin: auto;
    }
    
    /* Giao diện nút dàn hàng ngang (Horizontal Pills) */
    div[data-testid="stRadio"] > div {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 8px;
    }
    div[data-testid="stRadio"] label {
        background: #f1f5f9;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #cbd5e1;
        cursor: pointer;
        font-weight: 500;
        font-size: 14px;
        margin: 0 !important;
    }

    /* Hiệu ứng 3D Flashcard */
    .flashcard-wrapper {
        perspective: 1200px;
        margin: 12px auto;
        width: 100%;
    }
    .flashcard-toggle {
        display: none;
    }
    .flashcard-inner {
        position: relative;
        width: 100%;
        min-height: 380px;
        transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        transform-style: preserve-3d;
        cursor: pointer;
        user-select: none;
        -webkit-tap-highlight-color: transparent;
    }
    .flashcard-toggle:checked + .flashcard-inner {
        transform: rotateY(180deg);
    }
    .flashcard-face {
        position: absolute;
        width: 100%;
        height: 100%;
        min-height: 380px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        border-radius: 20px;
        padding: 24px 18px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.07);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }
    .flashcard-front {
        background: linear-gradient(145deg, #ffffff, #f0f7ff);
        border: 2px solid #bfdbfe;
        text-align: center;
        align-items: center;
        justify-content: center;
    }
    .flashcard-back {
        background: #ffffff;
        border: 2px solid #86efac;
        transform: rotateY(180deg);
        overflow-y: auto;
        text-align: left;
    }
    .chinese-word {
        font-size: 50px;
        font-weight: 700;
        color: #1e3a8a;
        margin: 0;
        line-height: 1.2;
    }
    .pinyin-word {
        font-size: 20px;
        color: #4b5563;
        margin-top: 8px;
    }
    .tap-hint {
        font-size: 13px;
        color: #9ca3af;
        margin-top: 25px;
        text-align: center;
    }
    .colloc-item {
        background-color: #f8fafc;
        border-left: 3px solid #10b981;
        padding: 6px 10px;
        margin: 5px 0;
        border-radius: 4px;
        font-size: 14px;
        color: #1e293b;
    }
    .example-box {
        background-color: #f0fdf4;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
        font-size: 13px;
        color: #166534;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU TỔNG 26 TỪ (BUỔI 1: 14 TỪ | BUỔI 2: 12 TỪ) ---
VOCAB_DATA = [
    # BUỔI 1 (14 từ)
    {
        "id": 1, "lesson": "Buổi 1 (14)",
        "word": "工厂", "pinyin": "gōngchǎng", "meaning": "Nhà máy, công xưởng",
        "collocations": ["参观工厂 (Tham quan xưởng)", "工厂规模 (Quy mô xưởng)", "现代化工厂 (Nhà máy hiện đại)"],
        "example": "欢迎各位领导来我们工厂参观考察。<br><i>(Hoan nghênh các vị lãnh đạo đến tham quan khảo sát nhà máy chúng tôi.)</i>"
    },
    {
        "id": 2, "lesson": "Buổi 1 (14)",
        "word": "车间", "pinyin": "chējiān", "meaning": "Phân xưởng sản xuất",
        "collocations": ["生产车间 (Xưởng sản xuất)", "无尘车间 (Phòng sạch)", "总装车间 (Xưởng lắp ráp tổng)"],
        "example": "进入生产车间之前，所有人必须戴好安全帽。<br><i>(Trước khi vào xưởng sản xuất, tất cả phải đội mũ bảo hộ.)</i>"
    },
    {
        "id": 3, "lesson": "Buổi 1 (14)",
        "word": "办公大楼", "pinyin": "bàngōng dàlóu", "meaning": "Tòa nhà văn phòng hành chính",
        "collocations": ["行政大楼 (Tòa hành chính)", "佩戴厂牌 (Đeo thẻ nhà máy)", "总经办 (Văn phòng Tổng giám đốc)"],
        "example": "行政部门都在这栋办公大楼里面办公。<br><i>(Các bộ phận hành chính đều làm việc trong tòa văn phòng này.)</i>"
    },
    {
        "id": 4, "lesson": "Buổi 1 (14)",
        "word": "仓库", "pinyin": "cāngkù", "meaning": "Kho bãi",
        "collocations": ["原料仓库 (Kho nguyên liệu)", "成品仓库 (Kho thành phẩm)", "月底盘点 (Kiểm kê cuối tháng)"],
        "example": "原料仓库在工厂东侧，靠近卸货平台。<br><i>(Kho nguyên liệu nằm ở phía đông nhà máy, sát sàn bốc dỡ.)</i>"
    },
    {
        "id": 5, "lesson": "Buổi 1 (14)",
        "word": "设备", "pinyin": "shèbèi", "meaning": "Thiết bị, máy móc",
        "collocations": ["先进设备 (Thiết bị tiên tiến)", "自动化设备 (Thiết bị tự động)", "数控机床 (Máy CNC)"],
        "example": "车间里大部分生产设备都是从德国引进的。<br><i>(Phần lớn thiết bị trong xưởng đều nhập từ Đức.)</i>"
    },
    {
        "id": 6, "lesson": "Buổi 1 (14)",
        "word": "流水线", "pinyin": "liúshuǐxiàn", "meaning": "Dây chuyền sản xuất lắp ráp",
        "collocations": ["自动化流水线 (Dây chuyền tự động)", "流水线作业 (Thao tác trên chuyền)", "流水线装配 (Lắp ráp dây chuyền)"],
        "example": "目前一号车间拥有八条全自动流水线。<br><i>(Hiện tại xưởng số 1 sở hữu 8 dây chuyền tự động hóa.)</i>"
    },
    {
        "id": 7, "lesson": "Buổi 1 (14)",
        "word": "生产部", "pinyin": "shēngchǎn bù", "meaning": "Bộ phận sản xuất",
        "collocations": ["安排生产 (Sắp xếp sản xuất)", "生产能力 (Năng lực sản xuất)", "生产进度 (Tiến độ sản xuất)"],
        "example": "生产部主要负责按照订单保质保量完成任务。<br><i>(Bộ phận sản xuất phụ trách hoàn thành đơn hàng bảo đảm chất và lượng.)</i>"
    },
    {
        "id": 8, "lesson": "Buổi 1 (14)",
        "word": "生产主管", "pinyin": "shēngchǎn zhǔguǎn", "meaning": "Chủ quản sản xuất",
        "collocations": ["车间主管 (Chủ quản xưởng)", "布置任务 (Bố trí nhiệm vụ)", "开早会 (Họp giao ban sáng)"],
        "example": "生产主管正在和产线组长开早会。<br><i>(Chủ quản sản xuất đang họp giao ban sáng với tổ trưởng chuyền.)</i>"
    },
    {
        "id": 9, "lesson": "Buổi 1 (14)",
        "word": "产线组长", "pinyin": "chǎnxiàn zǔzhǎng", "meaning": "Tổ trưởng chuyền sản xuất",
        "collocations": ["车间组长 (Tổ trưởng xưởng)", "巡视产线 (Đi tuần tra chuyền)", "跟催进度 (Đôn đốc tiến độ)"],
        "example": "产线组长负责管理现场作业员并监督产量。<br><i>(Tổ trưởng chuyền quản lý công nhân và giám sát sản lượng.)</i>"
    },
    {
        "id": 10, "lesson": "Buổi 1 (14)",
        "word": "作业员", "pinyin": "zuòyèyuán", "meaning": "Công nhân thao tác trực tiếp, thợ đứng chuyền",
        "collocations": ["一线作业员 (Công nhân tuyến đầu)", "操作规程 (Quy trình thao tác)", "严格遵守 (Tuân thủ nghiêm ngặt)"],
        "example": "作业员在工位上必须严格遵守操作规程。<br><i>(Công nhân tại vị trí làm việc phải tuân thủ nghiêm quy trình.)</i>"
    },
    {
        "id": 11, "lesson": "Buổi 1 (14)",
        "word": "品质部", "pinyin": "pǐnzhì bù", "meaning": "Bộ phận quản lý chất lượng (QC)",
        "collocations": ["品质主管 (Chủ quản chất lượng)", "严格把关 (Kiểm soát chặt chẽ)", "不良品 (Hàng lỗi)"],
        "example": "如果品质部判定不合格，货物绝对不能出厂。<br><i>(Nếu QC đánh giá không đạt, hàng tuyệt đối không được xuất xưởng.)</i>"
    },
    {
        "id": 12, "lesson": "Buổi 1 (14)",
        "word": "质检员", "pinyin": "zhìjiǎnyuán", "meaning": "Nhân viên kiểm tra chất lượng (QC)",
        "collocations": ["巡检 (Đi tuần kiểm)", "首件确认 (Xác nhận mẫu đầu)", "检验报告 (Báo cáo kiểm phẩm)"],
        "example": "质检员正在产线上抽检产品的外观和尺寸。<br><i>(QC đang rút mẫu kiểm tra ngoại quan và kích thước trên chuyền.)</i>"
    },
    {
        "id": 13, "lesson": "Buổi 1 (14)",
        "word": "工程部", "pinyin": "gōngchéng bù", "meaning": "Bộ phận kỹ thuật, công trình",
        "collocations": ["设备工程师 (Kỹ sư thiết bị)", "改善工艺 (Cải tiến công nghệ)", "技术支持 (Hỗ trợ kỹ thuật)"],
        "example": "工程部负责制定新产品的作业指导书。<br><i>(Phòng kỹ thuật soạn thảo tài liệu SOP cho sản phẩm mới.)</i>"
    },
    {
        "id": 14, "lesson": "Buổi 1 (14)",
        "word": "技术员", "pinyin": "jìshùyuán", "meaning": "Kỹ thuật viên (chỉnh máy, bảo trì)",
        "collocations": ["现场调机 (Chỉnh máy hiện trường)", "维修模具 (Sửa khuôn)", "排除故障 (Khắc phục sự cố)"],
        "example": "机台出现故障，技术员马上过来调机。<br><i>(Máy móc gặp sự cố, kỹ thuật viên lập tức qua căn chỉnh máy.)</i>"
    },

    # BUỔI 2 (12 từ)
    {
        "id": 15, "lesson": "Buổi 2 (12)",
        "word": "生管部", "pinyin": "shēngguǎn bù", "meaning": "Bộ phận sinh quản (PMC - Kế hoạch & Điều độ)",
        "collocations": ["生管排产 (Sinh quản lên lịch)", "核对交期 (Đối chiếu hạn giao)", "产能评估 (Đánh giá năng lực xưởng)"],
        "example": "生管部正在安排下周的排产计划。<br><i>(Phòng sinh quản đang sắp xếp lịch sản xuất tuần tới.)</i>"
    },
    {
        "id": 16, "lesson": "Buổi 2 (12)",
        "word": "采购部", "pinyin": "cǎigòu bù", "meaning": "Bộ phận thu mua",
        "collocations": ["寻找供应商 (Tìm nhà cung ứng)", "询价采购 (Hỏi giá thu mua)", "采购订单 (Đơn đặt mua hàng - PO)"],
        "example": "物料短缺时，采购部要第一时间催促交货。<br><i>(Khi thiếu vật tư, phòng thu mua phải giục giao hàng ngay.)</i>"
    },
    {
        "id": 17, "lesson": "Buổi 2 (12)",
        "word": "仓管员", "pinyin": "cāngguǎnyuán", "meaning": "Thủ kho, nhân viên kho",
        "collocations": ["办理入库 (Làm thủ tục nhập kho)", "核对库存 (Đối chiếu tồn kho)", "库存报表 (Báo cáo kho)"],
        "example": "仓管员核对送货单后才办理原材料入库。<br><i>(Thủ kho đối chiếu phiếu giao xong mới làm thủ tục nhập kho.)</i>"
    },
    {
        "id": 18, "lesson": "Buổi 2 (12)",
        "word": "物料员", "pinyin": "wùliàoyuán", "meaning": "Nhân viên tiếp liệu, cấp phát vật tư",
        "collocations": ["凭单领料 (Lĩnh liệu theo phiếu)", "现场配送 (Phát liệu tại chỗ)", "领料单 (Phiếu lĩnh vật tư)"],
        "example": "产线物料员拿着领料单去仓库领配件。<br><i>(Nhân viên tiếp liệu cầm phiếu lên kho nhận linh kiện.)</i>"
    },
    {
        "id": 19, "lesson": "Buổi 2 (12)",
        "word": "研发部", "pinyin": "yánfā bù", "meaning": "Bộ phận nghiên cứu và phát triển (R&D)",
        "collocations": ["研发中心 (Trung tâm R&D)", "打样员 (Nhân viên làm mẫu)", "新产品开发 (Phát triển sản phẩm mới)"],
        "example": "研发部负责根据客户样品进行图纸设计。<br><i>(Phòng R&D phụ trách thiết kế bản vẽ theo mẫu của khách.)</i>"
    },
    {
        "id": 20, "lesson": "Buổi 2 (12)",
        "word": "安全帽", "pinyin": "ānquánmào", "meaning": "Mũ bảo hộ lao động",
        "collocations": ["佩戴安全帽 (Đội mũ bảo hộ)", "劳保用品 (Đồ bảo hộ)", "安全规范 (Quy chuẩn an toàn)"],
        "example": "不戴安全帽，严禁进入生产车间！<br><i>(Không đội mũ bảo hộ, nghiêm cấm bước vào xưởng sản xuất!)</i>"
    },
    {
        "id": 21, "lesson": "Buổi 2 (12)",
        "word": "收到", "pinyin": "shōudào", "meaning": "Đã nhận được (chỉ thị, thông báo)",
        "collocations": ["收到指示 (Đã nhận chỉ thị)", "收到通知 (Đã nhận thông báo)", "收到回复 (Đã nhận phản hồi)"],
        "example": "收到，我马上安排车间组长挑选不良品。<br><i>(Đã nhận, tôi bố trí tổ trưởng lựa hàng lỗi ra ngay.)</i>"
    },
    {
        "id": 22, "lesson": "Buổi 2 (12)",
        "word": "马上", "pinyin": "mǎshàng", "meaning": "Ngay lập tức",
        "collocations": ["马上处理 (Xử lý ngay)", "马上跟进 (Bám sát ngay)", "马上核实 (Xác minh ngay)"],
        "example": "收到通知，我马上通知产线组织加班。<br><i>(Nhận thông báo, tôi báo chuyền tăng ca ngay.)</i>"
    },
    {
        "id": 23, "lesson": "Buổi 2 (12)",
        "word": "核对", "pinyin": "héduì", "meaning": "Đối chiếu, kiểm tra lại",
        "collocations": ["核对物料 (Đối chiếu vật tư)", "核对数量 (Đối chiếu số lượng)", "麻烦核对 (Phiền đối chiếu giúp)"],
        "example": "麻烦仓库帮忙核对这批面料的实际库存。<br><i>(Phiền kho hỗ trợ đối chiếu lượng tồn kho thực tế của lô vải.)</i>"
    },
    {
        "id": 24, "lesson": "Buổi 2 (12)",
        "word": "发", "pinyin": "fā", "meaning": "Gửi (tin nhắn), phát (liệu)",
        "collocations": ["发群里 (Gửi vào trong nhóm)", "发料单 (Phiếu cấp phát vật tư)", "发邮件 (Gửi email)"],
        "example": "生产日报表已经发群里，请主管查阅。<br><i>(Báo cáo ngày đã gửi vào nhóm, mời chủ quản duyệt.)</i>"
    },
    {
        "id": 25, "lesson": "Buổi 2 (12)",
        "word": "确认", "pinyin": "quèrèn", "meaning": "Xác nhận",
        "collocations": ["请确认 (Xin vui lòng xác nhận)", "签字确认 (Ký tên xác nhận)", "首件确认 (Duyệt mẫu đầu chuyền)"],
        "example": "排产计划已发群里，请各位主管确认。<br><i>(Lịch sản xuất đã gửi nhóm, xin các chủ quản xác nhận giúp.)</i>"
    },
    {
        "id": 26, "lesson": "Buổi 2 (12)",
        "word": "异常", "pinyin": "yìcháng", "meaning": "Bất thường, sự cố",
        "collocations": ["现场异常 (Sự cố hiện trường)", "品质异常 (Bất thường chất lượng)", "异常反馈 (Báo cáo sự cố)"],
        "example": "产线一有异常，必须立刻向上级汇报。<br><i>(Chuyền có sự cố là phải lập tức báo cáo cấp trên ngay.)</i>"
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

# --- KHỞI TẠO STATE ---
if "learned_ids" not in st.session_state:
    st.session_state.learned_ids = set()
if "failed_ids" not in st.session_state:
    st.session_state.failed_ids = set()
if "card_idx" not in st.session_state:
    st.session_state.card_idx = 0
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# --- TIÊU ĐỀ & NHẬP TÊN HỌC VIÊN ---
st.markdown("### 🏭 Tiếng Trung Công Xưởng Thực Chiến")
s_name = st.text_input("👤 Nhập tên học viên:", value=st.session_state.student_name, placeholder="Ví dụ: Nguyễn Văn A")
if s_name:
    st.session_state.student_name = s_name.strip()

# --- 1. DÀN HÀNG NGANG: PHẠM VI BÀI HỌC ---
st.markdown("**Phạm vi bài học:**")
scope_choice = st.radio(
    "scope_radio",
    ["Tất cả (26)", "Buổi 1 (14)", "Buổi 2 (12)"],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)

if scope_choice == "Tất cả (26)":
    current_vocab = VOCAB_DATA
elif scope_choice == "Buổi 1 (14)":
    current_vocab = [w for w in VOCAB_DATA if w["lesson"] == "Buổi 1 (14)"]
else:
    current_vocab = [w for w in VOCAB_DATA if w["lesson"] == "Buổi 2 (12)"]

# --- 2. DÀN HÀNG NGANG: CHẾ ĐỘ LUYỆN TẬP ---
st.markdown("**Chế độ luyện tập:**")
mode_choice = st.radio(
    "mode_radio",
    ["Thẻ từ", "Trắc nghiệm", "Nối từ", "Bảng từ", "Lịch sử"],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)

# --- THỐNG KÊ TIẾN ĐỘ ---
total_words = len(current_vocab)
scope_ids = {w["id"] for w in current_vocab}
learned_count = len(st.session_state.learned_ids.intersection(scope_ids))
failed_count = len(st.session_state.failed_ids.intersection(scope_ids))
pct = int((learned_count / total_words) * 100) if total_words > 0 else 0

st.markdown(f"📊 **Tiến độ:** 📚 Tổng: **{total_words}** từ | ✓ Đã nhớ: **{learned_count}/{total_words}** | ⚡ Chưa thuộc: **{failed_count}/{total_words}** | 🎯 Thuộc: **{pct}%**")
st.progress(pct / 100)
st.markdown("---")

# ==================== CHẾ ĐỘ 1: THẺ TỪ (FLASHCARD CHẠM LẬT) ====================
if mode_choice == "Thẻ từ":
    if total_words == 0:
        st.warning("Không có từ nào trong phạm vi này.")
    else:
        if st.session_state.card_idx >= total_words:
            st.session_state.card_idx = 0

        cur_word = current_vocab[st.session_state.card_idx]
        card_num = st.session_state.card_idx + 1

        colloc_html = "".join([f"<div class='colloc-item'>• {c}</div>" for c in cur_word["collocations"]])

        flashcard_html = f"""
        <div class="flashcard-wrapper">
            <label>
                <input type="checkbox" class="flashcard-toggle" id="card_{cur_word['id']}_{card_num}">
                <div class="flashcard-inner">
                    <!-- MẶT TRƯỚC -->
                    <div class="flashcard-face flashcard-front">
                        <span style="background:#e0e7ff; color:#3730a3; padding:4px 12px; border-radius:99px; font-size:12px; font-weight:600;">{cur_word['lesson']}</span>
                        <div style="flex-grow:1; display:flex; flex-direction:column; justify-content:center;">
                            <h1 class="chinese-word">{cur_word['word']}</h1>
                            <div class="pinyin-word">{cur_word['pinyin']}</div>
                        </div>
                        <div class="tap-hint">👆 <b>Chạm thẻ để lật mặt sau</b></div>
                    </div>
                    <!-- MẶT SAU -->
                    <div class="flashcard-face flashcard-back">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                                <h3 style="margin:0; color:#1e3a8a;">{cur_word['word']}</h3>
                                <span style="font-size:15px; color:#4b5563;">{cur_word['pinyin']}</span>
                            </div>
                            <div style="color:#047857; font-weight:700; font-size:18px; margin:6px 0 10px 0;">👉 {cur_word['meaning']}</div>
                            <div style="font-size:13px; font-weight:600; color:#374151; margin-bottom:4px;">🔗 Cụm từ hay dùng:</div>
                            {colloc_html}
                            <div class="example-box">💬 <b>Ví dụ:</b><br>{cur_word['example']}</div>
                        </div>
                        <div class="tap-hint">👆 <b>Chạm lại để lật về chữ Hán</b></div>
                    </div>
                </div>
            </label>
        </div>
        """
        st.markdown(flashcard_html, unsafe_allow_html=True)
        st.caption(f"Thẻ {card_num} / {total_words} (Mã #{cur_word['id']})")

        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            if st.button("✓ Đã nhớ", type="primary", use_container_width=True):
                st.session_state.learned_ids.add(cur_word["id"])
                st.session_state.failed_ids.discard(cur_word["id"])
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.rerun()
        with btn2:
            if st.button("⚡ Chưa thuộc", use_container_width=True):
                st.session_state.failed_ids.add(cur_word["id"])
                st.session_state.learned_ids.discard(cur_word["id"])
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.rerun()
        with btn3:
            if st.button("⏭️ Bỏ qua", use_container_width=True):
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.rerun()

# ==================== CHẾ ĐỘ 2: TRẮC NGHIỆM ====================
elif mode_choice == "Trắc nghiệm":
    st.markdown(f"##### ✍️ Trắc nghiệm phản xạ ({scope_choice})")

    if "quiz_set" not in st.session_state or st.button("🎲 Đổi đề thi mới"):
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
        st.session_state.quiz_set = questions
        st.rerun()

    with st.form("quiz_form"):
        ans = {}
        for i, q in enumerate(st.session_state.quiz_set, 1):
            st.markdown(f"**Câu {i}:** Từ **{q['word']}** *( {q['pinyin']} )* nghĩa là gì?")
            ans[i] = st.radio(f"q_{i}", q["options"], key=f"q_{i}", label_visibility="collapsed")
            st.write("")

        if st.form_submit_button("Nộp bài & Chấm điểm", type="primary", use_container_width=True):
            score = 0
            for i, q in enumerate(st.session_state.quiz_set, 1):
                if ans[i] == q["correct"]:
                    score += 1
                    st.session_state.learned_ids.add(q["id"])
                else:
                    st.session_state.failed_ids.add(q["id"])

            total_q = len(st.session_state.quiz_set)
            pct_score = round((score / total_q) * 100, 1)
            st.success(f"🎉 Kết quả: **{score}/{total_q} câu đúng** ({pct_score}%)")
            if pct_score >= 80:
                st.balloons()

            save_history({
                "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "name": st.session_state.student_name if st.session_state.student_name else "Ẩn danh",
                "type": "Trắc nghiệm",
                "scope": scope_choice,
                "score": f"{score}/{total_q} ({pct_score}%)"
            })

# ==================== CHẾ ĐỘ 3: NỐI TỪ ====================
elif mode_choice == "Nối từ":
    st.markdown(f"##### 🧩 Trò chơi Nối từ phản xạ ({scope_choice})")
    
    if "match_items" not in st.session_state or st.button("🎲 Tạo ván nối từ mới"):
        sample_match = random.sample(current_vocab, min(5, len(current_vocab)))
        words = [w["word"] for w in sample_match]
        meanings = [w["meaning"] for w in sample_match]
        random.shuffle(words)
        random.shuffle(meanings)
        st.session_state.match_items = sample_match
        st.session_state.match_words = words
        st.session_state.match_meanings = meanings
        st.rerun()

    st.caption("Chọn nghĩa tiếng Việt tương ứng cho từng từ tiếng Trung:")
    user_match = {}
    with st.form("match_form"):
        for w_text in st.session_state.match_words:
            correct_entry = next(item for item in st.session_state.match_items if item["word"] == w_text)
            st.markdown(f"👉 Từ: <b style='font-size:18px; color:#1e3a8a;'>{w_text}</b> <i>({correct_entry['pinyin']})</i>", unsafe_allow_html=True)
            user_match[w_text] = st.selectbox(
                f"Nghĩa của {w_text}:",
                ["-- Chọn nghĩa --"] + st.session_state.match_meanings,
                key=f"match_{w_text}",
                label_visibility="collapsed"
            )
            st.write("")

        if st.form_submit_button("Kiểm tra kết quả nối từ", type="primary", use_container_width=True):
            m_score = 0
            for item in st.session_state.match_items:
                if user_match[item["word"]] == item["meaning"]:
                    m_score += 1
                    st.session_state.learned_ids.add(item["id"])
                else:
                    st.session_state.failed_ids.add(item["id"])

            total_m = len(st.session_state.match_items)
            st.success(f"Bạn đã ghép đúng **{m_score}/{total_m}** cặp từ!")

            save_history({
                "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "name": st.session_state.student_name if st.session_state.student_name else "Ẩn danh",
                "type": "Nối từ",
                "scope": scope_choice,
                "score": f"{m_score}/{total_m} cặp"
            })

# ==================== CHẾ ĐỘ 4: BẢNG TỪ ====================
elif mode_choice == "Bảng từ":
    st.markdown(f"##### 📖 Bảng từ vựng ({scope_choice})")
    search_txt = st.text_input("🔍 Tìm kiếm từ vựng:", placeholder="Nhập Hán tự, Pinyin hoặc Tiếng Việt...")

    filtered = current_vocab
    if search_txt:
        q = search_txt.strip().lower()
        filtered = [w for w in current_vocab if q in w["word"].lower() or q in w["pinyin"].lower() or q in w["meaning"].lower()]

    rows = []
    for w in filtered:
        status = "✓ Đã nhớ" if w["id"] in st.session_state.learned_ids else ("⚡ Chưa thuộc" if w["id"] in st.session_state.failed_ids else "-")
        rows.append({
            "STT": w["id"],
            "Chữ Hán": w["word"],
            "Pinyin": w["pinyin"],
            "Nghĩa": w["meaning"],
            "Bài": w["lesson"],
            "Trạng thái": status
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ==================== CHẾ ĐỘ 5: LỊCH SỬ ====================
elif mode_choice == "Lịch sử":
    st.markdown("##### 📊 Lịch sử làm bài tập của học viên")
    h_data = load_history()

    if not h_data:
        st.info("Chưa có lịch sử làm bài. Hãy làm bài ở phần 'Trắc nghiệm' hoặc 'Nối từ' để ghi nhận điểm số nhé!")
    else:
        df_h = pd.DataFrame(h_data)
        df_h.columns = ["Thời gian", "Học viên", "Chế độ", "Phạm vi", "Kết quả"]
        st.dataframe(df_h, use_container_width=True, hide_index=True)

        if st.button("🗑️ Xóa toàn bộ lịch sử", type="secondary"):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.rerun()
