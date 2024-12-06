# Ice-Breaking Project

This repository contains the source code for the **Ice-Breaking** project, which generates and displays a web page with social media data visualization.

## Project Structure

- `work-ngrok/` - Contains the core scripts needed to run and display the Ice-Breaking web page.
- `work-ngrok/app.py` - The primary script to launch the web page.
- `mk_html.py` - A secondary script for generating a new version of the web page using different Weibo data.

## Getting Started

### Prerequisites
- Python 3.x

### Running the Web Page

1. Navigate to the `work-ngrok` directory.
   
   ```bash
   cd work-ngrok
   ```

2. Run the `app.py` script to generate and launch the web page.

   ```bash
   python app.py
   ```

   This will start a local server, and you can view the web page in your browser.

### Generating a New Web Page

If you'd like to generate a new version of the web page using a different set of Weibo data, you can run the `mk_html.py` script:

```bash
python mk_html.py
```

This will create a fresh HTML file with the new data integrated.

---

Feel free to modify this `README.md` file to suit your needs. If you encounter any issues, please open an issue in the repository.