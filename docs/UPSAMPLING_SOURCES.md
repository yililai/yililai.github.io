# 上采样图解：来源与数值核验

核验日期：2026-11-10。文章为方法专题，不将多种算子归为同一篇论文。

## 一手资料

- 最近邻、双线性及坐标约定：PyTorch interpolate 官方文档 https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.interpolate.html ；OpenCV Geometric Image Transformations https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html 。传统插值不归因于某篇深度学习论文。
- CARAFE：Jiaqi Wang, Kai Chen, Rui Xu, Ziwei Liu, Chen Change Loy, Dahua Lin. CARAFE: Content-Aware ReAssembly of FEatures, ICCV 2019。https://arxiv.org/abs/1905.02188 ；正式全文 https://openaccess.thecvf.com/content_ICCV_2019/papers/Wang_CARAFE_Content-Aware_ReAssembly_of_FEatures_ICCV_2019_paper.pdf ；作者官方 CUDA 实现 https://github.com/myownskyW7/CARAFE ；MMCV CARAFEPack https://mmcv.readthedocs.io/en/latest/api/generated/mmcv.ops.CARAFEPack.html 。按原文第 3 节说明通道压缩、内容编码、每个目标位置的独立 softmax 与空间重组。
- 双三次经典参考：R. G. Keys, Cubic Convolution Interpolation for Digital Image Processing, IEEE TASSP 29(6):1153–1160, 1981。https://doi.org/10.1109/TASSP.1981.1163711 。不声称所有三次插值均由该文首次提出。
- 转置卷积：PyTorch ConvTranspose2d 官方文档；FCN, CVPR 2015 https://arxiv.org/abs/1411.4038 仅作为代表应用，不声称 FCN 发明转置卷积。
- Pixel Shuffle：Shi et al., Real-Time Single Image and Video Super-Resolution Using an Efficient Sub-Pixel Convolutional Neural Network, CVPR 2016。正式论文 https://openaccess.thecvf.com/content_cvpr_2016/papers/Shi_Real-Time_Single_Image_CVPR_2016_paper.pdf ；PyTorch PixelShuffle 官方文档。

## 数值约定与独立核验

- 单通道示例 X = [[10,20],[30,40]]，输出 4×4。双线性使用半像素映射 x=(j+0.5)/2−0.5、y=(i+0.5)/2−0.5，越界坐标用边界值延拓；最近邻为整数倍复制。
- 所有图使用同一个目标输出索引 [1,2]。最近邻值为 20；双线性映射到 (x,y)=(0.75,0.25)，四邻权重为 [[0.1875,0.5625],[0.0625,0.1875]]，输出 22.5。
- CARAFE 对应源位置 floor([1,2]/2)=[0,1]。演算使用零填充 3×3 邻域 [[0,0,0],[10,20,0],[30,40,0]]，手设示意核 [[0.01,0.01,0.01],[0.10,0.70,0.01],[0.05,0.10,0.01]]，九项和为 1，输出 20.5。该核不是模型输出；未伪造完整 CARAFE 4×4 预测。
- 图 6 为单独的一维转置卷积机制简例：输入 [10,20]，stride=2，padding=0，核 [1,2,1]，贡献重叠后得到 [10,20,30,40,20]。核同样为演示值。Pixel Shuffle 展示四个单像素通道重排为二维网格。
- `scripts/draw_upsampling.py` 用 Python 标准库生成六张原创 SVG，内含数值断言；演算数据保存在 `assets/figures/upsampling/example-values.json`。浏览器验证检查图中文字边界、数值显示与移动端排版。文中 PyTorch 片段供读者复现，未声称本环境运行了 PyTorch。

## 图片

六张图均独立绘制，不复制论文原图。arXiv 的 CARAFE 版本采用 non-exclusive-distrib 许可，并非本文此前核验过的 SOLO 系列 CC BY-NC-SA 许可；不把不同论文的许可互相套用。示意核和机制图不冒充论文实验。逐图来源与 SHA-256 记录见 `assets/figures/sources.json`。
