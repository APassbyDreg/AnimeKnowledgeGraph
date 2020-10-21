# API Collections

## BiliBili

### 番剧列表

> 获取番剧列表

url: https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=50&type=1

参数说明：

- `season_version` : 类型
- `area` : 地区
- `is_finish` : 是否完结
- `copyright` : 版权信息
- `season_status` : 付费情况
- `page` : 分页编号

响应内容样例：`bamgumi-index.json`

重要内容：

- `title`
- `media_id`
- `season_id`

### 番剧主页

> 番剧主页地址

url: https://www.bilibili.com/bangumi/media/md + media_id

参数说明：

- `media_id` : 见 `番剧列表 API` 的响应内容

响应内容样例：`bamgumi-profile.html, bamgumi-profile-init.json`

重要内容（对于未经 JS 处理的文档）：

- `window.__INITIAL_STATE__.mediaInfo` : 影片信息
  - `actors、staff` 演职员表
  - `alias` 别名
  - `rating` 评分

### 番剧播放页

> 番剧播放页地址

url: https://www.bilibili.com/bangumi/play/ss + season_id

参数说明：

- `season_id` : 见 `番剧列表 API` 的响应内容

重要内容（对于未经 JS 处理的文档）：

- `window.__INITIAL_STATE__.mediaInfo` : 影片信息，包括统计信息等
- `window.__INITIAL_STATE__.eplist` : 分集播放信息，包括标题、分集 ID 、aid 、bvid 等

### 番剧分集播放页

> 番剧分集播放页地址

url: https://www.bilibili.com/bangumi/play/ep + episode_id

### 番剧统计数据

> 包括硬币数、弹幕数、追番数、系列追番数、播放量等

url = https://api.bilibili.com/pgc/web/season/stat?season_id= + season_id

参数说明：

- `season_id` : 见 `番剧列表 API` 的响应内容

### 视频信息

> 单个视频的统计信息

url: http://api.bilibili.com/x/web-interface/view? + aid or bvid

详情见 [此 Github Repo](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/video/info.md)


### API 封装包

> 封装了各类 BiliBili API 的包

```shell
pip install bilibili_api
```

文档：https://passkou.com/bilibili_api/docs/