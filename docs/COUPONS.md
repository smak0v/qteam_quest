# COUPONS API Endpoints

- ```/api/coupons/``` (GET)

    Returns info about all coupons.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    Only for staff users.

- ```/api/coupons/``` (POST)

    ```
    code (required)
    start_date (required, format YYYY-MM-DD)
    end_date (required, format YYYY-MM-DD)
    discount (required)
    units (required, PERCENT or RUB)
    type (required, INDIVIDUAL or GENERAL)
    user (required, can be null)
    ```
  
    Create new coupon.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    Only for staff users.

    ### Validators:
    
    - ```code``` - max_length = 10;

    - ```start_date```  and ```end_date``` - must be in format YYYY-MM-DD;

    - ```end_date``` - can`t be less that ```start_date```;

    - ```user``` - must be NULL for GENERAL type of coupon;
    
    - ```user``` - can`t be NULL for INDIVIDUAL type of coupon;
    
    - ```user``` - must be real user for INDIVIDUAL type of coupon.
    
- ```/api/coupons/coupon_pk/``` (GET)

    Returns info about a coupon by it primary key.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    Only for staff users.

- ```/api/coupons/coupon_pk/``` (DELETE)

    Delete a coupon by it primary key.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    Only for staff users.

- ```/api/coupons/coupon_pk/``` (PUT, PATCH)

    ```
    code
    start_date (format YYYY-MM-DD)
    end_date (format YYYY-MM-DD)
    discount
    units (PERCENT or RUB)
    type (INDIVIDUAL or GENERAL)
    user (can be null)
    ```

    Update a coupon by it primary key.
    
    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    Only for staff users.

    ### Validators

    - ```code``` - max_length = 10;

    - ```start_date```  and ```end_date``` - must be in format YYYY-MM-DD;

    - ```end_date``` - can`t be less that ```start_date```;

    - ```user``` - must be NULL for GENERAL type of coupon;

    - ```user``` - can`t be NULL for INDIVIDUAL type of coupon;

    - ```user``` - must be real user for INDIVIDUAL type of coupon.
