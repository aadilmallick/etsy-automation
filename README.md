# Gumroad Sheet Music Automation

A Python automation tool that streamlines the process of creating and publishing piano sheet music product listings on Gumroad using AI-powered content generation and Selenium browser automation.

## Motivation

Manually creating product listings for hundreds of sheet music PDFs on Gumroad is time-consuming and repetitive. Each listing requires:
- Writing compelling product titles and descriptions
- Creating attractive thumbnails and cover images
- Filling out forms with pricing, tags, categories, and metadata
- Uploading files and configuring product settings

This tool automates the entire workflow, enabling you to list sheet music at scale while maintaining quality through AI-generated content and professional-looking visuals.

## What It Does

This automation tool:

1. **AI-Powered Content Generation**: Uses Google's Gemini AI to generate:
   - Product titles from PDF filenames
   - SEO-optimized product descriptions
   - URL-friendly slugs

2. **Automatic Image Creation**: Generates professional product visuals:
   - Thumbnails (600x600px) with the first page of the sheet music
   - Cover images with scaled sheet music previews
   - Uses custom background templates for consistent branding

3. **End-to-End Gumroad Automation**: Automates the complete product creation workflow:
   - Navigates Gumroad's product creation interface
   - Fills out all required fields (name, price, description, slug)
   - Uploads thumbnails, covers, and PDF files
   - Configures tags, categories, and Gumroad Discover settings
   - Publishes products automatically

## Main Application Flow

```
1. Initialize Selenium with Chrome user profile (to maintain login session)
   ↓
2. Scan sheetmusic/ directory for PDF files
   ↓
3. For each PDF file:
   ├─ Extract first page as image using PyMuPDF
   ├─ Generate thumbnail and cover images with custom backgrounds
   ├─ Use Gemini AI to create product name, description, and slug
   ├─ Navigate to Gumroad's product creation page
   ├─ Fill product name and price ($2.99)
   ├─ Submit initial form and navigate to details page
   ├─ Add AI-generated description
   ├─ Upload thumbnail and cover images
   ├─ Add encouragement message and upload PDF file
   ├─ Configure tags: "sheet music", "piano sheet music", "piano solo", etc.
   ├─ Set category: "Music & Sound Design > Sound Design > Sheet Music"
   ├─ Enable Gumroad Discover with 50% fee
   └─ Save and publish the product
   ↓
4. Repeat for all sheet music files
```

## Setup

### Prerequisites

- Python 3.7+
- Google Chrome browser
- Gumroad account (must be logged in)
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aadilmallick/etsy-automation.git
cd etsy-automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

4. Prepare your files:
   - Place sheet music PDFs in the `sheetmusic/` directory
   - Add custom background images: `thumbnail-background.jpg` and `cover-background.jpg`

### Usage

Run the automation:
```bash
python app.py
```

**Important**: Close all Chrome browser windows before running the script. The tool uses Chrome's user data directory to maintain your logged-in Gumroad session.

## Key Features

- **Batch Processing**: Process hundreds of sheet music files automatically
- **AI Content Generation**: Professional product descriptions with SEO optimization
- **Custom Thumbnails**: Automatically generated product images
- **Consistent Pricing**: Fixed pricing ($2.99) for competitive pricing
- **Tag Automation**: Automatic tagging with relevant keywords
- **Gumroad Discover**: Automatic enrollment with configurable commission
- **Error Handling**: Configurable element detection with failure notifications

## Technical Details

### Core Components

- `app.py` - Main entry point that orchestrates the automation loop
- `automation.py` - Selenium automation logic for Gumroad interaction
- `ai.py` - Google Gemini AI integration for content generation
- `thumbnail_helpers.py` - Image processing for thumbnails and covers
- `selenium_lib/` - Reusable Selenium wrapper classes

### Gumroad API Endpoints (Reference)

- `POST https://app.gumroad.com/links/ekulr` - Save a product
- `POST https://app.gumroad.com/links/ekulr/publish` - Publish a product
- `GET https://app.gumroad.com/checkout/upsells/products` - Get products list
- `POST https://app.gumroad.com/links` - Create a product
- `POST https://app.gumroad.com/rails/active_storage/direct_uploads` - Upload a file
- `POST https://app.gumroad.com/links/mdezde/thumbnails` - Upload a thumbnail

## Important Notes

⚠️ **Chrome with user data directory doesn't work unless all Chrome windows are closed first.**

## License

This project is provided as-is for educational and automation purposes.
