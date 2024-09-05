from collections import deque


def DFC(dt_model): #dt_model hace referencia al objeto que representa el arbol de decision


    current_node = 0
    discover = deque()
    visited = deque()


    discover.append(current_node)

    while current_node != None:

        r_child = dt_model.tree_.children_right[current_node]
        l_child = dt_model.tree_.children_left[current_node]

        if r_child != l_child:  # no es hoja

            if r_child in visited and l_child in visited:
                visited.append(current_node)
                current_node = visit(current_node, disc = discover, vis = visited )

            else:

                if l_child not in visited:

                    discover.append(l_child)
                    current_node = l_child

                else:

                    discover.append(r_child)
                    current_node = r_child

        else:  # es hoja

            yield list(discover)

            visited.append(current_node)
            current_node = visit(current_node, disc = discover, vis = visited)


def visit(current_node, disc, vis):

    while current_node in vis:

        disc.pop()
        try:
            current_node = disc[-1]

        except:

            return None

    return current_node