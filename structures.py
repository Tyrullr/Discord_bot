class TreeNode:
    def __init__(self, text, left=None, right=None, is_result=False):
        self.text = text
        self.left = left
        self.right = right
        self.is_result = is_result

class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class HistoryStack:
    def __init__(self):
        self.top = None

    def push(self, command):
        node = StackNode(command)
        node.next = self.top
        self.top = node

    def get_all(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self):
        self.top = None

class BotData:
    def __init__(self):
        self.user_histories = {}
        self.current_nodes = {}
        self.houses = {}
        self.user_names = {}

bot_data = BotData()