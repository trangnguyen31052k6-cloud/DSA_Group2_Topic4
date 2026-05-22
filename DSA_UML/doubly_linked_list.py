import os

# =========================================================
# 1. CẤU TRÚC NODE 
# (Đại diện cho 1 dòng văn bản)
# =========================================================
class Node:
    def __init__(self, data: str):
        self.data = data      # Lưu trữ nội dung của 1 dòng văn bản
        self.prev = None      # Tham chiếu về dòng phía trước
        self.next = None      # Tham chiếu tới dòng tiếp theo

# =========================================================
# 2. CLASS DOUBLY LINKED LIST 
# (Quản lý toàn bộ cấu trúc văn bản và File I/O)
# =========================================================
class DoublyLinkedList:
    def __init__(self):
        self.head = None      # Trỏ đến dòng đầu tiên của file
        self.tail = None      # Trỏ đến dòng cuối cùng của file

    def append_node(self, text: str):
        """Thêm một dòng mới vào cuối văn bản"""
        new_node = Node(text)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def insert_at_beginning(self, text: str):
        """Thêm một dòng mới vào đầu văn bản"""
        new_node = Node(text)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def remove_node(self, node: Node):
        """Xóa một Node bất kỳ khỏi danh sách (Dành cho TV 3 và TV 4 gọi)"""
        if node is None or self.head is None:
            return

        # Nếu node cần xóa là node đầu tiên
        if node == self.head:
            self.head = node.next
            if self.head is not None:
                self.head.prev = None
            else:
                self.tail = None # Danh sách rỗng sau khi xóa
        
        # Nếu node cần xóa là node cuối cùng
        elif node == self.tail:
            self.tail = node.prev
            if self.tail is not None:
                self.tail.next = None
                
        # Nếu node cần xóa nằm ở giữa
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        # Xóa tham chiếu để bộ thu gom rác (Garbage Collector) dọn dẹp
        node.prev = None
        node.next = None

    def load_from_file(self, filename: str) -> bool:
        """Đọc dữ liệu từ file .txt đưa vào Doubly Linked List"""
        if not os.path.exists(filename):
            print(f"[Lỗi] Không tìm thấy file: {filename}")
            return False
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    # Dùng strip('\n') để loại bỏ ký tự xuống dòng dư thừa khi đọc file
                    self.append_node(line.strip('\n'))
            print(f"[Thành công] Đã tải văn bản từ file {filename}!")
            return True
        except Exception as e:
            print(f"[Lỗi] Lỗi khi đọc file: {e}")
            return False

    def save_to_file(self, filename: str) -> bool:
        """Xuất dữ liệu từ Doubly Linked List ra file .txt"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                current = self.head
                while current is not None:
                    file.write(current.data + "\n")
                    current = current.next
            print(f"[Thành công] Đã lưu văn bản vào file {filename}!")
            return True
        except Exception as e:
            print(f"[Lỗi] Lỗi khi ghi file: {e}")
            return False

    def display(self):
        """Hàm in ra màn hình Terminal để test code"""
        current = self.head
        line_number = 1
        print("--- Noi dung van ban ---")
        while current is not None:
            print(f"{line_number:02d} | {current.data}")
            current = current.next
            line_number += 1
        print("------------------------")

# =========================================================
# 3. KHỐI LỆNH TEST CODE (Chỉ chạy khi mở trực tiếp file này)
# =========================================================
if __name__ == "__main__":
    # 1. Khởi tạo
    editor = DoublyLinkedList()

    # 2. Test thêm dòng
    editor.append_node("Day la dong thu nhat.")
    editor.append_node("Day la dong thu hai.")
    editor.append_node("Day la dong thu ba (se bi xoa).")
    editor.insert_at_beginning("Day la dong chen vao dau tien.")

    # 3. Test xóa dòng (Xóa dòng cuối cùng)
    node_to_delete = editor.tail 
    editor.remove_node(node_to_delete)

    # 4. In thử ra màn hình
    editor.display()

    # 5. Test xuất ra file
    editor.save_to_file("test_document.txt")

    # 6. Test đọc từ file vào một danh sách hoàn toàn mới
    print("\n--- Test Load File ---")
    editor_from_file = DoublyLinkedList()
    editor_from_file.load_from_file("test_document.txt")
    editor_from_file.display()