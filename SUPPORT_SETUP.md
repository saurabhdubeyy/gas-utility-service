# Support Staff Setup Guide

This document explains how to set up and use the support staff functionality in the Gas Utility Customer Service application.

## Creating Support Staff Users

There are three ways to create support staff users:

### 1. Using the Admin Interface

1. Login to the admin interface at `/admin/` with a superuser account.
2. Go to "Users" and create a new user.
3. Mark the user as "Staff status" (this is important).
4. Go to "Groups" and create a "Support" group if it doesn't exist.
5. Add the user to the "Support" group.
6. Go to "Support representatives" and create a new entry linked to this user.

### 2. Using the Support Registration Form

1. Login to the admin interface with a superuser account.
2. Navigate to `/support/register/`.
3. Fill out the form with the support staff details.
4. Submit the form to create a new support representative.

### 3. Using the Script

Run the provided script to create a support user automatically:

```bash
python create_support_user.py
```

You can modify the script to create users with different credentials.

## Support Staff Login

Support staff can login through:

1. The main login page at `/login/` - this works for all users
2. The dedicated support login page at `/support/` - specifically for support staff

## Support Dashboard

After logging in, support staff will have access to:

1. **Support Dashboard** (`/support/dashboard/`): Shows an overview of all service requests with statistics.
2. **All Requests** (`/requests/all/`): Lists all service requests with filtering options.
3. **Request Details** (`/requests/{id}/`): Shows details of a specific request and allows:
   - Updating the request status
   - Adding comments (public or internal)
   - Viewing customer information

## Processing Service Requests

Support staff should follow this workflow:

1. Review new requests on the dashboard or all requests page.
2. Change the status from "Submitted" to "In Progress" when working on a request.
3. Add comments to communicate with the customer or add internal notes.
4. Mark the request as "Resolved" once completed, or "Canceled" if appropriate.

## Support User Permissions

Support staff have the following permissions:

- View all service requests in the system
- Update request statuses
- Add comments to requests (visible to customers or internal only)
- View customer information
- Access the support dashboard and tools

They do not have permission to:

- Delete users or service requests
- Modify system settings
- Access certain admin functions

## Troubleshooting

If a support user cannot login:

1. Check that the user is marked as "Staff status" in the admin.
2. Verify the user is assigned to the "Support" group.
3. Confirm that a SupportRepresentative record exists for the user.
4. Reset the password if needed through the admin interface. 