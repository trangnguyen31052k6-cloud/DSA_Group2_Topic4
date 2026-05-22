import os

# =========================================================
# 1. CẤU TRÚC NODE 
# (Đại diện cho 1 dòng văn bản)
# =========================================================
class Node:
    def __init__(self, data: str):
        self.data = data      
        self.prev = None      
        self.next = None      

# =========================================================
# 2. CLASS DOUBLY LINKED LIST 
# (Quản lý toàn bộ cấu trúc văn bản và File I/O)
# =========================================================
class DoublyLinkedList:
    def __init__(self):
        # [CẬP NHẬT CHO TV2]: Khởi tạo sẵn 1 dòng trống thay vì None 
        # để Cursor không bị lỗi khi mở app lên gõ luôn.
        self.head = Node("")
        self.tail = self.head

    def append_node(self, text: str):
        """Thêm một dòng mới vào cuối văn bản"""
        # [CẬP NHẬT]: Nếu danh sách đang chỉ có 1 dòng trống mặc định thì ghi đè luôn
        if self.head == self.tail and self.head.data == "":
            self.head.data = text
            return

        new_node = Node(text)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def insert_at_beginning(self, text: str):
        """Thêm một dòng mới vào đầu văn bản"""
        if self.head == self.tail and self.head.data == "":
            self.head.data = text
            return
            
        new_node = Node(text)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    # [CẬP NHẬT CHO TV3]: Hàm chèn dòng mới vào giữa khi người dùng ấn Enter
    def insert_after_node(self, current_node: Node, text: str):
        """Chèn một dòng mới ngay sau dòng hiện tại"""
        if current_node is None:
            return
        
        new_node = Node(text)
        new_node.prev = current_node
        new_node.next = current_node.next
        
        if current_node.next is not None:
            current_node.next.prev = new_node
        else:
            self.tail = new_node # Nếu chèn sau node cuối, cập nhật lại tail
            
        current_node.next = new_node

    def remove_node(self, node: Node):
        """Xóa một Node bất kỳ khỏi danh sách"""
        if node is None or self.head is None:
            return

        if node == self.head:
            self.head = node.next
            if self.head is not None:
                self.head.prev = None
            else:
                self.tail = None 
        elif node == self.tail:
            self.tail = node.prev
            if self.tail is not None:
                self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        node.prev = None
        node.next = None

        # [CẬP NHẬT]: Đảm bảo văn bản không bao giờ bị "chết" (None) hoàn toàn
        if self.head is None:
            self.head = self.tail = Node("")

    def load_from_file(self, filename: str) -> bool:
        """Đọc dữ liệu từ file .txt đưa vào Doubly Linked List"""
        if not os.path.exists(filename):
            print(f"[Lỗi] Không tìm thấy file: {filename}")
            return False
        
        try:
            # [CẬP NHẬT CHO TV5]: Reset sạch văn bản cũ trước khi load file mới
            self.head = Node("")
            self.tail = self.head

            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
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
# 3. KHỐI LỆNH TEST CODE
# =========================================================
if __name__ == "__main__":
    editor = DoublyLinkedList()

    editor.append_node("Day la dong thu nhat.")
    editor.append_node("Day la dong thu hai.")
    
    # Test chèn vào giữa
    node_thu_nhat = editor.head
    editor.insert_after_node(node_thu_nhat, "Day la dong chen vao giua bang Enter.")
    
    editor.append_node("Day la dong thu ba (se bi xoa).")
    editor.insert_at_beginning("Day la dong chen vao dau tien.")

    node_to_delete = editor.tail 
    editor.remove_node(node_to_delete)

    editor.display()
    editor.save_to_file("test_document.txt")

    print("\n--- Test Load File ---")
    editor_from_file = DoublyLinkedList()
    # Test thử việc gõ chữ rác vào trước khi load
    editor_from_file.append_node("Chu rac...") 
    editor_from_file.load_from_file("test_document.txt")
    editor_from_file.display()