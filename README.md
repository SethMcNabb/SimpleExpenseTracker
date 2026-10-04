# Personal Finance & Relational Ledger

## Overview

For this module, I built a command-line relational database expense tracker designed to log spending across customizable categories. The purpose of this project is to implement a normalized two-table relational database schema using SQLite and Python, enforcing data integrity via foreign keys, atomic transactions, and parameterized queries.

Users can create new categories, record expense transactions tied to those categories, view transaction logs via multi-table `JOIN` statements, calculate aggregate category spending totals using `GROUP BY` and `SUM()`, and update or delete existing records.

[Software Demo Video](https://www.youtube.com/watch?v=y3zSrcx_70U)

## Relational Database Structure

The database engine is **SQLite**, with foreign key constraint enforcement explicitly activated on every connection via `PRAGMA foreign_keys = ON;`. The schema consists of two normalized tables:

1. **`categories` (Parent Table):** Stores unique expense category names (`category_id`, `name`). It acts as the parent table that classifies expenses.
2. **`transactions` (Child Table):** Stores individual spending entries (`transaction_id`, `category_id`, `amount`, `description`). It enforces referential integrity through a foreign key referencing `categories(category_id)` with `ON DELETE RESTRICT` to prevent orphaned transaction records.

## Development Environment

- **Language:** Python
- **Database Engine:** SQLite 3
- **Tools:** Visual Studio Code, Integrated Terminal, SQLite Viewer
- **Version Control:** Git & GitHub

## Useful Websites

- [SQLite Documentation - Foreign Key Support](https://www.sqlite.org/foreignkeys.html)
- [Python sqlite3 Standard Library Documentation](https://docs.python.org/3/library/sqlite3.html)
- [W3Schools - SQL INNER JOIN Keyword](https://www.w3schools.com/sql/sql_join.asp)
- [SQLite Documentation - Aggregate Functions (SUM, COALESCE)](https://www.sqlite.org/lang_aggfunc.html)

## Future Work

- Expand schema to include a third parent table for `accounts` (Checking, Savings, Credit Cards) to track balances across multiple funding sources.
- Add budget limits to the `categories` table and calculate remaining allowances in the aggregate summary report.
- Implement date filtering and CSV export capabilities for periodic reporting.

## AI Disclosure

- **Tool Used:** Gemini
- **Purpose:** Refreshing myself on Python and SQL syntax, clarifying SQLite foreign key syntax and PRAGMA settings, troubleshooting schema DDL constraints, and discussing best practices for parameterized SQL queries in Python.
- **What Code was Influenced:** Structure of `schema.sql` for table relationships and foreign key syntax, using `executescript()` to initialize DDL, and parameterized query syntax (`?`) for safe inserts, updates, and deletes.
- **What I Changed to Make It Mine:** Designed and streamlined the schema to a focused two-table architecture (`categories` and `transactions`), authored the CLI menu loop, wrote the table formatting and user prompts, implemented custom error handling for invalid input and foreign key violations, and wrote seeding logic for default categories.
- **What I Learned & Why I Accepted the Suggestion:** I learned that SQLite disables foreign key enforcement by default for backward compatibility, requiring `PRAGMA foreign_keys = ON;` on every new connection. I also learned how to use `LEFT JOIN` alongside `COALESCE(SUM(...), 0.0)` so categories without logged transactions still appear accurately in reporting summaries.