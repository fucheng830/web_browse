import requests
from lxml import etree
import html2text
import re
import requests
import re
import logging
import asyncio
import os 
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 通过环境变量读取图片服务器地址
IMAGE_SERVER=os.getenv('IMAGE_SERVER')
# 

async def replace_image(img):
    url = img.get('data-src')
    res = requests.post(f'{IMAGE_SERVER}/replace_image', json={'url': url})
    markdown_img = f"![image]({res.text})"
    new_element = etree.Element("p")
    new_element.text = markdown_img
    try:
        img.getparent().replace(img, new_element)
    except Exception as e:
        print(e)
    print(f"Replaced image {url} with {markdown_img}")

async def process_images(content):
    images = content.xpath('.//img')
    tasks = []
    for img in images:
        img_url = img.get('data-src')
        if img_url:
            # Schedule replace_image for execution
            task = asyncio.create_task(replace_image(img))
            tasks.append(task)
    
    image_data_list = await asyncio.gather(*tasks)

async def gzh_reader(url):
    """公众号文章解析器
    """
    res = requests.get(url, timeout=10)
    html = etree.HTML(res.content)
    title = html.xpath('//meta[@property="og:title"]/@content')[0]
    head_img = html.xpath('//meta[@property="og:image"]/@content')[0]
    description = html.xpath('//meta[@property="og:description"]/@content')[0]
    content = html.xpath('//div[@id="js_content"]')[0]
    await process_images(content)
    head_img_url = requests.post(f'{IMAGE_SERVER}/replace_image', json={'url': head_img}).text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    text_maker.images_to_alt = True  # 将图片转换为其alt文本
    markdown = text_maker.handle(etree.tostring(content, pretty_print=True).decode())
 
    return {'title': title, 
            'head_img': head_img_url, 
            'description': description, 
            'markdown': markdown}


def toutiao_reader(url):
    """今日头条文章解析器
    """
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # To run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    html = driver.page_source
    content = etree.HTML(html).xpath('//div[@class="article-content"]/article')[0]
    driver.quit()
    process_images(content)
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    text_maker.images_to_alt = True  # 将图片转换为其alt文本
    markdown = text_maker.handle(etree.tostring(content, pretty_print=True).decode())
    return markdown   


def common_reader(url):
    """通用文章解析器
    """
    res = requests.get(url, timeout=10)
    html = etree.HTML(res.content)

    # Extract title
    title = html.xpath('//meta[@property="og:title"]/@content')
    if not title:
        title = html.xpath('//title/text()')
    title = title[0] if title else 'No Title Found'

    # Extract favicon
    favicon = html.xpath('//link[contains(@rel, "icon")]/@href')
    if favicon:
        favicon = favicon[0]
    else:
        favicon = 'No Icon Found'

    # Extract description
    description = html.xpath('//meta[@property="og:description"]/@content')
    description = description[0] if description else 'No Description Found'

    # Extract all text from the body
    body_texts = html.xpath('//body//text()')
    body_content = ' '.join([text.strip() for text in body_texts if text.strip()])

    return {
        'title': title,
        'head_img': favicon,
        'description': description,
        'markdown': body_content
    }



async def get_content_from_url(url):
    """用正则匹配不同的url，采用不同的解析器
    """
    print('url', url)
    if re.match(r'https?:\/\/mp\.weixin\.qq\.com\/s(\?[\s\S]*)?', url):
        return await gzh_reader(url)
    elif re.match(r'https://www.toutiao.com/article/*', url):
        return await toutiao_reader(url)
    else:
        return common_reader(url)


if __name__ == '__main__':
    
    asyncio.run(get_content_from_url('https://mp.weixin.qq.com/s/CkUXi7tUsQgilzSQvJl8xA'))




