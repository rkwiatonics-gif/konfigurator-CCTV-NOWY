import math
import streamlit as st

st.set_page_config(
    page_title="Konfigurator Systemu Video CCTV",
    page_icon="🎥",
    layout="wide",
)

# ---------------------------------------------------------
# BAZA DANYCH SPRZĘTU (Przykładowa baza produktowa)
# ---------------------------------------------------------
CAMERAS_DB = [
    {
        "symbol": "CAM-2M-FIX-BASIC",
        "name": "Kamera Kopułkowa 2MP (Standard)",
        "res_label": "Standardowa (2 MP / Full HD)",
        "resolution_mp": 2,
        "lens": "Stałoogniskowy (szeroki kąt 2.8mm)",
        "ai": "Brak (Podstawowa detekcja)",
        "housing": "Wewnętrzna / Kopułkowa",
        "bitrate_mbps": 2.0,
        "price_netto": 150.0,
        "mount_box": "BOX-DOME-SMALL",
    },
    {
        "symbol": "CAM-4M-FIX-AI",
        "name": "Kamera Tuba 4MP Smart AI",
        "res_label": "Wysoka (4 MP / 2K)",
        "resolution_mp": 4,
        "lens": "Stałoogniskowy (szeroki kąt 2.8mm)",
        "ai": "Detekcja Ludzi / Pojazdów (Ochrona obwodowa)",
        "housing": "Zewnętrzna / Tuba",
        "bitrate_mbps": 4.0,
        "price_netto": 320.0,
        "mount_box": "BOX-BULLET-STD",
    },
    {
        "symbol": "CAM-4M-MOTO-AI",
        "name": "Kamera Tuba 4MP Moto-zoom AI",
        "res_label": "Wysoka (4 MP / 2K)",
        "resolution_mp": 4,
        "lens": "Regulowany / Moto-zoom (2.8-12mm)",
        "ai": "Detekcja Ludzi / Pojazdów (Ochrona obwodowa)",
        "housing": "Zewnętrzna / Tuba",
        "bitrate_mbps": 5.0,
        "price_netto": 480.0,
        "mount_box": "BOX-BULLET-LARGE",
    },
    {
        "symbol": "CAM-8M-MOTO-AI",
        "name": "Kamera Turret 8MP 4K Moto-zoom Pro",
        "res_label": "Bardzo wysoka (8 MP / 4K)",
        "resolution_mp": 8,
        "lens": "Regulowany / Moto-zoom (2.8-12mm)",
        "ai": "Detekcja Ludzi / Pojazdów (Ochrona obwodowa)",
        "housing": "Zewnętrzna / Turret",
        "bitrate_mbps": 8.0,
        "price_netto": 750.0,
        "mount_box": "BOX-DOME-LARGE",
    },
    {
        "symbol": "CAM-4M-LPR",
        "name": "Kamera Specjalistyczna LPR (Tablice rejestracyjne)",
        "res_label": "Wysoka (4 MP / 2K)",
        "resolution_mp": 4,
        "lens": "Regulowany / Moto-zoom (2.8-12mm)",
        "ai": "Rozpoznawanie tablic rejestracyjnych (LPR)",
        "housing": "Zewnętrzna / Tuba",
        "bitrate_mbps": 6.0,
        "price_netto": 1200.0,
        "mount_box": "BOX-BULLET-LARGE",
    },
]

NVRS_DB = [
    {
        "symbol": "NVR-04-POE-STD",
        "name": "Rejestrator 4-kanałowy z PoE",
        "channels": 4,
        "max_bandwidth_mbps": 40,
        "supports_ai": False,
        "poe_ports": 4,
        "hdd_bays": 1,
        "price_netto": 450.0,
    },
    {
        "symbol": "NVR-08-POE-AI",
        "name": "Rejestrator 8-kanałowy Smart AI z PoE",
        "channels": 8,
        "max_bandwidth_mbps": 80,
        "supports_ai": True,
        "poe_ports": 8,
        "hdd_bays": 1,
        "price_netto": 850.0,
    },
    {
        "symbol": "NVR-16-PRO-AI",
        "name": "Rejestrator 16-kanałowy Pro AI (bez PoE)",
        "channels": 16,
        "max_bandwidth_mbps": 160,
        "supports_ai": True,
        "poe_ports": 0,
        "hdd_bays": 2,
        "price_netto": 1400.0,
    },
    {
        "symbol": "NVR-32-PRO-AI",
        "name": "Rejestrator 32-kanałowy Enterprise AI",
        "channels": 32,
        "max_bandwidth_mbps": 320,
        "supports_ai": True,
        "poe_ports": 0,
        "hdd_bays": 4,
        "price_netto": 2600.0,
    },
]

