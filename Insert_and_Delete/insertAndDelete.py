class InsertAndDelete:
    def __init__(self,document, cursor):
        self.document = document
        self.cursor = cursor

    def Insert_at_cursor(self, text):
        current_line = self.cursor.current_node.data
        position = self.cursor.col_index

        left = current_line[:position]
        right = current_line[position:]

        new_line = left + text + right

        self.cursor.current_node.data = new_line

        self.cursor.col_index = position + len(text)

    def Backspace_key(self):
        current_line = self.cursor.current_node.data
        position = self.cursor.col_index

        if self.cursor.col_index == 0 and self.cursor.current_node.prev:
            
            prev_node = self.cursor.current_node.prev
            future_position = len(prev_node.data)

            curr_node = self.cursor.current_node

            self.cursor.current_node.prev.data += curr_node.data

            self.document.remove_node(curr_node) 
            self.cursor.current_node = prev_node

            self.cursor.col_index = future_position
            
        elif position == 0:
            return
        
        else:
            left = current_line[:position - 1]
            right = current_line[position:]

            new_line = left + right
            self.cursor.current_node.data = new_line
            
            self.cursor.col_index -= 1


    def Enter_key(self):
        current_line = self.cursor.current_node.data
        position = self.cursor.col_index

        left = current_line[:position]
        right = current_line[position:]

        self.cursor.current_node.data = left
        self.document.insert_after_node(self.cursor.current_node, right)

        self.cursor.move_down()
        self.cursor.col_index = 0

    



    
