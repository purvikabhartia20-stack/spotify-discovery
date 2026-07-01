import os
import markdown2
from fpdf import FPDF

def export_report_to_pdf(markdown_path, pdf_path):
    if not os.path.exists(markdown_path):
        return False
        
    with open(markdown_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    # Convert MD to HTML
    # We replace unsupported unicode chars to avoid FPDF helvetica errors
    md_text = md_text.encode('latin-1', 'replace').decode('latin-1')
    html = markdown2.markdown(md_text, extras=["tables"])
    
    # FPDF2 supports writing HTML
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Simple CSS mapping in FPDF
    pdf.set_font("helvetica", size=12)
    
    try:
        # write_html will parse the HTML string
        pdf.write_html(html)
        pdf.output(pdf_path)
        return True
    except Exception as e:
        print(f"Error exporting PDF: {e}")
        return False

if __name__ == "__main__":
    import glob
    reports = glob.glob('reports/*.md')
    if reports:
        latest = sorted(reports)[-1]
        pdf_out = latest.replace('.md', '.pdf')
        if export_report_to_pdf(latest, pdf_out):
            print(f"Exported to {pdf_out}")