ACCESSORIES_DB = {
    "BOX-DOME-SMALL": {
        "name": "Puszka montażowa mała (Dome)",
        "price_netto": 45.0,
    },
    "BOX-BULLET-STD": {
        "name": "Puszka montażowa standardowa (Tuba)",
        "price_netto": 55.0,
    },
    "BOX-BULLET-LARGE": {
        "name": "Puszka montażowa duża (Moto-zoom/LPR)",
        "price_netto": 75.0,
    },
    "BOX-DOME-LARGE": {
        "name": "Puszka montażowa duża (Turret/4K)",
        "price_netto": 70.0,
    },
    "HDD-2TB": {"name": "Dysk twardy Surveillance 2TB", "price_netto": 280.0},
    "HDD-4TB": {"name": "Dysk twardy Surveillance 4TB", "price_netto": 420.0},
    "HDD-8TB": {"name": "Dysk twardy Surveillance 8TB", "price_netto": 850.0},
    "SWITCH-POE-8": {"name": "Switch PoE+ 8-portowy", "price_netto": 310.0},
    "SWITCH-POE-16": {"name": "Switch PoE+ 16-portowy", "price_netto": 680.0},
}

# ---------------------------------------------------------
# STAN APLIKACJI
# ---------------------------------------------------------
if "selected_cameras" not in st.session_state:
    st.session_state.selected_cameras = []

st.title("🎥 Konfigurator Systemu Video CCTV dla Dystrybutora")
st.caption(
    "Automatyczny dobór urządzeń, sprawdzanie kompatybilności oraz szybka wycena."
)

# ---------------------------------------------------------
# ZAKŁADKI
# ---------------------------------------------------------
tab_scenarios, tab_cameras, tab_nvr, tab_accessories, tab_quote = st.tabs(
    [
        "🚀 1. Szybkie Szablony",
        "📷 2. Dobór Kamer",
        "📼 3. Dobór Rejestratora",
        "🔌 4. Akcesoria i Dysk",
        "📄 5. Oferta Handlowa",
    ]
)

# ---------------------------------------------------------
# ZAKŁADKA 1: SZYBKIE SZABLONY
# ---------------------------------------------------------
with tab_scenarios:
    st.subheader("Wybierz gotowy scenariusz, aby szybko wypełnić konfigurację:")
    col_sc1, col_sc2, col_sc3 = st.columns(3)

    with col_sc1:
        st.info("### 🏠 Dom Jednorodzinny")
        st.write("- 4x Kamera Tuba 4MP Smart AI (Zewnętrzne)")
        st.write("- Obiektyw stały, ochrona obwodowa")
        if st.button("Załaduj szablon: Dom"):
            st.session_state.selected_cameras = [
                {**CAMERAS_DB[1], "qty": 4, "add_box": True}
            ]
            st.success("Załadowano szablon!")

    with col_sc2:
        st.info("### 🏢 Biuro / Mały Sklep")
        st.write("- 3x Kamera Kopułkowa 2MP (Wewnętrzne)")
        st.write("- 1x Kamera Tuba 4MP Smart AI (Zewnętrzna)")
        if st.button("Załaduj szablon: Biuro"):
            st.session_state.selected_cameras = [
                {**CAMERAS_DB[0], "qty": 3, "add_box": True},
                {**CAMERAS_DB[1], "qty": 1, "add_box": True},
            ]
            st.success("Załadowano szablon!")

    with col_sc3:
        st.info("### 🏭 Magazyn / Plac / LPR")
        st.write("- 4x Kamera Turret 8MP 4K Moto-zoom")
        st.write("- 1x Kamera LPR (Rozpoznawanie tablic)")
        if st.button("Załaduj szablon: Magazyn"):
            st.session_state.selected_cameras = [
                {**CAMERAS_DB[3], "qty": 4, "add_box": True},
                {**CAMERAS_DB[4], "qty": 1, "add_box": True},
            ]
            st.success("Załadowano szablon!")

