---
title: "SmartMembership: Building a Privacy-First Digital Loyalty Wallet on iOS"
description: "A technical deep dive into building a native iOS app for digitizing loyalty cards using SwiftUI, AVFoundation, and CoreImage, with a focus on local processing and robust barcode handling."
date: 2026-01-10
author: June Hong
tags: [iOS, Swift, SwiftUI, AVFoundation, CoreImage, Privacy]
---

## Introduction

We all have that one drawer (or wallet) overflowing with loyalty cards, gym passes, and library cards. While there are many apps to digitize these, many come with bloat: account requirements, cloud syncing, and data tracking.

**SmartMembership** is a lightweight, open-source iOS application designed to solve this simply and privately. It allows users to scan, store, and regenerate their membership cards entirely on-device.

In this post, I'll walk through the technical challenges of building a robust barcode scanner and renderer using native iOS frameworks.

---

## The Problem: Scanning vs. Rendering

Digitizing a card seems simple: take a picture, show the picture. However, photos of barcodes are often hard for laser scanners to read due to glare or screen reflections.

To ensure a 100% success rate at checkout, the app needs to:
1.  **Scan** the barcode data from the physical card.
2.  **Store** the raw string data and format type.
3.  **Regenerate** a crisp, high-contrast digital barcode on demand.

---

## Technical Deep Dive

### 1. Universal Scanning with AVFoundation

We used `AVFoundation` for real-time scanning. While the framework is powerful, we encountered a specific nuance with **UPC-A** barcodes.

UPC-A is common in North America (12 digits). However, iOS's `VNBarcodeObservation` often detects these as **EAN-13** (13 digits) by adding a leading zero.

To ensure data consistency, we implemented specific logic to normalize this:

```swift
// Logic to handle iOS detecting UPC-A as EAN-13
if type == .ean13 && code.hasPrefix("0") && code.count == 13 {
    // Strip leading zero to convert back to UPC-A
    return String(code.dropFirst())
}
```

### 2. Robust Rendering & The Fallback Strategy

For rendering, we utilized `CoreImage` filters (e.g., `CICode128BarcodeGenerator`, `CIEAN13BarcodeGenerator`).

A major challenge arose with **checksums**. EAN-13 and UPC-A formats require the last digit to be a mathematically valid checksum of the previous digits. If a user manually enters a number or a legacy card has a non-standard format, the Core Image filter returns `nil`.

To prevent the user from being stuck with an un-displayable card, we implemented a **Smart Fallback** mechanism:

> If the specific format generation (EAN-13/UPC) fails, the app automatically falls back to generating a **Code 128** barcode.

Code 128 is highly dense and supports any ASCII character set, making it a safe "catch-all" that most modern POS scanners can read.

### 3. Privacy with SwiftData

Since the goal was a digital wallet, not a data harvesting tool, we opted for **SwiftData** for local persistence. There is no backend, no analytics, and no internet permission required.

---

## Conclusion

SmartMembership demonstrates that useful, everyday utilities can be built without compromising privacy or relying on heavy third-party SDKs. By leveraging `AVFoundation` and `CoreImage` intelligently, we created a seamless bridge between physical cards and digital wallets.
