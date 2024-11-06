# ACDE Streamlit Dashboard

A multi-page Streamlit application for visualising data across different analytical sections. This demo showcases various data insights through approximately 20 visualisations spread across 5 sections.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd st-acde
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit .env file and set your desired password:
```bash
APP_PASSWORD=your_password_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to http://localhost:8501

3. Enter the password to access the dashboard

## Dependencies
See requirements.txt

## Security Note
- The password is stored in the .env file
- Never commit the .env file to version control