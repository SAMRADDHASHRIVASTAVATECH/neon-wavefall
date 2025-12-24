"""
AURA HYBRID — Ultimate Audio Suite (Pro Stable Build v7 + Copy Link)
------------------------------------------------
COMBINED ARCHITECTURE:
1. AURA Player (WAVEMIND) - Full Library & Player.
2. NEURO Core (Aftershock) - Stability Fixes Applied.
3. LAN STREAM CASTER - Blocking Sockets for guaranteed data integrity.

FEATURES:
  - LAN Streaming: Listen on any phone/laptop via Browser.
  - Web Interface: Premium Sci-Fi Frontend with Play/Pause & Visualizer.
  - Resilience: Auto-finds open ports if 5050 is locked.
  - UX: "Copy Link" button for easy sharing.
"""

from __future__ import annotations

import sys
import os
import math
import time
import random
import wave
import gc
import sqlite3
import ctypes
import socket
import struct
import threading
import queue
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any

import numpy as np

# --- IMPORTS & CHECKS ---
try:
    from PyQt6.QtCore import (
        Qt, QTimer, QSize, QRectF, QPointF, QThread, pyqtSignal, QObject, QUrl
    )
    from PyQt6.QtGui import (
        QColor, QFont, QPainter, QPainterPath, QPen, QBrush,
        QLinearGradient, QRadialGradient, QIcon, QPixmap,
        QDragEnterEvent, QPolygonF, QAction
    )
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QSlider, QFileDialog, QMessageBox,
        QLineEdit, QTreeWidget, QTreeWidgetItem, QFrame,
        QDial, QComboBox, QGroupBox, QCheckBox,
        QSizePolicy, QProgressBar, QTabWidget, QSystemTrayIcon, QMenu,
        QScrollArea, QGridLayout, QRadioButton
    )
    from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
except ImportError as e:
    raise SystemExit(f"PyQt6 is required. pip install pyqt6 numpy\nError: {e}")

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("WARNING: 'sounddevice' not found. 'System Core' tab will be disabled.")

# --- SYSTEM PRIORITY ---
def set_high_priority():
    try:
        if sys.platform == 'win32':
            # HIGH_PRIORITY_CLASS = 0x00000080
            ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000080)
    except Exception:
        pass

set_high_priority()


# ============================================================================
# PART 1: DATA & PRESETS
# ============================================================================

# --- WAVEMIND (PLAYER) FEATURES ---
PLAYER_FEATURES: Dict[str, Dict[str, List[str]]] = {
    "🔊 Core Audio Effects": {
        "Equalizer (EQ)": ["Graphic EQ", "Parametric EQ", "Dynamic EQ", "Linear Phase EQ", "Tilt EQ", "Bass boost", "Treble boost"],
        "Volume & Dynamics": ["Gain", "Loudness normalization", "Smart volume leveling", "Peak limiter", "Compressor", "Multiband compressor"],
        "Stereo & Spatial": ["Stereo widening", "Mono downmix", "Mid/Side control", "Crossfeed"],
        "Ambience": ["Reverb", "Room reverb", "Hall reverb", "Plate reverb"],
    },
    "🎚️ Editing & Time": {
        "Structure": ["Trim", "Fade in", "Fade out", "Crossfade"],
        "Time Manipulation": ["Stretch", "Warp", "Reverse playback"]
    },
    "🧠 AI & Special": {
        "Intelligent": ["AI mastering", "Stem separation", "Vocal isolation"],
        "Playback": ["Night mode EQ", "Focus mode clarity", "8D Audio Sim"]
    },
    "📀 Mastering": {
        "Finalization": ["Master EQ", "Limiter", "Dither", "Loudness targeting (LUFS)", "True peak limiting"]
    }
}

# --- WAVEMIND (PLAYER) PRESETS ---
PLAYER_PRESETS = {
    "--- Custom / Modified ---": {"i": 0.5, "w": 0.5, "fx": []},
    "💣 BASS GOD": {"i": 1.0, "w": 1.0, "fx": ["Bass boost", "Sub-bass generator", "Peak limiter", "Compressor"]},
    "💥 BOOM 3D SIM": {"i": 0.9, "w": 1.0, "fx": ["8D Audio Sim", "Bass boost", "Stereo widening", "Hall reverb"]},
    "💎 CRYSTAL CLEAR": {"i": 0.7, "w": 0.8, "fx": ["Treble boost", "Linear Phase EQ", "Dynamic EQ", "Peak limiter"]},
    "🏎️ MAX LOUDNESS": {"i": 1.0, "w": 1.0, "fx": ["Peak limiter", "Compressor", "Loudness normalization", "Tube warmth"]},
    "🔥 Club Master": {"i": 0.85, "w": 0.80, "fx": ["Bass boost", "Compressor", "Limiter", "Stereo widening"]},
    "🎸 Rock/Metal Polish": {"i": 0.80, "w": 0.65, "fx": ["Distortion", "Graphic EQ", "Compressor", "Stereo widening"]},
    "🎻 Classical Concert": {"i": 0.70, "w": 0.50, "fx": ["Hall reverb", "Linear Phase EQ", "Dynamic EQ"]},
    "🎷 Jazz Lounge": {"i": 0.60, "w": 0.40, "fx": ["Room reverb", "Tube warmth", "Mid-range shaping"]},
    "🎤 Hip Hop Slam": {"i": 0.90, "w": 0.85, "fx": ["Sub-bass generator", "Compressor", "Transient shaper"]},
    "🎹 Techno Rumble": {"i": 0.95, "w": 0.90, "fx": ["Bass boost", "Stereo widening", "Sidechain simulation", "Limiter"]},
    "🔊 Dubstep Grime": {"i": 0.95, "w": 1.0, "fx": ["Distortion", "Multi-band compressor", "Bass enhancer"]},
    "🎧 Generic Earbuds": {"i": 0.75, "w": 1.0, "fx": ["Bass boost", "Treble boost", "Crossfeed"]},
    "🎧 Open-Back Air": {"i": 0.60, "w": 0.40, "fx": ["Bass boost", "Crossfeed"]},
    "🚗 Car Bass Test": {"i": 0.95, "w": 1.0, "fx": ["Sub-bass generator", "Dynamic bass boost", "Peak limiter"]},
    "🚗 Highway Drive": {"i": 0.85, "w": 1.0, "fx": ["Compressor", "Loudness normalization", "Treble boost"]},
    "🎙️ Podcast Clarity": {"i": 0.60, "w": 1.0, "fx": ["Vocal isolation", "De-esser", "Compressor", "Smart volume leveling"]},
    "🧚 Airy Vocals": {"i": 0.50, "w": 0.40, "fx": ["Treble boost", "Plate reverb", "Exciter"]},
    "☕ Lo-Fi Study": {"i": 0.65, "w": 0.60, "fx": ["Sample rate reduction", "Tape warmth", "Low-pass filter"]},
    "🌃 Night Drive": {"i": 0.55, "w": 0.50, "fx": ["Stereo widening", "Bass boost", "Reverb", "Tilt EQ"]},
    "🌀 8D Audio Sim": {"i": 0.90, "w": 1.0, "fx": ["8D Audio Sim", "Stereo widening", "Reverb"]},
    "👣 Footsteps Focus": {"i": 0.80, "w": 1.0, "fx": ["Treble boost", "Compressor", "Graphic EQ", "Smart volume leveling"]},
    "⚔️ Cinematic RPG": {"i": 0.70, "w": 0.60, "fx": ["Stereo widening", "Bass boost", "Hall reverb"]},
    "🕰️ 1920s Gramophone": {"i": 0.90, "w": 1.0, "fx": ["Band-pass filter", "Noise generator", "Mono downmix"]},
    "📼 Old Telephone": {"i": 0.90, "w": 1.0, "fx": ["Band-pass filter", "Bitcrusher", "Distortion"]},
    "🧼 Clean Master": {"i": 0.60, "w": 1.0, "fx": ["Multiband compressor", "Master EQ", "True peak limiting"]},
}

