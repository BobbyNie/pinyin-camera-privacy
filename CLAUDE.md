# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a documentation repository for the **拼音相机 (Pinyin Camera)** app's privacy policies. It is not an active code repository.

## Repository Structure

- `privacy.txt` / `privacy.html` — 隐私政策 (Simplified Chinese for Mainland China)
- `privacy_hk.txt` / `docs/privacy-hk.html` — 隱私政策 (Traditional Chinese for Hong Kong)
- `docs/marketing.html` / `docs/marketing-hk.html` — Marketing landing pages
- `docs/support.html` / `docs/support-hk.html` — Support/contact pages
- `docs/images/` — Screenshots for marketing pages (iPhone/iPad)

## Maintenance

### Privacy Policy Updates

When updating the privacy policy content:

1. Keep both policy files synchronized in meaning — they are the same content in different script variants
2. Update the "最后更新日期" / "最後更新日期" to the current month when making changes
3. Mainland China file uses simplified characters (简体中文)
4. Hong Kong file uses traditional characters (繁體中文) and traditional terms (e.g., "資料" vs "数据", "相簿" vs "相册")

### HTML Files

The `docs/` directory contains HTML versions that mirror the text content. When updating privacy policies, ensure both `.txt` and `.html` files stay synchronized.

File naming convention:
- No suffix = Simplified Chinese (Mainland China): `privacy.txt`, `marketing.html`
- `-hk` suffix = Traditional Chinese (Hong Kong): `privacy_hk.txt`, `marketing-hk.html`

## Git Workflow

- Default branch: `main`
- Remote: `https://github.com/BobbyNie/pinyin-camera-privacy`
- This repository may be used for GitHub Pages (serving from `docs/` directory)