# ---------------------------------------------------------
# ZAKŁADKA 2: DOBÓR KAMER (PARAMETRYCZNY)
# ---------------------------------------------------------
with tab_cameras:
    st.subheader("Określ wymagania dotyczące kamer:")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        f_res = st.selectbox(
            "Jakość obrazu / Rozdzielczość:",
            options=[
                "Wszystkie",
                "Standardowa (2 MP / Full HD)",
                "Wysoka (4 MP / 2K)",
                "Bardzo wysoka (8 MP / 4K)",
            ],
        )
        f_lens = st.selectbox(
            "Obiektyw i kąt widzenia:",
            options=[
                "Wszystkie",
                "Stałoogniskowy (szeroki kąt 2.8mm)",
                "Regulowany / Moto-zoom (2.8-12mm)",
            ],
        )

    with col_f2:
        f_ai = st.selectbox(
            "Analityka wideo (AI):",
            options=[
                "Wszystkie",
                "Brak (Podstawowa detekcja)",
                "Detekcja Ludzi / Pojazdów (Ochrona obwodowa)",
                "Rozpoznawanie tablic rejestracyjnych (LPR)",
            ],
        )
        f_housing = st.selectbox(
            "Miejsce montażu / Obudowa:",
            options=[
                "Wszystkie",
                "Wewnętrzna / Kopułkowa",
                "Zewnętrzna / Tuba",
                "Zewnętrzna / Turret",
            ],
        )

    # Filtrowanie kamer
    filtered_cams = CAMERAS_DB.copy()
    if f_res != "Wszystkie":
        filtered_cams = [c for c in filtered_cams if c["res_label"] == f_res]
    if f_lens != "Wszystkie":
        filtered_cams = [c for c in filtered_cams if c["lens"] == f_lens]
    if f_ai != "Wszystkie":
        filtered_cams = [c for c in filtered_cams if c["ai"] == f_ai]
    if f_housing != "Wszystkie":
        filtered_cams = [
            c for c in filtered_cams if c["housing"] == f_housing
        ]

    st.markdown("---")
    st.markdown("### Pasujące modele kamer:")

    if not filtered_cams:
        st.warning(
            "Brak kamer spełniających wszystkie wybrane kryteria. Zmień filtry."
        )
    else:
        for cam in filtered_cams:
            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
            with c1:
                st.markdown(f"**{cam['name']}**")
                st.caption(
                    f"Obudowa: {cam['housing']} | Obiektyw: {cam['lens']}"
                )
            with c2:
                st.write(f"**AI:** {cam['ai']}")
                st.write(f"Strumień: {cam['bitrate_mbps']} Mbps")
            with c3:
                st.write(f"Cena netto: **{cam['price_netto']:.2f} PLN**")
            with c4:
                qty = st.number_input(
                    "Ilość",
                    min_value=1,
                    max_value=64,
                    value=1,
                    key=f"qty_{cam['symbol']}",
                )
                add_box = st.checkbox(
                    "Puszka montażowa", value=True, key=f"box_{cam['symbol']}"
                )
                if st.button("Dodaj do oferty", key=f"add_{cam['symbol']}"):
                    st.session_state.selected_cameras.append(
                        {**cam, "qty": qty, "add_box": add_box}
                    )
                    st.success(f"Dodano: {cam['name']} x{qty}")

    st.markdown("---")
    st.markdown("### Wybrane kamery w projekcie:")
    if st.session_state.selected_cameras:
        for idx, item in enumerate(st.session_state.selected_cameras):
            col_list1, col_list2, col_list3 = st.columns([4, 2, 1])
            with col_list1:
                st.write(f"• **{item['name']}** (x{item['qty']} szt.)")
            with col_list2:
                st.write(f"Suma: {item['price_netto'] * item['qty']:.2f} PLN")
            with col_list3:
                if st.button("Usuń", key=f"del_{idx}"):
                    st.session_state.selected_cameras.pop(idx)
                    st.rerun()
    else:
        st.info("Lista kamer jest obecnie pusta.")

# ---------------------------------------------------------
# OBLICZENIA POMOCNICZE
# ---------------------------------------------------------
total_cam_count = sum(c["qty"] for c in st.session_state.selected_cameras)
total_bitrate = sum(
    c["bitrate_mbps"] * c["qty"] for c in st.session_state.selected_cameras
)
requires_ai = any(
    c["ai"] != "Brak (Podstawowa detekcja)"
    for c in st.session_state.selected_cameras
)

