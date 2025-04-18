import unittest
import du09_balanced_bst as du
import os
import subprocess


Node = du.Node
BSTree = du.BSTree


"""
Najprv je potrebné nainštalovať Graphviz, aby tento program správne fungoval:
1. Otvorte WSL na počítači (musi byť Ubuntu alebo Debian).
2. Zadajte: sudo apt update
3. Zadajte: sudo apt install graphviz
4. Overte inštaláciu príkazom: dot -V

Pred spustením kódu je dôležité zmeniť hodnotu premennej directory (pozri nižšie)
na adresár, v ktorom sa nachádza súbor du09. Uistite sa,
že úvodzovky okolo adresy zostanú neporušené – stačí skopírovať adresu medzi úvodzovky (r"nova_adresa")
"""

path = os.getcwd()
directory = rf"{path}"

# --- Convertor to WSL directory ---
if len(directory) < 3 or directory[1] != ":":
    raise ValueError("Invalid Windows path format.")

drive_letter = directory[0].lower()

rest = directory[2:]
if rest.startswith("\\") or rest.startswith("/"):
    rest = rest[1:]

rest = rest.replace("\\", "/")

wsl_directory = f"/mnt/{drive_letter}/{rest}"

# --- Download GraphViz ---
try:
    res = subprocess.run(["wsl", "bash", "-c", "dot -V"], capture_output=True, text=True, check=True)
    print(f"You do have GraphViz installed, version: {res.stdout}")
    print()

except subprocess.CalledProcessError:
    print(f"GraphViz not installed.")
    ans = input("Do you want to install? Y/N")
    ans = ans.strip().upper()

    if ans == "Y":
        try:
            first = subprocess.run(["wsl", "bash", "-c", "sudo apt update && sudo apt install graphviz"],
                       capture_output=True, text=True, check=True)
            print(f"Successfully downloaded: version: {first.stdout}")
        except subprocess.CalledProcessError:
            print("Download failed")
            print("Try again later")

def before():
    # --- To remove old photos and old tree.dot files ---
    if os.path.isdir(directory):
        print(f"Successfully found '{directory}'.")

        for item in os.listdir(directory):
            if (item.startswith("tree") or item.startswith("After")) and (
                    item.endswith(".dot") or item.endswith(".png")):
                file_path = os.path.join(directory, item)

                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except OSError as error:
                        print(f"Error deleting '{file_path}': {error}")
                else:
                    print(f"'{file_path}' is not a file.")
        print("Completed checking for 'tree.dot', 'tree.png', 'Aftertree.dot', 'Aftertree.png'.")
    else:
        print(f"Directory '{directory}' does not exit!!!")
        raise NotADirectoryError

    # --- Draw ---
    tree1, tree2, tree3, tree4, tree5 = make_trees()
    du.draw_tree(tree1, 'tree1.dot')
    du.draw_tree(tree2, 'tree2.dot')
    du.draw_tree(tree3, 'tree3.dot')
    du.draw_tree(tree4, 'tree4.dot')
    du.draw_tree(tree5, 'tree5.dot')

    # --- Make PNG trees ---
    png = ("dot -Tpng tree1.dot -o tree1.png; "
           "dot -Tpng tree2.dot -o tree2.png; "
           "dot -Tpng tree3.dot -o tree3.png; "
           "dot -Tpng tree4.dot -o tree4.png; "
           "dot -Tpng tree5.dot -o tree5.png; "
           )

    command = f"cd '{wsl_directory}' && {png}"
    subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)


