# WWW / The Web Conference 论文插图工作指南

核对日期：2026-10-16。版本依据：The Web Conference 2026 Research Tracks 与 ACM 出版资料。范围：Research Tracks；其他 track 单独核对。

## 会议明确规范

[2026 Research Tracks 官方指南](https://www2026.thewebconf.org/calls/research-tracks.html)要求英文、ACM 双栏格式，推荐的审稿稿设置为：

```latex
\documentclass[sigconf,anonymous,review]{acmart}
```

提交整篇 PDF；录用后按 ACM 终稿生产要求修订。图必须适配指定模板且可正常显示与打印，不得侵入页边或栏间空白。模板与格式入口见[ACM Proceedings Template](https://www.acm.org/publications/proceedings-template)。

## 出版方建议与资料

[ACM 模板的图形准备说明](https://authors.acm.org/binaries/content/assets/publications/taps/acm_layout_submission_template.pdf)偏好可缩放矢量、要求嵌入图中文字字体，强调灰度可读，并建议结合形状、标签或线型表达差异。

[SIGACCESS 描述指南](https://www.sigaccess.org/welcome-to-sigaccess/resources/describing-figures/)用于准备不与 caption 简单重复的图像描述。具体 Description 字段与可访问性产物按所用 ACM 模板及生产流程检查。

本次未确认 WWW 独立规定的统一图内字号或最小线宽；不要把 IEEE 或 AAAI 的数值直接套作 WWW 明文规定。版心尺寸从本年、本阶段的 acmart 模板读取。

## 本项目绘图实践

- 以最终约 10 pt 普通标签、0.7–1.0 pt 主线为起始值；这些是本项目建议，需经过实际排版检查。
- 方法图交代用户／query／网页／图结构等实际输入、模型处理和输出，避免大量模块框却没有清楚关系。
- 颜色按功能赋义，标签和连线独立传达图意；保留灰度版本。
- SVG 保存编辑对象与布局；LaTeX 使用导出的矢量 PDF。
- 模板改变尺寸后，重新检查字号、数学上下标、曲线标记与线宽，不仅检查图片是否越界。

## 插入示例

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/method.pdf}
  \caption{Overview of the proposed method.}
  \Description{A concise description of the essential visual information.}
  \label{fig:method}
\end{figure*}
```

Description 必须根据实际图编写，不能把示例占位文字作为最终描述。单栏图使用 figure 与 columnwidth。

## 交付前检查

- [ ] 已确认目标年份、Research Track／其他 track 及审稿／终稿阶段。
- [ ] acmart 选项和实际版心正确，字体与图内符号在原尺寸可读。
- [ ] PDF 字体已嵌入，方法图保持矢量，无错误边界与遮挡。
- [ ] 灰度区分有效，caption、图像描述和正文引用一致。
- [ ] 审稿稿无识别作者的信息，最终稿按 ACM 生产流程复核。

不要以某个 WWW workshop 的独立要求替代 Research Tracks 正式指南。