# ---------------------------------------------------------
# ZAKŁADKA 3: DOBÓR REJESTRATORA (KOMPATYBILNOŚĆ)
# ---------------------------------------------------------
with tab_nvr:
    st.subheader("Automatyczny dobór kompatybilnego rejestratora")

    if total_cam_count == 0:
        st.warning(
            "Najpierw dodaj kamery w zakładce 'Dobór Kamer' lub wybierz Szablon."
        )
    else:
        st.info(
            f"Wymagania systemowe: **Liczba kamer: {total_cam_count}** | **Wymagane pasmo: {total_bitrate:.1f} Mbps** | **Wsparcie AI: {'TAK' if requires_ai else 'NIE'}**"
        )

        compatible_nvrs = []
        for nvr in NVRS_DB:
            is_compat = True
            reasons = []

            if nvr["channels"] < total_cam_count:
                is_compat = False
                reasons.append(
                    f"Za mało kanałów (ma {nvr['channels']}, potrzeba {total_cam_count})"
                )
            if nvr["max_bandwidth_mbps"] < total_bitrate:
                is_compat = False
                reasons.append(
                    f"Zbyt małe pasmo (ma {nvr['max_bandwidth_mbps']} Mbps, potrzeba {total_bitrate:.1f} Mbps)"
                )
            if requires_ai and not nvr["supports_ai"]:
                is_compat = False
                reasons.append("Brak obsługi funkcji AI wymagalnych przez kamery")

            compatible_nvrs.append(
                {"nvr": nvr, "is_compat": is_compat, "reasons": reasons}
            )

        st.markdown("### Dostępne rejestratory:")
        selected_nvr_symbol = st.radio(
            "Wybierz rejestrator do zestawu:",
            options=[item["nvr"]["symbol"] for item in compatible_nvrs],
            format_func=lambda sym: next(
                f"{n['nvr']['name']} - {n['nvr']['price_netto']:.2f} PLN "
                + (
                    "✅ (Kompatybilny)"
                    if n["is_compat"]
                    else f"❌ (Niekompatybilny: {', '.join(n['reasons'])})"
                )
                for n in compatible_nvrs
                if n["nvr"]["symbol"] == sym
            ),
        )

        selected_nvr_obj = next(
            n["nvr"]
            for n in compatible_nvrs
            if n["nvr"]["symbol"] == selected_nvr_symbol
        )
        st.session_state.selected_nvr = selected_nvr_obj

# ---------------------------------------------------------
# ZAKŁADKA 4: AKCESORIA I DYSK (KALKULATOR PA MIEĆI)
# ---------------------------------------------------------
with tab_accessories:
    st.subheader("Kalkulator Dyskowy oraz Akcesoria")

    if total_cam_count == 0:
        st.warning("Dodaj kamery, aby obliczyć przestrzeń dyskową.")
    else:
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            days_retention = st.slider(
                "Oczekiwany czas przechowywania nagrań (dni):",
                min_value=3,
                max_value=60,
                value=14,
            )
            recording_hours = st.slider(
                "Średni czas nagrywania na dobę (godziny):",
                min_value=1,
                max_value=24,
                value=24,
            )

        # Kalkulacja GB: (Bitrate Mbps / 8) * 3600 sek * godziny * dni * kamery
        # Dysk w TB:
        required_tb = (
            (total_bitrate / 8.0) * 3600 * recording_hours * days_retention
        ) / 1000000.0

        with col_h2:
            st.metric(
                label="Wymagana pojemność dyskowa:",
                value=f"{required_tb:.2f} TB",
            )

            # Sugestia dysku
            if required_tb <= 2.0:
                sug_hdd = "HDD-2TB"
            elif required_tb <= 4.0:
                sug_hdd = "HDD-4TB"
            else:
                sug_hdd = "HDD-8TB"

            st.write(
                f"Sugerowany dysk: **{ACCESSORIES_DB[sug_hdd]['name']}**"
            )

        selected_hdd = st.selectbox(
            "Wybierz dysk HDD do oferty:",
            options=["Brak", "HDD-2TB", "HDD-4TB", "HDD-8TB"],
            index=["Brak", "HDD-2TB", "HDD-4TB", "HDD-8TB"].index(sug_hdd),
        )
        st.session_state.selected_hdd = selected_hdd

        st.markdown("---")
        st.markdown("### Zasilanie i Switche PoE:")

        selected_nvr = st.session_state.get("selected_nvr", None)
        needed_poe_ports = total_cam_count

        if selected_nvr and selected_nvr["poe_ports"] >= needed_poe_ports:
            st.success(
                f"✅ Rejestrator {selected_nvr['name']} posiada wbudowany switch PoE ({selected_nvr['poe_ports']} portów). Zewnętrzny switch nie jest wymagany."
            )
            selected_switch = "Brak"
        else:
            st.warning(
                f"⚠️ Rejestrator nie posiada wystarczającej liczby portów PoE. Wybierz switch zewnętrzny:"
            )
            selected_switch = st.selectbox(
                "Rekomendowany switch PoE:",
                options=["Brak", "SWITCH-POE-8", "SWITCH-POE-16"],
                index=1 if needed_poe_ports <= 8 else 2,
            )

        st.session_state.selected_switch = selected_switch

