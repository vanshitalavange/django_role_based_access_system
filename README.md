# RBAC 
- RBAC stands for Role based access control

### Project details
- The system has three types of roles assigned to the user - (admin, user, viewer)
- based on role of the user they can perform certain actions

### Admin actions
- Can add users.
- Add API’s
- Remove Users.
- Update Users.
- Remove API
- Update API
- View API

### User actions
- Add API’s
- Update API’s.
- Map API’s to users.
- View API’s.

### Viewer actions
- View API's

### Fulfills below conditions
1. Add user: Add user and map the role for the user and the API’s the user can access.
2. Remove user: Remove user and the mapping of the role and API’s the user can access.
3. Update user: Update the role and the mapping of the API’s the user can access.
4. Add API: Create new API. A database entry in the Django app and the access to it.
5. Remove API: Remove the API and if there are any users mapped to the API an error
should be thrown.
6. Update API: Update the API in the database.
7. View API: List the API’s mapped against the user.
8. For all the above 7 there has to be different API’s created in the Django Application and the web
interface should be displaying and taking the input for it.
9. If the user is not authorized for the role to access the API then 401 UnAuthorized Exception
should be returned.
  
