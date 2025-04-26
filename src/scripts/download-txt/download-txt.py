import requests
from bs4 import BeautifulSoup
import os
import re
import time

def get_article_content_formatted(url, selector='#articlebody'):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try the provided selector first
        article_body = soup.select_one(selector)
        
        if not article_body:
            # Look for elements with ID containing "article" or "content"
            article_candidates = []
            for element in soup.find_all(id=re.compile(r'article|content|body', re.I)):
                article_candidates.append(f"#{element['id']}")
                print(f"Found potential article container: #{element['id']}")
            
            # Look for common article class names
            for element in soup.find_all(class_=re.compile(r'article|content|body|post|text', re.I)):
                if element.get('class'):
                    class_selector = '.'.join(element.get('class'))
                    article_candidates.append(f".{class_selector}")
                    print(f"Found potential article container by class: .{class_selector}")
            
            if article_candidates:
                print(f"Try using one of these selectors instead: {', '.join(article_candidates[:5])}")
                
                # Try the first candidate
                if article_candidates:
                    article_body = soup.select_one(article_candidates[0])
                    print(f"Using alternate selector: {article_candidates[0]}")
            
            if not article_body:
                print(f"No article body found in {url}")
                return ""
        
        # Extract formatted content, preserving paragraphs and structure
        formatted_content = []
        
        # Process common text elements while preserving structure
        for element in article_body.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'blockquote']):
            tag_name = element.name
            
            if tag_name.startswith('h'):
                # For headings, add some emphasis
                heading_level = int(tag_name[1])
                formatted_content.append(f"{'#' * heading_level} {element.get_text().strip()}")
            elif tag_name == 'p':
                # For paragraphs, preserve as is
                text = element.get_text().strip()
                if text:  # Only add non-empty paragraphs
                    formatted_content.append(text)
            elif tag_name == 'blockquote':
                # Format blockquotes
                text = element.get_text().strip()
                formatted_content.append(f"> {text}")
            elif tag_name in ['ul', 'ol']:
                # Format lists
                for i, li in enumerate(element.find_all('li')):
                    text = li.get_text().strip()
                    if tag_name == 'ul':
                        formatted_content.append(f"• {text}")
                    else:
                        formatted_content.append(f"{i+1}. {text}")
        
        # If no structured elements were found, fall back to all text with basic formatting
        if not formatted_content:
            # Try to create paragraphs based on double line breaks or significant spacing
            text = article_body.get_text(separator='\n', strip=True)
            paragraphs = re.split(r'\n\s*\n', text)
            formatted_content = [p.strip() for p in paragraphs if p.strip()]
        
        # Join with double newlines to preserve paragraph structure
        result = '\n\n'.join(formatted_content)
        print(f"Successfully extracted {len(result)} characters of formatted content")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def main():
    # Get parameters from user
    base_url = input("What's the URL? (e.g., example.com/1.html): ")
    range_end = input("What's the range? (e.g., 123): ")
    selector = input("Enter CSS selector for article content (default: #articlebody): ").strip() or '#articlebody'
    
    # Validate inputs
    try:
        range_end = int(range_end)
        if range_end <= 0:
            print("Range must be a positive number.")
            return
    except ValueError:
        print("Range must be a valid number.")
        return
    
    # Extract the URL pattern more intelligently
    url_parts = base_url.split('/')
    file_part = url_parts[-1]
    
    # Find the numeric part to replace
    match = re.search(r'(\d+)', file_part)
    if not match:
        print("Couldn't find a number in the URL to increment")
        return
    
    num_str = match.group(1)
    url_pattern = base_url.replace(num_str, "{}")
    
    # Create the output file path in the same directory as the script
    output_file = "scraped_articles_formatted.txt"
    
    print(f"Starting to scrape {range_end} articles from {url_pattern}...")
    print(f"Using selector: {selector}")
    
    all_content = []
    for i in range(1, range_end + 1):
        url = url_pattern.format(i)
        print(f"\nScraping article {i}/{range_end}: {url}")
        content = get_article_content_formatted(url, selector)
        
        if content:
            all_content.append(f"{'=' * 50}\nARTICLE {i}\n{'=' * 50}\n\n{content}\n\n")
            print(f"Article {i} saved successfully ({len(content)} characters)")
        else:
            print(f"Couldn't extract content from article {i}")
        
        # Small delay to avoid overwhelming the server
        if i < range_end:
            time.sleep(0.5)
    
    # Save all content to a file
    if all_content:
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(all_content)
        
        print(f"\nFinished! Saved {len(all_content)} articles to {os.path.abspath(output_file)}")
    else:
        print("\nNo articles were successfully scraped.")

if __name__ == "__main__":
    main()