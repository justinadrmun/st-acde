# copilot_instructions.md

## Objective
Build a multi-page Streamlit app for visualizing data across 5 sections, with approximately 20 visualizations in total. This app serves as a demo to showcase data insights for a client. The app must include user access control (password-protected) for private users and simulate data to demonstrate the visualizations. Each page in the app represents a different topic based on client requirements.

## Key Requirements
1. **Streamlit Multi-page Setup**: 
   - Use Streamlit’s sidebar for page navigation.
   - Each page should be in a separate file (e.g., `page_1.py`, `page_2.py`, etc.) and include:
     - A title (header) for the section.
     - A brief description of the section or topic.
     - One or more data visualizations (static) using either matplotlib or seaborn.
   - Create a main app file (`app.py`) to handle:
     - Page navigation using Streamlit's sidebar.
     - Password-protected login functionality.

2. **Simulated Data**:
   - Generate a synthetic dataset to showcase the visualizations.
   - The dataset should support a variety of data types (numerical, categorical, etc.).
   - Each page should include code to simulate and filter data specific to the visualizations needed for that page.

3. **User Access Control**:
   - Implement a simple password-based access control system on the main page (in `app.py`).
   - If the user provides the correct password, they can access the rest of the app pages.
   - Use Streamlit's `st.text_input` with `type="password"` for the password entry.

4. **Data Visualization Requirements**:
   - Use matplotlib and/or seaborn to create static visualizations.
   - The client requires approximately 20 visualizations in total, spread across 5 pages, following the specific topics or sections described below.

## Sections and Topics
1. **Section 1: Overview**
   - Description: General summary of the dataset.
   - Visualizations: Distribution of primary variables, correlations, and basic summaries.

2. **Section 2: Trends and Changes**
   - Description: Exploration of time series or trend-based data.
   - Visualizations: Line plots, bar charts to show changes over time.

3. **Section 3: Comparisons**
   - Description: Comparison between different groups or categories.
   - Visualizations: Grouped bar charts, box plots, and violin plots.

4. **Section 4: Relationships**
   - Description: Investigation of relationships between variables.
   - Visualizations: Scatter plots, pair plots, heatmaps for correlations.

5. **Section 5: Summary and Insights**
   - Description: Summary insights based on the visualizations from previous sections.
   - Visualizations: Summary charts, final correlation plots, or any other summary insights.

## Guidelines for Code Structure
- **app.py**:
  - Create the main file that serves as the entry point for the app.
  - Include login functionality to control user access based on a password.
  - Implement navigation using Streamlit’s sidebar.
- **page files (e.g., `page_1.py`, `page_2.py`, etc.)**:
  - Each file should have a function to render a specific section based on the topics listed above.
  - Use placeholders for simulated data (e.g., `pandas.DataFrame` with random data) where necessary.
  - Import matplotlib and seaborn for visualizations, ensuring the plots are static.
- **Simulated Data Generation**:
  - Include helper functions for generating sample data in each page.
  - Provide variable types that match real-world datasets for each section.

## Additional Notes
- **Code Quality**: Use clear, consistent naming conventions and comments to document each section and function.
- **Extensibility**: Structure the app and data simulation functions to allow for easy modification or scaling in the future.
- **User Experience**: Keep the UI simple and clear, with logical navigation and descriptions for each section.