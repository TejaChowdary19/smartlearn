#!/usr/bin/env python3
"""
PDF Documentation Generator for SmartLearn Assignment
Converts markdown documentation to PDF format
"""

import os
import subprocess
import sys

def create_pdf():
    print("📚 Creating PDF Documentation for SmartLearn Assignment...")
    
    # Check if required tools are available
    try:
        # Try using pandoc if available
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Pandoc found - using it to create PDF")
            create_pdf_with_pandoc()
            return
    except FileNotFoundError:
        pass
    
    try:
        # Try using wkhtmltopdf if available
        result = subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ wkhtmltopdf found - using it to create PDF")
            create_pdf_with_wkhtmltopdf()
            return
    except FileNotFoundError:
        pass
    
    # Fallback: Create HTML and provide instructions
    print("⚠️  No PDF converter found - creating HTML version")
    create_html_version()

def create_pdf_with_pandoc():
    """Create PDF using pandoc"""
    input_file = "docs/ASSIGNMENT_SUBMISSION.md"
    output_file = "SmartLearn_Assignment_Submission.pdf"
    
    cmd = [
        'pandoc',
        input_file,
        '-o', output_file,
        '--pdf-engine=xelatex',
        '--toc',
        '--number-sections',
        '--variable=geometry:margin=1in',
        '--variable=fontsize:11pt',
        '--variable=mainfont:DejaVu Sans',
        '--variable=monofont:DejaVu Sans Mono'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ PDF created successfully: {output_file}")
        print(f"📁 Location: {os.path.abspath(output_file)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating PDF with pandoc: {e}")
        print("🔄 Falling back to HTML version...")
        create_html_version()

def create_pdf_with_wkhtmltopdf():
    """Create PDF using wkhtmltopdf"""
    input_file = "docs/ASSIGNMENT_SUBMISSION.md"
    html_file = "SmartLearn_Assignment_Submission.html"
    output_file = "SmartLearn_Assignment_Submission.pdf"
    
    # First convert markdown to HTML
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple markdown to HTML conversion
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SmartLearn: AI-Powered Educational Platform</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .mermaid {{ text-align: center; margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
{content.replace('```mermaid', '<div class="mermaid">[Mermaid diagrams will be rendered in PDF]</div>').replace('```', '')}
</body>
</html>
"""
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Convert HTML to PDF
        cmd = [
            'wkhtmltopdf',
            '--page-size', 'A4',
            '--margin-top', '20',
            '--margin-right', '20',
            '--margin-bottom', '20',
            '--margin-left', '20',
            html_file,
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        print(f"✅ PDF created successfully: {output_file}")
        print(f"📁 Location: {os.path.abspath(output_file)}")
        
        # Clean up HTML file
        os.remove(html_file)
        
    except Exception as e:
        print(f"❌ Error creating PDF with wkhtmltopdf: {e}")
        print("🔄 Falling back to HTML version...")
        create_html_version()

def create_html_version():
    """Create HTML version as fallback"""
    input_file = "docs/ASSIGNMENT_SUBMISSION.md"
    output_file = "SmartLearn_Assignment_Submission.html"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SmartLearn: AI-Powered Educational Platform</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        h1 {{ border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; margin-top: 30px; }}
        .mermaid {{ text-align: center; margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 5px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: 'Courier New', monospace; }}
        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; border-left: 4px solid #3498db; }}
        .highlight {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; }}
        .success {{ background-color: #d4edda; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745; }}
        .info {{ background-color: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #17a2b8; }}
    </style>
</head>
<body>
{content.replace('```mermaid', '<div class="mermaid">[Mermaid diagrams will be rendered in PDF]</div>').replace('```', '')}
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML version created: {output_file}")
        print(f"📁 Location: {os.path.abspath(output_file)}")
        print("\n📋 To convert to PDF:")
        print("   1. Open the HTML file in a web browser")
        print("   2. Use 'Print' → 'Save as PDF'")
        print("   3. Or install pandoc: brew install pandoc")
        print("   4. Or install wkhtmltopdf: brew install wkhtmltopdf")
        
    except Exception as e:
        print(f"❌ Error creating HTML version: {e}")

def main():
    print("🚀 SmartLearn Assignment Documentation Generator")
    print("=" * 50)
    
    # Check if markdown file exists
    if not os.path.exists("docs/ASSIGNMENT_SUBMISSION.md"):
        print("❌ ASSIGNMENT_SUBMISSION.md not found!")
        print("   Please ensure the file exists in docs/ directory")
        return
    
    create_pdf()
    
    print("\n🎉 Documentation generation complete!")
    print("\n📚 Files created:")
    print("   - docs/ASSIGNMENT_SUBMISSION.md (Source)")
    print("   - SmartLearn_Assignment_Submission.pdf (PDF for submission)")
    print("   - SmartLearn_Assignment_Submission.html (HTML fallback)")
    
    print("\n📋 Next steps:")
    print("   1. Review the generated PDF")
    print("   2. Submit the PDF with your assignment")
    print("   3. Include the GitHub repository link")
    print("   4. Prepare your video demonstration")

if __name__ == "__main__":
    main()
