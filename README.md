# DSA_Group2_Topic14
# 📝 Mini Database Engine with Multiple Data Structures Create a simple in-memory database supporting tables (arrays/lists), indexes (BST/Hash), and queries (search, sort, join). Demonstrate different data structures' strengths.


## 👥 Thành viên nhóm 2 và Phân công công việc
* **Thành viên 1:Nguyễn Thị Đoan Trang_11245941** Xây dựng cấu trúc cốt lõi (Node, DoublyLinkedList) và hệ thống Đọc/Ghi file (File I/O).
* **Thành viên 2:Phạm Anh Thơ_11245934** Xử lý logic di chuyển con trỏ (Cursor - Lên, Xuống, Trái, Phải).
* **Thành viên 3:Nguyễn Nam Huy_11245880** Xử lý logic Thêm/Xóa văn bản (Insert/Delete).
* **Thành viên 4:Nguyễn Đình Khải_11245883** Tính năng Tìm kiếm và Thay thế (Find & Replace).
* **Thành viên 5:Trần Trúc Quỳnh_11245929** Quản lý lịch sử thao tác (Undo/Redo bằng Stack) và dựng Giao diện Menu (UI).
# 📑 Phase 1: System Architecture & Specification


## 🎯 Project Objectives
* Develop a lightweight, robust text editor operating entirely within the command-line interface (CLI) environment.
* Implement and optimize fundamental data structures—specifically a custom **Doubly Linked List** and an **Action Stack**—to handle real-time text manipulation.
* Adhere strictly to Object-Oriented Programming (OOP) principles, ensuring a clean Separation of Concerns between data storage, logical operations, and the user interface.

## 📌 System Requirements
The software architecture is engineered to satisfy the following technical specifications:
* **Memory Management:** Each individual line of text is encapsulated within a unique `Node` inside a Doubly Linked List structure to guarantee $O(1)$ structural mutations.
* **Functional Modules:**
  1. **File I/O Engine:** Streams data from external `.txt` files directly into the data structure and safely commits modifications back to disk.
  2. **Cursor Navigation Module:** Maintains an active pointer to allow free traversal (Up, Down, Left, Right) through lines and string offsets.
  3. **Text Manipulation Engine:** Supports precise string mutations, line insertions, and node deletions at the active cursor boundary.
  4. **Search & Replace Subsystem:** Executes pattern matching across the document topology to locate and substitute targeted text queries.
  5. **Transaction Ledger (Undo/Redo):** Records state transitions into a LIFO (Last-In-First-Out) Stack to guarantee safe state recovery.

## 🏗️ System Architecture
The structural layout relies on a decoupled, modular design. The UML Class Diagram below details the explicit attributes, methods, composition closures, and behavioral dependencies governing the system components.

![UML Class Diagram](UML.png)

