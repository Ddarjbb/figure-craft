# CVPR 论文插图工作指南

核对日期：2026-10-16。版本依据：CVPR 2026 官方作者指南及 cvpr-org/author-kit。范围：论文正文图，不是会议海报。

## 官方明确规范

[官方模板 Illustrations, graphs, and photographs 节](https://github.com/cvpr-org/author-kit/blob/main/sec/2_formatting.tex)要求图形居中；图中文字缩放后匹配正文字号，线宽适合印刷；读者不应必须放大才能看到要表达的关键细节。建议用 centering，避免 center 环境额外留白。

同一模板的 Color 节要求曲线区分不只靠颜色，增加线型、标记等第二种区分手段。

[cvpr.sty](https://github.com/cvpr-org/author-kit/blob/main/cvpr.sty)规定版心宽 6.875 in、栏间距 0.3125 in；换算总宽 174.625 mm、单栏约 83.344 mm。caption／subcaption 字体及格式交由该样式文件生成。

## 官方建议与未确认项

官方示例按 linewidth 比例插入 PDF。正文为 10 pt，可作为图中文字匹配的参照；没有将“所有图内文字统一 9 pt”写成通用标准。本次也未确认 CVPR 独立规定的统一 0.5 pt 最小线宽或“必须只用某一种绘图字体”的规则。

稿件要求从[2026 Author Guidelines](https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines)进入核对。仓库 main 分支持续变化，跨年使用时应查对应版本。

## 本项目绘图实践

- 普通标签按最终约 10 pt 设计，主线约 0.7–1.0 pt；这些数值起点不是新增的会议强制阈值。
- 方法图先呈现输入、关键处理、输出及必要训练回路；减少装饰性卡片和重复文字。
- 可用 (a)、(b) 等组织子图，正文符号与图内符号一致。
- 原生矢量 SVG 保留文字编辑能力；排版导出矢量 PDF，检查嵌入字体或路径。
- 只用少量颜色表达功能分类，同时用标签／边框／线型明确对象身份。

## 插入示例

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/method.pdf}
  \caption{Overview of the proposed method.}
  \label{fig:method}
\end{figure*}
```

只占一栏时使用 figure 与 columnwidth，并重排内容，避免将跨栏图直接缩小。

## 交付前检查

- [ ] 已使用目标年份官方模板，未改变页边距或栏宽。
- [ ] 普通标签与正文大小协调，实际打印尺寸可读。
- [ ] 线型、箭头及数学上下标可辨认，关键细节不依赖放大。
- [ ] 彩色之外有标签、线型或标记等第二种区分方式。
- [ ] 子图标记和正文引用一致，caption 由模板控制。
- [ ] PDF 矢量、字体、边界框以及模板内实际位置已检查。
