import requests
from bs4 import BeautifulSoup
import time
import logging
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(
    filename="logs/link_performance_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def extract_links(base_url):
    """Extract all links from a given base URL."""
    print(f"Extracting links from {base_url}...")
    visited = set()
    to_visit = [base_url]
    all_links = []
    
    parsed_base = urlparse(base_url)
    base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
    
    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
            
        visited.add(current_url)
        
        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code != 200:
                print(f"Failed to access {current_url}: Status code {response.status_code}")
                continue
                
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(current_url, href)
                
                # Only process links to the same domain
                if urlparse(full_url).netloc == parsed_base.netloc:
                    all_links.append(full_url)
                    if full_url not in visited and full_url not in to_visit:
                        to_visit.append(full_url)
                        
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {current_url}: {e}")
    
    # Remove duplicates and return
    return list(set(all_links))

def check_link_performance(links):
    """Test the performance of a list of links."""
    print(f"Testing performance of {len(links)} links...")
    results = []
    for link in links:
        try:
            start_time = time.time()
            response = requests.get(link, timeout=10)
            end_time = time.time()
            elapsed_time = end_time - start_time
            status = "Fast" if elapsed_time < 2 else "Slow"
            
            # Log the result
            logging.info(f"URL: {link}, Status Code: {response.status_code}, Response Time: {elapsed_time:.2f}s, Performance: {status}")
            
            # Add to results
            results.append({
                "url": link,
                "status_code": response.status_code,
                "response_time": elapsed_time,
                "performance": status
            })
            
            # Alert for slow responses
            if status == "Slow":
                print(f"Alert: {link} is slow with a response time of {elapsed_time:.2f}s")
                
        except requests.exceptions.RequestException as e:
            error_message = str(e)
            logging.error(f"URL: {link}, Error: {error_message}")
            results.append({
                "url": link,
                "error": error_message,
                "performance": "Failed"
            })
            
    return results

def generate_report(results):
    """Generate a summary report of the performance test results."""
    total = len(results)
    fast_count = sum(1 for r in results if r.get('performance') == 'Fast')
    slow_count = sum(1 for r in results if r.get('performance') == 'Slow')
    failed_count = sum(1 for r in results if r.get('performance') == 'Failed')
    
    print("\n===== PERFORMANCE TEST REPORT =====")
    print(f"Total Links Tested: {total}")
    print(f"Fast Links: {fast_count} ({fast_count/total*100:.1f}%)")
    print(f"Slow Links: {slow_count} ({slow_count/total*100:.1f}%)")
    print(f"Failed Links: {failed_count} ({failed_count/total*100:.1f}%)")
    
    if slow_count > 0:
        print("\nSlow Links:")
        for r in results:
            if r.get('performance') == 'Slow':
                print(f"  - {r['url']} ({r['response_time']:.2f}s)")
    
    if failed_count > 0:
        print("\nFailed Links:")
        for r in results:
            if r.get('performance') == 'Failed':
                print(f"  - {r['url']} ({r.get('error', 'Unknown error')})")

if __name__ == "__main__":
    # Base URL of your webapp
    base_url = "http://127.0.0.1:5000"
    
    # Extract all links
    all_links = extract_links(base_url)
    print(f"Found {len(all_links)} unique links")
    
    # Check performance
    performance_results = check_link_performance(all_links)
    
    # Generate report
    generate_report(performance_results)
    
    print("\nDetailed results have been logged to link_performance_log.txt")