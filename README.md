# AnimeKnowledgeGraph

## 开放 API 接口

- URL ：`http://api.apassbydreg.work/anime-qa?question={question_in_chinese}` via `GET / POST`
- RESPONSE：json 字典
  - `"success"`：是否成功
  - `"result"`：回答或错误信息（ascii 编码的 utf-8 字符串，可能需要转码）

> 调用样例： http://api.apassbydreg.work/anime-qa?question=有马公生是哪个番剧里的角色？

## 应用样例

> Github Pages：[https://apassbydreg.github.io/AnimeKnowledgeGraph/](https://apassbydreg.github.io/AnimeKnowledgeGraph/)
>
> 中国内地：[http://apassbydreg.work/wordpress/personal-works/websites/AnimeKnowledgeGraph/](http://apassbydreg.work/wordpress/personal-works/websites/AnimeKnowledgeGraph/)