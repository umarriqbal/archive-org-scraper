import scrapy
from archive_org_scraper.util import remove_whitespace


class ArchiveorgbooksSpider(scrapy.Spider):
    name = 'archiveorgbooks'
    book_year_url = 'https://archive.org/details/books?and%5B%5D=year%3A%22{year}%22&sort=-week&page=1'
    base_url = 'https://archive.org/'
    init_year = 1927

    meta_map = {
        'by': {'title': 'author', 'css': 'a::text'},
        'Publication date': {'title': 'published', 'css': 'span::text'},
        'Publisher': {'title': 'publisher', 'css': 'span::text'},
        'Topics': {'title': 'tags', 'css': 'a::text'}
    }

    def start_requests(self):
        for year in reversed(range(self.init_year+1)):
            yield f'https://archive.org/details/books?and[]=year%3A%22{year}%22'

    def parse(self, response, **kwargs):

        current_page_url = response.request.url
        current_page = int(current_page_url[-1])

        has_books = not response.css('.no-results::text').get()

        if has_books:
            all_books = response.css('.item-ttl a::attr(href)').getall()
            for book_uri in all_books:
                book_url = f'{self.base_url}{book_uri}'
                yield scrapy.Request(book_url, callback=self.parse_book)

            next_page_url = f'{current_page_url[:-1]}{current_page+1}'
            yield scrapy.Request(next_page_url)

    def parse_book(self, response):

        book_title = remove_whitespace(response.css('.item-title span::text').get())
        book_meta = {
            'title': book_title
        }
        book_meta_html = response.css('.metadata-definition')

        for meta_info in book_meta_html:
            meta_title = meta_info.css('dt::text').get()
            if meta_title in self.meta_map:
                meta_tag = self.meta_map[meta_title]
                book_meta[meta_tag['title']] = meta_info.css(meta_tag['css']).get()

        download_html = response.css('.format-summary.download-pill')
        for download_opt in download_html:
            opt = remove_whitespace(download_opt.css('a::text').get(default='')).lower()
            if opt == 'pdf':
                pdf_uri = download_opt.css('a::attr(href)').get()
                if pdf_uri:
                    book_meta['download_url'] = f'{self.base_url}{pdf_uri}'

        yield book_meta

