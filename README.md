# FigureCraft

**Publication-focused scientific figures, with editable vectors and properly typeset mathematics.**

FigureCraft 是面向 Codex 等支持 `SKILL.md` 的 Agent 的科研绘图 skill，用于论文架构图、技术路线图、机制图、实验曲线和多子图。首个公开版本为 **v0.1.0**。

它关注科学结构、最终论文尺寸下的可读性与可编辑矢量交付。绘制方式可按任务选择：直接 SVG/XML、Python、声明式图形语言或矢量编辑工具；需要数学公式时使用真实 LaTeX 或同等级排版引擎。

## 能做什么

- 按实际数据流表达输入、输出、分支、跳跃连接，以及训练与推理阶段。
- 为 U-Net、向量、矩阵、MLP 等对象使用可识别的结构示意。
- 使用衬线数学字形排版公式、上下标和单独变量，保留公式源文件。
- 按目标插入尺寸设置字号、线宽和布局，提供 SVG、矢量 PDF 和预览。
- 提供 ICML、ICLR、AAAI、CVPR、SIGIR、ACL、WWW 的独立参考指南，区分官方规则与设计实践。
- 检查 SVG/PDF 的位图、字体嵌入、页面尺寸和边界，生成彩色与灰度预览。

用户明确指定的工具、字体、原创要求和交付格式优先。会议参考主要面向 2026 年，核对日期为 2026-10-16；更换年份、track 或投稿阶段时应复核官方模板。

## 安装

仓库根目录就是 skill 目录，入口为 [SKILL.md](SKILL.md)。

在 Codex 中可向内置 skill installer 提出：

```text
使用 skill-installer 从 https://github.com/Ddarjbb/figure-craft 安装 skill，
仓库内路径为 .，安装名为 figure-craft，版本为 v0.1.0。
```

也可手动将仓库克隆到用户级 skills 目录：

```text
git clone --branch v0.1.0 https://github.com/Ddarjbb/figure-craft.git ~/.codex/skills/figure-craft
```

Windows 默认目录为 `%USERPROFILE%\.codex\skills\figure-craft`。如果目标目录已经存在，先处理已有安装，再安装到该位置。安装完成后重启 Codex 或开启新会话，以重新发现 skill。

## 使用

```text
使用 $figure-craft，从零绘制一张 CVPR 风格的 DDPM 技术路线图。
采用跨双栏布局，交付可编辑 SVG、矢量 PDF 和预览，保留 LaTeX 公式输入。
```

也可以用于修订：

```text
使用 $figure-craft，检查这张架构图的箭头关系、公式排版和最终尺寸可读性，
修复遮挡并导出矢量 PDF。
```

## 可选工具

仅阅读和遵循绘图指南不需要安装 Python 依赖。使用附带脚本时安装：

```text
python -m pip install -r requirements.txt
```

### SVG / PDF 检查

```text
python scripts/inspect_figure.py --svg figure.svg --pdf figure.pdf --require-vector --output check.json
```

检查覆盖结构证据，不能替代对科学语义、连线关系和实际阅读效果的目视判断。

### LaTeX 数学字形

```text
python scripts/math_renderer.py --demo --output-dir math_demo
```

数学渲染另需 PATH 中的 `pdflatex`，以及 TeX 发行版中的 `standalone`、`amsmath`、`amssymb`、`newtxtext` 和 `newtxmath`。这些 TeX 包和字体不随本仓库分发。详细说明见 [公式与字体指南](references/TYPOGRAPHY.md)。

## 文件结构

```text
figure-craft/
  SKILL.md                     Agent 工作指南
  agents/openai.yaml           Codex 展示名称与调用信息
  references/                 通用规范、字体与各会议参考
  scripts/math_renderer.py     LaTeX 转矢量数学字形
  scripts/inspect_figure.py    SVG/PDF 结构与字体检查
  requirements.txt            可选 Python 依赖
```

## 版本与许可

v0.1.0 基于此前本地使用的 research-figure 1.0.1 整理并改名发布，保留其绘图规则、会议参考和两个辅助脚本。版本号从首个公开发布重新计为 0.1.0。

代码和原创文档采用 [MIT License](LICENSE)。指南中引用的会议模板、外部网页、字体和 TeX 包遵循各自的许可，不因本仓库许可而改变。
