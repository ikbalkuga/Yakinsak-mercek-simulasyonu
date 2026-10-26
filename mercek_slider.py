import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Mercek parametreleri (sunumdaki gosterim: d, d', f)
f = 10      # odak uzakligi
ho = 5      # cisim yuksekligi

X_MAX = 45  
Y_MAX = 22
EPS = 1e-9


def ciz(ax, d):
    """Cisim merceginden d uzakliktayken isin diyagramini ax uzerine cizer."""
    ax.clear()
    odakta = abs(d - f) < EPS

    # Ince mercek denklemi: 1/d + 1/d' = 1/f
    if not odakta:
        dp = 1 / (1 / f - 1 / d)
        hi = -(dp / d) * ho

    # Isinlarin mercek uzerindeki yuksekligi
    y1 = ho                          # eksene paralel gelen isin
    y2 = 0                           # mercek merkezinden (O) gecen isin
    if not odakta:
        y3 = -f * ho / (d - f)       # F'den gecen (F dogrultusunda gelen) isin

    # Mercekten sonraki egimler
    m1 = -ho / f                     # F' noktasindan gecer
    m2 = -ho / d                     # kirilmadan devam eder
    m3 = 0                           # eksene paralel cikar

    # Optik eksen, mercek, odak noktalari
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="blue", linewidth=2)
    ax.scatter([-f, f], [0, 0], color="red", zorder=5)
    ax.annotate("F", (-f, 0), xytext=(0, -14), textcoords="offset points", ha="center")
    ax.annotate("F'", (f, 0), xytext=(0, -14), textcoords="offset points", ha="center")
    ax.annotate("O", (0, 0), xytext=(9, -14), textcoords="offset points", ha="center")

    # Cisim
    ax.annotate("", xy=(-d, ho), xytext=(-d, 0),
                arrowprops=dict(arrowstyle="-|>", color="green", lw=2, mutation_scale=15))
    ax.text(-d - 0.8, ho / 2, "Cisim", ha="right", va="center", color="green")

    # Mercege gelen isinlar
    ax.plot([-d, 0], [ho, y1], color="orange", linewidth=1.8, label="Paralel gelen ışın")
    ax.plot([-d, 0], [ho, y2], color="red", linewidth=1.8, label="Merkez ışını")
    if not odakta:
        ax.plot([-d, 0], [ho, y3], color="brown", linewidth=1.8, label="Odak ışını")

    if odakta:
        # d = f: cikan isinlar paralel, goruntu sonsuzda
        ax.plot([0, X_MAX], [y1, y1 + m1 * X_MAX], color="orange", linewidth=1.8)
        ax.plot([0, X_MAX], [y2, y2 + m2 * X_MAX], color="red", linewidth=1.8)
        satirlar = [f"d = {d:.1f} = f",
                    "Görüntü oluşmaz (sonsuzda)",
                    "Çıkan ışınlar paralel; odak ışını merceğe ulaşmaz"]
        renk = "gray"
    else:
        if dp > 0:
            # Gercek goruntu: isinlar goruntu ucunda (T') birlesir
            ax.plot([0, dp], [y1, hi], color="orange", linewidth=1.8)
            ax.plot([0, dp], [y2, hi], color="red", linewidth=1.8)
            ax.plot([0, dp], [y3, hi], color="brown", linewidth=1.8)
            tur = "Gerçek, ters"
            renk = "purple"
        else:
            # Sanal goruntu: isinlar iraksar, geriye uzantilar (noktali) T' de kesisir
            ax.plot([0, X_MAX], [y1, y1 + m1 * X_MAX], color="orange", linewidth=1.8)
            ax.plot([0, X_MAX], [y2, y2 + m2 * X_MAX], color="red", linewidth=1.8)
            ax.plot([0, X_MAX], [y3, y3 + m3 * X_MAX], color="brown", linewidth=1.8)
            ax.plot([0, dp], [y1, hi], color="orange", linestyle=":", linewidth=1.5)
            ax.plot([0, dp], [y2, hi], color="red", linestyle=":", linewidth=1.5)
            ax.plot([0, dp], [y3, hi], color="brown", linestyle=":", linewidth=1.5)
            tur = "Sanal, düz"
            renk = "purple"

        if abs(abs(hi) - ho) < 1e-6:
            boyut = "cisimle aynı boyda"
        elif abs(hi) > ho:
            boyut = "büyük"
        else:
            boyut = "küçük"

        satirlar = [f"d = {d:.1f}    d′ = {dp:.1f}    h′ = {hi:.1f}    büyütme = {hi / ho:.2f}×",
                    f"Görüntü: {tur}, {boyut}"]

        # Goruntu oku ve T' yalnizca gorunur alandaysa cizilir
        if abs(dp) < X_MAX and abs(hi) < Y_MAX:
            ax.annotate("", xy=(dp, hi), xytext=(dp, 0),
                        arrowprops=dict(arrowstyle="-|>", color="purple", lw=2, mutation_scale=15))
            ax.scatter([dp], [hi], color="black", s=18, zorder=6)
            ax.text(dp + 0.8, hi + (1.0 if hi > 0 else -2.2), "T′  Görüntü", color="purple")
        else:
            satirlar.append("(Görüntü çizim alanının dışında)")

    ax.text(0.01, 0.98, "\n".join(satirlar), transform=ax.transAxes, va="top", ha="left",
            fontsize=11, bbox=dict(boxstyle="round", fc="white", ec=renk, alpha=0.95))

    ax.set_xlim(-X_MAX, X_MAX)
    ax.set_ylim(-Y_MAX, Y_MAX)
    ax.set_xlabel("Konum")
    ax.set_ylabel("Yükseklik")
    ax.set_title("Yakınsak Mercek:  1/d + 1/d′ = 1/f   (f = 10)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", framealpha=0.9)


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.subplots_adjust(bottom=0.17)

    ax_slider = fig.add_axes([0.15, 0.04, 0.7, 0.04])
    slider = Slider(ax_slider, "d (cisim uzaklığı)", 1, 40, valinit=30, valstep=0.5)

    def guncelle(val):
        ciz(ax, slider.val)
        fig.canvas.draw_idle()

    slider.on_changed(guncelle)
    ciz(ax, slider.val)
    plt.show()