def after(tree1=None, tree2=None, tree3=None, tree4=None, tree5=None):
    dot_files = []
    # --- Draw After ---
    for idx, tree in enumerate(
            (tree1, tree2, tree3, tree4, tree5), start=1):
        if tree is not None:
            du.draw_tree(tree, f"Aftertree{idx}.dot")
            dot_files.append(f"Aftertree{idx}.dot")


    png_commands = " ; ".join(
        f"dot -Tpng {dot} -o {dot[:-4]}.png" for dot in dot_files
    )

    if png_commands:
        cmd = f"cd '{wsl_directory}' && {png_commands}"
        subprocess.run(["wsl", "bash", "-c", cmd],
                       capture_output=True, text=True, check=True)

    # --- To remove tree.dot files ---
    for file_name in os.listdir(directory):
        if file_name.endswith(".dot"):
            try:
                os.remove(os.path.join(directory, file_name))
                print(f"Deleted {file_name}!!!")
            except OSError as err:
                print(f"Cannot delete {file_name}: {err}")


def update_sizes(node):
    if node is None: return 0
    node.size = 1 + update_sizes(node.left) + update_sizes(node.right)
    return node.size

def make_trees():
    # --- tree1 ---
    n1 = Node(1); n2 = Node(2, left=n1); n3 = Node(3, left=n2)
    n1.parent = n2; n2.parent = n3
    tree1 = BSTree(n3); update_sizes(tree1.root)

    # --- tree2 ---
    a1 = Node(1); a3 = Node(3)
    a2 = Node(2, left=a1, right=a3)
    a1.parent = a2; a3.parent = a2
    a5 = Node(5); a4 = Node(4, left=a2, right=a5)
    a2.parent = a4; a5.parent = a4
    tree2 = BSTree(a4); update_sizes(tree2.root)

    # --- tree3 ---
    b1 = Node(1); b3 = Node(3)
    b2 = Node(2, left=b1, right=b3)
    b1.parent = b2; b3.parent = b2
    b5 = Node(5); b7 = Node(7); b6 = Node(6, left=b5, right=b7)
    b5.parent = b6; b7.parent = b6
    b4 = Node(4, left=b2, right=b6)
    b2.parent = b4; b6.parent = b4
    tree3 = BSTree(b4); update_sizes(tree3.root)

    # --- tree4 ---
    c1 = Node(1); c2 = Node(2, left=c1); c1.parent = c2
    c3 = Node(3, left=c2); c2.parent = c3
    c5 = Node(5); c7 = Node(7); c9 = Node(9)
    c8 = Node(8, left=c7, right=c9); c7.parent = c8; c9.parent = c8
    c6 = Node(6, left=c5, right=c8); c5.parent = c6; c8.parent = c6
    c4 = Node(4, left=c3, right=c6); c3.parent = c4; c6.parent = c4
    tree4 = BSTree(c4); update_sizes(tree4.root)

    # --- tree5 ---
    d0 = Node(0); d1 = Node(1, left=d0); d0.parent = d1
    d3 = Node(3); d2 = Node(2, left=d1, right=d3); d1.parent = d2; d3.parent = d2
    d5 = Node(5); d7 = Node(7); d9 = Node(9)
    d8 = Node(8, left=d7, right=d9); d7.parent = d8; d9.parent = d8
    d6 = Node(6, left=d5, right=d8); d5.parent = d6; d8.parent = d6
    d4 = Node(4, left=d2, right=d6); d2.parent = d4; d6.parent = d4
    tree5 = BSTree(d4); update_sizes(tree5.root)

    return tree1, tree2, tree3, tree4, tree5


