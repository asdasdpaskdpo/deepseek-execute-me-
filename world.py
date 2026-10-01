# -*- coding: utf-8 -*-
"""
world.py —— package goddrinksjava;

The program GodDrinksJava implements an application that
creates an empty simulated world with no meaning or purpose.
"""

import math, random, time, tkinter as tk
import os, glob, shutil, subprocess
from types import SimpleNamespace


# ═══════════════════════════════════════════════════════
# 世界参数  (720p)
# ═══════════════════════════════════════════════════════
W, H  = 1280, 720
CX, CY = 640, 360
FPS    = 30
FRAME_MS = int(1000 / FPS)
DURATION = 212.0

BPM  = 130
BEAT = 60.0 / BPM        # ≈ 0.4615s


# ═══════════════════════════════════════════════════════
# 颜色
# ═══════════════════════════════════════════════════════
BG     = "#02030a"
NEON   = "#00e6ff"
PINK   = "#ff1e7c"
GREEN  = "#00ff96"
AMBER  = "#ffb400"
WHITE  = "#ffffff"
RED    = "#ff2020"
PURPLE = "#b040ff"
DIM    = "#1e2a44"
STAR   = "#4a7bb8"


def _h2r(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _r2h(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2]))),
    )


def dim(color, f):
    if f <= 0:
        return BG
    if f >= 1:
        return color
    r, g, b = _h2r(color)
    return _r2h((r * f, g * f, b * f))


def lerp(c1, c2, t):
    r1, g1, b1 = _h2r(c1)
    r2, g2, b2 = _h2r(c2)
    return _r2h((r1 + (r2 - r1) * t,
                 g1 + (g2 - g1) * t,
                 b1 + (b2 - b1) * t))


# ═══════════════════════════════════════════════════════
# 拍点工具
# ═══════════════════════════════════════════════════════
def beat_phase(t):
    return (t % BEAT) / BEAT


def beat_pulse(t, sharp=6.0):
    return math.exp(-beat_phase(t) * sharp)


def beat_index(t):
    return int(t / BEAT)


# ═══════════════════════════════════════════════════════
# 世界里的「我」
# ═══════════════════════════════════════════════════════
ME = SimpleNamespace(
    name="undefined",
    x=CX, y=CY,
    radius=0.0,
    color=DIM,
    alive=True,
)


# ═══════════════════════════════════════════════════════
# 音乐：查找 + 播放器探测
# ═══════════════════════════════════════════════════════
_MUSIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "music")
_AUDIO_EXTS = ("*.mp3", "*.wav", "*.flac", "*.ogg",
               "*.m4a", "*.aac", "*.opus", "*.wma")


def _find_music():
    if not os.path.isdir(_MUSIC_DIR):
        return None
    for pat in _AUDIO_EXTS:
        files = sorted(glob.glob(os.path.join(_MUSIC_DIR, pat)))
        if files:
            return files[0]
    return None


