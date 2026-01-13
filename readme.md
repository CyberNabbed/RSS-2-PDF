# RSS to PDF Summarizer

## What this script does
This tool takes a list of RSS feeds and converts them into a single PDF summary.

It grabs the latest articles, filters out topics you don't want (based on a list of keywords), and uses Gemini (with your API key) to write a short summary for each one. Once it's done, it compiles the images and text into a PDF on your desktop and opens it for you.

## How it works
1.  **Input:** It asks you for RSS URLs (comma-separated).
2.  **Filtering:** It checks the articles against a "forbidden words" list. If an article matches, it gets skipped.
3.  **Summarization:** It sends the remaining articles to the Google Generative AI API to get a summary.
4.  **Output:** It generates `rss_feed.pdf`, saves it to the Desktop, opens the file, and closes the application.

## How to use it
1.  Run the application.
2.  When the prompt appears, paste your feed URLs (e.g., `site1.com/rss, site2.com/feed`).
3.  Wait a moment—the app will close itself once the PDF opens.