# ---------------------------------------------------------
# ZAKŁADKA 5: OFERTA HANDLOWA / PODSUMOWANIE
# ---------------------------------------------------------
with tab_quote:
    st.subheader("Podsumowanie Wyceny dla Klienta")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        margin_percent = st.number_input(
            "Narzut / Marża dystrybutora (%):",
            min_value=0.0,
            max_value=100.0,
            value=15.0,
        )
    with col_q2:
        vat_rate = st.selectbox("Stawka VAT:", options=[23, 8, 0], index=0)

    st.markdown("---")

    # Tabela pozycji
    quote_items = []

    # 1. Kamery i Puszki
    for item in st.session_state.selected_cameras:
        quote_items.append(
            {
                "nazwa": item["name"],
                "ilosc": item["qty"],
                "cena_netto_katalog": item["price_netto"],
            }
        )
        if item.get("add_box"):
            box_info = ACCESSORIES_DB[item["mount_box"]]
            quote_items.append(
                {
                    "nazwa": f"Puszka montażowa dla {item['symbol']}",
                    "ilosc": item["qty"],
                    "cena_netto_katalog": box_info["price_netto"],
                }
            )

    # 2. Rejestrator
    if "selected_nvr" in st.session_state and st.session_state.selected_nvr:
        nvr = st.session_state.selected_nvr
        quote_items.append(
            {
                "nazwa": nvr["name"],
                "ilosc": 1,
                "cena_netto_katalog": nvr["price_netto"],
            }
        )

    # 3. Dysk HDD
    hdd_sym = st.session_state.get("selected_hdd", "Brak")
    if hdd_sym != "Brak":
        hdd = ACCESSORIES_DB[hdd_sym]
        quote_items.append(
            {
                "nazwa": hdd["name"],
                "ilosc": 1,
                "cena_netto_katalog": hdd["price_netto"],
            }
        )

    # 4. Switch
    sw_sym = st.session_state.get("selected_switch", "Brak")
    if sw_sym != "Brak":
        sw = ACCESSORIES_DB[sw_sym]
        quote_items.append(
            {
                "nazwa": sw["name"],
                "ilosc": 1,
                "cena_netto_katalog": sw["price_netto"],
            }
        )

    if not quote_items:
        st.info("Brak pozycji w ofercie.")
    else:
        total_netto_zakup = 0.0
        total_netto_sprzedaz = 0.0

        st.markdown("#### Zestawienie Pozycji:")

        for row in quote_items:
            c_n = row["cena_netto_katalog"]
            c_s = c_n * (1 + margin_percent / 100.0)
            val_s = c_s * row["ilosc"]

            total_netto_zakup += c_n * row["ilosc"]
            total_netto_sprzedaz += val_s

            st.write(
                f"- **{row['nazwa']}** | Ilość: {row['ilosc']} | Cena spredaży netto: {c_s:.2f} PLN | Wartość netto: **{val_s:.2f} PLN**"
            )

        total_vat = total_netto_sprzedaz * (vat_rate / 100.0)
        total_brutto = total_netto_sprzedaz + total_vat

        st.markdown("---")
        col_tot1, col_tot2, col_tot3 = st.columns(3)
        with col_tot1:
            st.metric(
                label="Suma NETTO dla klienta:",
                value=f"{total_netto_sprzedaz:.2f} PLN",
            )
        with col_tot2:
            st.metric(
                label=f"Podatek VAT ({vat_rate}%):", value=f"{total_vat:.2f} PLN"
            )
        with col_tot3:
            st.metric(
                label="Suma BRUTTO:", value=f"{total_brutto:.2f} PLN"
            )

        st.caption(
            f"Twój zysk netto (Marża {margin_percent}%): **{(total_netto_sprzedaz - total_netto_zakup):.2f} PLN**"
        )

        st.download_button(
            label="📥 Pobierz ofertę handlową (.TXT)",
            data=f"OFERTA HANDLOWA CCTV\nWartość netto: {total_netto_sprzedaz:.2f} PLN\nWartość brutto: {total_brutto:.2f} PLN",
            file_name="oferta_cctv.txt",
            mime="text/plain",
        )