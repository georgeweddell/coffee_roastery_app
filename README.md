# ☕ Coffee Roastery Management App

A web application for managing customers, products, orders, and inventory in a coffee roastery. Built with **FastAPI**, **SQLAlchemy**, and **Jinja2**, with a **SQLite database** backend. Includes Excel integration to quickly populate and refresh data.

---

## 🚀 Features

- **Customers Management**: Add, view, and manage customer information.  
- **Products Management**: Add, view, and manage coffee products with descriptions and prices.  
- **Orders Management**: Create new orders, linking customers and products.  
- **Inventory Tracking**: Manage stock levels for products.  
- **Dashboard**: Home page displays key metrics:  
  - Top customers by purchase  
  - Best-selling products  
  - Stock summary  
- **Data Import**: Populate database from Excel file (`fake_coffee_data.xlsx`) with a single click.  

---

## 🛠 Tech Stack

- **Backend**: FastAPI  
- **Database**: SQLAlchemy ORM with SQLite  
- **Frontend**: Jinja2 templates, Chart.js for visualizations  
- **Data**: Excel integration via Pandas  
- **Environment**: Python 3.13  

---

## ⚡ Installation

1. **Clone the repository**:  
```bash
git clone https://github.com/yourusername/coffee_roastery_app.git
cd coffee_roastery_app
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
uvicorn app.main:app --reload
Open in your browser:

cpp
Copy code
http://127.0.0.1:8000
📝 Usage
Navigate using the top menu to switch between Customers, Products, Orders, and Inventory.

Add new data using the forms in each section.

Refresh the database from the Excel file using the Refresh button.

Dashboard shows key metrics and visual summaries.

📂 Project Structure
bash
Copy code
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
🤝 Contributing
Feel free to fork, submit issues, or create pull requests. Suggestions for improving the dashboard, adding authentication, or connecting to a real database are welcome!

📄 License
MIT License
