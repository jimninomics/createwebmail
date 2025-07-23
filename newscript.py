import requests
import gzip
import json
import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote
from collections import defaultdict
from typing import Dict, List, Optional
import io

class ZillowAddressExtractor:
    def __init__(self, output_file: str = "zillow_addresses.json"):
        """Initialize the Zillow address extractor.
        
        Args:
            output_file: Path to the JSON file where addresses will be saved
        """
        self.output_file = output_file
        self.addresses_by_zip = self._load_existing_data()
    
    def _load_existing_data(self) -> Dict[str, List[str]]:
        """Load existing address data from the JSON file if it exists."""
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse existing file {self.output_file}. Creating new data.")
                return defaultdict(list)
        return defaultdict(list)
    
    def _save_data(self):
        """Save the address data to the JSON file."""
        with open(self.output_file, 'w') as f:
            json.dump(self.addresses_by_zip, f, indent=2)
        print(f"Saved {sum(len(addresses) for addresses in self.addresses_by_zip.values())} addresses to {self.output_file}")
    
    def extract_address_from_url(self, url: str) -> Optional[Dict[str, str]]:
        """Extract address components from a Zillow URL.
        
        Args:
            url: A Zillow property URL
            
        Returns:
            Dictionary with address components or None if parsing failed
        """
        # Parse the URL path
        path = unquote(urlparse(url).path)
        
        # Extract address using regex patterns
        # Pattern for addresses like: /123-main-st-city-state-zip/
        address_pattern = r'/([^/]+)-([^/]+)-([^/]+)-([^/]+)-(\d{5})/'
        match = re.search(address_pattern, path)
        
        if match:
            street_num, street_name, city, state, zipcode = match.groups()
            return {
                "street": f"{street_num} {street_name}".replace('-', ' '),
                "city": city.replace('-', ' '),
                "state": state.upper(),
                "zipcode": zipcode,
                "full_address": f"{street_num} {street_name}, {city}, {state} {zipcode}".replace('-', ' ')
            }
        
        # Alternative pattern for other URL formats
        alt_pattern = r'/([^/]+)/(\d{5})/'
        match = re.search(alt_pattern, path)
        if match:
            location, zipcode = match.groups()
            return {
                "location": location.replace('-', ' '),
                "zipcode": zipcode,
                "full_address": f"{location}, {zipcode}".replace('-', ' ')
            }
        
        return None
    
    def process_sitemap(self, sitemap_url: str):
        """Process a Zillow sitemap XML file and extract addresses.
        
        Args:
            sitemap_url: URL to the Zillow sitemap XML file (can be gzipped)
        """
        print(f"Downloading and processing {sitemap_url}...")
        
        try:
            # Download the file with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            
            response = requests.get(sitemap_url, headers=headers, stream=True)
            response.raise_for_status()
            
            # Check content type to determine if it's gzipped
            content_type = response.headers.get('Content-Type', '')
            content_encoding = response.headers.get('Content-Encoding', '')
            
            # Try to decompress if it's gzipped
            if 'gzip' in content_encoding or sitemap_url.endswith('.gz'):
                try:
                    xml_content = gzip.decompress(response.content)
                except Exception as e:
                    print(f"Warning: Failed to decompress as gzip: {e}")
                    # If decompression fails, try to use the content directly
                    xml_content = response.content
            else:
                xml_content = response.content
            
            # Check if the content starts with XML declaration
            if not xml_content.startswith(b'<?xml'):
                print(f"Warning: Response doesn't look like XML. First 100 bytes: {xml_content[:100]}")
                
                # Try to find an XML declaration in the content
                xml_start = xml_content.find(b'<?xml')
                if xml_start >= 0:
                    xml_content = xml_content[xml_start:]
                else:
                    raise ValueError("Response doesn't contain valid XML")
            
            # Parse the XML
            root = ET.fromstring(xml_content)
            
            # Define the XML namespace
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            
            # Extract URLs
            urls = [url_elem.text for url_elem in root.findall('.//sm:url/sm:loc', ns) if url_elem.text]
            
            if not urls:
                # Try without namespace if no URLs found
                urls = [url_elem.text for url_elem in root.findall('.//url/loc') if url_elem.text]
            
            print(f"Found {len(urls)} URLs in the sitemap")
            new_addresses = 0
            
            # Process each URL to extract addresses
            for url in urls:
                address_info = self.extract_address_from_url(url)
                if address_info and 'zipcode' in address_info:
                    zipcode = address_info['zipcode']
                    full_address = address_info['full_address']
                    
                    # Add address to the appropriate zip code list if it's not already there
                    if full_address not in self.addresses_by_zip[zipcode]:
                        self.addresses_by_zip[zipcode].append(full_address)
                        new_addresses += 1
            
            print(f"Added {new_addresses} new addresses")
            
            # Save the updated data
            self._save_data()
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading sitemap: {e}")
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            print(f"First 200 bytes of content: {xml_content[:200]}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def get_addresses_by_zip(self, zipcode: str) -> List[str]:
        """Get all addresses for a specific zip code.
        
        Args:
            zipcode: The zip code to search for
            
        Returns:
            List of addresses in the specified zip code
        """
        return self.addresses_by_zip.get(zipcode, [])

def extract_addresses_from_sitemap(sitemap_url="https://www.zillow.com/sitemap/homes/", 
                                  output_file="zillow_addresses.json"):
    """Extract addresses from a Zillow sitemap and save them to a JSON file."""
    extractor = ZillowAddressExtractor(output_file=output_file)
    extractor.process_sitemap(sitemap_url)
    return extractor

def get_addresses_by_zipcode(zipcode, output_file="zillow_addresses.json"):
    all_addresses = []
    """Get all addresses for a specific zip code from the saved JSON file."""
    extractor = ZillowAddressExtractor(output_file=output_file)
    addresses = extractor.get_addresses_by_zip(zipcode)
    
    if addresses:
        print(f"Found {len(addresses)} addresses in zip code {zipcode}:")
        for address in addresses:
            all_addresses.append(address)
    else:
        print(f"No addresses found for zip code {zipcode}")
    
    return all_addresses

# Example usage
if __name__ == "__main__":
    # Configuration
    # Try a different sitemap URL since the original one is giving errors
    sitemap_num = 21
    num=f"{sitemap_num:03d}"
    print(num)
    sitemap_url = f"https://www.zillow.com/xml/sitemaps/us/hdp/for-rent/sitemap-0{num}.xml.gz"
    output_file = "alladdress/zillow_addresses21.json"
    
    # Extract addresses from the sitemap
    extractor = extract_addresses_from_sitemap(sitemap_url, output_file)
    
    # Example: Search for addresses in a specific zip code
    # Uncomment the line below and replace with your desired zip code
    # print(get_addresses_by_zipcode("11229", output_file))