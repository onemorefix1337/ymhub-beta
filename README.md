# YMHub Beta

Beta branch for experimenting with new Yandex Music UI features.
YMHub is a DLL mod injected via Forge into the Yandex Music Desktop app.

## Beta Features
- **Vibe background brightness slider** - fully integrated into the mod menu. Adjust the brightness of the main animated background!
- **RGB player borders** - an animated RGB gradient outline for the player bar and controls. Includes full support for circular buttons.
- Full compatibility with the new React-based Yandex Music Desktop App.

## Auto-build via GitHub Actions
This repository is configured to auto-build the DLL on every new tag (starting with `v*`).
The built DLL will be attached as a Release artifact (`YMHubBetaDll.dll`).

## Setup
1. Clone this repository.
2. The GitHub Actions workflow automatically fetches the WebView2 SDK and builds the DLL.