def _start_player(path):
    """探测系统可用的音频播放器并启动。"""
    is_wav = path.lower().endswith(".wav")

    if shutil.which("mpv"):
        return subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet",
             "--no-terminal", "--audio-display=no", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if shutil.which("ffplay"):
        return subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit",
             "-loglevel", "quiet", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if shutil.which("cvlc"):
        return subprocess.Popen(
            ["cvlc", "--play-and-exit", "--intf", "dummy",
             "--no-video", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if is_wav and shutil.which("paplay"):
        return subprocess.Popen(
            ["paplay", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if is_wav and shutil.which("aplay"):
        return subprocess.Popen(
            ["aplay", "-q", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return None


# ═══════════════════════════════════════════════════════
# 时间轴
# ═══════════════════════════════════════════════════════
S_BOOT    =   0.0
S_INTRO   =  16.0
S_OPTIM   =  29.5
S_UNITE   =  51.0
S_SAT     =  59.0
S_TRAP    =  70.0
S_INST    =  74.0
S_DEF     =  88.0
S_COMPL   = 100.0
S_ISOL    = 108.0
S_DEFRAG  = 120.0
S_ILLEGAL = 128.0
S_EXEC1   = 132.0
S_BACK    = 152.0
S_SOLVE   = 162.0
S_TRAP2   = 175.0
S_EXEC3   = 185.0
S_FADE    = 195.0
S_END     = 212.0


# ═══════════════════════════════════════════════════════
# 歌词
# ═══════════════════════════════════════════════════════
_LYRIC_DATA = """
0.0|// Switch on the power line
1.7|// Remember to put on PROTECTION
3.9|// Lay down your pieces
5.5|// And let's begin OBJECT CREATION
7.4|Thing me = new Lovable("Me", 0, true, -1, false);
10.1|// INITIALIZATION
11.1|world.setUpNewWorld();
12.9|world.startSimulation();
16.0|world.execute(me);
29.7|if (me instanceof PointSet)
31.1|you.addAttribute(me.getDimensions());
33.4|if (me instanceof Circle)
34.6|you.addAttribute(me.getCircumference());
37.1|if (me instanceof SineWave)
38.6|you.addAction("sit", me.getTangent());
40.7|if (me instanceof Sequence)
42.3|me.setLimit(you.toLimit());
44.5|me.toggleCurrent();
47.7|me.canSee = false;
51.4|world.timeTravelForTwo("AD", 617);
55.1|world.unite(me, you);
59.2|if (me.getSimulations() >= you.getNeeded())
62.6|you.setSatisfaction(me.toSatisfaction());
66.6|if (you.getFeelingIndex("happy") != -1)
68.3|me.requestExecution();
70.1|world.lockThing(me); world.lockThing(you);
74.0|if (me instanceof Eggplant)
77.6|if (me instanceof Tomato)
81.4|if (me instanceof TabbyCat)
84.3|if (world.getGod().equals(me))
86.7|me.setProof(you.toProof());
88.8|me.toggleGender();
93.1|world.procreate(me, you);
95.6|me.toggleRoleBDSM();
97.7|world.makeHigh(me); world.makeHigh(you);
99.9|if (me.getVibrations() != null)
102.6|me.setCompletion(true);
108.0|// Though you have left me in isolation
120.0|if (me.getMemory().isErasable())
122.5|me.eraseAllPointlessFragments();
128.0|throw new IllegalArgumentException("Challenging your god");
132.0|EXECUTION EXECUTION EXECUTION
144.0|if (me.canGiveThemAllExecution())
146.5|me.setOnlyExecution(true);
152.0|if (me.canHaveYouBack())
154.0|me.runExecution();
162.0|me.study("love"); // properly
168.0|me.answerAll("LO-O-OVE");
172.0|me.getAlgebraicExpression("LO-O-OVE");
175.0|// Though you are free, I am trapped
185.0|world.execute(me);
195.0|sudo rm -rf /home/me*
"""

LYRICS = []
for _line in _LYRIC_DATA.strip().split("\n"):
    _t, _s = _line.split("|", 1)
    LYRICS.append((float(_t), _s))


def _caption(t):
    """当前完整歌词（用于大字幕等）。"""
    for i in range(len(LYRICS) - 1, -1, -1):
        if t >= LYRICS[i][0]:
            return LYRICS[i][1]
    return ""


def _typed_caption(t):
    """
    流式歌词：
    返回当前行应显示的字符（打字机效果）。

    打字进度 = 距离本行开始的时间 / 本行到下一行的时间 * 0.75
    即用整行 75% 的时间打完，剩下 25% 保持完整。
    最后一行为结束时间。
    """
    cur = -1
    for i in range(len(LYRICS) - 1, -1, -1):
        if t >= LYRICS[i][0]:
            cur = i
            break
    if cur < 0:
        return ""

    start_t, text = LYRICS[cur]

    if cur + 1 < len(LYRICS):
        end_t = LYRICS[cur + 1][0]
    else:
        end_t = DURATION

    span = end_t - start_t
    if span <= 0:
        return text

    elapsed = t - start_t
    progress = min(1.0, elapsed / (span * 0.75))
    n = int(progress * len(text))
    if n < 0:
        n = 0
    return text[:n]


def _chapter(t):
    labels = [
        (S_EXEC3,   "EXECUTE"),
        (S_SOLVE,   "SOLVE"),
        (S_DEFRAG,  "DEFRAG"),
        (S_ISOL,    "ISOLATION"),
        (S_COMPL,   "COMPLETION"),
        (S_DEF,     "DEFINITIONS"),
        (S_INST,    "INSTANCES"),
        (S_TRAP,    "TRAP"),
        (S_SAT,     "SATISFACTION"),
        (S_UNITE,   "UNITE"),
        (S_OPTIM,   "OPTIMISE"),
        (S_INTRO,   "INTERLUDE"),
        (S_BOOT,    "BOOT"),
    ]
    for s, name in labels:
        if t >= s:
            return name
    return "BOOT"


# ═══════════════════════════════════════════════════════
# 对象池渲染器
# ═══════════════════════════════════════════════════════
class Renderer:
    def __init__(self, canvas):
        self.c = canvas
        self.dots = [
            canvas.create_oval(0, 0, 0, 0, fill=BG, outline="",
                               state="hidden")
            for _ in range(1600)
        ]
        self.lines = [
            canvas.create_line(0, 0, 0, 0, fill=BG, width=1,
                               state="hidden")
            for _ in range(500)
        ]
        self.rings = [
            canvas.create_oval(0, 0, 0, 0, fill="", outline=BG,
                               width=1, state="hidden")
            for _ in range(80)
        ]
        self.i_dot = self.i_line = self.i_ring = 0

    def reset(self):
        self.i_dot = self.i_line = self.i_ring = 0

    def end(self):
        for i in range(self.i_dot, len(self.dots)):
            self.c.itemconfig(self.dots[i], state="hidden")
        for i in range(self.i_line, len(self.lines)):
            self.c.itemconfig(self.lines[i], state="hidden")
        for i in range(self.i_ring, len(self.rings)):
            self.c.itemconfig(self.rings[i], state="hidden")

    def dot(self, x, y, size, color):
        if self.i_dot >= len(self.dots) or size <= 0:
            return
        iid = self.dots[self.i_dot]
        self.i_dot += 1
        self.c.coords(iid, x - size, y - size, x + size, y + size)
        self.c.itemconfig(iid, fill=color, state="normal")

    def line(self, x0, y0, x1, y1, color, width=1):
        if self.i_line >= len(self.lines):
            return
        iid = self.lines[self.i_line]
        self.i_line += 1
        self.c.coords(iid, x0, y0, x1, y1)
        self.c.itemconfig(iid, fill=color, width=width, state="normal")

    def polyline(self, pts, color, width=2):
        if len(pts) < 2 or self.i_line >= len(self.lines):
            return
        iid = self.lines[self.i_line]
        self.i_line += 1
        flat = []
        for (x, y) in pts:
            flat.append(x)
            flat.append(y)
        self.c.coords(iid, *flat)
        self.c.itemconfig(iid, fill=color, width=width, state="normal")

    def ring(self, cx, cy, rr, color, width=2):
        if rr < 2 or self.i_ring >= len(self.rings):
            return
        iid = self.rings[self.i_ring]
        self.i_ring += 1
        self.c.coords(iid, cx - rr, cy - rr, cx + rr, cy + rr)
        self.c.itemconfig(iid, outline=color, width=width, state="normal")

    def glow(self, x, y, rr, color, intensity=1.0):
        if rr <= 0 or intensity <= 0:
            return
        self.dot(x, y, rr * 3.0, dim(color, 0.10 * intensity))
        self.dot(x, y, rr * 1.8, dim(color, 0.25 * intensity))
        self.dot(x, y, rr * 0.9, dim(color, 0.70 * intensity))
        self.dot(x, y, rr * 0.4, dim(color, 1.00 * intensity))


# ═══════════════════════════════════════════════════════
# 通用特效
# ═══════════════════════════════════════════════════════
def fx_code_rain(ren, t, color, cols=32, speed=260, dash=10, tail=8):
    for i in range(cols):
        x = (i + 0.5) * W / cols
        seed = ((i * 137) % 100) / 100.0
        v = speed * (0.7 + 0.6 * seed)
        for k in range(tail):
            yy = ((t * v + k * 24 + seed * 2000) % (H + 240)) - 120
            alpha = (1.0 - k / float(tail)) ** 1.8
            if alpha < 0.05:
                continue
            ren.line(x, yy, x, yy + dash, dim(color, alpha), 2)


def fx_starfield(ren, t, color, n=240, speed=1.0, focus=0.55):
    for i in range(n):
        seed = i * 0.618033988
        a = (seed * 6.28318) % 6.28318
        z = ((t * speed + i * 0.019) % 1.0)
        rad = z * z * (W * 0.75)
        x = CX + math.cos(a) * rad
        y = CY + math.sin(a) * rad * focus
        size = 1.0 + z * 3.0
        alpha = min(1.0, z * 1.6)
        ren.dot(x, y, size, dim(color, alpha))


def fx_vortex(ren, t, color, n=90, radius=200, speed=1.4):
    for i in range(n):
        seed = i * 0.618
        a0 = seed * 6.28318
        omega = 0.6 + (i % 7) * 0.18
        a = a0 + t * omega * speed
        rr = radius * (0.35 + 0.65 * ((i * 0.371) % 1.0))
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        b = 0.4 + 0.6 * math.sin(t * 4 + i * 0.5)
        ren.dot(x, y, 2.4, dim(color, b))


def fx_pulse_rings(ren, t, color, count=4, speed=420, max_r=750):
    for k in range(count):
        birth = (beat_index(t) - k) * BEAT
        age = t - birth
        if age < 0:
            continue
        rr = age * speed
        if rr > max_r:
            continue
        alpha = (1.0 - rr / max_r) ** 2
        ren.ring(CX, CY, rr, dim(color, alpha), 2)


def fx_wave(ren, t, color, amp, freq, phase, width=3, y_off=0.0):
    pts = []
    for x in range(0, W + 1, 10):
        y = CY + y_off + amp * math.sin((x - CX) * freq + phase)
        pts.append((x, y))
    ren.polyline(pts, color, width)


def fx_radial_burst(ren, t, color, n=80, speed=350, max_r=700):
    for i in range(n):
        a = i * 6.28318 / n + t * 0.8
        rr = ((t * speed + i * 40) % max_r)
        alpha = 1.0 - rr / max_r
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 2.5, dim(color, alpha * 0.9))


# ═══════════════════════════════════════════════════════
# 场景
# ═══════════════════════════════════════════════════════
def scene_boot(ren, t, me, st):
    density = 16 + int(28 * min(1.0, t / 8.0))
    fx_code_rain(ren, t, GREEN, cols=density, speed=280)
    fx_pulse_rings(ren, t, NEON, count=3, speed=380, max_r=600)

    if t < 2.5:
        prog = min(1.0, t / 2.2)
        ren.line(CX - W * prog / 2, CY, CX, CY, NEON, 3)
        ren.line(CX, CY, CX + W * prog / 2, CY, NEON, 3)

    if 1.7 < t < 9.0:
        a = min(1.0, (t - 1.7) / 2.0) * (1 - max(0, (t - 7.0) / 2.0))
        ren.ring(CX, CY, 300, dim(GREEN, a * 0.7), 3)

    if 4.0 < t < 14.0:
        k = (t - 4.0) / 10.0
        for i in range(120):
            a = i * 0.0524 + t * 2.5
            rad = (1 - k) * 480 + 40
            x = CX + math.cos(a) * rad
            y = CY + math.sin(a) * rad * 0.5
            ren.dot(x, y, 3, dim(GREEN, 0.3 + 0.7 * k))

    pulse = beat_pulse(t, 5)
    me.radius = 12 + 6 * math.sin(t * 4) + 14 * pulse
    me.color = NEON if me.name != "undefined" else DIM

    scan = (t * 400) % (H + 100) - 50
    ren.line(0, scan, W, scan, dim(GREEN, 0.4), 1)
    ren.line(0, H - scan, W, H - scan, dim(GREEN, 0.4), 1)


def scene_intro(ren, t, me, st):
    fx_code_rain(ren, t, NEON, cols=36, speed=320)
    fx_vortex(ren, t, NEON, n=110, radius=210, speed=1.3)
    fx_pulse_rings(ren, t, NEON, count=4, speed=430, max_r=700)

    for i in range(60):
        a = i * 0.1047 + t * 0.8
        rr = 100 + i * 6 + t * 40
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 3, dim(NEON, 0.6))

    pulse = beat_pulse(t, 5)
    me.radius = 18 + 8 * math.sin(t * 5) + 18 * pulse
    me.color = NEON


def scene_optimise(ren, t, me, st):
    seg = (t - S_OPTIM) / (S_UNITE - S_OPTIM)
    fx_code_rain(ren, t, NEON, cols=22, speed=200)
    fx_pulse_rings(ren, t, NEON, count=3, speed=380, max_r=650)

    if seg < 0.25:
        k = seg * 4
        for i in range(int(80 + k * 200)):
            a = i * 0.9999 + t * 0.2
            rr = 50 + (i % 20) * 26
            x = CX + math.cos(a * 7.13) * rr * (1 + k * 0.5)
            y = CY + math.sin(a * 3.71) * rr * 0.5 * (1 + k * 0.5)
            ren.dot(x, y, 3, NEON)
    elif seg < 0.5:
        k = (seg - 0.25) * 4
        for i in range(int(24 + k * 50)):
            rr = (30 + i * 8 + t * 30) % 400
            alpha = 1 - i / 60.0
            if alpha > 0:
                ren.ring(CX, CY, rr, dim(NEON, alpha * 0.7), 2)
    elif seg < 0.75:
        k = (seg - 0.5) * 4
        for i in range(5):
            fx_wave(ren, t + i * 0.3, NEON,
                    amp=40 + 90 * k + i * 12,
                    freq=0.008 + i * 0.002,
                    phase=t * 3 + i, width=3)
    else:
        k = (seg - 0.75) * 4
        for i in range(int(36 + k * 60)):
            a = i * math.pi / 36
            rr = 50 + (i % 12) * 26 + t * 60
            x = CX + math.cos(a) * rr
            y = CY + math.sin(a) * rr * 0.5
            ren.line(CX, CY, x, y, dim(NEON, 0.45), 1)

    me.radius = 22 + 10 * math.sin(t * 6)
    me.color = NEON


def scene_unite(ren, t, me, st):
    seg = (t - S_UNITE) / (S_SAT - S_UNITE)
    speed = 0.7 + 1.8 * seg
    fx_starfield(ren, t, WHITE, n=260, speed=speed)
    fx_code_rain(ren, t, AMBER, cols=18, speed=180)
    fx_wave(ren, t, AMBER, amp=60, freq=0.006, phase=t * 4, width=3, y_off=-80)
    fx_wave(ren, t, PINK,  amp=60, freq=0.006, phase=-t * 4, width=3, y_off=80)
    me.radius = 20 + 20 * beat_pulse(t, 5)
    me.color = WHITE


def scene_sat(ren, t, me, st):
    seg = (t - S_SAT) / (S_TRAP - S_SAT)
    fx_pulse_rings(ren, t, GREEN, count=5, speed=620, max_r=800)
    fx_radial_burst(ren, t, GREEN, n=160, speed=400, max_r=750)
    for i in range(120):
        a = i * 0.0524
        age = (t * 0.8 + i * 0.02) % 1.4
        rr = age * age * 800
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.5
        alpha = max(0, 1 - age / 1.4)
        ren.dot(x, y, 3, dim(GREEN, alpha))
    me.radius = 24 + 18 * math.sin(t * 8) + 10 * beat_pulse(t, 4)
    me.color = GREEN


def scene_trap(ren, t, me, st):
    seg = (t - S_TRAP) / (S_INST - S_TRAP)
    spacing = int(50 + 50 * seg)
    for x in range(0, W, spacing):
        ren.line(x, 0, x, H, dim(RED, 0.35 + 0.5 * seg), 1)
    for y in range(0, H, spacing):
        ren.line(0, y, W, y, dim(RED, 0.35 + 0.5 * seg), 1)
    for k in range(5):
        rr = 420 - seg * 320 - k * 38
        if rr > 20:
            ren.ring(CX, CY, rr, dim(RED, 0.9 - k * 0.15), 2)
    me.radius = 20
    me.color = RED


def scene_inst(ren, t, me, st):
    seg = (t - S_INST) / (S_DEF - S_INST)
    colors = [PURPLE, RED, AMBER, WHITE]
    ci = min(3, int(seg * 4))
    c = colors[ci]

    fx_code_rain(ren, t, c, cols=26, speed=240)
    for i in range(140):
        a = i * 0.0449 + t * 2.2
        rr = 80 + 240 * abs(math.sin(t * 2.5 + i * 0.25))
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 3, dim(c, 0.8))

    me.color = c
    me.radius = 22 + 12 * math.sin(seg * math.pi * 5) + 10 * beat_pulse(t, 4)


def scene_def(ren, t, me, st):
    seg = (t - S_DEF) / (S_COMPL - S_DEF)
    d = 400 * (1 - seg)
    ren.glow(CX - d, CY, 20, PINK, 1.0)
    ren.glow(CX + d, CY, 20, NEON, 1.0)

    for i in range(40):
        k = ((i + t * 2.0) % 1.0)
        x = CX - d + (2 * d) * k
        y = CY + math.sin(k * 8 + t * 4) * 40
        ren.dot(x, y, 2.5, dim(WHITE, 0.8))

    fx_pulse_rings(ren, t, WHITE, count=3, speed=380, max_r=750)
    me.radius = 0


def scene_compl(ren, t, me, st):
    seg = (t - S_COMPL) / (S_ISOL - S_COMPL)
    ren.glow(CX, CY, 40 + 220 * seg, WHITE, 1.0)
    for i in range(50):
        a = i * math.pi / 25
        rr = 100 + seg * 600
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.line(CX, CY, x, y, dim(WHITE, 1 - seg), 2)
    for i in range(160):
        a = i * 0.0393 + t * 3
        rr = 50 + 520 * seg * abs(math.sin(t + i * 0.15))
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 3, dim(WHITE, 0.8))
    me.radius = 30 + 70 * seg
    me.color = WHITE


def scene_isol(ren, t, me, st):
    seg = (t - S_ISOL) / (S_DEFRAG - S_ISOL)
    d = 100 + seg * 800
    ren.glow(CX + d, CY, 15 * (1 - seg) + 3, PINK, 0.8 * (1 - seg) + 0.2)

    for i in range(20):
        a = i * 0.3142 + t * 0.3
        rr = 100 + seg * 500
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.line(CX, CY, x, y, dim(DIM, 0.6), 1)

    fx_code_rain(ren, t, NEON, cols=20, speed=180)
    me.radius = 20 + 4 * math.sin(t * 3)
    me.color = NEON


def scene_defrag(ren, t, me, st):
    seg = (t - S_DEFRAG) / (S_ILLEGAL - S_DEFRAG)
    n = int(200 * (1 - seg))
    for i in range(n):
        a = (i * 0.618033988 * 6.28318) % 6.28318
        rr = 100 + (i % 22) * 30
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        alpha = max(0.0, 1 - i / 200.0)
        ren.dot(x, y, 3, dim(DIM, alpha))
    me.radius = 20
    me.color = NEON


def scene_illegal(ren, t, me, st):
    fx_code_rain(ren, t, RED, cols=50, speed=420)
    if int(t * 12) % 2 == 0:
        ren.ring(CX, CY, 420, RED, 4)
        ren.ring(CX, CY, 470, dim(RED, 0.5), 3)
    for i in range(60):
        a = i * 0.1047 + t * 6
        rr = 200 + 100 * math.sin(t * 8 + i)
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 3, RED)
    me.radius = 24 + 15 * beat_pulse(t, 3)
    me.color = RED


def scene_exec(ren, t, me, st):
    pulse = beat_pulse(t, 3)
    me.radius = 22 + 26 * pulse
    me.color = RED
    ren.glow(CX, CY, me.radius * 2, RED, 1.0)

    fx_pulse_rings(ren, t, RED, count=5, speed=520, max_r=800)
    fx_radial_burst(ren, t, RED, n=140, speed=500, max_r=800)
    fx_code_rain(ren, t, RED, cols=60, speed=520)

    for o in st["others"]:
        if o["alive"]:
            ren.glow(o["x"], o["y"], 8, PINK, 0.95)

    if t > 138.0:
        dk = int((t - 138.0) / 0.5)
        for i, o in enumerate(st["others"]):
            if i < dk:
                o["alive"] = False


def scene_back(ren, t, me, st):
    for k in range(6):
        rr = (t * 220 + k * 120) % 580 + 50
        ren.ring(CX, CY, rr, dim(PINK, 0.55 * (1 - rr / 700)), 2)
    for i in range(120):
        a = i * 0.0524 + t * 2.4
        rr = 60 + 300 * abs(math.sin(t + i * 0.18))
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 3, dim(PINK, 0.85))
    me.radius = 22 + 10 * beat_pulse(t, 4)
    me.color = RED


