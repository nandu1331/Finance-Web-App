

---

# Money-Mate [Financial Advisor and Management System]

A comprehensive Django-based web application for managing and analyzing personal finances and predicting future stock prices. This application enables users to upload expense CSV files, view detailed expense breakdowns, gain financial insights through dynamic charts and graphs, and predict stock prices using a machine learning model.

![Finance-Web-App](path_to_main_image)

## Features

- **Expense Tracking**: Upload CSV files to keep track of all your expenses.
- **Dynamic Charts**: View monthly and category-wise spending with interactive charts.
- **Financial Tips**: Get personalized financial tips based on your spending habits.
- **User Authentication**: Secure user login and profile management.
- **Responsive Design**: Access your financial data seamlessly on any device.
- **Stock Prediction**: Predict future 30 days of stock closing prices using a machine learning model.

## Screenshots

### Dashboard
![Dash Board](https://github.com/user-attachments/assets/7f18b8fd-9c4c-4d44-8efb-325d2b5852e3)

### Expense Upload
![Statement Upload](https://github.com/user-attachments/assets/6512df1e-d6c0-46aa-8db2-9b681bf636cd)

### Charts and Graphs
![Expense Summary with Charts and Graphs](https://github.com/user-attachments/assets/02cd425a-f1ee-4bdb-a365-4bf34951c73c)

### Stock Prediction
![Stock Prediction](path_to_stock_prediction_image)

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/nandu1331/Finance-Web-App.git
   cd Finance-Web-App
   ```

2. **Create and activate a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the migrations**:
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```sh
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```sh
   python manage.py runserver
   ```

## Usage

### Expense Management

1. **Upload CSV**: Log in and upload your expense CSV file through the dashboard.
 
   <img src="https://github.com/user-attachments/assets/6512df1e-d6c0-46aa-8db2-9b681bf636cd" alt="Upload CSV" style="width: 45%; height: auto; margin: auto;">

3. **View Expenses**: Navigate to the expenses page to view your transactions.
   <div style="display: flex; justify-content: space-around; margin: auto;">
        <img src="https://github.com/user-attachments/assets/7f18b8fd-9c4c-4d44-8efb-325d2b5852e3" alt="Image 1" style="width: 45%; height: auto; padding-right: 20px;">
        <img src="https://github.com/user-attachments/assets/0d7ce8bd-2185-41ba-a897-11787007daf4" alt="Image 2" style="width: 45%; height: auto;">
   </div>


4. **Analyze Data**: Use the charts to analyze spending patterns and categories.
 
   <img src="https://github.com/user-attachments/assets/02cd425a-f1ee-4bdb-a365-4bf34951c73c" alt="Upload CSV" style="width: 45%; height: auto; margin: auto;">

6. **Get Tips**: Visit the tips section to receive personalized financial advice.


    <img src="https://github.com/user-attachments/assets/6f0f3374-7a46-487f-afce-a19405bc38ab" alt="Upload CSV" style="width: 45%; height: auto; margin: auto;">
   

### Stock Prediction

1. **Access Prediction Page**: Navigate to the stock prediction section from the dashboard.
   ![Access Prediction](path_to_access_prediction_image)

2. **Enter Stock Ticker**: Input the stock ticker symbol for which you want to predict the closing prices.
   ![Enter Stock Ticker](path_to_enter_stock_ticker_image)

3. **View Predictions**: See the predicted stock closing prices for the next 30 days.
   ![View Predictions](path_to_view_predictions_image)

## Machine Learning Model

The stock prediction feature uses a machine learning model to forecast the closing prices of stocks for the next 30 days. The model is trained on historical stock price data and leverages techniques such as time series analysis and regression models.

### Training the Model

To train the model on new data:
1. Prepare the dataset with historical stock prices.
2. Run the training script:
   ```sh
   python train_stock_model.py
   ```

3. The trained model will be saved and used for future predictions.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [nandu1331](https://github.com/nandu1331).

---
