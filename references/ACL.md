# ACL 论文插图工作指南

核对日期：2026-10-16。依据：官方 ACLPUB 持续更新的通用格式指南；具体年份、ARR／会议 track 仍需从其当年通知核实。

## 官方明确规范

[ACLPUB 的 Paper formatting guidelines](https://acl-org.github.io/ACLPUB/formatting.html)规定双栏 A4 版式：每栏 77 mm，栏间距 6 mm，通栏换算宽 160 mm。图表至少一栏宽，不做栏内文字绕排；允许跨双栏、合并子图。图注位于图下，10 pt Roman；单行居中、多行左齐，连续编号。

同一指南规定正文 11 pt；图内文字和数字应**尽可能**采用正文字号，打印时清楚可读。滥用图表小字号或间距可能导致直接拒稿。这里的 11 pt 是匹配正文的官方建议，不能误写成所有图中文字的独立强制最低值。

## 官方建议

同一指南建议优先 PDF／EPS 矢量格式，避免低分辨率或重压缩图，兼顾纸面与屏幕，并保持文件大小合理。灰度可读性受到强调，关键区分不能只依靠颜色。

[ACLPUB 终稿检查说明](https://acl-org.github.io/ACLPUB/final-version.html)还要求检查图表可读性、页面尺寸与字体嵌入。PDFLaTeX 工作流下用 PDF 导入，EPS 先转换，不将格式建议理解为任意编译器均直接接收 EPS。

## 本项目绘图实践

- 按最终约 11 pt 普通标签设计，从 77 mm 单栏或 160 mm 通栏开始构图。
- 内容过密时删去重复解释、拆分子图或重排，不优先缩字。
- 本次未确认独立的最小线宽数值；主线约 0.7–1.0 pt 是项目设计起点。
- 方法图中的 token、序列、模块输入输出及符号与正文一致，完整推导留给正文。
- 保留可编辑 SVG，排版用矢量 PDF，并提供灰度预览。

## 插入示例

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/method.pdf}
  \caption{Overview of the proposed method.}
  \label{fig:method}
\end{figure*}
```

单栏使用 figure 与 columnwidth。请让官方模板控制 caption，避免从其他会议照搬字体设置。

## 交付前检查

- [ ] 已核对当年 ACL／ARR／track 通知及其官方模板。
- [ ] 在 A4、真实插入尺寸下可读，标签尽可能匹配正文。
- [ ] 未靠小字号或异常间距塞入信息；图不越界、不绕排。
- [ ] 图注字号、位置及编号由模板控制。
- [ ] 图在灰度下有明确含义，矢量／嵌入字体检查通过。
- [ ] 坐标、单位、图例和子图标记与正文一致。

注意：ACLPUB 是通用来源，本文不冒称所有内容均为某个年份新增的 ACL 独立规则。
