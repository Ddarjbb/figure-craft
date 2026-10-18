# ICLR 论文插图工作指南

核对日期：2026-10-16。版本依据：ICLR 2026 官方 Author Guide、LaTeX 源码及样式文件。范围：正文插图。

## 官方明确规范

[官方模板 Figures 节](https://github.com/ICLR/Master-Template/blob/master/iclr2026/iclr2026_conference.tex)要求图形整洁清晰、线条足够深，不使用手绘图；图号与 caption 放在图后，连续编号，图与图注不可分离。caption 使用句式大小写，保留专有名词所需大写。版式不可自行改变。

[官方样式文件](https://github.com/ICLR/Master-Template/blob/master/iclr2026/iclr2026_conference.sty)设置单栏版心宽 5.5 in，即 139.7 mm。不要把它视为 ICML／CVPR 的双栏版式。

本次核对未确认官方另设的统一图内字号或线宽数值下限。不能将 AAAI 的 9 pt、0.5 pt 自动称为 ICLR 要求。

## 官方建议

官方模板允许彩色，同时建议黑白打印时图注、正文与图意仍可理解；示例使用 graphicx，按 linewidth 的比例插图。[ICLR 2026 Author Guide](https://iclr.cc/Conferences/2026/AuthorGuide)给出该年份的模板入口，跨年应从新入口核实。

## 本项目绘图实践

- 按 139.7 mm 以内的实际宽度构图，先保证标签可读再安排模块数量。
- 可把较宽流程分成两行或上下两部分，并显式连接数据流；不将双栏横图机械缩到 80%。
- 普通标签约 10 pt、主连线约 0.7–1.0 pt 可作为设计起点；二者均为项目建议。
- 避免把黑白含义写成仅靠“蓝色／橙色”才能理解；增加模块名称和线型。
- 导出矢量 PDF 并保留编辑源文件，图像内不预写论文 Figure 编号。

## 插入示例

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/method.pdf}
  \caption{Overview of the proposed method.}
  \label{fig:method}
\end{figure}
```

单栏正常使用 figure；不要从双栏模板照搬 figure* 的布局逻辑。宽度也可以小于 linewidth，但必须重新核算字号。

## 交付前检查

- [ ] 已从目标年份 Author Guide 取得正确模板。
- [ ] 在单栏版心中完成编译与实际尺寸检查。
- [ ] 图注位于图下，句式大小写正确，编号由模板生成。
- [ ] 连线、箭头、上下标和标签在纸面上可辨认。
- [ ] 灰度下可理解，caption 不依赖纯颜色指称。
- [ ] 保留矢量 PDF 与可编辑源文件，检查字体与边界。

参见[通用执行流程](README.md)。本文件不设一个未经官方证实的“ICLR 最小字号”。
