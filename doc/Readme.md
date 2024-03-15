# ZMP Console Shell Service

## Requirements

### Functional Requirements

- Login & Auth Management
  - Backend \
    . Check Login Session. Redirect when non-privileged session \
    . After login, redirect previous url reqeusted \
    . Login based on Keycloak \
    . Fetch Role and RBAC
  - Fronend \
    . Login view \
    . ID/Password finder view \
    . Register view
- User Profile Service \
  - Backend \
    . Fetch User's information \
    . Fetch notifications \
    . CRUD for user's information
  - Frontend \
    . Profile View \
    . Change basic information view \
    . Show instant notification and show badge \
    . View of notification list
- GNB Service
  - Backend \
    . Load product menu information \
    . Serve aligned with Role
  - Frontend \ 
    . Show breadcumbs \
    . Show menus
- LNB Service
  - Backend \
    . Load features menu information \
    . Serve aligned with Role
  - Frontend \ 
    . Show menus 
- Alarm Service