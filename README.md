# yililai.github.io
My personal academic website and research blog https://yililai.github.io/

中文论文精读与密集小目标实例分割研究笔记。现有 FCN、U-Net 页面保持独立；SOLO 系列采用可复用的文章模板与来源记录。

- [维护与写作流程](docs/BLOG_WORKFLOW.md)
- [SOLO / SOLOv2 论文核验记录](docs/SOLO_SOURCES.md)
- [图片来源与许可审查](assets/figures/sources.json)

```bash
python scripts/build_blog.py
python scripts/build_blog.py --check
python scripts/check_site.py
python -m http.server 8000
```

只需 Python 标准库，无前端构建依赖。正文在 `content/`，元数据在 `data/posts.json`。生成器仅更新新文章及首页标记内的新增目录，不重建旧文章。推送前检查差异、浏览器移动端布局及外部来源；GitHub Actions 自动检查生成一致性和站内资源。
