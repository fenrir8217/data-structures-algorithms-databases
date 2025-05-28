from AVLTree import AVLTree

avl = AVLTree()

# List of values to insert
values = [37, 24, 42, 7, 32, 40, 44, 2, 120]
# Insert all values using a loop
for value in values:
    avl.insert(value)

avl.print_tree();

avl.insert(45)

avl.print_tree();

avl.delete(45)
avl.print_tree();
