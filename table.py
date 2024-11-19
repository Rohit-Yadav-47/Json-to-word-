import json
import streamlit as st
from docx import Document
from io import BytesIO
import base64

# Function to create the question tables document
def create_question_tables(data):
    doc = Document()

    for question in data:
        # Create a table with 2 columns for metadata
        table = doc.add_table(rows=0, cols=2)
        table.style = 'Table Grid'

        # Add metadata rows
        rows = [
            ("Grade", str(question["Grade"])),
            ("Domain", question["Domain"]),
            ("Standard/Core Concept", question["Standard/Core Concept"]),
            ("Question Type", question["Question Type"]),
            ("Difficulty Level", question["Difficulty Level"]),
            ("Cognitive Dimension (Bloom's Level)", question["Cognitive Dimension (Bloom's Level)"] ),
            ("Question ID", question["Question ID"]),
            ("Title (Stem and Prompt)", question["Title (Stem and Prompt)"])
        ]

        for category, detail in rows:
            row = table.add_row()
            row.cells[0].text = category
            row.cells[1].text = detail

        # Add a separate 4-column section for options
        options_table = doc.add_table(rows=1, cols=4)
        options_table.style = 'Table Grid'

        # Add headers for the options table
        hdr_cells = options_table.rows[0].cells
        hdr_cells[0].text = "Option"
        hdr_cells[1].text = "Text"
        hdr_cells[2].text = "Type of Distractor"
        hdr_cells[3].text = "Distractor Rationale"

        # Add options rows
        for option in question["Options"]:
            row = options_table.add_row()
            row.cells[0].text = option.get("Option", "N/A")
            row.cells[1].text = option.get("Text", "N/A")
            row.cells[2].text = option.get("Type of Distractor", "N/A")
            row.cells[3].text = option.get("Distractor Rationale", "N/A")

        # Add a new table for Hint and Solution
        bottom_table = doc.add_table(rows=0, cols=2)
        bottom_table.style = 'Table Grid'

        # Add bottom rows
        bottom_rows = [
            ("Hint", question["Hint"]),
            ("Solution", question["Solution"])
        ]

        for category, detail in bottom_rows:
            row = bottom_table.add_row()
            row.cells[0].text = category
            row.cells[1].text = detail

        # Add a page break after each question
        doc.add_page_break()

    # Save the document to a BytesIO object
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

# Function to create a download link
def create_download_link(file_stream, filename):
    b64 = base64.b64encode(file_stream.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download the generated document</a>'
    return href

# Streamlit app layout
def main():
    st.title("Question Table Generator")
    st.markdown("### Paste the JSON data below to generate the Google Doc-style output")

    # JSON input from user
    json_input = st.text_area("Enter JSON Data:", height=350)

    if st.button("Generate Document"):
        try:
            # Parse JSON input
            data = json.loads(json_input)

            # Create document
            file_stream = create_question_tables(data)

            # Create download link
            st.success("Document generated successfully!")
            download_link = create_download_link(file_stream, "Generated_Questions.docx")
            st.markdown(download_link, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
