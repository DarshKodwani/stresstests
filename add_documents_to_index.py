import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import gc
from dotenv import load_dotenv
import tiktoken
import pandas as pd

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import PyPDF2

load_dotenv()

def extract_pdf_full_document(pdf_path: Path) -> str:
    """Extract text from ALL pages of the PDF"""
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if len(pdf_reader.pages) == 0:
                return ""
            
            pages_to_process = len(pdf_reader.pages)
            print(f"📊 Processing ALL {pages_to_process} pages...")
            
            text = ""
            
            for page_num in range(pages_to_process):
                try:
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    # Progress indicator and memory cleanup every 10 pages
                    if (page_num + 1) % 10 == 0:
                        print(f"   📄 Processed {page_num + 1}/{pages_to_process} pages")
                        gc.collect()  # Memory cleanup
                        
                except Exception as e:
                    print(f"⚠️ Warning: Could not extract page {page_num + 1}: {e}")
            
            print(f"✅ Extracted {len(text)} characters from {pages_to_process} pages")
            return text.strip()
            
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        return ""

def extract_excel_content(excel_path: Path) -> str:
    """Extract text content from Excel file"""
    print(f"📊 Extracting Excel content from: {excel_path.name}")
    
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(excel_path)
        content_parts = []
        
        print(f"📋 Found {len(excel_file.sheet_names)} sheets: {', '.join(excel_file.sheet_names)}")
        
        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                
                # Add sheet header
                content_parts.append(f"\n=== SHEET: {sheet_name} ===\n")
                
                # Convert DataFrame to string representation
                if not df.empty:
                    # Get column info
                    content_parts.append(f"Columns: {', '.join(df.columns.astype(str))}\n")
                    
                    # Add first few rows as sample data
                    sample_rows = min(20, len(df))  # Limit to 20 rows per sheet
                    content_parts.append(f"Sample data ({sample_rows} of {len(df)} rows):\n")
                    content_parts.append(df.head(sample_rows).to_string(index=False))
                    content_parts.append("\n")
                    
                    # Add summary statistics if numeric columns exist
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        content_parts.append(f"\nNumeric summary for {len(numeric_cols)} columns:\n")
                        content_parts.append(df[numeric_cols].describe().to_string())
                        content_parts.append("\n")
                else:
                    content_parts.append("(Empty sheet)\n")
                    
            except Exception as e:
                print(f"⚠️ Warning: Could not read sheet '{sheet_name}': {e}")
                content_parts.append(f"\n=== SHEET: {sheet_name} (ERROR) ===\nError reading sheet: {e}\n")
        
        content = ''.join(content_parts)
        print(f"✅ Extracted {len(content)} characters from Excel file")
        return content.strip()
        
    except Exception as e:
        print(f"❌ Error extracting Excel: {e}")
        return ""