# --- AFTERSHOCK (SYSTEM CORE) PRESETS ---
SYSTEM_PRESETS = {
    "🚀 EXTREME BOOSTERS": {
        "💣 BASS GOD":       {"bass": 3.0, "treble": 1.0, "loudness": 1.5, "spatial": 0.5, "color": "#FF0040"},
        "☢️ NUKE BASS":      {"bass": 5.0, "treble": 0.8, "loudness": 1.6, "spatial": 0.3, "color": "#D70000"},
        "💥 MEGA BOOM":      {"bass": 2.5, "treble": 1.2, "loudness": 1.8, "spatial": 0.6, "color": "#FF4500"},
        "👂 EAR RAPE":       {"bass": 4.0, "treble": 4.0, "loudness": 3.0, "spatial": 0.1, "color": "#000000"},
        "🔊 LOUDNESS MAX":   {"bass": 1.5, "treble": 1.5, "loudness": 2.5, "spatial": 0.2, "color": "#FFD700"},
        "💎 CRYSTAL CLEAR":  {"bass": 0.8, "treble": 3.5, "loudness": 1.4, "spatial": 0.6, "color": "#00CED1"},
        "⛰️ HIGH PEAKS":     {"bass": 1.0, "treble": 4.0, "loudness": 1.2, "spatial": 0.4, "color": "#E0FFFF"},
        "🔨 HARD HITTING":   {"bass": 3.5, "treble": 1.5, "loudness": 1.9, "spatial": 0.4, "color": "#8B0000"},
        "🌪️ TURBO":          {"bass": 2.5, "treble": 2.5, "loudness": 2.0, "spatial": 0.7, "color": "#FF8C00"},
        "📏 FLATTENED":      {"bass": 1.0, "treble": 1.0, "loudness": 1.0, "spatial": 0.0, "color": "#808080"},
    },
    "🌀 8D & SPATIAL FX": {
        "🌀 8D Motion":      {"bass": 1.0, "treble": 1.0, "loudness": 1.0, "spatial": 0.5, "pan_depth": 0.7, "pan_speed": 0.12, "phase_offset": 0.3, "delay_ms": 5, "head_shadow": 0.4, "distance": 0.3, "color": "#00FFFF"},
        "🌌 Galaxy Surround": {"bass": 1.5, "treble": 1.2, "loudness": 1.0, "spatial": 2.5, "pan_depth": 0.5, "pan_speed": 0.08, "phase_offset": 0.2, "delay_ms": 10, "head_shadow": 0.3, "distance": 0.5, "color": "#9400D3"},
        "😵 Dizzy Spin":      {"bass": 1.2, "treble": 1.2, "loudness": 1.0, "spatial": 1.8, "pan_depth": 1.0, "pan_speed": 0.8, "phase_offset": 0.5, "delay_ms": 2, "head_shadow": 0.6, "distance": 0.1, "color": "#FF00FF"},
        "🏟️ Wide Arena":      {"bass": 1.8, "treble": 1.0, "loudness": 1.2, "spatial": 1.5, "pan_depth": 0.2, "pan_speed": 0.05, "phase_offset": 0.1, "delay_ms": 15, "head_shadow": 0.2, "distance": 0.7, "color": "#4169E1"},
    },
    "🎮 GAMING: COMPETITIVE": {
        "👣 Footsteps Pro":  {"bass": 0.6, "treble": 2.5, "loudness": 1.5, "spatial": 0.8, "color": "#8B4513"},
        "🎯 FPS Focus":      {"bass": 0.8, "treble": 2.2, "loudness": 1.4, "spatial": 0.7, "color": "#556B2F"},
        "🔭 Sniper":         {"bass": 0.9, "treble": 2.5, "loudness": 1.3, "spatial": 0.9, "color": "#2F4F4F"},
        "🏟️ MOBA Arena":     {"bass": 1.5, "treble": 1.5, "loudness": 1.2, "spatial": 0.6, "color": "#483D8B"},
        "🗣️ Voice Chat":     {"bass": 0.5, "treble": 1.8, "loudness": 1.5, "spatial": 0.2, "color": "#20B2AA"},
    },
    "🗡️ GAMING: IMMERSION": {
        "💥 Action RPG":     {"bass": 2.5, "treble": 1.5, "loudness": 1.6, "spatial": 0.6, "color": "#FF4500"},
        "🏎️ Racing Sim":     {"bass": 2.8, "treble": 1.2, "loudness": 1.7, "spatial": 0.5, "color": "#B22222"},
        "👻 Horror":         {"bass": 2.2, "treble": 2.0, "loudness": 1.5, "spatial": 0.9, "color": "#000000"},
        "🌍 Open World":     {"bass": 1.8, "treble": 1.6, "loudness": 1.3, "spatial": 0.8, "color": "#228B22"},
        "🚀 Sci-Fi":         {"bass": 2.0, "treble": 2.2, "loudness": 1.4, "spatial": 0.7, "color": "#00FFFF"},
    },
    "✨ VIBE & ATMOSPHERE": {
        "🌃 Night Drive":    {"bass": 2.2, "treble": 1.2, "loudness": 1.3, "spatial": 0.7, "color": "#191970"},
        "🌧️ Rainy Day":      {"bass": 1.4, "treble": 0.8, "loudness": 1.1, "spatial": 0.6, "color": "#708090"},
        "☕ Coffee Shop":    {"bass": 1.2, "treble": 1.1, "loudness": 1.0, "spatial": 0.8, "color": "#D2691E"},
        "🏋️ Gym Pump":       {"bass": 3.0, "treble": 1.5, "loudness": 1.8, "spatial": 0.4, "color": "#FF0000"},
    },
}

# ============================================================================
# PART 2: SHARED UTILITIES
# ============================================================================

def read_wav(path: str) -> Tuple[np.ndarray, int]:
    try:
        with wave.open(path, "rb") as wf:
            ch = wf.getnchannels()
            sr = wf.getframerate()
            sampwidth = wf.getsampwidth()
            nframes = wf.getnframes()
            raw = wf.readframes(nframes)
        
        if sampwidth == 1:
            data = np.frombuffer(raw, dtype=np.uint8).astype(np.float64)
            data -= 128.0; data /= 128.0
        elif sampwidth == 2:
            data = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
            data /= 32768.0
        elif sampwidth == 3:
            a = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
            b = (a[:, 0].astype(np.int32) | (a[:, 1].astype(np.int32) << 8) | (a[:, 2].astype(np.int32) << 16))
            mask = (b & 0x800000) != 0; b[mask] |= 0xFF000000
            data = b.astype(np.float64) / 8388608.0
        elif sampwidth == 4:
            data = np.frombuffer(raw, dtype=np.int32).astype(np.float64) / 2147483648.0
        else:
            raise ValueError(f"Unsupported bit depth: {sampwidth*8}")

        if ch > 1: data = data.reshape(-1, ch)
        else: data = data.reshape(-1, 1)

        del raw; gc.collect()
        return np.clip(data, -1.0, 1.0), sr
    except Exception as e:
        raise IOError(f"Read error: {e}")

def write_wav(path: str, audio: np.ndarray, sr: int) -> None:
    audio = np.clip(audio, -1.0, 1.0)
    pcm = (audio * 2147483647.0).astype(np.int32)
    ch = 1 if pcm.ndim == 1 else pcm.shape[1]
    with wave.open(path, "wb") as wf:
        wf.setnchannels(ch); wf.setsampwidth(4); wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    del pcm; gc.collect()

def db_to_lin(db: float) -> float:
    return float(10.0 ** (db / 20.0))

# ============================================================================
# PART 3: WAVEMIND (PLAYER) LOGIC
# ============================================================================

def wm_one_pole_low_shelf(x: np.ndarray, sr: int, freq: float, gain_db: float) -> np.ndarray:
    if gain_db == 0.0: return x
    g = db_to_lin(gain_db)
    alpha = math.exp(-2.0 * math.pi * freq / max(sr, 1))
    y = np.empty_like(x)
    coeff_b = 1.0 - alpha
    z = np.zeros(x.shape[1], dtype=np.float64)
    for i in range(len(x)):
        z = alpha * z + coeff_b * x[i]
        y[i] = x[i] + (g - 1.0) * z
    return y

def wm_simple_compressor(x: np.ndarray, threshold_db: float, ratio: float) -> np.ndarray:
    env = np.abs(x)
    env_db = 20.0 * np.log10(np.maximum(env, 1e-12))
    over_mask = env_db > threshold_db
    gain_db = np.zeros_like(env_db)
    diff = env_db[over_mask] - threshold_db
    gain_db[over_mask] = -diff * (1.0 - 1.0/max(ratio, 1.0))
    gain_lin = np.power(10.0, gain_db / 20.0)
    return x * gain_lin

def wm_stereo_widen(x: np.ndarray, amount: float) -> np.ndarray:
    if x.shape[1] < 2: return x
    mid = 0.5 * (x[:, 0] + x[:, 1]); side = 0.5 * (x[:, 0] - x[:, 1])
    side *= (1.0 + amount)
    res = np.empty_like(x)
    res[:, 0] = mid + side; res[:, 1] = mid - side
    return res

class LibraryManager:
    DB_NAME = "aura_library.db"
    def __init__(self): self.init_db()
    def init_db(self):
        with sqlite3.connect(self.DB_NAME) as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS tracks (id INTEGER PRIMARY KEY, path TEXT UNIQUE, filename TEXT, folder TEXT)')
    def add_track(self, path):
        try:
            with sqlite3.connect(self.DB_NAME) as conn:
                conn.execute('INSERT INTO tracks (path, filename, folder) VALUES (?, ?, ?)', (path, os.path.basename(path), os.path.basename(os.path.dirname(path))))
        except sqlite3.IntegrityError: pass
    def get_folders(self, filter_text=None):
        with sqlite3.connect(self.DB_NAME) as conn:
            sql = 'SELECT DISTINCT folder FROM tracks'
            if filter_text: sql += f" WHERE filename LIKE '%{filter_text}%' OR folder LIKE '%{filter_text}%'"
            sql += ' ORDER BY folder'
            return [r[0] for r in conn.execute(sql).fetchall()]
    def get_tracks_in_folder(self, folder, filter_text=None):
        with sqlite3.connect(self.DB_NAME) as conn:
            sql = 'SELECT filename, path FROM tracks WHERE folder = ?'
            if filter_text: sql += f" AND (filename LIKE '%{filter_text}%' OR folder LIKE '%{filter_text}%')"
            sql += ' ORDER BY filename'
            return conn.execute(sql, (folder,)).fetchall()

class LibraryScanner(QObject):
    finished = pyqtSignal(int)
    def __init__(self, root_path): super().__init__(); self.root_path = root_path; self.db = LibraryManager()
    def run(self):
        count = 0
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file.lower().endswith(('.wav', '.mp3', '.flac', '.ogg', '.m4a')):
                    self.db.add_track(os.path.join(root, file))
                    count += 1
        self.finished.emit(count)

class AudioLoader(QObject):
    finished = pyqtSignal(object, int, str); error = pyqtSignal(str)
    def load(self, path):
        try:
            data, sr = read_wav(path)
            self.finished.emit(data, sr, path)
        except Exception as e: self.error.emit(str(e))

@dataclass
class PlayerEngineState:
    enabled: Dict[str, bool]
    global_intensity: float
    wet_dry: float

class PlayerEngine:
    def __init__(self): self.state = PlayerEngineState(enabled={}, global_intensity=0.72, wet_dry=0.60)
    def set_enabled(self, name, value): self.state.enabled[name] = bool(value)
    def is_enabled(self, name): return self.state.enabled.get(name, False)
    def apply_chain(self, audio, sr):
        dry = audio; y = audio.copy(); I = self.state.global_intensity
        if self.is_enabled("Gain"): y *= db_to_lin(-6.0 + 18.0 * I)
        if self.is_enabled("Bass boost"): y = wm_one_pole_low_shelf(y, sr, 120.0, 4.0 * I)
        if self.is_enabled("Compressor"): y = wm_simple_compressor(y, -12.0 - (6.0*I), 2.5 + I)
        if self.is_enabled("Peak limiter") or self.is_enabled("Limiter"): np.clip(y, -0.98, 0.98, out=y)
        if self.is_enabled("Stereo widening"): y = wm_stereo_widen(y, 0.3 * I)
        wet = self.state.wet_dry
        if wet < 1.0: y = y * wet + dry * (1.0 - wet)
        return np.clip(y, -1.0, 1.0)

