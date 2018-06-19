import scrapy
from datetime import timedelta, date
import json
import re

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def return_url_list():
    start_date = date(2017, 1, 1)
    end_date = date(2018, 6, 17)
    my_list = []
    count = 6
    for single_date in daterange(start_date, end_date):
        count += 1
        if(count == 7):
            count = 0
            my_list.append(single_date.strftime("https://www.sundayobserver.lk/%Y/%m/%d/classifieds/employment-services"))
    return my_list

class observer_spider(scrapy.Spider):
    name = "jobs"

    start_urls = return_url_list()

    def parse(self, response):
        page = response.url.split("/")
        my_date = '{}-{}-{}'.format(page[-5],page[-4],page[-3])
        type = ""
        for job_notice in response.css('div.content div.field.field-name-body.field-type-text-with-summary.field-label-hidden div.field-items div.field-item.even p'):    
            job_id = job_notice.css("strong::text").extract_first()
            inner_content = job_notice.css("::text").extract_first()
           

            pattern=re.compile('^[0-9]+$')

            if(pattern.match(job_id)):
                filename = '{}_{}.txt'.format(page[-5],job_id)
                data_file = open(filename, "a+")
            
           
                data_file.write("date : ")
                data_file.write(my_date)
                data_file.write("\ncontent : ")
                data_file.write(inner_content)
                data_file.write("\ntype : ")
                data_file.write(type)
                data_file.write("\n")
                data_file.close()
            else:
                type = job_id

