# AAAI 论文插图工作指南

核对日期：2026-10-16。版本依据：AAAI-26 投稿说明和 AAAI Press 2026 模板。范围：正文图；具体 track 通知优先于通用 Press 指南。

## 官方明确规范

[AAAI-26 投稿说明](https://aaai.org/conference/aaai/aaai-26/submission-instructions/)指定 AAAI 双栏样式。下列细节见[AAAI 发布的 2026 模板](https://www.overleaf.com/latex/templates/aaai-2026-press-formatting-instructions-for-authors-using-latex/qnpmwrzmddjj)中 Illustrations and Figures、Using Color、Drawings 和 Fonts in Your Illustrations：

- 图内标签至少 9 pt；caption 在图下，10 pt Roman，不整体加粗或斜体。
- 连线至少 0.5 pt；标注字体使用 Times Roman 或 Helvetica。
- PDFLaTeX 使用 PDF／PNG／JPG，PS／EPS 需预先转换；字体须嵌入，禁止 Type-3。
- 彩色仅限图内，使用 CMYK，满足指南给出的对比度高于 4.5:1；灰度下仍能理解。
- 裁切在绘图工具中完成，不用 includegraphics 的 trim／clip；不使用 minipage 分组插图。

## 官方建议与尺寸换算

同一模板建议避免带阴影底色的文字，保持线宽一致，并优先考虑黑白／灰度输出。栅格图在最终尺寸下约 300 dpi；这一要求不应套到纯矢量路径上。

模板为 Letter，左右各 0.75 in，换算可用总宽约 177.8 mm。此为版心换算，不是每张图的固定宽度；实际值以官方模板编译为准。

## 本项目绘图实践

- 原生矢量图先做白底、黑字、清晰轮廓的版本，再决定是否需要 CMYK 色彩。
- 普通标签以 10 pt 为起点，为插入缩放留余量；实际标签不得落到官方下限以下。
- RGB PDF 不能仅靠改文件名宣称为 CMYK；检查 PDF 实际色彩空间。
- 对复杂分图先在绘图阶段组合并裁切，输出一个边界正确的 PDF。

## 插入示例

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/method.pdf}
  \caption{Overview of the proposed method.}
  \label{fig:method}
\end{figure*}
```

单栏改用 figure 与 columnwidth；不手工改 caption 字体、压间距或添加 clip／trim。

## 交付前检查

- [ ] 已核对本年、本 track 的 author kit，未擅改模板。
- [ ] 最终图内普通文字至少 9 pt，线条至少 0.5 pt。
- [ ] caption 为模板控制的 10 pt Roman，位置正确。
- [ ] 字体已嵌入，无 Type-3；原始 PDF 裁切及边界框正确。
- [ ] 使用 CMYK 彩色或灰度，检查颜色对比及黑白可辨识性。
- [ ] 所有图文件能被 PDFLaTeX 直接读取。

来源说明：AAAI 主站 author kit 在本次访问中返回 403；使用署名 AAAI、明确注明来源为官方 author kit 的 Overleaf 页面核对内容。跨年／终稿必须重新核实。
