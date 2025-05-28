from TreeNode import TreeNode

class AVLTree:
    def __init__(self):
        self.root = None  # Track the root node

    # ------------------------------
    # 1. INSERTION OPERATION
    # ------------------------------
    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, root, key):
        if not root:
            return TreeNode(key)

        if key < root.value:
            root.left = self._insert_recursive(root.left, key)
        else:
            root.right = self._insert_recursive(root.right, key)

        # Update height and balance
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        return self._balance(root, key)

    # ------------------------------
    # 2. DELETION OPERATION
    # ------------------------------
    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key):
        if not root:
            return root

        if key < root.value:
            root.left = self._delete_recursive(root.left, key)
        elif key > root.value:
            root.right = self._delete_recursive(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.getMinValueNode(root.right)
            root.value = temp.value
            root.right = self._delete_recursive(root.right, temp.value)

        if not root:
            return root

        # Update height and balance
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        return self._balance(root, key)

    # ------------------------------
    # 3. BALANCING METHODS
    # ------------------------------
    def _balance(self, root, key):
        balance = self.getBalance(root)

        # LL Case
        if balance > 1 and key < root.left.value:
            return self.rightRotate(root)

        # RR Case
        if balance < -1 and key > root.right.value:
            return self.leftRotate(root)

        # LR Case
        if balance > 1 and key > root.left.value:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # RL Case
        if balance < -1 and key < root.right.value:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    # ------------------------------
    # 4. ROTATIONS
    # ------------------------------
    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def rightRotate(self, y):
        x = y.left # Step 1: Identify the new root (x)
        T2 = x.right # Step 2: Store x's right subtree (T2)

        x.right = y # Step 3: Move y down, making it x's right child
        y.left = T2 # Step 4: Reattach T2 as y's left subtree

        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        return x

    # ------------------------------
    # 5. HELPER FUNCTIONS
    # ------------------------------
    def getHeight(self, root):
        return root.height if root else 0

    def getBalance(self, root):
        return self.getHeight(root.left) - self.getHeight(root.right) if root else 0

    def getMinValueNode(self, root):
        while root.left:
            root = root.left
        return root

    # ------------------------------
    # 6. PRINT TREE METHOD (FIXED)
    # ------------------------------
    def print_tree(self):
        if not self.root:
            print("Tree is empty")
        else:
            lines, *_ = self._display_aux(self.root)
            for line in lines:
                print(line)

    def _display_aux(self, node):
        """Helper function to visually print the tree structure."""
        if node is None:
            return [""]

        # Case: Node is a leaf
        if node.left is None and node.right is None:
            line = f"{node.value}"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Case: Node has only a left child
        if node.right is None:
            left_lines, left_width, left_height, left_middle = self._display_aux(node.left)
            s = f"{node.value}"
            u = len(s)
            first_line = (left_middle + 1) * " " + (left_width - left_middle - 1) * "_" + s
            second_line = left_middle * " " + "/" + (left_width - left_middle - 1 + u) * " "
            shifted_lines = [line + u * " " for line in left_lines]
            return [first_line, second_line] + shifted_lines, left_width + u, left_height + 2, left_width + u // 2

        # Case: Node has only a right child
        if node.left is None:
            right_lines, right_width, right_height, right_middle = self._display_aux(node.right)
            s = f"{node.value}"
            u = len(s)
            first_line = s + right_middle * "_" + (right_width - right_middle) * " "
            second_line = (u + right_middle) * " " + "\\" + (right_width - right_middle - 1) * " "
            shifted_lines = [u * " " + line for line in right_lines]
            return [first_line, second_line] + shifted_lines, right_width + u, right_height + 2, u // 2

        # Case: Node has two children
        left_lines, left_width, left_height, left_middle = self._display_aux(node.left)
        right_lines, right_width, right_height, right_middle = self._display_aux(node.right)
        s = f"{node.value}"
        u = len(s)
        first_line = (left_middle + 1) * " " + (left_width - left_middle - 1) * "_" + s + right_middle * "_" + (right_width - right_middle) * " "
        second_line = left_middle * " " + "/" + (left_width - left_middle - 1 + u + right_middle) * " " + "\\" + (right_width - right_middle - 1) * " "
        if left_height < right_height:
            left_lines += [left_width * " "] * (right_height - left_height)
        elif right_height < left_height:
            right_lines += [right_width * " "] * (left_height - right_height)
        zipped_lines = zip(left_lines, right_lines)
        lines = [first_line, second_line] + [a + u * " " + b for a, b in zipped_lines]
        return lines, left_width + right_width + u, max(left_height, right_height) + 2, left_width + u // 2

