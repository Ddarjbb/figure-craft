# 图库样例与留出验证

来源为指定图库的本地快照：`538355a3fdd4d4475e00fe48adbbae54a890a6c5`，权威清单 `data/figures.json` 含 3,449 张图。图库只读，原图片未复制进 skill。完整题名、作者、原论文、外部图片路径、哈希和观察记录见 [evidence.json](evidence.json)。

## 方法与结论边界

- 在六个会议中按固定随机种子各取 6 张，共 36 张提炼候选；按同类元数据另取 36 张、与提炼组题名无重叠的留出候选。候选类别限定为 architecture/pipeline/conceptual/comparison，不能视为全图库的代表性抽样。
- 提炼组看完后，先固定三个家族各三项判定特征，再查看留出组。全部 72 张通过彩色联系表实际查看；关键样例另打开原分辨率图复核。
- 每个家族列出三张提炼主例、三张独立留出主例和一个边界反例。其余留出图有筛选备注；不把所有候选强行归类，不报告伪精确通过率。
- 留出主例在三项特征上均能找到对应视觉证据。反例表明家族有适用条件；只支持在多篇论文中重复成立，不能声称普遍适用于全部方法图。
- 这是同一观察者的定性论文间核对，不是独立评审者盲测或统计 k-fold CV。主验证例是查看整组后的解释性样例，不能用于估计全图库比例。
- 具体字体文件、原始pt字号及作者矢量HEX无法从JPEG可靠推断；风格文档的数值是实现建议。JPEG量化色仅作近似调色参考。

## 固定的家族判定特征

### p1
**P1 浅色作用域模块框架**

- At least two named operational groups use pale bounded scopes or outline panels.
- Groups contain recognizable local structures or a locally connected chain, beyond names alone.
- Directed relations connect groups; grouping makes module responsibility legible.

