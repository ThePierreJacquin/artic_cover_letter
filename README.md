# Cover Letter Generator with Artic

This Streamlit app helps users generate a cover letter tailored to a specific job offer using their CV. The app leverages the Replicate API for generating the cover letter and key points linking the job offer requirements to the CV.

## Features

- **Upload CV**: Upload your CV in PDF format.
- **Paste Job Offer**: Paste the job offer details.
- **Key Points Generation**: Identify and list key points linking the CV to the job offer requirements.
- **Generate Cover Letter**: Automatically generate a cover letter tailored to the job offer.

## Requirements

- Python 3.7 or higher
- Streamlit
- PyPDF2
- Transformers
- Replicate API token

## Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yourusername/cover-letter-generator.git
    cd cover-letter-generator
    ```

2. **Install Dependencies**

    Use pip to install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up Replicate API Token**

    Ensure you have a Replicate API token. You can sign up for one at [Replicate](https://replicate.com). Save the token in the `.streamlit/secrets.toml` file as follows:

    ```toml
    [secrets]
    REPLICATE_API_TOKEN = "your_replicate_api_token"
    ```

## Usage

1. **Run the Streamlit App**

    ```sh
    streamlit run app.py
    ```

2. **Upload Your CV**

    - Click on the "Upload your CV" button on the sidebar.
    - Upload your CV in PDF format.

3. **Paste the Job Offer**

    - Copy and paste the job offer details in the provided text area.

4. **Generate Cover Letter**

    - Click the "Confirm" button to generate the cover letter and key points.

## File Structure

- `app.py`: Main application file containing the Streamlit app code.
- `requirements.txt`: List of Python dependencies.
- `.streamlit/secrets.toml`: Configuration file to store secrets like the Replicate API token.

## Code Overview

### Main Functions

- `initialization()`: Initializes the Streamlit page configuration and header.
- `sidebar()`: Sets up the sidebar for parameter input and Replicate API token validation.
- `input_form()`: Creates the input form for uploading CV and pasting the job offer.
- `get_tokenizer()`: Caches and returns a tokenizer for text processing.
- `get_num_tokens(prompt)`: Returns the number of tokens in a given prompt.
- `generate_cover_letter()`: Generates the cover letter based on CV and job offer.
- `generate_links()`: Generates key points linking CV to job offer requirements.
- `stream_data_in_column(function, container, ctx)`: Populates columns simultaneously with streamed data.
- `main()`: Main function to set up the layout and start streaming data.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or feedback, please contact [yourname@example.com](mailto:yourname@example.com).

---

Enjoy using the Cover Letter Generator with Artic!