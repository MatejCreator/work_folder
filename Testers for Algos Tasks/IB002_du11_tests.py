import unittest, os, subprocess, shutil
import du11_graph_components as du

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

def example_graph1() -> Graph:
    graph = Graph(10)
    graph.succs[0] = [2, 3, 6]
    graph.succs[1] = [4, 8]
    graph.succs[2] = [5]
    graph.succs[3] = [7, 8]
    graph.succs[4] = [8]
    graph.succs[5] = [6]
    graph.succs[6] = [2]
    graph.succs[7] = [6, 9]
    graph.succs[8] = [0]
    graph.succs[9] = [7]
    return graph

def example_graph2() -> Graph:
    graph = Graph(8)
    graph.succs[0] = [5, 1, 4]
    graph.succs[1] = [0, 6]
    graph.succs[2] = [7, 2]
    graph.succs[3] = [7]
    # vertex 4 has no successors
    graph.succs[5] = [5]
    graph.succs[6] = [7]
    graph.succs[7] = [6]
    return graph

class Tester(unittest.TestCase):
    def setUp(self):
        self.graph1 = example_graph1()
        self.graph2 = example_graph2()

    def test_strongly_connected_components(self):
        self.assertIn(du.strongly_connected_components(self.graph1), ([[1], [4], [0, 8, 3], [7, 9], [2, 6, 5]], [[1], [4], [0, 3, 8], [7, 9], [2, 5, 6]]))
        self.assertIn(du.strongly_connected_components(self.graph2), ([[0, 1], [2], [3], [4], [5], [6, 7]], [[3], [2], [0, 1], [4], [6, 7], [5]]))

    def test_terminal_sccs(self):
        self.assertIn(du.terminal_sccs(self.graph1), ( [[2, 5, 6]], [[2, 6, 5]] ))
        self.assertIn(du.terminal_sccs(self.graph2), ( [[4], [5], [6, 7]], [[4], [6, 7], [5]] ))

    def test_initial_sccs(self):
        self.assertIn(du.initial_sccs(self.graph1), ( [[1]], ))
        self.assertIn(du.initial_sccs(self.graph2), ( [[0, 1], [2], [3]], [[3], [2], [0, 1]] ))


before()
if __name__ == '__main__':
    unittest.main()