| 分组 | 图与论文来源 | 观察 |
|---|---|---|
| 提炼主例 | D04 [BSDB-Net: Band-Split Dual-Branch Network with Selective State Spaces Mechanism for Monaural Speech Enhancement](https://ojs.aaai.org/index.php/AAAI/article/view/34557) — AAAI 2025 | 两条浅底作用域内有局部模块和交互，暗色有向流连接。 |
| 提炼主例 | D14 [Guiding Diffusion Models with Fine-Grained Conditions and Semantics-Preserving Sampling for One-Shot Federated Learning](https://openaccess.thecvf.com/content/CVPR2026/html/Deng_Guiding_Diffusion_Models_with_Fine-Grained_Conditions_and_Semantics-Preserving_Sampling_for_CVPR_2026_paper.html) — CVPR 2026 | 客户端与服务器职责分区，组内有结构对象，跨组方向明确。 |
| 提炼主例 | D23 [Multi-resolution HuBERT: Multi-resolution Speech Self-Supervised Learning with Masked Unit Prediction](https://openreview.net/forum?id=kUuKFW7DIF) — ICLR 2024 | 一整体作用域内分出多分辨率层级与预测分支，局部轮廓不等权。 |
| 独立留出主例 | H07 [OZS peech: One-step Zero-shot Speech Synthesis with Learned-Prior-Conditioned Flow Matching](https://aclanthology.org/2025.acl-long.1043/) — ACL 2025 | 浅蓝与浅米范围组织编码、先验和合成；范围内有token与投影结构。 |
| 独立留出主例 | H18 [Theory-Inspired Deep Multi-View Multi-Label Learning with Incomplete Views and Noisy Labels](https://openaccess.thecvf.com/content/CVPR2025/html/Li_Theory-Inspired_Deep_Multi-View_Multi-Label_Learning_with_Incomplete_Views_and_Noisy_CVPR_2025_paper.html) — CVPR 2025 | 多职责浅色分区，组内矩阵／模型与跨区域有向关系明确。 |
| 独立留出主例 | H36 [SpGesture: Source-Free Domain-adaptive sEMG-based Gesture Recognition with Jaccard Attentive Spiking Neural Network](https://proceedings.neurips.cc/paper_files/paper/2024/hash/409334f42cbb57d07aa152f2d0433ec7-Abstract-Conference.html) — NEURIPS 2024 | 灰蓝轮廓范围嵌套神经元／卷积结构，连通主流与反馈记忆；支持中性底而非强制多彩大面板。 |
| 边界反例 | H24 [Retrieval-based Controllable Molecule Generation](https://openreview.net/forum?id=vDFA1tpuLvk) — ICLR 2023 | 边界反例：虽有矩形与数据库，主线是开放的检索—融合对象链，缺少多职责作用域组织；不符合第一条件。 |

### p2
**P2 开放对象机制**

- Central scientific objects have intrinsic structure such as token cells, graphs, code or node lattices.
- Transformation or correspondence is conveyed through object arrangement and local arrows.
- The key mechanism sits on an open or neutral background rather than a dominant collection of colored panels.

| 分组 | 图与论文来源 | 观察 |
|---|---|---|
| 提炼主例 | D26 [Graph Generation with Diffusion Mixture](https://proceedings.mlr.press/v235/jo24b.html) — ICML 2024 | 图拓扑与预测对象直接成形，局部算子和箭头表现变换。 |
| 提炼主例 | D27 [Exploiting Code Symmetries for Learning Program Semantics](https://proceedings.mlr.press/v235/pei24b.html) — ICML 2024 | 代码行、token单元与对应映射形成主线，背景开放。 |
| 提炼主例 | D34 [Understanding the Expressivity and Trainability of Fourier Neural Operator: A Mean-Field Perspective](https://proceedings.neurips.cc/paper_files/paper/2024/hash/14da7aea05debb963b3d8d46449d51a0-Abstract-Conference.html) — NEURIPS 2024 | 网络格点前后变化直接表达相位差异，局部箭头与对象位置承担关系。 |
| 独立留出主例 | H13 [X-Pruner: eXplainable Pruning for Vision Transformers](https://openaccess.thecvf.com/content/CVPR2023/html/Yu_X-Pruner_eXplainable_Pruning_for_Vision_Transformers_CVPR_2023_paper.html) — CVPR 2023 | 矩阵、权重层和剪枝对象直接成形；白底线框只作局部分隔。 |
| 独立留出主例 | H28 [SHE: Streaming-media Hashing Retrieval](https://proceedings.mlr.press/v267/pu25b.html) — ICML 2025 | 哈希码、图节点和原型沿多模态对象链变化；大部分主体保持开放背景。 |
| 独立留出主例 | H35 [Energy-based Epistemic Uncertainty for Graph Neural Networks](https://proceedings.neurips.cc/paper_files/paper/2024/hash/3cd50f2922b7adaaa9e5113e35bae095-Abstract-Conference.html) — NEURIPS 2024 | 图对象与扩散前后节点状态组织机制；局部算子范围不替代对象主线。 |
| 边界反例 | H10 [Before Generation, Align it! A Novel and Effective Strategy for Mitigating Hallucinations in Text-to- SQL Generation](https://aclanthology.org/2024.findings-acl.324/) — ACL 2024 | 边界反例：SQL文本出现不等于对象机制风格；主体靠文字阶段块叙事，不符合开放机制背景条件。 |

### p3
**P3 对齐叙事对照**

- At least two comparable conditions, states or methods are shown in parallel rows or columns.
- Corresponding objects or operations repeat in aligned positions with consistent geometry.
- A local change in links, state or marks explains the difference; the comparison is more than unrelated panels.

| 分组 | 图与论文来源 | 观察 |
|---|---|---|
| 提炼主例 | D07 [TADA : Efficient Task-Agnostic Domain Adaptation for Transformers](https://aclanthology.org/2023.findings-acl.31/) — ACL 2023 | 预训练与微调并列，共同Transformer与token结构提供比较锚点。 |
| 提炼主例 | D22 [UniCon: Unidirectional Information Flow for Effective Control of Large-Scale Diffusion Models](https://openreview.net/forum?id=uJqKf24HGN) — ICLR 2025 | ControlNet与UniCon对应层对齐，局部梯度路径区别突出。 |
| 提炼主例 | D35 [Discrete Spatial Diffusion: Intensity-Preserving Diffusion Modeling](https://openreview.net/forum?id=kz3w2A2y0e) — NEURIPS 2025 | 相邻状态共享几何基元，局部差异与排列解释状态演变。 |
| 独立留出主例 | H12 [Modular Sentence Encoders: Separating Language Specialization from Cross-Lingual Alignment](https://aclanthology.org/2025.acl-long.108/) — ACL 2025 | 语言适配与编码训练保留相应块几何，局部适配器位置与组合形成区别。 |
| 独立留出主例 | H17 [CVT-SLR: Contrastive Visual-Textual Transformation for Sign Language Recognition With Variational Alignment](https://openaccess.thecvf.com/content/CVPR2023/html/Zheng_CVT-SLR_Contrastive_Visual-Textual_Transformation_for_Sign_Language_Recognition_With_Variational_CVPR_2023_paper.html) — CVPR 2023 | 两行共享视频—特征—输出路径，对齐模块揭示不同对齐方法。 |
| 独立留出主例 | H25 [Towards Interpretable Deep Local Learning with Successive Gradient Reconciliation](https://proceedings.mlr.press/v235/yang24m.html) — ICML 2024 | 表格三行对齐相同网络层，梯度连线局部改变明确。 |
| 边界反例 | H36 [SpGesture: Source-Free Domain-adaptive sEMG-based Gesture Recognition with Jaccard Attentive Spiking Neural Network](https://proceedings.neurips.cc/paper_files/paper/2024/hash/409334f42cbb57d07aa152f2d0433ec7-Abstract-Conference.html) — NEURIPS 2024 | 边界反例：主链加记忆反馈没有平行比较条件；不满足第一条件，不能凭空添加对照。 |

## 其余留出候选的筛选记录

| 编号 | 图 ID | 观察与适用边界 |
|---|---|---|
| H01 | `aaai2026-37714` | 多色阶段范围与局部步骤，适合P1；插画较多，不能推广其字体。 |
| H02 | `aaai2026-37094` | 嵌套职责范围和局部层结构，P1候选；混合局部展开。 |
| H03 | `aaai2024-28483` | 轮廓分组与对象图结构混合，P1/P2候选。 |
| H04 | `aaai2025-32491` | U形架构及局部模块展开，P1候选；不强迫归为开放对象轨迹。 |
| H05 | `aaai2025-32367` | 阶段范围、点云和局部场景对象混合，P1候选。 |
| H06 | `aaai2025-34083` | 命名范围内有节点、网格与处理链，P1/P2混合候选。 |
| H07 | `acl2025-2025.acl-long.1043` | P1主验证例：浅底职责范围、结构对象和组间箭头。 |
| H08 | `acl2023-2023.findings-acl.617` | 对比学习的对象阵列与局部容器混合；不作为纯风格主验证例。 |
| H09 | `acl2023-2023.acl-long.849` | 训练和推理并列，重复PLM与插件块；P3候选并含范围。 |
| H10 | `acl2024-2024.findings-acl.324` | P2边界反例；虽含SQL文本，但主要是阶段叙事块。 |
| H11 | `acl2025-2025.acl-long.1186` | 图结构、trie与文字上下文混合；开放对象关系可借鉴，密度不可作为默认。 |
| H12 | `acl2025-2025.acl-long.108` | P3主验证例：对应Transformer块与适配器的局部差异。 |
| H13 | `cvpr2023-Yu_X-Pruner_eXplainable_Pruning_for_Vision_Transformers_CVPR_2023_paper` | P2主验证例：矩阵、权重层与剪枝对象，局部线框。 |
| H14 | `cvpr2026-Luo_Self-Corrected_Image_Generation_with_Explainable_Latent_Rewards_CVPR_2026_paper` | 定性生成样例与结果图，只有对齐排版可借鉴，不作为框架风格主证据。 |
| H15 | `cvpr2025-He_Generalized_Diffusion_Detector_Mining_Robust_Features_from_Diffusion_Models_for_CVPR_2025_paper` | 数据域样例和雷达图为主，三种方法图家族均不能直接套用。 |
| H16 | `cvpr2026-Fan_SMVRT_Implicit_Human_3D_Modeling_Using_Sparse_Multi-View_Volumetric_Reconstruction_CVPR_2026_paper` | 多模态实体、体素和架构并存；局部可迁移，混合而非纯家族。 |
| H17 | `cvpr2023-Zheng_CVT-SLR_Contrastive_Visual-Textual_Transformation_for_Sign_Language_Recognition_With_Variational_CVPR_2023_paper` | P3主验证例：两行对应的处理链，局部结构变化。 |
| H18 | `cvpr2025-Li_Theory-Inspired_Deep_Multi-View_Multi-Label_Learning_with_Incomplete_Views_and_Noisy_CVPR_2025_paper` | P1主验证例：职责作用域中的矩阵、层级与有向流。 |
| H19 | `iclr2025-3147` | 设备范围与路由层重复，P1候选；设备并列不自动构成方法优劣对比。 |
| H20 | `iclr2026-1474` | 对齐问答示例与结果混排；可借鉴叙事比较，但不是架构主验证例。 |
| H21 | `iclr2026-0201` | 定性特征图和时序证据为主，开放对象部分可参考，不能移植其数据颜色语义。 |
| H22 | `iclr2025-1881` | 多基线小图与主方法展开混合；局部比较可参考，不作为单一家族主例。 |
| H23 | `iclr2026-0122` | Token主架构和局部放大混合；不能推出所有开放对象图都需要插图窗。 |
| H24 | `iclr2023-0499` | P1边界反例：开放检索与融合链，小模块不构成多作用域框架。 |
| H25 | `icml2024-2526` | P3主验证例：对齐网络层和局部梯度流差异，表格线稿也成立。 |
| H26 | `icml2025-0918` | 两类蒸馏方法并列、对象重复，P3候选。 |
| H27 | `icml2023-0027` | 分类与生成攻击对照但几何层级不同；属于部分可迁移对照。 |
| H28 | `icml2025-1368` | P2主验证例：哈希、原型与图对象的连续映射；也含多模态对齐。 |
| H29 | `icml2026-0052` | 理论阶段说明和曲线为主，不作为模块框架或对象机制主验证例。 |
| H30 | `icml2026-0129` | 单一雷达结果图；三种框架风格的共同非适用例。 |
| H31 | `neurips2023-0715` | 局部／全局对象结构和双向交互混合，可借鉴P2但无需复制图片高亮。 |
| H32 | `neurips2025-2371` | 教师与学生训练作用域及局部网络，P1候选；阶段职责而非直接同条件对照。 |
| H33 | `neurips2025-2787` | 奖励曲面、行列对齐与范围分组混合；不把曲面或渐变作为方法图通用规则。 |
| H34 | `neurips2023-0559` | 特征图墙与硬件概念并列，只有局部对齐可迁移，不作为主验证例。 |
| H35 | `neurips2024-3036` | P2主验证例：图对象变化、局部操作与开放路径。 |
| H36 | `neurips2024-4170` | P1主验证例，同时为P3边界反例：单一路径和反馈而非平行对照。 |

## 可复核性与使用

原图库中的 `image` 相对路径、论文链接与 SHA256 已写入 evidence.json。联系表及提炼／留出清单保存在本次工作区的 `outputs/gallery_style_study_20261019/`，不是技能执行的前置依赖。使用者只需在明确指定风格时读取对应风格文档；无需复看这些样例。

提炼的是通用组织方式，没有改写原作者的研究主张，也没有复制图中模块、图标或数据作为新资产。图库代码许可不代表所有原论文图片的许可。
