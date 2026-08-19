import re

with open('src/dll/dllmain.cpp', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''// Used to also own an IPC shared-memory struct and poll it for commands
// from the host'''

replacement = '''static DWORD WINAPI UpdateCheckThreadFn(LPVOID) {
    bool notified = false;
    while (g_run) {
        if (!notified) {
            HINTERNET hSes = WinHttpOpen(L"YMHub/" YMHUB_VERSION_W, WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
            if (hSes) {
                HINTERNET hCon = WinHttpConnect(hSes, L"api.github.com", INTERNET_DEFAULT_HTTPS_PORT, 0);
                if (hCon) {
                    HINTERNET hReq = WinHttpOpenRequest(hCon, L"GET", L"/repos/onemorefix1337/ymhub/releases/latest", nullptr, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE);
                    if (hReq) {
                        std::wstring headers = L"User-Agent: YMHub\\r\\n";
                        if (WinHttpSendRequest(hReq, headers.c_str(), (DWORD)-1, WINHTTP_NO_REQUEST_DATA, 0, 0, 0) && WinHttpReceiveResponse(hReq, nullptr)) {
                            DWORD status = 0; DWORD size = sizeof(status);
                            if (WinHttpQueryHeaders(hReq, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER, WINHTTP_HEADER_NAME_BY_INDEX, &status, &size, WINHTTP_NO_HEADER_INDEX) && status == 200) {
                                std::string body; DWORD avail = 0;
                                while (WinHttpQueryDataAvailable(hReq, &avail) && avail > 0) {
                                    std::string chunk(avail, 0); DWORD read = 0;
                                    if (WinHttpReadData(hReq, (LPVOID)chunk.data(), avail, &read) && read > 0) {
                                        chunk.resize(read); body += chunk;
                                    } else break;
                                }
                                auto pos = body.find("\\"tag_name\\":");
                                if (pos != std::string::npos) {
                                    pos = body.find('"', pos + 11);
                                    if (pos != std::string::npos) {
                                        auto end = body.find('"', pos + 1);
                                        if (end != std::string::npos) {
                                            std::string tag = body.substr(pos + 1, end - pos - 1);
                                            if (tag != "v" YMHUB_VERSION && tag != YMHUB_VERSION) {
                                                notified = true;
                                                std::wstring wtag(tag.begin(), tag.end());
                                                std::wstring js =
                                                    L"(function(){if(document.getElementById('ymhub-update'))return;"
                                                    L"var o=document.createElement('div');o.id='ymhub-update';"
                                                    L"o.style.cssText='position:fixed;top:20px;right:20px;z-index:999999;"
                                                    L"opacity:0;transform:translateY(-8px);"
                                                    L"transition:opacity .3s ease,transform .3s ease;pointer-events:none;';"
                                                    L"var card=document.createElement('div');"
                                                    L"card.style.cssText='display:flex;align-items:center;gap:12px;"
                                                    L"background:rgba(13,13,20,.88);backdrop-filter:blur(16px);"
                                                    L"border:1px solid rgba(91,143,255,.35);border-radius:14px;padding:12px 16px;"
                                                    L"box-shadow:0 0 0 1px rgba(91,143,255,.08),0 8px 28px rgba(0,0,0,.45),"
                                                    L"0 0 24px rgba(91,143,255,.18);min-width:230px;';"
                                                    L"var badge=document.createElement('div');"
                                                    L"badge.style.cssText='width:32px;height:32px;flex-shrink:0;border-radius:9px;"
                                                    L"background:#3DD68C;display:flex;align-items:center;justify-content:center;"
                                                    L"font-size:15px;color:#fff;';"
                                                    L"badge.textContent='\\\\u2191';"
                                                    L"var body=document.createElement('div');body.style.cssText='flex:1;min-width:0;';"
                                                    L"var row=document.createElement('div');"
                                                    L"row.style.cssText='display:flex;align-items:baseline;justify-content:space-between;gap:8px;';"
                                                    L"var title=document.createElement('div');"
                                                    L"title.textContent='YMHub Update';"
                                                    L"title.style.cssText='font:600 13.5px \\"Segoe UI Variable Text\\",\\"Segoe UI\\",sans-serif;"
                                                    L"color:rgba(255,255,255,.92);';"
                                                    L"row.appendChild(title);"
                                                    L"var sub=document.createElement('div');"
                                                    L"sub.textContent='Доступна версия ' + '";
                                                js += wtag;
                                                js += L"';"
                                                    L"sub.style.cssText='font:400 12px \\"Segoe UI Variable Text\\",\\"Segoe UI\\",sans-serif;"
                                                    L"color:rgba(255,255,255,.55);margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;';"
                                                    L"body.appendChild(row);body.appendChild(sub);"
                                                    L"card.appendChild(badge);card.appendChild(body);"
                                                    L"o.appendChild(card);document.body.appendChild(o);"
                                                    L"requestAnimationFrame(function(){o.style.opacity='1';o.style.transform='translateY(0)';});"
                                                    L"setTimeout(function(){o.style.opacity='0';o.style.transform='translateY(-8px)';setTimeout(function(){o.remove();},350);},8000);"
                                                    L"})()";
                                                {
                                                    std::lock_guard<std::mutex> lk(g_cdpMx);
                                                    if (CdpEnsureConnected()) {
                                                        std::string req = "{\\"id\\":11,\\"method\\":\\"Runtime.evaluate\\",\\"params\\":{\\"expression\\":\\"" + CdpJsonEscape(js) + "\\"}}";
                                                        if (CdpSend(req)) {
                                                            std::string r; CdpRecv(r);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        WinHttpCloseHandle(hReq);
                    }
                    WinHttpCloseHandle(hCon);
                }
                WinHttpCloseHandle(hSes);
            }
        }
        for (int i = 0; i < 300 && g_run; i++) Sleep(1000); // 5 minutes sleep
    }
    return 0;
}

// Used to also own an IPC shared-memory struct and poll it for commands
// from the host'''

if target in text:
    new_text = text.replace(target, replacement)
    with open('src/dll/dllmain.cpp', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Success")
else:
    print("Not found")
