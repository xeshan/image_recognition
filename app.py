import streamlit as st
from PIL import Image
import os
import pandas as pd
import pytesseract
import fitz

# Set browser title and favicon
st.set_page_config(page_title="Pokemon Card Recognition", page_icon="🔍")

# Read the README file
with open('README.md', 'r') as file:
    readme_text = file.read()

def main():
    st.title("Pokemon Card Image Recognition")

    if st.button("Run Image Recognition"):
        pdf_directory = "images"

        if not os.path.exists(pdf_directory):
            st.warning("Directory not found.")
        else:
            st.balloons()
            data = []
            pdf_files = [file for file in os.listdir(pdf_directory) if file.lower().endswith('.pdf')]
            if pdf_files:
                st.write("PDF files found in the directory:")
                for pdf_file in pdf_files:
                    st.write(pdf_file)
                    pdf_path = os.path.join(pdf_directory, pdf_file)

                    pdf_document = fitz.open(pdf_path)
                    page = pdf_document[0]  # Assuming you want to process the first page
                    image_list = page.get_images(full=True)

                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_data = base_image["image"]

                        pixmap = fitz.Pixmap(image_data)
                        pil_image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)

                        # Perform image recognition using pytesseract
                        extracted_text = pytesseract.image_to_string(pil_image)
                        data.append(extracted_text.strip())

                # Create a DataFrame from the extracted data
                df = pd.DataFrame(data, columns=["Extracted Text"])
                st.write(df)
            else:
                st.warning("No PDF files found in the directory.")

    # Display README Documentation using an expander
    readme_expander = st.expander("📖 README Documentation")
    with readme_expander:
        st.markdown(readme_text)

    # Display prompts from this conversation using an expander
    prompts_expander = st.expander("🚀 Prompts from This Conversation")
    prompts_url = "https://chat.openai.com/share/51b3b640-96c5-49bf-a155-888fa96d0c8d"
    prompts_text = f"[Click here to view the prompts]({prompts_url})"
    with prompts_expander:
        st.markdown(prompts_text, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