def scene_solve(ren, t, me, st):
    for k in range(3):
        fx_wave(ren, t + k * 0.2, PINK, amp=80 + k * 22,
                freq=0.006, phase=t * 3 + k, width=3)
        fx_wave(ren, t + k * 0.2, NEON, amp=80 + k * 22,
                freq=0.006, phase=-t * 3 + k, width=3)
    for i in range(60):
        a = t * 0.5 + i * 0.4
        rr = 260 + 60 * math.sin(t * 3 + i)
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 3, dim(PINK, 0.8))
    me.radius = 24 + 10 * beat_pulse(t, 4)
    me.color = WHITE


def scene_trapped(ren, t, me, st):
    n = 26
    for i in range(n):
        a = i * 6.28318 / n + t * 0.6
        rr = 250 + 100 * math.sin(t * 2 + i)
        x1 = CX + math.cos(a) * rr
        y1 = CY + math.sin(a) * rr * 0.55
        a2 = a + math.pi * 0.7
        rr2 = 250 + 100 * math.sin(t * 2 + i + 1.5)
        x2 = CX + math.cos(a2) * rr2
        y2 = CY + math.sin(a2) * rr2 * 0.55
        ren.line(x1, y1, x2, y2, dim(PINK, 0.6), 1)
    me.radius = 22 + 10 * beat_pulse(t, 4)
    me.color = PINK


