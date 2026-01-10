import tkinter as tk
from tkinter import messagebox, simpledialog
import feedparser
from fpdf import FPDF
import requests
from PIL import Image
from io import BytesIO
import os
from bs4 import BeautifulSoup
import uuid
import time
import platform
import subprocess


class RSSPDFConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("RSS to PDF Converter")
        self.feed_urls = []

        # Load API key from environment variable
        self.google_api_key = os.getenv("GOOGLE_API_KEY")

        if not self.google_api_key:
            messagebox.showerror(
                "Missing API Key",
                "Set the GOOGLE_API_KEY environment variable before running."
            )
            self.master.destroy()
            return

        # Placeholder list for content filtering
        # Replace with your own terms if needed
        self.forbidden_words = [
            "example_word_1",
            "example_word_2",
            "example_phrase_here"
        ]

        self.title_label = tk.Label(
            master, text="RSS to PDF Converter", font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=(20, 5))

        self.instruction_label = tk.Label(
            master,
            text="Enter RSS feed URLs separated by commas.\n"
                 "Articles containing filtered terms will be skipped.",
            font=("Arial", 10)
        )
        self.instruction_label.pack(pady=(0, 15))

        self.convert_button = tk.Button(
            master, text="Collect & Convert", command=self.collect_feeds, width=20
        )
        self.convert_button.pack(pady=10)

    def collect_feeds(self):
        feeds_input = simpledialog.askstring(
            "RSS Feeds", "Enter RSS feed URLs (separated by commas):"
        )
        if feeds_input:
            self.feed_urls = [url.strip() for url in feeds_input.split(",") if url.strip()]

        if not self.feed_urls:
            messagebox.showinfo("No feeds entered", "No RSS feeds were provided.")
            return

        self.create_pdf()

    def create_pdf(self):
        pdf = FPDF("P", "mm", "Letter")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for url in self.feed_urls:
            feed_data = feedparser.parse(url)
            if not feed_data.entries:
                continue

            for entry in feed_data.entries:
                title = entry.get("title", "No Title")
                summary = entry.get("summary", "No Summary")

                soup = BeautifulSoup(summary, "html.parser")
                plain_summary = soup.get_text()

                if self.contains_forbidden_words(title, plain_summary):
                    continue

                pdf.add_page()

                summarized_text = self.summarize_text(title, plain_summary)
                if summarized_text:
                    plain_summary = summarized_text

                title = self.clean_text(title)
                plain_summary = self.clean_text(plain_summary)

                pdf.set_font("Arial", "B", 14)
                pdf.multi_cell(0, 10, txt=title)
                pdf.ln(5)

                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, txt=plain_summary)
                pdf.ln(10)

                image_url = self.get_image_url(entry)
                if image_url:
                    try:
                        response = requests.get(image_url, timeout=10)
                        response.raise_for_status()

                        img = Image.open(BytesIO(response.content))
                        if img.mode == "RGBA":
                            img = img.convert("RGB")

                        temp_path = f"temp_image_{uuid.uuid4().hex}.jpg"
                        img.save(temp_path, format="JPEG", quality=95)
                        pdf.image(temp_path, x=10, y=pdf.get_y(), w=150)
                        os.remove(temp_path)
                        pdf.ln(15)
                    except Exception:
                        pass

        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        output_path = os.path.join(desktop, "rss_feed.pdf")

        try:
            pdf.output(output_path)
            messagebox.showinfo("Success", f"PDF saved as {output_path}")
            self.open_pdf(output_path)
            self.master.destroy()
        except PermissionError:
            messagebox.showerror(
                "Permission Denied",
                "Close the PDF if it is open or check file permissions."
            )

    def contains_forbidden_words(self, title, content):
        text = f"{title} {content}".lower()
        return any(word.lower() in text for word in self.forbidden_words)

    def get_image_url(self, entry):
        for key in ("media_content", "media_thumbnail", "enclosures"):
            items = entry.get(key, [])
            for item in items:
                url = item.get("url")
                if url and url.startswith("http"):
                    return url

        for link in entry.get("links", []):
            if link.get("type", "").startswith("image"):
                href = link.get("href")
                if href and href.startswith("http"):
                    return href
        return None

    def summarize_text(self, title, text):
        api_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-1.5-flash:generateContent"
        )
        headers = {"Content-Type": "application/json"}
        params = {"key": self.google_api_key}

        prompt = (
            "Summarize the following article in 100–250 words, "
            "preserving important details:\n\n"
            f"{title}\n\n{text}"
        )

        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(
                api_url, headers=headers, params=params, json=payload, timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
        except Exception:
            return "Error summarizing the content."
        finally:
            time.sleep(5)

    def clean_text(self, text):
        return text.encode("latin-1", "replace").decode("latin-1", "replace")

    def open_pdf(self, path):
        system = platform.system()
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.call(["open", path])
        else:
            subprocess.call(["xdg-open", path])


def main():
    root = tk.Tk()
    RSSPDFConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