def extract_csv_content(csv_path: Path) -> str:
    """Extract text content from CSV file"""
    print(f"📈 Extracting CSV content from: {csv_path.name}")
    
    try:
        df = pd.read_csv(csv_path)
        content_parts = []
        
        # Add file info
        content_parts.append(f"CSV File: {csv_path.name}\n")
        content_parts.append(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n\n")
        
        # Add column info
        content_parts.append(f"Columns: {', '.join(df.columns.astype(str))}\n\n")
        
        # Add sample data (first 25 rows)
        sample_rows = min(25, len(df))
        content_parts.append(f"Sample data (first {sample_rows} of {df.shape[0]} rows):\n")
        content_parts.append(df.head(sample_rows).to_string(index=False))
        content_parts.append("\n\n")
        
        # Add summary statistics if numeric columns exist
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            content_parts.append(f"Summary statistics for {len(numeric_cols)} numeric columns:\n")
            content_parts.append(df[numeric_cols].describe().to_string())
            content_parts.append("\n\n")
        
        # Add info about categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            content_parts.append(f"Categorical columns ({len(categorical_cols)}):\n")
            for col in categorical_cols:
                unique_vals = df[col].nunique()
                content_parts.append(f"  {col}: {unique_vals} unique values")
                if unique_vals <= 10:  # Show values if not too many
                    content_parts.append(f" -> {', '.join(df[col].dropna().unique().astype(str)[:10])}")
                content_parts.append("\n")
        
        content = ''.join(content_parts)
        print(f"✅ Extracted {len(content)} characters from CSV file")
        return content.strip()
        
    except Exception as e:
        print(f"❌ Error extracting CSV: {e}")
        return ""

def chunk_text(text: str, max_tokens: int = 800, overlap: int = 150) -> List[str]:
    """Split text into overlapping chunks - optimized for mixed document types"""
    print(f"🔧 Chunking text into {max_tokens}-token pieces with {overlap}-token overlap...")
    
    try:
        tokenizer = tiktoken.encoding_for_model("gpt-4")
        tokens = tokenizer.encode(text)
        
        print(f"📊 Total tokens to process: {len(tokens)}")
        
        if len(tokens) <= max_tokens:
            print(f"✅ Text fits in single chunk ({len(tokens)} tokens)")
            return [text]
        
        chunks = []
        start = 0
        chunk_num = 0
        max_chunks = 2000  # Reasonable limit for mixed document types
        
        while start < len(tokens) and chunk_num < max_chunks:
            end = min(start + max_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            chunk_num += 1
            if chunk_num % 50 == 0:  # Progress every 50 chunks
                print(f"   🔧 Created {chunk_num} chunks... ({start}/{len(tokens)} tokens)")
                gc.collect()  # Memory cleanup
            
            # Fixed overlap logic - ensure we always make progress
            start = end - overlap
            if start >= end - overlap:  # Safety check
                start = end
                
            if start >= len(tokens):
                break
        
        if chunk_num >= max_chunks:
            print(f"⚠️ WARNING: Hit chunk limit of {max_chunks}. Document truncated.")
        
        print(f"✅ Created {len(chunks)} chunks total")
        return chunks
        
    except Exception as e:
        print(f"❌ Error chunking text: {e}")
        return [text]  # Return original text as fallback

def get_embeddings(text: str, openai_client, model: str) -> List[float]:
    """Generate embeddings for text"""
    try:
        print(f"🔄 Generating embeddings for {len(text)} characters...")
        response = openai_client.embeddings.create(
            input=text,
            model=model
        )
        print("✅ Embeddings generated successfully")
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return []

def get_document_metadata(file_path: Path) -> Dict[str, Any]:
    """Extract metadata based on filename patterns"""
    filename = file_path.name.lower()
    
    # Default metadata
    metadata = {
        'institution': 'Unknown',
        'document_type': 'Financial Document',
        'year': 2024,
        'tags': 'financial,document'
    }
    
    # BOE documents
    if 'boe' in filename or 'bank-of-england' in filename:
        metadata['institution'] = 'Bank of England'
        if 'stress-test' in filename:
            metadata['document_type'] = 'Stress Test'
            metadata['tags'] = 'stress-test,boe,bank-of-england'
        elif 'climate' in filename:
            metadata['document_type'] = 'Climate Stress Test'
            metadata['tags'] = 'climate,stress-test,boe'
        elif 'framework' in filename:
            metadata['document_type'] = 'Framework Manual'
            metadata['tags'] = 'framework,manual,boe'
    
    # Fed documents
    elif 'fed' in filename or 'dfast' in filename:
        metadata['institution'] = 'Federal Reserve'
        metadata['document_type'] = 'DFAST Results'
        metadata['tags'] = 'fed,dfast,stress-test,federal-reserve'
    
    # BIS documents
    elif 'bis' in filename:
        metadata['institution'] = 'Bank for International Settlements'
        metadata['document_type'] = 'BIS Report'
        metadata['tags'] = 'bis,international,banking'
        
    # Basel documents
    elif 'basel' in filename:
        metadata['institution'] = 'Basel Committee'
        metadata['document_type'] = 'Basel III Report'
        metadata['tags'] = 'basel,basel-iii,regulation'
        
    # IMF documents
    elif 'imf' in filename or 'gfsr' in filename:
        metadata['institution'] = 'International Monetary Fund'
        metadata['document_type'] = 'GFSR Report'
        metadata['tags'] = 'imf,gfsr,financial-stability'
        
    # FRED data
    elif 'fred' in filename:
        metadata['institution'] = 'Federal Reserve Economic Data'
        metadata['document_type'] = 'Economic Data'
        metadata['tags'] = 'fred,economic-data,time-series'
    
    # Extract year from filename if possible
    import re
    year_match = re.search(r'20\d{2}', filename)
    if year_match:
        metadata['year'] = int(year_match.group())
    
    return metadata

def main():
    print("🚀 Adding ALL Financial Documents to Azure AI Search Vector Index")
    print("=" * 70)
    
    FINANCIAL_DATA_DIR = Path("financial_data")
    INDEX_NAME = "financial-stress-test-index"
    
    # Supported file types
    SUPPORTED_EXTENSIONS = {'.pdf', '.xlsx', '.csv'}
    
    # Check environment variables
    required_vars = [
        'AZURE_SEARCH_ENDPOINT',
        'AZURE_SEARCH_KEY', 
        'AZURE_OPENAI_EMBEDDINGS_ENDPOINT',
        'AZURE_OPENAI_EMBEDDINGS_API_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return
    
    print("🔧 Initializing Azure clients...")
    
    # Initialize clients
    search_client = SearchClient(
        endpoint=os.getenv('AZURE_SEARCH_ENDPOINT'),
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY'))
    )
    
    openai_client = AzureOpenAI(
        azure_endpoint=os.getenv('AZURE_OPENAI_EMBEDDINGS_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_EMBEDDINGS_API_KEY'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-01')
    )
    
    embedding_model = os.getenv('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME', 'text-embedding-3-large')
    
    # Check if directory exists
    if not FINANCIAL_DATA_DIR.exists():
        print(f"❌ Directory not found: {FINANCIAL_DATA_DIR}")
        return
    
    # Find all supported files
    all_files = []
    for ext in SUPPORTED_EXTENSIONS:
        files = list(FINANCIAL_DATA_DIR.glob(f"*{ext}"))
        all_files.extend(files)
    
    # Filter out non-document files
    document_files = []
    for file_path in all_files:
        if file_path.name.lower() not in ['document_inventory.json', 'document_inventory.md']:
            document_files.append(file_path)
    
    if not document_files:
        print(f"❌ No supported documents found in {FINANCIAL_DATA_DIR}")
        return
    
    print(f"📂 Found {len(document_files)} documents to process:")
    for i, file_path in enumerate(document_files, 1):
        print(f"   {i:2d}. {file_path.name} ({file_path.suffix.upper()})")
    
    print(f"\n🔄 Starting document processing...")
    
    all_documents = []
    processed_files = 0
    
    for file_index, file_path in enumerate(document_files, 1):
        print(f"\n{'='*60}")
        print(f"� Processing {file_index}/{len(document_files)}: {file_path.name}")
        print(f"{'='*60}")
        
        try:
            # Extract text based on file type
            text = ""
            if file_path.suffix.lower() == '.pdf':
                text = extract_pdf_full_document(file_path)
            elif file_path.suffix.lower() == '.xlsx':
                text = extract_excel_content(file_path)
            elif file_path.suffix.lower() == '.csv':
                text = extract_csv_content(file_path)
            
            if not text:
                print(f"⚠️ Skipping {file_path.name} - no text extracted")
                continue
            
            print(f"📝 Total text length: {len(text)} characters")
            
            # Get document metadata
            metadata = get_document_metadata(file_path)
            
            # Chunk the text
            chunks = chunk_text(text, max_tokens=800, overlap=150)
            print(f"📦 Created {len(chunks)} chunks for processing")
            
            # Process each chunk
            file_documents = []
            for i, chunk in enumerate(chunks):
                print(f"🔄 Processing chunk {i+1}/{len(chunks)} for {file_path.name}...")
                
                # Generate unique ID
                chunk_suffix = f"_chunk{i}" if len(chunks) > 1 else "_single"
                doc_id = hashlib.md5(f"{file_path.name}{chunk_suffix}".encode()).hexdigest()
                
                # Generate embeddings
                embeddings = get_embeddings(chunk, openai_client, embedding_model)
                if not embeddings:
                    print(f"⚠️ Skipping chunk {i+1} - no embeddings")
                    continue
                
                # Create document
                if len(chunks) > 1:
                    title_suffix = f" (Chunk {i+1}/{len(chunks)})"
                    summary = f"Chunk {i+1} of {len(chunks)} from {file_path.name}"
                else:
                    title_suffix = ""
                    summary = f"Complete content from {file_path.name}"
                
                document = {
                    'id': doc_id,
                    'title': f"{file_path.name}{title_suffix}",
                    'content': chunk,
                    'summary': summary,
                    'document_type': metadata['document_type'],
                    'institution': metadata['institution'], 
                    'year': metadata['year'],
                    'file_format': file_path.suffix.upper().replace('.', ''),
                    'tags': metadata['tags'],
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'file_path': str(file_path),
                    'file_size': file_path.stat().st_size,
                    'created_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    'relevance_score': len(chunk.split()) / 1000.0,
                    'content_vector': embeddings
                }
                
                file_documents.append(document)
                print(f"✅ Created document for chunk {i+1}")
                
                # Memory cleanup every few chunks
                if (i + 1) % 3 == 0:
                    gc.collect()
            
            all_documents.extend(file_documents)
            processed_files += 1
            
            print(f"✅ Completed {file_path.name}: {len(file_documents)} chunks ready for upload")
            print(f"📊 Progress: {processed_files}/{len(document_files)} files processed")
            
            # Major cleanup after each file
            gc.collect()
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            continue
    
    # Upload all documents in batches
    if all_documents:
        print(f"\n{'='*60}")
        print(f"📤 UPLOADING {len(all_documents)} DOCUMENTS TO INDEX")
        print(f"{'='*60}")
        
        batch_size = 8  # Smaller batches for mixed document types
        total_uploaded = 0
        
        for i in range(0, len(all_documents), batch_size):
            batch = all_documents[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(all_documents) + batch_size - 1) // batch_size
            
            print(f"📤 Uploading batch {batch_num}/{total_batches} ({len(batch)} documents)...")
            
            try:
                result = search_client.upload_documents(documents=batch)
                
                success_count = sum(1 for r in result if r.succeeded)
                error_count = len(batch) - success_count
                total_uploaded += success_count
                
                if error_count > 0:
                    print(f"⚠️ Batch {batch_num}: {success_count} succeeded, {error_count} failed")
                    for r in result:
                        if not r.succeeded:
                            print(f"   ❌ Error: {r.error_message}")
                else:
                    print(f"✅ Batch {batch_num}: {success_count} documents uploaded")
                    
                gc.collect()  # Memory cleanup after each batch
                    
            except Exception as e:
                print(f"❌ Error uploading batch {batch_num}: {e}")
        
        print(f"\n🎉 UPLOAD COMPLETED!")
        print(f"📊 Final Summary:")
        print(f"   📄 Files processed: {processed_files}/{len(document_files)}")
        print(f"   � Total documents uploaded: {total_uploaded}/{len(all_documents)}")
        print(f"   🏦 Index: {INDEX_NAME}")
        print(f"   🔍 Ready for vector search across all financial documents!")
    else:
        print("❌ No documents to upload")
    
    # Final cleanup
    gc.collect()
    print("🎉 Multi-document processing completed!")

if __name__ == "__main__":
    main()
