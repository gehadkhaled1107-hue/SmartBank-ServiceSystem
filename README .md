# SIC Smart Bank System

## Overview

SIC Smart Bank System is a command-line banking application built in Python. It simulates core banking operations — account registration, authentication, wallet transactions, ATM/branch monitoring, and administrative reporting — entirely through in-memory data structures, with no external database. The system is organized into independent modules (Core & Authentication, Wallet & Transactions, ATM Matrix, Account Settings, and Admin Reports) that operate on a single shared user data structure.

## Data Structures Used & Their Purpose

| Data Structure | Where It's Used | Why It Was Chosen |
|---|---|---|
| **List of Nested Dictionaries** | `user_data` — the master collection of all registered users | Each user is a self-contained record; a list allows ordered iteration and easy appending of new users, while nested dictionaries let each record group related data (`profile`, `security`, `wallet`, `transactions`, `settings`) under clear, named keys instead of flat, ambiguous fields. |
| **Dictionary (per user record)** | Each element of `user_data`, and its sub-sections (`profile`, `security`, `wallet`, `settings`) | Dictionaries provide fast, direct key-based access (e.g., `user["security"]["is_locked"]`) and make the schema self-documenting. Methods such as `.update()`, `.get()`, `.pop()`, and `.items()` are used throughout Account Settings and Admin Reports to modify or inspect fields safely. |
| **List** | `transactions` and `login_attempts` (per user) | Both are chronological, append-only logs. Lists preserve insertion order and support **indexing and slicing** (`transactions[0]`, `transactions[-1]`, `transactions[-5:]`, `login_attempts[-3:]`) to retrieve the first, most recent, or last-N entries efficiently. |
| **2D List (List of Lists)** | `atm_matrix` | ATM/branch status is naturally grid-shaped (row = branch, column = machine). A 2D list allows direct row/column addressing (`atm_matrix[row][col]`) for both display and status updates, including support for jagged (unequal-length) rows. |
| **Set** | `active_users`, `vip_users`, `failed_login_users`, `users_with_transfers`, `dup_phones`, `dup_emails` | Sets enforce uniqueness automatically and provide fast membership testing (`in`). They also enable direct use of set algebra — intersection (`&`), union (`|`), difference (`-`), and symmetric difference (`^`) — to build the VIP/active user segmentation reports without manual loops. |
| **`defaultdict`** | `transaction_frequency_report()` | Counting occurrences of each transaction type (deposit/withdraw/transfer) requires incrementing a counter for keys that may not exist yet. `defaultdict(int)` removes the need for manual key-existence checks. |
| **Tuple** | Fixed validation sets, e.g. `status not in (0, 1)`, `choice in ("0", "1", "2", "3", "4")` | Tuples are used for small, fixed, unchanging collections of valid options — signaling that these values are constants that should not be modified at runtime. |

## Copy / Deepcopy Scenario

`copy.deepcopy()` is used in two places where a user record must be duplicated **without** the copy sharing memory with the original:

1. **Registration (`Authentication.py`)** — before a newly built user dictionary is appended to `user_data`, it is passed through `deepcopy()` to guarantee the stored record is fully independent of any local variables used during input collection.
2. **Profile Snapshot (`ACCOUNT_SETTINGS`)** — before any sensitive change (city, phone, password, emergency contact), `copy.deepcopy(user["profile"])` is taken and stored in `user["settings"]["last_snapshot"]`. Because the user record contains **nested** dictionaries, a shallow copy would still reference the same inner dictionaries — mutating the "snapshot" whenever the live profile changes. `deepcopy()` recursively copies every nested level, so the snapshot remains a true, isolated backup that can be safely inspected or restored later.

