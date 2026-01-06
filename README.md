# Gardensms

Helps woth gardening customers

## Customer manager CLI

Run the Python script to manage customers in a spreadsheet-style table stored in `customers.json`:

```bash
python customer_manager.py list            # show all customers
python customer_manager.py add "Alice" --phone "555-1234" --notes "Quarterly lawn" 
python customer_manager.py edit 1 --email "alice@example.com"
python customer_manager.py delete 1
```

Example output:

```
ID | Name  | Phone    | Email | Notes
-- + ----- + -------- + ----- + ----------------
1  | Alice | 555-1234 |       | Quarterly lawn
```
