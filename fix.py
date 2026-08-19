import re

with open('src/dll/dllmain.cpp', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Beta badge CSS
target1 = "if (customCssW && customCssW[0]) css += CdpUtf8(customCssW);"
rep1 = target1 + "\n      css += \"body::after { content: 'YMHub BETA'; position: fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.2); color: rgba(255,255,255,0.4); padding: 4px 8px; font-weight: 600; font-family: sans-serif; font-size: 10px; border-radius: 6px; z-index: 999999; pointer-events: none; }\";"
text = text.replace(target1, rep1)

# 2. Add Beta feature HTML
target2 = 'L"<div class=\\"yc-sec\\" data-sec=\\"integrations\\"><div class=\\"yc-sectitle\\">"'
# But the string has non-ascii chars. Let's just use regex for the whole line.
text = re.sub(
    r'(L"<div class=\\"yc-sec\\" data-sec=\\"integrations\\"><div class=\\"yc-sectitle\\">.*?</div>")',
    r'\1\n          L"<div class=\\"yc-tw-row\\"><div class=\\"yc-tw-name\\" style=\\"color:#ff9900\\">[BETA] RGB Анимация плеера</div><div class=\\"yc-tw-switch\\" id=\\"yc-betargb\\"><div class=\\"yc-knob\\"></div></div></div>"',
    text
)

# 3. Add Beta feature JS handlers
target3 = r'(L"var swBridge=document.getElementById\(''yc-bridge''\);if\(window\.__ymhubBridge\)swBridge.classList.add\(''on''\);")'
rep3 = r'L"var swBeta=document.getElementById(''yc-betargb'');if(window.__ymhubBetaRgb)swBeta.classList.add(''on'');"\n          L"swBeta.onclick=function(){var on=!swBeta.classList.contains(''on'');swBeta.classList.toggle(''on'');window.__ymhubQ.push(''betargb:''+(on?1:0));};"\n          \1'
text = re.sub(target3, rep3, text)

# 4. Add Beta State JS injection
target4 = r'("window\.__ymhubDrpc=" \+ std::to_string\(g_discordEnabled \? 1 : 0\) \+ ";")'
rep4 = r'"window.__ymhubBetaRgb=" + std::to_string(g_betaRgb ? 1 : 0) + ";"\n          \1'
text = re.sub(target4, rep4, text)

# 5. Add Global state in C++
target5 = r'(static bool         g_discordEnabled = true;)'
rep5 = r'static bool         g_betaRgb = false;\n\1'
text = re.sub(target5, rep5, text)

# 6. Add dispatcher action
target6 = r'(if \(item.rfind\("drpc:", 0\) == 0\) {)'
rep6 = r'if (item.rfind("betargb:", 0) == 0) {\n          g_betaRgb = (item.substr(8) == "1");\n          RegSetDW(HKEY_CURRENT_USER, REG_APP, L"BetaRgb", g_betaRgb ? 1 : 0);\n          ApplyTweaksNow();\n          return;\n      }\n      \1'
text = re.sub(target6, rep6, text)

# 7. Apply CSS when BetaRgb is true
target7 = r'(if \(mask & \(1u << i\)\) css \+= kTweakRules\[i\];\n      })'
rep7 = r'\1\n      if (g_betaRgb) {\n          css += "[class*=''PlayerBarDesktop_root''], [class*=''VibePlayerBar_root''] { animation: rgbPulse 5s infinite; border-top: 1px solid transparent; } "\n                 "@keyframes rgbPulse { 0% { box-shadow: 0 -4px 20px rgba(255,0,0,0.3); border-color: rgba(255,0,0,0.5); } 33% { box-shadow: 0 -4px 20px rgba(0,255,0,0.3); border-color: rgba(0,255,0,0.5); } 66% { box-shadow: 0 -4px 20px rgba(0,0,255,0.3); border-color: rgba(0,0,255,0.5); } 100% { box-shadow: 0 -4px 20px rgba(255,0,0,0.3); border-color: rgba(255,0,0,0.5); } }";\n      }'
text = re.sub(target7, rep7, text)

# 8. Load state from registry
target8 = r'(g_customCss = RegGetStr\(HKEY_CURRENT_USER, REG_APP, L"CustomCss"\);)'
rep8 = r'\1\n      g_betaRgb = RegGetDW(HKEY_CURRENT_USER, REG_APP, L"BetaRgb", 0) != 0;'
text = re.sub(target8, rep8, text)

with open('src/dll/dllmain.cpp', 'w', encoding='utf-8') as f:
    f.write(text)
