# Represents a node in the decision tree
class TreeNode:
    def __init__(self, text, left=None, right=None, is_result=False):
        self.text = text  # The question or result text
        self.left = left  # Left child node
        self.right = right  # Right child node
        self.is_result = is_result  # Indicates if this is a result node

# Represents a node in the stack
class StackNode:
    def __init__(self, data):
        self.data = data  # The data stored in the node
        self.next = None  # Pointer to the next node

# Represents a stack to store user command history
class HistoryStack:
    def __init__(self):
        self.top = None  # Top of the stack

    # Pushes a command onto the stack
    def push(self, command):
        node = StackNode(command)
        node.next = self.top
        self.top = node

    # Retrieves all commands from the stack
    def get_all(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    # Clears the stack
    def clear(self):
        self.top = None

# Stores bot-related data such as user histories and quiz progress
class BotData:
    def __init__(self):
        self.user_histories = {}  # Stores user command histories
        self.current_nodes = {}  # Tracks current quiz nodes for users
        self.houses = {}  # Stores user house assignments
        self.user_names = {}  # Maps user IDs to usernames

# Global instance of BotData
bot_data = BotData()