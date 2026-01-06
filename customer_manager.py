"""
Customer management CLI for adding, listing, editing, and deleting customers.
Data is stored locally in JSON format. Table rendering is done without extra
packages to keep the script portable.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Optional

DATA_FILE = "customers.json"


def load_customers(path: str = DATA_FILE) -> List[dict]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    if not isinstance(data, list):
        return []
    return data


def save_customers(customers: List[dict], path: str = DATA_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2)


def next_id(customers: List[dict]) -> int:
    if not customers:
        return 1
    return max(c.get("id", 0) for c in customers) + 1


def render_table(rows: List[dict]) -> str:
    if not rows:
        return "(no customers yet)"

    headers = ["ID", "Name", "Phone", "Email", "Notes"]
    keys = ["id", "name", "phone", "email", "notes"]
    str_rows = [[str(row.get(key, "")) for key in keys] for row in rows]

    widths = [len(header) for header in headers]
    for row in str_rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    def format_row(parts: List[str]) -> str:
        return " | ".join(part.ljust(widths[idx]) for idx, part in enumerate(parts))

    horizontal = "-+-".join("-" * width for width in widths)
    lines = [format_row(headers), horizontal]
    for row in str_rows:
        lines.append(format_row(row))
    return "\n".join(lines)


def list_customers(args: argparse.Namespace) -> None:
    customers = load_customers()
    print(render_table(customers))


def add_customer(args: argparse.Namespace) -> None:
    customers = load_customers()
    customer = {
        "id": next_id(customers),
        "name": args.name,
        "phone": args.phone or "",
        "email": args.email or "",
        "notes": args.notes or "",
    }
    customers.append(customer)
    save_customers(customers)
    print("Added customer:")
    print(render_table([customer]))


def find_customer(customers: List[dict], customer_id: int) -> Optional[dict]:
    for customer in customers:
        if customer.get("id") == customer_id:
            return customer
    return None


def edit_customer(args: argparse.Namespace) -> None:
    customers = load_customers()
    customer = find_customer(customers, args.id)
    if customer is None:
        print(f"Customer with ID {args.id} not found.")
        sys.exit(1)

    if args.name is not None:
        customer["name"] = args.name
    if args.phone is not None:
        customer["phone"] = args.phone
    if args.email is not None:
        customer["email"] = args.email
    if args.notes is not None:
        customer["notes"] = args.notes

    save_customers(customers)
    print("Updated customer:")
    print(render_table([customer]))


def delete_customer(args: argparse.Namespace) -> None:
    customers = load_customers()
    customer = find_customer(customers, args.id)
    if customer is None:
        print(f"Customer with ID {args.id} not found.")
        sys.exit(1)
    customers = [c for c in customers if c.get("id") != args.id]
    save_customers(customers)
    print(f"Deleted customer {args.id}.")
    if customers:
        print("Remaining customers:")
        print(render_table(customers))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage customers in a tidy spreadsheet-like list.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="Show all customers")
    list_parser.set_defaults(func=list_customers)

    add_parser = subparsers.add_parser("add", help="Add a new customer")
    add_parser.add_argument("name", help="Customer name")
    add_parser.add_argument("--phone", help="Phone number")
    add_parser.add_argument("--email", help="Email address")
    add_parser.add_argument("--notes", help="Notes or reminders")
    add_parser.set_defaults(func=add_customer)

    edit_parser = subparsers.add_parser("edit", help="Edit an existing customer")
    edit_parser.add_argument("id", type=int, help="Customer ID to edit")
    edit_parser.add_argument("--name", help="New name")
    edit_parser.add_argument("--phone", help="New phone number")
    edit_parser.add_argument("--email", help="New email")
    edit_parser.add_argument("--notes", help="New notes")
    edit_parser.set_defaults(func=edit_customer)

    delete_parser = subparsers.add_parser(
        "delete", help="Remove a customer from the list"
    )
    delete_parser.add_argument("id", type=int, help="Customer ID to delete")
    delete_parser.set_defaults(func=delete_customer)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
