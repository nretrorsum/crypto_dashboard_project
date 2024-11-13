# Creating a markdown file with detailed API documentation based on the user's provided code
Code review
This code showcases a well-structured FastAPI application that includes essential features for a user-centered cryptocurrency portfolio and news service, with particular attention to secure authentication, caching, and efficient data access.

Key Features
Authentication & Authorization: The code uses JWT-based authentication through OAuth2PasswordBearer to secure API endpoints, ensuring that only authenticated users can access specific resources. This mechanism is complemented by a permission dependency to provide granular control over user actions based on their role.

Caching Mechanism: The cache_user and get_cached_user functions enable efficient data retrieval by storing frequently accessed user data. This reduces database load and improves response times, which is especially useful in high-traffic scenarios. Additionally, cache_currencies is implemented to cache cryptocurrency data, allowing for fast responses in frequently requested data such as coin lists.

Portfolio Management: The code includes several endpoints for portfolio CRUD operations, including adding, updating, and deleting portfolio items. This allows users to manage their investment portfolios and retrieve profit data through get_profit endpoints. This endpoint also demonstrates an investment performance calculation method, which could be enhanced with more complex financial metrics.

Third-Party Data Integration: The application integrates external data sources for cryptocurrency and news information. By utilizing coin_data_request and news_api_processing, the code gathers real-time financial and news data relevant to users’ interests. The system further provides a cached_currency_list endpoint, displaying cached data for performance optimization.

Error Handling and Validation: The code implements robust error handling through HTTPException, ensuring that unauthorized access and invalid operations are met with clear status codes and error messages, improving the API’s usability and security.

Dependency Injection and Annotated Typing: The code effectively uses FastAPI’s Depends and Annotated for dependency injection, providing clear separation of concerns and making it easier to test individual components.
# API Documentation

## Authentication Endpoints

### Register User

- **URL**: `/register`
- **Method**: `POST`
- **Description**: Registers a new user.
- **Request Body**:
  - **id**: `int`, required
  - **name**: `str`, required
  - **email**: `str`, required
  - **hashed_password**: `str`, required
  - **subscription**: `str`, optional
  - **is_active**: `bool`, optional
  - **is_verified**: `bool`, optional

- **Response**:
  - **Status Code**: `201 Created`
  - **Body**: `{"message": "User created"}`

---

### Obtain Access Token

- **URL**: `/token`
- **Method**: `POST`
- **Description**: Generates an access token for authenticated users.
- **Request Body**:
  - **username**: `str`, required
  - **password**: `str`, required

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: `{"access_token": "<token>", "token_type": "Bearer", "user_id": <user_id>}`

---

## User Endpoints

### Get User by ID

- **URL**: `/user/{id}`
- **Method**: `GET`
- **Description**: Retrieves user details by ID. Requires authentication and checks permissions.
- **Path Parameter**:
  - **id**: `int`, user ID to retrieve

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: `ReadUser` (user details)

---

### Get User Portfolio

- **URL**: `/portfolio/{id}`
- **Method**: `GET`
- **Description**: Retrieves user's portfolio by user ID.
- **Path Parameter**:
  - **id**: `int`, user ID for portfolio retrieval

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: `List[ReadPortfolio]` (portfolio details)

---

### Add User Portfolio

- **URL**: `/user/{id}/portfolio`
- **Method**: `POST`
- **Description**: Adds a new portfolio entry for a user.
- **Path Parameter**:
  - **id**: `int`, user ID

- **Response**:
  - **Status Code**: `201 Created`
  - **Body**: `AddPortfolio`

---

### Update User Portfolio

- **URL**: `/user/{id}/portfolio/{portfolio_id}`
- **Method**: `PATCH`
- **Description**: Updates an existing user portfolio entry.
- **Path Parameters**:
  - **id**: `int`, user ID
  - **portfolio_id**: `int`, portfolio ID

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Updated portfolio entry details

---

### Delete User Portfolio

- **URL**: `/user/{id}/portfolio/{portfolio_id}`
- **Method**: `DELETE`
- **Description**: Deletes a portfolio entry for a user.
- **Path Parameters**:
  - **id**: `int`, user ID
  - **portfolio_id**: `int`, portfolio ID

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Deletion confirmation

---

### Get Portfolio Profit

- **URL**: `/get_profit/{user_id}/{portfolio_id}`
- **Method**: `GET`
- **Description**: Calculates the profit for a specific portfolio.
- **Path Parameters**:
  - **user_id**: `int`, user ID
  - **portfolio_id**: `int`, portfolio ID

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: `{"status": "success", "data": <profit_data>}`

---

## Currency and News Endpoints

### Get Coin Data

- **URL**: `/coin/{id}`
- **Method**: `GET`
- **Description**: Retrieves data about a specific cryptocurrency by ID.
- **Path Parameter**:
  - **id**: `int`, cryptocurrency ID

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Cryptocurrency data

---

### Get News for Currency

- **URL**: `/news/{currency_name}`
- **Method**: `GET`
- **Description**: Fetches the latest news for a given currency.
- **Path Parameter**:
  - **currency_name**: `str`, currency name

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Latest news articles

---

### Get Cached Currency List

- **URL**: `/cached_currency_list`
- **Method**: `GET`
- **Description**: Retrieves a list of cached cryptocurrency data.

- **Response**:
  - **Status Code**: `200 OK`
  - **Body**: Cached cryptocurrency data
