DOWNLOAD_DELAY = 10
ITEM_PIPELINES = {
    'habrproject.pipelines.HabrImagesPipeline': 1,
    'habrproject.pipelines.HtmlWriterPipeline': 900,
}
