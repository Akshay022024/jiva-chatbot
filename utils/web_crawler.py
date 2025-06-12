import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
from typing import Set

class WebCrawler:
    def __init__(self, base_url: str, output_file: str):
        self.base_url = base_url
        self.output_file = output_file
        self.visited_urls: Set[str] = set()

    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the base domain."""
        return urlparse(self.base_url).netloc == urlparse(url).netloc

    def clean_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text content from HTML."""
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get text and clean it
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())

    def crawl_page(self, url: str) -> str:
        """Crawl a single page and return its cleaned content."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return self.clean_text(soup)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return ""

    def extract_links(self, url: str, soup: BeautifulSoup) -> Set[str]:
        """Extract all valid links from the page."""
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                links.add(full_url)
        return links

    def crawl_website(self):
        """Main crawling function."""
        to_visit = {self.base_url}
        all_content = []

        while to_visit:
            url = to_visit.pop()
            if url in self.visited_urls:
                continue

            print(f"Crawling: {url}")
            self.visited_urls.add(url)

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract content
                content = self.clean_text(soup)
                if content:
                    all_content.append(content)

                # Find new links
                new_links = self.extract_links(url, soup)
                to_visit.update(new_links)

            except Exception as e:
                print(f"Error processing {url}: {str(e)}")

        # Save all content
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(all_content))

if __name__ == "__main__":
    BASE_URL = "https://www.jivainfotech.com/"
    OUTPUT_FILE = os.path.join("data", "website_data.txt")
    
    crawler = WebCrawler(BASE_URL, OUTPUT_FILE)
    crawler.crawl_website()
    print(f"Crawling completed. Data saved to {OUTPUT_FILE}")
