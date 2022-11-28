def enumerate_cells(cells):
    """
    Enumerate the cells in the grid
    :param cells: The cells we want to use on all belts. To
    :return:
    """
    cell_list = []
    for r in range(3):
        for c in cells:
            cell_list.append([r, c])
    cells_dictionary = {cell_n: cell_list[cell_n] for cell_n in range(len(cell_list))}
    return cells_dictionary
