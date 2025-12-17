from langgraph.graph import StateGraph

def build_payroll_graph():
    graph = StateGraph(dict)

    graph.add_node("validate", lambda state: state)
    graph.add_node("anomaly", lambda state: state)
    graph.add_node("explain", lambda state: state)

    graph.set_entry_point("validate")
    graph.add_edge("validate", "anomaly")
    graph.add_edge("anomaly", "explain")

    return graph.compile()
