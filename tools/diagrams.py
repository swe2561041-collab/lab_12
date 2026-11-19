"""Архитектур ба компонентын диаграмм үүсгэх (matplotlib)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "diagrams")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2937"
TIER_BG = ["#eef4fb", "#eefaf1", "#fdf3e7"]
EXT_BG = "#f7f2fb"
mpl_rc = {"font.family": "DejaVu Sans", "font.size": 10, "text.color": INK}
plt.rcParams.update(mpl_rc)


def box(ax, x, y, w, h, title, sub="", fc="white", ec="#475569", fs=10.5, ss=8.6, lw=1.2, ls="-"):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.4,rounding_size=1.0",
            linewidth=lw, edgecolor=ec, facecolor=fc, linestyle=ls, zorder=3,
        )
    )
    if sub:
        ax.text(x + w / 2, y + h / 2 + 1.6, title, ha="center", va="center",
                fontsize=fs, fontweight="bold", zorder=4)
        ax.text(x + w / 2, y + h / 2 - 2.2, sub, ha="center", va="center",
                fontsize=ss, color="#475569", zorder=4)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=fs, fontweight="bold", zorder=4)


def tier(ax, x, y, w, h, label, fc):
    ax.add_patch(
        FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.4",
                       linewidth=1.4, edgecolor="#94a3b8", facecolor=fc,
                       linestyle="--", zorder=1)
    )
    ax.text(x + 1.0, y + h + 0.8, label, ha="left", va="bottom",
            fontsize=9.2, color="#475569", style="italic", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))


def arrow(ax, p1, p2, label="", ls="-", color="#334155", dx=0, dy=1.2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=13,
                                 linewidth=1.3, color=color, linestyle=ls,
                                 shrinkA=1, shrinkB=1, zorder=5))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + dx, (p1[1] + p2[1]) / 2 + dy, label,
                ha="center", va="bottom", fontsize=8, color=color,
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"), zorder=6)


def architecture():
    fig, ax = plt.subplots(figsize=(12.6, 7.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # --- Гадаад системүүд ---
    ax.add_patch(FancyBboxPatch((76.5, 4), 22, 92,
                                boxstyle="round,pad=0.6,rounding_size=1.4",
                                linewidth=1.4, edgecolor="#a78bfa",
                                facecolor=EXT_BG, linestyle="--", zorder=1))
    ax.text(77.5, 94.5, "Гадаад системүүд", ha="left", fontsize=9.2,
            color="#6b21a8", style="italic", zorder=6)
    box(ax, 79, 77, 17, 12, "Газрын зураг,\nмаршрут", "Google Maps / OSRM", fc="#ffffff", ec="#a78bfa")
    box(ax, 79, 58, 17, 12, "SSO / OTP", "Нэвтрэлт, баталгаажуулалт", fc="#ffffff", ec="#a78bfa", ss=7.8)
    box(ax, 79, 39, 17, 12, "Төлбөрийн гарц", "QPay / карт", fc="#ffffff", ec="#a78bfa")
    box(ax, 79, 20, 17, 12, "Push / SMS", "FCM, SMS gateway", fc="#ffffff", ec="#a78bfa")

    # --- Түвшин 1: Танилцуулга ---
    tier(ax, 2, 72, 70, 22, "Танилцуулгын түвшин — клиент (React / React Native)",
         TIER_BG[0])
    box(ax, 5, 76, 20, 13, "Зорчигчийн апп", "React Native", fc="#dbeafe", ec="#2563eb")
    box(ax, 27, 76, 20, 13, "Жолоочийн апп", "React Native + GPS", fc="#dbeafe", ec="#2563eb")
    box(ax, 49, 76, 20, 13, "Диспетчерын вэб", "React SPA", fc="#dbeafe", ec="#2563eb")

    # --- Түвшин 2: Хэрэглээ ---
    tier(ax, 2, 40, 70, 26, "Хэрэглээний түвшин — Node.js REST + WebSocket API",
         TIER_BG[1])
    box(ax, 5, 53, 15.4, 10, "Захиалгын\nүйлчилгээ", "", fc="#dcfce7", ec="#16a34a")
    box(ax, 22, 53, 15.4, 10, "Хуваарилалтын\nүйлчилгээ", "", fc="#dcfce7", ec="#16a34a")
    box(ax, 39, 53, 15.4, 10, "Байршлын\nүйлчилгээ (WS)", "", fc="#dcfce7", ec="#16a34a")
    box(ax, 56, 53, 13, 10, "Төлбөрийн\nүйлчилгээ", "", fc="#dcfce7", ec="#16a34a")
    box(ax, 5, 43, 64, 7, "Тарифын модуль · Аудитын бүртгэл · API Gateway (ratе limit, JWT)", "",
        fc="#f0fdf4", ec="#86efac", fs=9.2)

    # --- Түвшин 3: Өгөгдөл ---
    tier(ax, 2, 8, 70, 24, "Өгөгдлийн түвшин — PostgreSQL + PostGIS",
         TIER_BG[2])
    box(ax, 5, 18, 21, 10, "Захиалга, жолооч", "ride · driver · payment", fc="#fed7aa", ec="#ea580c")
    box(ax, 28, 18, 19, 10, "Байршлын индекс", "GIST / PostGIS", fc="#fed7aa", ec="#ea580c")
    box(ax, 49, 18, 20, 10, "Redis кэш", "session, driver TTL", fc="#fed7aa", ec="#ea580c")
    ax.text(6, 11.5, "Өдөр тутмын нөөцлөлт (WAL + S3) · Унших реплик", fontsize=8.6, color="#7c2d12")

    # --- Холбоосууд ---
    for x in (15, 37, 59):
        arrow(ax, (x, 75.6), (x, 63.4), "HTTPS / WSS" if x == 37 else "", dy=0.6)
    for x in (12, 30, 47, 62):
        arrow(ax, (x, 52.2), (x, 28.4), "SQL" if x == 30 else "", dy=0.4)
    arrow(ax, (69.6, 46), (78.6, 46), "REST")
    arrow(ax, (69.6, 84), (78.6, 84), "static map / route")
    arrow(ax, (69.6, 63.5), (85.5, 70.6), "OAuth / OTP", dy=0.4)
    arrow(ax, (69.6, 44), (78.6, 28), "push", ls="--", dy=-1.0)

    ax.text(50, 98.6, "Зураг 1. Такси дуудлагын системийн гурван түвшинт архитектур",
            ha="center", fontsize=11.5, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "architecture.png"), dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


def components():
    fig, ax = plt.subplots(figsize=(12.2, 7.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def comp(x, y, w, h, name, sub=""):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.3,rounding_size=0.8",
                                    linewidth=1.4, edgecolor="#2563eb",
                                    facecolor="#eff6ff", zorder=3))
        text = "«component»\n" + name
        if sub:
            text += "\n" + sub
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=8.8, zorder=4, color=INK)
        return (x, y, w, h)

    ui = comp(3, 78, 24, 14, "Вэб / Мобайл UI", "зорчигч · жолооч · диспетчер")
    dispatch_ui = comp(3, 40, 24, 12, "Диспетчерийн консол", "гараар оноох, хянах")

    s_ride = comp(38, 78, 26, 14, "Захиалгын үйлчилгээ", "createRide / cancelRide")
    s_disp = comp(38, 57, 26, 14, "Хуваарилалтын үйлчилгээ", "assignDriver / ETA")
    s_loc = comp(38, 36, 26, 14, "Байршлын үйлчилгээ", "WebSocket / geo stream")
    s_pay = comp(38, 15, 26, 14, "Төлбөрийн үйлчилгээ", "computeFare / charge")

    data = comp(74, 45, 23, 15, "Өгөгдөлд хандах", "repository, transaction")

    ax.add_patch(plt.Circle((90.5, 22), 2.4, facecolor="#fed7aa", edgecolor="#ea580c", zorder=3))
    ax.text(90.5, 17.5, "PostgreSQL\n/ PostGIS", ha="center", va="top", fontsize=8.6)

    ext = comp(74, 68, 23, 12, "Гадаад үйлчилгээ", "QPay · Maps · FCM")

    def iface(p1, p2, label, dy=1.4, dx=0.0, ls="-"):
        arrow(ax, p1, p2, label, dx=dx, dy=dy, ls=ls, color="#7c3aed")

    iface((27.4, 86), (37.6, 86), "IЗахиалга")
    iface((27.4, 46), (37.6, 63), "IХуваарилалт", dy=0.4)
    iface((28, 80), (37.6, 66), "IХуваарилалт", dy=1.0)
    iface((27.4, 44), (37.6, 43), "IБайршил", dy=0.6)
    iface((27.4, 42), (37.6, 23), "IТөлбөр", dy=0.6)
    iface((64.4, 85), (73.6, 58), "IӨгөгдөл", dy=0.4, dx=1.5)
    iface((64.4, 64), (73.6, 54), "IӨгөгдөл", dy=0.4)
    iface((64.4, 43), (73.6, 48), "IӨгөгдөл", dy=0.4)
    iface((64.4, 22), (73.6, 47), "IӨгөгдөл", dy=0.4)
    iface((86.5, 45), (88.5, 25), "", dy=0.2)
    iface((64.4, 26), (73.6, 70), "REST (адаптер)", dy=0.4, ls="--")

    ax.text(50, 97.5, "Зураг 2. Компонентын диаграмм ба интерфейсүүд",
            ha="center", fontsize=11.5, fontweight="bold")
    ax.text(50, 2.0,
            "Сул холбоос: компонентууд зөвхөн интерфейсээр (contract) харилцана; "
            "хэрэгжүүлэлтийг солиход бусад компонент өөрчлөгдөхгүй.",
            ha="center", fontsize=8.8, color="#475569")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "components.png"), dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    components()
    print("diagrams written to", os.path.abspath(OUT))
