import scrapy
from course_scraper.items import Course

class OeruSpider(scrapy.Spider):
    name = "oeru"
    allowed_domains = ["oeru.org"]
    start_urls = ['http://oeru.org/courses/']

    def parse(self, response):


        for sel in response.xpath(u'//a[@class="thumb"]'):
            #title = sel.xpath('.//h4/text()').extract()
            link = sel.xpath('./@href').extract()[0]
            yield scrapy.Request('http://oeru.org/' + link, callback = self.parse_course)

    def extract_data_table(self, data):
        xp = u'//span[contains(text(), "{}")]/following-sibling::span/text()'.format(data.title()[:-1])
        return self.extract_xp(xp)

    def extract_xp(self, xp):
        data = self.sel.xpath(xp).extract()
        if data:
            return data[0].strip()
        else:
            print '-->', xp
            return None

    def parse_credentialing(self):
        credentialing = []
        ribbon = '//img[@src="themes/oeru/img/ribbon.png"]'
        if self.sel.xpath(ribbon):
            credentialing.append("Official course credit")
        gradhat = '//img[@src="themes/oeru/img/gradhat.png"]'
        if self.sel.xpath(gradhat):
            credentialing.append("Certificates of achievement")
        return credentialing

    def parse_level(self, course):
        level = course.get('level')
        if level:
            lines = level.split('\n')
            lines = [l.strip() for l in lines if l.strip()]
            if len(lines) > 1:
                course['level'] = lines

    def parse_duration(self, course):
        duration = course.get('duration')
        if duration:
            dur_ = duration.split(',')
            if len(dur_) == 2:
                course['weeks'] = dur_[0].replace('weeks', '').replace("Weeks", '').replace('hours', '').strip()
                course['hpw'] = dur_[1].replace('hours per week', '').replace("hours", '').strip()

    def parse_course(self, response):
        self.sel = response.selector
        c = Course()
        data_rules = {
            'name': '//h3/text()',
            'university': '//span[contains(@class, "course-partner-logo")]//img/@alt'
            }

        data_at_table = 'starts finishes duration type assessments credit level'.split()

        c['url'] = response.url

        for k in data_rules:
            c[k] = self.extract_xp(data_rules.get(k))

        for d in data_at_table:
            c[d] = self.extract_data_table(d)

        c['credentialing'] = self.parse_credentialing()

        self.parse_level(c)
        self.parse_duration(c)

        return c



        '''
        'title',
        'periodo/ nuevo'  --> span@class, contains course-period
        Future
          closed/link?                  --> span@class, contins course-register-button
          course register button  Text = REGISTER TO START LEARNING   LINK --> HREF
          starts                -> sel.xpath(u'//span[contains(text(), "Start")]/following-sibling::span/text()').extract()[0].strip()
          Finishes
          Duration
          Type
          Assessments
          Credentialing  *
          Course credit
          Credential
          Level
          university    span class, contains course-partner-logo  > img >alt
          setattr(c, 'name')

'''
