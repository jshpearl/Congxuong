import streamlit as st
import pandas as pd
import random
import json
import os
from datetime import datetime

# --- CẤU HÌNH TRANG STREAMLIT ---
st.set_page_config(
    page_title="Tiếng Trung Công Xưởng 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS GIAO DIỆN PASTEL NỮ TÍNH, MỀM MẠI, DỄ THƯƠNG ---
st.markdown("""
<style>
    /* 1. ẨN HOÀN TOÀN HEADER & GIAO DIỆN MẶC ĐỊNH */
    #MainMenu {visibility: hidden; display: none !important;}
    header[data-testid="stHeader"] {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden; display: none !important;}
    [data-testid="stDecoration"] {visibility: hidden; display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none !important;}

    /* 2. BACKGROUND GRADIENT PASTEL HỒNG PHẤN & KEM ĐÀO MỘNG MƠ */
    .stApp {
        background: linear-gradient(140deg, #FFF1F5 0%, #FDF4FF 30%, #FFF7ED 65%, #F0FDF4 100%);
        background-attachment: fixed;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* 3. KHUNG TRUNG TÂM MOBILE-FIRST */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
        max-width: 660px;
        margin: auto;
    }

    /* 4. TIÊU ĐỀ NỮ TÍNH, THANH LỊCH & NGỌT NGÀO */
    .hero-title-box {
        text-align: center;
        padding: 20px 10px 12px 10px;
        margin-bottom: 12px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #FFE4E6 0%, #FCE7F3 100%);
        color: #BE185D;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.8px;
        padding: 5px 16px;
        border-radius: 999px;
        box-shadow: 0 2px 8px rgba(244, 63, 94, 0.12);
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #881337;
        margin: 0;
        text-shadow: 0 2px 10px rgba(136, 19, 55, 0.08);
    }
    .hero-subtitle {
        font-size: 13.5px;
        color: #9D174D;
        margin-top: 6px;
        margin-bottom: 0;
        font-weight: 500;
        opacity: 0.85;
    }

    /* 5. Ô NHẬP LIỆU BO TRÒN MỀM MẠI */
    div[data-testid="stTextInput"] input {
        border-radius: 20px !important;
        border: 1.5px solid #FBCFE8 !important;
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 10px 18px !important;
        color: #4C0519 !important;
        box-shadow: 0 2px 8px rgba(244, 63, 94, 0.04) !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #F43F5E !important;
        box-shadow: 0 0 0 3px rgba(244, 63, 94, 0.15) !important;
    }

    /* 6. NÚT DÀN HÀNG NGANG PASTEL HỒNG DỊU DÀNG */
    div[data-testid="stRadio"] > div {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 8px;
    }
    div[data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(8px);
        padding: 8px 18px;
        border-radius: 22px;
        border: 1.5px solid #FCE7F3;
        cursor: pointer;
        font-weight: 600;
        font-size: 13.5px;
        color: #9D174D;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 0 !important;
        box-shadow: 0 2px 8px rgba(244, 63, 94, 0.05);
    }
    div[data-testid="stRadio"] label:hover {
        background: #FFF1F2;
        border-color: #FDA4AF;
        color: #BE123C;
        transform: translateY(-1.5px);
        box-shadow: 0 4px 14px rgba(244, 63, 94, 0.12);
    }

    /* 7. FLASHCARD 3D PASTEL NỮ TÍNH */
    .flashcard-wrapper {
        perspective: 1200px;
        margin: 14px auto;
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
        border-radius: 28px;
        padding: 26px 24px;
        box-shadow: 0 14px 35px rgba(244, 63, 94, 0.09), 0 4px 12px rgba(251, 113, 133, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }

    /* MẶT TRƯỚC: HỒNG PASTEL PHA TÍM NHẸ DỄ THƯƠNG */
    .flashcard-front {
        background: linear-gradient(145deg, #FFF5F7 0%, #FAF5FF 100%);
        border: 2px solid #FBCFE8;
        text-align: center;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
    }

    /* MẶT SAU: KEM TRẮNG SỨ VIỀN ĐÀO MỀM MẠI */
    .flashcard-back {
        background: rgba(255, 255, 255, 0.97);
        border: 2px solid #FED7AA;
        transform: rotateY(180deg);
        overflow-y: auto;
        text-align: left;
        backdrop-filter: blur(10px);
    }

    .chinese-word {
        font-size: 56px;
        font-weight: 800;
        color: #881337;
        margin: 0;
        line-height: 1.2;
        letter-spacing: 1.5px;
    }
    .pinyin-word {
        font-size: 22px;
        color: #BE185D;
        margin-top: 8px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    /* 8. NÚT STREAMLIT BO TRÒN DỄ THƯƠNG */
    div.stButton > button {
        border-radius: 22px !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease !important;
        border: 1.5px solid #FCE7F3 !important;
        box-shadow: 0 2px 8px rgba(244, 63, 94, 0.06) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1.5px) !important;
        box-shadow: 0 4px 14px rgba(244, 63, 94, 0.15) !important;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #FB7185 0%, #F43F5E 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
    }

    /* 9. KHUNG THẺ TỪ MỤC LỤC CHI TIẾT */
    .vocab-card {
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(8px);
        border: 1.5px solid #FCE7F3;
        border-radius: 24px;
        padding: 22px 24px;
        margin-bottom: 18px;
        box-shadow: 0 6px 20px rgba(244, 63, 94, 0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .vocab-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(244, 63, 94, 0.12);
        border-color: #FBCFE8;
    }
    .vocab-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .vocab-card-title {
        font-size: 28px;
        font-weight: 800;
        color: #881337;
        margin: 0;
    }
    .vocab-card-pinyin {
        font-size: 16px;
        color: #BE185D;
        margin-top: 2px;
        margin-bottom: 10px;
        font-style: italic;
    }
    .vocab-card-meaning {
        font-size: 16px;
        font-weight: 700;
        color: #059669;
        margin-bottom: 10px;
    }
    .vocab-card-colloc {
        font-size: 14px;
        color: #475569;
        line-height: 1.6;
    }
    .vocab-card-example {
        background: #FFF7ED;
        border-left: 3.5px solid #FB923C;
        border-radius: 12px;
        padding: 10px 14px;
        margin-top: 10px;
        font-size: 13.5px;
        color: #9A3412;
        line-height: 1.55;
    }

    .colloc-item {
        background-color: #FFF1F2;
        border-left: 3px solid #FB7185;
        padding: 6px 12px;
        margin: 5px 0;
        border-radius: 10px;
        font-size: 13.5px;
        color: #4C0519;
    }
    .example-box {
        background-color: #FFF7ED;
        border-radius: 14px;
        padding: 11px 14px;
        margin-top: 10px;
        font-size: 13px;
        color: #9A3412;
        line-height: 1.55;
    }

    /* THANH TIẾN ĐỘ PASTEL */
    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #F472B6 0%, #FB7185 100%) !important;
        border-radius: 99px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU TỔNG 26 TỪ CỐT LÕI ---
VOCAB_DATA = [
    {
        "id": 1,
        "word": "工厂", "pinyin": "gōngchǎng", "meaning": "nhà máy, công xưởng",
        "collocations": ["参观工厂 (cānguān gōngchǎng) — tham quan nhà máy", "工厂规模 (gōngchǎng guīmó) — quy mô nhà xưởng", "现代化工厂 (xiàndàihuà gōngchǎng) — nhà máy hiện đại"],
        "example": "欢迎各位领导来我们工厂参观考察。(Huānyíng gèwèi lǐngdǎo lái wǒmen gōngchǎng cānguān kǎochá.) — Hoan nghênh các vị lãnh đạo đến tham quan khảo sát nhà máy chúng tôi."
    },
    {
        "id": 2,
        "word": "车间", "pinyin": "chējiān", "meaning": "phân xưởng sản xuất",
        "collocations": ["生产车间 (shēngchǎn chējiān) — phân xưởng sản xuất", "无尘车间 (wúchén chējiān) — phòng sạch", "总装车间 (zǒngzhuāng chējiān) — xưởng lắp ráp tổng"],
        "example": "进入生产车间之前，所有人必须戴好安全帽。(Jìnrù shēngchǎn chējiān zhīqián, suǒyǒu rén bìxū dài hǎo ānquánmào.) — Trước khi vào xưởng sản xuất, tất cả mọi người phải đội mũ bảo hộ."
    },
    {
        "id": 3,
        "word": "办公大楼", "pinyin": "bàngōng dàlóu", "meaning": "tòa nhà văn phòng hành chính",
        "collocations": ["行政大楼 (xíngzhèng dàlóu) — tòa nhà hành chính", "佩戴厂牌 (pèidài chǎngpái) — đeo thẻ công xưởng", "总经办 (zǒngjīngbàn) — văn phòng tổng giám đốc"],
        "example": "行政部门都在这栋办公大楼里面办公。(Xíngzhèng bùmén dōu zài zhè dòng bàngōng dàlóu lǐmiàn bàngōng.) — Các bộ phận hành chính đều làm việc trong tòa văn phòng này."
    },
    {
        "id": 4,
        "word": "仓库", "pinyin": "cāngkù", "meaning": "kho bãi, nhà kho",
        "collocations": ["原料仓库 (yuánliào cāngkù) — kho nguyên liệu", "成品仓库 (chéngpǐn cāngkù) — kho thành phẩm", "月底盘点 (yuèdǐ pándiǎn) — kiểm kê kho cuối tháng"],
        "example": "原料仓库在工厂东侧，靠近卸货平台。(Yuánliào cāngkù zài gōngchǎng dōng cè, kàojìn xièhuò píngtái.) — Kho nguyên liệu nằm ở phía đông nhà máy, sát ngay sàn bốc dỡ hàng."
    },
    {
        "id": 5,
        "word": "设备", "pinyin": "shèbèi", "meaning": "thiết bị, máy móc",
        "collocations": ["先进设备 (xiānjìn shèbèi) — thiết bị tiên tiến", "自动化设备 (zìdònghuà shèbèi) — thiết bị tự động hóa", "数控机床 (shùkòng jīchuáng) — máy gia công CNC"],
        "example": "车间里大部分生产设备都是从德国引进的。(Chējiān lǐ dà bùfen shēngchǎn shèbèi dōu shì cóng Déguó yǐnjìn de.) — Phần lớn thiết bị trong xưởng đều được nhập khẩu từ Đức."
    },
    {
        "id": 6,
        "word": "流水线", "pinyin": "liúshuǐxiàn", "meaning": "dây chuyền sản xuất lắp ráp",
        "collocations": ["自动化流水线 (zìdònghuà liúshuǐxiàn) — dây chuyền tự động", "流水线作业 (liúshuǐxiàn zuòyè) — thao tác trên chuyền", "流水线装配 (liúshuǐxiàn zhuāngpèi) — lắp ráp trên dây chuyền"],
        "example": "目前一号车间拥有八条全自动流水线。(Mùqián yī hào chējiān yōngyǒu bā tiáo quán zìdòng liúshuǐxiàn.) — Hiện tại xưởng số 1 sở hữu 8 dây chuyền tự động hóa hoàn toàn."
    },
    {
        "id": 7,
        "word": "生产部", "pinyin": "shēngchǎn bù", "meaning": "bộ phận sản xuất",
        "collocations": ["安排生产 (ānpái shēngchǎn) — bố trí lịch sản xuất", "生产能力 (shēngchǎn nénglì) — năng lực sản xuất", "生产进度 (shēngchǎn jìndù) — tiến độ sản xuất"],
        "example": "生产部主要负责按照订单保质保量完成任务。(Shēngchǎn bù zhǔyào fùzé ànzhào dìngdān bǎozhì bǎoliàng wánchéng rènwù.) — Bộ phận sản xuất phụ trách hoàn thành đơn hàng bảo đảm chất và lượng."
    },
    {
        "id": 8,
        "word": "生产主管", "pinyin": "shēngchǎn zhǔguǎn", "meaning": "chủ quản sản xuất",
        "collocations": ["车间主管 (chējiān zhǔguǎn) — chủ quản xưởng", "布置任务 (bùzhì rènwù) — giao nhiệm vụ sản xuất", "开早会 (kāi zǎohuì) — họp giao ban sáng"],
        "example": "生产主管正在和产线组长开早会。(Shēngchǎn zhǔguǎn zhèngzài hé chǎnxiàn zǔzhǎng kāi zǎohuì.) — Chủ quản sản xuất đang họp giao ban sáng với các tổ trưởng chuyền."
    },
    {
        "id": 9,
        "word": "产线组长", "pinyin": "chǎnxiàn zǔzhǎng", "meaning": "tổ trưởng chuyền sản xuất",
        "collocations": ["车间组长 (chējiān zǔzhǎng) — tổ trưởng xưởng", "巡视产线 (xúnshì chǎnxiàn) — đi tuần kiểm chuyền", "跟催进度 (gēncuī jìndù) — đôn đốc tiến độ"],
        "example": "产线组长负责管理现场作业员并监督产量。(Chǎnxiàn zǔzhǎng fùzé guǎnlǐ xiànchǎng zuòyèyuán bìng jiāndū chǎnliàng.) — Tổ trưởng chuyền quản lý công nhân và giám sát sản lượng."
    },
    {
        "id": 10,
        "word": "作业员", "pinyin": "zuòyèyuán", "meaning": "công nhân thao tác trực tiếp, thợ đứng chuyền",
        "collocations": ["一线作业员 (yīxiàn zuòyèyuán) — công nhân tuyến đầu", "操作规程 (cāozuò guīchéng) — quy trình thao tác", "严格遵守 (yángé zūnshǒu) — tuân thủ nghiêm ngặt"],
        "example": "作业员在工位上必须严格遵守操作规程。(Zuòyèyuán zài gōngwèi shàng bìxū yángé zūnshǒu cāozuò guīchéng.) — Công nhân tại vị trí làm việc bắt buộc phải tuân thủ nghiêm quy trình."
    },
    {
        "id": 11,
        "word": "品质部", "pinyin": "pǐnzhì bù", "meaning": "bộ phận quản lý chất lượng (QC/QA)",
        "collocations": ["品质主管 (pǐnzhì zhǔguǎn) — chủ quản chất lượng", "严格把关 (yángé bǎguān) — kiểm soát chặt chẽ", "不良品 (bùliángpǐn) — hàng phế phẩm, hàng lỗi"],
        "example": "如果品质部判定不合格，货物绝对不能出厂。(Rúguǒ pǐnzhì bù pàndìng bù hégé, huòwù juéduì bùnéng chūchǎng.) — Nếu bộ phận QC đánh giá không đạt, hàng tuyệt đối không được xuất xưởng."
    },
    {
        "id": 12,
        "word": "质检员", "pinyin": "zhìjiǎnyuán", "meaning": "nhân viên kiểm tra chất lượng (QC)",
        "collocations": ["巡检 (xúnjiǎn) — đi tuần tra kiểm tra", "首件确认 (shǒujiàn quèrèn) — duyệt mẫu sản phẩm đầu", "检验报告 (jiǎnyàn bàogào) — báo cáo kiểm phẩm"],
        "example": "质检员正在产线上抽检产品的外观和尺寸。(Zhìjiǎnyuán zhèngzài chǎnxiàn shàng chōujiǎn chǎnpǐn de wàiguān hé chǐcunn.) — Nhân viên QC đang rút mẫu kiểm tra ngoại quan và kích thước trên chuyền."
    },
    {
        "id": 13,
        "word": "工程部", "pinyin": "gōngchéng bù", "meaning": "bộ phận kỹ thuật, công trình",
        "collocations": ["设备工程师 (shèbèi gōngchéngshī) — kỹ sư thiết bị", "改善工艺 (gǎishàn gōngyì) — cải tiến công nghệ", "技术支持 (jìshù zhīchí) — hỗ trợ mặt kỹ thuật"],
        "example": "工程部负责制定新产品的作业指导书。(Gōngchéng bù fùzé zhìdìng xīn chǎnpǐn de zuòyè zhǐdǎoshū.) — Phòng kỹ thuật phụ trách soạn thảo tài liệu SOP cho sản phẩm mới."
    },
    {
        "id": 14,
        "word": "技术员", "pinyin": "jìshùyuán", "meaning": "kỹ thuật viên (chỉnh máy, bảo trì khuôn)",
        "collocations": ["现场调机 (xiànchǎng tiáojī) — căn chỉnh máy hiện trường", "维修模具 (wéixiū mójù) — sửa chữa khuôn", "排除故障 (páichú gùzhàng) — khắc phục sự cố máy"],
        "example": "机台出现故障，技术员马上过来调机。(Jītái chūxiàn gùzhàng, jìshùyuán mǎshàng guòlái tiáojī.) — Máy móc gặp sự cố, kỹ thuật viên lập tức qua căn chỉnh máy."
    },
    {
        "id": 15,
        "word": "生管部", "pinyin": "shēngguǎn bù", "meaning": "bộ phận sinh quản (PMC - Kế hoạch & Điều độ)",
        "collocations": ["生管排产 (shēngguǎn páichǎn) — sinh quản lên lịch sản xuất", "核对交期 (héduì jiāoqī) — đối chiếu hạn giao hàng", "产能评估 (chánnéng pínggū) — đánh giá năng suất xưởng"],
        "example": "生管部正在根据订单安排下周的排产计划。(Shēngguǎn bù zhèngzài gēnjù dìngdān ānpái xià zhōu de páichǎn jìhuà.) — Phòng sinh quản đang sắp xếp lịch sản xuất tuần tới theo đơn hàng."
    },
    {
        "id": 16,
        "word": "采购部", "pinyin": "cǎigòu bù", "meaning": "bộ phận thu mua",
        "collocations": ["寻找供应商 (xúnzhǎo gōngyìngshāng) — tìm nhà cung cấp", "询价采购 (xúnjià cǎigòu) — hỏi giá thu mua", "采购订单 (cǎigòu dìngdān) — đơn đặt mua hàng (PO)"],
        "example": "物料短缺时，采购部要第一时间催促供应商交货。(Wùliào duǎnquē shí, cǎigòu bù yào dì-yī shíjiān cuīcù gōngyìngshāng jiāohuò.) — Khi thiếu vật tư, phòng thu mua phải giục nhà cung cấp giao hàng ngay."
    },
    {
        "id": 17,
        "word": "仓管员", "pinyin": "cāngguǎnyuán", "meaning": "thủ kho, nhân viên quản lý kho",
        "collocations": ["办理入库 (bànlǐ rùkù) — làm thủ tục nhập kho", "核对库存 (héduì kùcún) — đối chiếu lượng tồn kho", "库存报表 (kùcún bàobiǎo) — báo cáo tồn kho"],
        "example": "仓管员核对送货单后才办理原材料入库。(Cāngguǎnyuán héduì sònghuòdān hòu cái bànlǐ yuáncáiliào rùkù.) — Thủ kho đối chiếu phiếu giao hàng xong mới làm thủ tục nhập kho."
    },
    {
        "id": 18,
        "word": "物料员", "pinyin": "wùliàoyuán", "meaning": "nhân viên tiếp liệu, cấp phát vật tư",
        "collocations": ["凭单领料 (píngdān lǐngliào) — lĩnh liệu theo phiếu", "现场配送 (xiànchǎng pèisòng) — phát vật tư tại chỗ", "领料单 (lǐngliàodān) — phiếu lĩnh vật tư"],
        "example": "产线物料员拿着领料单去仓库领配件。(Chǎnxiàn wùliàoyuán názhe lǐngliàodān qù cāngkù lǐng pèijiàn.) — Nhân viên tiếp liệu của chuyền cầm phiếu lĩnh liệu lên kho nhận linh kiện."
    },
    {
        "id": 19,
        "word": "研发部", "pinyin": "yánfā bù", "meaning": "bộ phận nghiên cứu và phát triển (R&D)",
        "collocations": ["研发中心 (yánfā zhōngxīn) — trung tâm R&D", "打样员 (dǎyàngyuán) — nhân viên làm mẫu thử", "新产品开发 (xīn chǎnpǐn kāifā) — phát triển sản phẩm mới"],
        "example": "研发部负责根据客户样品进行图纸设计。(Yánfā bù fùzé gēnjù kèhù yàngpǐn jìnxíng túzhǐ shèjì.) — Phòng R&D phụ trách thiết kế bản vẽ dựa theo mẫu của khách hàng."
    },
    {
        "id": 20,
        "word": "安全帽", "pinyin": "ānquánmào", "meaning": "mũ bảo hộ lao động",
        "collocations": ["佩戴安全帽 (pèidài ānquánmào) — đội mũ bảo hộ", "劳保用品 (láobǎo yòngpǐn) — đồ bảo hộ lao động", "安全规范 (ānquán guīfàn) — quy chuẩn an toàn"],
        "example": "不戴安全帽，严禁进入生产车间！(Bù dài ānquánmào, yánjìn jìnrù shēngchǎn chējiān!) — Không đội mũ bảo hộ, nghiêm cấm bước vào xưởng sản xuất!"
    },
    {
        "id": 21,
        "word": "收到", "pinyin": "shōudào", "meaning": "đã nhận được (chỉ thị, thông báo)",
        "collocations": ["收到指示 (shōudào zhǐshì) — đã nhận được chỉ thị", "收到通知 (shōudào tōngzhī) — đã nhận thông báo", "收到回复 (shōudào huífù) — đã nhận phản hồi"],
        "example": "收到，我马上安排车间组长挑选不良品。(Shōudào, wǒ mǎshàng ānpái chējiān zǔzhǎng tiāoxuǎn bùliángpǐn.) — Đã nhận, tôi bố trí tổ trưởng lựa hàng lỗi ra ngay."
    },
    {
        "id": 22,
        "word": "马上", "pinyin": "mǎshàng", "meaning": "ngay lập tức",
        "collocations": ["马上处理 (mǎshàng chǔlǐ) — xử lý ngay lập tức", "马上跟进 (mǎshàng gēnjìn) — bám sát tiến độ ngay", "马上核实 (mǎshàng héshí) — xác minh lại ngay"],
        "example": "收到通知，我马上通知产线组织加班。(Shōudào tōngzhī, wǒ mǎshàng tōngzhī chǎnxiàn zǔzhī jiābān.) — Nhận thông báo, tôi lập tức báo chuyền tăng ca ngay."
    },
    {
        "id": 23,
        "word": "核对", "pinyin": "héduì", "meaning": "đối chiếu, so sánh kiểm tra lại",
        "collocations": ["核对物料 (héduì wùliào) — đối chiếu vật tư", "核对数量 (héduì shùliàng) — đối chiếu số lượng", "麻烦核对 (máfan héduì) — phiền đối chiếu giúp"],
        "example": "麻烦仓库帮忙核对这批面料的实际库存。(Máfan cāngkù bāngmáng héduì zhè pī miànliào de shíjì kùcún.) — Phiền kho hỗ trợ đối chiếu lượng tồn kho thực tế của lô vải này."
    },
    {
        "id": 24,
        "word": "发", "pinyin": "fā", "meaning": "gửi (tin nhắn, mail), phát (vật liệu)",
        "collocations": ["发群里 (fā qún lǐ) — gửi vào trong nhóm", "发料单 (fāliàodān) — phiếu cấp phát vật tư", "发邮件 (fā yóujiàn) — gửi email"],
        "example": "生产日报表已经发群里，请主管查阅。(Shēngchǎn rì bàobiǎo yǐjīng fā qún lǐ, qǐng zhǔguǎn cháyuè.) — Báo cáo ngày đã gửi vào nhóm, mời chủ quản duyệt."
    },
    {
        "id": 25,
        "word": "确认", "pinyin": "quèrèn", "meaning": "xác nhận",
        "collocations": ["请确认 (qǐng quèrèn) — xin vui lòng xác nhận", "签字确认 (qiānzì quèrèn) — ký tên xác nhận", "首件确认 (shǒujiàn quèrèn) — duyệt mẫu đầu chuyền"],
        "example": "排产计划已发群里，请各位主管确认。(Páichǎn jìhuà yǐ fā qún lǐ, qǐng gèwèi zhǔguǎn quèrèn.) — Lịch sản xuất đã gửi nhóm, xin các chủ quản xác nhận giúp."
    },
    {
        "id": 26,
        "word": "异常", "pinyin": "yìcháng", "meaning": "bất thường, sự cố phát sinh",
        "collocations": ["现场异常 (xiànchǎng yìcháng) — sự cố tại hiện trường", "品质异常 (pǐnzhì yìcháng) — bất thường chất lượng", "异常反馈 (yìcháng fǎnkuì) — báo cáo sự cố"],
        "example": "产线一有异常，必须立刻向上级汇报。(Chǎnxiàn yī yǒu yìcháng, bìxū lìkè xiàng shàngjí huìbào.) — Chuyền có sự cố là phải lập tức báo cáo cấp trên ngay."
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
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# STATE CHO TRẮC NGHIỆM TỪNG CÂU
if "quiz_active_idx" not in st.session_state:
    st.session_state.quiz_active_idx = 0
if "quiz_list" not in st.session_state:
    st.session_state.quiz_list = []
if "quiz_answered_correctly" not in st.session_state:
    st.session_state.quiz_answered_correctly = False
if "quiz_error_msg" not in st.session_state:
    st.session_state.quiz_error_msg = ""
if "quiz_wrong_attempts" not in st.session_state:
    st.session_state.quiz_wrong_attempts = 0

# --- TIÊU ĐỀ TRANG TRÍ VỚI NÉT NỮ TÍNH DỄ THƯƠNG ---
st.markdown("""
<div class="hero-title-box">
    <div class="hero-badge">🌸 TIẾNG TRUNG CÔNG XƯỞNG THỰC CHIẾN ✨</div>
    <h1 class="hero-title">TIẾNG TRUNG CÔNG XƯỞNG</h1>
    <p class="hero-subtitle">Góc học từ vựng & luyện phản xạ nhà xưởng nhẹ nhàng, thanh lịch 🌷</p>
</div>
""", unsafe_allow_html=True)

# Ô NHẬP TÊN HỌC VIÊN
s_name = st.text_input("🌷 Họ tên học viên:", value=st.session_state.student_name, placeholder="Ví dụ: Diệu Linh, Minh Anh...")
if s_name:
    st.session_state.student_name = s_name.strip()

# --- 1. PHẠM VI BÀI HỌC (GỘP CHUNG) ---
st.markdown("**Phạm vi từ vựng:**")
scope_choice = st.radio(
    "scope_radio",
    ["Tất cả từ cốt lõi (26 từ)"],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)
current_vocab = VOCAB_DATA

# --- 2. DÀN HÀNG NGANG: CHẾ ĐỘ LUYỆN TẬP ---
st.markdown("**Chế độ luyện tập:**")
mode_choice = st.radio(
    "mode_radio",
    ["Thẻ từ", "Trắc nghiệm", "Nối từ", "Mục lục từ", "Lịch sử"],
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

st.markdown(f"🌸 **Tiến độ học tập:** 📚 Tổng: **{total_words}** từ | ✓ Đã thuộc: **{learned_count}/{total_words}** | ⚡ Cần ôn: **{failed_count}/{total_words}** | 🎯 Thuộc: **{pct}%**")
st.progress(pct / 100)
st.markdown("---")

# ==================== CHẾ ĐỘ 1: THẺ TỪ (LẬT 3D + LẬT NGẪU NHIÊN) ====================
if mode_choice == "Thẻ từ":
    if total_words == 0:
        st.warning("Không có từ nào trong danh mục.")
    else:
        if st.session_state.card_idx >= total_words:
            st.session_state.card_idx = 0

        top_btn1, top_btn2 = st.columns(2)
        with top_btn1:
            st.caption(f"Thẻ hiện tại: **{st.session_state.card_idx + 1} / {total_words}** 🎀")
        with top_btn2:
            if st.button("🎲 Xáo thẻ ngẫu nhiên", use_container_width=True):
                st.session_state.card_idx = random.randint(0, total_words - 1)
                st.rerun()

        cur_word = current_vocab[st.session_state.card_idx]
        colloc_html = "".join([f"<div class='colloc-item'>• {c}</div>" for c in cur_word["collocations"]])

        flashcard_html = f"""
        <div class="flashcard-wrapper">
            <label>
                <input type="checkbox" class="flashcard-toggle" id="card_{cur_word['id']}_{st.session_state.card_idx}">
                <div class="flashcard-inner">
                    <!-- MẶT TRƯỚC -->
                    <div class="flashcard-face flashcard-front">
                        <span style="background:rgba(255, 255, 255, 0.85); color:#BE185D; padding:5px 16px; border-radius:99px; font-size:12px; font-weight:700; border: 1px solid #FBCFE8;">TỪ VỰNG #{cur_word['id']} 🌸</span>
                        <div style="flex-grow:1; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                            <h1 class="chinese-word">{cur_word['word']}</h1>
                            <div class="pinyin-word">{cur_word['pinyin']}</div>
                        </div>
                        <div style="color: #BE185D; font-size: 13px; opacity: 0.8;">✨ <b>Chạm nhẹ vào thẻ để lật mặt sau</b></div>
                    </div>
                    <!-- MẶT SAU -->
                    <div class="flashcard-face flashcard-back">
                        <div>
                            <div>
                                <h3 style="margin:0; color:#881337; display:inline;">{cur_word['word']}</h3>
                                <span style="font-size:16px; color:#BE185D; margin-left:8px; font-style:italic;">{cur_word['pinyin']}</span>
                            </div>
                            <div style="color:#059669; font-weight:700; font-size:17px; margin:8px 0 10px 0;">👉 {cur_word['meaning']}</div>
                            <div style="font-size:13px; font-weight:600; color:#475569; margin-bottom:4px;">🔗 Cụm từ hay dùng:</div>
                            {colloc_html}
                            <div class="example-box">💬 <b>Ví dụ thực tế:</b><br>{cur_word['example']}</div>
                        </div>
                        <div style="color: #FB923C; font-size: 13px; text-align: center; margin-top: 10px;">✨ <b>Chạm lại để xem chữ Hán</b></div>
                    </div>
                </div>
            </label>
        </div>
        """
        st.markdown(flashcard_html, unsafe_allow_html=True)

        # HÀNG 3 NÚT ĐIỀU HƯỚNG PASTEL DỄ THƯƠNG
        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            if st.button("🌸 Đã thuộc", type="primary", use_container_width=True):
                st.session_state.learned_ids.add(cur_word["id"])
                st.session_state.failed_ids.discard(cur_word["id"])
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.rerun()
        with btn2:
            if st.button("🌱 Cần ôn lại", use_container_width=True):
                st.session_state.failed_ids.add(cur_word["id"])
                st.session_state.learned_ids.discard(cur_word["id"])
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.rerun()
        with btn3:
            if st.button("⏭️ Thẻ sau", use_container_width=True):
                st.session_state.card_idx = (st.session_state.card_idx + 1) % total_words
                st.rerun()

# ==================== CHẾ ĐỘ 2: TRẮC NGHIỆM TỪNG CÂU ====================
elif mode_choice == "Trắc nghiệm":
    st.markdown("##### ✍️ Trắc nghiệm phản xạ từng câu")

    if len(st.session_state.quiz_list) == 0 or st.button("🎲 Tạo bài kiểm tra mới (10 câu)"):
        sample_size = min(10, len(current_vocab))
        sampled = random.sample(current_vocab, sample_size)
        new_quiz = []
        for item in sampled:
            wrong_pool = [w["meaning"] for w in VOCAB_DATA if w["id"] != item["id"]]
            distractors = random.sample(wrong_pool, 3)
            options = distractors + [item["meaning"]]
            random.shuffle(options)
            new_quiz.append({
                "id": item["id"],
                "word": item["word"],
                "pinyin": item["pinyin"],
                "correct": item["meaning"],
                "options": options
            })
        st.session_state.quiz_list = new_quiz
        st.session_state.quiz_active_idx = 0
        st.session_state.quiz_answered_correctly = False
        st.session_state.quiz_error_msg = ""
        st.session_state.quiz_wrong_attempts = 0
        st.rerun()

    total_q = len(st.session_state.quiz_list)
    cur_q_idx = st.session_state.quiz_active_idx

    if cur_q_idx >= total_q:
        st.balloons()
        st.success(f"🎉 **Chúc mừng bạn đã hoàn thành xuất sắc toàn bộ {total_q} câu trắc nghiệm!** 🌸")
        st.markdown(f"Tổng số lần chọn nhầm trong cả bài: **{st.session_state.quiz_wrong_attempts} lần**")

        save_history({
            "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "name": st.session_state.student_name if st.session_state.student_name else "Ẩn danh",
            "type": "Trắc nghiệm từng câu",
            "scope": "Toàn bộ từ vựng (26)",
            "score": f"Đạt {total_q}/{total_q} câu (Lỗi: {st.session_state.quiz_wrong_attempts})"
        })

        if st.button("🔄 Luyện tập lại từ đầu", type="primary", use_container_width=True):
            st.session_state.quiz_list = []
            st.rerun()
    else:
        q_item = st.session_state.quiz_list[cur_q_idx]

        st.caption(f"Tiến độ câu hỏi: **Câu {cur_q_idx + 1} / {total_q}** 🎀")
        st.progress((cur_q_idx) / total_q)

        with st.container(border=True):
            st.markdown(f"""
            <h2 style="color:#881337; margin:0 0 6px 0;">{q_item['word']} <span style="font-size:18px; color:#BE185D; font-weight:normal; font-style:italic;">({q_item['pinyin']})</span></h2>
            <p style="color:#475569; margin:4px 0 12px 0; font-size:15px;">👉 Từ trên có nghĩa là gì?</p>
            """, unsafe_allow_html=True)

            selected_answer = st.radio(
                "Lựa chọn đáp án:",
                q_item["options"],
                key=f"radio_q_{cur_q_idx}",
                label_visibility="collapsed"
            )

            if not st.session_state.quiz_answered_correctly:
                if st.button("Kiểm tra đáp án 🌸", type="primary", use_container_width=True):
                    if selected_answer == q_item["correct"]:
                        st.session_state.quiz_answered_correctly = True
                        st.session_state.quiz_error_msg = ""
                        st.session_state.learned_ids.add(q_item["id"])
                        st.rerun()
                    else:
                        st.session_state.quiz_wrong_attempts += 1
                        st.session_state.quiz_error_msg = f"❌ Bạn chọn '{selected_answer}' chưa chính xác. Đừng nản lòng, hãy chọn lại nhé! 💕"
                        st.session_state.failed_ids.add(q_item["id"])
                        st.rerun()

            if st.session_state.quiz_error_msg:
                st.error(st.session_state.quiz_error_msg)

            if st.session_state.quiz_answered_correctly:
                st.success(f"✓ Giỏi quá! **{q_item['word']}** nghĩa là: **{q_item['correct']}** 🌷")
                next_label = "➡️ Câu tiếp theo" if (cur_q_idx + 1 < total_q) else "🏁 Hoàn thành bài kiểm tra"
                if st.button(next_label, type="primary", use_container_width=True):
                    st.session_state.quiz_active_idx += 1
                    st.session_state.quiz_answered_correctly = False
                    st.session_state.quiz_error_msg = ""
                    st.rerun()

# ==================== CHẾ ĐỘ 3: NỐI TỪ ====================
elif mode_choice == "Nối từ":
    st.markdown("##### 🧩 Trò chơi Nối từ phản xạ")

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

    st.caption("Chọn nghĩa tương ứng cho từng từ tiếng Trung:")
    user_match = {}
    with st.form("match_form"):
        for w_text in st.session_state.match_words:
            entry = next(item for item in st.session_state.match_items if item["word"] == w_text)
            st.markdown(f"👉 Từ: <b style='font-size:18px; color:#881337;'>{w_text}</b> <i style='color:#BE185D;'>({entry['pinyin']})</i>", unsafe_allow_html=True)
            user_match[w_text] = st.selectbox(
                f"Nghĩa của {w_text}:",
                ["-- Chọn nghĩa phù hợp --"] + st.session_state.match_meanings,
                key=f"match_{w_text}",
                label_visibility="collapsed"
            )
            st.write("")

        if st.form_submit_button("Kiểm tra kết quả nối từ 🌸", type="primary", use_container_width=True):
            m_score = 0
            for item in st.session_state.match_items:
                if user_match[item["word"]] == item["meaning"]:
                    m_score += 1
                    st.session_state.learned_ids.add(item["id"])
                else:
                    st.session_state.failed_ids.add(item["id"])

            total_m = len(st.session_state.match_items)
            st.success(f"Tuyệt vời! Bạn đã ghép đúng **{m_score}/{total_m}** cặp từ! 🌷")

            save_history({
                "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "name": st.session_state.student_name if st.session_state.student_name else "Ẩn danh",
                "type": "Nối từ",
                "scope": "Toàn bộ từ vựng (26)",
                "score": f"{m_score}/{total_m} cặp"
            })

# ==================== CHẾ ĐỘ 4: MỤC LỤC TỪ (CARD VIEW) ====================
elif mode_choice == "Mục lục từ":
    st.markdown("##### 📖 Mục lục từ vựng dễ nhớ")
    search_txt = st.text_input("🔍 Tìm kiếm từ:", placeholder="Nhập Hán tự, Pinyin hoặc Tiếng Việt...")

    filtered = current_vocab
    if search_txt:
        q = search_txt.strip().lower()
        filtered = [w for w in current_vocab if q in w["word"].lower() or q in w["pinyin"].lower() or q in w["meaning"].lower()]

    st.caption(f"Hiển thị **{len(filtered)}** từ vựng theo dạng thẻ pastel mềm mại:")

    for w in filtered:
        collocs_str = "".join([f"<div class='vocab-card-colloc'>• {c}</div>" for c in w["collocations"]])
        card_html = f"""
        <div class="vocab-card">
            <div class="vocab-card-header">
                <span class="vocab-card-title">{w['word']}</span>
                <span style="font-size:12px; background:#FFE4E6; color:#BE185D; font-weight:700; padding:4px 12px; border-radius:99px;">#{w['id']}</span>
            </div>
            <div class="vocab-card-pinyin">{w['pinyin']}</div>
            <div class="vocab-card-meaning">➔ {w['meaning']}</div>
            {collocs_str}
            <div class="vocab-card-example">
                💬 {w['example']}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# ==================== CHẾ ĐỘ 5: LỊCH SỬ ====================
elif mode_choice == "Lịch sử":
    st.markdown("##### 📊 Lịch sử ôn tập của bạn")
    h_data = load_history()

    if not h_data:
        st.info("Chưa có lịch sử làm bài. Hãy thử một bài ở phần 'Trắc nghiệm' hoặc 'Nối từ' để lưu nhật ký học tập nhé! 💕")
    else:
        df_h = pd.DataFrame(h_data)
        df_h.columns = ["Thời gian", "Học viên", "Chế độ", "Phạm vi", "Kết quả"]
        st.dataframe(df_h, use_container_width=True, hide_index=True)

        if st.button("🗑️ Xóa toàn bộ lịch sử", type="secondary"):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
            st.rerun()
