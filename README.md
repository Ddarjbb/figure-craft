# FigureCraft

**Publication-focused scientific figures, with editable vectors and properly typeset mathematics.**

FigureCraft 是面向 Codex 等支持 `SKILL.md` 的 Agent 的科研绘图 skill，用于论文架构图、技术路线图、机制图、实验曲线和多子图。当前版本为 **v0.3.0**，随附 **2,405 个 SVG 参考资产**、可离线浏览的图库和逐图来源／许可清单。

它关注科学结构、最终论文尺寸下的可读性与可编辑矢量交付。绘制方式可按任务选择：直接 SVG/XML、Python、声明式图形语言或矢量编辑工具；需要数学公式时使用真实 LaTeX 或同等级排版引擎。

## 能做什么

- 按实际数据流表达输入、输出、分支、跳跃连接，以及训练与推理阶段。
- 为 U-Net、向量、矩阵、MLP 等对象使用可识别的结构示意。
- 论文原文出图时先确立科学主线和真实依赖；仅在参考图能直接帮助当前表达时检索和查看，观察学习与资产复用分别处理。
- 普通文字与公式默认黑色或深灰色，彩色文字承担明确的信息功能。
- 使用衬线数学字形排版公式、上下标和单独变量，保留公式源文件。
- 按目标插入尺寸设置字号、线宽和布局，依提示词选择交付格式。
- SVG 请求提供适合 PPT 编辑的 SVG、矢量 PDF 和 PNG；普通文字保持文本，公式展开引用并成形，模块按语义分组。
- 明确要求直接产出 PPT 时，提供可编辑文本、矢量形状及原生组合构成的 PPTX。
- 提供 ICML、ICLR、AAAI、CVPR、SIGIR、ACL、WWW 的独立参考指南，区分官方规则与设计实践。
- 检查 SVG/PDF 的位图、字体嵌入、页面尺寸和边界，默认检查最终彩色成图；按用户要求处理灰度交付。

用户明确指定的工具、字体、原创要求和交付格式优先。会议参考主要面向 2026 年，核对日期为 2026-10-16；更换年份、track 或投稿阶段时应复核官方模板。

## 交付范围

| 提示词 | 默认交付 |
|---|---|
| “提供 SVG”“能拖进 PPT 的 SVG”“SVG 在 PPT 中公式缺失” | PPT 友好的 SVG、PDF、PNG；不生成 PPTX |
| “直接生成 PPT”“提供原生 PPT/PPTX” | 原生 PPTX、PNG 预览 |
| 明确同时要 SVG 和 PPT | SVG、PDF、PNG、原生 PPTX |

“用于 PPT”不是“生成 PPTX”的同义词。源码、LaTeX、检查报告和中间变体默认只保留在工作目录；按用户要求再交付。实现要点见 [PPT 编辑与分组](references/POWERPOINT.md)。

## 安装

仓库根目录就是 skill 目录，入口为 [SKILL.md](SKILL.md)。

在 Codex 中可向内置 skill installer 提出：

```text
使用 skill-installer 从 https://github.com/Ddarjbb/figure-craft 安装 skill，
仓库内路径为 .，安装名为 figure-craft，版本为 v0.3.0。
```

也可手动将仓库克隆到用户级 skills 目录：

```text
git clone --branch v0.3.0 https://github.com/Ddarjbb/figure-craft.git ~/.codex/skills/figure-craft
```

Windows 默认目录为 `%USERPROFILE%\.codex\skills\figure-craft`。如果目标目录已经存在，先处理已有安装，再安装到该位置。安装完成后重启 Codex 或开启新会话，以重新发现 skill。

## 使用

```text
使用 $figure-craft，从零绘制一张 CVPR 风格的 DDPM 技术路线图。
采用跨双栏布局，交付适合 PPT 编辑的 SVG、矢量 PDF 和 PNG，工作目录保留 LaTeX 公式输入。
```

也可以用于修订：

```text
使用 $figure-craft，检查这张架构图的箭头关系、公式排版和最终尺寸可读性，
修复遮挡并导出矢量 PDF。
```

## 视觉惯例与论文转图

[视觉惯例与选择条件](references/VISUAL_CONVENTIONS.md)统一整理数据对象、网络模块、运算与参数状态、几何对象、时序与阶段关系。向量的单色长条、离散色块、连续数值色块、柱状表达与其他元素并列，按需要传达的信息选择。

根据论文文字绘制框架或技术路线图时，遵循 [text-to-figure](references/text-to-figure.md)：确定读者应理解的核心机制，核实对象与依赖，再分配视觉主次。

用户明确指定风格或要求使用风格库时，可读取[风格索引](references/styles/风格索引.md)，选择浅色作用域模块框架、开放对象机制或对齐叙事对照。未指定时根据研究内容独立构图。

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

### 本地参考图检索

```text
python scripts/search_figures.py 编码器 解码器 --kind svg --limit 6
python scripts/search_figures.py MLP projection --kind all --json
```

仅需 Python 标准库，默认直接检索随包的 [SVG 库](assets/svg-library/README.md)，可用浏览器打开 [gallery.html](assets/svg-library/gallery.html) 查看。也支持外部 SVG 库及可选论文裁剪图的 `agent_*/results.csv`，通过 `--library` / `--benchmark` 指定。检索按元数据词汇匹配，默认不以许可或位图状态过滤观察候选；需实际查看结果。详见[参考图检索与学习](references/REFERENCE_STUDY.md)与[视觉惯例](references/VISUAL_CONVENTIONS.md)。

用户明确要求匿名纯文字绘图、不得查看参考图时，跳过参考观察，独立提炼结构。普通文字默认灰黑、真实数学排版、矢量交付及最终尺寸检查仍然适用。

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
  assets/svg-library/          随包 SVG、离线 gallery、来源及许可
  references/                 通用规范、字体与各会议参考
  scripts/math_renderer.py     LaTeX 转矢量数学字形
  scripts/inspect_figure.py    SVG/PDF 结构与字体检查
  scripts/prepare_ppt_svg.py   保留文字、展开字形引用并合并公式
  scripts/search_figures.py   只读检索本地 SVG 与论文裁剪图
  requirements.txt            可选 Python 依赖
```

## 版本与许可

v0.1.0 基于此前本地使用的 research-figure 1.0.1 整理并改名发布，保留其绘图规则、会议参考和两个辅助脚本。版本号从首个公开发布重新计为 0.1.0。

代码和原创文档采用 [MIT License](LICENSE)。[随附图库](assets/svg-library/README.md)中的第三方资产分别采用 CC0、公有领域、MIT、Apache、CC BY 或 CC BY-SA 等许可；逐文件作者、来源、许可及原始链接见 [manifest.csv](assets/svg-library/manifest.csv)，通知与许可文本见 [THIRD_PARTY_NOTICES.md](assets/svg-library/THIRD_PARTY_NOTICES.md)。它们不统一改授为 MIT。指南中引用的会议模板、外部网页、字体和 TeX 包也遵循各自许可。

维护者可运行 `python -m unittest discover -s tests -v`，检查检索行为、路径发现、图库哈希及许可分档。
