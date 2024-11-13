# Creating a markdown file with detailed API documentation based on the user's provided code

markdown_content = """
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