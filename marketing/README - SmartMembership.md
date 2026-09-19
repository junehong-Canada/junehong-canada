# SmartMembership

**Digital Loyalty Card Wallet**

SmartMembership is a lightweight and efficient iOS application designed to digitize your physical membership and loyalty cards. Keep your wallet slim and your cards organized in one secure place.

## Key Features

*   **Universal Scanner**: Instantly scan physical cards using your device's camera.
    *   Supports **QR Codes**, **EAN-13**, **UPC-A**, and **Code 128**.
    *   Includes specific logic to correctly identify UPC-A barcodes that iOS detects as EAN-13 (by handling leading zeros).
*   **High-Quality Rendering**: Generates crisp, scannable barcodes on-screen.
    *   **Smart Fallback**: Includes logic to ensure your barcode is always readable. If a specific format generation (e.g., EAN-13) fails due to checksum errors, the app falls back to generating a Code 128 barcode.
*   **Digital Card Wallet**: View your cards with a generated visual layout displaying your name, membership number, and barcode.
*   **Privacy Focused**: All processing happens locally on your device using native iOS frameworks.

## Technical Overview

This project is built using native iOS frameworks to ensure performance and privacy:

*   **Scanning**: Implemented via `BarcodeScannerViewController` using `AVFoundation` for real-time capture.
*   **Rendering**: Uses `BarcodeRenderer` with `CoreImage` to generate barcode images from string data.
*   **Card Visualization**: Uses `generateCardImage` to create composite images of the membership card containing the user's name, card number, and the generated barcode.

## Usage

1.  Tap scan to capture a barcode from a physical card.
2.  The app automatically detects the barcode type (including correcting UPC-A codes scanned as EAN-13).
3.  Save the card and present your screen at the store checkout.

## Contact

For inquiries, email: junehong.dominicus@gmail.com

---
*Version 1.0.0*