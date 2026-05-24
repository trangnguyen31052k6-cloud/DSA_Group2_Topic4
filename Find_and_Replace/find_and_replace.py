from doubly_linked_list import DoublyLinkedList, Node


class FindAndReplace:
    """
    Module tìm kiếm và thay thế văn bản trong Doubly Linked List.
    Mỗi Node đại diện cho 1 dòng văn bản.
    """

    def __init__(self, document: DoublyLinkedList):
        self.document = document

    # =========================================================
    # 1. FIND — Duyệt tuần tự, trả về danh sách kết quả
    # =========================================================
    def find(self, keyword: str) -> list[dict]:
        """
        Duyệt tuần tự toàn bộ DLL để tìm tất cả vị trí xuất hiện của keyword.

        Trả về danh sách các dict:
            {
                "node"     : <Node object>,   # node chứa kết quả
                "line"     : int,             # số thứ tự dòng (bắt đầu từ 1)
                "col_start": int,             # vị trí bắt đầu trong node.data
                "col_end"  : int,             # vị trí kết thúc (exclusive)
                "context"  : str              # nội dung dòng để hiển thị
            }
        """
        if not keyword:
            return []

        results = []
        current = self.document.head
        line_number = 1

        while current is not None:
            line_data = current.data
            search_from = 0

            # Tìm tất cả vị trí khớp trong cùng 1 dòng
            while True:
                col_start = line_data.find(keyword, search_from)
                if col_start == -1:
                    break

                results.append({
                    "node"     : current,
                    "line"     : line_number,
                    "col_start": col_start,
                    "col_end"  : col_start + len(keyword),
                    "context"  : line_data
                })

                search_from = col_start + len(keyword)

            current = current.next
            line_number += 1

        return results

    # =========================================================
    # 2. REPLACE FIRST — Thay thế lần xuất hiện đầu tiên
    # =========================================================
    def replace_first(self, keyword: str, new_text: str) -> bool:
        """
        Thay thế lần xuất hiện đầu tiên của keyword bằng new_text.
        Trả về True nếu thay thế thành công, False nếu không tìm thấy.

        Sơ đồ pointer logic:
          TRƯỚC:  node.data = [ left | keyword | right ]
          SAU:    node.data = [ left | new_text | right ]
        """
        results = self.find(keyword)
        if not results:
            print(f'[Find & Replace] Không tìm thấy: "{keyword}"')
            return False

        match = results[0]
        node = match["node"]
        left  = node.data[:match["col_start"]]
        right = node.data[match["col_end"]:]
        node.data = left + new_text + right

        print(f'[Find & Replace] Đã thay thế dòng {match["line"]}: '
              f'"{keyword}" → "{new_text}"')
        return True

    # =========================================================
    # 3. REPLACE ALL — Thay thế tất cả lần xuất hiện
    # =========================================================
    def replace_all(self, keyword: str, new_text: str) -> int:
        """
        Thay thế tất cả lần xuất hiện của keyword bằng new_text.
        Trả về số lần thay thế đã thực hiện.

        Dùng str.replace() trên node.data để xử lý tất cả match trong 1 dòng
        một lần duy nhất → O(n) trên từng dòng.
        Python tự thu hồi bộ nhớ string cũ (garbage collection).
        """
        if not keyword:
            return 0

        count = 0
        current = self.document.head
        line_number = 1

        while current is not None:
            occurrences = current.data.count(keyword)
            if occurrences > 0:
                current.data = current.data.replace(keyword, new_text)
                count += occurrences
                print(f'[Find & Replace] Dòng {line_number}: thay {occurrences} lần')

            current = current.next
            line_number += 1

        print(f'[Find & Replace] Tổng cộng đã thay thế {count} lần.')
        return count