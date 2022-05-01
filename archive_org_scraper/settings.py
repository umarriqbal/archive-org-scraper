
BOT_NAME = 'archive_org_scraper'
SPIDER_MODULES = ['archive_org_scraper.spiders']
NEWSPIDER_MODULE = 'archive_org_scraper.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
   'archive_org_scraper.pipelines.ArchiveOrgScraperPipeline': 300,
}
