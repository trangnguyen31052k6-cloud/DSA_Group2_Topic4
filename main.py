import os
import traceback
from doubly_linked_list import DoublyLinkedList, Node
from cursor_and_texteditor import Cursor 
from insertAndDelete import InsertAndDelete
from find_and_replace import FindAndReplace

class ActionStack:
    """
    Architecture: Hybrid Command + Snapshot Strategy
    - Command Pattern: For lightweight, incremental operations (insert, delete, enter).
    - Snapshot (Memento) Pattern: For mass structural mutations (replace_all).
    """
    def __init__(self, document):
        self.document = document
        self.history = []      
        self.redo_stack = []   

    def push(self, action_type, node=None, col=0, data=None, snapshot=None):
        """Records the action before state mutation."""
        self.history.append({
            'type': action_type,
            'node': node,
            'col': col,
            'data': data,
            'snapshot': snapshot 
        })
        self.redo_stack.clear()

    def create_snapshot(self, cursor):
        """
        Captures full document state AND cursor position.
        Prevents cursor reset issue upon restoration.
        """
        snapshot_data = []
        current = self.document.head
        cursor_line_idx = 0
        current_idx = 0
        
        while current:
            snapshot_data.append(current.data)
            if current == cursor.current_node:
                cursor_line_idx = current_idx
            current = current.next
            current_idx += 1
            
        return {
            'text_array': snapshot_data,
            'cursor_line': cursor_line_idx,
            'cursor_col': cursor.col_index
        }

    def restore_snapshot(self, snapshot, cursor):
        """
        Reconstructs the Doubly Linked List from snapshot data.
        Note: Old nodes become orphans and are reclaimed by Python's Garbage Collector.
        """
        data = snapshot['text_array']
        if not data:
            return
            
        self.document.head = Node(data[0])
        self.document.tail = self.document.head
        
        current = self.document.head
        target_cursor_node = self.document.head if snapshot['cursor_line'] == 0 else None

        for i, text in enumerate(data[1:], 1):
            new_node = Node(text)
            current.next = new_node
            new_node.prev = current
            current = new_node
            self.document.tail = current
            
            if i == snapshot['cursor_line']:
                target_cursor_node = current
                
        cursor.current_node = target_cursor_node if target_cursor_node else self.document.head
        cursor.col_index = snapshot['cursor_col']

    def undo(self, cursor):
        if not self.history:
            print("\n[Undo] No actions to undo.")
            return

        action = self.history.pop()
        
        # Explicit dict creation prevents shallow copy/shared state bugs
        redo_action = {
            'type': action['type'],
            'node': action['node'],
            'col': action['col'],
            'data': action['data'],
            'snapshot': self.create_snapshot(cursor) if action['type'] == 'replace_all' else None
        }
        self.redo_stack.append(redo_action) 

        if action['type'] == 'replace_all':
            self.restore_snapshot(action['snapshot'], cursor)
            print("\n[Undo] Restored state prior to Replace All.")
            return

        node = action['node']
        col = action['col']

        if action['type'] == 'insert':
            text_len = len(action['data'])
            node.data = node.data[:col] + node.data[col + text_len:]
            cursor.current_node = node
            cursor.col_index = col
            
        elif action['type'] == 'enter':
            if node.next:
                node.data += node.next.data 
                self.document.remove_node(node.next) 
            cursor.current_node = node
            cursor.col_index = col
            
        elif action['type'] == 'backspace_char':
            char = action['data']
            node.data = node.data[:col-1] + char + node.data[col-1:]
            cursor.current_node = node
            cursor.col_index = col
            
        elif action['type'] == 'backspace_merge':
            right_text = node.data[col:]
            node.data = node.data[:col] 
            self.document.insert_after_node(node, right_text) 
            cursor.current_node = node.next
            cursor.col_index = 0
            
        elif action['type'] == 'forward_delete':
            char = action['data']
            node.data = node.data[:col] + char + node.data[col:]
            cursor.current_node = node
            cursor.col_index = col

        print(f"\n[Undo] Reverted: {action['type']}")

    def redo(self, cursor):
        if not self.redo_stack:
            print("\n[Redo] No actions to redo.")
            return

        action = self.redo_stack.pop()
        
        undo_action = {
            'type': action['type'],
            'node': action['node'],
            'col': action['col'],
            'data': action['data'],
            'snapshot': self.create_snapshot(cursor) if action['type'] == 'replace_all' else None
        }
        self.history.append(undo_action) 

        if action['type'] == 'replace_all':
            self.restore_snapshot(action['snapshot'], cursor)
            print("\n[Redo] Re-applied Replace All.")
            return

        node = action['node']
        col = action['col']

        if action['type'] == 'insert':
            text = action['data']
            node.data = node.data[:col] + text + node.data[col:]
            cursor.current_node = node
            cursor.col_index = col + len(text)
            
        elif action['type'] == 'enter':
            right_text = node.data[col:]
            node.data = node.data[:col]
            self.document.insert_after_node(node, right_text)
            cursor.current_node = node.next
            cursor.col_index = 0
            
        elif action['type'] == 'backspace_char':
            node.data = node.data[:col-1] + node.data[col:]
            cursor.current_node = node
            cursor.col_index = col - 1
            
        elif action['type'] == 'backspace_merge':
            if node.next:
                node.data += node.next.data
                self.document.remove_node(node.next)
            cursor.current_node = node
            cursor.col_index = col
            
        elif action['type'] == 'forward_delete':
            node.data = node.data[:col] + node.data[col+1:]
            cursor.current_node = node
            cursor.col_index = col

        print(f"\n[Redo] Re-applied: {action['type']}")