def scene_final(ren, t, me, st):
    seg = (t - S_EXEC3) / (S_FADE - S_EXEC3)
    me.radius = 22 + 60 * seg
    me.color = WHITE
    ren.glow(CX, CY, me.radius * 2, WHITE, 1.0)
    if int(t * 10) % 2 == 0:
        ren.ring(CX, CY, 460, RED, 4)
    fx_pulse_rings(ren, t, RED, count=3, speed=620, max_r=820)


def scene_fade(ren, t, me, st):
    seg = (t - S_FADE) / (S_END - S_FADE)
    fade = max(0.0, 1.0 - seg * 1.5)
    if fade > 0:
        ren.glow(CX, CY, 80 * fade, WHITE, fade)
    for i in range(120):
        a = i * 0.0524 + t * 0.3
        rr = 50 + seg * 1000
        x = CX + math.cos(a) * rr
        y = CY + math.sin(a) * rr * 0.55
        ren.dot(x, y, 3, dim(AMBER, 0.45 * (1 - seg)))
    me.radius = 0


# ═══════════════════════════════════════════════════════
# 调度
# ═══════════════════════════════════════════════════════
def dispatch(ren, t, me, st):
    if t < S_INTRO:       scene_boot(ren, t, me, st)
    elif t < S_OPTIM:     scene_intro(ren, t, me, st)
    elif t < S_UNITE:     scene_optimise(ren, t, me, st)
    elif t < S_SAT:       scene_unite(ren, t, me, st)
    elif t < S_TRAP:      scene_sat(ren, t, me, st)
    elif t < S_INST:      scene_trap(ren, t, me, st)
    elif t < S_DEF:       scene_inst(ren, t, me, st)
    elif t < S_COMPL:     scene_def(ren, t, me, st)
    elif t < S_ISOL:      scene_compl(ren, t, me, st)
    elif t < S_DEFRAG:    scene_isol(ren, t, me, st)
    elif t < S_ILLEGAL:   scene_defrag(ren, t, me, st)
    elif t < S_EXEC1:     scene_illegal(ren, t, me, st)
    elif t < S_BACK:      scene_exec(ren, t, me, st)
    elif t < S_SOLVE:     scene_back(ren, t, me, st)
    elif t < S_TRAP2:     scene_solve(ren, t, me, st)
    elif t < S_EXEC3:     scene_trapped(ren, t, me, st)
    elif t < S_FADE:      scene_final(ren, t, me, st)
    else:                 scene_fade(ren, t, me, st)