class FileAudioProcessor(QObject):
    finished = pyqtSignal(object); error = pyqtSignal(str)
    def __init__(self, engine, audio, sr): super().__init__(); self.engine = engine; self.audio = audio; self.sr = sr
    def run(self):
        try:
            res = self.engine.apply_chain(self.audio, self.sr)
            self.finished.emit(res); del res; gc.collect()
        except Exception as e: self.error.emit(str(e))

class AuraOrb(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.setMinimumSize(400, 320); self.phase = 0.0; self.is_playing = False; self.pulse = 0.0
        self.timer = QTimer(self); self.timer.timeout.connect(self._animate); self.timer.start(16)
        self.cpu_load = 0.0; self.ram_load = 0.0
    def set_playing(self, playing): self.is_playing = playing
    def _animate(self):
        self.phase += 0.08 if self.is_playing else 0.02
        self.pulse = (math.sin(self.phase * 2.0) + 1.0) * (0.8 if self.is_playing else 0.5)
        self.cpu_load = 12.0 + math.sin(self.phase * 5) * 2; self.ram_load = 4.0 + math.cos(self.phase * 3)
        self.update()
    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height(); cx, cy = w/2, h/2 - 20; radius = min(w, h) * 0.25
        bg = QLinearGradient(0,0,0,h); bg.setColorAt(0, QColor(5,8,15)); bg.setColorAt(1, QColor(10,14,24)); p.fillRect(0,0,w,h,bg)
        p.setPen(QPen(QColor(40,60,90,40), 1))
        for i in range(0, w, 40): p.drawLine(i, 0, i, h)
        for i in range(0, h, 40): p.drawLine(0, i, w, i)
        glow = QRadialGradient(cx, cy, radius*2.5)
        glow.setColorAt(0, QColor(0,255,200,40) if self.is_playing else QColor(100,200,255,20))
        glow.setColorAt(0.6, Qt.GlobalColor.transparent); p.setBrush(QBrush(glow)); p.setPen(Qt.PenStyle.NoPen); p.drawEllipse(QPointF(cx, cy), radius*2.5, radius*2.0)
        
        def ring(sc, off, col, wid):
            path = QPainterPath(); r_b = radius * sc
            for i in range(101):
                a = (i/100)*6.28 + off + self.phase
                wob = (5+self.pulse*5) if self.is_playing else (5+self.pulse*2)
                r = r_b + math.sin(a*3 + self.phase*2) * wob
                x = cx + math.cos(a)*r; y = cy + math.sin(a)*r*0.85
                if i==0: path.moveTo(x,y)
                else: path.lineTo(x,y)
            p.setPen(QPen(col, wid)); p.setBrush(Qt.BrushStyle.NoBrush); p.drawPath(path)

        c1 = QColor(0,255,100,120) if self.is_playing else QColor(0,255,255,100)
        c2 = QColor(255,50,200,100) if self.is_playing else QColor(255,0,255,80)
        ring(1.2, 0, c1, 2); ring(1.1, 2.0, c2, 3); ring(0.9, 4.0, QColor(0,150,255,120), 1.5)
        
        p.setBrush(QBrush(QColor(5,10,20))); p.setPen(Qt.PenStyle.NoPen); p.drawEllipse(QPointF(cx, cy), radius, radius*0.85)
        p.setPen(QColor(200,240,255,200)); p.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold)); p.drawText(QRectF(cx-100, cy-15, 200, 30), Qt.AlignmentFlag.AlignCenter, "AURA PLAYER")
        p.setFont(QFont("Consolas", 8)); p.setPen(QColor(100,200,200,150)); p.drawText(QRectF(cx-60, cy+20, 120, 15), Qt.AlignmentFlag.AlignCenter, f"SYS: {'ACTIVE' if self.is_playing else 'IDLE'}")


# ============================================================================
# PART 4: AFTERSHOCK (SYSTEM CORE) LOGIC - OPTIMIZED
# ============================================================================

class RealtimeAudioProcessor:
    def __init__(self, sample_rate, block_size):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.preset = {"bass": 1.0, "treble": 1.0, "loudness": 1.0, "spatial": 0.0}
        self.master_volume = 1.0
        self.phase = 0.0
        self.input_level = 0.0
        self.output_level = 0.0
        
        # INCREASED STABILITY: Fixed sizing logic
        self._update_bins(block_size)

    def _update_bins(self, bs):
        self.block_size = bs
        # NO HANNING WINDOW in Realtime - causes amplitude modulation (pumping) without Overlap-Add
        self.freqs = np.fft.rfftfreq(bs, 1.0 / self.sample_rate)
        self.bass_indices = np.where(self.freqs < 280)[0]
        self.treble_indices = np.where(self.freqs > 3500)[0]

    def set_preset(self, params):
        self.preset = params.copy()

    def set_volume(self, volume):
        self.master_volume = max(0.0, min(3.0, volume))

    def process(self, indata):
        """
        Processes audio blocks. 
        Fail-safe implementation to prevent crashes on buffer mismatch.
        """
        try:
            if indata is None: return np.zeros((self.block_size, 2), dtype=np.float32)
            
            current_len = len(indata)
            
            # Dynamic Resize if driver changes buffer size
            if current_len != self.block_size:
                self._update_bins(current_len)

            # Stereo normalization
            if indata.ndim == 1: audio = np.column_stack((indata, indata))
            elif indata.shape[1] == 1: audio = np.column_stack((indata[:, 0], indata[:, 0]))
            else: audio = indata

            # Metering
            self.input_level = np.max(np.abs(audio[:200])) * 1.5
            
            bass = self.preset.get("bass", 1.0)
            treble = self.preset.get("treble", 1.0)
            loud = self.preset.get("loudness", 1.0)
            spatial = self.preset.get("spatial", 0.0)
            
            # FFT EQ (No Windowing to prevent pumping)
            if abs(bass - 1.0) > 0.01 or abs(treble - 1.0) > 0.01:
                out = np.zeros_like(audio)
                for ch in range(audio.shape[1]):
                    spec = np.fft.rfft(audio[:, ch])
                    if bass != 1.0: spec[self.bass_indices] *= bass
                    if treble != 1.0: spec[self.treble_indices] *= treble
                    out[:, ch] = np.fft.irfft(spec, n=current_len)
            else:
                out = audio.copy()

            # Global Gains
            out *= (loud * self.master_volume)

            # 8D Motion
            pan_depth = self.preset.get("pan_depth", 0.0)
            if pan_depth > 0.05:
                pan_speed = self.preset.get("pan_speed", 0.1)
                t = np.arange(len(out)) / self.sample_rate
                lfo = np.sin(self.phase + 2 * np.pi * pan_speed * t)
                self.phase = (self.phase + 2 * np.pi * pan_speed * len(out) / self.sample_rate) % (2 * np.pi)
                
                # Smooth panning
                left_gain = (1.0 - lfo * pan_depth)
                right_gain = (1.0 + lfo * pan_depth)
                out[:, 0] *= left_gain
                out[:, 1] *= right_gain

            # Spatial Width
            if abs(spatial) > 0.05:
                mid = (out[:, 0] + out[:, 1]) * 0.5
                side = (out[:, 0] - out[:, 1]) * 0.5
                side *= (1.0 + spatial)
                out[:, 0] = mid + side
                out[:, 1] = mid - side

            # Final safety clip (Soft saturation)
            np.tanh(out, out=out)
            
            self.output_level = np.max(np.abs(out[:200])) * 1.5
            return out.astype(np.float32)

        except Exception:
            # SAFETY FALLBACK: Return input audio if math fails
            # This prevents silent crashes
            return indata.astype(np.float32) if indata is not None else np.zeros((self.block_size, 2), dtype=np.float32)

