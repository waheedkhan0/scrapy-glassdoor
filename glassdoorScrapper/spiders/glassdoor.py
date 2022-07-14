# -*- coding: UTF-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from glassdoorScrapper.items import Test1Item
import json
import re


class WestDoorSpider(Spider):
    name = 'glassdoor'
    allowed_domains = ['glassdoor.com']
    search_links = [
        'https://www.glassdoor.com/Job/us-appfolio-bookkeeper-jobs-SRCH_IL.0,2_IN1_KO3,22.htm',
        'https://www.glassdoor.com/Job/us-yardi-bookkeeper-jobs-SRCH_IL.0,2_IN1_KO3,19.htm',
        'https://www.glassdoor.com/Job/us-rent-manager-bookkeeper-jobs-SRCH_IL.0,2_IN1_KO3,26.htm',
        'https://www.glassdoor.com/Job/us-property-management-bookkeeper-jobs-SRCH_IL.0,2_IN1_KO3,33.htm',
        'https://www.glassdoor.com/Job/us-property-management-accountant-jobs-SRCH_IL.0,2_IN1_KO3,33.htm'

    ]
    # https://www.glassdoor.com/Job/united-states-property-management-accountant-jobs-SRCH_IL.0,13_IN1_KO14,44_IP2.htm?includeNoSalaryJobs=true&pgc=AB4AAYEAHgAAAAAAAAAAAAAAAd0VPV0ARAEBAQcXyEBT7rNJN9ghq1L7uuMlWI6TSwsjuG6abVw8HxJALmaSLtulqrkx3JdyNyqah37M9ykkwtb1CvfAE5S%2BpuApAAA%3D
    search_keywords = ['Appfolio Bookkeeper', 'Buildium Bookkeeper', 'Yardi Bookkeeper',
                       'Rent Manager Bookkeeper', 'Property Management Bookkeeper', 'Property Management Accountant']
    # https://www.glassdoor.com/Search/results.htm?keyword=&locId=1&locT=N&locName=United%20States
    # https://www.glassdoor.com/Job/jobs.htm?location-redirect=true
    # https://www.glassdoor.com/Search/results.htm?keyword=&locId=1&locT=N&locName=United%20States
    # https://www.glassdoor.com/Search/results.htm?keyword=software&locId=1&locT=N&locName=United%20States

    # https://www.glassdoor.com/job-listing/full-stack-engineer-freightwaves-JV_KO0,19_KE20,32.htm?jl=1007998493471&pos=303&ao=1136043&s=58&guid=00000181fb166c27b8408808b45dfe11&src=GD_JOB_AD&t=SR&vt=w&uido=F7E0E112FED2E0384887D26AA4DF2D0D&ea=1&cs=1_9cd9ba32&cb=1657774960165&jobListingId=1007998493471&jrtk=3-0-1g7thcr3djigh801-1g7thcr49h4fr800-7e7dd8f5e22e4dd5-&ctt=1657777857124

    def start_requests(self):
        for keyword in self.search_keywords:
            yield scrapy.Request(url="https://www.glassdoor.com/Search/results.htm?keyword={keyword}&locId=1&locT=N&locName=United%20States".format(keyword), callback=self.parse_page)

    def parse_page(self, response):
        list_elements = response.css('li.react-job-listing')
        for list_item in list_elements:
            title = list_item.css('.job-search-key-1rd3saf span::text').get()
            company = list_item.css('a.jobLink span::text').get()
            rate = list_item.css('.job-search-key-1a46cm1 span::text').get()
            location = list_item.css(
                '.job-search-key-1mn3dn8 .e1rrn5ka4::text').get()
            city = location.split(',')[0]
            state = location.split(',')[1]
            post_age = list_item.xpath(
                '//div[@data-test="job-age"]/text()').get()
            job_post_link = list_item.css(
                '.jobLink.job-search-key-1rd3saf.eigr9kq1').xpath('@href').get()
        for firm in firms:
            yield Request('http://www.glassdoor.com'+firm, callback=self.parse_detail)
        next_page = response.xpath("//li[@class='next']//@href").extract()
        next_page = next_page[0] if next_page else None
        if next_page is not None:
            yield Request('http://www.glassdoor.com'+next_page, callback=self.parse_page)

    def parse_detail(self, response):
        sel = response.xpath('//ol/li[contains(@id, "empReview")]')
        sel = response.css('.desc.css-58vpdc.ecgq1xb5')
        for review in sel:
            item = Test1Item()
            item['title'] = ''.join(review.xpath(
                './/h2/a/span[@class = "summary "]/text()').extract())
            item['link'] = ''.join(review.xpath(
                './/h2[@class="h2 summary strong tightTop"]/a/@href').extract())
            item['job_title'] = ''.join(review.xpath(
                './/span[@class = "authorJobTitle middle"]/text()').extract())
            item['work_life_balance'] = ''.join(review.xpath(
                ".//div[text()='Work/Life Balance']/following-sibling::node()/@title").extract())
            item['location'] = ''.join(review.xpath(
                './/span[@class="authorLocation i-loc middle"]/text()').extract())
            item['time'] = ''.join(review.xpath(
                './/time[@class="date subtle small"]/text()').extract())
            item['pos'] = ''.join(review.xpath('.//p[contains(@class, "pros")]/text()').extract() + review.xpath(
                './/p[contains(@class, "pros")]/span[@class = "moreEllipses"]/following-sibling::node()/span/text()').extract())
            item['cons'] = ''.join(review.xpath('.//p[contains(@class, "cons")]/text()').extract() + review.xpath(
                './/p[contains(@class, "cons")]/span[@class = "moreEllipses"]/following-sibling::node()/span/text()').extract())
            item['advice'] = ''.join(review.xpath(
                './/p[contains(@class, "adviceMgmt")]/text()').extract())
            item['overal_rating'] = ''.join(review.xpath(
                './/span[@class = "gdStars gdRatings sm margRt"]/span[@class = "rating notranslate_title"]//@title').extract())
            item['Culture_Values'] = ''.join(review.xpath(
                './/div[text() = "Culture & Values"]/following-sibling::node()/@title').extract())
            item['Career_Opportunities'] = ''.join(review.xpath(
                './/div[text() = "Career Opportunities"]/following-sibling::node()/@title').extract())
            item['Comp_Benefits'] = ''.join(review.xpath(
                './/div[text() = "Comp & Benefits"]/following-sibling::node()/@title').extract())
            item['Senior_Management'] = ''.join(review.xpath(
                './/div[text() = "Senior Management"]/following-sibling::node()/@title').extract())
            yield item

        next_url = response.xpath("//li[@class='next']//@href").extract()
        next_url = next_url[0] if next_url else None
        if next_url is not None:
            yield Request('http://www.glassdoor.com'+next_url, callback=self.parse_item)
