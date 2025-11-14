# StudentID_LabX.py
# BSD3513 – Lab Report 1 (Search Algorithms: BFS & DFS)
# Name: NUR AISYAH FAIRUZ BINTI MUHAMAD FERDAUS
# Student ID: SD23036
# Section: 01G

import streamlit as st
from collections import deque
from PIL import Image
import json
from datetime import datetime

st.set_page_config(page_title="BFS & DFS Visualizer", layout="centered")
st.title("🔍 BFS and DFS Graph Traversal Visualizer")
st.markdown("### BSD3513 – Lab Report 1")
st.markdown(f"*Name:* <Your Name> | *Student ID:* <Your ID> | *Section:* <Your Section>")

st.subheader("Graph Reference Image")
st.info("If you have a graph image (e.g., BFS_img1.jpg), place it in the same folder to display here.")
try:
    image = Image.open("BFS_img1.jpg")
    st.image(image, caption="Graph used for BFS and DFS Traversal", use_column_width=True)
except Exception:
    st.warning("Image 'BFS_img1.jpg' not found. Using default graph dictionary below.")

# Default graph (directed). Adjacency lists will be sorted alphabetically when traversing.
default_graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

st.subheader("1️⃣ Graph Input")
st.markdown("You may either use the default graph or upload a JSON file containing adjacency lists (format: { 'A':['B','C'], ... }).")

uploaded = st.file_uploader("Upload graph JSON file (optional)", type=["json"])
if uploaded:
    try:
        graph = json.load(uploaded)
        # ensure lists and sort neighbors for deterministic alphabetical tie-breaking
        graph = {str(k): sorted(list(v)) for k, v in graph.items()}
        st.success("Graph loaded from JSON.")
    except Exception as e:
        st.error("Failed to read JSON file. Using default graph.")
        graph = {k: sorted(v) for k, v in default_graph.items()}
else:
    graph = {k: sorted(v) for k, v in default_graph.items()}

st.json(graph)

# ------------------------------------------------------------
# BFS that returns order + levels
# ------------------------------------------------------------
def bfs_with_levels(graph, start_node):
    visited = set()
    queue = deque()
    level = {start_node: 0}
    order = []
    queue.append(start_node)
    visited.add(start_node)
    while queue:
        node = queue.popleft()
        order.append(node)
        # expand neighbours in alphabetical order (graph already sorted)
        for nb in graph.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                level[nb] = level[node] + 1
    return order, level

# ------------------------------------------------------------
# DFS (recursive) using alphabetical tie-breaking
# ------------------------------------------------------------
def dfs_alpha(graph, start_node, visited=None, order=None):
    if visited is None:
        visited = set()
    if order is None:
        order = []
    visited.add(start_node)
    order.append(start_node)
    for nb in graph.get(start_node, []):
        if nb not in visited:
            dfs_alpha(graph, nb, visited, order)
    return order

# Interface
st.subheader("2️⃣ Choose Traversal")
start_node = st.selectbox("Select Starting Node:", sorted(list(graph.keys())))
algorithm = st.radio("Choose Algorithm:", ["Breadth-First Search (BFS)", "Depth-First Search (DFS)"])
run = st.button("Run Traversal")

if run:
    if algorithm.startswith("Breadth"):
        order, levels = bfs_with_levels(graph, start_node)
        st.success("Traversal Order (BFS): " + " → ".join(order))
        st.markdown("**Levels:**")
        # show nodes grouped by level
        max_level = max(levels.values()) if levels else 0
        for l in range(0, max_level + 1):
            nodes_at_level = [n for n, lev in levels.items() if lev == l]
            st.write(f"Level {l}: " + ", ".join(sorted(nodes_at_level)))
    else:
        order = dfs_alpha(graph, start_node)
        st.success("Traversal Order (DFS): " + " → ".join(order))
        st.markdown("**Note:** DFS does not have explicit 'levels' in the same sense as BFS; it follows depth-first paths.")

    st.markdown("*Visited Nodes Order:*")
    st.code(", ".join(order))

    # Prepare a small report for download
    report = {
        "timestamp": datetime.now().isoformat(),
        "start_node": start_node,
        "algorithm": algorithm,
        "order": order
    }
    if algorithm.startswith("Breadth"):
        report["levels"] = levels

    st.download_button("Download report (JSON)", data=json.dumps(report, indent=2), file_name="traversal_report.json", mime="application/json")

# ------------------------------------------------------------
# Explanation section
# ------------------------------------------------------------
st.markdown("---")
st.subheader("3️⃣ Algorithm Explanation (Short)")
st.markdown("""
**Breadth-First Search (BFS)**  
- Explores all neighbors level by level before moving deeper.  
- Uses a *queue* (FIFO).  
- Produces levels: nodes at distance 0, 1, 2, ... from the start.

**Depth-First Search (DFS)**  
- Explores as far as possible down one branch before backtracking.  
- Can be implemented recursively (stack implicit).  
- Produces a traversal order that follows one path deeply, then backtracks.
""")

st.markdown("### 📘 Complexity Summary")
st.table({
    "Algorithm": ["BFS", "DFS"],
    "Time Complexity": ["O(V + E)", "O(V + E)"],
    "Space Complexity": ["O(V)", "O(V)"]
})
st.markdown("---")
st.caption("Developed with Streamlit for BSD3513 Lab Report 1 – AI Search Algorithms.")
