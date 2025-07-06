import streamlit as st
import PyPDF2
import io
from pathlib import Path
import zipfile

# Page config
st.set_page_config(
    page_title="PDF Alternative Page Mixer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Tokyo dark theme
st.markdown("""
<style>
    .main > div {
        background-color: #0a0e27;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #0a0e27;
    }
    
    .css-1d391kg {
        background-color: #0a0e27;
    }
    
    .css-18e3th9 {
        background-color: #0a0e27;
    }
    
    .block-container {
        background-color: #0a0e27;
        border: 2px solid #1a1f3a;
        border-radius: 10px;
        padding: 20px;
        margin: 20px;
    }
    
    .title {
        color: #00d4ff;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .section-header {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        background-color: #1a1f3a;
        padding: 10px;
        border-radius: 5px;
    }
    
    .reverse-section {
        background-color: #1a1f3a;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
        text-align: center;
    }
    
    .output-section {
        background-color: #1a1f3a;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }
    
    .start-button {
        background-color: #00d4ff;
        color: #000000;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 10px 30px;
        border-radius: 5px;
        border: none;
        margin: 20px auto;
        display: block;
    }
    
    .status-text {
        text-align: center;
        font-size: 1.1rem;
        margin: 20px 0;
    }
    
    .credit {
        text-align: right;
        font-size: 0.8rem;
        color: #888;
        margin-top: 30px;
    }
    
    .stFileUploader > div {
        background-color: #1a1f3a;
        border: 1px solid #00d4ff;
        border-radius: 5px;
    }
    
    .stCheckbox > div {
        background-color: #1a1f3a;
        color: #ffffff;
    }
    
    .stButton > button {
        background-color: #00d4ff;
        color: #000000;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        background-color: #0099cc;
    }
    
    .stSuccess {
        background-color: #1a1f3a;
        color: #00d4ff;
        border: 1px solid #00d4ff;
    }
    
    .stError {
        background-color: #1a1f3a;
        color: #ff4444;
        border: 1px solid #ff4444;
    }
    
    .stInfo {
        background-color: #1a1f3a;
        color: #ffffff;
        border: 1px solid #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title
    st.markdown('<h1 class="title">PDF Alternative Page Mixer</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'reverse_order' not in st.session_state:
        st.session_state.reverse_order = False
    
    # Create layout columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # PDF 1 Section
        st.markdown('<div class="section-header">PDF 1:</div>', unsafe_allow_html=True)
        pdf1_file = st.file_uploader(
            "Select PDF 1",
            type=['pdf'],
            key="pdf1",
            label_visibility="collapsed"
        )
        
        # PDF 2 Section
        st.markdown('<div class="section-header">PDF 2:</div>', unsafe_allow_html=True)
        pdf2_file = st.file_uploader(
            "Select PDF 2",
            type=['pdf'],
            key="pdf2",
            label_visibility="collapsed"
        )
        
        # Reverse Order Section
        st.markdown('<div class="reverse-section">', unsafe_allow_html=True)
        reverse_order = st.checkbox("☑ Reverse Order (PDF 2)", value=st.session_state.reverse_order)
        st.session_state.reverse_order = reverse_order
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Start Mixing Button
        if st.button("🚀 Start Mixing", use_container_width=True):
            if pdf1_file and pdf2_file:
                try:
                    # Process PDFs
                    result_pdf = mix_pdfs(pdf1_file, pdf2_file, reverse_order)
                    
                    if result_pdf:
                        # Generate filename
                        pdf1_name = Path(pdf1_file.name).stem
                        pdf2_name = Path(pdf2_file.name).stem
                        reverse_suffix = "_reversed" if reverse_order else ""
                        output_filename = f"{pdf1_name}_mixed_{pdf2_name}{reverse_suffix}.pdf"
                        
                        # Provide download button
                        st.success("✅ PDF mixing completed successfully!")
                        st.download_button(
                            label="📥 Download Mixed PDF",
                            data=result_pdf,
                            file_name=output_filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                except Exception as e:
                    st.error(f"❌ Error during mixing: {str(e)}")
            else:
                st.error("⚠️ Please select both PDF files")
        
        # Status
        if pdf1_file and pdf2_file:
            st.markdown('<div class="status-text">Ready to mix PDFs</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-text">Please select PDF files</div>', unsafe_allow_html=True)
    
    with col2:
        # Display file info
        if pdf1_file:
            st.info(f"📄 PDF 1: {pdf1_file.name}")
        else:
            st.info("📄 PDF 1: Not selected")
            
        if pdf2_file:
            st.info(f"📄 PDF 2: {pdf2_file.name}")
        else:
            st.info("📄 PDF 2: Not selected")
            
        # Reverse status
        if reverse_order:
            st.info("🔄 PDF 2 will be reversed")
        else:
            st.info("➡️ PDF 2 normal order")
    
    # Credit
    st.markdown('<div class="credit">Created By Jay Nemlawala</div>', unsafe_allow_html=True)

def mix_pdfs(pdf1_file, pdf2_file, reverse_order):
    """Mix two PDFs alternately"""
    try:
        # Read PDF files
        pdf1_reader = PyPDF2.PdfReader(pdf1_file)
        pdf2_reader = PyPDF2.PdfReader(pdf2_file)
        
        # Get page counts
        pdf1_page_count = len(pdf1_reader.pages)
        pdf2_page_count = len(pdf2_reader.pages)
        
        # Create output PDF writer
        output_writer = PyPDF2.PdfWriter()
        
        # Create page indices for PDF2 (reversed if needed)
        if reverse_order:
            pdf2_indices = list(range(pdf2_page_count - 1, -1, -1))
        else:
            pdf2_indices = list(range(pdf2_page_count))
        
        # Mix pages alternately
        max_pages = max(pdf1_page_count, pdf2_page_count)
        
        for i in range(max_pages):
            # Add page from PDF1 if available
            if i < pdf1_page_count:
                output_writer.add_page(pdf1_reader.pages[i])
                
            # Add page from PDF2 if available
            if i < pdf2_page_count:
                page_index = pdf2_indices[i]
                output_writer.add_page(pdf2_reader.pages[page_index])
        
        # Create bytes buffer
        output_buffer = io.BytesIO()
        output_writer.write(output_buffer)
        output_buffer.seek(0)
        
        return output_buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error processing PDFs: {str(e)}")
        return None

if __name__ == "__main__":
    main()