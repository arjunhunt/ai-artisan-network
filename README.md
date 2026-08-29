# 🧵 AI Artisan Commerce Network
> **“From Craft to Customer — with AI & Fair Wages”**  
> *Smart India Hackathon (SIH 2026) Prototype | Theme: Heritage, Culture & AI Digital Inclusion*  
> **Team**: `SIH TEAM A`

---

## 🌟 Overview
The **AI Artisan Commerce Network** is an autonomous AI enablement, GI verification, and fair-pricing digital layer built for traditional Indian handloom and handicraft artisans. It empowers rural creators to onboard via local voice dialects, protects them against middleman exploitation through statutory cost-plus pricing algorithms, validates Geographical Indication (GI) provenance, and broadcasts inventory across the open **ONDC (Open Network for Digital Commerce)** network using Beckn Protocol JSON-LD schemas.

---

## 🚀 Key Features

1. **🎙️ Indic Voice-to-Catalog Engine (Bhashini AI Simulation)**:
   * Zero-typing onboarding allowing rural artisans to speak in native dialects (Marathi, Hindi, Tamil, Bengali, English).
   * Generates market-ready product descriptions, extracts dimensions/weights, and detects GI tags.

2. **⚖️ Statutory Fair-Pricing & Wage Protection Engine**:
   * Automated cost-plus wage formulation using state-level skilled artisan wage benchmarks (`₹65.00/hr` for Maharashtra).
   * **Active Underpricing Defense**: Real-time alerts warning artisans when intended retail prices fall below production break-even floors.

3. **🛡️ National GI Tag Verification & Digital Certificates**:
   * Direct validation against the National Geographical Indication Registry database.
   * Cryptographic verification badges and digital provenance certificates.

4. **🔒 10-Stage Trust Escrow State Machine**:
   * Seamless progression: `ORDER_CREATED` $\rightarrow$ `PAYMENT_SECURED` $\rightarrow$ `ARTISAN_ACCEPTED` $\rightarrow$ `CRAFTING` $\rightarrow$ `QUALITY_CHECK` $\rightarrow$ `DISPATCHED` $\rightarrow$ `DELIVERED` $\rightarrow$ `ESCROW_RELEASED`.
   * Payouts locked in escrow vault and automatically disbursed upon delivery confirmation.

5. **🚚 Pan-India Logistics & Real-Time Tracking**:
   * 6-digit Indian PIN code serviceability check across 28 states & UTs via India Post SpeedPost adapter.
   * Event-based delivery milestone timeline.

6. **💬 Direct Artisan ↔ Buyer Chat with AI Translation**:
   * Order-specific messaging with bidirectional Indic dialect translation (e.g. Marathi $\leftrightarrow$ English).

7. **🏛️ Administrative Control Center & Audit Log**:
   * Live ecosystem metrics (GMV, Escrow vault, middleman leakage eliminated).
   * Artisan application review/moderation, AI seasonal demand forecasting, and immutable audit logs.

8. **🌐 ONDC Beckn Protocol Integration**:
   * Real-time generation of Beckn JSON-LD discovery schemas (`bpp/descriptor`, `bpp/providers`, `items`, `price`) for instant catalog indexing across buyer apps (Paytm, Mystore, Pincode).

9. **📡 Offline / Low-Bandwidth Draft Mode**:
   * Local draft caching for rural connectivity drops with automatic background synchronization.

---

## 👥 Demo Personas (1-Click Switcher)

| Persona | Role | Identifier | Focus |
| :--- | :--- | :--- | :--- |
| **Savita Tai** | Master Artisan | `DEMO-ARTISAN-001` | Paithani Silk Handloom Weaver (Yeola, Maharashtra) |
| **Sunita Devi** | Folk Artist | `DEMO-ARTISAN-002` | Madhubani Mithila Painting (Bihar) |
| **Rajesh Kumar** | Verified Buyer | `DEMO-BUYER-001` | Fair-Trade Handloom Purchaser (Bengaluru, Karnataka) |
| **SIH Official** | State Admin | `DEMO-ADMIN-001` | Ecosystem Governance, Moderation & Audit Oversight |

---

## ⚡ Quickstart Guide

### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 2. Start the Server
```bash
python server.py
```

### 3. Open in Browser
Visit **`http://localhost:8000`** in your browser.  
Interactive API Docs (Swagger UI) available at **`http://localhost:8000/docs`**.

---

## 🧪 Run Automated Verification Tests
```bash
python test_suite.py
```

---

*Built with ❤️ for Indian Artisans and the Smart India Hackathon 2026.*
