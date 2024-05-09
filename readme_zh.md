# Web Browse 

Web Browse 是一个用于解析不同类型网页内容的工具，包括微信公众号文章，头条文章，以及其他网站的内容。

## 特性

- 解析微信公众号文章
- 解析头条文章
- 解析其他通用网页
- 提取并替换文章中的图片链接
- 将解析后的内容转换为Markdown格式

## 安装

首先，你需要通过环境变量配置图片服务器地址。例如，你可以在你的环境变量中添加如下行：

```bash
export IMAGE_SERVER=https://static.123qiming.com
```

然后，你可以使用Docker来运行此应用。在项目目录下，使用以下命令启动服务：

```bash
docker-compose up
```

Web Browse App 将在端口9998上运行。

## 使用

Web Browse App 提供一个POST接口 `/get_content`， 你可以将要解析的网页URL作为请求体发送，返回值将是解析后的内容。

例如：

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://mp.weixin.qq.com/s/CkUXi7tUsQgilzSQvJl8xA"}' http://localhost:9998/get_content
```

## 许可证

此项目已根据Apache License 2.0进行许可 - 查看[LICENSE](LICENSE)文件以获取详情。 

