# DocScan
  DocScan is a comprehensive platform designed to allow users to upload, scan, and manage documents digitally. It includes advanced features such as text extraction, document matching, and a credit-based usage system to regulate user activity. The system is self-contained, meaning it handles everything from user authentication to document storage, processing, and analytics.

The built-in credit system ensures fair usage by limiting the number of scans or uploads a user can perform within a specific time frame (e.g., daily or monthly). Users can request additional credits, which are managed by an admin.
## Features
  1. Uses cosine similarity and embeddings (e.g., Sentence Transformers) to compare documents and find matches.
  2. Allows users to set a similarity threshold (e.g., 70%) to filter results.
  3. Displays a list of similar documents with their similarity scores.
  4. Users receive a fixed number of credits daily (e.g., 20 credits).
  5. Users can request additional credits, which are approved or denied by an admin.
  6. Admins can manage users, approve credit requests, and view analytics.
  7. Authentication: Users can register, log in, and manage their profiles.
  8. Admins can approve or deny credit requests.
  9. Admins can view usage statistics, such as:


# Setup Instructions
  Follow these steps to set up and run the DocScan project on your local machine.

## Prerequisites
    1. Python 3.7 or higher
   
    2. pip (Python package manager)

## Installation
  1. Clone the repository:
     
  ```bash
  git clone https://github.com/Harigovind3002/DocScan.git
  cd DocScan
  ```

 
  2. Create a virtual environment :
     
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```


  3. Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

  
  4. Run the application:

  ```bash
  python3 app.py
  ```

  5.Access the application:
  
    Open your web browser and navigate to http://127.0.0.1:5000 (or the specified port).

