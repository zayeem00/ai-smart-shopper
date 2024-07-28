# AI Smart Shopper

AI Smart Shopper is an AI-powered product recommendation system that leverages OpenAI's language models and Pinecone's vector database for generating contextual recommendations. The system provides an intuitive interface for uploading product catalogs and querying product recommendations.

## Features

- **Product Catalog Management**: Upload product catalogs via CSV files.
- **Product Recommendations**: Generate recommendations based on user queries.
- **Contextual Messaging**: Generate contextual messages based on user queries and recommended products.
- **User-Friendly Interface**: A sleek, easy-to-use interface built with Gradio.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

   git clone https://github.com/your-username/ai-smart-shopper.git

   cd ai-smart-shopper

3. Create a virtual environment and activate it:

   python -m venv venv

   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

5. Install the required packages:

   pip install -r requirements.txt

6. Running the Application:

   Python app.py


## Usage

- **API Keys**: Enter your OpenAI and Pinecone API keys along with the Pinecone environment.
- **Upload Catalog**: Upload your product catalog in CSV format. The CSV should contain the following columns: product_id, product_name, description, image_url.
- **Get Recommendations**: Enter a query to get product recommendations. The system will display a list of recommended products along with a contextual message.

## Dependencies
OpenAI
Pinecone
Pandas
Gradio

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the apache 2.0 License. See the LICENSE file for details.

## Acknowledgements
Thanks to OpenAI and Pinecone for their amazing APIs.
Thanks to the Gradio team for the easy-to-use UI framework.
