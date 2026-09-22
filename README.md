# Backend Workshop — Final Projects

This repository contains the final projects for the **StarUnion Backend Workshop**.

Each student is required to implement an individual backend project and submit it through their assigned GitHub branch.

---

## Project Requirements

### 1. Backend API

* The project must be implemented as a **RESTful API** using **Django REST Framework (DRF)**.
* No frontend implementation is required.
* Follow proper REST API principles.
* Use appropriate HTTP methods and status codes.

### 2. GitHub

All students will work in this repository.

Each student must create their own branch using the following format:

```text
firstname-lastname
```

Example:

```text
omar-awad
```

Please follow these rules:

* All project development must be done on your own branch.
* **Do NOT push directly to `main`.**
* **Do NOT merge your branch into `main`.**
* Your branch will be used for the final evaluation.

### 3. Database

* The implemented database must follow the **approved Lucidchart database design** submitted previously.
* If you make changes to the database design during development, make sure the implementation and database design remain consistent.

### 4. Authentication & Permissions

* Implement authentication where required by your project.
* Use **JWT Authentication**.
* Implement appropriate permissions and authorization rules.
* Users should only be able to access or modify resources they are authorized to access.

### 5. Validation & Error Handling

* Validate incoming data properly using DRF serializers.
* Return appropriate HTTP status codes.
* Handle common API errors properly, including:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
```

### 6. API Documentation

Your API must be documented using **Apidog**.

The documentation should include:

* All implemented endpoints
* HTTP methods
* Request parameters
* Request body
* Authentication requirements
* Expected responses
* Possible errors

Make sure your Apidog documentation is accessible through the submitted link.

### 7. Git & Commits

Make regular and meaningful commits throughout the development process.

Examples:

```text
feat: add user authentication
feat: implement product endpoints
feat: add order management
fix: validate order creation
docs: update API documentation
```

Avoid unclear commit messages such as:

```text
update
final
test
last
aaa
```

### 8. Environment Variables

* Do **NOT** push sensitive information to GitHub.
* Use a `.env` file for sensitive configuration.
* Add `.env` to `.gitignore`.
* Provide a `.env.example` file when needed.

Never expose:

* Secret keys
* Database credentials
* API keys
* Other sensitive information

### 9. README

Your project must contain its own `README.md`.

The README should include:

* Project overview
* Main features
* Technologies used
* Installation instructions
* Environment variables
* How to run the project
* API documentation link
* Database/ERD information

---

# Final Submission Checklist

Before submitting your project, make sure:

* [ ] The project is implemented using Django REST Framework.
* [ ] All required features are implemented.
* [ ] Authentication is implemented where required.
* [ ] Permissions are implemented correctly.
* [ ] The database matches the approved ERD.
* [ ] Input validation is implemented.
* [ ] Proper error handling is implemented.
* [ ] API documentation is available on Apidog.
* [ ] A project README is included.
* [ ] No secrets or sensitive information are committed.
* [ ] Meaningful Git commits were used.
* [ ] The final version is pushed to your assigned branch.
* [ ] Your branch follows the required naming format.
* [ ] You have tested your API before submission.

---

# Final Submission

After completing your project:

1. Push the final version to your assigned GitHub branch.
2. Make sure your Apidog documentation is updated with the final version of your API.
3. Submit your project through the **Final Project Submission Form**.

### Submission Form

[Submit Your Final Project](https://forms.gle/GTUsquy673e479JbA)

You will be asked to provide:

* Full Name
* GitHub Branch Name
* Apidog API Documentation Link

Your GitHub branch and Apidog documentation will be used for project evaluation. Make sure both contain the final version of your project before submitting the form.

---

## Important

* Each student has **one individual project**.
* Each student must work on **their own branch**.
* Do **NOT** push directly to `main`.
* Do **NOT** merge your branch into `main`.
* Your branch is your official project submission.
* Make sure your final changes are pushed before the submission deadline.
