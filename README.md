# Local Basket

A mobile-friendly Progressive Web App connecting local homesteaders and farmers with their communities. Local Basket enables sellers to showcase their fresh produce, eggs, firewood, and other goods while helping buyers discover local sources near them.

## Features

### For Sellers
- Create and manage your virtual shop front
- Upload banner images and product photos
- Set your location and operating hours
- List products with custom pricing and descriptions
- Toggle availability and shop status (open/closed)
- Accept multiple payment methods (cash, Venmo, PayPal, Zelle)
- Receive and respond to customer reviews

### For Buyers
- Interactive map showing nearby sellers
- Search and filter by product type, distance, and ratings
- View seller profiles with contact information and hours
- Access integrated payment options
- Leave reviews and ratings
- Location-based discovery

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM
- **Frontend**: Progressive Web App with responsive design
- **Authentication**: Flask-Login with email confirmation
- **Maps**: Location services integration
- **Design**: Earthy, organic color palette with artisan typography

## Getting Started

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   python app.py
   ```

The app will be available at `http://localhost:5000`

## Contributing

This project aims to support local food systems and sustainable agriculture. Contributions are welcome to improve the platform for both sellers and buyers.

## License

This project is designed to be free with minimal advertising to keep the platform accessible to local farmers and homesteaders.