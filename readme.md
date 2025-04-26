# Web Article Scraper

A Python utility for scraping and extracting article content from a series of web pages following a numerical pattern. This tool preserves the original formatting of articles while collecting them into a single document.

## Features

- Scrapes article content from a sequence of webpages (e.g., example.com/1.html through example.com/123.html)
- Preserves paragraph structure and text formatting from the original HTML
- Handles various HTML elements including paragraphs, headings, and lists
- Auto-detection of article content containers if the specified selector isn't found
- User-agent spoofing to reduce chances of being blocked
- Rate limiting to avoid overwhelming target servers
- Extensive error handling and debugging information

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - beautifulsoup4

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/web-article-scraper.git
   cd web-article-scraper
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```
   pip install requests beautifulsoup4
   ```

## Usage

Run the script with Python:

```
python web_scraper.py
```

The script will prompt you for:

1. **URL pattern**: Enter the first URL in the sequence (e.g., `example.com/1.html`)
2. **Range**: Enter the number of articles to scrape (e.g., `123`)
3. **CSS Selector**: Enter the selector for the article body (default: `#articlebody`)

### Example

```
What's the URL? (e.g., example.com/1.html): example.com/article/1.html
What's the range? (e.g., 123): 10
Enter CSS selector for article content (default: #articlebody): .article-content
```

This will scrape articles from `example.com/article/1.html` through `example.com/article/10.html`, extracting content from elements with the class `article-content`.

## Output

The script generates a file named `scraped_articles_formatted.txt` containing all the extracted articles, with preserved formatting including:

- Paragraph structure
- Headings
- Lists (ordered and unordered)
- Block quotes

Each article is clearly separated with divider lines for easy reading.

## Troubleshooting

If the script fails to find article content:

1. Check the CSS selector - inspect the HTML of the target page to confirm the correct ID or class
2. Look at the suggested alternative selectors in the output
3. Try running with one of the suggested alternatives

## Legal Notice

This tool is provided for educational purposes only. Please respect website terms of service and robots.txt files when using this scraper. Be considerate about rate limiting to avoid overwhelming servers.

## License

MIT License - See LICENSE file for details