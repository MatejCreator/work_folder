import unittest, os, subprocess, shutil
import du10_graph_traversal as du

Vertex = du.Vertex

def before():
    directory = rf"{os.getcwd()}"
    # --- Convertor to WSL directory ---
    drive_letter = directory[0].lower()
    rest = directory[2:]
    if rest.startswith("\\") or rest.startswith("/"):
        rest = rest[1:]
    rest = rest.replace("\\", "/")
    wsl_directory = f"/mnt/{drive_letter}/{rest}"

    if os.path.isdir(directory):
        if any(item.startswith("ib002") and item.endswith(".png") for item in os.listdir(directory)):
            pass
        else:
            graphviz_checker()
            du.draw_example()
            command = f"cd '{wsl_directory}' && dot -Tpng ib002_graph.dot -o ib002_graph.png"
            subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)
            something = os.path.join(directory, "ib002_graph.dot")
            try:
                os.remove(something)
            except FileNotFoundError:
                pass

        if any(item.startswith("Big_Boy") and item.endswith(".png") for item in os.listdir(directory)):
            pass
        else:
            graphviz_checker()
            du.draw_graph(list(maker2().values()), "Big_Boy.dot")
            command = f"cd '{wsl_directory}' && dot -Tpng Big_Boy.dot -o Big_Boy.png"
            subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)
            something = os.path.join(directory, "Big_Boy.dot")
            try:
                os.remove(something)
            except FileNotFoundError:
                pass


def graphviz_checker():
    # --- GraphViz downloader and checker ---
    def have_wsl_launcher() -> str | None:
        return shutil.which("wsl.exe") or shutil.which("wsl")

    def wsl_default_distro_ready() -> bool:
        return subprocess.run(["wsl", "-e", "true"],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL).returncode == 0

    def inside_wsl() -> bool:
        return "WSL_DISTRO_NAME" in os.environ

    def run_in_wsl(cmd, *, root=False, check=True):
        if inside_wsl():
            return subprocess.run(cmd, check=check)
        if not have_wsl_launcher():
            raise RuntimeError("WSL is not installed on this machine.")
        if not wsl_default_distro_ready():
            raise RuntimeError(
                "WSL exists but no distro is installed or it requires `wsl --update`."
            )
        full = ["wsl", "--user", "root"] + ["--"] + cmd if root else ["wsl", "--"] + cmd
        return subprocess.run(full, check=check)

    def has_graphviz() -> bool:
        return run_in_wsl(["sh", "-c", "command -v dot"],
                          check=False).returncode == 0

    def ensure_graphviz():
        if has_graphviz():
            print("✅ Graphviz already installed")
            return
        print("Installing Graphviz…")
        run_in_wsl(
            ["sh", "-c",
             "export DEBIAN_FRONTEND=noninteractive && "
             "(command -v apt-get && apt-get update -qq && "
             "apt-get install -y graphviz) || "
             "(command -v apk && apk add graphviz) || "
             "(command -v dnf && dnf -y install graphviz)"],
            root=True
        )
        if not has_graphviz():
            raise RuntimeError("Graphviz installation failed")

    ensure_graphviz()

def maker1():
    vertices = {name: Vertex(name) for name in ["A", "B", "C", "D", "E", "F", "G"]}
    edges = [
        ("A", "D"),
        ("B", "A"),
        ("B", "E"),
        ("C", "E"),
        ("C", "F"),
        ("C", "G"),
        ("D", "B"),
        ("E", "F"),
        ("E", "G")
    ]
    for src, dst in edges:
        vertices[src].succs.append(vertices[dst])
    return vertices

def maker2():
    vertices = {i: Vertex(f"V{i}") for i in range(0, 18)}
    edges = [
        (0, 4), (0, 7), (7, 0), (14, 7),
        (4, 5), (5, 1), (5, 6), (1, 5),
        (2, 1), (2, 3), (3, 2), (3, 6),
        (6, 10), (10, 9), (9, 10), (9, 5),
        (8, 9), (11, 8), (11, 12),

        (15, 17), (17, 16),
        (17, 13), (13, 16),
    ]
    for src, dst in edges:
        vertices[src].succs.append(vertices[dst])
    return vertices


def maker3():
    vertices = {i: Vertex(f"V{i}") for i in range(100, 106)}
    edges = [
        (100, 102),
        (102, 103),
        (103, 104),
        (104, 105),
        (100, 101),
        (101, 105)
    ]
    for src, dst in edges:
        vertices[src].succs.append(vertices[dst])
    return vertices


class Tester(unittest.TestCase):
    def setUp(self):
        self.vertices1 = maker1()
        self.vertices2 = maker2()
        self.vertices3 = maker3()

    def test_reachable_size1(self):
        self.assertEqual(du.reachable_size(self.vertices1['A']), (6, 6))

        self.setUp()
        self.assertEqual(du.reachable_size(self.vertices1['C']), (4, 5))

        self.setUp()
        self.assertEqual(du.reachable_size(self.vertices1['E']), (3, 2))

        self.setUp()
        self.assertEqual(du.reachable_size(self.vertices2[15]), (4, 4))

        self.setUp()
        self.assertEqual(du.reachable_size(self.vertices2[12]), (1, 0))

        self.setUp()
        self.assertEqual(du.reachable_size(self.vertices2[6]), (5, 7))

    def test_has_cycle(self):
        self.assertTrue(du.has_cycle(self.vertices1['A']))
        self.assertTrue(du.has_cycle(self.vertices1['B']))
        self.assertFalse(du.has_cycle(self.vertices1['C']))
        self.assertFalse(du.has_cycle(self.vertices1['E']))
        self.assertFalse(du.has_cycle(self.vertices1['F']))
        self.assertFalse(du.has_cycle(self.vertices1['G']))

        self.assertTrue(du.has_cycle(self.vertices2[10]))
        self.assertTrue(du.has_cycle(self.vertices2[6]))
        self.assertTrue(du.has_cycle(self.vertices2[11]))
        self.assertFalse(du.has_cycle(self.vertices2[13]))

    def test_is_tree(self):
        self.assertFalse(du.is_tree(self.vertices1['A']))

        self.setUp()
        self.assertFalse(du.is_tree(self.vertices1['C']))

        self.setUp()
        self.assertTrue(du.is_tree(self.vertices1['E']))

        self.setUp()
        self.assertTrue(du.is_tree(self.vertices1['F']))

        self.setUp()
        self.assertFalse(du.is_tree(self.vertices2[15]))

        self.setUp()
        self.assertFalse(du.is_tree(self.vertices2[14]))

    def test_distance(self):
        self.assertEqual(du.distance(self.vertices1["A"], self.vertices1["G"]), 4)

        self.setUp()
        self.assertEqual(du.distance(self.vertices1["C"], self.vertices1["G"]), 1)

        self.setUp()
        self.assertIsNone(du.distance(self.vertices1["E"], self.vertices1["D"]))

        self.setUp()
        self.assertEqual(du.distance(self.vertices2[15], self.vertices2[16]), 2)

        self.setUp()
        self.assertIsNone(du.distance(self.vertices2[4], self.vertices2[14]))

        self.setUp()
        self.assertEqual(du.distance(self.vertices2[3], self.vertices2[5]), 3)

        self.setUp()
        self.assertEqual(du.distance(self.vertices2[14], self.vertices2[9]), 7)

        self.setUp()
        self.assertEqual(du.distance(self.vertices3[100], self.vertices3[105]), 2)

before()
if __name__ == '__main__':
    unittest.main()
