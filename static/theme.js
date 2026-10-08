import { setTheme } from "./fwc.js";
import { webDarkTheme, webLightTheme } from "./fluent-themes.js";
import { legacyDarkPalette, legacyLightPalette } from "./legacy-palette.js";

const colorModeQuery = window.matchMedia("(prefers-color-scheme: dark)");
const lightTheme = { ...webLightTheme, ...legacyLightPalette };
const darkTheme = { ...webDarkTheme, ...legacyDarkPalette };

function applyColorMode() {
    setTheme(colorModeQuery.matches ? darkTheme : lightTheme);
}

colorModeQuery.addEventListener("change", applyColorMode);
applyColorMode();