# --- NEW CLASS: LAN STREAM SERVER (PREMIUM UI) ---
WEB_INTERFACE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>AURA // NEURO STREAM</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
        :root { --neon: #00ffcc; --neon-dim: rgba(0, 255, 204, 0.2); --alert: #ff3366; --bg: #05080f; --panel: rgba(10, 15, 25, 0.85); }
        * { box-sizing: border-box; user-select: none; -webkit-tap-highlight-color: transparent; }
        body { margin: 0; background: var(--bg); color: var(--neon); font-family: 'Rajdhani', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; overflow: hidden; }
        
        /* Background Grid Animation */
        .grid-bg { position: fixed; top: -50%; left: -50%; width: 200%; height: 200%; background: linear-gradient(transparent 0%, var(--bg) 80%), linear-gradient(90deg, var(--neon-dim) 1px, transparent 1px), linear-gradient(var(--neon-dim) 1px, transparent 1px); background-size: 40px 40px; transform: perspective(500px) rotateX(60deg); animation: grid-move 20s linear infinite; z-index: -2; opacity: 0.3; pointer-events: none; }
        @keyframes grid-move { 0% { transform: perspective(500px) rotateX(60deg) translateY(0); } 100% { transform: perspective(500px) rotateX(60deg) translateY(40px); } }
        
        /* Main Card */
        .card { width: 90%; max-width: 380px; background: var(--panel); border: 1px solid var(--neon-dim); border-radius: 20px; padding: 30px; box-shadow: 0 0 40px rgba(0, 255, 204, 0.1); backdrop-filter: blur(12px); display: flex; flex-direction: column; align-items: center; position: relative; overflow: hidden; }
        .card::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, var(--neon), transparent); box-shadow: 0 0 10px var(--neon); }
        
        /* Header */
        h1 { margin: 0; font-size: 32px; letter-spacing: 4px; text-shadow: 0 0 15px var(--neon); text-transform: uppercase; font-weight: 800; }
        .badge { font-size: 10px; background: var(--neon-dim); color: var(--neon); padding: 4px 8px; border-radius: 4px; margin-top: 5px; border: 1px solid var(--neon); letter-spacing: 2px; }
        .live-dot { display: inline-block; width: 8px; height: 8px; background: var(--alert); border-radius: 50%; margin-right: 5px; box-shadow: 0 0 5px var(--alert); animation: blink 1s infinite; display: none; }
        .is-live .live-dot { display: inline-block; }
        .is-live .badge { border-color: var(--alert); color: var(--alert); background: rgba(255, 51, 102, 0.1); }
        @keyframes blink { 50% { opacity: 0.3; } }

        /* Visualizer */
        .viz-container { width: 100%; height: 100px; background: rgba(0,0,0,0.5); border-radius: 12px; margin: 30px 0; border: 1px solid var(--neon-dim); position: relative; overflow: hidden; }
        canvas { width: 100%; height: 100%; display: block; }
        
        /* Controls */
        .controls { display: flex; gap: 20px; width: 100%; justify-content: center; align-items: center; margin-bottom: 20px; }
        .btn-main { width: 80px; height: 80px; border-radius: 50%; border: 2px solid var(--neon); background: rgba(0, 255, 204, 0.1); color: var(--neon); font-size: 30px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 20px rgba(0, 255, 204, 0.1); position: relative; }
        .btn-main::before { content: ''; position: absolute; inset: -5px; border-radius: 50%; border: 2px dashed var(--neon-dim); animation: spin 10s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .btn-main:hover { background: var(--neon); color: #000; box-shadow: 0 0 40px var(--neon); transform: scale(1.05); }
        .btn-main:active { transform: scale(0.95); }
        
        .play-icon { display: block; width: 0; height: 0; border-style: solid; border-width: 15px 0 15px 25px; border-color: transparent transparent transparent currentColor; margin-left: 5px; }
        .pause-icon { display: none; width: 20px; height: 25px; border-left: 6px solid currentColor; border-right: 6px solid currentColor; }
        .playing .play-icon { display: none; }
        .playing .pause-icon { display: block; }
        .playing .btn-main { border-color: var(--alert); color: var(--alert); box-shadow: 0 0 20px var(--alert); background: rgba(255, 51, 102, 0.1); }
        .playing .btn-main:hover { background: var(--alert); color: #000; }
        .playing .btn-main::before { border-color: rgba(255, 51, 102, 0.3); }

        /* Volume */
        .vol-wrap { width: 100%; display: flex; align-items: center; gap: 15px; color: var(--neon-dim); font-size: 14px; }
        input[type=range] { flex: 1; -webkit-appearance: none; background: transparent; height: 4px; border-radius: 2px; background: var(--neon-dim); outline: none; }
        input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; border-radius: 50%; background: var(--neon); cursor: pointer; box-shadow: 0 0 10px var(--neon); transition: 0.2s; margin-top: -6px; }
        input[type=range]::-webkit-slider-runnable-track { height: 4px; border-radius: 2px; }
        input[type=range]:hover::-webkit-slider-thumb { transform: scale(1.2); }

        /* Footer */
        .status-text { margin-top: 20px; font-size: 12px; color: #668899; letter-spacing: 1px; }
        .connection-bar { position: absolute; bottom: 0; left: 0; height: 4px; background: var(--neon); width: 0%; transition: width 0.5s; box-shadow: 0 0 10px var(--neon); }
        .playing .connection-bar { width: 100%; background: var(--alert); box-shadow: 0 0 15px var(--alert); }

        /* Loader */
        .loader { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 10px; color: var(--neon); letter-spacing: 2px; animation: flash 1s infinite; display: none; pointer-events: none; }
        @keyframes flash { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        .loading .loader { display: block; }
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="card" id="card">
        <h1>AURA</h1>
        <div class="badge" id="badge"><span class="live-dot"></span><span id="status-label">SYSTEM OFFLINE</span></div>
        
        <div class="viz-container">
            <canvas id="c"></canvas>
            <div class="loader">ESTABLISHING UPLINK...</div>
        </div>

        <div class="controls">
            <div class="btn-main" id="playBtn" onclick="togglePlay()">
                <div class="play-icon"></div>
                <div class="pause-icon"></div>
            </div>
        </div>

        <div class="vol-wrap">
            <span>VOL</span>
            <input type="range" id="vol" min="0" max="1" step="0.01" value="1" oninput="setVolume(this.value)">
        </div>

        <div class="status-text" id="log">WAITING FOR INPUT</div>
        <div class="connection-bar" id="bar"></div>
    </div>

    <script>
        const audio = new Audio();
        audio.crossOrigin = "anonymous";
        // Prevent audio caching
        audio.preload = "none";

        let ctx, analyser, source, gainNode;
        let isPlaying = false;
        let animationId;
        const canvas = document.getElementById('c');
        const c = canvas.getContext('2d');
        const card = document.getElementById('card');
        const badge = document.getElementById('badge');
        const statusLabel = document.getElementById('status-label');
        const log = document.getElementById('log');

        function resize() {
            const rect = canvas.getBoundingClientRect();
            canvas.width = rect.width * (window.devicePixelRatio || 1);
            canvas.height = rect.height * (window.devicePixelRatio || 1);
            c.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
        }
        window.addEventListener('resize', resize);
        resize();

        function initAudio() {
            if (!ctx) {
                ctx = new (window.AudioContext || window.webkitAudioContext)();
                analyser = ctx.createAnalyser();
                analyser.fftSize = 128; // Lower FFT size for snappier mobile viz
                analyser.smoothingTimeConstant = 0.85;
                
                source = ctx.createMediaElementSource(audio);
                gainNode = ctx.createGain();
                
                source.connect(gainNode);
                gainNode.connect(analyser);
                analyser.connect(ctx.destination);
                
                setVolume(document.getElementById('vol').value);
            }
            if (ctx.state === 'suspended') ctx.resume();
        }

        async function togglePlay() {
            if (isPlaying) {
                // STOP
                audio.pause();
                audio.src = ""; // Cut connection
                audio.load();   // Reset buffer
                isPlaying = false;
                updateUI(false);
                log.innerText = "LINK TERMINATED";
                cancelAnimationFrame(animationId);
                c.clearRect(0,0,canvas.width,canvas.height);
            } else {
                // PLAY
                card.classList.add('loading');
                log.innerText = "INITIALIZING STREAM...";
                initAudio();
                
                // Bust cache with timestamp
                audio.src = "/stream?t=" + Date.now();
                
                try {
                    await audio.play();
                    isPlaying = true;
                    updateUI(true);
                    log.innerText = "RECEIVING NEURO STREAM";
                    renderFrame();
                } catch (err) {
                    console.error(err);
                    log.innerText = "CONNECTION FAILED";
                    card.classList.remove('loading');
                }
            }
        }

        function updateUI(active) {
            if (active) {
                card.classList.remove('loading');
                card.classList.add('playing');
                card.classList.add('is-live');
                statusLabel.innerText = "LIVE BROADCAST";
            } else {
                card.classList.remove('playing');
                card.classList.remove('is-live');
                card.classList.remove('loading');
                statusLabel.innerText = "SYSTEM OFFLINE";
            }
        }

        function setVolume(v) {
            if (gainNode) gainNode.gain.value = v;
        }

        function renderFrame() {
            if (!isPlaying) return;
            animationId = requestAnimationFrame(renderFrame);
            
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            analyser.getByteFrequencyData(dataArray);

            const w = canvas.width / (window.devicePixelRatio || 1);
            const h = canvas.height / (window.devicePixelRatio || 1);
            
            c.clearRect(0, 0, w, h);

            const barWidth = (w / bufferLength) * 2.5;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                const barHeight = (dataArray[i] / 255) * h;
                
                // Color based on height (Green/Teal to Pink/Red)
                const hue = 160 - (dataArray[i] / 255 * 60); // 160 is teal
                c.fillStyle = `hsl(${hue}, 100%, 50%)`;
                
                // Rounded tops
                c.fillRect(x, h - barHeight, barWidth, barHeight);
                
                x += barWidth + 1;
            }
        }
        
        // Auto-reconnect play handler for mobile waking
        audio.onstalled = () => { if(isPlaying) log.innerText = "BUFFERING..."; };
        audio.onplaying = () => { if(isPlaying) { log.innerText = "SIGNAL STABLE"; card.classList.remove('loading'); }};
    </script>
</body>
</html>"""

class StreamBroadcaster(QThread):
    port_found_signal = pyqtSignal(str) # Signal to update UI with real port

    def __init__(self, start_port=5050):
        super().__init__()
        self.start_port = start_port
        self.actual_port = start_port
        self.running = False
        self.clients = []
        self.socket = None
        self.data_queue = []
        self.header_sent = False
        self.sample_rate = 44100
        # New safe queue for pending clients added by threads
        self.new_stream_clients = queue.Queue()

    def run(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # AUTO PORT FINDER
        bound = False
        for p in range(self.start_port, self.start_port + 10):
            try:
                self.socket.bind(('0.0.0.0', p))
                self.actual_port = p
                bound = True
                break
            except OSError:
                continue
        
        if not bound:
            print("ERROR: No ports available 5050-5060")
            return

        self.socket.listen(5)
        self.socket.settimeout(0.05)
        
        # Notify UI of the actual port used
        ip = self.get_ip()
        self.port_found_signal.emit(f"LIVE: http://{ip}:{self.actual_port}")

        while self.running:
            # 1. Accept connections (Multi-threaded handshake)
            try:
                client, addr = self.socket.accept()
                # Spawn a thread so handshake doesn't block audio loop
                t = threading.Thread(target=self._client_handshake, args=(client,))
                t.daemon = True
                t.start()
            except socket.timeout:
                pass
            except Exception:
                pass

            # 2. Add verified clients to broadcast list
            while not self.new_stream_clients.empty():
                try:
                    self.clients.append(self.new_stream_clients.get_nowait())
                except queue.Empty:
                    break

            # 3. Broadcast Audio
            if self.data_queue:
                chunk = self.data_queue.pop(0)
                dead_clients = []
                for client in self.clients:
                    try:
                        # KEY FIX: Blocking send with small timeout guarantees delivery
                        # or cleanly drops client. No half-sent chunks.
                        client.settimeout(0.2)
                        client.sendall(chunk) 
                    except (OSError, socket.timeout, BrokenPipeError):
                        dead_clients.append(client)
                
                for c in dead_clients:
                    if c in self.clients: self.clients.remove(c)
                    try: c.close()
                    except: pass
            else:
                self.msleep(5)

        if self.socket: self.socket.close()
        for c in self.clients: 
            try: c.close()
            except: pass

    def _client_handshake(self, client):
        """Runs in background thread to parse request safely."""
        try:
            client.settimeout(3.0) # Give 3s to send header
            req = client.recv(1024).decode('utf-8', errors='ignore')
            
            if "GET /stream" in req:
                self._send_header(client)
                # KEY FIX: Do NOT set non-blocking. Keep blocking to ensure data integrity.
                # The main loop handles timeouts.
                self.new_stream_clients.put(client)
            else:
                self._handle_web_request(client)
        except:
            try: client.close()
            except: pass

    def stop(self):
        self.running = False
        self.wait()

    def add_audio(self, audio_data):
        if not self.running: return
        pcm = (audio_data * 32767).astype(np.int16)
        self.data_queue.append(pcm.tobytes())
        if len(self.data_queue) > 3: self.data_queue.pop(0)

    def _handle_web_request(self, client):
        try:
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
            client.send(header.encode('utf-8'))
            client.send(WEB_INTERFACE.encode('utf-8'))
        except: pass
        finally:
            try: client.close()
            except: pass

    def _send_header(self, client):
        # Optimized header for live streaming
        http_header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: audio/wav\r\n"
            "Connection: keep-alive\r\n"
            "Cache-Control: no-cache, no-store\r\n"
            "Accept-Ranges: none\r\n\r\n"
        ).encode('utf-8')
        
        byte_rate = self.sample_rate * 2 * 2
        header = struct.pack('<4sI4s4sIHHIIHH4sI', 
            b'RIFF', 0xFFFFFFFF, b'WAVE', b'fmt ', 16, 1, 2, 
            self.sample_rate, byte_rate, 4, 16, b'data', 0xFFFFFFFF
        )
        try:
            client.send(http_header) 
            client.send(header)
        except: pass

    def get_ip(self):
        # Robust Offline IP Detection (Does not require internet)
        try:
            # 1. Try connecting to a local subnet address (router/gateway usually)
            # This doesn't actually send packets, just checks routing table
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("192.168.1.1", 1)) 
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            try:
                # 2. Fallback to standard hostname resolution
                return socket.gethostbyname(socket.gethostname())
            except:
                return "127.0.0.1"


class SystemAudioThread(QThread):
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, processor, input_idx, output_idx, sample_rate, buffer_mode):
        super().__init__()
        self.processor = processor
        self.input_idx = input_idx
        self.output_idx = output_idx
        self.sample_rate = sample_rate
        self.buffer_mode = buffer_mode
        self.running = False
        self.broadcaster = None  # Link to streamer

    def run(self):
        if not AUDIO_AVAILABLE: return
        self.running = True
        
        # ENHANCED SIZES: 
        # Stable uses 8192 (safest large buffer). 16k is too prone to timeouts.
        # Fast uses 4096.
        bs = 8192 if self.buffer_mode == "stable" else 4096
        lat = 'high'
        
        self.processor._update_bins(bs)

        try:
            with sd.Stream(
                device=(self.input_idx, self.output_idx),
                samplerate=self.sample_rate,
                blocksize=bs,
                dtype=np.float32,
                channels=2,
                latency=lat,
                callback=self.audio_callback
            ):
                self.status_signal.emit(f"ONLINE | {bs} BLOCKS")
                while self.running:
                    self.msleep(100)
        except Exception as e:
            self.error_signal.emit(str(e))
        
        self.status_signal.emit("OFFLINE")

    def audio_callback(self, indata, outdata, frames, time_info, status):
        if status:
            outdata.fill(0)
            return
        result = self.processor.process(indata)
        
        # LINK: Send processed audio to LAN Streamer if active
        if self.broadcaster and self.broadcaster.running:
            self.broadcaster.add_audio(result)

        # Ensure result fits in outdata
        n = min(len(result), len(outdata))
        outdata[:n] = result[:n]
        if n < len(outdata):
            outdata[n:] = 0

    def stop(self):
        self.running = False
        self.wait(1000)

class SciFiReactor(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(300, 300)
        self.audio_level = 0.0
        self.angle_1 = 0
        self.angle_2 = 180
        self.angle_3 = 90
        # Animation loop
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16) # ~60 FPS

    def set_level(self, level):
        # Smooth attack, fast decay
        target = level
        if target > self.audio_level:
            self.audio_level = self.audio_level * 0.7 + target * 0.3
        else:
            self.audio_level = self.audio_level * 0.9 + target * 0.1

    def animate(self):
        # Rotation speed based on audio intensity
        speed = 2 + (self.audio_level * 15)
        self.angle_1 = (self.angle_1 + speed) % 360
        self.angle_2 = (self.angle_2 - (speed * 0.7)) % 360
        self.angle_3 = (self.angle_3 + (speed * 0.3)) % 360
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        center = QPointF(w/2, h/2)
        base_size = min(w, h) * 0.35
        
        # Audio reactive pulse size
        pulse = base_size * (1 + (self.audio_level * 0.5))
        
        # 1. Background Glow
        grad = QRadialGradient(center, base_size * 2)
        grad.setColorAt(0, QColor(0, 255, 200, 40))
        grad.setColorAt(1, QColor(0, 0, 0, 0))
        p.fillRect(self.rect(), Qt.BrushStyle.NoBrush) # Clear
        p.setBrush(grad)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(center, base_size*2, base_size*2)

        # 2. Outer Rotating Ring (Tech HUD style)
        pen = QPen(QColor("#00ffcc"))
        pen.setWidth(3)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        
        rect_outer = QRectF(center.x() - pulse, center.y() - pulse, pulse*2, pulse*2)
        p.drawArc(rect_outer, int(self.angle_1 * 16), 100 * 16)
        p.drawArc(rect_outer, int((self.angle_1 + 180) * 16), 100 * 16)
        
        # 3. Inner Rotating Ring
        pen.setColor(QColor("#ff00cc"))
        pen.setWidth(2)
        p.setPen(pen)
        pulse_inner = pulse * 0.8
        rect_inner = QRectF(center.x() - pulse_inner, center.y() - pulse_inner, pulse_inner*2, pulse_inner*2)
        p.drawArc(rect_inner, int(self.angle_2 * 16), 240 * 16)
        
        # 4. Center Core
        core_rad = pulse * 0.5
        core_grad = QRadialGradient(center, core_rad)
        if self.audio_level > 0.5:
            core_grad.setColorAt(0, QColor("#ffaa00")) # Warning orange/red
            core_grad.setColorAt(1, QColor("#550000"))
        else:
            core_grad.setColorAt(0, QColor("#ffffff"))
            core_grad.setColorAt(0.3, QColor("#00ccff"))
            core_grad.setColorAt(1, QColor("#002233"))
            
        p.setBrush(core_grad)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(center, core_rad, core_rad)
        
        # 5. Triangle Spin
        p.save()
        p.translate(center)
        p.rotate(self.angle_3)
        poly = QPolygonF([QPointF(0, -core_rad*0.6), QPointF(core_rad*0.5, core_rad*0.3), QPointF(-core_rad*0.5, core_rad*0.3)])
        p.setBrush(QColor(255, 255, 255, 100))
        p.drawPolygon(poly)
        p.restore()


# ============================================================================
# PART 5: UI WIDGETS
# ============================================================================

class ModernButton(QPushButton):
    def __init__(self, text, is_primary=False):
        super().__init__(text)
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_primary = is_primary
        self.set_style()

    def set_style(self):
        if self.is_primary:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #009977, stop:1 #00cc88);
                    color: white; border: none; border-radius: 5px; font-weight: bold; font-size: 13px;
                }
                QPushButton:hover { background: #00ffaa; }
                QPushButton:pressed { background: #007755; }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: #2a2a3a; color: #ccc; border: 1px solid #444;
                    border-radius: 5px; font-size: 12px;
                }
                QPushButton:hover { border: 1px solid #00ffcc; color: white; background: #333; }
                QPushButton:checked { background: #00ffcc; color: black; border: none; font-weight: bold;}
            """)

# --- TAB 1: AURA PLAYER WIDGET ---
class PlayerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = PlayerEngine()
        self.db = LibraryManager()
        self.setAcceptDrops(True)

        # Audio setup
        self.player_a = QMediaPlayer(); self.out_a = QAudioOutput(); self.player_a.setAudioOutput(self.out_a)
        self.player_b = QMediaPlayer(); self.out_b = QAudioOutput(); self.player_b.setAudioOutput(self.out_b)
        self.active_player = 0
        self.master_volume = 1.0

        for p in [self.player_a, self.player_b]:
            p.mediaStatusChanged.connect(self._on_media_status_changed)
            p.playbackStateChanged.connect(self._on_playback_state_changed)
            p.positionChanged.connect(self._on_pos_changed)
            p.durationChanged.connect(self._on_dur_changed)

        self.cross_timer = QTimer(self); self.cross_timer.setInterval(100); self.cross_timer.timeout.connect(self._crossfade_step)
        self.is_crossfading = False
        self.xfade_duration = 4000
        self.monitor_timer = QTimer(self); self.monitor_timer.setInterval(500); self.monitor_timer.timeout.connect(self._check_xfade_trigger)
        self.monitor_timer.start()

        self.is_slider_dragging = False; self.current_playlist = []; self.current_index = -1; self.audio_data = None; self.effect_items = {}
        self.shuffle_state = False; self.loop_state = 1

        self._init_ui()

    @property
    def current_player(self): return self.player_a if self.active_player == 0 else self.player_b
    @property
    def next_player(self): return self.player_b if self.active_player == 0 else self.player_a
    @property
    def current_out(self): return self.out_a if self.active_player == 0 else self.out_b
    @property
    def next_out(self): return self.out_b if self.active_player == 0 else self.out_a

    def _init_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)
        
        # TOP BAR
        top_bar = QFrame(); top_bar.setFixedHeight(70); top_bar.setStyleSheet("background: rgba(10, 15, 25, 0.9); border-bottom: 1px solid #223344;")
        tb_lay = QHBoxLayout(top_bar)
        
        self.btn_prev = QPushButton("|◀"); self.btn_prev.setFixedWidth(40); self.btn_prev.clicked.connect(self._play_prev)
        self.btn_play = QPushButton("▶"); self.btn_play.setFixedWidth(50); self.btn_play.clicked.connect(self._toggle_playback)
        self.btn_play.setStyleSheet("font-size: 20px; font-weight: bold; color: #88ffaa;")
        self.btn_next = QPushButton("▶|"); self.btn_next.setFixedWidth(40); self.btn_next.clicked.connect(self._play_next)
        self.btn_stop = QPushButton("⏹"); self.btn_stop.setFixedWidth(40); self.btn_stop.clicked.connect(self._stop_playback)
        self.btn_shuffle = QPushButton("🔀"); self.btn_shuffle.setFixedWidth(40); self.btn_shuffle.clicked.connect(self._toggle_shuffle)
        self.btn_loop = QPushButton("🔁"); self.btn_loop.setFixedWidth(40); self.btn_loop.clicked.connect(self._toggle_loop); self.btn_loop.setStyleSheet("color: #00ffaa;")
        
        seek_l = QVBoxLayout(); seek_l.setSpacing(2)
        self.seek = QSlider(Qt.Orientation.Horizontal); self.seek.setRange(0,0)
        self.seek.sliderPressed.connect(self._seek_press); self.seek.sliderReleased.connect(self._seek_release); self.seek.sliderMoved.connect(self._seek_move)
        self.time_lbl = QLabel("00:00 / 00:00"); self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); self.time_lbl.setStyleSheet("color: #6688aa; font-family: Consolas;")
        seek_l.addWidget(self.seek); seek_l.addWidget(self.time_lbl)
        
        vol_box = QHBoxLayout(); vol_box.setSpacing(4)
        v_lbl = QLabel("🔊"); v_lbl.setStyleSheet("color: #6688aa; font-size: 14px;")
        self.vol_slider = QSlider(Qt.Orientation.Horizontal); self.vol_slider.setRange(0, 100); self.vol_slider.setValue(100); self.vol_slider.setFixedWidth(80)
        self.vol_slider.valueChanged.connect(self._set_master_vol)
        vol_box.addWidget(v_lbl); vol_box.addWidget(self.vol_slider)
        
        tb_lay.addWidget(self.btn_shuffle); tb_lay.addWidget(self.btn_prev); tb_lay.addWidget(self.btn_play); tb_lay.addWidget(self.btn_next); tb_lay.addWidget(self.btn_loop); tb_lay.addWidget(self.btn_stop)
        tb_lay.addSpacing(20); tb_lay.addLayout(seek_l, 1); tb_lay.addSpacing(15); tb_lay.addLayout(vol_box); tb_lay.addSpacing(10)
        layout.addWidget(top_bar)

        # CONTENT
        content = QHBoxLayout(); content.setContentsMargins(20,20,20,20); content.setSpacing(20)
        
        # LEFT PANEL
        left = QFrame(); left.setObjectName("Panel"); left.setFixedWidth(300); lp = QVBoxLayout(left)
        preset_grp = QGroupBox("Smart Presets"); pg_lay = QVBoxLayout(preset_grp)
        self.combo = QComboBox(); self.combo.addItems(PLAYER_PRESETS.keys()); self.combo.currentTextChanged.connect(self._on_preset_changed)
        pg_lay.addWidget(self.combo); lp.addWidget(preset_grp)
        
        dial_grp = QGroupBox("Intensity"); dg_lay = QVBoxLayout(dial_grp)
        self.dial = QDial(); self.dial.setRange(0,100); self.dial.setValue(72); self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(lambda v: self._set_param('global_intensity', v/100)); dg_lay.addWidget(self.dial); lp.addWidget(dial_grp)
        
        mix_grp = QGroupBox("Mix"); mg_lay = QVBoxLayout(mix_grp)
        self.mix = QSlider(Qt.Orientation.Horizontal); self.mix.setRange(0,100); self.mix.setValue(60)
        self.mix.valueChanged.connect(lambda v: self._set_param('wet_dry', v/100)); mg_lay.addWidget(self.mix); lp.addWidget(mix_grp)
        lp.addStretch(); content.addWidget(left)
        
        # CENTER ORB
        center_l = QVBoxLayout(); self.orb = AuraOrb(); center_l.addWidget(self.orb)
        io_panel = QFrame(); io_panel.setObjectName("Panel"); io_panel.setFixedHeight(120); io_lay = QVBoxLayout(io_panel)
        row = QHBoxLayout(); self.path_txt = QLineEdit(); self.path_txt.setReadOnly(True); self.path_txt.setPlaceholderText("Current Track...")
        load_b = QPushButton("Process WAV"); load_b.clicked.connect(self._load_process)
        exp_b = QPushButton("RENDER EXPORT"); exp_b.setObjectName("Primary"); exp_b.clicked.connect(self._export)
        row.addWidget(self.path_txt); row.addWidget(load_b); row.addWidget(exp_b)
        self.prog = QProgressBar(); self.prog.setTextVisible(False); self.prog.setStyleSheet("QProgressBar{height:4px;border:none;background:#222}QProgressBar::chunk{background:#00ffff}")
        io_lay.addLayout(row); io_lay.addWidget(self.prog); center_l.addWidget(io_panel); content.addLayout(center_l, 2)
        
        # RIGHT PANEL
        right = QFrame(); right.setObjectName("Panel"); right.setFixedWidth(300); rp = QVBoxLayout(right)
        self.tabs = QTabWidget()
        tab1 = QWidget(); t1 = QVBoxLayout(tab1); self.tree = QTreeWidget(); self.tree.setHeaderHidden(True); self.tree.itemChanged.connect(self._toggle_fx)
        t1.addWidget(self.tree); self._populate_tree(); self.tabs.addTab(tab1, "FX")
        
        tab2 = QWidget(); t2 = QVBoxLayout(tab2)
        self.lib_search = QLineEdit(); self.lib_search.setPlaceholderText("Search..."); self.lib_search.textChanged.connect(self._refresh_lib)
        self.lib_tree = QTreeWidget(); self.lib_tree.setHeaderLabel("Library"); self.lib_tree.itemDoubleClicked.connect(self._lib_dbl_click)
        row2 = QHBoxLayout(); scan_b = QPushButton("Add Folder"); scan_b.clicked.connect(self._scan); ref_b = QPushButton("Refresh"); ref_b.clicked.connect(lambda: self._refresh_lib(""))
        row2.addWidget(scan_b); row2.addWidget(ref_b); t2.addWidget(self.lib_search); t2.addWidget(self.lib_tree); t2.addLayout(row2)
        self.tabs.addTab(tab2, "Lib")
        rp.addWidget(self.tabs); content.addWidget(right); layout.addLayout(content)
        self._refresh_lib()

    # --- Logic ---
    def dragEnterEvent(self, e): e.accept() if e.mimeData().hasUrls() else e.ignore()
    def dropEvent(self, e):
        files = [u.toLocalFile() for u in e.mimeData().urls()]
        valid = [f for f in files if f.lower().endswith(('.wav', '.mp3', '.flac', '.ogg', '.m4a'))]
        if valid:
            self.current_playlist = valid; self.current_index = 0; self._play_current()
            if len(valid) == 1 and valid[0].lower().endswith(".wav"):
                self.ld = AudioLoader(); self.th = QThread(); self.ld.moveToThread(self.th)
                self.th.started.connect(lambda: self.ld.load(valid[0])); self.ld.finished.connect(self._loaded); self.th.start()
    
    def _toggle_shuffle(self): self.shuffle_state = not self.shuffle_state; self.btn_shuffle.setStyleSheet("color: #00ffaa;" if self.shuffle_state else "color: #666;")
    def _toggle_loop(self):
        self.loop_state = (self.loop_state + 1) % 3
        if self.loop_state == 0: self.btn_loop.setText("🔁"); self.btn_loop.setStyleSheet("color: #666;")
        elif self.loop_state == 1: self.btn_loop.setText("🔁"); self.btn_loop.setStyleSheet("color: #00ffaa;")
        else: self.btn_loop.setText("🔂"); self.btn_loop.setStyleSheet("color: #ffaa00;")

    def _set_master_vol(self, val):
        self.master_volume = val / 100.0
        if not self.is_crossfading: self.out_a.setVolume(self.master_volume); self.out_b.setVolume(self.master_volume)

    def _populate_tree(self):
        self.tree.blockSignals(True)
        for cat, sub in PLAYER_FEATURES.items():
            p = QTreeWidgetItem(self.tree, [cat]); p.setFlags(Qt.ItemFlag.ItemIsEnabled)
            for s, items in sub.items():
                g = QTreeWidgetItem(p, [s]); g.setFlags(Qt.ItemFlag.ItemIsEnabled)
                for i in items:
                    it = QTreeWidgetItem(g, [i]); it.setCheckState(0, Qt.CheckState.Unchecked); it.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                    self.effect_items[i] = it
        self.tree.expandToDepth(1); self.tree.blockSignals(False)

    def _on_preset_changed(self, name):
        if name not in PLAYER_PRESETS: return
        p = PLAYER_PRESETS[name]
        self.dial.blockSignals(True); self.dial.setValue(int(p["i"]*100)); self.dial.blockSignals(False)
        self.mix.blockSignals(True); self.mix.setValue(int(p["w"]*100)); self.mix.blockSignals(False)
        self.engine.state.global_intensity = p["i"]; self.engine.state.wet_dry = p["w"]
        self.tree.blockSignals(True)
        for it in self.effect_items.values(): it.setCheckState(0, Qt.CheckState.Unchecked)
        self.engine.state.enabled.clear()
        for fx in p["fx"]:
            if fx in self.effect_items: self.effect_items[fx].setCheckState(0, Qt.CheckState.Checked); self.engine.set_enabled(fx, True)
        self.tree.blockSignals(False)

    def _toggle_fx(self, item, col):
        if item.childCount() == 0: 
            self.engine.set_enabled(item.text(0), item.checkState(0) == Qt.CheckState.Checked)
            self._save_custom()
            self.combo.blockSignals(True); self.combo.setCurrentIndex(0); self.combo.blockSignals(False)

    def _set_param(self, k, v): setattr(self.engine.state, k, v); self._save_custom(); self.combo.blockSignals(True); self.combo.setCurrentIndex(0); self.combo.blockSignals(False)
    def _save_custom(self): PLAYER_PRESETS["--- Custom / Modified ---"] = {"i": self.engine.state.global_intensity, "w": self.engine.state.wet_dry, "fx": [k for k, v in self.engine.state.enabled.items() if v]}

    def _scan(self):
        d = QFileDialog.getExistingDirectory(self, "Music Folder"); 
        if not d: return
        self.sc = LibraryScanner(d); self.th = QThread(); self.sc.moveToThread(self.th)
        self.th.started.connect(self.sc.run); self.sc.finished.connect(lambda: (self._refresh_lib(), self.th.quit())); self.th.start()

    def _refresh_lib(self, txt=None):
        if txt is None and isinstance(self.sender(), QLineEdit): txt = self.sender().text()
        self.lib_tree.clear()
        for f in self.db.get_folders(txt):
            fi = QTreeWidgetItem(self.lib_tree, [f]); fi.setFlags(Qt.ItemFlag.ItemIsEnabled)
            for n, p in self.db.get_tracks_in_folder(f, txt): QTreeWidgetItem(fi, [n]).setData(0, Qt.ItemDataRole.UserRole, p)
        self.lib_tree.expandAll() if txt else self.lib_tree.expandToDepth(0)

    def _lib_dbl_click(self, item):
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path:
            parent = item.parent()
            self.current_playlist = [parent.child(i).data(0, Qt.ItemDataRole.UserRole) for i in range(parent.childCount())]
            self.current_index = self.current_playlist.index(path)
            self._play_current()

    def _play_current(self):
        if not (0 <= self.current_index < len(self.current_playlist)): return
        target_path = self.current_playlist[self.current_index]
        if self.current_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState and not self.is_crossfading:
            self.next_out.setVolume(0.0); self.next_player.setSource(QUrl.fromLocalFile(target_path)); self.next_player.play()
            self.is_crossfading = True; self.xfade_start_time = time.time(); self.cross_timer.start(); self.path_txt.setText(f"Mixing: {os.path.basename(target_path)}")
            return
        self.is_crossfading = False; self.cross_timer.stop(); self.player_a.stop(); self.player_b.stop()
        self.out_a.setVolume(self.master_volume); self.out_b.setVolume(self.master_volume); self.active_player = 0 
        self.current_player.setSource(QUrl.fromLocalFile(target_path)); self.current_player.play(); self.path_txt.setText(f"Playing: {os.path.basename(target_path)}")

    def _get_next_index(self, advance=True):
        if not self.current_playlist: return -1
        N = len(self.current_playlist)
        if self.shuffle_state: return random.randint(0, N - 1)
        if not advance: idx = self.current_index - 1; return (N - 1 if self.loop_state == 1 else 0) if idx < 0 else idx
        idx = self.current_index + 1
        return (0 if self.loop_state == 1 else -1) if idx >= N else idx

    def _check_xfade_trigger(self):
        if not self.engine.is_enabled("Crossfade"): return
        if self.current_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState or self.is_crossfading: return
        dur = self.current_player.duration(); pos = self.current_player.position()
        if dur > 5000 and (dur - pos) < self.xfade_duration:
            next_idx = self.current_index if self.loop_state == 2 else self._get_next_index(True)
            if next_idx != -1: self.current_index = next_idx; self._play_current()

    def _crossfade_step(self):
        now = time.time(); elapsed = (now - self.xfade_start_time) * 1000
        progress = elapsed / self.xfade_duration
        if progress >= 1.0:
            self.cross_timer.stop(); self.is_crossfading = False; self.current_player.stop(); self.active_player = 1 - self.active_player
            self.current_out.setVolume(self.master_volume); self.next_out.setVolume(self.master_volume)
        else:
            self.current_out.setVolume((1.0 - progress) * self.master_volume); self.next_out.setVolume(progress * self.master_volume)

    def _play_next(self): idx = self._get_next_index(True); self.current_index = idx; self._play_current() if idx != -1 else self._stop_playback()
    def _play_prev(self): idx = self._get_next_index(False); self.current_index = idx; self._play_current() if idx != -1 else None
    def _toggle_playback(self):
        if self.current_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState: self.current_player.pause(); self.next_player.pause()
        elif self.current_player.source().isEmpty(): QMessageBox.info(self, "Empty", "Select track.")
        else: self.current_player.play()
    def _stop_playback(self): self.player_a.stop(); self.player_b.stop(); self.orb.set_playing(False)
    def _on_media_status_changed(self, s): 
        if s == QMediaPlayer.MediaStatus.EndOfMedia and not self.is_crossfading: self.current_player.play() if self.loop_state == 2 else self._play_next()
    def _on_playback_state_changed(self, s): self.orb.set_playing(s == QMediaPlayer.PlaybackState.PlayingState); self.btn_play.setText("⏸" if s == QMediaPlayer.PlaybackState.PlayingState else "▶")
    
    def _seek_press(self): self.is_slider_dragging = True
    def _seek_release(self): self.current_player.setPosition(self.seek.value()); self.is_slider_dragging = False
    def _seek_move(self, v): self._upd_time(v, self.current_player.duration())
    def _on_pos_changed(self, p): 
        if not self.is_slider_dragging: self.seek.setValue(p)
        self._upd_time(p, self.current_player.duration())
    def _on_dur_changed(self, d): self.seek.setRange(0, d)
    def _upd_time(self, c, t): self.time_lbl.setText(f"{c//60000}:{(c//1000)%60:02} / {t//60000}:{(t//1000)%60:02}")

    def _load_process(self):
        p, _ = QFileDialog.getOpenFileName(self, "Open WAV", "", "WAV (*.wav)"); 
        if not p: return
        self.ld = AudioLoader(); self.th = QThread(); self.ld.moveToThread(self.th)
        self.th.started.connect(lambda: self.ld.load(p)); self.ld.finished.connect(self._loaded); self.th.start()
    def _loaded(self, d, sr, p): self.audio_data = d; self.sample_rate = sr; self.orb.ram_load = d.nbytes/(1024*1024); self.th.quit(); self.prog.setValue(100)
    def _export(self):
        if self.audio_data is None: return
        p, _ = QFileDialog.getSaveFileName(self, "Save", "", "WAV (*.wav)"); 
        if not p: return
        self.pr = FileAudioProcessor(self.engine, self.audio_data, self.sample_rate); self.th = QThread(); self.pr.moveToThread(self.th)
        self.th.started.connect(self.pr.run); self.pr.finished.connect(lambda r: (write_wav(p, r, self.sample_rate), self.th.quit(), QMessageBox.information(self, "Done", "Saved!"))); self.th.start()


