```markdown
# Your Flask Application

This is a simple guide on how to migrate your Flask database using Flask-Migrate.

## Installation

Make sure you have Python and pip installed. Then install Flask-Migrate:

```bash
pip install Flask-Migrate
```

## Configuration

Ensure that your Flask application is properly configured. Modify the `config.py` file with your database configuration.

## Initialize Migration

Navigate to your Flask application directory and run:

```bash
flask db init
```

This initializes the migration environment and creates a `migrations` folder in your project directory.

## Create a Migration

After making changes to your models or database schema, generate a migration:

```bash
flask db migrate -m "Your migration message"
```

Replace "Your migration message" with a descriptive message of the changes.

## Apply the Migration

Apply the migration to your database:

```bash
flask db upgrade
```

This updates your database schema based on the migration script.

## Verify Database

Verify that your database has been updated with the changes.

## Additional Notes

- Include the `migrations` folder in your version control system, but exclude the `*.db` file to avoid unnecessary versioning of the database.

- Ensure your database connection details in your Flask app match those configured in your migration script.

```

Customize this template based on your specific application structure and requirements.