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
    - **Endpoint:** `/api/project/{id_user}`
    - **Description:** Add a new project.

    ### Request
    ```json
    {
        "title": "AI Waste Management",
        "description": "A project to automate waste sorting using AI",
        "category": "Environment",
        "file_url": "https://example.com/docs/ai_waste.pdf",
        "image_url": "https://example.com/images/waste_project.jpg"
    }
    ```

    ### Response
    ```json
    {
        "message": "Project added successfully",
        "data": {
            "id": 5,
            "title": "AI Waste Management",
            "description": "A project to automate waste sorting using AI",
            "category": "Environment",
            "file_url": "https://example.com/docs/ai_waste.pdf",
            "image_url": "https://example.com/images/waste_project.jpg",
            "views": 0,
            "created_at": "2025-03-17T16:43:34.587595Z",
            "edited_at": "2025-03-17T16:43:34.587633Z",
            "id_user": 1
        }
    }
    ```

14. **Get Project Details**
    - **Method:** GET
    - **Endpoint:** `/api/project/{id}`
    - **Description:** Fetch project details by ID.

    ### Response
    ```json
    {
        "id": 5,
        "title": "AI Waste Management",
        "description": "A project to automate waste sorting using AI",
        "category": "Environment",
        "file_url": "https://example.com/docs/ai_waste.pdf",
        "image_url": "https://example.com/images/waste_project.jpg",
        "views": 0,
        "created_at": "2025-03-17T16:43:34.587595Z",
        "edited_at": "2025-03-17T16:43:34.587633Z",
        "id_user": 1
    }
    ```


15. **Update Project**
    - **Method:** PUT
    - **Endpoint:** `/api/project/5`
    - **Description:** Update project information.

    ### Request
    ```json
    {
        "id_user": "1",
        "title": "Rancang Penyiraman",
        "description": "Pembuatan sistem penyiraman",
        "category": "pendidikan, Manajemen",
        "file_url": "test",
        "image_url": "test"
    }
    ```

    ### Response
    ```json
    {
        "message": "Project User updated successfully",
        "data": {
            "id": 2,
            "title": "Rancang Penyiraman",
            "description": "Pembuatan sistem penyiraman",
            "category": "pendidikan, Manajemen",
            "file_url": "test",
            "image_url": "test",
            "views": 0,
            "created_at": "2025-03-08T07:51:10.012813Z",
            "edited_at": "2025-03-17T17:23:06.403229Z",
            "id_user": 1
        }
    }
    ```


16. **Delete Project**
    - **Method:** DELETE
    - **Endpoint:** `/api/project/{id_user}`
    - **Description:** Delete a specific project.

    ### Request
    ```json
    {
        "project_id": "2"
    }
    ```

    ### Response
    ```json
    {
        "message": "Project berhasil dihapus"
    }
    ```

17. **Search Projects**
    - **Method:** GET
    - **Endpoint:** `/api/project?search={string}`
    - **Description:** Search projects by keywords, category, etc.

    ### Response
    ```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 4,
                "title": "Sistem Penyiraman",
                "description": "Pembuatan sistem penyiraman",
                "category": "pendidikan, Manajemen",
                "file_url": "test",
                "image_url": "test",
                "views": 0,
                "created_at": "2025-03-17T16:33:42.481912Z",
                "edited_at": "2025-03-17T16:33:42.481957Z",
                "id_user": 1
            },
            {
                "id": 3,
                "title": "Sistem Penyiraman",
                "description": "Pembuatan sistem penyiraman",
                "category": "pendidikan, Manajemen",
                "file_url": "test",
                "image_url": "test",
                "views": 0,
                "created_at": "2025-03-08T07:52:39.491773Z",
                "edited_at": "2025-03-08T07:52:39.491805Z",
                "id_user": 1
            }
        ]
    }
    ```


---

### **Interaction (Likes and Comments)**
18. **Like and Unlike Project**
    - **Method:** POST
    - **Endpoint:** `/api/like/{id}`
    - **Description:** Like a specific project.

    ### Response
    if haven't liked yet
    ```json
    {
        "message": "User or Project not found"
    }
    ```
    if have liked
    ```json
    {
        "message": "Like removed successfully"
    }
    ```

19. **Get Project Likes and list user like**
    - **Method:** GET
    - **Endpoint:** `/api/like/{id_project}`
    - **Description:** Fetch likes for a project.

    ### Response
    ```json
    {
    "message": "Likes retrieved successfully",
    "likes_count": 1,
    "liked_by": [
            {
                "id": 1,
                "name": "user",
                "email": "user@gmail.com",
                "position": "CEO Google and Alibaba",
                "address": "Jl. Mangku Bumi No. 140",
                "created_at": "2025-01-26T13:42:32.869581Z",
                "edited_at": "2025-01-30T13:43:37.960472Z"
            }
        ]
    }
    ```

20. **Add Comment**
    - **Method:** POST
    - **Endpoint:** `/api/comment/{id}`
    - **Description:** Add a comment to a project.
    ### Request
    ```json
    {
        "id_user": 1,
        "message": "This is a great project!"
    }
    ```

    ### Response
    ```json
    {
        "message": "Comment added successfully",
        "data": {
            "id": 3,
            "message": "This is a great project!",
            "created_at": "2025-03-17T17:38:36.193744Z",
            "edited_at": "2025-03-17T17:38:36.193774Z",
            "id_user": 1,
            "id_project": 5
        }
    }
    ```
21. **Get Project Comments**
    - **Method:** GET
    - **Endpoint:** `/api/comment/{id}`
    - **Description:** Fetch comments for a project.
    ### Request
    ```json
    {
        "id_user": 1
    }
    ```

    ### Response
    ```json
    {
        "message": "Comments Project retrieved successfully",
        "data": [
            {
                "id": 3,
                "message": "This is a great project!",
                "created_at": "2025-03-17T17:38:36.193744Z",
                "edited_at": "2025-03-17T17:38:36.193774Z",
                "id_user": 1,
                "id_project": 5
            }
        ]
    }
    ```
22. **Update Comment**
    - **Method:** PUT/PATCH
    - **Endpoint:** `/api/comment/{id}`
    - **Description:** Update a specific comment.
    ### Request
    ```json
    {
        "message": "Updated comment text!"
    }
    ```

    ### Response
    ```json
    {
        "message": "Comment updated successfully",
        "data": {
            "id": 3,
            "message": "Updated comment text!",
            "created_at": "2025-03-17T17:38:36.193744Z",
            "edited_at": "2025-03-17T17:41:56.922586Z",
            "id_user": 1,
            "id_project": 5
        }
    }
    ```
23. **Delete Comment**
    - **Method:** DELETE
    - **Endpoint:** `/api/comment/{id}`
    - **Description:** Delete a specific comment.

    ### Response
    ```json
    {
        "message": "Comment deleted successfully"
    }
    ```
---

### **Statistics**
24. **Get Project Statistics**
    - **Method:** GET
    - **Endpoint:** `/api/projects/{id}/stats`
    - **Description:** Fetch project statistics such as views, likes, and comments.

---

### **Setup Instructions**

1. Clone the repository:
   ```bash
   git clone https://github.com/dikrifzn/pameraja-backend.git
   ```

2. Navigate into the project directory:
   ```bash
   cd pameraja-backend
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