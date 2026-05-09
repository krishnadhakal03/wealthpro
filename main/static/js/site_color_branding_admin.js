(function () {
    const palettes = {
        default_blue: { primary: "#0D6EFD", accent: "#38BDF8" },
        premium_dark: { primary: "#02070F", accent: "#3B82F6" },
        trust_navy: { primary: "#0B1F3A", accent: "#2F80ED" },
        modern_teal: { primary: "#0F3D3E", accent: "#2DD4BF" },
        executive_gold: { primary: "#111827", accent: "#D4AF37" },
        clean_blue: { primary: "#0D6EFD", accent: "#38BDF8" },
        carrier_classic: { primary: "#003366", accent: "#F2B705" },
    };

    function syncPalette() {
        const mode = document.getElementById("id_theme_mode");
        const primary = document.getElementById("id_theme_primary_color");
        const accent = document.getElementById("id_theme_accent_color");

        if (!mode || !primary || !accent || mode.value === "custom") {
            return;
        }

        const palette = palettes[mode.value];
        if (!palette) {
            return;
        }

        primary.value = palette.primary;
        accent.value = palette.accent;
    }

    document.addEventListener("DOMContentLoaded", function () {
        const mode = document.getElementById("id_theme_mode");
        if (!mode) {
            return;
        }

        mode.addEventListener("change", syncPalette);
    });
})();
