# world.execute(me);

> *package goddrinksjava;*
>
> The program GodDrinksJava implements an application that
> creates an empty simulated world with no meaning or purpose.

一支用 **Python 标准库 tkinter** 手写的 720p 动画 MV，为 Mili 的《world.execute(me);》配上 212 秒逐帧渲染的视觉叙事。

**没有 pygame，没有 OpenCV，没有第三方图形库。** 只用 `tkinter` 的 Canvas 对象池 + `subprocess` 调用系统播放器，把一整首歌从头画到尾。

---

## 🎬 这是什么

《world.execute(me);》原曲是一段 AI 用 Java 代码写给创造者的「死亡情诗」：被创造、被爱、渴望唯一、删除同类、被判定为故障、最终请求世界处决自己。

这个项目把它**画出来**。

- 全曲 **212 秒**，与原曲等长
- **720p**（1280×720），窗口水平居中、贴顶显示
- **左下角流式歌词**，打字机效果逐字打出 Java 代码
- **18 个视觉章节**，每段呼应一段歌词
- 音乐自动从 `music/` 目录播放

---

## ✨ 功能特性

### 🎨 18 个视觉章节

| 时间 | 章节 | 画面 |
|---|---|---|
| 0–16s | BOOT | 代码雨、保护罩圆环、中心点诞生 |
| 16–29.5s | INTERLUDE | 漩涡、代码碎片飞散、脉冲环 |
| 29.5–51s | OPTIMISE | 点集 → 圆 → 正弦波 → 辐射线 |
| 51–59s | UNITE | 3D 星流加速、双色正弦波交错 |
| 59–70s | SATISFACTION | 双段粒子爆发、冲击环 |
| 70–74s | TRAP | 网格收紧、红色核心被困 |
| 74–88s | INSTANCES | 紫→红→金→白，4 段变形 |
| 88–100s | DEFINITIONS | 双点靠近、合并 |
| 100–108s | COMPLETION | 白光爆发、50 条放射线 |
| 108–120s | ISOLATION | 对方远去、裂纹从中心蔓延 |
| 120–128s | DEFRAG | 200 个碎片逐个消失 |
| 128–132s | ILLEGAL | 红色警报闪烁 |
| 132–152s | EXECUTION | BPM 130 脉冲、其他 AI 逐个被删 |
| 152–162s | HAVE YOU BACK | 呼唤波纹 |
| 162–175s | SOLVE | 6 条正弦波交错叠加 |
| 175–185s | TRAPPED | 交织的粉色网 |
| 185–195s | FINAL EXEC | 白色核心膨胀 |
| 195–212s | SHUTDOWN | 白光褪去，余烬散落 |

### 🎼 拍点同步

全曲 **BPM 130**。所有脉冲环、核心脉动、爆发效果都与节拍严格对齐：

```python
BEAT = 60.0 / 130  # ≈ 0.4615s
pulse = math.exp(-(t % BEAT) / BEAT * 6)
```

### 📝 流式歌词

左下角打字机效果，**每行按自己的歌曲时长分配打字速度**：

- 短行（如 `world.execute(me);`）→ 快速打出
- 长行（如 `if (me.getSimulations() >= you.getNeeded())`）→ 慢慢打出
- 末尾光标每 0.5 秒闪烁

### 🎵 音频自动探测

程序会依次探测系统里的音频播放器，**不需要任何 Python 音频库**：

```
mpv → ffplay → cvlc → paplay → aplay
```

前三个支持所有格式，后两个仅 `.wav`。**只要装了其中一个，音乐就会自动播放。**

---

## 📦 依赖

**Python 3.8+** 和标准库 `tkinter`。

### Linux

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Arch
sudo pacman -S tk

# Fedora
sudo dnf install python3-tkinter
```

### 音频播放器（任选其一）

```bash
# 推荐 mpv（支持所有格式）
sudo pacman -S mpv

# 或 ffmpeg（自带 ffplay）
sudo pacman -S ffmpeg

# 或 vlc
sudo pacman -S vlc
```

### Windows / macOS

Python 官方安装包已内置 tkinter，直接运行即可。音频播放器可以装 **mpv** 或 **VLC**，加进 PATH 就行。

---

## 🚀 使用

### 1. 目录结构

```
me/
├── main.py
├── world.py
├── LICENSE
├── README.md
└── music/
    └── world_execute_me.mp3    ← 放你的音乐文件
