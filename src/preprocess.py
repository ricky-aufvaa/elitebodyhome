import os
import glob
import pickle
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings

model_name ="amazon.titan-embed-text-v2:0"
embedding_function = BedrockEmbeddings()
# model_name = "sentence-transformers/all-mpnet-base-v2"
# model_kwargs = {"device": "cpu"}
# encode_kwargs = {"normalize_embeddings": False}
# embedding_function = HuggingFaceEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs,
# )
def process_all_markdown_files():
    """
    Process all markdown files in the pages folder and create Document objects
    """
    # Get all markdown files in the pages folder
    md_files = glob.glob("pages/*.md")
    print(f"Found {len(md_files)} markdown files to process")
    
    # Headers to split on
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        # ("###", "Header 3"),
        # ("####", "Header 4"),
    ]
    
    # Initialize splitters
    markdown_splitter = MarkdownHeaderTextSplitter(
        strip_headers=False, headers_to_split_on=headers_to_split_on
    )
    
    chunk_size = 1000
    chunk_overlap = 300
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    
    # List to store all documents
    all_documents = []
    
    # Process each markdown file
    for file_path in sorted(md_files):
        print(f"Processing: {file_path}")
        
        try:
            # Read the markdown file
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_document = f.read()
            
            # Skip empty files
            if not markdown_document.strip():
                print(f"  Skipping empty file: {file_path}")
                continue
            
            # Split by markdown headers first
            md_header_splits = markdown_splitter.split_text(markdown_document)
            
            # Add source file metadata to each split
            for split in md_header_splits:
                if hasattr(split, 'metadata'):
                    split.metadata['source_file'] = file_path
                else:
                    # If it's a string, convert to Document-like object
                    from langchain.schema import Document
                    split = Document(page_content=split, metadata={'source_file': file_path})
            
            # Further split by character count
            splits = text_splitter.split_documents(md_header_splits)
            
            # Add to our collection
            all_documents.extend(splits)
            
            print(f"  Created {len(splits)} document chunks from {file_path}")
            
        except Exception as e:
            print(f"  Error processing {file_path}: {e}")
            continue
    
    print(f"\nTotal documents created: {len(all_documents)}")
    
    # Save to pickle file for debugging
    with open("all_documents.pkl", "wb") as f:
        pickle.dump(all_documents, f)
    print("Documents saved to 'all_documents.pkl'")
    
    # Also save a readable text version for debugging
    with open("all_documents_debug.txt", "w", encoding="utf-8") as f:
        f.write(f"Total Documents: {len(all_documents)}\n")
        f.write("=" * 80 + "\n\n")
        
        for idx, doc in enumerate(all_documents):
            f.write(f"Document {idx + 1}:\n")
            f.write(f"Source: {doc.metadata.get('source_file', 'Unknown')}\n")
            f.write(f"Metadata: {doc.metadata}\n")
            f.write(f"Content Length: {len(doc.page_content)} characters\n")
            f.write(f"Content Preview: {doc.page_content[:200]}...\n")
            f.write("-" * 80 + "\n\n")
    
    print("Debug information saved to 'all_documents_debug.txt'")
    
    return all_documents

if __name__ == "__main__":
    # Process all files
    # documents = process_all_markdown_files()
    embeddigns = FAISS.load_local("faiss_embeddings",embeddings=embedding_function,allow_dangerous_deserialization=True)
    print(embeddigns)
    
    # Print summary
    # print(f"\nSummary:")
    # print(f"Total documents: {len(documents)}")
    
    # if documents:
    #     print(f"\nCreating embeddings for all {len(documents)} documents...")
        
    #     # Create FAISS embeddings from ALL documents
    #     # db = FAISS.from_documents(documents, embedding_function)
        
    #     # Save the FAISS index locally
    #     # db.save_local("faiss_embeddings")

        
    #     print(f"FAISS embeddings saved locally to 'faiss_embeddings' directory")
    #     print(f"Total vectors in index: {db.index.ntotal}")
        
    #     # Show first few documents as examples
    #     print(f"\nFirst 3 documents that were embedded:")
    #     for i, doc in enumerate(documents[:3]):
    #         print(f"\nDocument {i+1}:")
    #         print(f"  Source: {doc.metadata.get('source_file', 'Unknown')}")
    #         print(f"  Content length: {len(doc.page_content)}")
    #         print(f"  Content preview: {doc.page_content[:100]}...")
    # else:
    #     print("No documents found to embed!")