class Tester(unittest.TestCase):
    def setUp(self):
        self.tree1, self.tree2, self.tree3, self.tree4, self.tree5 = make_trees()

    # --- check_size ---
    def test_check_size(self):

        self.tree1.root.left.left.size = 0
        self.tree2.root.left.size = 2
        self.tree3.root.size = 10
        self.assertFalse(du.check_size(self.tree1))
        self.assertFalse(du.check_size(self.tree2))
        self.assertFalse(du.check_size(self.tree3))
        self.assertTrue(du.check_size(self.tree4))
        self.assertTrue(du.check_size(self.tree5))

        empty = du.BSTree()
        self.assertTrue(du.check_size(empty))
        single = du.BSTree(Node(10))
        self.assertTrue(du.check_size(single))
        bad = du.BSTree(Node(10)); bad.root.size = 999
        self.assertFalse(du.check_size(bad))

    # --- check_3_5_balanced ---
    def test_check_balance(self):
        self.assertFalse(du.check_3_5_balanced(self.tree1))
        self.assertTrue(du.check_3_5_balanced(self.tree2))
        self.assertTrue(du.check_3_5_balanced(self.tree3))
        self.assertFalse(du.check_3_5_balanced(self.tree4))
        self.assertTrue(du.check_3_5_balanced(self.tree5))
        self.assertTrue(du.check_3_5_balanced(du.BSTree()))
        self.assertTrue(du.check_3_5_balanced(du.BSTree(Node(10))))

    # --- insert ---
    def test_insert(self):
        n1 = self.tree1.root.left.left
        n2 = self.tree1.root.left
        n1.parent = None; n2.left = None
        du.insert(self.tree1, 1)
        self.assertEqual(n2.left.key, 1)

        c1 = self.tree4.root.left.left.left
        c2 = self.tree4.root.left.left
        c1.parent, c2.left = None, None
        c8 = self.tree4.root.right.right
        c9 = self.tree4.root.right.right.right
        c8.right = None; c9.parent = None
        du.insert(self.tree4, 1)
        self.assertEqual(c2.left.key, 1)
        du.insert(self.tree4, 9)
        self.assertEqual(c8.right.key, 9)

        t = du.BSTree()
        self.assertIsNone(du.insert(t, 42))
        self.assertIsNotNone(t.root)
        self.assertEqual(t.root.key, 42)

        self.assertIsNone(du.insert(du.BSTree(du.Node(10)), 10))

        n10 = Node(10); n5 = Node(5, parent=n10); n15 = Node(15, parent=n10)
        n10.left, n10.right, n10.size, n5.size, n15.size = n5, n15, 3, 1, 1
        tree = BSTree(n10)
        self.assertIsNone(du.insert(tree, 7))
        self.assertEqual(n5.right.key, 7)
        self.assertEqual(n5.size, 2)
        self.assertEqual(n10.size, 4)

        after(tree1=self.tree1, tree4=self.tree4)

    # --- rebalance ---
    def test_rebalance(self):
        tree = self.tree4
        c3 = tree.root.left; c2 = c3.left; c1 = c2.left
        du.rebalance(tree, c3)
        self.assertTrue(du.check_size(tree))
        self.assertTrue(du.check_3_5_balanced(tree))
        self.assertIs(c2.right, c3)
        self.assertIs(c3.parent, c2)

        c6 = tree.root.right; c8 = c6.right; c7 = c8.left
        du.rebalance(tree, c6)
        self.assertTrue(du.check_3_5_balanced(tree))
        self.assertIs(c7.left, c6)
        self.assertIs(c7.right, c8)
        self.assertIs(c6.parent, c7)

        c5 = tree.root.right.left.left
        du.rebalance(tree, tree.root)
        self.assertTrue(du.check_3_5_balanced(tree))
        self.assertIs(tree.root, c5)

        single = du.BSTree(Node(10))
        du.rebalance(single, single.root)
        self.assertIs(single.root.left, None)
        self.assertIs(single.root.right, None)

        n1 = Node(1); n2 = Node(2, left=n1); n1.parent = n2; n3 = Node(3, left=n2)
        n2.parent = n3; n4 = Node(4, left=n3); n3.parent = n4; n5 = Node(5, left=n4)
        n4.parent = n5; baby = BSTree(root=n5); update_sizes(baby.root); du.rebalance(baby, baby.root)
        self.assertTrue(du.check_size(baby))
        self.assertTrue(du.check_3_5_balanced(baby))

        after(tree4=self.tree4)


before()
if __name__ == '__main__':
    unittest.main()
