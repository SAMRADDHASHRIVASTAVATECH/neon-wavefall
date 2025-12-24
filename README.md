# Project Overview

© 2025 ARCHOTECT. All rights reserved.

This software is proprietary and confidential.
Unauthorized copying, modification, distribution, or use of this software,
via any medium, is strictly prohibited without explicit written permission
from the author.

---

## Introduction

Most consumer audio technologies—most notably Bluetooth—are fundamentally
designed for one-to-one audio transmission. At any given time, a single
source device can typically stream audio to only one output device.

This project was developed to overcome that limitation.

It provides a one-to-many audio streaming system that allows audio from a
single source device to be delivered simultaneously to multiple devices
over a local network, while maintaining centralized control and real-time
processing.

screenshots are as follows:

<img width="949" height="497" alt="Screenshot 2025-12-24 161646" src="https://github.com/user-attachments/assets/785948ab-d027-4c30-87b9-429f5d92ee76" />


<img width="944" height="485" alt="Screenshot 2025-12-24 161731" src="https://github.com/user-attachments/assets/a10c7425-f0d3-4e4a-8a1a-23e4ec65e460" />


---

## What This System Does (Simple Explanation)

- One device plays or captures audio
- The audio is processed in real time on that device
- The audio is streamed once over the local network
- Multiple devices can listen at the same time
- All listeners remain synchronized to the same source

Listener devices require only a web browser and access to the same local
network. No pairing, no cloud services, and no third-party platforms
are involved.

---

## Technical Description

This project is a real-time audio platform that integrates:

- Audio playback and file-based processing
- System-level real-time audio capture and output
- A low-latency digital signal processing pipeline
- A built-in LAN audio broadcaster
- A browser-based client interface for listener devices

Rather than establishing individual connections per device (as Bluetooth
does), the system operates using a centralized broadcast model. Audio is
generated and processed once, then distributed to multiple clients
concurrently over the local network.

All control logic, effects, and signal routing remain on the source device.

---

## Problems This Project Solves

- Bluetooth audio is limited to a single connected output device
- Switching or reconnecting devices interrupts playback
- Multi-device listening requires duplicated setups or additional hardware

This system:
- Enables simultaneous multi-device audio playback
- Maintains a single authoritative audio source
- Eliminates device pairing and reconnection overhead
- Operates entirely within a local network environment

---

## Core Capabilities

- One-to-many audio streaming
- Real-time audio processing and effects
- Centralized audio control from a single device
- Multi-device listening via standard web browsers
- Stable operation under continuous processing load

---

## Design Philosophy

The system is designed with the following priorities:

- Clarity — one source, many listeners
- Stability — resilient under real-time processing
- Accessibility — no client-side installation required
- Control — all audio logic remains centralized

The architecture favors predictable behavior, transparency, and
maintainability over opaque or cloud-dependent solutions.

---

## Conceptual Inspiration

The system draws inspiration from conceptual audio distribution models
often depicted in futuristic and cinematic scenarios, where a single
source seamlessly broadcasts sound to multiple endpoints in perfect
synchronization.

This project translates that conceptual idea into a practical,
real-world implementation using modern software-based audio processing
and local network communication, without reliance on specialized
hardware or external services.

---

## Installation

### System Requirements

- Windows OS
- Python 3.10 or newer
- A supported audio device
- Local network connection (LAN or Wi-Fi)

### Dependencies

Install required Python packages using pip:

pip install pyqt6 numpy sounddevice

---

## Recommended Audio Driver (Strongly Recommended)

For best performance, stability, and proper system-audio capture,
it is **strongly recommended** to install a virtual audio driver.

### VB-Audio Virtual Cable

Download and install:
https://vb-audio.com/Cable/

This driver enables clean routing of system audio into the application
and significantly improves reliability and performance.

---

## Windows Sound Configuration (IMPORTANT)

After installing VB-Audio Virtual Cable:

1. Open **Windows Sound Settings**
2. Go to the **Sound** section
3. Under **Output**, select:
   **CABLE Input (VB-Audio Virtual Cable)**
4. Under **Input**, select:
   **CABLE Output (VB-Audio Virtual Cable)**

This step is required for proper system audio routing and is necessary
for the application to capture and stream system audio correctly.

---

## Running the Application

From the project root directory, run:

python synthesis.py

When the application starts:

- The source device controls playback and processing
- A local network URL will be displayed
- Listener devices can open that URL in a web browser
- Multiple devices can connect and listen simultaneously

No additional software is required on listener devices.

---

## Usage Notice

This project is not open source.

Viewing this repository does not grant permission to:
- Copy or reuse the source code
- Modify or redistribute any portion of the project
- Claim authorship or derive competing works

All rights are reserved by the author.

---

## Author

Samraddha Shrivastava

For licensing inquiries or permission requests, contact the author directly.
