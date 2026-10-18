# 参考图检索与学习

用于新建论文图或大幅重构布局。局部修订可沿用已有参考。先确定科学主线和必须表达的关系，再检索，避免参考图替代事实依据。用户明确要求只依据文字且不看参考图时跳过检索与观察，并继续执行科学与输出检查。

## 本地入口

附带 `scripts/search_figures.py` 只读检索，不修改图库，不下载或重新分发候选资产。默认发现：

- SVG 库：优先使用 skill 随附的 `assets/svg-library/manifest.csv`，无需另行配置；未附带图库时再查当前目录及其祖先目录下的 `svg-library/manifest.csv`，其次 `~/Documents/deepseek-harness/default-workspace/svg-library/manifest.csv`。
- 论文裁剪图：当前目录及其祖先目录下的 `cvpr2026_figure_benchmark/agent_batches/agent_*/results.csv`，其次 `~/Documents/ChatGPT/DDPM/cvpr2026_figure_benchmark/agent_batches`。
- 可用 `--library` / `--benchmark` 指定其他位置，或设置 `FIGURECRAFT_SVG_LIBRARY` / `FIGURECRAFT_BENCHMARK`；这些显式配置优先于默认发现。显式路径错误会报告失败；未发现某个默认库时仍可搜索另一个库。论文裁剪图索引是可选外部输入，不包含在发布包内。

以下命令以 skill 目录为工作目录；从其他目录运行时使用脚本的完整路径：

```text
python scripts/search_figures.py 编码器 解码器 --kind svg --limit 6
python scripts/search_figures.py MLP projection --kind all --limit 8 --json
python scripts/search_figures.py encoder decoder --kind benchmark --limit 4
python scripts/search_figures.py skip connection --library "C:/path/to/svg-library" --limit 6
python scripts/search_figures.py encoder --benchmark "C:/path/to/agent_batches" --kind benchmark
```

结果包括候选绝对路径、标题、匹配词、来源、许可及资产标记。匹配基于文件名、标题、分类、描述或 caption 的词汇，支持常用中英文扩展；它不是图像相似度或拓扑识别模型，不能由排序分数推断布局优劣。默认覆盖含位图和许可未明的观察候选，许可和矢量状态不参与相关性排序。`--vector-only` 或 `--tier` 仅在明确寻找待复用资产时按需指定；过滤结果不等于完成授权判断。

随附图库的 `manifest.csv` 保留逐文件来源、作者、许可与哈希；图库各自的许可不因 skill 的 MIT 许可而改变。复制或嵌入时核对候选实际许可和来源，不能把图库分档当作完整使用条件。

## 怎样找相似图

分别尝试对象词与关系词，而不是把整段需求当作一个关键词：

| 需要解决的问题 | 检索起点 |
|---|---|
| 编码／解码、压缩／重建 | encoder, decoder, autoencoder, VAE |
| MLP、投影头、分类头 | MLP, perceptron, projection, head |
| 多尺度与跳跃连接 | U-Net, UNet, skip connection, multiscale |
| 共享、双塔、并行分支 | shared, siamese, dual, branch, fusion |
| 特征图、向量与 token | feature map, tensor, embedding, token, patch |
| 训练阶段与局部机制 | training, stage, overview, detail, module |

先查看少量最相关候选，例如 2–4 张；这是工作起点，不是固定配额。没有相关结果时换同义词或查看对应分类；候选仍不足就记录并继续绘制，不无休止检索。图标候选只能帮助对象识别，不能替代方法图的结构参考。

## 怎样读参考

1. **查看渲染图。** 对 PNG 直接查看；对 SVG 使用可用的 SVG 渲染器或浏览器生成预览并查看。关注阅读顺序、主次层级、形状语义、分组、留白和连线，不只读检索摘要。
2. **按需读 SVG。** 只查看相关模块的分组、路径、变换、端口、线型与文字布局；大型转曲文件不必全量灌入上下文。裁剪图没有 SVG 时，只能据其外观学习，不声称读过源结构。
3. **决定如何采用。** 按本图科学对象、真实维度关系和最终尺寸重组。参考图的装饰、字体、彩色文字与细节仍须经过本 skill 的规则判断。

将简短记录保存在本图构建目录，例如：`来源路径／论文及图号；学到的表达；本图采用与调整；是否复制或改编资产及其许可处理`。仅观察通用表达与实际复用分开记录。参考图中的科学主张仍须由本任务资料核实。

视觉表达的选择条件见 [VISUAL_CONVENTIONS.md](VISUAL_CONVENTIONS.md)。
