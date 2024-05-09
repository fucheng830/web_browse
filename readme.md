# Web Browse
[中文说明](readme_zh.md)
Web Browse App is a tool for parsing different types of web page content, including WeChat public articles, Toutiao articles, and other website content.

## Features

- Parsing of WeChat public articles
- Parsing of Toutiao articles
- Parsing of other general web pages
- Extraction and replacement of image links within the articles
- Conversion of the parsed content into Markdown format

## Installation

Firstly, you need to configure the image server address through environment variables. For example, you can add the following line in your environment variables:

```bash
export IMAGE_SERVER=https://static.123qiming.com
```

Then, you can use Docker to run this application. From the project directory, use the following command to start the service:

```bash
docker-compose up
```

The Web Browse App will run on port 9998.

## Usage

Web Browse App provides a POST endpoint `/get_content`. You can send the URL of the web page you want to parse as the request body, and the response will be the parsed content.

For example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://mp.weixin.qq.com/s/CkUXi7tUsQgilzSQvJl8xA"}' http://localhost:9998/get_content
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

