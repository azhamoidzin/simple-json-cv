#!/usr/bin/env python3
"""
Simple JSON CV - Generate professional PDF resumes from JSON data
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import base64
import asyncio

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional, continue without it
    print("Warning: dotenv is not installed. Please install it with: pip install python-dotenv")

from jinja2 import Environment, FileSystemLoader
from dateutil import parser

# Import pyppeteer for PDF generation
try:
    if not (CHROME_EXECUTABLE_PATH := os.getenv('CHROME_EXECUTABLE_PATH')):
        print("Error: CHROME_EXECUTABLE_PATH is not set. Please set it in the environment variables.")
        sys.exit(1)
    from pyppeteer import launch
    PYUPPETEER_AVAILABLE = True
except ImportError:
    PYUPPETEER_AVAILABLE = False
    print("Error: Pyppeteer is required for PDF generation. Install it with: pip install pyppeteer")
    sys.exit(1)


class SimpleJSONCV:
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)
        
        # Create static folder for icons
        static_dir = self.template_dir / "static" / "icons"
        static_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy static icons if they exist in project root
        project_static = Path("static/icons")
        if project_static.exists():
            import shutil
            for icon_file in project_static.glob("*"):
                if icon_file.is_file():
                    shutil.copy2(icon_file, static_dir / icon_file.name)
        
        # Initialize Jinja2 environment after template is created
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        
        # Add custom filters
        def b64encode_filter(s):
            if isinstance(s, str):
                return base64.b64encode(s.encode('utf-8')).decode('utf-8')
            return ''
        
        self.env.filters['b64encode'] = b64encode_filter
    
 
    def load_cv_data(self, json_file: str) -> Dict[str, Any]:
        """Load CV data from JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            print(f"Error: File '{json_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{json_file}': {e}")
            sys.exit(1)
    
    def generate_html(self, cv_data: Dict[str, Any]) -> str:
        """Generate HTML from CV data using Jinja2 template"""
        template = self.env.get_template("cv_template.html")
        
        # Separate education and certificates
        education_certificates = []
        certificates = []
        
        for item in cv_data.get('education_certificates', []):
            education_certificates.append(item)
        # Prepare template context
        context = {
            'name': cv_data.get('name', ''),
            'position': cv_data.get('position', ''),
            'contacts': cv_data.get('contacts', []),
            'summary': cv_data.get('summary', ''),
            'skills': cv_data.get('skills', []),
            'education_certificates': education_certificates,
            'languages': cv_data.get('languages', []),
            'experience': cv_data.get('experience', []),
            'cv_icon': cv_data.get('cv_icon', '')
        }
        
        
        return template.render(**context)
    
    async def generate_pdf_pyppeteer(self, html_file_path: str, output_file: str):
        """Convert HTML to PDF using Pyppeteer (Chrome headless)"""
        try:
            browser = await launch(executablePath=CHROME_EXECUTABLE_PATH)
            page = await browser.newPage()
            
            # Convert file path to file:// URL
            file_url = f"file://{Path(html_file_path).absolute()}"
            await page.goto(file_url)
            
            await page.pdf({'path': output_file, 'format': 'A4'})
            await browser.close()
            
            print(f"PDF generated successfully: {output_file}")
            return True
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def generate_pdf(self, html_content: str, output_file: str):
        """Convert HTML to PDF using Pyppeteer"""
        # Save HTML to temporary file for Pyppeteer
        html_file = output_file.replace('.pdf', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Run Pyppeteer in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            success = loop.run_until_complete(self.generate_pdf_pyppeteer(html_file, output_file))
            if not success:
                sys.exit(1)
        finally:
            loop.close()


    def build_cv(self, json_file: str, output_file_name: str = None):
        """Main method to build CV from JSON to PDF"""
        if output_file_name is None:
            output_file_name = f"output/cv"
        
        print(f"Loading CV data from {json_file}...")
        cv_data = self.load_cv_data(json_file)
        
        # Embed SVG icons into the CV data
        cv_data = self._embed_svg_icons(cv_data)
        
        print("Generating HTML...")
        html_content = self.generate_html(cv_data)
        
        if not os.path.exists(output_file_name):
            os.makedirs(os.path.dirname(output_file_name))
            
        # Save HTML to output file
        with open(output_file_name + ".html", "w", encoding="utf-8") as f:
            f.write(html_content)
                
        print("Converting to PDF...")
        self.generate_pdf(html_content, output_file_name + ".pdf")
        
        print("CV generation completed!")

    def _embed_svg_icons(self, cv_data: dict) -> dict:
        """Read SVG files and embed their content directly into the CV data"""
        # Embed CV icon
        cv_icon_path = Path("templates/static/icons/cv.svg")
        if cv_icon_path.exists():
            try:
                with open(cv_icon_path, 'r', encoding='utf-8') as f:
                    cv_icon_content = f.read().strip()
                cv_data['cv_icon'] = cv_icon_content
                print(f"Embedded CV icon: {cv_icon_path.name}")
            except Exception as e:
                print(f"Warning: Could not read CV icon file: {e}")
                cv_data['cv_icon'] = ""
        else:
            print(f"Warning: CV icon file not found: {cv_icon_path}")
            cv_data['cv_icon'] = ""
        
        # Embed contact icons
        if 'contacts' in cv_data:
            for contact in cv_data['contacts']:
                if 'icon' in contact and contact['icon']:
                    # Check if icon is a file path
                    if contact['icon'].startswith('static/icons/') or contact['icon'].startswith('templates/static/icons/'):
                        # Try to read the SVG file
                        svg_path = Path(contact['icon'])
                        if not svg_path.exists():
                            # Try alternative paths
                            alt_paths = [
                                Path(contact['icon']),
                                Path("static/icons") / Path(contact['icon']).name,
                                Path("templates/static/icons") / Path(contact['icon']).name
                            ]
                            
                            svg_path = None
                            for path in alt_paths:
                                if path.exists():
                                    svg_path = path
                                    break
                        
                        if svg_path and svg_path.exists():
                            try:
                                with open(svg_path, 'r', encoding='utf-8') as f:
                                    svg_content = f.read().strip()
                                # Replace the icon path with the actual SVG content
                                contact['icon'] = svg_content
                                print(f"Embedded SVG icon: {svg_path.name}")
                            except Exception as e:
                                print(f"Warning: Could not read SVG file {svg_path}: {e}")
                                # Keep the original path as fallback
                        else:
                            print(f"Warning: SVG file not found for icon: {contact['icon']}")
        
        return cv_data


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Simple JSON CV - Generate professional HTML resumes from JSON data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -input=cv.json -output=my_resume.html
  python main.py -input=my_cv.json
  python main.py -output=custom_output.html
        """
    )
    
    parser.add_argument(
        "-input", 
        default="cv.json",
        help="Input JSON file (default: cv.json)"
    )
    
    parser.add_argument(
        "-output-name", 
        default="output/cv",
        help="Output filename (default: output/cv)"
    )
    
    
    args = parser.parse_args()

    
    json_file = args.input
    output_file_name = args.output_name
    
    cv_builder = SimpleJSONCV()
    cv_builder.build_cv(json_file, output_file_name)


if __name__ == "__main__":
    main()