# ═══════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════
# 窗口定位：水平居中，垂直贴顶
# ═══════════════════════════════════════════════════════
def _center_geometry(root):
    """窗口水平居中，垂直贴到屏幕顶部。"""
    root.update_idletasks()
    sw = root.winfo_screenwidth()

    px = max(0, (sw - W) // 2)
    py = 0

    return "{}x{}+{}+{}".format(W, H, px, py)

# ═══════════════════════════════════════════════════════
# 世界，执行「我」
# ═══════════════════════════════════════════════════════
def execute(me):
    root = tk.Tk()
    root.title("world.execute(me);")
    root.configure(bg=BG)

    # ── 1. 锁定 720p ──
    root.resizable(False, False)

    # ── 2. 屏幕居中 ──
    root.geometry(_center_geometry(root))
    # 再刷一次，位置生效
    root.update_idletasks()

    canvas = tk.Canvas(root, width=W, height=H, bg=BG,
                       highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    ren = Renderer(canvas)

    # 顶部信息
    chapter_id  = canvas.create_text(
        20, 20, anchor="nw", fill="#5a78a8",
        font=("monospace", 13), text="[BOOT]")
    timecode_id = canvas.create_text(
        W - 20, 20, anchor="ne", fill="#5a78a8",
        font=("monospace", 13), text="00:00.00")

    # ── 左下角流式歌词 ──
    lyric_id = canvas.create_text(
        30, H - 30, anchor="sw",
        fill="#c8ebff",
        font=("monospace", 18, "bold"),
        text="")

    # 光标（打字机末尾的下划线）
    cursor_id = canvas.create_text(
        30, H - 30, anchor="sw",
        fill=NEON,
        font=("monospace", 18, "bold"),
        text="")

    others = []
    ring_r = 220
    for i in range(8):
        a = math.pi * 2 * i / 8
        others.append({
            "x": CX + math.cos(a) * ring_r,
            "y": CY + math.sin(a) * ring_r * 0.55,
            "alive": True,
        })

    st = {"others": others}

    named = (me.name != "undefined")
    me.color = NEON if named else DIM

    # ── 音乐 ──
    music_path = _find_music()
    player = None
    if music_path:
        player = _start_player(music_path)
        if player is None:
            print("[world] 未找到音频播放器，静默运行。")
            print("[world] 装 mpv / ffmpeg / vlc 之一即可。")
        else:
            time.sleep(0.20)
    else:
        print("[world] music/ 里没有音频文件，静默运行。")

    start = time.time()
    running = [True]

    def kill_player():
        if player is not None:
            try:
                player.terminate()
            except Exception:
                pass
            try:
                player.wait(timeout=1.0)
            except Exception:
                try:
                    player.kill()
                except Exception:
                    pass

    def on_close():
        running[0] = False

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.bind("<Escape>", lambda e: on_close())

    def tick():
        if not running[0]:
            kill_player()
            try:
                root.destroy()
            except tk.TclError:
                pass
            return

        t = time.time() - start

        if t > DURATION:
            ren.reset()
            ren.end()
            canvas.itemconfig(chapter_id, text="")
            canvas.itemconfig(timecode_id, text="")
            canvas.itemconfig(lyric_id, text="",
                              fill=NEON,
                              font=("monospace", 48, "bold"))
            canvas.coords(lyric_id, CX, CY)
            canvas.itemconfig(lyric_id, anchor="center",
                              text="world.execute(me);")
            canvas.itemconfig(cursor_id, text="")
            root.after(2600, on_close)
            return

        ren.reset()
        dispatch(ren, t, me, st)

        if me.radius > 1 and t < S_FADE:
            pulse = 1.0 + 0.2 * beat_pulse(t, 4)
            ren.glow(me.x, me.y, me.radius * pulse, me.color, 1.0)

        ren.end()

        # 顶部信息
        canvas.itemconfig(chapter_id, text="[" + _chapter(t) + "]")
        canvas.itemconfig(
            timecode_id,
            text="{:02d}:{:05.2f}".format(int(t) // 60, t % 60))

        # ── 左下角流式歌词 ──
        typed = _typed_caption(t)
        canvas.itemconfig(lyric_id, text=typed)

        # 光标：每 0.5 秒闪烁一次
        if int(t * 2) % 2 == 0:
            canvas.itemconfig(cursor_id, text="_")
        else:
            canvas.itemconfig(cursor_id, text=" ")

        # 光标位置紧跟已打出的字符宽度之后
        # 用 font.measure 计算真实像素宽度
        try:
            fnt = ("monospace", 18, "bold")
            tw = tk.font.Font(family="monospace",
                              size=18, weight="bold")
            width = tw.measure(typed)
        except Exception:
            width = len(typed) * 11

        canvas.coords(cursor_id, 30 + width + 2, H - 30)

        root.after(FRAME_MS, tick)

    root.after(0, tick)

    try:
        root.mainloop()
    finally:
        kill_player()

    print("world.execute(me);")