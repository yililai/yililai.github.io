# SOLO 系列核验记录

核验日期：2026-10-24。所有实验数值均为作者论文报告，未在本项目复现。

| 条目 | SOLO | SOLOv2 |
|---|---|---|
| 正式标题 | SOLO: Segmenting Objects by Locations | SOLOv2: Dynamic and Fast Instance Segmentation |
| 状态 | 正式发表，ECCV 2020 | 正式发表，NeurIPS 2020，NeurIPS 33 |
| 作者 | Xinlong Wang, Tao Kong, Chunhua Shen, Yuning Jiang, Lei Li | Xinlong Wang, Rufeng Zhang, Tao Kong, Lei Li, Chunhua Shen |
| 预印本首发 | 2019-12-10，arXiv:1912.04488 | 2020-03-23，arXiv:2003.10152 |
| 正式记录 | https://doi.org/10.1007/978-3-030-58523-5_38 | https://proceedings.neurips.cc/paper/2020/hash/cd3afef9b8b89558cd56638c3631868a-Abstract.html |
| 核验全文 | https://lileicc.github.io/pubs/wang2020solo.pdf | https://proceedings.neurips.cc/paper/2020/file/cd3afef9b8b89558cd56638c3631868a-Paper.pdf |
| 官方代码 | https://github.com/WXinlong/SOLO | https://github.com/WXinlong/SOLO；另有作者团队 AdelaiDet 实现 |

## 图解版图片来源与许可

两篇 arXiv v3 的论文页面均标注 CC BY-NC-SA 4.0：

- SOLO：https://arxiv.org/html/1912.04488v3 ，页面 License 链接；正文 Fig. 2、Fig. 3。
- SOLOv2：https://arxiv.org/html/2003.10152v3 ，页面 License 链接；正文 Fig. 2(a)、Fig. 2(b)、附录 Fig. 5。
- 许可正文入口：https://creativecommons.org/licenses/by-nc-sa/4.0/ 。允许非商用分享与改编，要求署名、链接许可、标明修改，改编沿用相同许可。

本次使用 arXiv HTML 中的 5 个原图文件，保留下载字节，未裁剪、涂改或重绘；SOLOv2 的两幅子图以独立面板展示。每幅图旁提供原论文、作者简称、许可和修改情况，完整作者列表位于可展开资料区。逐图下载地址、来源版本、许可和 SHA-256 见 assets/figures/sources.json。图片及其改编沿用 CC BY-NC-SA 4.0；该说明不为第三方内容或整个网站重新授权。

此前只查看了出版方和代码仓库许可，遗漏了 arXiv 版本的明确许可，导致采用全部原创示意图。此次已纠正该审查结论；旧 SVG 文件保留但不再用于正文。

## 内容范围

按用户要求，正文改为简短的图解方法介绍，移除实验数值、结果表、消融建议及医学任务延伸。保留核心表示、方法流程、原图图注、全文与官方代码入口。原图中的符号由相邻中文说明解释；新增流程卡片为本站排版，未冒充论文原图。
