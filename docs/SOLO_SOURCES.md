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

## 数值与定位

SOLO：作者公开全文 Table 1 使用 6×（72 epochs）主结果，COCO test-dev，ResNet-101-FPN：SOLO AP 37.8，增强版 Mask R-CNN* AP 37.8。Table 2 的 val2017 单层网格 S=12/24/36 AP 27.2/29.0/28.6，Pyramid AP 35.8。Table 3 的 0/1 层 CoordConv AP 32.2/35.8。主结果与消融训练设置不同，不跨表作因果相加。

SOLOv2：正式全文 Table 1，COCO test-dev，ResNet-101-FPN，SOLO 37.8、SOLOv2 39.7 AP。Table 3(a)，val2017，1×1×256 / 1×1×512 核 AP 37.8 / 37.7。Table 3(d)，Separate / Unified AP 37.3 / 37.8。Table 3(c)，Hard-NMS / Matrix NMS AP 36.3 / 36.6，NMS 衰减步骤耗时 9 / <1 ms。第 3.1.2 节说明该计时排除 IoU 矩阵构造，正文保留此限定。

## 权限审查

SOLO Springer 页面列明 © 2020 Springer Nature Switzerland AG，并提供 Reprints and permissions 链接。未取得明确适用于本站原图转载的授权。SOLOv2 的官方 proceedings、论文入口与作者仓库已查看，未确认适用于本站论文原图的明确转载条款；这不等于断言所有原图均不可转载。

WXinlong/SOLO 的 LICENSE 开头标注 “SOLO for non-commercial purposes”，并含源代码 / 二进制再分发保留说明。本项目没有复制其代码或图片，也不将这份代码许可视作论文插图许可。

使用的四张 SVG 均为独立布局的原创概念图，图注注明论文来源与分析属性；无原图截图、裁切、描摹或第三方图片文件。图源逐图记录于 `assets/figures/sources.json`。

## 区分原文与本文贡献

GT—槽位二部图匹配诊断、固定图像下 Z=KF 的线性秩观察、医学任务的分层诊断及新增消融方案均为文章分析。它们不是两篇原论文已有的细胞核实验，也没有在本项目训练验证；不作新颖性或性能承诺。
