const fs = require('fs');

let text = fs.readFileSync('src/dll/dllmain.cpp', 'utf-8');

// 1. Beta badge CSS
const target1 = "if (customCssW && customCssW[0]) css += CdpUtf8(customCssW);";
const rep1 = target1 + "\n      css += \"body::after { content: 'YMHub BETA'; position: fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.2); color: rgba(255,255,255,0.4); padding: 4px 8px; font-weight: 600; font-family: sans-serif; font-size: 10px; border-radius: 6px; z-index: 999999; pointer-events: none; }\";";
text = text.replace(target1, rep1);

// 2. Add Beta feature HTML
const target2 = /(L"<div class=\\"yc-sec\\" data-sec=\\"integrations\\"><div class=\\"yc-sectitle\\">.*?<\/div>")/g;
const rep2 = "\n          L\"<div class=\\\"yc-tw-row\\\"><div class=\\\"yc-tw-name\\\" style=\\\"color:#ff9900\\\">[BETA] RGB Анимация плеера</div><div class=\\\"yc-tw-switch\\\" id=\\\"yc-betargb\\\"><div class=\\\"yc-knob\\\"></div></div></div>\"";
text = text.replace(target2, rep2);

// 3. Add Beta feature JS handlers
const target3 = /(L"var swBridge=document\.getElementById\('yc-bridge'\);if\(window\.__ymhubBridge\)swBridge\.classList\.add\('on'\);")/g;
const rep3 = "L\"var swBeta=document.getElementById('yc-betargb');if(window.__ymhubBetaRgb)swBeta.classList.add('on');\"\n          L\"swBeta.onclick=function(){var on=!swBeta.classList.contains('on');swBeta.classList.toggle('on');window.__ymhubQ.push('betargb:'+(on?1:0));};\"\n          ";
text = text.replace(target3, rep3);

// 4. Add Beta State JS injection
const target4 = /("window\.__ymhubDrpc=" \+ std::to_string\(g_discordEnabled \? 1 : 0\) \+ ";")/g;
const rep4 = "\"window.__ymhubBetaRgb=\" + std::to_string(g_betaRgb ? 1 : 0) + \";\"\n          ";
text = text.replace(target4, rep4);

// 5. Add Global state in C++
const target5 = /(static bool         g_discordEnabled = true;)/g;
const rep5 = "static bool         g_betaRgb = false;\n";
text = text.replace(target5, rep5);

// 6. Add dispatcher action
const target6 = /(if \(item\.rfind\("drpc:", 0\) == 0\) \{)/g;
const rep6 = "if (item.rfind(\"betargb:\", 0) == 0) {\n          g_betaRgb = (item.substr(8) == \"1\");\n          RegSetDW(HKEY_CURRENT_USER, REG_APP, L\"BetaRgb\", g_betaRgb ? 1 : 0);\n          ApplyTweaksNow();\n          return;\n      }\n      ";
text = text.replace(target6, rep6);

// 7. Apply CSS when BetaRgb is true
const target7 = /(if \(mask & \(1u << i\)\) css \+= kTweakRules\[i\];\n      \})/g;
const rep7 = "\n      if (g_betaRgb) {\n          css += \"[class*='PlayerBarDesktop_root'], [class*='VibePlayerBar_root'] { animation: rgbPulse 5s infinite; border-top: 1px solid transparent; } \"\n                 \"@keyframes rgbPulse { 0% { box-shadow: 0 -4px 20px rgba(255,0,0,0.3); border-color: rgba(255,0,0,0.5); } 33% { box-shadow: 0 -4px 20px rgba(0,255,0,0.3); border-color: rgba(0,255,0,0.5); } 66% { box-shadow: 0 -4px 20px rgba(0,0,255,0.3); border-color: rgba(0,0,255,0.5); } 100% { box-shadow: 0 -4px 20px rgba(255,0,0,0.3); border-color: rgba(255,0,0,0.5); } }\";\n      }";
text = text.replace(target7, rep7);

// 8. Load state from registry
const target8 = /(g_customCss = RegGetStr\(HKEY_CURRENT_USER, REG_APP, L"CustomCss"\);)/g;
const rep8 = "\n      g_betaRgb = RegGetDW(HKEY_CURRENT_USER, REG_APP, L\"BetaRgb\", 0) != 0;";
text = text.replace(target8, rep8);

fs.writeFileSync('src/dll/dllmain.cpp', text, 'utf-8');
