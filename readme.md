# RSS Feed Summarizer & PDF Generator

## What is this?
This is a utility designed to help you digest news faster. Instead of clicking through dozens of articles, this tool grabs your favorite RSS feeds, filters out topics you don't care about, and uses Google's Generative AI to write concise summaries for you.

Everything gets compiled into a single PDF that lands on your desktop, ready to read.

## How it works
1.  **Input:** When you run the app, it asks for your RSS feed URLs.
2.  **Filtering:** It fetches the latest articles but automatically skips anything containing "forbidden words" (so you don't waste time on irrelevant topics).
3.  **AI Summaries:** It sends the good articles to Google's AI to generate a quick summary.
4.  **Delivery:** It grabs the article images and the new summaries, stamps them into a PDF (`rss_feed.pdf`), saves it to your Desktop, and opens it immediately.

## Quick Start
1.  **Launch the application.**
2.  **Paste your feeds:** When the prompt appears, paste in your RSS URLs separated by commas (e.g., `techcrunch.com/feed, nytimes.com/rss`).
3.  **Wait for the popup:** The app will do its work, generate the file, open the PDF for you, and then close itself automatically.
