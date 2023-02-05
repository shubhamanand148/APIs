Reference: https://www.youtube.com/watch?v=0sOvCWFmrtA&t=16260s
TimeStamp: 7 hr: 35 min


This Project is an extension of CRUD Project.


To run this project:
1. Open the folder which contains main.py file in CMD.
2. Run in CMD: uvicorn main:app --reload
3. Open postman and check the response with appropriate operation (GET/POST/PUT/DELETE).

	a. <ip>:<port-number>/posts for the posts.
		1. For POST (Creating Post) enter the value for below keys as Json in the body of Postman:
			i. title: Required
			ii. content: Required
			iii. rating: Optional
			iv. published: Optional

		    And the data in Header:- Key: Authorization
						 Value: Bearer <JWT Token>

		    To get the JWT Token: Run the <ip>:<port-number>/login URL with below data in Body -> Form-data.
			Key: username	Value: <email ID>
			Key: password	Value: <password>

		2. For DELETE (Deleting Post) or Getting Post by ID enter the "Post ID" in URL.

		3. For PUT (Updating a Post) enter the "Post ID" in URL and enter the value for below keys as Json in the body of Postman:
			i. title: Required
			ii. content: Required
			iii. rating: Optional
			iv. published: Optional

		   And the data in Header:- 	Key: Authorization
						 	Value: Bearer <JWT Token>

		   To get the JWT Token: Call the <ip>:<port-number>/login API with below data in Body -> Form-data.

				Key: username	Value: <email ID for already created user>
				Key: password	Value: <password>



	b. <ip>:<port-number>/login for user login and getting JWT Token.
		For logging in and getting JWT Token enter below data in Body -> Form-data.
			Key: username	Value: <email ID for already created user>
			Key: password	Value: <password>

	c. <ip>:<port-number>/users for creating for getting users by User ID (primary key).



Project Files:
1. main.py: The main file of the project. It calls the posts, users, login function when mentioned.
2. utils: This file is used for password hasing (while creating account)
	    and password verification while logging in.

3. models: It defines the table name and data types of the fields with which the table is created.
	     In this project it will create 2 tables.
		a. Posts table
		b. Users table

4. Schemas: It have the classes which define the data and datatypes of the data which will be accepted
		while sending data (body) with the API.
5. Database: It connects us to the postgres database

6. Oauth2: This file has 2 functions/uses:
		a. Create JWT access token for user login.
		b. Get the currently logged in user by using the verify_access_token function.

7. Routers: The main file redirects the Browser to this folder for posts, users, login (auth.py).
			a. auth.py: This file is used for user login 