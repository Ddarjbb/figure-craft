# SIGIR 论文插图工作指南

核对日期：2026-10-16。版本依据：SIGIR 2026 Full Papers、ACM 模板和图像无障碍资料。范围：Full Papers；其他 track 另查其通知。

## 会议明确规范

[SIGIR 2026 Full Papers 官方页面](https://sigir2026.org/en-AU/pages/submissions/full-papers-track)指定英文 PDF 和 ACM 双栏 sigconf 格式，并给出审稿稿类选项：

```latex
\documentclass[sigconf,natbib=true,anonymous=true]{acmart}
```

图必须适配该版式。不要将其他年份、其他 track 的类选项照搬到当前稿件。模板入口见[ACM Proceedings Template](https://www.acm.org/publications/proceedings-template)。

## 出版方建议与资料

[ACM 模板说明的 Preparing Graphics／Figures 节](https://authors.acm.org/binaries/content/assets/publications/taps/acm_layout_submission_template.pdf)偏好可缩放矢量格式，要求图文件嵌入字体；用标签、形状与线型补充颜色。

[SIGACCESS 图像描述指南](https://www.sigaccess.org/welcome-to-sigaccess/resources/describing-figures/)说明图像描述应传达不能直接看到图时所需的信息，不机械重复 caption。具体 figure description／Description 字段按目标 ACM 模板和生产要求提供。

本次未确认 SIGIR 单独设定的统一图内字号／线宽数值下限；不能把“9 pt／0.5 pt”写成 SIGIR 独立规定。图形可用宽度应从实际 acmart 版本读取，不硬编码 IEEE 栏宽。

## 本项目绘图实践

- 普通标签先按最终约 10 pt、主线约 0.7–1.0 pt 设计，再与真实正文、图注比较。
- 方法图交代 query／输入、关键处理、输出或排序目标；通用网络模块名称不能替代具体数据关系。
- 实验图同时使用颜色和线型／点型，直接标注或清楚解释指标与单位。
- 保留 SVG 等源文件，论文使用矢量 PDF；SVG 不作为默认的直接编译输入。
- 记录实际插入宽度，重新核算字号与线宽；用匿名素材与元数据准备审稿版。

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

Description 内容应针对实际图改写。普通单栏图改用 figure 与 columnwidth。

## 交付前检查

- [ ] 已确认年份、track、审稿／终稿类选项与实际模板尺寸。
- [ ] 普通标签及曲线标记在最终宽度下清楚，不依赖放大。
- [ ] PDF 字体嵌入与矢量状态已验证。
- [ ] 图意明确，图注和描述分别承担合适作用。
- [ ] 无越界、遮挡与匿名信息泄露。

取证说明：官方站点为 Next.js，本次网页正文解析为空；已读取官方 HTML 中序列化的 Full Papers 内容核实 sigconf 要求，未用其他会议替代。
