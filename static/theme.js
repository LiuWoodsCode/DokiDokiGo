import { baseLayerLuminance, StandardLuminance } from "./fwc.js";

const colorModeQuery = window.matchMedia("(prefers-color-scheme: dark)");

function applyColorMode() {
    baseLayerLuminance.setValueFor(
        document.body,
        colorModeQuery.matches ? StandardLuminance.DarkMode : StandardLuminance.LightMode
    );
}

colorModeQuery.addEventListener("change", applyColorMode);
applyColorMode();
