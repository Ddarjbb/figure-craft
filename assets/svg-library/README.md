# FigureCraft SVG reference library

随 FigureCraft 提供 **2,405 个 SVG 资产**。使用浏览器打开 [gallery.html](gallery.html) 可离线按关键词、分类和许可档浏览；命令行在 skill 根目录运行 `python scripts/search_figures.py 编码器 解码器 --kind svg`。

[manifest.csv](manifest.csv) 保留每个文件的作者、来源、原始链接、许可、许可链接和 SHA-256。[第三方通知](THIRD_PARTY_NOTICES.md)与 [licenses](licenses/) 保留许可文本。第三方资产分别保留原许可，不统一采用 skill 的 MIT 许可。

| 许可档 | 数量 | 使用时核对 |
|---|---:|---|
| T1：CC0、公有领域、MIT、Apache 等 | 1367 | MIT/Apache 等仍需保留相关通知；不是所有 T1 都免除通知义务 |
| T2：CC BY | 609 | 按实际许可保留作者、来源与许可信息 |
| T3：CC BY-SA | 429 | 署名，并按实际版本处理改编的 ShareAlike 条件 |

观察构图与直接复用分别处理：检索默认不因许可档或位图状态排除参考；复制、改编或嵌入时核对逐文件条件。不要把重写 SVG 自动等同于独立创作。

所有资产按清单中的原始字节保留并校验哈希及 XML。SVG 不等于全矢量：其中 **155** 个文件含位图，**64** 个文件带外部引用标记；这些状态在清单和 gallery 中保留，离线渲染可能需要单独处理。

仅分发清单中的资产、来源、许可和浏览索引；不包含本机抓取缓存、第三方仓库克隆、字体缓存、论文裁剪图或实验记录。
