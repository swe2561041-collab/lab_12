"""Лаборатори 12 — Такси дуудлагын систем: Word тайлан үүсгэх."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIAG = os.path.join(BASE, "docs", "diagrams")
OUT_FILE = os.path.join(BASE, "docs", "lab12-taxi-architecture.docx")

NAVY = RGBColor(0x1F, 0x38, 0x64)
GREY = RGBColor(0x47, 0x55, 0x69)
ACCENT = RGBColor(0x1D, 0x4E, 0xD8)


# --------------------------------------------------------------------------- #
# Туслах функцууд
# --------------------------------------------------------------------------- #
def shade(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def cell_text(cell, text, bold=False, size=9.5, color=None, align=None):
    cell.text = ""
    para = cell.paragraphs[0]
    if align is not None:
        para.alignment = align
    para.paragraph_format.space_before = Pt(2)
    para.paragraph_format.space_after = Pt(2)
    run = para.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = "Calibri"
    if color is not None:
        run.font.color.rgb = color


def add_table(doc, headers, rows, widths, header_fill="1F3864", font_size=9.5,
              first_col_bold=False, zebra="F2F5FA"):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    hdr = table.rows[0].cells
    for i, head in enumerate(headers):
        cell_text(hdr[i], head, bold=True, size=font_size, color=RGBColor(0xFF, 0xFF, 0xFF))
        shade(hdr[i], header_fill)
    for r_idx, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cell_text(cells[i], str(value), size=font_size,
                      bold=(first_col_bold and i == 0))
            if zebra and r_idx % 2 == 1:
                shade(cells[i], zebra)
    for row in table.rows:
        for i, width in enumerate(widths):
            row.cells[i].width = Cm(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def h1(doc, number, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(f"Алхам {number}. {text}")
    run.bold = True
    run.font.size = Pt(15)
    run.font.color.rgb = NAVY
    bar = doc.add_paragraph()
    bar.paragraph_format.space_after = Pt(8)
    p_pr = bar._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "1D4ED8")
    borders.append(bottom)
    p_pr.append(borders)


def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11.5)
    run.font.color.rgb = ACCENT
    return p


def body(doc, text, size=10.5, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.italic = italic
    return p


def bullet(doc, text, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.75)
    run = p.add_run(text)
    run.font.size = Pt(size)
    return p


def note(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.left_indent = Cm(0.4)
    p_pr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), "FFF8E1")
    p_pr.append(shd)
    run = p.add_run("Гол санаа: ")
    run.bold = True
    run.font.size = Pt(9.8)
    run2 = p.add_run(text)
    run2.font.size = Pt(9.8)
    run2.italic = True


def code_block(doc, lines):
    for line in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.left_indent = Cm(0.4)
        p_pr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), "F3F4F6")
        p_pr.append(shd)
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(8.8)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(text)
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = GREY


def picture(doc, path, width_cm=16.4):
    doc.add_picture(path, width=Cm(width_cm))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


def page_number_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.font.size = Pt(9)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)


# --------------------------------------------------------------------------- #
# Баримт бий болгох
# --------------------------------------------------------------------------- #
doc = Document()
section = doc.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.2)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.3)
section.right_margin = Cm(2.0)
page_number_footer(section)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

# ------------------------------ Нүүр хуудас ------------------------------ #
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(36)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Л А Б О Р А Т О Р И  12")
run.bold = True
run.font.size = Pt(26)
run.font.color.rgb = NAVY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
run = p.add_run("Архитектурын зохиомж")
run.font.size = Pt(15)
run.font.color.rgb = ACCENT
run.italic = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(28)
run = p.add_run("Architecture, Components and CI")
run.font.size = Pt(11)
run.font.color.rgb = GREY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
p.paragraph_format.space_after = Pt(2)
run = p.add_run("ТАКСИ ДУУДЛАГЫН СИСТЕМ")
run.bold = True
run.font.size = Pt(22)
run.font.color.rgb = NAVY

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(30)
run = p.add_run("Зорчигч · Жолооч · Диспетчер — нэгдсэн платформ")
run.font.size = Pt(11)
run.font.color.rgb = GREY

picture(doc, os.path.join(DIAG, "architecture.png"), width_cm=15.6)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

info = [
    ["Хичээл", "SAD236 · Системийн шинжилгээ ба зохиомж"],
    ["Лаборатори", "Лаборатори 12 — Архитектур, компонент ба CI"],
    ["Сэдэв", "Такси дуудлагын систем"],
    ["Баг / гишүүд", "……………………………………… (3–5 гишүүн)"],
    ["Багшийн нэр", "………………………………………"],
    ["Огноо", "2026 оны 11 сарын 19"],
    ["GitHub репозитори", "github.com/<баг>/taxi-dispatch"],
]
t = doc.add_table(rows=0, cols=2)
t.style = "Table Grid"
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for label, value in info:
    cells = t.add_row().cells
    cell_text(cells[0], label, bold=True, size=10)
    shade(cells[0], "E8EEF9")
    cell_text(cells[1], value, size=10)
    cells[0].width = Cm(4.6)
    cells[1].width = Cm(11.0)

body(doc, "")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Гүйцэтгэсэн ажлын хураангуй: 6 NFR, 2 хувилбарын жигнэсэн харьцуулалт, "
                "3 түвшинт архитектур, компонентын диаграмм ба 6 REST интерфейс, "
                "ADR-001, GitHub + CI (ажилладаг 9 тест).")
run.font.size = Pt(9)
run.italic = True
run.font.color.rgb = GREY

doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ------------------------------ Алхам 1 ------------------------------ #
h1(doc, 1, "Архитектурт нөлөөлөх NFR")
body(doc,
     "Такси дуудлагын систем нь бодит цагийн байршил, төлбөр, олон төрлийн клиент "
     "ашигладаг тул дараах функциональ бус шаардлагууд (NFR) архитектурын шийдвэрт "
     "шууд нөлөөлнө. Шаардлага бүрийг хэмжүүртэй зорилт болгон задалж, аль "
     "архитектурын механизмаар хангахыг тодорхойлов.")

add_table(
    doc,
    ["Ангилал", "Шаардлага", "Хэмжүүр / зорилт", "Архитектурт нөлөө"],
    [
        ["Гүйцэтгэл",
         "Оргил цагт олон зорчигч нэгэн зэрэг дуудлага хийж, ойр жолооч хайна",
         "500 зэрэг дуудлага; жолооч хайлт ≤ 1 сек; API p95 ≤ 300 мс",
         "PostGIS-ийн GIST индекс, Redis кэш, stateless API-г 2 instance-аар кластерлэх"],
        ["Хүртээмж",
         "Систем 24/7 тасралтгүй ажиллаж, дуудлага алдагдахгүй",
         "≥ 99.9% (жилд ≤ 8.7 цаг зогсолт); RPO ≤ 5 мин, RTO ≤ 15 мин",
         "Идэвхтэй-нөөц сервер, автомат failover, WAL архивлал, унших реплик"],
        ["Бодит цаг / хөдөлгөөнт байдал",
         "Жолоочийн байршил байнга ирж, зорчигч машинаа газрын зураг дээр харна",
         "5 сек тутам шинэчлэл; зураг дээрх саатал ≤ 2 сек; iOS/Android/Chrome/Safari",
         "WebSocket (WSS) суваг, геомэдээллийн урсгал, responsive React клиент"],
        ["Аюулгүй байдал",
         "Зорчигч зөвхөн өөрийн захиалгыг харна; картын мэдээлэл манайд хадгалагдахгүй",
         "TLS 1.3, OTP нэвтрэлт, JWT 15 мин, PCI-DSS-ийг төлбөрийн гарцад шилжүүлэх",
         "Нэвтрэлтийн давхарга (API Gateway), эрхийн шалгалт, гадаад гарцын адаптер"],
        ["Интеграц",
         "Газрын зураг/маршрут, төлбөр, push/SMS-ийг гадаад үйлчилгээнээс авна",
         "Гадаад API-ийн алдаа ≤ 0.5%; timeout 3 сек; fallback заавал",
         "Anti-corruption адаптер, retry + circuit breaker, үйл явдлын дараалал"],
        ["Зардал ба өргөтгөл",
         "Жолоочийн тоо 3 дахин өсөхөд шинэ архитектур шаардахгүй; шинэ сервер авахгүй",
         "300 → 3000 жолооч, 1 кластер; сарын зардал одоогийн серверт багтана",
         "Хэвтээ өргөтгөл, stateless үйлчилгээ, Docker контейнер, нээлттэй эх технологи"],
    ],
    widths=[2.5, 4.3, 4.6, 5.2],
    first_col_bold=True,
)
note(doc, "NFR бүр «хэмжүүр → механизм» гэсэн хосоор бичигдсэн тул архитектурын "
          "шийдвэрийг дараа нь шалгах боломжтой (жишээ нь p95 ≤ 300 мс гэсэн зорилтыг "
          "APM хэмжилтээр батална).")

# ------------------------------ Алхам 2 ------------------------------ #
h1(doc, 2, "Хоёр хувилбарыг харьцуулах")
body(doc,
     "Архитектурын үндсэн сонголтыг хоёр хувилбараар харьцуулав. Хувилбар бүрийг "
     "NFR-ээс гаралтай шалгуураар 1–5 оноогоор үнэлж, жингээр үржүүлэн жигнэсэн "
     "нийлбэрийг гаргав.")

h2(doc, "Хувилбар A — Диспетчерын desktop програм + төв өгөгдлийн сан (2 түвшин)")
body(doc,
     "Дуудлагыг утсаар хүлээж авч, диспетчер гар аргаар жолооч оноодог. Клиент нь "
     "зөвхөн диспетчерын компьютерт суусан програм, өгөгдөл нь төв сервер дээр. "
     "Жолоочийн байршил автоматаар ирэхгүй, зорчигч машинаа харж чадахгүй.")

h2(doc, "Хувилбар B — Вэб/мобайл 3 түвшинт платформ")
body(doc,
     "Зорчигч, жолооч, диспетчер гурвуулаа нэг REST/WebSocket API-г ашиглана. "
     "Жолоочийн байршил 5 секунд тутам ирж, хуваарилалт автоматаар хийгдэнэ. "
     "Өгөгдөл PostgreSQL + PostGIS дээр, төлбөр гадаад гарцаар гүйцэтгэнэ.")

add_table(
    doc,
    ["Шалгуур (NFR)", "Жин", "A: Desktop + төв DB", "B: Вэб/мобайл 3 түвшин"],
    [
        ["Бодит цагийн байршил ба өөртөө үйлчилгээ", "25%", "2", "5"],
        ["Гүйцэтгэл (оргил цаг)", "20%", "3", "4"],
        ["Аюулгүй байдал, төлбөр", "20%", "4", "5"],
        ["Өргөтгөх, шинэчлэхэд хялбар", "20%", "2", "5"],
        ["Зардал (одоо байгаа сервер)", "15%", "3", "3"],
        ["Жигнэсэн нийлбэр", "100%", "2.75", "4.50"],
    ],
    widths=[8.0, 2.2, 3.2, 3.2],
    first_col_bold=False,
)
body(doc, "Тооцоолол:", size=10)
code_block(doc, [
    "A = 2×0.25 + 3×0.20 + 4×0.20 + 2×0.20 + 3×0.15 = 0.50 + 0.60 + 0.80 + 0.40 + 0.45 = 2.75",
    "B = 5×0.25 + 4×0.20 + 5×0.20 + 5×0.20 + 3×0.15 = 1.25 + 0.80 + 1.00 + 1.00 + 0.45 = 4.50",
    "→ B хувилбар 1.75 оноогоор илүү тул B сонгогдов.",
])
body(doc,
     "B хувилбар нь бодит цагийн байршил ба өөртөө үйлчилгээний шаардлагыг бүрэн "
     "хангаж, жолоочийн тоо өсөхөд архитектур өөрчлөх шаардлагагүй. A хувилбар нь "
     "зөвхөн диспетчерээс хамааралтай тул оргил цагт саатал үүсгэж, NFR-ийг "
     "хангахгүй.")

# ------------------------------ Алхам 3 ------------------------------ #
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
h1(doc, 3, "Гурван түвшинт архитектур")
body(doc,
     "Сонгосон B хувилбарыг танилцуулга, хэрэглээ, өгөгдлийн гэсэн гурван түвшинд "
     "задалж, гадаад системүүдийг тасархай хүрээгээр тусгаарлав. Түвшин бүрт "
     "технологийг нэрлэсэн бөгөөд сонголтын үндэслэлийг ADR-001-д бичев.")

picture(doc, os.path.join(DIAG, "architecture.png"), width_cm=16.6)
caption(doc, "Зураг 1. Такси дуудлагын системийн гурван түвшинт архитектур "
             "(гадаад системүүд баруун талд, тасархай хүрээтэй).")

h2(doc, "Давхарга тус бүрийн үүрэг ба технологи")
add_table(
    doc,
    ["Түвшин", "Технологи", "Хариуцлага", "Холбоо"],
    [
        ["Танилцуулга", "React 18 (SPA), React Native 0.74",
         "Зорчигчийн дуудлага, жолоочийн навигаци, диспетчерын хяналтын самбар",
         "HTTPS (REST), WSS (байршил)"],
        ["Хэрэглээ", "Node.js 22, Express/Fastify, ws, JWT",
         "Захиалгын төлөв, хуваарилалт, тариф, бодит цагийн урсгал, нэвтрэлт",
         "SQL (pg), REST (гадаад)"],
        ["Өгөгдөл", "PostgreSQL 16 + PostGIS, Redis 7",
         "Жолооч, захиалга, төлбөр, байршлын индекс, кэш, нөөцлөлт",
         "WAL архив → S3"],
    ],
    widths=[2.6, 4.4, 6.2, 3.4],
    first_col_bold=True,
)

h2(doc, "Гадаад системүүд")
add_table(
    doc,
    ["Гадаад систем", "Хэрэглээ", "Холболтын хэлбэр", "Алдааны стратеги"],
    [
        ["Google Maps Platform / OSRM", "Маршрут, зай, хугацаа, газрын зураг",
         "REST + static map", "Кэш 10 мин, OSRM fallback"],
        ["QPay / банкны картын гарц", "Төлбөр, буцаалт", "REST + webhook",
         "Idempotency key, 3 удаа retry"],
        ["Firebase Cloud Messaging, SMS", "Push ба SMS мэдэгдэл", "REST",
         "Дараалалд хийж дахин илгээх"],
        ["SSO / OTP үйлчилгээ", "Нэвтрэлт, утасны баталгаажуулалт", "OAuth 2.0 / OTP",
         "60 сек хүчинтэй код, 5 оролдлого"],
    ],
    widths=[4.6, 4.2, 3.6, 4.2],
)
note(doc, "Тасархай хүрээ = гадаад систем. Хэрэглээний түвшин гадаад системтэй шууд "
          "харилцахгүй, адаптер компонентоор дамжина — ингэснээр нийлүүлэгч "
          "солигдоход бусад хэсэг өөрчлөгдөхгүй.")

# ------------------------------ Алхам 4 ------------------------------ #
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
h1(doc, 4, "Компонентын диаграмм ба интерфейс")
body(doc,
     "Хэрэглээний түвшинг хариуцлагаар нь дөрвөн компонент болгон задалж, "
     "компонентуудыг зөвхөн интерфейсээр холбов. Интерфейс бүр нь гэрээ (contract) "
     "тул хэрэгжүүлэлтийг сольсон ч хэрэглэгч компонент өөрчлөгдөхгүй.")

picture(doc, os.path.join(DIAG, "components.png"), width_cm=16.6)
caption(doc, "Зураг 2. Компонентын диаграмм: UI, дөрвөн үйлчилгээ, өгөгдөлд хандах "
             "давхарга ба интерфейсүүд.")

add_table(
    doc,
    ["Компонент", "Хариуцлага", "Нээлттэй интерфейс"],
    [
        ["Захиалгын үйлчилгээ", "Захиалга үүсгэх, цуцлах, төлөв хянах",
         "IЗахиалга: createRide, cancelRide, getRide"],
        ["Хуваарилалтын үйлчилгээ", "Хамгийн ойрын чөлөөт жолоочийг сонгож, ETA тооцох",
         "IХуваарилалт: assignDriver, reassign"],
        ["Байршлын үйлчилгээ", "Жолоочийн GPS урсгалыг хүлээж, зорчигчид дамжуулах",
         "IБайршил: WebSocket stream, lastPosition"],
        ["Төлбөрийн үйлчилгээ", "Тариф тооцож, гадаад гарцаар төлбөр авах",
         "IТөлбөр: computeFare, charge, refund"],
        ["Өгөгдөлд хандах", "SQL гүйлгээ, индекс, репозиторийн хийсвэрлэл",
         "IӨгөгдөл: findNearestDrivers, saveRide, savePayment"],
    ],
    widths=[3.6, 6.4, 6.6],
    first_col_bold=True,
)

h2(doc, "Интерфейсийн жагсаалт (REST API)")
add_table(
    doc,
    ["Интерфейс", "Үйлдэл (endpoint)", "Хэн хэрэглэх", "Холбогдох UC"],
    [
        ["IЗахиалга", "POST /api/v1/rides {pickup, dropoff, rideType}", "Зорчигчийн апп", "UC-01"],
        ["IЗахиалга", "GET /api/v1/rides/{id}", "Зорчигч, жолооч, диспетчер", "UC-02"],
        ["IЗахиалга", "PATCH /api/v1/rides/{id}/cancel", "Зорчигч, диспетчер", "UC-06"],
        ["IХуваарилалт", "POST /api/v1/rides/{id}/assign {driverId}", "Хуваарилалтын үйлчилгээ, диспетчер", "UC-03"],
        ["IБайршил", "WS /api/v1/ws/drivers/{id}/location", "Жолоочийн апп", "UC-04"],
        ["IТөлбөр", "POST /api/v1/rides/{id}/payment {method}", "Зорчигчийн апп", "UC-05"],
        ["IТөлбөр", "POST /api/v1/rides/{id}/fare {distanceKm, durationMin, demandLevel}", "Зорчигчийн апп, диспетчер", "UC-05"],
        ["IӨгөгдөл", "findNearestDrivers(point, radius), saveRide(ride)", "Захиалга, Хуваарилалт", "—"],
    ],
    widths=[2.9, 7.2, 4.1, 2.4],
)
body(doc,
     "Сул холбоос (loose coupling)-ыг дараах гурван дүрмээр хангав: (1) компонент "
     "бүр зөвхөн өөрийн интерфейсээр хандах, (2) интерфейсийг эхлээд тодорхойлж "
     "(contract-first) дараа нь хэрэгжүүлэх, (3) API-г /api/v1 замын доор хувилбарлаж, "
     "эвдрэх өөрчлөлтийг шинэ хувилбарт хийх.")

# ------------------------------ Алхам 5 ------------------------------ #
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
h1(doc, 5, "Архитектурын шийдвэрийн баримт (ADR-001)")
body(doc,
     "Дараах ADR нь архитектурын гол шийдвэрийг нөхцөл, харьцуулсан хувилбар, "
     "үр дагаврын хамт баримтжуулна. Файл: docs/adr-001.md (репозиторид).")

add_table(
    doc,
    ["Хэсэг", "Агуулга"],
    [
        ["Дугаар, гарчиг",
         "ADR-001: Такси дуудлагын системийг вэб/мобайл гурван түвшинт архитектураар хэрэгжүүлэх"],
        ["Статус", "Хүлээн зөвшөөрсөн (2026-11-19)"],
        ["Нөхцөл",
         "Зорчигч гар утаснаас дуудлага хийж, машинаа бодит цагт харна; оргил цагт 500 зэрэг "
         "дуудлага; жолоочийн байршил 5 сек тутам; картын мэдээлэл манайд хадгалагдахгүй; "
         "шинэ сервер авах төсөв байхгүй"],
        ["Шийдвэр",
         "React (зорчигч, диспетчер) + React Native (жолооч) клиент; Node.js REST/WebSocket API; "
         "PostgreSQL + PostGIS өгөгдлийн сан; Docker контейнероор одоо байгаа 2 серверт байршуулна"],
        ["Харьцуулсан хувилбар",
         "A: Диспетчерын desktop програм + төв DB — 2.75 оноо; бодит цагийн байршил, "
         "өөртөө үйлчилгээ байхгүй тул хасагдсан"],
        ["Үр дагавар (+)",
         "Нэг газар шинэчилнэ; гурван клиент нэг API-г ашиглана; stateless тул хэвтээ "
         "өргөтгөл хямд; PCI-DSS-ийн хүрээ багассан"],
        ["Үр дагавар (−)",
         "Сүлжээ тасрахад дуудлага хийх боломжгүй (offline горим байхгүй); WebSocket-ийн "
         "бодит цагийн холболт нэмэлт мониторинг шаардана; газрын зураг/төлбөрийн "
         "гадаад API-аас хамааралтай"],
        ["Хяналт",
         "p95 ≤ 300 мс, 99.9% хүртээмж, гадаад API-ийн алдаа ≤ 0.5% — сар бүр хэмжиж, "
         "зөрвөл ADR-ийг шинэчилнэ"],
    ],
    widths=[4.0, 12.6],
    first_col_bold=True,
)

# ------------------------------ Алхам 6 ------------------------------ #
h1(doc, 6, "GitHub репозитори ба CI")
body(doc,
     "Кодыг багийн хамтын ажиллагаанд бэлтгэхийн тулд репозиторийн бүтэц, салбарын "
     "дүрэм, автомат тестийг (CI) тохируулав. Бүх гишүүн репозиторид уригдсан байна.")

h2(doc, "Репозиторийн бүтэц")
add_table(
    doc,
    ["Хавтас / файл", "Агуулга"],
    [
        ["docs/", "Архитектурын диаграмм (PNG), ADR-001, энэхүү тайлан (DOCX)"],
        ["db/", "schema.sql — PostgreSQL + PostGIS схем, индексүүд"],
        ["src/", "fare.js (тариф), dispatch.js (хуваарилалт), server.js (REST API)"],
        ["test/", "node:test нэгж тестүүд (тариф, хуваарилалт)"],
        [".github/workflows/ci.yml", "GitHub Actions CI — push, pull request бүрт ажиллана"],
        ["README.md", "Ажиллуулах заавар, API жишээ, GitHub-ийн алхмууд"],
    ],
    widths=[5.2, 11.4],
    first_col_bold=True,
)

h2(doc, "Тохиргооны алхмууд")
steps = [
    ("1. Репо үүсгэх", "github.com → New repository → «taxi-dispatch», README нэмэх."),
    ("2. Баг урих", "Settings → Collaborators → гишүүд болон багшийг урих."),
    ("3. Бүтэц", "docs/, db/, src/, test/ хавтсуудыг үүсгэж, эхний commit хийх."),
    ("4. Салбар", "main хамгаалалттай; ажлыг feature/<нэр> салбар дээр хийж, "
                  "pull request-ээр нэгтгэнэ (1 review + CI ногоон байх шаардлагатай)."),
    ("5. CI нэмэх", ".github/workflows/ci.yml файлыг үүсгэж push хийнэ."),
]
for title, text in steps:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(4)
    run = p.add_run(title + " — ")
    run.bold = True
    run.font.size = Pt(10.5)
    run.font.color.rgb = ACCENT
    run2 = p.add_run(text)
    run2.font.size = Pt(10.5)

h2(doc, "CI тохиргоо (.github/workflows/ci.yml)")
code_block(doc, [
    "name: CI",
    "",
    "on: [push, pull_request]",
    "",
    "jobs:",
    "  test:",
    "    runs-on: ubuntu-latest",
    "    steps:",
    "      - uses: actions/checkout@v4",
    "      - uses: actions/setup-node@v4",
    "        with:",
    "          node-version: 22",
    "          cache: npm",
    "      - run: npm ci",
    "      - run: npm test",
])

add_table(
    doc,
    ["Мөр", "Утга", "Тайлбар"],
    [
        ["on", "push, pull_request",
         "Код push хийх, pull request нээх бүрт ажиллана"],
        ["runs-on", "ubuntu-latest", "GitHub-ийн үнэгүй виртуал машин дээр"],
        ["steps", "checkout → setup-node → npm ci → npm test",
         "Кодыг татах → Node 22 суулгах → сангуудыг цэвэр суулгах → тест ажиллуулах"],
        ["Үр дүн", "Actions таб дээр ✓ / ✕",
         "Амжилтгүй бол pull request нэгтгэгдэхгүй (branch protection)"],
    ],
    widths=[2.2, 5.6, 8.8],
    first_col_bold=True,
)

h2(doc, "Тестийн жишээ — тариф ба хуваарилалт")
body(doc,
     "CI-д ажиллах хамгийн бага боловч бодит тест нь тарифын тооцоолол ба жолооч "
     "сонголт. `npm test` нь 9 тест ажиллуулж, бүгд амжилттай болсон:")
add_table(
    doc,
    ["Тест", "Шалгах зүйл", "Хүлээгдэх утга"],
    [
        ["Өдрийн цагийн энгийн тариф", "1500 + 5км×1200 + 12мин×150", "9,300₮"],
        ["Шөнийн нэмэгдэл", "22:00–06:00 хооронд суурь+км-ийн 15%", "10,400₮"],
        ["Эрэлтийн коэффициент", "Эрэлтийн түвшин 3 → ×1.5", "25,900₮"],
        ["Доод хязгаар", "Маш богино зам", "2,000₮"],
        ["Хуваарилалт", "Зөвхөн чөлөөт, радиус доторх жолооч, ETA", "d4, ~1 мин"],
    ],
    widths=[4.4, 8.2, 4.0],
)

body(doc,
     "Локал шалгах команд: `npm ci && npm test`. Репозитори push хийсний дараа "
     "Actions таб дээр CI-ийн ногоон ✓ харагдана — энэ нь «Ажилладаг CI» гэсэн "
     "шалгуурыг хангана.")

# ------------------------------ Хавсралт ------------------------------ #
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(10)
run = p.add_run("Хавсралт. Үнэлгээний шалгуур ба хийсэн ажлын харгалзаа")
run.bold = True
run.font.size = Pt(13)
run.font.color.rgb = NAVY

add_table(
    doc,
    ["Шалгуур", "Жин", "Хаана хийгдсэн"],
    [
        ["NFR", "15%", "Алхам 1 — 6 NFR, хэмжүүртэй зорилт, архитектурт нөлөөллийн тайлбар"],
        ["Хувилбарын харьцуулалт, ADR", "20%", "Алхам 2 (жигнэсэн матриц, тооцоо) + Алхам 5 (ADR-001)"],
        ["Архитектурын диаграмм", "25%", "Алхам 3 — түвшин, технологи, гадаад систем (Зураг 1)"],
        ["Компонент ба интерфейс", "25%", "Алхам 4 — компонентын диаграмм (Зураг 2), 8 интерфейс, сул холбоос"],
        ["GitHub ба CI", "15%", "Алхам 6 — репозиторийн бүтэц, салбарын дүрэм, ci.yml, 9 тест"],
    ],
    widths=[4.6, 1.8, 10.2],
    first_col_bold=True,
)

h2(doc, "Хүлээлгэн өгөх файлууд")
for item in [
    "docs/lab12-taxi-architecture.docx — энэхүү тайлан",
    "docs/diagrams/architecture.png, components.png — диаграммууд",
    "docs/adr-001.md — ADR-001",
    "db/schema.sql — өгөгдлийн сангийн схем",
    "src/fare.js, src/dispatch.js, src/server.js — ажилладаг код",
    "test/fare.test.js, test/dispatch.test.js — 9 нэгж тест",
    ".github/workflows/ci.yml — GitHub Actions CI",
]:
    bullet(doc, item, size=10)

body(doc,
     "Тайланг бэлтгэхдээ byte-ийн түвшинд шалгасан: `npm ci` амжилттай, `npm test` "
     "9/9 тест амжилттай, REST API нь Node.js 22-т ажиллана.", italic=True, size=9.5)

doc.save(OUT_FILE)
print("saved:", OUT_FILE)
