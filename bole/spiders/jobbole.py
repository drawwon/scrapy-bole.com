# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib.parse import urljoin
from ..items import JobBoleArticleItem
from ..utils.common import get_md5



class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = [r'http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        #解析具体某个页面
        #获取下一页的url交给scrapy下载
        :param response:
        :return:
        """
        #获取某一页的url
        response_nodes = response.css('#archive .floated-thumb .post-thumb a')
        # response_url = response.css('a.archive-title::attr(href)').extract()
        for response_node in response_nodes:
            post_url = response_node.css('::attr(href)').extract_first(default="")
            image_url = response_node.css('img::attr(src)').extract_first(default="")
            # i = urljoin(response.url, post_url)
            # print(i)
            yield Request(url=post_url, meta={'front_image_url':image_url},
                        callback=self.parse_detail)

        # 提取下一页
        next_page_url = response.css('a[class="next page-numbers"]::attr(href)').extract_first(default="")
        if next_page_url:
            yield Request(url=next_page_url, callback=self.parse)


    def parse_detail(self,response):
        article_item = JobBoleArticleItem()
        article_item['url'] = response.url
        article_item['url_id'] = get_md5(response.url)
        # article_item['url_id'] =

        #封面图
        front_image_url = response.meta.get('front_image_url','')
        article_item['front_image_url'] = [front_image_url]
        #标题
        head_selector = response.xpath('//*[@class="entry-header"]/h1/text()')
        head = head_selector.extract()[0]
        css_head_selector = response.css('.entry-header h1::text').extract()[0]
        article_item['head'] = head

        #发布时间
        post_time_selector = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()')
        post_time_selector_css = response.css('.entry-meta-hide-on-mobile::text').extract()
        time_pattern = re.compile(r'\d{4}/\d{2}/\d{2}')
        time_content = post_time_selector.extract()[0]
        match = re.findall(time_pattern, time_content.strip())
        if match:
            print(match)
            post_time = match[0]
            article_item['post_time'] = post_time

        vote_up_selector = response.xpath('//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()')
        vote_up_selector_css = response.css('.vote-post-up h10::text').extract()
        if vote_up_selector.extract():
            vote_num = int(vote_up_selector.extract()[0])
        else:
            vote_num = 0
        article_item['vote_num'] = vote_num

        collection_selector = response.xpath('//span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()')
        collection_selector_css = response.css('span.bookmark-btn::text').extract()
        collection_re = re.findall('(\d+)收藏',collection_selector.extract()[0])
        if collection_re:
            collection_num = int(collection_re[0])
        else:
            collection_num = 0
        article_item['collection_num'] = collection_num

        comment_selector = response.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()')
        comment_selector_css = response.css('a[href="#article-comment"] span::text').extract()[0]
        comment_re = re.findall('(\d+)评论',comment_selector.extract_first(default=0))
        if comment_re:
            comment_num = int(comment_re[0])
        else:
            comment_num = 0
        article_item['comment_num'] = comment_num

        content = response.xpath('//div[@class="entry"]').extract_first('')
        article_item['content'] = content

        tag_selector = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        tag_selector_css = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag = tag_selector.extract()
        tag = [element for element in tag if not element.strip().endswith("评论")]
        tags = ','.join(tag)
        article_item['tags'] = tags
        yield article_item
