import unittest, os, subprocess, shutil
import du12_paths as du

Graph = du.Graph

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
        if any(item.startswith("example1") and item.endswith(".png") for item in os.listdir(directory)):
            pass
        else:
            graphviz_checker()
            du.draw_graph(example_graph1(), "example1.dot")
            command = f"cd '{wsl_directory}' && dot -Tpng example1.dot -o example1.png"
            subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)
            something = os.path.join(directory, "example1.dot")
            try:
                os.remove(something)
            except FileNotFoundError:
                pass

        if any(item.startswith("example2") and item.endswith(".png") for item in os.listdir(directory)):
            pass
        else:
            graphviz_checker()
            du.draw_graph(example_graph2(), "example2.dot")
            command = f"cd '{wsl_directory}' && dot -Tpng example2.dot -o example2.png"
            subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)
            something = os.path.join(directory, "example2.dot")
            try:
                os.remove(something)
            except FileNotFoundError:
                pass

        if any(item.startswith("example3") and item.endswith(".png") for item in os.listdir(directory)):
            pass
        else:
            graphviz_checker()
            du.draw_graph(example_graph3(), "example3.dot")
            command = f"cd '{wsl_directory}' && dot -Tpng example3.dot -o example3.png"
            subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)
            something = os.path.join(directory, "example3.dot")
            try:
                os.remove(something)
            except FileNotFoundError:
                pass

        if any(item.startswith("example4") and item.endswith(".png") for item in os.listdir(directory)):
            pass
        else:
            graphviz_checker()
            du.draw_graph(example_graph4(), "example4.dot")
            command = f"cd '{wsl_directory}' && dot -Tpng example4.dot -o example4.png"
            subprocess.run(["wsl", "bash", "-c", command], capture_output=True, text=True)
            something = os.path.join(directory, "example4.dot")
            try:
                os.remove(something)
            except FileNotFoundError:
                pass


flag_for_graphviz_print = False
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
            return subprocess.run(cmd, check=check, capture_output=True)
        elif not have_wsl_launcher():
            raise RuntimeError("WSL is not installed on this machine.")
        elif not wsl_default_distro_ready():
            raise RuntimeError(
                "WSL exists but no distro is installed or it requires `wsl --update`."
            )
        full = ["wsl", "--user", "root"] + ["--"] + cmd if root else ["wsl", "--"] + cmd
        return subprocess.run(full, check=check)

    def has_graphviz() -> bool:
        return run_in_wsl(["sh", "-c", "command -v dot"], check=False).returncode == 0

    def ensure_graphviz():
        global flag_for_graphviz_print

        if has_graphviz():
            if not flag_for_graphviz_print:
                print("✅ Graphviz already installed")
                flag_for_graphviz_print = True
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


def example_graph1() -> Graph:
    graph = Graph(5)
    graph.succs[0] = [(3, 1), (4, 3)]
    graph.succs[1] = [(5, 3), (2, 2), (1, 4)]
    graph.succs[2] = [(2, 0)]
    graph.succs[3] = [(2, 2), (1, 4)]
    graph.succs[4] = [(7, 2), (3, 0)]
    return graph

def example_graph2() -> Graph:
    graph = Graph(5)
    graph.succs[0] = [(9, 1), (4, 2)]
    graph.succs[1] = [(-8, 3)]
    graph.succs[2] = [(-2, 3)]
    graph.succs[3] = [(3, 4)]
    # vertex 4 has no successors
    return graph

def example_graph3() -> Graph:
    graph = Graph(10)
    graph.succs[0] = [(5, 1), (7, 2), (21, 8)]
    graph.succs[1] = [(7, 5), (100, 7)]
    graph.succs[2] = [(3, 3), (-5, 1)]
    graph.succs[3] = [(4, 4)]
    graph.succs[4] = [(-9, 2), (100, 5)]
    graph.succs[5] = [(100, 6)]
    # vertex 6 has no successors
    # vertex 7 has no successors
    graph.succs[8] = [(0, 6), (-20, 9)]
    graph.succs[9] = [(0, 0)]
    return graph

def example_graph4() -> Graph:
    graph = Graph(8)
    graph.succs[0] = [(-41, 6), (0, 0)]
    graph.succs[1] = []
    graph.succs[2] = [(0, 1), (0, 6), (0, 4), (0, 5), (5, 7), (-9, 0)]
    graph.succs[3] = []
    graph.succs[4] = []
    graph.succs[5] = []
    graph.succs[6] = [(0, 3), (49, 2)]
    graph.succs[7] = [(0, 6)]
    return graph


class Tester(unittest.TestCase):
    def setUp(self):
        self.graph1 = example_graph1()
        self.graph2 = example_graph2()
        self.graph3 = example_graph3()
        self.graph4 = example_graph4()

    def test_reachable(self):
        # Dijkstra
        self.assertEqual(du.reachable(self.graph1, 0, 1), [0], "First one is wrong already :(")
        self.assertEqual(du.reachable(self.graph1, 0, 2), [0])
        self.assertEqual(du.reachable(self.graph1, 0, 3), [0, 1])
        self.assertEqual(du.reachable(self.graph1, 0, 4), [0, 1, 3, 4], "These are harder now...")
        self.assertEqual(sorted(du.reachable(self.graph1, 0, 5)), [0, 1, 2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 0, 6)), [0, 1, 2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 0, 100)), [0, 1, 2 ,3 ,4])

        self.assertEqual(du.reachable(self.graph1, 3, 1), [3, 4], "OK second graph but still... first assert :(")
        self.assertEqual(sorted(du.reachable(self.graph1, 3, 2)), [2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 3, 3)), [2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 3, 4)), [0, 2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 3, 5)), [0, 2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 3, 6)), [0, 2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 3, 7)), [0, 1, 2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 3, 100)), [0, 1, 2, 3, 4])

        self.assertEqual(sorted(du.reachable(self.graph1, 2, 1)), [2])
        self.assertEqual(sorted(du.reachable(self.graph1, 2, 2)), [0, 2])
        self.assertEqual(sorted(du.reachable(self.graph1, 2, 100)), [0, 1, 2, 3, 4])
        self.assertEqual(sorted(du.reachable(self.graph1, 4, 7)), [0, 1, 2, 3, 4])

    def test_reachable_with_charging(self):
        # Bellman Ford
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 1)), [0])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 2)), [0])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 3)), [0])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 4)), [0, 2, 3])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 5)), [0, 2, 3, 4])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 6)), [0, 2, 3, 4])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 7)), [0, 2, 3, 4])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 8)), [0, 2, 3, 4])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 0, 9)), [0, 1, 2, 3, 4])

        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 3, -2)), [3])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph2, 3, 3)), [3, 4])

        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 1)), [0])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 3)), [0])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 5)), [0, 1])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 7)), [0, 1, 2])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 9)), [0, 1, 2, 5])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 11)), [0, 1, 2, 3, 5])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 13)), [0, 1, 2, 3, 5])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 15)), [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 17)), [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 19)), [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 21)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 0, 1000)), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 6, -10)), [6])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 7, 100)), [7])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph3, 3, 4)), [1, 2, 3, 4, 5, 6, 7], "This is just extra?!")

        self.assertEqual(sorted(du.reachable_with_charging(self.graph4, 2, 1)), [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph4, 0, 0)), [0, 3, 6])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph4, 7, 0)), [3, 6, 7])
        self.assertEqual(sorted(du.reachable_with_charging(self.graph4, 0, 8)), [0, 1, 2, 3, 4, 5, 6, 7])


before()
if __name__ == '__main__':
    unittest.main()
