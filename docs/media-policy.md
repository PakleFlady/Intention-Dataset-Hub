# MIntRec 素材、真实样例与本地播放

**可以整理官方来源、样例编号、少量有署名的标注摘录及读取工具；本次不把视频压缩包、原视频或抽帧副本上传到 GitHub。** 下载成功本身不构成再分发授权。

2026-11-17 检查发现，本地解压目录包含 2,224 个 MP4。官方 MMLA 标注表中的 `S06_E04_70` 与本地文件 `MIntRec_S06_E04_70.mp4` 对应：

- 输入：该视频及音轨；官方文字为 “you're gonna go back and work on that register”。
- 输出：`arrange`（安排）。原 TSV 标签带有前导空格，展示时已去除。
- 来源：[THUIAR/MMLA-Datasets 的固定版本 test.tsv](https://huggingface.co/datasets/THUIAR/MMLA-Datasets/blob/ff135d32adaac2c3d5b0268e88a7ce6af200f544/MIntRec/test.tsv)，第一条数据记录。

这次核对确认了标注 ID 与本地文件名的对应关系，没有对下载包进行官方哈希校验，也没有重新判定标签。详情页保留的官方示意图是另一张任务演示图，不冒充该视频的抽帧。

## 许可调查结果

| 组件 / 来源 | 核验到的声明 | 本仓库的处理 |
| --- | --- | --- |
| [原项目软件 LICENSE](https://github.com/thuiar/MIntRec/blob/6bc239695df342c22c324bb3a76789fa295ff999/LICENSE) | MIT，针对软件及关联文档 | 不据此推断电视剧素材也获得 MIT 授权 |
| [MMLA 数据卡](https://huggingface.co/datasets/THUIAR/MMLA-Datasets/blob/ff135d32adaac2c3d5b0268e88a7ce6af200f544/README.md) | CC BY 4.0 | 标注摘录注明发布者、固定版本、许可及空白规范化修改 |
| [MIntRec 数据卡](https://huggingface.co/datasets/THU-IAR/MIntRec) | CC BY-SA 4.0 | 如使用这个发布包，需核对其自身许可；不把两个数据卡视为完全一致 |
| Superstore 电视剧音视频 | 尚未确认独立再分发授权 | 仅保留官方入口和本地读取方式 |

这些是发布页声明的记录，不是对完整版权链的证明。CC 许可也不保证授予使用素材所需的全部权利，见 [CC BY 4.0 官方说明](https://creativecommons.org/licenses/by/4.0/)。若计划公开镜像原视频，需要先核实发布方对底层素材的授权及其适用范围；当前证据不足以认定整包上传合规。

## 在本机看这条输入输出

使用官方 `test.tsv` 与已经解压的视频目录：

```powershell
python scripts/preview_mintrec.py --video-root 'E:\MIntRec_video\video' --annotations 'local-data\mintrec-test.tsv' --sample-id S06_E04_70
```

脚本生成 `local-data/mintrec-example.html`。用浏览器打开，可以播放本地视频并同时看到原标注文字与标签。脚本不联网、不复制视频、不上传文件；输出目录已加入 `.gitignore`。其他使用者可将参数换成自己的合法取得的本地文件位置。

第三方标注摘录归原权利人所有，按其发布条款使用，不随本仓库原创文档重新许可。请同时引用 [MIntRec 原始论文与项目](https://github.com/thuiar/MIntRec)及 [MMLA 项目](https://github.com/thuiar/MMLA)。