# --- TAB 2: SYSTEM CORE WIDGET ---
class SystemCoreWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.processor = None
        self.thread = None
        self.broadcaster = None
        self.device_pairs = []
        self.active_preset_btn = None
        self.init_ui()
        self.scan_devices()
        self.sync_timer = QTimer(); self.sync_timer.timeout.connect(self.sync_ui); self.sync_timer.start(30)

    def init_ui(self):
        main_layout = QHBoxLayout(self); main_layout.setContentsMargins(20, 20, 20, 20); main_layout.setSpacing(20)
        
        # LEFT COLUMN
        left_panel = QFrame(); left_panel.setFixedWidth(300); left_panel.setStyleSheet("background: #111625; border-radius: 15px; border: 1px solid #223344;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("INPUT / OUTPUT CHAIN"))
        self.combo_dev = QComboBox(); left_layout.addWidget(self.combo_dev)
        btn_refresh = ModernButton("Scan Devices"); btn_refresh.clicked.connect(self.scan_devices); left_layout.addWidget(btn_refresh)
        
        g_mode = QGroupBox("Latency Mode"); v_mode = QVBoxLayout(g_mode)
        self.btn_stable = QRadioButton("ULTRA STABLE (No Jitter)"); self.btn_fast = QRadioButton("FAST (Low Latency)"); self.btn_stable.setChecked(True)
        v_mode.addWidget(self.btn_stable); v_mode.addWidget(self.btn_fast); left_layout.addWidget(g_mode)
        
        # STREAMING SECTION
        lan_grp = QGroupBox("LAN STREAMING (WIFI)"); lan_lay = QVBoxLayout(lan_grp)
        
        # IP & Copy Row
        ip_row = QHBoxLayout()
        self.lbl_ip = QLabel("IP: OFFLINE"); self.lbl_ip.setStyleSheet("color: #666; font-size: 11px;")
        
        self.btn_copy = QPushButton("COPY LINK"); 
        self.btn_copy.setFixedWidth(70); 
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.setStyleSheet("background: #2a2a3a; color: #555; border: none; border-radius: 4px; font-size: 10px;")
        self.btn_copy.clicked.connect(self.copy_link)
        self.btn_copy.setEnabled(False)
        
        ip_row.addWidget(self.lbl_ip)
        ip_row.addWidget(self.btn_copy)
        
        self.lbl_warn = QLabel("Allow Python in Firewall!"); self.lbl_warn.setStyleSheet("color: #ffaa00; font-size: 10px; font-style: italic;") 
        self.btn_stream = ModernButton("GO LIVE (Broadcast)"); self.btn_stream.clicked.connect(self.toggle_stream)
        self.btn_stream.setCheckable(True)
        
        lan_lay.addLayout(ip_row)
        lan_lay.addWidget(self.lbl_warn)
        lan_lay.addWidget(self.btn_stream)
        left_layout.addWidget(lan_grp)
        
        left_layout.addSpacing(10); left_layout.addWidget(QLabel("MASTER GAIN"))
        self.slider_vol = QSlider(Qt.Orientation.Horizontal); self.slider_vol.setRange(0, 200); self.slider_vol.setValue(100); self.slider_vol.valueChanged.connect(self.update_volume); left_layout.addWidget(self.slider_vol)
        left_layout.addStretch()
        
        self.btn_power = ModernButton("INITIALIZE CORE", is_primary=True); self.btn_power.setFixedHeight(60); self.btn_power.clicked.connect(self.toggle_power); left_layout.addWidget(self.btn_power)
        main_layout.addWidget(left_panel)
        
        # CENTER COLUMN
        center_panel = QFrame(); center_panel.setStyleSheet("background: transparent;"); c_layout = QVBoxLayout(center_panel)
        self.visualizer = SciFiReactor(); c_layout.addWidget(self.visualizer)
        meter_layout = QHBoxLayout()
        self.lbl_in_meter = QLabel("IN: -Inf dB"); self.lbl_out_meter = QLabel("OUT: -Inf dB")
        meter_layout.addWidget(self.lbl_in_meter); meter_layout.addStretch(); meter_layout.addWidget(self.lbl_out_meter); c_layout.addLayout(meter_layout)
        main_layout.addWidget(center_panel, 1)
        
        # RIGHT COLUMN
        right_panel = QFrame(); right_panel.setFixedWidth(280); right_panel.setStyleSheet("background: #111625; border-radius: 15px; border: 1px solid #223344;")
        r_layout = QVBoxLayout(right_panel); r_layout.addWidget(QLabel("SOUND SIGNATURES"))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setStyleSheet("background: transparent; border: none;")
        p_widget = QWidget(); p_layout = QVBoxLayout(p_widget)
        for category, presets in SYSTEM_PRESETS.items():
            grp = QGroupBox(category); g_layout = QGridLayout(grp); g_layout.setSpacing(8)
            row, col = 0, 0
            for name, params in presets.items():
                short_name = name.split(" ", 1)[1] if " " in name else name
                emoji = name.split(" ")[0] if " " in name else ""
                btn = ModernButton(f"{emoji} {short_name}"); btn.setCheckable(True)
                btn.clicked.connect(lambda checked, n=name, p=params, b=btn: self.apply_preset(n, p, b))
                g_layout.addWidget(btn, row, col)
                col += 1
                if col > 1: col = 0; row += 1
            p_layout.addWidget(grp)
        p_layout.addStretch(); scroll.setWidget(p_widget); r_layout.addWidget(scroll); main_layout.addWidget(right_panel)

    def scan_devices(self):
        self.combo_dev.clear(); self.device_pairs = []
        if not AUDIO_AVAILABLE: self.combo_dev.addItem("Install sounddevice lib"); return
        try:
            devs = sd.query_devices(); apis = sd.query_hostapis()
            valid_inputs = [i for i, d in enumerate(devs) if d['max_input_channels'] > 0]
            valid_outputs = [i for i, d in enumerate(devs) if d['max_output_channels'] > 0]
            for i_idx in valid_inputs:
                for o_idx in valid_outputs:
                    i_d = devs[i_idx]; o_d = devs[o_idx]
                    if i_d['hostapi'] != o_d['hostapi'] or int(i_d['default_samplerate']) != int(o_d['default_samplerate']) or i_idx == o_idx: continue
                    api_name = apis[i_d['hostapi']]['name']
                    self.device_pairs.append({'in': i_idx, 'out': o_idx, 'rate': int(i_d['default_samplerate']), 'api': api_name})
                    self.combo_dev.addItem(f"[{api_name}] {i_d['name'][:15]}... ➜ {o_d['name'][:15]}...")
            if self.combo_dev.count() > 0: self.combo_dev.setCurrentIndex(0)
        except Exception as e: self.combo_dev.addItem(f"Error: {e}")

    def toggle_power(self):
        if not AUDIO_AVAILABLE: return
        if self.thread and self.thread.isRunning():
            self.thread.stop(); self.thread = None; self.btn_power.setText("INITIALIZE CORE"); self.btn_power.set_style()
            self.visualizer.set_level(0)
            if self.broadcaster: self.toggle_stream() # Force stop stream
        else:
            idx = self.combo_dev.currentIndex()
            if idx < 0: return
            cfg = self.device_pairs[idx]; mode = "stable" if self.btn_stable.isChecked() else "fast"
            self.processor = RealtimeAudioProcessor(cfg['rate'], 8192); self.processor.set_volume(self.slider_vol.value() / 100.0)
            if self.active_preset_btn: self.active_preset_btn.click()
            self.thread = SystemAudioThread(self.processor, cfg['in'], cfg['out'], cfg['rate'], mode)
            
            # LINK BROADCASTER IF ACTIVE
            if self.broadcaster and self.broadcaster.running:
                self.broadcaster.sample_rate = cfg['rate']
                self.thread.broadcaster = self.broadcaster
                
            self.thread.error_signal.connect(lambda e: QMessageBox.critical(self, "Core Error", e)); self.thread.start()
            self.btn_power.setText("TERMINATE PROCESS"); self.btn_power.setStyleSheet("background: #550000; color: white; border: none; border-radius: 5px; font-weight: bold; font-size: 16px;")

    def toggle_stream(self):
        if self.btn_stream.isChecked():
            # START
            self.broadcaster = StreamBroadcaster(5050)
            # Connect signal to update UI text safely
            self.broadcaster.port_found_signal.connect(self.on_stream_live)
            
            # Update Sample Rate if core is running
            if self.thread and self.thread.isRunning():
                self.broadcaster.sample_rate = self.thread.sample_rate
                self.thread.broadcaster = self.broadcaster
            
            self.broadcaster.start()
            self.btn_stream.setText("STOP BROADCAST")
            self.btn_stream.setStyleSheet("background: #ff0000; color: white; font-weight: bold;")
        else:
            # STOP
            if self.broadcaster:
                self.broadcaster.stop()
                self.broadcaster = None
            if self.thread:
                self.thread.broadcaster = None
            
            self.lbl_ip.setText("IP: OFFLINE")
            self.lbl_ip.setStyleSheet("color: #666;")
            self.btn_copy.setEnabled(False)
            self.btn_copy.setText("COPY LINK")
            self.btn_copy.setStyleSheet("background: #2a2a3a; color: #555; border: none; border-radius: 4px; font-size: 10px;")
            self.btn_stream.setText("GO LIVE (Broadcast)")
            self.btn_stream.set_style() # Reset

    def on_stream_live(self, text):
        self.lbl_ip.setText(text)
        self.lbl_ip.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.btn_copy.setEnabled(True)
        self.btn_copy.setStyleSheet("background: #00aa88; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 10px;")

    def copy_link(self):
        text = self.lbl_ip.text()
        if "LIVE: " in text:
            url = text.replace("LIVE: ", "")
            QApplication.clipboard().setText(url)
            self.btn_copy.setText("COPIED!")
            QTimer.singleShot(2000, lambda: self.btn_copy.setText("COPY LINK"))

    def apply_preset(self, name, params, btn):
        if self.active_preset_btn: self.active_preset_btn.setChecked(False)
        self.active_preset_btn = btn; btn.setChecked(True)
        if self.processor: self.processor.set_preset(params)

    def update_volume(self, val):
        if self.processor: self.processor.set_volume(val / 100.0)
    
    def sync_ui(self):
        if self.processor and self.thread and self.thread.isRunning():
            self.visualizer.set_level(min(1.0, self.processor.output_level * 1.5))
            self.lbl_in_meter.setText(f"IN: {self.processor.input_level*100:.1f}%"); self.lbl_out_meter.setText(f"OUT: {self.processor.output_level*100:.1f}%")
        else: self.visualizer.set_level(0)


# ============================================================================
# PART 6: MAIN APPLICATION
# ============================================================================

STYLESHEET = """
QMainWindow { background-color: #05080f; }
QWidget { color: #d0e0ff; font-family: "Segoe UI"; font-size: 12px; }
QFrame#Panel, QGroupBox { background-color: rgba(16, 24, 40, 0.7); border: 1px solid rgba(100, 150, 255, 0.2); border-radius: 12px; }
QGroupBox { margin-top: 15px; padding-top: 10px; font-weight: bold; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #88ccff; }
QPushButton { background-color: rgba(30, 45, 70, 0.6); border: 1px solid rgba(80, 120, 180, 0.4); border-radius: 8px; padding: 8px 16px; color: #ffffff; }
QPushButton:hover { background-color: rgba(50, 80, 120, 0.8); border-color: #00ffff; }
QPushButton#Primary { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 100, 200, 0.8), stop:1 rgba(0, 180, 220, 0.8)); border: 1px solid #00ffff; font-weight: bold; }
QSlider::groove:horizontal { height: 6px; background: #223344; border-radius: 3px; }
QSlider::handle:horizontal { width: 14px; margin: -5px 0; border-radius: 7px; background: #00ffff; }
QSlider::sub-page:horizontal { background: #00aaff; border-radius: 3px; }
QTabWidget::pane { border: none; }
QTabBar::tab { background: rgba(30, 45, 70, 0.6); color: #88ccff; padding: 8px 16px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 2px; }
QTabBar::tab:selected { background: rgba(50, 80, 120, 0.9); color: #fff; border-bottom: 2px solid #00ffff; }
QTreeWidget, QListWidget { background: rgba(10, 15, 25, 0.5); border: none; font-size: 13px; }
QTreeWidget::item:selected { background: rgba(0, 150, 255, 0.3); color: #fff; }
QLineEdit { background: #0a1018; border: 1px solid #335577; border-radius: 6px; padding: 4px; }
QComboBox { background: #1a2535; border: 1px solid #335577; border-radius: 6px; padding: 4px; color: #eee; }
QComboBox::drop-down { border: none; }
"""

class AuraHybridApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AURA: AFTERSHOCK EDITION")
        self.resize(1280, 850)
        
        # Tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self._create_icon(QColor(0, 255, 255)))
        tray_menu = QMenu(); restore = QAction("Open", self); restore.triggered.connect(self.showNormal)
        quit_a = QAction("Quit", self); quit_a.triggered.connect(self.force_quit)
        tray_menu.addAction(restore); tray_menu.addAction(quit_a)
        self.tray_icon.setContextMenu(tray_menu); self.tray_icon.show()

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(PlayerWidget(), " 🎵 AURA PLAYER ")
        self.tabs.addTab(SystemCoreWidget(), " ⚡ NEURO SYSTEM CORE ")
        self.setCentralWidget(self.tabs)

    def closeEvent(self, event):
        self.hide(); self.tray_icon.showMessage("AURA", "Running in Background", QSystemTrayIcon.MessageIcon.Information, 2000); event.ignore()
    def force_quit(self): self.tray_icon.hide(); QApplication.quit()
    def _create_icon(self, color):
        pixmap = QPixmap(64, 64); pixmap.fill(Qt.GlobalColor.transparent)
        p = QPainter(pixmap); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QBrush(QColor(10, 20, 30))); p.setPen(QPen(color, 4)); p.drawEllipse(4, 4, 56, 56)
        p.setBrush(QBrush(color)); p.drawEllipse(22, 22, 20, 20); p.end()
        return QIcon(pixmap)

def main():
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;*.warning=false"
    app = QApplication(sys.argv); app.setStyleSheet(STYLESHEET)
    w = AuraHybridApp(); w.show(); sys.exit(app.exec())

if __name__ == "__main__":
    main()