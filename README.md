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

# Output
  ## Screenshot 1
  
  ![Screenshot 2025-03-01 at 6 55 28 AM](https://github.com/user-attachments/assets/8199a038-617b-440b-873c-78c0d7ed2558)

  ## Screenshot 2
  
  <img width="1465" alt="Screenshot 2025-03-01 at 6 57 29 AM" src="https://github.com/user-attachments/assets/1dc5b37b-4587-40d4-b884-ebf9275ea001" />

  ## Screenshot 3
  
  <img width="1464" alt="Screenshot 2025-03-01 at 6 58 53 AM" src="https://github.com/user-attachments/assets/95af2cdb-4398-41d4-955c-cc3703a96893" />
  
  ## Screenshot 4
  
  <img width="1470" alt="Screenshot 2025-03-01 at 7 00 17 AM" src="https://github.com/user-attachments/assets/796d6c63-3b31-46d3-b7f1-2a14b9654024" />

  ## Screenshot 5
  
  ![Screenshot 2025-03-01 at 7 00 32 AM](https://github.com/user-attachments/assets/51042c8e-543e-45a1-8c0d-5d4d3026ee7f)

  ## Screenshot 6
  
  <img width="1470" alt="Screenshot 2025-03-01 at 7 00 39 AM" src="https://github.com/user-attachments/assets/99d0f424-8ec6-48b8-9658-d77770dc9100" />

  ## Screenshot 7
  
  <img width="1470" alt="Screenshot 2025-03-01 at 7 00 49 AM" src="https://github.com/user-attachments/assets/21b7c094-1c65-4f60-b62c-a645109228f9" />
  
  ## Screenshot 8
  
  <img width="1461" alt="Screenshot 2025-03-01 at 6 58 04 AM" src="https://github.com/user-attachments/assets/f2de5bf7-1ff7-4c5f-8bae-b10adb97655f" />

  ## Screenshot 9
  
  <img width="1463" alt="Screenshot 2025-03-01 at 6 59 29 AM" src="https://github.com/user-attachments/assets/54e4222d-c136-4979-94d2-87ec99753a79" />

  ## Screenshot 10
  
  <img width="1460" alt="Screenshot 2025-03-01 at 7 00 02 AM" src="https://github.com/user-attachments/assets/f8688ce0-4565-4103-abdf-31458bc50c4e" />



