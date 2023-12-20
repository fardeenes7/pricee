
# Description

Pricee is a web scraping project that allows users to compare prices of products across multiple websites. It is built with Django Rest Framework and uses web scraping techniques to collect data from various e-commerce websites.

# Tech Stack

![Tech Stack](https://fardiin.com/images/projects/pricee/stack.png)

# Installation

1.  Clone the repository to your local machine:

    ```bash
    git clone https://github.com/fardeenes7/pricee.git
    ```

2.  Create a virtual environment and activate it:

    
    ```bash
    python -m venv env
    source env/bin/activate (Linux/Mac)
    env\Scripts\activate (Windows)
    ```

3.  Install the required packages:


    ```bash
    pip install -r requirements.txt
    ```

4.  Run the migrations:

    ```bash
    python manage.py migrate
    ```

5.  Start the development server:

    ```bash
    python manage.py runserver
    ```

6.  Use a REST client like [Postman](https://www.postman.com/downloads/) to interact with the Pricee API.

# Endpoints

The following API endpoints are available in Pricee:

## Client API

## `/api/v2/refreshAllRecords/`

-   `GET`: Refresh all records in the database.

### `/api/v2/all/`

-   `GET`: Get a list of all records in the database.

### `/api/v2/products/`

-   `GET`: Get a list of all products.

### `/api/v2/products/all/`

-   `GET`: Get a paginated list of all products.

### `/api/v2/products/all/<int:page>/`

-   `GET`: Get a specific page of paginated list of all products.

### `/api/v2/products/category/<str:category>/<int:page>/`

-   `GET`: Get a specific page of paginated list of all products in a given category.

### `/api/v2/products/subcategory/<str:subcategory>/<int:page>/`

-   `GET`: Get a specific page of paginated list of all products in a given subcategory.

### `/api/v2/products/<str:product_slug>/`

-   `GET`: Get the details of a specific product with the given `product_slug`.

### `/api/v2/products/record_view/<int:id>/`

-   `POST`: Record a view of a specific product with the given `id`.

### `/api/v2/categories/`

-   `GET`: Get a list of all categories.

### `/api/v2/subcategories/`

-   `GET`: Get a list of all subcategories.

### `/api/v2/navigation/`

-   `GET`: Get a list of all categories and their subcategories for navigation.

### `/api/v2/landing/`

-   `GET`: Get a landing page with featured products.

### `/api/v2/user/`

-   Includes endpoints from the `user.urls` module.

## Management API

### `/api/manage/bannerads/`

-   `GET`: Get a list of all banner ads.
-   `POST`: Create a new banner ad.

### `/api/manage/permission/`

-   `GET`: Check if the user has admin permissions.

### `/api/manage/products/`

-   `GET`: Get a list of all products.

### `/api/manage/users/`

-   `GET`: Get a list of all users.
-   `POST`: Create a new user.

### `/api/manage/users/new/`

-   `GET`: Get a form to create a new user.

### `/api/manage/users/<int:pk>/`

-   `GET`: Get the details of a specific user with the given primary key `pk`.

### `/api/manage/users/<int:pk>/update/`

-   `GET`: Get a form to update the details of a specific user with the given primary key `pk`.
-   `POST`: Update the details of a specific user with the given primary key `pk`.

### `/api/manage/users/<int:pk>/delete/`

-   `GET`: Get a form to delete a specific user with the given primary key `pk`.
-   `POST`: Delete a specific user with the given primary key `pk`.

## Contributing

If you would like to contribute to Pricee, please open a pull request or submit an issue on the GitHub repository.

## License

[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
