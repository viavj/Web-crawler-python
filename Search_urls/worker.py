from urllib.request import urlopen
from page_filter import PageFilter
from domain import *
from general import *


class Worker:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Worker.project_name = project_name
        Worker.base_url = base_url
        Worker.domain_name = domain_name
        Worker.queue_file = Worker.project_name + '/queue.txt'
        Worker.crawled_file = Worker.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('Worker 1 ', Worker.base_url)

    # Create directory and files, and run the project
    @staticmethod
    def boot():
        create_project_dir(Worker.project_name)
        create_data_files(Worker.project_name, Worker.base_url)
        Worker.queue = file_to_set(Worker.queue_file)
        Worker.crawled = file_to_set(Worker.crawled_file)

    # Show process details,  update sets (queue, crawled)
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Worker.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Worker.queue)) + ' | Crawled  ' + str(len(Worker.crawled)))
            Worker.add_links_to_queue(Worker.gather_links(page_url))
            Worker.queue.remove(page_url)
            Worker.crawled.add(page_url)
            Worker.update_files()

    # Make the response readable
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            #  Check if we are not in some 'pdf' or 'txt' or some other weird file
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = PageFilter(Worker.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            # Ok this function needs to return some set of links, if there is an error - we still need to return something
            return set()      # IMPORTANT,  to prevent the error - return an empty set
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Worker.queue) or (url in Worker.crawled):
                continue
            if Worker.domain_name != get_domain_name(url):
                continue
            Worker.queue.add(url)

    @staticmethod  # Actually there's no need declare them as staticmethod, just this way you don't use 'self' arg.
    def update_files():
        set_to_file(Worker.queue, Worker.queue_file)
        set_to_file(Worker.crawled, Worker.crawled_file)
