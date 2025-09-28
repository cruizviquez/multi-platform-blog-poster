import requests
import time
import random
from datetime import datetime
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('url_visitor.log'),
        logging.StreamHandler()
    ]
)

class URLVisitor:
    def __init__(self, url, interval_minutes=1, randomize_interval=True):
        """
        Initialize the URL visitor
        
        Args:
            url (str): Target URL to visit
            interval_minutes (int): Base interval between visits in minutes
            randomize_interval (bool): Add randomization to interval to appear more natural
        """
        self.url = url
        self.base_interval = interval_minutes * 60  # Convert to seconds
        self.randomize_interval = randomize_interval
        self.session = requests.Session()
        self.visit_count = 0
        
        # Validate URL
        if not self._is_valid_url(url):
            raise ValueError(f"Invalid URL: {url}")
        
        # User agents to rotate through
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        # Set initial session configuration
        self.session.timeout = 30
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def _is_valid_url(self, url):
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _get_random_user_agent(self):
        """Return a random user agent string"""
        return random.choice(self.user_agents)
    
    def _calculate_next_interval(self):
        """Calculate the next interval with optional randomization"""
        if self.randomize_interval:
            # Add ±30% randomization to the base interval
            variation = self.base_interval * 0.3
            return self.base_interval + random.uniform(-variation, variation)
        return self.base_interval
    
    def visit_url(self):
        """Visit the target URL once"""
        try:
            # Rotate user agent
            self.session.headers['User-Agent'] = self._get_random_user_agent()
            
            # Make the request
            response = self.session.get(self.url)
            response.raise_for_status()
            
            self.visit_count += 1
            
            logging.info(f"Visit #{self.visit_count} successful - Status: {response.status_code}, Size: {len(response.content)} bytes")
            return True
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error visiting URL: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return False
    
    def start_visiting(self, max_visits=None):
        """
        Start the automated visiting process
        
        Args:
            max_visits (int): Maximum number of visits (None for unlimited)
        """
        logging.info(f"Starting automated visits to: {self.url}")
        logging.info(f"Base interval: {self.base_interval/60:.1f} minutes")
        logging.info(f"Randomization: {'Enabled' if self.randomize_interval else 'Disabled'}")
        
        try:
            while max_visits is None or self.visit_count < max_visits:
                # Visit the URL
                success = self.visit_url()
                
                # Calculate next interval
                next_interval = self._calculate_next_interval()
                
                if success:
                    logging.info(f"Next visit in {next_interval/60:.1f} minutes")
                else:
                    logging.info(f"Retrying in {next_interval/60:.1f} minutes")
                
                # Wait for the calculated interval
                time.sleep(next_interval)
                
        except KeyboardInterrupt:
            logging.info("Stopping automated visits (Ctrl+C pressed)")
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {str(e)}")
    
    def get_stats(self):
        """Return visit statistics"""
        return {
            'total_visits': self.visit_count,
            'target_url': self.url,
            'base_interval_minutes': self.base_interval / 60
        }

def main():
    # Configuration - You can add multiple URLs here
    TARGET_URLS = [
        "https://carlosruizviquezinformationtechnology.blogspot.com",
        "https://carlosruizviquezinformationtechnology.blogspot.com/2025/09/about-dr-carlos-ruiz-viquez.html", 
        "https://medium.com/@bradley.adam/quantum-ready-ai-powered-the-future-of-cybersecurity-with-dr-ruizviquez-283e8dec2c88",
        "https://dev.to/ridley_jacobs_494aa92d35e/carlos-ruizviquez-cuevas-a-visionary-mind-shaping-the-future-of-technology-39p4",
        "https://medium.com/@cruizviquez/the-future-of-work-let-your-robot-earn-while-you-live-522e3bc7a122",
        "https://dev.to/drcarlosruizviquez",
        "https://mastodon.social/@DrCarlosRuizViquez",
        "https://www.facebook.com/dr.carlos.ruiz.viquez",
        "https://www.reddit.com/user/DrCarlosRuizViquez",
        "https://about.me/carlosruizviquez",
        "https://medium.com/@cruizviquez",
        "https://x.com/CRuizViquez"
    ]
    
    INTERVAL_MINUTES = 5  # Base interval between visits
    MAX_VISITS_PER_URL = None  # Set to a number to limit visits per URL, None for unlimited
    
    # Display configured URLs
    print("Configured URLs:")
    for i, url in enumerate(TARGET_URLS, 1):
        print(f"  {i}. {url}")
    print()
        
    try:
        visitors = []
        
        # Create visitor instance for each URL
        for i, url in enumerate(TARGET_URLS):
            visitor = URLVisitor(
                url=url,
                interval_minutes=INTERVAL_MINUTES,
                randomize_interval=True
            )
            visitors.append(visitor)
            logging.info(f"Initialized visitor {i+1}/{len(TARGET_URLS)}: {url}")
        
        # Start visiting URLs in rotation
        logging.info(f"Starting rotation of {len(TARGET_URLS)} URLs")
        visit_cycle = 0
        
        while True:
            visit_cycle += 1
            logging.info(f"=== Starting Cycle {visit_cycle} ===")
            
            for i, visitor in enumerate(visitors):
                if MAX_VISITS_PER_URL and visitor.visit_count >= MAX_VISITS_PER_URL:
                    logging.info(f"URL {i+1} has reached maximum visits ({MAX_VISITS_PER_URL})")
                    continue
                    
                logging.info(f"Visiting URL {i+1}/{len(TARGET_URLS)}: {visitor.url}")
                visitor.visit_url()
                
                # Wait between each URL in the cycle (except after the last one)
                if i < len(visitors) - 1:
                    wait_time = (INTERVAL_MINUTES * 60) / len(TARGET_URLS)
                    logging.info(f"Waiting {wait_time/60:.1f} minutes before next URL...")
                    time.sleep(wait_time)
            
            # Check if all visitors have reached max visits
            if MAX_VISITS_PER_URL and all(v.visit_count >= MAX_VISITS_PER_URL for v in visitors):
                logging.info("All URLs have reached maximum visits")
                break
            
            # Wait before starting next cycle
            cycle_wait = INTERVAL_MINUTES * 60
            logging.info(f"Cycle {visit_cycle} complete. Waiting {cycle_wait/60:.1f} minutes before next cycle...")
            time.sleep(cycle_wait)
        
    except KeyboardInterrupt:
        logging.info("Stopping all automated visits (Ctrl+C pressed)")
    except ValueError as e:
        logging.error(f"Configuration error: {str(e)}")
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
    finally:
        # Print final stats for all URLs
        if 'visitors' in locals():
            logging.info("=== Final Statistics ===")
            total_visits = 0
            for i, visitor in enumerate(visitors):
                stats = visitor.get_stats()
                logging.info(f"URL {i+1} ({visitor.url}): {stats['total_visits']} visits")
                total_visits += stats['total_visits']
            logging.info(f"Total visits across all URLs: {total_visits}")

if __name__ == "__main__":
    main()