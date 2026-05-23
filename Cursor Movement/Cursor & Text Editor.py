class Cursor:
    """
    Manages the current coordinates of the user within the text document.
    """
    def __init__(self, start_node):
        # Initialize cursor at the first node of the document
        self.current_node = start_node
        self.col_index = 0

    def move_up(self):
        # Move cursor to the previous line
        if self.current_node is not None and self.current_node.prev is not None:
            self.current_node = self.current_node.prev
            # Prevent out-of-bounds index on the new line
            self.col_index = min(self.col_index, len(self.current_node.data))

    def move_down(self):
        # Move cursor to the next line
        if self.current_node is not None and self.current_node.next is not None:
            self.current_node = self.current_node.next
            self.col_index = min(self.col_index, len(self.current_node.data))

    def move_left(self):
        # Move cursor left by one character
        if self.col_index > 0:
            self.col_index -= 1

    def move_right(self):
        # Move cursor right by one character
        if self.current_node is not None and self.col_index < len(self.current_node.data):
            self.col_index += 1


class TextEditor:
    """
    Business Logic Layer: Acts as the central controller.
    Manages data flow between the Web GUI, DoublyLinkedList, and ActionStack.
    """
    def __init__(self, document_instance, history_instance):
        # Inject dependencies (Separation of Concerns)
        self.document = document_instance
        self.history = history_instance
        self.cursor = Cursor(self.document.head)

    def insert_text(self, text: str):
        # Step 1: Save state to ActionStack before modification
        self.history.push_action("insert", self.cursor.current_node, text)
        
        # Step 2: Call Data Access Layer to insert data
        self.document.insert_after_node(self.cursor.current_node, text)
        
        # Step 3: Update cursor position to the newly inserted node
        self.cursor.move_down()

    def delete_text(self):
        if self.cursor.current_node is None:
            return
            
        node_to_delete = self.cursor.current_node
        
        # Step 1: Save state to ActionStack before deletion
        self.history.push_action("delete", node_to_delete, node_to_delete.data)
        
        # Step 2: Update cursor reference before disconnecting the node
        if node_to_delete.prev:
            self.cursor.move_up()
        elif node_to_delete.next:
            self.cursor.move_down()
            
        # Step 3: Call Data Access Layer to remove the node
        self.document.remove_node(node_to_delete)

    def find_and_replace(self):
        # Placeholder for Member 3/4's algorithm implementation
        pass

    def run_ui(self):
        # Web GUI event listener integration endpoint
        # (Console/CLI inputs have been removed to align with Web GUI architecture)
        pass
    