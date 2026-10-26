# 公式与混合字体排版规范

日期：2026-10-16。依据：用户对本项目科研插图的明确要求。本文件是项目执行规则，不声称各会议强制使用同一种排版引擎或字体。

## 字体角色

| 内容 | 本项目默认选择 | 要求 |
|---|---|---|
| 模块名称、普通说明、图例 | 原图的 Arial 或 DejaVu Sans | 同层级一致，最终尺寸可读 |
| 子图标题 | Times New Roman Bold | 使用真正的 Times New Roman 字体，控制字重和层次 |
| 数学变量、算子、公式 | LaTeX NewTX Math，或同等级衬线数学字体 | 必须由 LaTeX／MathJax 等引擎处理数学语义 |

Times New Roman 与完整数学字体有不同职责。公式不得仅将原有普通字符串的 font-family 改成 Times New Roman；上下标、帽号、伸缩括号、求和和范数应由数学排版引擎生成。单独出现的数学变量也遵守此规则。自然语言中的数字和子图编号可继续使用普通文本。

## 输出与留存

用户指定的[风格文档](styles/风格索引.md)或直接字体要求可以为普通标签与标题选择不同字体；上表是未作选择时的回退值。未指定风格时不为选字体而打开风格索引。绘制时为对应标签显式设置所选 font-family，不因辅助工具的默认字体而忽略风格要求。实际缺少字体时记录替换字体并复查字宽，数学字体与引擎的要求不变。

1. 在源码中用 LaTeX 记录数学内容，例如 `F'_{c,h,w}=\gamma_c(q)\,F_{c,h,w}+\beta_c(q)`。
2. 由 LaTeX 或 MathJax 导出矢量字形，并与图稿组合，不使用公式截图。
3. 同时保留公式 `.tex`、表达式清单、SVG、嵌入普通字体的 PDF 和生成脚本。转路径后的公式从 `.tex` 或表达式清单修改，普通标签仍可在 SVG 中编辑。
4. 检查最终尺寸下的基线、字距、上下标、溢出、裁切和线条遮挡，必要时重排。

## 公式渲染辅助工具

随包提供 [math_renderer.py](../scripts/math_renderer.py)。它通过真实 pdfLaTeX / NewTX Math 编译公式，再以 PyMuPDF 提取矢量字形；普通标签保留为 SVG 文本，数学部分为路径。输出的普通文本字体需在后续 SVG 转 PDF 时嵌入。

在 skill 根目录安装 Python 依赖，并确保 `pdflatex` 可从 PATH 调用。TeX 发行版需包含 `standalone`、`amsmath`、`amssymb`、`newtxtext` 和 `newtxmath`；它们及字体不包含在 Python 依赖或发布包中。

```bash
python -m pip install -r requirements.txt
python scripts/math_renderer.py --demo --output-dir math_demo
```

在绘图脚本中，将 skill 的 `scripts` 目录加入 Python 模块搜索路径，或将该辅助脚本随可复现图稿一起交付，然后调用：

```python
from pathlib import Path
from math_renderer import Typography

out = Path("figure_output")
typography = Typography(out, sans="DejaVu Sans")
label = typography.label(30, 55, r"User vector: $\mathbf{z}_u\in\mathbb{R}^{d}$", size=18)
source = '<svg xmlns="http://www.w3.org/2000/svg" width="100mm" height="30mm" viewBox="0 0 300 90">' + label + '</svg>'
(out / "figure.svg").write_text(typography.resolve(source), encoding="utf-8")
```

`label()` 返回占位符，`resolve()` 批量替换占位符并导出 `math_source/` 与 `label_layout.json`。坐标和字号采用 SVG viewBox 单位，按最终插入尺寸核算实际字号；标签的纵坐标为基线。数学表达式用单个 `$...$` 包裹，支持与普通文字交替；需要较大分式时在表达式内使用 `\displaystyle`。普通文本中的字面 `$` 及跨行公式不在该轻量接口的支持范围内。

普通标签通过系统字体发现机制选择字体；缺失字体时回退到 DejaVu Sans，Times New Roman 则回退到 DejaVu Serif，并在布局记录中报告实际字体。中文标签应显式指定已安装且覆盖相应字形的中文字体，回退字体不保证中文覆盖。公式仍使用 NewTX Math。`(a)`–`(c)` 开头的子图标题默认请求 Times New Roman；需要其他标题字体时可修改返回占位符对应的 `typography.labels` 字体配置。

该脚本提供公式与混排 SVG 输出，不负责整图布局、PDF 转换或碰撞检查。缺少 TeX 或编译失败时报告错误，不把普通文字或截图作为公式替代。`math_source/equations.pdf` 为公式页集合，不是整图 PDF；最终整图仍需按指南导出和检查。

## 工具依据

- [MathJax 官方输出格式文档](https://docs.mathjax.org/en/stable/output/index.html)：支持 SVG 等输出。
- [CTAN NewTX](https://www.ctan.org/pkg/newtx)：提供独立的文本与数学字体包。

选择字体和引擎不能替代目标会议模板核验；实际字体大小、版心和提交文件类型仍按目标模板检查。
