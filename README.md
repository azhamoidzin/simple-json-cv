# Simple JSON CV 📄

A professional CV builder that generates beautiful HTML and PDF resumes from JSON data. Create stunning, modern CVs with minimal effort using a simple JSON configuration file.

## ✨ Features

- **JSON-based Configuration**: Define your CV data in a simple JSON format
- **Modern Design**: Clean, professional template with responsive design
- **PDF Generation**: Convert your CV to high-quality PDF using Chrome headless
- **SVG Icon Support**: Built-in support for contact icons (email, phone, LinkedIn, etc.)
- **Flexible Structure**: Support for skills, experience, education, and certificates
- **Command Line Interface**: Easy-to-use CLI for quick CV generation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Chrome browser (for PDF generation)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/azhamoidzin/simple-json-cv
   cd simple-json-cv
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or using uv (recommended):
   ```bash
   uv sync
   ```

### Basic Usage

1. **Create your CV data file:**
   ```bash
   cp example_cv.json my_cv.json
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and set your Chrome executable path
   ```

3. **Edit `my_cv.json` with your information**

4. **Generate your CV:**
   ```bash
   python main.py -input=my_cv.json -output-name=output/my_resume
   ```

This will create both `my_resume.html` and `my_resume.pdf` files in the `output/` directory.

## 📋 JSON Structure

Your CV JSON file should follow this structure:

```json
{
  "name": "Your Name",
  "position": "Your Job Title",
  "contacts": [
    {
      "icon": "static/icons/email.svg",
      "link": "mailto:your.email@example.com",
      "text": "your.email@example.com"
    }
  ],
  "summary": "Your professional summary...",
  "skills": [
    {
      "name": "Category Name",
      "skills": ["Skill 1", "Skill 2", "Skill 3"]
    }
  ],
  "education_certificates": [
    {
      "name": "Degree/Certificate Name",
      "date": "Year",
      "description": "Institution and details"
    }
  ],
  "languages": [
    {
      "language": "English",
      "level": "Native"
    },
    {
      "language": "Spanish",
      "level": "Fluent"
    }
  ],
  "experience": [
    {
      "company": "Company Name",
      "project": "Project Name",
      "date_from": "Start Date",
      "date_to": "End Date",
      "position": "Your Position",
      "description": "Brief description",
      "stack": ["Technology 1", "Technology 2"],
      "goals": ["Achievement 1", "Achievement 2"]
    }
  ]
}
```

## 🎨 Available Icons

The project includes pre-built SVG icons for common contact methods:

- `email.svg` - Email address
- `phone.svg` - Phone number
- `linkedin.svg` - LinkedIn profile
- `github.svg` - GitHub profile
- `location.svg` - Location/address
- `telegram.svg` - Telegram contact

## 📖 Command Line Options

```bash
python main.py [options]

Options:
  -input INPUT         Input JSON file (default: cv.json)
  -output-name OUTPUT  Output filename without extension (default: output/cv)
  -h, --help          Show help message

Examples:
  python main.py -input=my_cv.json -output-name=output/my_resume
  python main.py -input=cv.json
  python main.py -output-name=custom_output
```

## 🏗️ Project Structure

```
simple-json-cv/
├── main.py                 # Main application file
├── example_cv.json        # Example CV data
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── templates/
│   ├── cv_template.html   # HTML template
│   └── static/
│       └── icons/         # SVG icons
├── output/                # Generated files
└── README.md             # This file
```

## 🛠️ Development

### Adding Custom Icons

1. Place your SVG files in `templates/static/icons/`
2. Reference them in your JSON: `"icon": "static/icons/your_icon.svg"`
3. The application will automatically embed the SVG content

### Customizing the Template

The HTML template (`templates/cv_template.html`) uses:
- **Jinja2** templating engine
- **Inter font** for modern typography
- **CSS Grid/Flexbox** for responsive layout
- **Custom CSS** for professional styling

### Dependencies

- `jinja2` - Template engine
- `python-dateutil` - Date parsing utilities
- `pyppeteer` - PDF generation via Chrome headless
- `python-dotenv` - Environment variable loading

## 🐛 Troubleshooting

### Common Issues

1. **PDF generation fails:**
   - Ensure Google Chrome is installed
   - Set `CHROME_EXECUTABLE_PATH` in your `.env` file
   - Verify pyppeteer is properly installed
   - Check that the Chrome path in `.env` is correct

2. **Icons not displaying:**
   - Check that SVG files exist in `templates/static/icons/`
   - Verify icon paths in your JSON file
   - Ensure SVG files are valid

3. **Template not found:**
   - Make sure `templates/cv_template.html` exists
   - Check file permissions

### Environment Configuration

Create a `.env` file in the project root to configure Chrome executable path:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and set your Chrome path
CHROME_EXECUTABLE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
```

Common Chrome paths:
- **macOS**: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- **Linux**: `/usr/bin/google-chrome` or `/usr/bin/chromium-browser`
- **Windows**: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Optional Environment Variables

You can also configure Pyppeteer settings:

```bash
# Optional Pyppeteer configuration
PYPPETEER_DOWNLOAD_HOST=https://storage.googleapis.com
PYPPETEER_CHROMIUM_REVISION=1181217
```

## 📄 Output

The application generates:
- **HTML file**: Viewable in any web browser
- **PDF file**: Print-ready, professional format

Both files are saved to the specified output directory with the same base name.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source. Feel free to use and modify as needed.

## 🙏 Acknowledgments

- Built with Python and modern web technologies
- Uses Inter font for typography
- SVG icons for clean, scalable graphics
- Chrome headless for reliable PDF generation

---

**Happy CV building!** 🎉
