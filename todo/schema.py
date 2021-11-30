instructions = [
    'DROP TABLE IF EXISTS todo;',
    'DROP TABLE IF EXISTS users;',
    """
        CREATE TABLE users (
            id INT PRIMARY KEY IDENTITY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(150) NOT NULL
        )
    """,
    """
        CREATE TABLE dbo.todo (
            id INT PRIMARY KEY IDENTITY,
            created_by INT NOT NULL,
            created_at DATE NOT NULL,
            description TEXT NOT NULL,
            completed BIT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    """
]