def run_ui():
    document = DoublyLinkedList()
    cursor = Cursor(document.head)
    history = ActionStack(document)
    
    inserter = InsertAndDelete(document, cursor)
    finder = FindAndReplace(document)
    
    def clear_screen():
        """Safe console clear with fallback for IDE terminals."""
        try:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        except:
            print("\n" * 50)

    def print_editor():
        clear_screen()
        print("="*60)
        print("         DLL TEXT EDITOR - ENHANCED ARCHITECTURE         ")
        print("="*60)
        current = document.head
        line_num = 1
        while current:
            if current == cursor.current_node:
                text = current.data
                col = cursor.col_index
                display_text = text[:col] + "█" + text[col:] 
                print(f" {line_num:02d} | {display_text}")
            else:
                print(f" {line_num:02d} | {current.data}")
            current = current.next
            line_num += 1
        print("="*60)
        print(" [1] Type     [2] Enter   [3] Backspace  [4] Delete")
        print(" [5] Replace  [6] W/A/S/D [7] Undo       [8] Redo")
        print(" [9] I/O File [0] Exit")
        print("="*60)

    while True:
        print_editor()
        choice = input("\n[?] Select an option: ")
        
        try:
            if choice == "1":
                text = input("Enter text: ")
                if text:
                    history.push("insert", cursor.current_node, cursor.col_index, text)
                    inserter.Insert_at_cursor(text) 
                
            elif choice == "2":
                history.push("enter", cursor.current_node, cursor.col_index)
                inserter.Enter_key()
                
            elif choice == "3":
                node = cursor.current_node
                col = cursor.col_index
                if col == 0 and node.prev:
                    history.push("backspace_merge", node.prev, len(node.prev.data))
                elif col > 0:
                    history.push("backspace_char", node, col, node.data[col-1])
                inserter.Backspace_key()
                
            elif choice == "4":
                node = cursor.current_node
                col = cursor.col_index
                if col < len(node.data):
                    history.push("forward_delete", node, col, node.data[col])
                    inserter.forward_delete() 
                
            elif choice == "5":
                keyword = input("Find: ")
                new_text = input("Replace with: ")
                
                # Snapshot captures both text array and cursor state
                old_snapshot = history.create_snapshot(cursor)
                finder.replace_all(keyword, new_text)
                
                history.push("replace_all", snapshot=old_snapshot)
                
            elif choice == "6":
                direction = input("Direction (W=Up, S=Down, A=Left, D=Right): ").upper()
                if direction == 'W': cursor.move_up()
                elif direction == 'S': cursor.move_down()
                elif direction == 'A': cursor.move_left()
                elif direction == 'D': cursor.move_right()
                
            elif choice == "7":
                history.undo(cursor)
                input("\nPress Enter to continue...") 
                
            elif choice == "8":
                history.redo(cursor)
                input("\nPress Enter to continue...")
                
            elif choice == "9":
                sub = input("Open (O) or Save (S)? ").upper()
                filename = input("Filename: ")
                if sub == 'O':
                    if document.load_from_file(filename):
                        cursor.current_node = document.head
                        cursor.col_index = 0
                        history.history.clear()
                        history.redo_stack.clear()
                elif sub == 'S':
                    document.save_to_file(filename)
                input("\nPress Enter to continue...")
                    
            elif choice == "0":
                print("\nExiting...")
                break
                
        except KeyboardInterrupt:
            print("\n[System] Emergency interrupt received. Exiting...")
            break
            
        except Exception as e:
            # Professional Error Logging - Tránh nuốt lỗi mù mờ
            print(f"\n[Core System Error]: {type(e).__name__} - {e}")
            print(f"[Detailed Traceback]:\n{traceback.format_exc()}")
            input("Press Enter to recover interface...")

if __name__ == "__main__":
    run_ui()