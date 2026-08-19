if(NOT DEFINED WV2_SDK)
    message(FATAL_ERROR
        "WV2_SDK is not set. Point it at an extracted Microsoft.Web.WebView2 "
        "NuGet package, e.g.:\n"
        "  nuget install Microsoft.Web.WebView2 -Version 1.0.2592.51 -OutputDirectory webview2sdk\n"
        "  cmake -S . -B build -A x64 -DWV2_SDK=\"<path>\\webview2sdk\\Microsoft.Web.WebView2.1.0.2592.51\"")
endif()

add_library(YMHubBetaDll SHARED dllmain.cpp)
target_compile_definitions(YMHubBetaDll PRIVATE UNICODE _UNICODE WIN32_LEAN_AND_MEAN NOMINMAX)
target_compile_options(YMHubBetaDll PRIVATE /std:c++20 /D_SILENCE_EXPERIMENTAL_COROUTINE_DEPRECATION_WARNINGS /Zi)
set_property(TARGET YMHubBetaDll PROPERTY MSVC_RUNTIME_LIBRARY "MultiThreaded")
target_include_directories(YMHubBetaDll PRIVATE "${WV2_SDK}/build/native/include")
target_link_libraries(YMHubBetaDll PRIVATE
    "${WV2_SDK}/build/native/x64/WebView2LoaderStatic.lib"
    user32 kernel32 gdi32 dwmapi dbghelp comctl32
    runtimeobject windowscodecs shcore ole32 oleaut32)
target_link_options(YMHubBetaDll PRIVATE /DEBUG)
set_target_properties(YMHubBetaDll PROPERTIES
    INTERPROCEDURAL_OPTIMIZATION TRUE
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    OUTPUT_NAME "YMHubBetaDll")
