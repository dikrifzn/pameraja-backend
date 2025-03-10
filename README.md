# Django API Documentation

## Overview
This API is built using Django to manage users, social media accounts, projects, and user interactions such as likes and comments.

---

## **Database Design**
### Users Table
| Field         | Type    | Constraints               |
|---------------|---------|---------------------------|
| id            | int     | Primary Key, Auto Increment |
| nama          | varchar |                           |
| email         | varchar | Unique                    |
| position      | varchar |                           |
| password      | varchar |                           |
| role          | enum    |                           |
| address       | varchar |                           |
| created_at    | varchar |                           |
| edited_at     | varchar |                           |

### Social_Media Table
| Field    | Type | Constraints                         |
|----------|------|-------------------------------------|
| id       | int  | Primary Key, Auto Increment         |
| id_user  | int  | Foreign Key (Users.id)              |
| name     | varchar |                                   |
| url      | varchar |                                   |

### Projects Table
| Field       | Type    | Constraints                    |
|-------------|---------|--------------------------------|
| id          | int     | Primary Key, Auto Increment    |
| id_user     | int     | Foreign Key (Users.id)         |
| title       | varchar |                                |
| description | text    |                                |
| category    | enum    |                                |
| file_url    | varchar |                                |
| image_url   | varchar |                                |
| views       | int     |                                |
| created_at  | date    |                                |
| edited_at   | date    |                                |

### Likes Table
| Field       | Type | Constraints                      |
|-------------|------|----------------------------------|
| id          | int  | Primary Key, Auto Increment      |
| id_user     | int  | Foreign Key (Users.id)           |
| id_project  | int  | Foreign Key (Projects.id)        |

### Comments Table
| Field       | Type | Constraints                      |
|-------------|------|----------------------------------|
| id          | int  | Primary Key, Auto Increment      |
| id_user     | int  | Foreign Key (Users.id)           |
| id_project  | int  | Foreign Key (Projects.id)        |
| content     | text |                                  |
| created_at  | date |                                  |
| edited_at   | date |                                  |

---

## **Endpoints**

### **Authentication**
1. **User Registration**
   - **Method:** POST
   - **Endpoint:** `/api/auth/register`
   - **Description:** Register a new user.

2. **User Login**
   - **Method:** POST
   - **Endpoint:** `/api/auth/login`
   - **Description:** Authenticate user and issue token.

3. **User Logout**
   - **Method:** POST
   - **Endpoint:** `/api/auth/logout`
   - **Description:** Log the user out.

4. **Password Reset**
   - **Method:** POST
   - **Endpoint:** `/api/auth/reset-password`
   - **Description:** Initiate password reset process.

---

### **User Management**
5. **Get User Profile**
   - **Method:** GET
   - **Endpoint:** `/api/users/{id}`
   - **Description:** Fetch user profile by ID.

    ### Response
    if success
   ```json
    {
        "message": "User profile retrieved successfully",
        "data": {
            "id": 1,
            "name": "User Example",
            "email": "user@gmail.com",
            "position": "CEO Google",
            "address": "Jl. Veteran No. 140",
            "created_at": "2025-01-26T13:42:32.869581Z",
            "edited_at": "2025-01-26T13:42:32.869617Z"
        }
    }
    ```

    if not found
    ```json
    {
        "message": "User not found"
    }
    ```

6. **Update User Profile**
   - **Method:** PUT/PATCH
   - **Endpoint:** `/api/users/{id}`
   - **Description:** Update user profile information.

    ### Request
    ```json
    {
        {
            "name": "User Example",
            "email": "user@gmail.com",
            "position": "CEO Google",
            "address": "Jl. Veteran No. 140",
            "password": "user123" //opsional
        }
    }
    ```
    ### Response
    if success
   ```json
    {
        "message": "User profile updated successfully",
        "data": {
            "id": 1,
            "name": "User Example",
            "email": "user@gmail.com",
            "position": "CEO Google",
            "address": "Jl. Veteran No. 140",
            "created_at": "2025-01-26T13:42:32.869581Z",
            "edited_at": "2025-01-26T13:42:32.869617Z"
        }
    }
    ```

    if error
    ```json
    {
        "message": "Failed to update user profile",
        "errors": {
            "error point": [
                "Description problem"
            ]
        }
    }
    ```

   if user not found
      ```json
    {
        "message": "User not found"
    }
   ```


7. **Delete User**
   - **Method:** DELETE
   - **Endpoint:** `/api/users/{id}`
   - **Description:** Delete a user account.

    ### Response
   if success

   ```json
    {
        "message": "User deleted successfully"
    }
   ```

   if user not found
      ```json
    {
        "message": "User not found"
    }
   ```

---

### **Social Media Management**
8. **Add Social Media**
   - **Method:** POST
   - **Endpoint:** `/api/social-media/{id_user}`
   - **Description:** Add a social media account for the user.

    ### Request
    ```json
    {
        "id_user": "1",
        "name": "Instagram",
        "url": "https://instagram.com/dikrifzn"
    }
    ```
    ### Response
    if user not found
      ```json
    {
        "message": "User not found"
    }
    ```
    if success
    ```json
    {
        "message": "Social media account added successfully",
        "data": {
            "id": 1,
            "name": "Instagram",
            "url": "https://instagram.com/example",
            "created_at": "2025-01-31T15:17:02.507805Z",
            "edited_at": "2025-01-31T15:17:02.507847Z",
            "id_user": 1
        }
    }
    ```

