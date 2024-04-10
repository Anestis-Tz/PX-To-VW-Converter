# PX, REM, EM to VW Converter

This web application converts files containing CSS unit values from px, em, and rem to vw units within LESS and CSS files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for you to try.

### Prerequisites

You'll need to have Python installed on your machine. The application was built using Python 3.11. If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).

### Installing

A step-by-step series of commands that tell you how to get a development environment running.

1. **Clone the repository**

   ```bash
   git clone https://github.com/Anestis-Tz/VW-Converter.git
   cd VW-Converter
   ```
2. **Download Python from the Microsoft Store**
   
3. **Install Flask**
   ```bash
   pip install Flask
   ```
4. **Set Up a Virtual Environment (Optional but Recommended)**
   
     Navigate to the project root folder and type
   ```bash
      python -m venv myenv
   ```
5. **Activate the virtual environment**

    ***On Windows:***
    ```bash
    cd myenv\Scripts\activate
    ```
     ***On macOS/Linux:***
     ```bash
    source myenv/bin/activate
    ```

6. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
7. **Running the application**
    ```bash
    python app.py
    ```
You can then access the application at http://localhost:5000 in your web browser.

Using the Application
1. Navigate to http://localhost:5000 in your web browser.
2. Use the interface to upload a .less file.
3. Click the "Convert" button to convert the file. The application will automatically download the converted file to the project root folder and allow you to copy the content of the converted file.

