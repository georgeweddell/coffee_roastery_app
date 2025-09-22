Coffee Roastery Management App ☕️

A web application for managing customers, products, orders, and inventory in a coffee roastery. Built with FastAPI, SQLAlchemy, and Jinja2, with a SQLite database backend. Includes an Excel integration to quickly populate and refresh data.

Features

Customers Management: Add, view, and manage customer information.

Products Management: Add, view, and manage coffee products with descriptions and prices.

Orders Management: Create new orders, linking customers and products.

Inventory Tracking: Manage stock levels for products.

Dashboard: Home page displays key metrics:

Top customers by purchase

Best-selling products

Stock summary

Data Import: Populate database from Excel file (fake_coffee_data.xlsx) with a single click.

Tech Stack

Backend: FastAPI

Database: SQLAlchemy ORM with SQLite

Frontend: Jinja2 templates, Chart.js for visualizations

Data: Excel integration via Pandas

Environment: Python 3.13

Installation

Clone the repository:

git clone https://github.com/yourusername/coffee_roastery_app.git
cd coffee_roastery_app


Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the app:

uvicorn app.main:app --reload


Open in your browser:

http://127.0.0.1:8000

Usage

Use the navigation bar to switch between Customers, Products, Orders, and Inventory pages.

Add new data using forms in each section.

Refresh the database from the Excel file using the Refresh button in the nav bar.

View dashboard metrics on the home page.

Project Structure
coffee_roastery_app/
│
├── app/
│   ├── main.py          # FastAPI app
│   ├── models.py        # Database models
│   ├── database.py      # SQLAlchemy setup
│   └── templates/       # Jinja2 HTML templates
│
├── fake_coffee_data.xlsx # Sample data for testing
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

Contributing

Feel free to fork, submit issues, or create pull requests. Suggestions for improving the dashboard, adding authentication, or connecting to a real database are welcome!

License

MIT License