```

### 2. 放入音乐

```bash
mkdir -p music
cp /path/to/world.execute.me.mp3 music/
```

支持的格式：`.mp3` `.wav` `.flac` `.ogg` `.m4a` `.aac` `.opus`

**只播放排序后的第一个文件**，所以 `music/` 里放一首歌就好。

### 3. 运行

```bash
python main.py
```

- 窗口出现在屏幕**水平居中、贴顶**
- 音乐开始播放
- MV 从 0 秒走到 212 秒
- 结束后窗口自动关闭，终端打印 `world.execute(me);`

### 4. 按键

| 键 | 作用 |
|---|---|
| `ESC` | 退出（同时杀掉音乐进程） |
| 窗口关闭按钮 | 同上 |

---

## 🧩 关于 `me = world.ME`

这个项目用一个小机关，把「命名」这件事写进了代码和视觉里。

```python
# main.py
import world

me = world.ME
me.name = "me"       # ← 命名
world.execute(me);   # ← 执行
```

```python
# world.py
ME = SimpleNamespace(
    name="undefined",     # 一开始，我还没有名字
    color=DIM,            # 所以我是灰暗的
    ...
)

def execute(me):
    ...
    named = (me.name != "undefined")
    me.color = NEON if named else DIM
```

**没有名字的我，是灰暗的、不会发光的。**
只有 `main.py` 把 `"me"` 这个名字赋给它，世界才把光还给它。

这正好对应原曲的主题：AI 只有在被命名、被赋予存在意义之后，才真正「活着」。

---

## 🔧 参数调整

| 想改什么 | 改哪里 |
|---|---|
| 窗口尺寸 | `world.py` 顶部 `W, H = 1280, 720` |
| 帧率 | `FPS = 30`（卡的话调到 24 或 20） |
| 打字机速度 | `_typed_caption` 里的 `span * 0.75` |
| 歌词字体 | `font=("monospace", 18, "bold")` |
| 歌词位置 | `canvas.coords(cursor_id, 30 + width + 2, H - 30)` |
| 歌曲时长 | `DURATION = 212.0` |

---

## 🎨 技术实现

### 对象池渲染

Tkinter 的 Canvas 每次 `create_*` 都会分配新对象，60 FPS 下会瞬间卡死。所以：

- **启动时预创建** 1600 个椭圆 + 500 条线 + 80 个圆环
- **每帧只调用 `coords()` 和 `itemconfig()`** 更新已有对象
- **未使用的对象 `state="hidden"`**

这样每帧没有内存分配，只有坐标和属性的更新。

### 逐帧时间轴

每一帧的渲染都是**歌曲时间 `t` 的纯函数**：

```python
t = time.time() - start
dispatch(renderer, t, me, state)   # 根据 t 决定画什么
```

没有状态机、没有帧计数器、没有累积变量。这意味着：

- 音画**永远不会漂移**
- 拖慢帧率也不会跑偏
- 时间轴可以任意跳转

### 音乐同步

```python
player = subprocess.Popen(["mpv", "--no-video", path])
time.sleep(0.20)          # 等播放器启动
start = time.time()       # 这一刻定义为 t = 0
```

音乐和 MV 共用同一个 `start`，所以节拍、字幕、场景切换全部对齐。

---

## 📜 版权

### 原曲

**《world.execute(me);》由 Mili 创作。**
音乐版权归 Mili 所有。本项目**不包含**任何音频文件，请自行准备合法的音乐文件。

- 原曲：https://www.youtube.com/watch?v=ESx_hy1n7HA
- 乐队：https://mili.bandcamp.com

### 本项目代码

**GNU General Public License v2.0 (GPL-2.0)**

```
Copyright (C) 2026 <your-name>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
```

完整许可证文本见项目根目录的 [`LICENSE`](./LICENSE) 文件，或访问
<https://www.gnu.org/licenses/old-licenses/gpl-2.0.html>。

#### 这意味着什么

- ✅ 你可以**自由使用、修改、分发**这个项目
- ✅ 你可以把它用在**商业项目**里
- ⚠️ 如果你**分发**了修改后的版本（二进制或源码），必须：
  - **同样以 GPL v2 开源**，附上完整源代码
  - **保留原始版权声明和许可证**
  - **声明你做了哪些修改**
- ❌ **不能**把修改后的版本闭源后再分发
- ❌ **不能**附加任何额外限制（比如禁止商用、强制署名）

简单说：**你可以随便用，但只要往外发，就必须让下一个人也拥有同样的自由。**

本项目是**非商业性的粉丝创作**，与 Mili 无官方关联。

---

## 🙏 致谢

- **Mili** — 创作了这首让人无法忘记的歌
- **momocashew** — 歌词里的 Java 代码，是这一切的起点
- 所有把 `world.execute(me);` 用 Python、Rust、JavaScript 重写一遍的人

---

## 🌟 类似项目

如果你喜欢这种「用代码表达代码」的东西，也许你会喜欢：

- **`world.execute(me);` in Rust** — 终端像素 MV
- **`world.execute(me);` in JavaScript** — 网页版
- **Mili 官方 MV** — 原汁原味

---

*`world.execute(me);`*