9. **Get Social Media**
   - **Method:** GET
   - **Endpoint:** `/api/social-media/{id_user}`
   - **Description:** Fetch social media accounts by user ID.

    ### Response
    if user not found
    ```json
    {
        "message": "User not found"
    }
    ```

    if success
    ```json
    {
        "message": "Social Media User retrieved successfully",
        "data": {
            "id": 1,
            "name": "instagram",
            "url": "https://www.instagram.com/example",
            "created_at": "2025-01-27T09:59:50.957601Z",
            "edited_at": "2025-01-27T09:59:50.957640Z",
            "id_user": 1
        }
    }

10. **Update Social Media**
    - **Method:** PUT
    - **Endpoint:** `/api/social-media/{id}`
    - **Description:** Update social media account information.

    ### Request
    ```json
    {
        "id_user": "1",
        "name": "Instagram",
        "url": "https://instagram.com/example"
    }
    ```

    ### Response
    if user not found
    ```json
    {
        "message": "User not found"
    }
    ```

    if success
    ```json
    {
        "message": "Social Media User updated successfully",
        "data": {
            "id": 3,
            "name": "Instagram",
            "url": "https://instagram.com/example",
            "created_at": "2025-01-31T15:17:02.507805Z",
            "edited_at": "2025-02-02T15:27:21.042478Z",
            "id_user": 1
        }
    }
    ```

    if error
    ```json
    {
        "message": "Failed to update user Social Media User",
        "errors": {
            "error point": [
                "Description problem"
            ]
        }
    }
    ```

11. **Delete Social Media**
    - **Method:** DELETE
    - **Endpoint:** `/api/social-media/{id}`
    - **Description:** Delete a specific social media account.
    
    ### Request
    ```json
    {
        "social_media_id": "1"
    }
    ```
    ### Response
    if user not found
    ```json
    {
        "message": "User not found"
    }
    ```
     
    if success
    ```json
    {
        "message": "Social Media berhasil dihapus"
    }
    ```
---

### **Project Management**
12. **Get All Projects**
    - **Method:** GET
    - **Endpoint:** `/api/project/`
    - **Description:** Fetch all projects.

    ### Response
    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "title": "Sistem Absensi",
                "description": "Pembuatan sistem absensi",
                "category": "pendidikan, Manajemen",
                "file_url": "test",
                "image_url": "test",
                "views": 1,
                "created_at": "2025-01-27T09:52:35.810295Z",
                "edited_at": "2025-01-27T09:52:35.810337Z",
                "id_user": 1
            }
        ]
    }
    ```

13. **Create Project**
    - **Method:** POST
    - **Endpoint:** `/api/projects`
    - **Description:** Add a new project.

14. **Get Project Details**
    - **Method:** GET
    - **Endpoint:** `/api/projects/{id}`
    - **Description:** Fetch project details by ID.

15. **Update Project**
    - **Method:** PUT
    - **Endpoint:** `/api/projects/{id}`
    - **Description:** Update project information.

16. **Delete Project**
    - **Method:** DELETE
    - **Endpoint:** `/api/projects/{id}`
    - **Description:** Delete a specific project.

17. **Search Projects**
    - **Method:** GET
    - **Endpoint:** `/api/projects/search`
    - **Description:** Search projects by keywords, category, etc.

---

### **Interaction (Likes and Comments)**
18. **Like Project**
    - **Method:** POST
    - **Endpoint:** `/api/projects/{id}/like`
    - **Description:** Like a specific project.

19. **Unlike Project**
    - **Method:** DELETE
    - **Endpoint:** `/api/projects/{id}/unlike`
    - **Description:** Unlike a specific project.

20. **Get Project Likes**
    - **Method:** GET
    - **Endpoint:** `/api/projects/{id}/likes`
    - **Description:** Fetch likes for a project.

21. **Add Comment**
    - **Method:** POST
    - **Endpoint:** `/api/projects/{id}/comments`
    - **Description:** Add a comment to a project.

22. **Get Project Comments**
    - **Method:** GET
    - **Endpoint:** `/api/projects/{id}/comments`
    - **Description:** Fetch comments for a project.

23. **Update Comment**
    - **Method:** PUT/PATCH
    - **Endpoint:** `/api/comments/{id}`
    - **Description:** Update a specific comment.

24. **Delete Comment**
    - **Method:** DELETE
    - **Endpoint:** `/api/comments/{id}`
    - **Description:** Delete a specific comment.

---

### **Statistics**
25. **Get Project Statistics**
    - **Method:** GET
    - **Endpoint:** `/api/projects/{id}/stats`
    - **Description:** Fetch project statistics such as views, likes, and comments.

---

### **Setup Instructions**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate into the project directory:
   ```bash
   cd <project-directory>
   ```

3. Install Pipenv (if not installed):
   ```bash
   pip install pipenv
   ```

4. Install dependencies:
   ```bash
   pipenv install
   ```

5. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

6. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Start the server:
   ```bash
   python manage.py runserver
   ```

8. Access the API documentation at `/api/docs` (if using tools like Django REST Framework Swagger or DRF-YASG).

---

## **Technologies Used**
- Django
- Django REST Framework
- PostgreSQL/MySQL (configurable)
- JWT for authentication
- Pipenv for environment management

For additional questions, contact the developer team.